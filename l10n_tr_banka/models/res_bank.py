import re

from odoo import api, fields, models


def iban_bank_code(account_number):
    """EFT code of the bank in a Turkish IBAN: positions 5-9 are the bank code (TCMB IBAN Tebliği)."""
    iban = re.sub(r"\s", "", account_number or "").upper()
    if not re.fullmatch(r"TR\d{24}", iban):
        return None
    return iban[4:9][-4:] if iban[4] == "0" else iban[4:9]


class ResBank(models.Model):
    _inherit = "res.bank"

    l10n_tr_eft_code = fields.Char(string="EFT Code", index=True, help="Bank code of the Turkish EFT system, also in the IBAN.")


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    def _l10n_tr_bank_from_iban(self, account_number):
        code = iban_bank_code(account_number)
        if not code:
            return self.env["res.bank"]
        return self.env["res.bank"].search([("l10n_tr_eft_code", "=", code)], limit=1)

    @api.onchange("acc_number")
    def _onchange_acc_number_l10n_tr_bank(self):
        if self.acc_number and not self.bank_id:
            self.bank_id = self._l10n_tr_bank_from_iban(self.acc_number)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("acc_number") and not vals.get("bank_id"):
                bank = self._l10n_tr_bank_from_iban(vals["acc_number"])
                if bank:
                    vals["bank_id"] = bank.id
        return super().create(vals_list)
