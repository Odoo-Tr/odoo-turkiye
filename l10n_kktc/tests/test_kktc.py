from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.addons.l10n_kktc.hooks import post_init_hook


@tagged("post_install_l10n", "post_install", "-at_install")
class TestKktc(AccountTestInvoicingCommon):
    @classmethod
    @AccountTestInvoicingCommon.setup_chart_template("kktc")
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.company_data["company"]
        cls.kktc = cls.env.ref("l10n_kktc.ct")

    def _ref(self, xmlid):
        return self.env.ref(f"account.{self.company.id}_{xmlid}")

    def test_country(self):
        self.assertEqual(self.kktc.code, "CT")
        self.assertEqual(self.kktc.currency_id, self.env.ref("base.TRY"))
        self.assertEqual(self.kktc.phone_code, 90)
        self.assertEqual(
            sorted(self.kktc.state_ids.mapped("name")),
            sorted(["Lefkoşa", "Gazimağusa", "Girne", "Güzelyurt", "İskele", "Lefke"]),
        )
        self.assertEqual(self.kktc.image_url, "/l10n_kktc/static/img/flag_ct.png")
        self.assertEqual(self.env.ref("base.tr").image_url, "/base/static/img/country_flags/tr.png")

    def test_chart(self):
        self.assertEqual(self.company.chart_template, "kktc")
        self.assertEqual(self.company.account_fiscal_country_id, self.kktc)
        Account = self.env["account.account"]
        # The Turkish chart pads codes to six digits
        for code in ("120000", "191000", "320000", "360000", "391000", "600000"):
            self.assertTrue(Account.search_count([*Account._check_company_domain(self.company), ("code", "=", code)]), code)
        self.assertEqual(self.env["account.chart.template"]._guess_chart_template(self.kktc), "kktc")

    def test_taxes(self):
        template_taxes = {
            xmlid.split(f"{self.company.id}_", 1)[1]: tax
            for tax, xmlid in self.env["account.tax"].search([("company_id", "=", self.company.id)]).get_external_id().items()
            if xmlid.startswith(f"account.{self.company.id}_")
        }
        expected = {f"kktc_{use}_{rate}" for use in "sp" for rate in (0, 5, 10, 16, 20)}
        self.assertEqual(set(template_taxes), expected, "Only the KKTC VAT taxes, none of Türkiye's")
        for xmlid, tax_id in template_taxes.items():
            tax = self.env["account.tax"].browse(tax_id)
            self.assertEqual(tax.amount, int(xmlid.rsplit("_", 1)[1]))
            self.assertEqual(tax.country_id, self.kktc)
        self.assertEqual(self.company.account_sale_tax_id, self._ref("kktc_s_16"))
        self.assertEqual(self.company.account_purchase_tax_id, self._ref("kktc_p_16"))

    def test_invoice(self):
        invoice = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner_a.id,
                "invoice_date": "2026-10-15",
                "invoice_line_ids": [
                    (0, 0, {"name": "Hizmet", "quantity": 1, "price_unit": 1000, "tax_ids": [(6, 0, self._ref("kktc_s_16").ids)]})
                ],
            }
        )
        invoice.action_post()
        self.assertEqual(invoice.amount_total, 1160)
        vat_line = invoice.line_ids.filtered(lambda line: line.tax_line_id)
        self.assertEqual((vat_line.account_id.code, vat_line.balance), ("391000", -160))

    def test_hook_loads_chart_for_kktc_company(self):
        company = self.env["res.company"].create({"name": "Girne Ticaret Ltd.", "country_id": self.kktc.id})
        self.env.user.company_ids |= company
        # Odoo runs install hooks as superuser
        post_init_hook(self.env(su=True))
        self.assertEqual(company.chart_template, "kktc")
        self.assertEqual(company.currency_id, self.env.ref("base.TRY"))
