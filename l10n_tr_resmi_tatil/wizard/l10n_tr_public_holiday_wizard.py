from datetime import date

from odoo import _, api, fields, models

from ..models.holidays import YEARS


def _year_selection(*_args):
    return [(str(year), str(year)) for year in YEARS]


class L10nTrPublicHolidayWizard(models.TransientModel):
    _name = "l10n_tr.public.holiday.wizard"
    _description = "Load Turkish Public Holidays"

    year_from = fields.Selection(_year_selection, required=True, default=lambda self: self._default_year())
    year_to = fields.Selection(_year_selection, required=True, default=lambda self: str(YEARS[-1]))
    company_ids = fields.Many2many("res.company", required=True, default=lambda self: self.env.company)

    @api.model
    def _default_year(self):
        return str(max(YEARS[0], min(date.today().year, YEARS[-1])))

    def action_load(self):
        self.ensure_one()
        years = [y for y in YEARS if int(self.year_from) <= y <= int(self.year_to)]
        created = self.env["resource.calendar.leaves"]._l10n_tr_create_public_holidays(self.company_ids, years)
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "type": "success" if created else "info",
                "message": _("%s public holidays created.", len(created)),
                "next": {"type": "ir.actions.act_window_close"},
            },
        }
