from datetime import datetime

from odoo.tests import TransactionCase, tagged

from odoo.addons.l10n_tr_resmi_tatil.models.holidays import holidays_for_year


@tagged("post_install", "-at_install")
class TestTurkishHolidays(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env["res.company"].create({"name": "Tatil A.Ş.", "country_id": cls.env.ref("base.tr").id})
        cls.Leave = cls.env["resource.calendar.leaves"]

    def test_2026_list(self):
        holidays = {name: (start, end) for name, start, end in holidays_for_year(2026)}
        self.assertEqual(len(holidays), 10)
        # Istanbul is UTC+3: arife from 13:00 local is 10:00 UTC
        self.assertEqual(holidays["Ramazan Bayramı"], (datetime(2026, 3, 19, 10, 0), datetime(2026, 3, 22, 20, 59, 59)))
        self.assertEqual(holidays["Kurban Bayramı"], (datetime(2026, 5, 26, 10, 0), datetime(2026, 5, 30, 20, 59, 59)))
        self.assertEqual(holidays["Cumhuriyet Bayramı Arifesi (yarım gün)"], (datetime(2026, 10, 28, 10, 0), datetime(2026, 10, 28, 20, 59, 59)))
        self.assertEqual(holidays["Yılbaşı"], (datetime(2025, 12, 31, 21, 0), datetime(2026, 1, 1, 20, 59, 59)))

    def test_overlaps_are_merged(self):
        holidays = holidays_for_year(2027)
        merged = [h for h in holidays if "Kurban" in h[0]]
        self.assertEqual(len(merged), 1)
        self.assertIn("Gençlik ve Spor", merged[0][0])
        self.assertEqual((merged[0][1], merged[0][2]), (datetime(2027, 5, 15, 10, 0), datetime(2027, 5, 19, 20, 59, 59)))
        merged_2029 = [h for h in holidays_for_year(2029) if "Kurban" in h[0]][0]
        self.assertEqual(merged_2029[1], datetime(2029, 4, 22, 21, 0), "23 Nisan full day starts the merged period")
        for year in range(2025, 2031):
            periods = holidays_for_year(year)
            for (_, _, end), (_, start, _) in zip(periods, periods[1:]):
                self.assertLess(end, start, year)

    def test_existing_holiday_is_kept(self):
        manual = self.Leave.with_company(self.company).create({"name": "Elle girilen", "company_id": self.company.id, "calendar_id": False,
                                    "date_from": datetime(2026, 10, 29, 6, 0), "date_to": datetime(2026, 10, 29, 15, 0)})
        created = self.Leave._l10n_tr_create_public_holidays(self.company, [2026])
        self.assertEqual(len(created), 9)
        self.assertTrue(manual.exists())

    def test_create_is_idempotent(self):
        created = self.Leave._l10n_tr_create_public_holidays(self.company, [2026, 2027])
        self.assertEqual(len(created), 19)  # 2026: 10, 2027: 9 after merging Kurban Bayramı with 19 Mayıs
        self.assertFalse(created.resource_id)
        self.assertEqual(created.company_id, self.company)
        self.assertFalse(self.Leave._l10n_tr_create_public_holidays(self.company, [2026]))

    def test_wizard(self):
        wizard = self.env["l10n_tr.public.holiday.wizard"].with_company(self.company).create(
            {"year_from": "2028", "year_to": "2028", "company_ids": [(6, 0, self.company.ids)]}
        )
        action = wizard.action_load()
        self.assertEqual(action["params"]["type"], "success")
        self.assertEqual(self.Leave.search_count([("company_id", "=", self.company.id)]), 10)

    def test_working_calendar(self):
        """The holidays remove working hours from the company's calendar."""
        vals = {"company_id": self.company.id}
        if "tz" in self.env["resource.calendar"]._fields:  # removed in Odoo 20
            vals["tz"] = "Europe/Istanbul"
        calendar = self.env.ref("resource.resource_calendar_std").copy(vals)
        # A past year: the install hook loads holidays from this year on, and a calendar without
        # resources counts the company-wide holidays of every company
        start, end = datetime(2024, 10, 29, 5, 0), datetime(2024, 10, 29, 15, 0)  # 08:00-18:00 in Istanbul
        before = calendar.get_work_hours_count(start, end, compute_leaves=True)
        self.Leave._l10n_tr_create_public_holidays(self.company, [2024])
        self.assertGreater(before, 0)
        self.assertEqual(calendar.get_work_hours_count(start, end, compute_leaves=True), 0)
