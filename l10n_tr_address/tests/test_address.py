from lxml import etree

from odoo.tests import Form, TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestTurkishAddress(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tr = cls.env.ref("base.tr")
        cls.istanbul = cls.env.ref("base.state_tr_34")
        cls.amasya = cls.env.ref("base.state_tr_05")
        cls.ankara = cls.env.ref("base.state_tr_06")
        City = cls.env["res.city"]
        cls.kadikoy = City.search([("state_id", "=", cls.istanbul.id), ("name", "=", "Kadıköy")])
        cls.amasya_merkez = City.search([("state_id", "=", cls.amasya.id), ("name", "=", "Merkez")])

    def _partner(self, **vals):
        return self.env["res.partner"].create({"name": "Test", "country_id": self.tr.id, **vals})

    def test_districts_data(self):
        cities = self.env["res.city"].search([("country_id", "=", self.tr.id)])
        self.assertEqual(len(cities), 973)
        self.assertEqual(len(cities.state_id), 81)
        self.assertEqual(len(cities.filtered(lambda c: c.state_id == self.istanbul)), 39)
        self.assertEqual(len(cities.filtered(lambda c: c.name == "Merkez")), 51)
        self.assertTrue(self.kadikoy and self.amasya_merkez)

    def test_country_settings(self):
        self.assertTrue(self.tr.enforce_cities)
        self.assertTrue(self.tr.state_required)

    def test_address_format(self):
        partner = self._partner(
            street="Caferağa Mah. Moda Cad. No:1",
            zip="34710",
            city_id=self.kadikoy.id,
            city="Kadıköy",
            state_id=self.istanbul.id,
        )
        self.assertIn("34710 Kadıköy/İstanbul", partner._display_address())

    def test_match_districts(self):
        exact = self._partner(city="Kadıköy", state_id=self.istanbul.id)
        upper = self._partner(city="KADIKOY")
        with_province = self._partner(city="Merkez / Amasya")
        ambiguous = self._partner(city="Merkez")
        province_only = self._partner(city="Ankara")
        unknown = self._partner(city="Atlantis", state_id=self.istanbul.id)
        foreign = self.env["res.partner"].create(
            {"name": "Foreign", "city": "Kadıköy", "country_id": self.env.ref("base.de").id}
        )
        partners = exact | upper | with_province | ambiguous | province_only | unknown | foreign

        self.assertEqual(partners._l10n_tr_match_districts(), 4)
        self.assertEqual(exact.city_id, self.kadikoy)
        self.assertEqual(upper.city_id, self.kadikoy)
        self.assertEqual(upper.city, "Kadıköy")
        self.assertEqual(upper.state_id, self.istanbul)
        self.assertEqual(with_province.city_id, self.amasya_merkez)
        self.assertEqual(with_province.state_id, self.amasya)
        self.assertFalse(ambiguous.city_id)
        self.assertFalse(province_only.city_id)
        self.assertEqual(province_only.state_id, self.ankara)
        self.assertFalse(unknown.city_id)
        self.assertFalse(foreign.city_id)

    def test_match_action(self):
        partner = self._partner(city="Kadıköy", state_id=self.istanbul.id)
        action = partner.action_l10n_tr_match_districts()
        self.assertEqual(action["params"]["type"], "success")
        self.assertEqual(partner.city_id, self.kadikoy)

    def test_onchange_province_clears_other_district(self):
        with Form(self.env["res.partner"]) as form:
            form.name = "Test"
            form.country_id = self.tr
            form.city_id = self.kadikoy
            self.assertEqual(form.state_id, self.istanbul)
            self.assertEqual(form.city, "Kadıköy")
            form.state_id = self.ankara
            self.assertFalse(form.city_id)
            self.assertFalse(form.city)

    def test_district_domain_follows_province(self):
        arch = self.env["res.partner"].get_view(view_type="form")["arch"]
        domains = [node.get("domain") for node in etree.fromstring(arch).iter("field") if node.get("name") == "city_id"]
        self.assertTrue(domains)
        for domain in domains:
            self.assertIn("('state_id', '=', state_id)", domain)
