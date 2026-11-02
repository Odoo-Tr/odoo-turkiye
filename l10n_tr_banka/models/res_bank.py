import re

from odoo import api, models

from .banks import BANKS

# Odoo 20 has no bank directory (res.bank); the bank's name and BIC are stored on the account
BANK_BY_CODE = {code: (name, bic) for name, code, bic in BANKS if code}


def iban_bank_code(account_number):
    """EFT code of the bank in a Turkish IBAN: positions 5-9 are the bank code (TCMB IBAN Tebliği)."""
    iban = re.sub(r"\s", "", account_number or "").upper()
    if not re.fullmatch(r"TR\d{24}", iban):
        return None
    return iban[4:9][-4:] if iban[4] == "0" else iban[4:9]


def bank_from_iban(account_number):
    return BANK_BY_CODE.get(iban_bank_code(account_number))


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    @api.onchange("account_number")
    def _onchange_account_number_l10n_tr_bank(self):
        bank = bank_from_iban(self.account_number)
        if bank and not self.bank_name:
            self.bank_name, bic = bank
            self.bank_bic = self.bank_bic or bic

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            bank = bank_from_iban(vals.get("account_number"))
            if bank and not vals.get("bank_name"):
                vals["bank_name"] = bank[0]
                if bank[1] and not vals.get("bank_bic"):
                    vals["bank_bic"] = bank[1]
        return super().create(vals_list)
