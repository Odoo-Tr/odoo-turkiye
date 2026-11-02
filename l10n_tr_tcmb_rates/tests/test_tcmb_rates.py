from datetime import date

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged

SAMPLE = b"""<?xml version="1.0" encoding="UTF-8"?>
<Tarih_Date Tarih="30.10.2026" Date="10/30/2026" Bulten_No="2026/204">
  <Currency CrossOrder="0" Kod="USD" CurrencyCode="USD">
    <Unit>1</Unit><ForexBuying>40.0000</ForexBuying><ForexSelling>40.2000</ForexSelling>
    <BanknoteBuying>39.9000</BanknoteBuying><BanknoteSelling>40.3000</BanknoteSelling>
  </Currency>
  <Currency CrossOrder="1" Kod="EUR" CurrencyCode="EUR">
    <Unit>1</Unit><ForexBuying>50.0000</ForexBuying><ForexSelling>50.5000</ForexSelling>
    <BanknoteBuying/><BanknoteSelling/>
  </Currency>
  <Currency CrossOrder="2" Kod="JPY" CurrencyCode="JPY">
    <Unit>100</Unit><ForexBuying>25.0000</ForexBuying><ForexSelling>25.5000</ForexSelling>
    <BanknoteBuying/><BanknoteSelling/>
  </Currency>
</Tarih_Date>
"""


@tagged("post_install", "-at_install")
class TestTcmbRates(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.try_currency = cls.env.ref("base.TRY")
        cls.usd = cls.env.ref("base.USD")
        cls.eur = cls.env.ref("base.EUR")
        cls.jpy = cls.env.ref("base.JPY")
        (cls.try_currency | cls.usd | cls.eur | cls.jpy).write({"active": True})
        cls.company = cls.env["res.company"].create(
            {"name": "TCMB Test A.Ş.", "currency_id": cls.try_currency.id}
        )

    def _rate(self, currency, company, day):
        return self.env["res.currency.rate"].search(
            [("currency_id", "=", currency.id), ("company_id", "=", company.id), ("name", "=", day)]
        )

    def test_parse(self):
        bulletin_date, rates = self.company._tcmb_parse(SAMPLE)
        self.assertEqual(bulletin_date, date(2026, 10, 30))
        self.assertAlmostEqual(rates["USD"]["ForexBuying"], 40.0)
        self.assertAlmostEqual(rates["JPY"]["ForexBuying"], 0.25)  # 100 birim üzerinden
        self.assertNotIn("BanknoteBuying", rates["EUR"])

    def test_apply_next_day_try_company(self):
        bulletin_date, rates = self.company._tcmb_parse(SAMPLE)
        self.company._tcmb_apply(bulletin_date, rates)
        day = date(2026, 10, 31)
        self.assertAlmostEqual(self._rate(self.usd, self.company, day).rate, 1 / 40.0)
        self.assertAlmostEqual(self._rate(self.jpy, self.company, day).rate, 1 / 0.25)
        self.assertFalse(self._rate(self.usd, self.company, date(2026, 10, 30)))
        self.assertTrue(self.company.tcmb_last_update)

    def _usd_in_try_on(self, day):
        """TRY value of 1 USD that Odoo uses on `day`."""
        getattr(self.env.cr, "cache", {}).pop("res.currency.rate.values", None)
        self.env.cache.invalidate()
        return self.usd._convert(1, self.try_currency, self.company, fields.Date.to_date(day), round=False)

    def test_effective_dates(self):
        """Check the day each bulletin is used on, not the stored date: Odoo 20 applies a rate from
        the day after its date, earlier versions from its date."""
        self.env["res.currency.rate"].create(
            {"name": "2026-10-01", "currency_id": self.usd.id, "company_id": self.company.id, "rate": 1 / 35}
        )
        self.company._tcmb_apply(*self.company._tcmb_parse(SAMPLE))
        self.assertAlmostEqual(self._usd_in_try_on("2026-10-30"), 35, places=4)
        self.assertAlmostEqual(self._usd_in_try_on("2026-10-31"), 40, places=4)

        self.company.tcmb_next_day = False
        self.company._tcmb_apply(*self.company._tcmb_parse(SAMPLE))
        self.assertAlmostEqual(self._usd_in_try_on("2026-10-30"), 40, places=4)

    def test_same_day_and_rate_type_fallback(self):
        self.company.write({"tcmb_next_day": False, "tcmb_rate_type": "BanknoteSelling"})
        bulletin_date, rates = self.company._tcmb_parse(SAMPLE)
        self.company._tcmb_apply(bulletin_date, rates)
        day = date(2026, 10, 30)
        self.assertAlmostEqual(self._rate(self.usd, self.company, day).rate, 1 / 40.3)
        # EUR için efektif kur yok: döviz alışa düşer
        self.assertAlmostEqual(self._rate(self.eur, self.company, day).rate, 1 / 50.0)

    def test_update_existing_rate(self):
        bulletin_date, rates = self.company._tcmb_parse(SAMPLE)
        self.company._tcmb_apply(bulletin_date, rates)
        self.company._tcmb_apply(bulletin_date, rates)
        self.assertEqual(len(self._rate(self.usd, self.company, date(2026, 10, 31))), 1)

    def test_non_try_company(self):
        usd_company = self.env["res.company"].create({"name": "USD Co", "currency_id": self.usd.id})
        bulletin_date, rates = usd_company._tcmb_parse(SAMPLE)
        usd_company._tcmb_apply(bulletin_date, rates)
        day = date(2026, 10, 31)
        # 1 USD = 40 TL ve 1 EUR = 50 TL ise 1 USD = 0,8 EUR
        self.assertAlmostEqual(self._rate(self.eur, usd_company, day).rate, 40.0 / 50.0)
        self.assertAlmostEqual(self._rate(self.try_currency, usd_company, day).rate, 40.0)

    def test_unsupported_company_currency(self):
        xof = self.env.ref("base.XOF")
        xof.active = True
        other = self.env["res.company"].create({"name": "XOF Co", "currency_id": xof.id})
        bulletin_date, rates = other._tcmb_parse(SAMPLE)
        with self.assertRaises(UserError):
            other._tcmb_apply(bulletin_date, rates)
