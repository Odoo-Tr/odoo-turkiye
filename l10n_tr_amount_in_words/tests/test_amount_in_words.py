from odoo.tests import TransactionCase, tagged

from ..models.tr_number_words import amount_to_words, integer_to_words


@tagged("post_install", "-at_install")
class TestAmountInWords(TransactionCase):
    def test_integers(self):
        cases = {
            0: "sıfır",
            1: "bir",
            10: "on",
            100: "yüz",
            101: "yüz bir",
            1000: "bin",
            1001: "bin bir",
            2000: "iki bin",
            11111: "on bir bin yüz on bir",
            100000: "yüz bin",
            1000000: "bir milyon",
            1234567: "bir milyon iki yüz otuz dört bin beş yüz altmış yedi",
            2000000000: "iki milyar",
        }
        for number, expected in cases.items():
            self.assertEqual(" ".join(integer_to_words(number)), expected, number)

    def test_amounts(self):
        self.assertEqual(
            amount_to_words(1234.56, "TRY"),
            "Bin İki Yüz Otuz Dört Türk Lirası Elli Altı Kuruş",
        )
        self.assertEqual(amount_to_words(1000, "TRY"), "Bin Türk Lirası")
        self.assertEqual(amount_to_words(0.5, "TRY"), "Sıfır Türk Lirası Elli Kuruş")
        self.assertEqual(amount_to_words(81.01, "USD"), "Seksen Bir ABD Doları Bir Sent")
        self.assertEqual(amount_to_words(19.999, "EUR"), "Yirmi Avro")
        self.assertEqual(amount_to_words(-15, "TRY"), "On Beş Türk Lirası")

    def test_invoice_field(self):
        partner = self.env["res.partner"].create({"name": "Test Müşteri"})
        move = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": partner.id,
                "currency_id": self.env.company.currency_id.id,
                "invoice_line_ids": [
                    (0, 0, {"name": "Hizmet", "quantity": 1, "price_unit": 1234.56, "tax_ids": [(6, 0, [])]})
                ],
            }
        )
        self.assertTrue(move.tr_amount_total_words.startswith("Bin İki Yüz Otuz Dört"))
        self.env.company.tr_show_amount_in_words = False
        move.invalidate_recordset(["tr_amount_total_words"])
        self.assertFalse(move.tr_amount_total_words)
