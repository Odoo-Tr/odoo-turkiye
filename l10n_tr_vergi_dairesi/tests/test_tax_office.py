from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestTaxOffice(TransactionCase):
    def test_data(self):
        offices = self.env["l10n_tr.tax.office"].search([])
        self.assertGreater(len(offices), 1000)
        self.assertEqual(len(offices.state_id), 81)
        self.assertTrue(offices.filtered(lambda o: o.name == "Kadıköy Vergi Dairesi Müdürlüğü" or "Kadıköy" in o.name))

    def test_partner_and_company(self):
        office = self.env["l10n_tr.tax.office"].search([("state_id", "=", self.env.ref("base.state_tr_34").id)], limit=1)
        partner = self.env["res.partner"].create({"name": "Test A.Ş.", "country_id": self.env.ref("base.tr").id, "l10n_tr_tax_office_id": office.id})
        self.assertIn(office.name, partner.with_context(show_address=True).display_name)
        self.assertNotIn(office.name, partner.display_name)
        company = self.env["res.company"].create({"name": "TR Co"})
        company.l10n_tr_tax_office_id = office
        self.assertEqual(company.partner_id.l10n_tr_tax_office_id, office)

    def test_views_load(self):
        self.env["res.partner"].get_view(view_type="form")
        self.env["res.company"].get_view(view_type="form")
