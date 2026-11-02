from odoo import _, api, fields, models

from .entitlement import annual_leave_days, service_years


class HrLeaveType(models.Model):
    _inherit = "hr.leave.type"

    l10n_tr_annual_leave = fields.Boolean(
        string="Turkish annual leave",
        help="Allocate this time off type automatically on each service anniversary, "
        "according to Turkish Labour Law no. 4857, article 53.",
    )


class HrLeaveAllocation(models.Model):
    _inherit = "hr.leave.allocation"

    l10n_tr_service_year = fields.Integer(string="Service Year", readonly=True, copy=False)


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    l10n_tr_seniority_date = fields.Date(
        string="Seniority Date",
        groups="hr.group_hr_user",
        help="Start of service with the employer, used for annual leave (İş Kanunu md. 53-54).",
    )
    l10n_tr_underground = fields.Boolean(
        string="Underground Work", groups="hr.group_hr_user", help="Adds 4 days to the annual leave."
    )
    l10n_tr_service_years = fields.Integer(
        string="Completed Service Years", compute="_compute_l10n_tr_annual_leave", groups="hr.group_hr_user"
    )
    l10n_tr_annual_leave_days = fields.Integer(
        string="Annual Leave Entitlement",
        compute="_compute_l10n_tr_annual_leave",
        groups="hr.group_hr_user",
        help="Days earned at the last service anniversary.",
    )

    @api.depends("l10n_tr_seniority_date", "l10n_tr_underground", "birthday")
    def _compute_l10n_tr_annual_leave(self):
        today = fields.Date.context_today(self)
        for employee in self:
            years = service_years(employee.l10n_tr_seniority_date, today)
            employee.l10n_tr_service_years = years
            employee.l10n_tr_annual_leave_days = employee._l10n_tr_days_for_year(years)

    def _l10n_tr_anniversary(self, years):
        self.ensure_one()
        return fields.Date.add(self.l10n_tr_seniority_date, years=years)

    def _l10n_tr_days_for_year(self, years):
        """Days earned when the employee completes the given service year; age is taken on that date."""
        self.ensure_one()
        if years < 1 or not self.l10n_tr_seniority_date:
            return 0
        anniversary = self._l10n_tr_anniversary(years)
        age = service_years(self.birthday, anniversary) if self.birthday else None
        return annual_leave_days(years, age=age, underground=self.l10n_tr_underground)

    def _l10n_tr_annual_leave_type(self, leave_types):
        """The flagged time off type for the employee's company: same country first, then generic."""
        self.ensure_one()
        company = self.company_id
        if "company_id" in leave_types._fields:
            leave_types = leave_types.filtered(lambda t: not t.company_id or t.company_id == company)
        if "country_id" in leave_types._fields:
            return (
                leave_types.filtered(lambda t: t.country_id == company.country_id)[:1]
                or leave_types.filtered(lambda t: not t.country_id)[:1]
                or leave_types[:1]
            )
        return leave_types[:1]

    def _l10n_tr_allocate_annual_leave(self):
        """Allocate the current service year's leave once. Earlier years are left to the HR team,
        as the time already taken is not known. Returns the created allocations."""
        Allocation = self.env["hr.leave.allocation"].sudo()
        leave_types = self.env["hr.leave.type"].sudo().search([("l10n_tr_annual_leave", "=", True)])
        today = fields.Date.context_today(self)
        created = Allocation
        for employee in self.filtered("l10n_tr_seniority_date"):
            years = service_years(employee.l10n_tr_seniority_date, today)
            days = employee._l10n_tr_days_for_year(years)
            leave_type = employee._l10n_tr_annual_leave_type(leave_types)
            if not days or not leave_type:
                continue
            if Allocation.search_count(
                [("employee_id", "=", employee.id), ("holiday_status_id", "=", leave_type.id), ("l10n_tr_service_year", "=", years)]
            ):
                continue
            vals = {
                "name": _("Annual leave, service year %s", years),
                "employee_id": employee.id,
                "holiday_status_id": leave_type.id,
                "number_of_days": days,
                "date_from": employee._l10n_tr_anniversary(years),
                "l10n_tr_service_year": years,
            }
            if "allocation_type" in Allocation._fields:  # removed in Odoo 20
                vals["allocation_type"] = "regular"
            allocation = Allocation.create(vals)
            if allocation.state == "draft":  # Odoo 15 creates allocations as drafts
                allocation.action_confirm()
            if allocation.state != "validate":
                # The approval method is action_validate up to Odoo 18, action_approve from 19
                if hasattr(allocation, "action_validate"):
                    allocation.action_validate()
                else:
                    allocation.action_approve()
            created |= allocation
        return created

    def action_l10n_tr_allocate_annual_leave(self):
        created = self._l10n_tr_allocate_annual_leave()
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "type": "success" if created else "info",
                "message": _("%s annual leave allocations created.", len(created)),
                "next": {"type": "ir.actions.client", "tag": "soft_reload"},
            },
        }

    @api.model
    def _l10n_tr_cron_allocate_annual_leave(self):
        self.search([("l10n_tr_seniority_date", "!=", False)])._l10n_tr_allocate_annual_leave()
