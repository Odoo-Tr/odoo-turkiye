from datetime import date

from odoo.exceptions import UserError
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install_l10n", "post_install", "-at_install")
class TestFxRevaluation(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref="l10n_tr.chart_template_7a"):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.company = cls.company_data["company"]
        cls.l10n_tr_taxes = {}
        tax_group = cls.env["account.tax.group"].create({"name": "KDV"})
        vat_accounts = {
            use: cls.env["account.account"].create({"name": name, "code": code, "account_type": kind, "company_id": cls.company.id})
            for use, name, code, kind in [("sale", "Hesaplanan KDV", "391900", "liability_current"),
                                          ("purchase", "İndirilecek KDV", "191900", "asset_current")]
        }
        def repartition(account):
            return [(0, 0, {"repartition_type": "base", "factor_percent": 100}),
                    (0, 0, {"repartition_type": "tax", "factor_percent": 100, "account_id": account.id})]
        for key, name, use, amount in [("tr_s_20", "KDV %20", "sale", 20), ("tr_p_20", "KDV %20", "purchase", 20),
                                       ("tr_s_10", "KDV %10", "sale", 10), ("tr_p_10", "KDV %10", "purchase", 10)]:
            cls.l10n_tr_taxes[key] = cls.env["account.tax"].create({
                "name": f"{name} ({use})", "type_tax_use": use, "amount": amount, "amount_type": "percent",
                "company_id": cls.company.id, "tax_group_id": tax_group.id,
                "invoice_repartition_line_ids": repartition(vat_accounts[use]),
                "refund_repartition_line_ids": repartition(vat_accounts[use])})
        withholding = cls.env["account.tax"].create({
            "name": "KDV tevkifat 5/10", "type_tax_use": "none", "amount": -10, "amount_type": "percent",
            "company_id": cls.company.id, "tax_group_id": tax_group.id})
        cls.l10n_tr_taxes["tr_s_wh_20_5_10"] = cls.env["account.tax"].create({
            "name": "KDV %20 tevkifat 5/10", "type_tax_use": "sale", "amount_type": "group", "amount": 0,
            "company_id": cls.company.id, "tax_group_id": tax_group.id,
            "children_tax_ids": [(6, 0, (cls.l10n_tr_taxes["tr_s_20"] | withholding).ids)]})
        cls.usd = cls.env.ref("base.USD")
        cls.usd.active = True
        cls.env["res.currency.rate"].search([("currency_id", "=", cls.usd.id)]).unlink()
        # TRY per USD, dated the day before use: Odoo 20 applies a rate from the day after its date
        for day, try_per_usd in [("2026-08-31", 30), ("2026-09-29", 33), ("2026-10-14", 35)]:
            cls.env["res.currency.rate"].create({"name": day, "currency_id": cls.usd.id, "company_id": cls.company.id, "rate": 1 / try_per_usd})
        cls.gain = cls.company.income_currency_exchange_account_id
        cls.loss = cls.company.expense_currency_exchange_account_id

    def _ref(self, xmlid):
        return self.l10n_tr_taxes.get(xmlid) or self.env.ref(f"account.{self.company.id}_{xmlid}")

    def _invoice(self, move_type, price, taxes):
        move = self.env["account.move"].create({
            "move_type": move_type, "partner_id": self.partner_a.id, "currency_id": self.usd.id, "invoice_date": "2026-09-01",
            "invoice_line_ids": [(0, 0, {"name": "Hizmet", "quantity": 1, "price_unit": price, "tax_ids": [(6, 0, taxes.ids)]})],
        })
        move.action_post()
        return move

    def _revalue(self, day="2026-09-30", **vals):
        wizard = self.env["l10n_tr.fx.revaluation.wizard"].with_company(self.company).create({"date": day, "journal_id": self.company_data["default_journal_misc"].id, **vals})
        action = wizard.action_revalue()
        return self.env["account.move"].browse(action["domain"][0][2]).sorted("date")

    def _balance(self, moves, account):
        return sum(moves.line_ids.filtered(lambda l: l.account_id == account).mapped("balance"))

    def test_receivable_and_payable(self):
        """1.200 USD receivable and 600 USD payable booked at 30, revalued at 33."""
        invoice = self._invoice("out_invoice", 1000, self._ref("tr_s_20"))
        self._invoice("in_invoice", 500, self._ref("tr_p_20"))
        revaluation, reversal = self._revalue()
        self.assertEqual(revaluation.date, date(2026, 9, 30))
        self.assertEqual(reversal.date, date(2026, 10, 1))
        receivable = invoice.line_ids.filtered(lambda l: l.display_type == "payment_term").account_id
        self.assertEqual(self._balance(revaluation, receivable), 3600)
        self.assertEqual(self._balance(revaluation, self.gain), -3600)
        self.assertEqual(self._balance(revaluation, self.loss), 1800)
        self.assertEqual(self._balance(reversal, self.gain), 3600)
        # The open invoice keeps its booked amount once the reversal is reconciled
        self.assertFalse(invoice.line_ids.filtered(lambda l: l.display_type == "payment_term").reconciled)
        self.assertTrue(all(l.reconciled for l in revaluation.line_ids if l.account_id.reconcile))

    def test_payment_after_the_date(self):
        """A payment made after the revaluation date does not reduce the amount revalued."""
        invoice = self._invoice("out_invoice", 1000, self._ref("tr_s_20"))
        self.env["account.payment.register"].with_context(active_model="account.move", active_ids=invoice.ids).create(
            {"payment_date": "2026-10-20", "currency_id": self.usd.id, "amount": 1200})._create_payments()
        revaluation, _reversal = self._revalue(include_liquidity=False)
        self.assertEqual(self._balance(revaluation, self.gain), -3600)

    def test_paid_before_the_date_is_skipped(self):
        invoice = self._invoice("out_invoice", 1000, self._ref("tr_s_20"))
        self.env["account.payment.register"].with_context(active_model="account.move", active_ids=invoice.ids).create(
            {"payment_date": "2026-09-15", "currency_id": self.usd.id, "amount": 1200})._create_payments()
        with self.assertRaises(UserError):
            self._revalue(include_liquidity=False)

    def test_bank_account(self):
        journal = self.env["account.journal"].create({"name": "USD Banka", "type": "bank", "code": "USDB", "currency_id": self.usd.id, "company_id": self.company.id})
        move = self.env["account.move"].create({"move_type": "entry", "date": "2026-09-01", "journal_id": self.company_data["default_journal_misc"].id, "line_ids": [
            (0, 0, {"account_id": journal.default_account_id.id, "currency_id": self.usd.id, "amount_currency": 1000, "balance": 30000}),
            (0, 0, {"account_id": self.company_data["default_account_revenue"].id, "balance": -30000}),
        ]})
        move.action_post()
        revaluation, _reversal = self._revalue(include_partners=False, reverse=True)
        self.assertEqual(self._balance(revaluation, journal.default_account_id), 3000)
        self.assertEqual(self._balance(revaluation, self.gain), -3000)

    def test_without_reversal(self):
        self._invoice("out_invoice", 1000, self._ref("tr_s_20"))
        moves = self._revalue(reverse=False, include_liquidity=False)
        self.assertEqual(len(moves), 1)
