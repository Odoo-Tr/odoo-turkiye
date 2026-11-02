from odoo import api, models


class ResCountry(models.Model):
    _inherit = "res.country"

    @api.depends("code")
    def _compute_image_url(self):
        super()._compute_image_url()
        for country in self.filtered(lambda c: c.code == "CT"):
            country.image_url = "/l10n_kktc/static/img/flag_ct.png"
