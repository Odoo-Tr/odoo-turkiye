from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.addons.l10n_tr_stopaj.hooks import post_init_hook


@tagged("post_install_l10n", "post_install", "-at_install")
class TestStopaj(AccountTestInvoicingCommon):
    @classmethod
    @AccountTestInvoicingCommon.setup_country("tr")
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.company_data["company"]

    def _ref(self, xmlid):
        return self.env.ref(f"account.{self.company.id}_{xmlid}")

    def _move(self, move_type, price, taxes):
        move = self.env["account.move"].create(
            {
                "move_type": move_type,
                "partner_id": self.partner_a.id,
                "invoice_date": "2026-10-15",
                "invoice_line_ids": [
                    (0, 0, {"name": "Hizmet", "quantity": 1, "price_unit": price, "tax_ids": [(6, 0, taxes.ids)]})
                ],
            }
        )
        move.action_post()
        return move

    def _line(self, move, account):
        return move.line_ids.filtered(lambda line: line.account_id == account)

    def test_chart_data(self):
        payable = self._ref("tr360001")
        prepaid = self._ref("tr193001")
        self.assertEqual((payable.code, payable.account_type), ("360001", "liability_current"))
        self.assertEqual((prepaid.code, prepaid.account_type), ("193001", "asset_current"))
        for xmlid, use in [
            ("tr_stopaj_p_smm_20", "purchase"),
            ("tr_stopaj_p_smm_20_net", "purchase"),
            ("tr_stopaj_p_kira_20", "purchase"),
            ("tr_stopaj_p_kira_20_net", "purchase"),
            ("tr_stopaj_s_smm_20", "sale"),
            ("tr_stopaj_s_smm_20_net", "sale"),
        ]:
            tax = self._ref(xmlid)
            self.assertEqual((tax.amount, tax.type_tax_use), (-20, use))
            self.assertTrue(tax.l10n_tr_stopaj_type)

    def test_hook_is_idempotent(self):
        taxes = self.env["account.tax"].search_count([("company_id", "=", self.company.id)])
        # Odoo runs install hooks as superuser
        post_init_hook(self.env(su=True))
        self.assertEqual(self.env["account.tax"].search_count([("company_id", "=", self.company.id)]), taxes)

    def test_self_employment_bill(self):
        """10.000 gross + 20% VAT - 20% withholding: 10.000 to pay, 2.000 owed to the tax office."""
        bill = self._move("in_invoice", 10000, self._ref("tr_p_20") | self._ref("tr_stopaj_p_smm_20"))
        self.assertEqual(bill.amount_untaxed, 10000)
        self.assertEqual(bill.amount_total, 10000)
        self.assertEqual(self._line(bill, self._ref("tr360001")).balance, -2000)

    def test_rent_from_net_amount(self):
        """A landlord paid 8.000 net: the gross rent is 10.000 and the withholding 2.000."""
        bill = self._move("in_invoice", 8000, self._ref("tr_stopaj_p_kira_20_net"))
        self.assertEqual(bill.amount_untaxed, 10000)
        self.assertEqual(bill.amount_total, 8000)
        self.assertEqual(self._line(bill, self._ref("tr360001")).balance, -2000)

    def test_self_employment_net_with_vat(self):
        bill = self._move("in_invoice", 8000, self._ref("tr_p_20") | self._ref("tr_stopaj_p_smm_20_net"))
        self.assertEqual(bill.amount_untaxed, 10000)
        self.assertEqual(bill.amount_tax, 0)
        self.assertEqual(bill.amount_total, 10000)

    def test_sale_withheld_by_customer(self):
        invoice = self._move("out_invoice", 10000, self._ref("tr_s_20") | self._ref("tr_stopaj_s_smm_20"))
        self.assertEqual(invoice.amount_total, 10000)
        self.assertEqual(self._line(invoice, self._ref("tr193001")).balance, 2000)

    def test_withholding_list(self):
        smm = self._ref("tr_stopaj_p_smm_20")
        bill = self._move("in_invoice", 10000, self._ref("tr_p_20") | smm)
        refund = self._move("in_refund", 1000, smm)
        sale = self._move("out_invoice", 5000, self._ref("tr_stopaj_s_smm_20"))
        self._move("in_invoice", 500, self._ref("tr_p_20"))  # no withholding, not listed
        # Created last, so its lines are still pending in the ORM when the view is read
        rent = self._move("in_invoice", 8000, self._ref("tr_stopaj_p_kira_20_net"))

        Report = self.env["l10n_tr.stopaj.report"]
        rows = Report.search([("company_id", "=", self.company.id)])
        self.assertEqual(len(rows), 4)
        by_move = {row.move_id: row for row in rows}
        self.assertRecordValues(
            by_move[bill], [{"stopaj_type": "serbest_meslek", "direction": "purchase", "base_amount": 10000, "stopaj_amount": 2000}]
        )
        self.assertRecordValues(by_move[rent], [{"stopaj_type": "kira", "base_amount": 10000, "stopaj_amount": 2000}])
        self.assertRecordValues(by_move[refund], [{"base_amount": -1000, "stopaj_amount": -200}])
        self.assertRecordValues(by_move[sale], [{"direction": "sale", "base_amount": 5000, "stopaj_amount": 1000}])
