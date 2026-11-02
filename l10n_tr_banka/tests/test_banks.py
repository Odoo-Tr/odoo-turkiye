from odoo.tests import TransactionCase, tagged

from odoo.addons.l10n_tr_banka.models.res_bank import BANK_BY_CODE, iban_bank_code


@tagged("post_install", "-at_install")
class TestTurkishBanks(TransactionCase):
    def test_data(self):
        self.assertGreaterEqual(len(BANK_BY_CODE), 60)
        self.assertEqual(BANK_BY_CODE["0062"], ("TÜRKİYE GARANTİ BANKASI A.Ş.", "TGBATRIS"))

    def test_iban_code(self):
        self.assertEqual(iban_bank_code("TR33 0006 1005 1978 6457 8413 26"), "0061")
        self.assertIsNone(iban_bank_code("DE89370400440532013000"))

    def test_bank_from_iban(self):
        partner = self.env["res.partner"].create({"name": "Banka Testi"})
        account = self.env["res.partner.bank"].create({"partner_id": partner.id, "account_number": "TR79 0001 0000 0000 0000 0000 01"})
        self.assertEqual((account.bank_name, account.bank_bic), ("T.C. ZİRAAT BANKASI A.Ş.", "TCZBTR2A"))
        other = self.env["res.partner.bank"].create({"partner_id": partner.id, "account_number": "DE89370400440532013000"})
        self.assertFalse(other.bank_name)
