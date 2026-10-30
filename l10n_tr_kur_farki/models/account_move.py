from collections import defaultdict

from odoo import Command, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class AccountMove(models.Model):
    _inherit = "account.move"

    # On the exchange difference invoice
    l10n_tr_kur_farki_origin_id = fields.Many2one(
        "account.move",
        string="Exchange Difference Of",
        readonly=True,
        copy=False,
        index="btree_not_null",
    )
    l10n_tr_kur_farki_exchange_move_ids = fields.Many2many(
        "account.move",
        "l10n_tr_kur_farki_exchange_move_rel",
        "invoice_id",
        "exchange_move_id",
        string="Invoiced Exchange Difference Entries",
        readonly=True,
        copy=False,
    )
    l10n_tr_kur_farki_offset_move_id = fields.Many2one(
        "account.move", string="Exchange Difference Offset", readonly=True, copy=False
    )
    # On the foreign currency invoice
    l10n_tr_kur_farki_ids = fields.One2many(
        "account.move", "l10n_tr_kur_farki_origin_id", string="Exchange Difference Invoices"
    )
    l10n_tr_kur_farki_count = fields.Integer(
        string="Exchange Difference Invoice Count", compute="_compute_l10n_tr_kur_farki_count"
    )
    l10n_tr_kur_farki_pending = fields.Monetary(
        string="Exchange Difference to Invoice",
        compute="_compute_l10n_tr_kur_farki_pending",
        currency_field="company_currency_id",
        help="Realized exchange difference of the payments of this invoice that no exchange "
        "difference invoice covers yet. Positive: in our favour.",
    )
    l10n_tr_kur_farki_pending_abs = fields.Monetary(
        string="Exchange Difference Amount",
        compute="_compute_l10n_tr_kur_farki_pending",
        currency_field="company_currency_id",
    )

    @api.depends("l10n_tr_kur_farki_ids")
    def _compute_l10n_tr_kur_farki_count(self):
        for move in self:
            move.l10n_tr_kur_farki_count = len(move.l10n_tr_kur_farki_ids)

    @api.depends(
        "state",
        "line_ids.matched_debit_ids",
        "line_ids.matched_credit_ids",
        "l10n_tr_kur_farki_ids.state",
    )
    def _compute_l10n_tr_kur_farki_pending(self):
        for move in self:
            pending = 0.0
            if move._l10n_tr_kur_farki_applicable():
                pending = sum(move._l10n_tr_kur_farki_exchange_lines().mapped("balance"))
            move.l10n_tr_kur_farki_pending = move.company_currency_id.round(pending)
            move.l10n_tr_kur_farki_pending_abs = abs(move.l10n_tr_kur_farki_pending)

    def _l10n_tr_kur_farki_applicable(self):
        self.ensure_one()
        return (
            self.state == "posted"
            and self.move_type in ("out_invoice", "in_invoice")
            and self.currency_id != self.company_currency_id
        )

    def _l10n_tr_kur_farki_exchange_lines(self):
        """Receivable/payable lines of the realized exchange difference entries of this invoice's
        payments that are not covered by an exchange difference invoice yet.

        A positive balance means the difference is in our favour: we received more, or paid less,
        in company currency than the invoice was booked at.
        """
        self.ensure_one()
        term_lines = self.line_ids.filtered(lambda line: line.display_type == "payment_term")
        partials = term_lines.matched_debit_ids | term_lines.matched_credit_ids
        exchange_moves = partials.exchange_move_id
        if "exchange_move_id" in self.env["account.full.reconcile"]._fields:  # Odoo 18
            exchange_moves |= term_lines.full_reconcile_id.exchange_move_id
        covered = self.l10n_tr_kur_farki_ids.filtered(lambda m: m.state != "cancel")
        exchange_moves = (exchange_moves - covered.l10n_tr_kur_farki_exchange_move_ids).filtered(
            lambda m: m.state == "posted"
        )
        return exchange_moves.line_ids.filtered(lambda line: line.account_id in term_lines.account_id)

    def _l10n_tr_kur_farki_payment_date(self, exchange_moves):
        """Date of the payments behind these exchange difference entries. Odoo may date the entries
        themselves later (lock dates, journal sequence); the invoice belongs to the payment date."""
        self.ensure_one()
        term_lines = self.line_ids.filtered(lambda line: line.display_type == "payment_term")
        partials = (term_lines.matched_debit_ids | term_lines.matched_credit_ids).filtered(
            lambda p: p.exchange_move_id in exchange_moves
        )
        payment_lines = (partials.debit_move_id | partials.credit_move_id) - term_lines
        return max(payment_lines.mapped("date") or exchange_moves.mapped("date"))

    def _l10n_tr_kur_farki_tax(self, tax, tax_use):
        """Tax of the same rate for the exchange difference invoice, which may be on the other side."""
        if tax.type_tax_use == tax_use and not tax.price_include:
            return tax
        Tax = self.env["account.tax"]
        candidates = Tax.search(
            [
                *Tax._check_company_domain(self.company_id),
                ("type_tax_use", "=", tax_use),
                ("amount_type", "=", "percent"),
            ]
        ).filtered(lambda t: not t.price_include and float_compare(t.amount, tax.amount, precision_digits=4) == 0)
        candidates = candidates.sorted(lambda t: (t.tax_group_id != tax.tax_group_id, t.sequence, t.id))
        if not candidates:
            raise UserError(
                self.env._(
                    "No %(type)s tax at %(rate)s%% was found for the exchange difference invoice of %(invoice)s.",
                    type=dict(Tax._fields["type_tax_use"].selection)[tax_use],
                    rate=tax.amount,
                    invoice=self.name,
                )
            )
        return candidates[0]

    def _l10n_tr_kur_farki_invoice_vals(self):
        self.ensure_one()
        if not self._l10n_tr_kur_farki_applicable():
            raise UserError(
                self.env._("%s is not a posted invoice in a foreign currency.", self.display_name)
            )
        exchange_lines = self._l10n_tr_kur_farki_exchange_lines()
        currency = self.company_currency_id
        amount = currency.round(sum(exchange_lines.mapped("balance")))
        if currency.is_zero(amount):
            raise UserError(self.env._("%s has no exchange difference left to invoice.", self.display_name))

        # The party in whose favour the difference is issues the invoice: we do when it is ours,
        # otherwise we record the invoice the customer or vendor sends us.
        in_our_favour = amount > 0
        tax_use = "sale" if in_our_favour else "purchase"
        company = self.company_id
        account = (
            company.income_currency_exchange_account_id
            if in_our_favour
            else company.expense_currency_exchange_account_id
        )

        totals = defaultdict(float)
        for line in self.invoice_line_ids.filtered(lambda line: line.display_type == "product"):
            for tax in line.tax_ids:
                if tax.amount_type != "percent" or tax.amount < 0:
                    raise UserError(
                        self.env._(
                            "%(invoice)s uses %(tax)s. Exchange difference invoices are only created "
                            "for invoices with plain VAT rates; create this one manually.",
                            invoice=self.display_name,
                            tax=tax.name,
                        )
                    )
            totals[line.tax_ids] += line.price_total
        grand_total = sum(totals.values())
        if self.currency_id.is_zero(grand_total):
            raise UserError(self.env._("%s has no amount to split the exchange difference on.", self.display_name))

        # The difference includes VAT (iç yüzde): split it by VAT rate in proportion to the invoice,
        # then take the VAT out of each part.
        lines = []
        remaining = abs(amount)
        groups = list(totals.items())
        for index, (taxes, total) in enumerate(groups):
            part = remaining if index == len(groups) - 1 else currency.round(abs(amount) * total / grand_total)
            remaining -= part
            rate = sum(taxes.mapped("amount"))
            new_taxes = self.env["account.tax"]
            for tax in taxes:
                new_taxes |= self._l10n_tr_kur_farki_tax(tax, tax_use)
            lines.append(
                Command.create(
                    {
                        "name": self.env._(
                            "Exchange difference: %(invoice)s (%(rate)s%% VAT)",
                            invoice=self.name,
                            rate=f"{rate:g}",
                        ),
                        "quantity": 1,
                        "price_unit": currency.round(part / (1 + rate / 100)),
                        "account_id": account.id,
                        "tax_ids": [Command.set(new_taxes.ids)],
                    }
                )
            )

        return {
            "move_type": "out_invoice" if in_our_favour else "in_invoice",
            "partner_id": self.partner_id.id,
            "currency_id": currency.id,
            "invoice_date": self._l10n_tr_kur_farki_payment_date(exchange_lines.move_id),
            "invoice_origin": self.name,
            "l10n_tr_kur_farki_origin_id": self.id,
            "l10n_tr_kur_farki_exchange_move_ids": [Command.set(exchange_lines.move_id.ids)],
            "invoice_line_ids": lines,
        }

    def action_l10n_tr_create_kur_farki(self):
        if not self:
            raise UserError(self.env._("None of the selected invoices has an exchange difference left to invoice."))
        created = self.env["account.move"]
        for invoice in self:
            move = self.env["account.move"].with_company(invoice.company_id).create(
                invoice._l10n_tr_kur_farki_invoice_vals()
            )
            invoice.message_post(
                body=self.env._("Exchange difference invoice %s created.", move._get_html_link())
            )
            created |= move
        return created._l10n_tr_kur_farki_action()

    def action_l10n_tr_view_kur_farki(self):
        self.ensure_one()
        return self.l10n_tr_kur_farki_ids._l10n_tr_kur_farki_action()

    def action_l10n_tr_view_kur_farki_origin(self):
        self.ensure_one()
        return self.l10n_tr_kur_farki_origin_id._get_records_action()

    def _l10n_tr_kur_farki_action(self):
        action = {
            "type": "ir.actions.act_window",
            "name": self.env._("Exchange Difference Invoices"),
            "res_model": "account.move",
            "context": {"create": False},
        }
        if len(self) == 1:
            action.update({"view_mode": "form", "res_id": self.id, "views": [(False, "form")]})
        else:
            action.update({"view_mode": "list,form", "domain": [("id", "in", self.ids)], "views": [(False, "list"), (False, "form")]})
        return action

    def _post(self, soft=True):
        posted = super()._post(soft=soft)
        for move in posted.filtered(lambda m: m.l10n_tr_kur_farki_origin_id and not m.l10n_tr_kur_farki_offset_move_id):
            move._l10n_tr_kur_farki_create_offset()
        return posted

    def _l10n_tr_kur_farki_create_offset(self):
        """The difference was already received or paid with the original payment, so close the
        invoice against the exchange difference account Odoo booked it on. What remains is the
        VAT moved out of that account."""
        self.ensure_one()
        term_lines = self.line_ids.filtered(lambda line: line.display_type == "payment_term")
        term_account = term_lines.account_id
        if len(term_account) != 1:
            raise UserError(self.env._("%s must use a single receivable or payable account.", self.display_name))
        company = self.company_id
        exchange_account = (
            company.income_currency_exchange_account_id
            if self.move_type == "out_invoice"
            else company.expense_currency_exchange_account_id
        )
        journal = company.currency_exchange_journal_id or self.env["account.journal"].search(
            [*self.env["account.journal"]._check_company_domain(company), ("type", "=", "general")], limit=1
        )
        balance = sum(term_lines.mapped("balance"))
        label = self.env._("Exchange difference invoice %s", self.name)
        offset = self.env["account.move"].create(
            {
                "move_type": "entry",
                "journal_id": journal.id,
                "date": self.date,
                "ref": label,
                "line_ids": [
                    Command.create(
                        {
                            "name": label,
                            "account_id": term_account.id,
                            "partner_id": self.commercial_partner_id.id,
                            "balance": -balance,
                        }
                    ),
                    Command.create({"name": label, "account_id": exchange_account.id, "balance": balance}),
                ],
            }
        )
        offset._post(soft=False)
        (term_lines | offset.line_ids.filtered(lambda line: line.account_id == term_account)).reconcile()
        self.l10n_tr_kur_farki_offset_move_id = offset

    def button_draft(self):
        res = super().button_draft()
        for move in self.filtered("l10n_tr_kur_farki_offset_move_id"):
            offset = move.l10n_tr_kur_farki_offset_move_id
            offset.line_ids.remove_move_reconcile()
            offset._reverse_moves(cancel=True)
            move.l10n_tr_kur_farki_offset_move_id = False
        return res
