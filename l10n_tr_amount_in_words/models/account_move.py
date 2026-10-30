from odoo import api, fields, models

from .tr_number_words import amount_to_words


class AccountMove(models.Model):
    _inherit = "account.move"

    tr_amount_total_words = fields.Char(
        string="Yazıyla tutar",
        compute="_compute_tr_amount_total_words",
    )

    @api.depends("amount_total", "currency_id", "company_id.tr_show_amount_in_words")
    def _compute_tr_amount_total_words(self):
        for move in self:
            if not move.company_id.tr_show_amount_in_words or not move.currency_id:
                move.tr_amount_total_words = False
                continue
            currency = move.currency_id
            move.tr_amount_total_words = amount_to_words(
                move.amount_total,
                currency_code=currency.name,
                unit_label=currency.currency_unit_label,
                subunit_label=currency.currency_subunit_label,
                decimals=currency.decimal_places,
            )
