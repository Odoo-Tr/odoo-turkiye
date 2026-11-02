from odoo.tests import TransactionCase, tagged

from odoo.addons.l10n_tr_banka.models.res_bank import iban_bank_code


@tagged("post_install", "-at_install")
class TestTurkishBanks(TransactionCase):
    def test_data(self):
        banks = self.env["res.bank"].search([("country", "=", self.env.ref("base.tr").id), ("l10n_tr_eft_code", "!=", False)])
        self.assertGreaterEqual(len(banks), 60)
        garanti = self.env["res.bank"].search([("l10n_tr_eft_code", "=", "0062")])
        self.assertEqual((garanti.name, garanti.bic), ("TÜRKİYE GARANTİ BANKASI A.Ş.", "TGBATRIS"))
        self.assertEqual(len(set(banks.mapped("l10n_tr_eft_code"))), len(banks), "EFT codes are unique")

    def test_iban_code(self):
        self.assertEqual(iban_bank_code("TR33 0006 1005 1978 6457 8413 26"), "0061")
        self.assertEqual(iban_bank_code("TR710006200000000000000000"), "0062")
        self.assertIsNone(iban_bank_code("DE89370400440532013000"))
        self.assertIsNone(iban_bank_code("TR12"))

    def test_bank_from_iban(self):
        partner = self.env["res.partner"].create({"name": "Banka Testi"})
        account = self.env["res.partner.bank"].create({"partner_id": partner.id, "acc_number": "TR79 0001 0000 0000 0000 0000 01"})
        self.assertEqual(account.bank_id.l10n_tr_eft_code, "0010")
        other = self.env["res.partner.bank"].create({"partner_id": partner.id, "acc_number": "DE89370400440532013000"})
        self.assertFalse(other.bank_id)
