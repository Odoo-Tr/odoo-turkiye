from odoo import _, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    tcmb_auto_update = fields.Boolean(related="company_id.tcmb_auto_update", readonly=False)
    tcmb_rate_type = fields.Selection(related="company_id.tcmb_rate_type", readonly=False)
    tcmb_next_day = fields.Boolean(related="company_id.tcmb_next_day", readonly=False)
    tcmb_last_update = fields.Datetime(related="company_id.tcmb_last_update")

    def action_tcmb_update_rates(self):
        self.ensure_one()
        bulletin_date, updated = self.company_id.action_tcmb_update_rates()
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "type": "success",
                "title": _("TCMB rates updated"),
                "message": _(
                    "%(count)s rates saved from the bulletin of %(date)s.",
                    date=bulletin_date.strftime("%d.%m.%Y"),
                    count=updated,
                ),
                "next": {"type": "ir.actions.client", "tag": "soft_reload"},
            },
        }
