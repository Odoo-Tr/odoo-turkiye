from odoo.exceptions import UserError
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install_l10n", "post_install", "-at_install")
class TestKurFarki(AccountTestInvoicingCommon):
    @classmethod
    @AccountTestInvoicingCommon.setup_country("tr")
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.company_data["company"]
        cls.usd = cls.env.ref("base.USD")
        cls.usd.active = True
        cls.env["res.currency.rate"].search([("currency_id", "=", cls.usd.id)]).unlink()
        # TRY per USD, dated the day before the invoice and payments that use it: Odoo 20 applies a
        # rate from the day after its date, earlier versions from its date
        for day, try_per_usd in [("2026-08-31", 30), ("2026-09-30", 33), ("2026-10-14", 27), ("2026-10-19", 35)]:
            cls.env["res.currency.rate"].create(
                {"name": day, "currency_id": cls.usd.id, "company_id": cls.company.id, "rate": 1 / try_per_usd}
            )
        cls.gain = cls.company.income_currency_exchange_account_id
        cls.loss = cls.company.expense_currency_exchange_account_id

    def _ref(self, xmlid):
        return self.env.ref(f"account.{self.company.id}_{xmlid}")

    def _invoice(self, move_type, lines, date="2026-09-01"):
        move = self.env["account.move"].create(
            {
                "move_type": move_type,
                "partner_id": self.partner_a.id,
                "currency_id": self.usd.id,
                "invoice_date": date,
                "invoice_line_ids": [
                    (0, 0, {"name": "Hizmet", "quantity": 1, "price_unit": price, "tax_ids": [(6, 0, taxes.ids)]})
                    for price, taxes in lines
                ],
            }
        )
        move.action_post()
        return move

    def _pay(self, move, date, amount=None):
        self.env["account.payment.register"].with_context(active_model="account.move", active_ids=move.ids).create(
            {"payment_date": date, "currency_id": self.usd.id, "amount": amount or move.amount_residual}
        )._create_payments()

    def _balance(self, account, moves):
        return sum(moves.line_ids.filtered(lambda line: line.account_id == account).mapped("balance"))

    def test_customer_invoice_in_our_favour(self):
        """1.000 USD + 20% VAT booked at 30, collected at 33: 3.600 TRY difference, VAT 600 inside it."""
        invoice = self._invoice("out_invoice", [(1000, self._ref("tr_s_20"))])
        self._pay(invoice, "2026-10-01")
        self.assertEqual(invoice.l10n_tr_kur_farki_pending, 3600)

        kur_farki = self.env["account.move"].browse(invoice.action_l10n_tr_create_kur_farki()["res_id"])
        self.assertEqual(kur_farki.move_type, "out_invoice")
        self.assertEqual(kur_farki.currency_id, self.company.currency_id)
        self.assertEqual(kur_farki.l10n_tr_kur_farki_origin_id, invoice)
        self.assertEqual(str(kur_farki.invoice_date), "2026-10-01", "Dated on the payment, not on the exchange entry")
        self.assertEqual(kur_farki.invoice_line_ids.tax_ids, self._ref("tr_s_20"))
        self.assertEqual(kur_farki.invoice_line_ids.account_id, self.gain)
        self.assertEqual((kur_farki.amount_untaxed, kur_farki.amount_tax, kur_farki.amount_total), (3000, 600, 3600))
        self.assertEqual(invoice.l10n_tr_kur_farki_pending, 0)
        with self.assertRaises(UserError):
            invoice.action_l10n_tr_create_kur_farki()

        kur_farki.action_post()
        self.assertIn(kur_farki.payment_state, ("paid", "in_payment"))
        moves = self.env["account.move"].search([("company_id", "=", self.company.id), ("state", "=", "posted")])
        # Odoo booked 3.600 on the gain account; the invoice leaves 3.000 there and 600 as VAT
        self.assertEqual(self._balance(self.gain, moves), -3000)
        self.assertEqual(self._balance(kur_farki.line_ids.tax_line_id.invoice_repartition_line_ids.account_id, kur_farki), -600)

    def test_customer_invoice_in_customer_favour(self):
        """Collected at 27: the customer invoices us 3.600 TRY, VAT 600 deductible."""
        invoice = self._invoice("out_invoice", [(1000, self._ref("tr_s_20"))])
        self._pay(invoice, "2026-10-15")
        self.assertEqual(invoice.l10n_tr_kur_farki_pending, -3600)
        kur_farki = self.env["account.move"].browse(invoice.action_l10n_tr_create_kur_farki()["res_id"])
        self.assertEqual(kur_farki.move_type, "in_invoice")
        self.assertEqual(kur_farki.partner_id, self.partner_a)
        self.assertEqual(kur_farki.invoice_line_ids.tax_ids, self._ref("tr_p_20"))
        self.assertEqual(kur_farki.invoice_line_ids.account_id, self.loss)
        self.assertEqual((kur_farki.amount_untaxed, kur_farki.amount_total), (3000, 3600))
        kur_farki.action_post()
        moves = self.env["account.move"].search([("company_id", "=", self.company.id), ("state", "=", "posted")])
        self.assertEqual(self._balance(self.loss, moves), 3000)

    def test_vendor_bill(self):
        """A bill paid at 33 cost us more: the vendor invoices the difference. Paid at 27: we do."""
        bill = self._invoice("in_invoice", [(1000, self._ref("tr_p_20"))])
        self._pay(bill, "2026-10-01")
        self.assertEqual(bill.l10n_tr_kur_farki_pending, -3600)
        kur_farki = self.env["account.move"].browse(bill.action_l10n_tr_create_kur_farki()["res_id"])
        self.assertEqual((kur_farki.move_type, kur_farki.invoice_line_ids.tax_ids), ("in_invoice", self._ref("tr_p_20")))

        bill = self._invoice("in_invoice", [(1000, self._ref("tr_p_20"))])
        self._pay(bill, "2026-10-15")
        kur_farki = self.env["account.move"].browse(bill.action_l10n_tr_create_kur_farki()["res_id"])
        self.assertEqual((kur_farki.move_type, kur_farki.invoice_line_ids.tax_ids), ("out_invoice", self._ref("tr_s_20")))
        self.assertEqual(kur_farki.amount_total, 3600)

    def test_mixed_rates(self):
        """1.200 USD at 20% and 550 USD at 10% collected 3 TRY higher: 3.600 and 1.650 TRY parts."""
        invoice = self._invoice("out_invoice", [(1000, self._ref("tr_s_20")), (500, self._ref("tr_s_10"))])
        self._pay(invoice, "2026-10-01")
        kur_farki = self.env["account.move"].browse(invoice.action_l10n_tr_create_kur_farki()["res_id"])
        by_tax = {line.tax_ids: line.price_subtotal for line in kur_farki.invoice_line_ids}
        self.assertEqual(by_tax, {self._ref("tr_s_20"): 3000, self._ref("tr_s_10"): 1500})
        self.assertEqual(kur_farki.amount_total, 5250)

    def test_partial_payments(self):
        invoice = self._invoice("out_invoice", [(1000, self._ref("tr_s_20"))])
        self._pay(invoice, "2026-10-01", amount=600)
        self.assertEqual(invoice.l10n_tr_kur_farki_pending, 1800)
        first = self.env["account.move"].browse(invoice.action_l10n_tr_create_kur_farki()["res_id"])
        self.assertEqual(first.amount_total, 1800)
        self._pay(invoice, "2026-10-20", amount=600)
        self.assertEqual(invoice.l10n_tr_kur_farki_pending, 3000)
        second = self.env["account.move"].browse(invoice.action_l10n_tr_create_kur_farki()["res_id"])
        self.assertEqual(second.amount_total, 3000)
        self.assertEqual(str(second.invoice_date), "2026-10-20")
        self.assertEqual(invoice.l10n_tr_kur_farki_count, 2)

    def test_reset_to_draft_and_repost(self):
        invoice = self._invoice("out_invoice", [(1000, self._ref("tr_s_20"))])
        self._pay(invoice, "2026-10-01")
        kur_farki = self.env["account.move"].browse(invoice.action_l10n_tr_create_kur_farki()["res_id"])
        kur_farki.action_post()
        first_offset = kur_farki.l10n_tr_kur_farki_offset_move_id
        kur_farki.button_draft()
        self.assertFalse(kur_farki.l10n_tr_kur_farki_offset_move_id)
        reversal = self.env["account.move"].search([("reversed_entry_id", "=", first_offset.id)])
        self.assertEqual(reversal.state, "posted")
        kur_farki.action_post()
        moves = self.env["account.move"].search([("company_id", "=", self.company.id), ("state", "=", "posted")])
        self.assertEqual(self._balance(self.gain, moves), -3000)

    def test_cancelled_invoice_frees_the_difference(self):
        invoice = self._invoice("out_invoice", [(1000, self._ref("tr_s_20"))])
        self._pay(invoice, "2026-10-01")
        kur_farki = self.env["account.move"].browse(invoice.action_l10n_tr_create_kur_farki()["res_id"])
        kur_farki.button_cancel()
        self.assertEqual(invoice.l10n_tr_kur_farki_pending, 3600)

    def test_withholding_invoice_is_refused(self):
        invoice = self._invoice("out_invoice", [(1000, self._ref("tr_s_wh_20_5_10"))])
        self._pay(invoice, "2026-10-01")
        with self.assertRaises(UserError):
            invoice.action_l10n_tr_create_kur_farki()

    def test_company_currency_invoice(self):
        invoice = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner_a.id,
                "invoice_date": "2026-09-01",
                "invoice_line_ids": [(0, 0, {"name": "X", "quantity": 1, "price_unit": 100})],
            }
        )
        invoice.action_post()
        self.assertEqual(invoice.l10n_tr_kur_farki_pending, 0)
