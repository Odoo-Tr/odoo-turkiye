from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    tr_show_amount_in_words = fields.Boolean(
        string="Show amount in words on invoices",
        default=True,
        help="Adds the Turkish \"Yalnız: ...\" line under the total on the invoice report.",
    )
