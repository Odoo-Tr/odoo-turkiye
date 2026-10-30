from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    tr_show_amount_in_words = fields.Boolean(
        string="Faturada yazıyla tutar göster",
        default=True,
        help="Fatura çıktısında toplamın altına \"Yalnız: ...\" satırını ekler.",
    )
