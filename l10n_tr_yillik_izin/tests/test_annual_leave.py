from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests import TransactionCase, tagged

from odoo.addons.l10n_tr_yillik_izin.hooks import paid_time_off
from odoo.addons.l10n_tr_yillik_izin.models.entitlement import annual_leave_days, service_years


@tagged("post_install", "-at_install")
class TestAnnualLeave(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.company.country_id = cls.env.ref("base.tr")

    def test_law_bands(self):
        self.assertEqual(annual_leave_days(0), 0)
        self.assertEqual([annual_leave_days(y, age=30) for y in (1, 5, 6, 14, 15, 30)], [14, 14, 20, 20, 26, 26])
        self.assertEqual(annual_leave_days(2, age=18), 20)
        self.assertEqual(annual_leave_days(2, age=19), 14)
        self.assertEqual(annual_leave_days(2, age=50), 20)
        self.assertEqual(annual_leave_days(20, age=55), 26)
        self.assertEqual(annual_leave_days(2, age=30, underground=True), 18)
        self.assertEqual(annual_leave_days(2, age=50, underground=True), 24)
        self.assertEqual(service_years(date(2020, 3, 1), date(2026, 2, 28)), 5)
        self.assertEqual(service_years(date(2020, 3, 1), date(2026, 3, 1)), 6)

    def _employee(self, years_ago, birthday=None, **vals):
        today = fields.Date.context_today(self.env["hr.employee"])
        return self.env["hr.employee"].create(
            {"name": "Çalışan", "l10n_tr_seniority_date": today - relativedelta(years=years_ago, days=10), "birthday": birthday, **vals}
        )

    def test_allocation(self):
        employee = self._employee(6, birthday=date(1990, 1, 1))
        self.assertEqual((employee.l10n_tr_service_years, employee.l10n_tr_annual_leave_days), (6, 20))
        allocations = employee._l10n_tr_allocate_annual_leave()
        self.assertEqual(len(allocations), 1)
        self.assertEqual((allocations.number_of_days, allocations.state, allocations.l10n_tr_service_year), (20, "validate", 6))
        self.assertEqual(allocations.holiday_status_id, paid_time_off(self.env))
        self.assertTrue(paid_time_off(self.env).l10n_tr_annual_leave)
        self.assertFalse(employee._l10n_tr_allocate_annual_leave(), "Once per service year")

    def test_age_on_anniversary(self):
        """The age floor uses the age on the anniversary date."""
        today = fields.Date.context_today(self.env["hr.employee"])
        employee = self._employee(3, birthday=today - relativedelta(years=50, days=5))
        self.assertEqual(employee.l10n_tr_annual_leave_days, 14, "Turned 50 after the anniversary")
        employee.birthday = today - relativedelta(years=50, days=30)
        self.assertEqual(employee.l10n_tr_annual_leave_days, 20)

    def test_less_than_a_year(self):
        employee = self._employee(0)
        self.assertEqual(employee.l10n_tr_annual_leave_days, 0)
        self.assertFalse(employee._l10n_tr_allocate_annual_leave())

    def test_views_load(self):
        self.env["hr.employee"].fields_view_get(view_type="form")
        self.env["hr.leave.type"].fields_view_get(view_type="form")
