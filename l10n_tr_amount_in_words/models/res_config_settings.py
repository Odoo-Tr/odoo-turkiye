from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    tr_show_amount_in_words = fields.Boolean(
        related="company_id.tr_show_amount_in_words", readonly=False
    )
