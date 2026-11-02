from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    l10n_tr_tax_office_id = fields.Many2one(
        "l10n_tr.tax.office",
        string="Tax Office",
        help="Turkish tax office (vergi dairesi) where the partner is registered.",
    )

    @api.depends("l10n_tr_tax_office_id")
    def _compute_display_name(self):
        super()._compute_display_name()
        if not self.env.context.get("show_address"):
            return
        for partner in self.filtered("l10n_tr_tax_office_id"):
            partner.display_name = f"{partner.display_name}\n{partner.l10n_tr_tax_office_id.name}"


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_tr_tax_office_id = fields.Many2one(
        related="partner_id.l10n_tr_tax_office_id", readonly=False, string="Tax Office"
    )
    # res.company has no country_code field before Odoo 18
    l10n_tr_country_code = fields.Char(related="country_id.code", string="Country Code")
