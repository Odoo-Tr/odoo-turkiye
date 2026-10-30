from odoo import fields, models

STOPAJ_TYPES = [
    ("serbest_meslek", "Self-employment fees (GVK 94/2-b)"),
    ("kira", "Rent (GVK 94/5-a)"),
]


class AccountTax(models.Model):
    _inherit = "account.tax"

    l10n_tr_stopaj_type = fields.Selection(
        STOPAJ_TYPES,
        string="Income tax withholding",
        help="Marks the tax as Turkish income tax withholding (stopaj) for the withholding list.",
    )
