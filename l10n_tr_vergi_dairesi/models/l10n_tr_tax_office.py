from odoo import fields, models


class L10nTrTaxOffice(models.Model):
    # Same model and field names as Odoo 20's l10n_tr, which ships this list itself
    _name = "l10n_tr.tax.office"
    _description = "Turkish Tax Office"
    _order = "name"

    name = fields.Char(required=True, translate=True)
    code = fields.Integer(help="Code of the tax office.")
    state_id = fields.Many2one(
        "res.country.state", string="Province", help="The Turkish province (il) of the tax office."
    )
    state_code = fields.Char(related="state_id.code")
