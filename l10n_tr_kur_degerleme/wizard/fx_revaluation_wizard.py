from collections import defaultdict

from dateutil.relativedelta import relativedelta

from odoo import Command, api, fields, models
from odoo.exceptions import UserError


class L10nTrFxRevaluationWizard(models.TransientModel):
    """Period-end revaluation of foreign currency items (VUK madde 280).

    Each open receivable/payable and each foreign currency bank or cash balance is valued at the
    company's rate on the revaluation date; the difference goes to the exchange gain or loss
    account. Tax rules use the TCMB forex buying rate of the bulletin published before that date,
    which is what the TCMB Exchange Rates module stores with its next-day rule.
    """

    _name = "l10n_tr.fx.revaluation.wizard"
    _description = "Foreign Currency Revaluation"

    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company)
    date = fields.Date(string="Revaluation Date", required=True, default=lambda self: self._default_date())
    journal_id = fields.Many2one(
        "account.journal",
        required=True,
        domain="[('type', '=', 'general'), ('company_id', '=', company_id)]",
        default=lambda self: self.env.company.currency_exchange_journal_id,
    )
    include_partners = fields.Boolean(string="Receivables and payables", default=True)
    include_liquidity = fields.Boolean(string="Bank and cash accounts", default=True)
    reverse = fields.Boolean(
        string="Reverse on the next day",
        default=True,
        help="Post the opposite entry on the next day so that the open items keep their invoice rates.",
    )

    @api.model
    def _default_date(self):
        return fields.Date.context_today(self).replace(day=1) - relativedelta(days=1)

    # -- Computation ---------------------------------------------------------------------------

    def _open_partner_lines(self):
        company = self.company_id
        return self.env["account.move.line"].search(
            [
                ("company_id", "=", company.id),
                ("parent_state", "=", "posted"),
                ("date", "<=", self.date),
                ("account_id.account_type", "in", ("asset_receivable", "liability_payable")),
                ("currency_id", "!=", company.currency_id.id),
                ("reconciled", "=", False),
            ]
        ) | self._lines_reconciled_after_date()

    def _lines_reconciled_after_date(self):
        """Lines fully reconciled now but still open on the revaluation date."""
        partials = self.env["account.partial.reconcile"].search(
            [("company_id", "=", self.company_id.id), ("max_date", ">", self.date)]
        )
        lines = partials.debit_move_id | partials.credit_move_id
        return lines.filtered(
            lambda line: line.date <= self.date
            and line.parent_state == "posted"
            and line.account_id.account_type in ("asset_receivable", "liability_payable")
            and line.currency_id != self.company_id.currency_id
        )

    def _residual_on_date(self, line):
        """(foreign amount, company amount) still open on the revaluation date."""
        amount_currency, balance = line.amount_residual_currency, line.amount_residual
        for partial in line.matched_credit_ids.filtered(lambda p: p.max_date > self.date):
            amount_currency += partial.debit_amount_currency
            balance += partial.amount
        for partial in line.matched_debit_ids.filtered(lambda p: p.max_date > self.date):
            amount_currency -= partial.credit_amount_currency
            balance -= partial.amount
        return amount_currency, balance

    def _liquidity_accounts(self):
        journals = self.env["account.journal"].search(
            [("company_id", "=", self.company_id.id), ("type", "in", ("bank", "cash")), ("currency_id", "!=", False)]
        ).filtered(lambda j: j.currency_id != self.company_id.currency_id)
        return {journal.default_account_id: journal.currency_id for journal in journals if journal.default_account_id}

    def _revaluation_items(self):
        """[(account, partner, currency, foreign amount, booked company amount, revalued company amount)]"""
        company, currency = self.company_id, self.company_id.currency_id
        groups = defaultdict(lambda: [0.0, 0.0])
        if self.include_partners:
            for line in self._open_partner_lines():
                amount_currency, balance = self._residual_on_date(line)
                key = (line.account_id, line.partner_id, line.currency_id)
                groups[key][0] += amount_currency
                groups[key][1] += balance
        if self.include_liquidity:
            for account, foreign in self._liquidity_accounts().items():
                lines = self.env["account.move.line"].search(
                    [("account_id", "=", account.id), ("parent_state", "=", "posted"), ("date", "<=", self.date)]
                )
                key = (account, self.env["res.partner"], foreign)
                groups[key][0] += sum(lines.mapped("amount_currency"))
                groups[key][1] += sum(lines.mapped("balance"))
        items = []
        for (account, partner, foreign), (amount_currency, balance) in groups.items():
            revalued = foreign._convert(amount_currency, currency, company, self.date)
            if not currency.is_zero(revalued - balance):
                items.append((account, partner, foreign, amount_currency, balance, revalued))
        return items

    # -- Entry ---------------------------------------------------------------------------------

    def action_revalue(self):
        self.ensure_one()
        company = self.company_id
        gain_account = company.income_currency_exchange_account_id
        loss_account = company.expense_currency_exchange_account_id
        if not (gain_account and loss_account):
            raise UserError(self.env._("Set the exchange gain and loss accounts in the accounting settings first."))
        items = self._revaluation_items()
        if not items:
            raise UserError(self.env._("Nothing to revalue on %s.", self.date))

        label = self.env._("Foreign currency revaluation %s", self.date)
        line_vals, gain, loss = [], 0.0, 0.0
        for account, partner, foreign, amount_currency, balance, revalued in items:
            diff = company.currency_id.round(revalued - balance)
            line_vals.append(
                Command.create(
                    {
                        "name": f"{label} ({foreign.name} {amount_currency:,.2f})",
                        "account_id": account.id,
                        "partner_id": partner.id,
                        "currency_id": foreign.id,
                        "amount_currency": 0.0,
                        "balance": diff,
                    }
                )
            )
            if diff > 0:
                gain += diff
            else:
                loss -= diff
        if gain:
            line_vals.append(Command.create({"name": label, "account_id": gain_account.id, "balance": -gain}))
        if loss:
            line_vals.append(Command.create({"name": label, "account_id": loss_account.id, "balance": loss}))

        move = self.env["account.move"].create(
            {"move_type": "entry", "journal_id": self.journal_id.id, "date": self.date, "ref": label, "line_ids": line_vals}
        )
        move.action_post()
        moves = move
        if self.reverse:
            reversal = move._reverse_moves(
                [{"date": self.date + relativedelta(days=1), "ref": self.env._("Reversal of %s", label)}]
            )
            reversal.action_post()
            # Recent versions reconcile the reversal themselves; earlier ones do not
            for line in move.line_ids.filtered(lambda l: l.account_id.reconcile and not l.reconciled):
                counterpart = reversal.line_ids.filtered(
                    lambda l, line=line: l.account_id == line.account_id and l.partner_id == line.partner_id
                    and l.currency_id == line.currency_id and not l.reconciled
                )[:1]
                (line | counterpart).reconcile()
            moves |= reversal
        return {
            "type": "ir.actions.act_window",
            "name": label,
            "res_model": "account.move",
            "view_mode": "list,form",
            "domain": [("id", "in", moves.ids)],
        }
