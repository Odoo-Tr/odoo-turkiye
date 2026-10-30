import logging
from datetime import datetime, timedelta
from xml.etree import ElementTree

import requests

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

TCMB_TODAY_URL = "https://www.tcmb.gov.tr/kurlar/today.xml"

# TCMB bülteninde her para birimi için yayınlanan kur türleri (XML etiketi, etiket)
TCMB_RATE_TYPES = [
    ("ForexBuying", "Döviz alış"),
    ("ForexSelling", "Döviz satış"),
    ("BanknoteBuying", "Efektif alış"),
    ("BanknoteSelling", "Efektif satış"),
]


class ResCompany(models.Model):
    _inherit = "res.company"

    tcmb_auto_update = fields.Boolean(
        string="TCMB kurlarını otomatik güncelle",
        help="Açıksa döviz kurları her gün TCMB'nin gösterge kurları bülteninden alınır.",
    )
    tcmb_rate_type = fields.Selection(
        TCMB_RATE_TYPES,
        string="TCMB kur türü",
        default="ForexBuying",
        required=True,
    )
    tcmb_next_day = fields.Boolean(
        string="Kuru ertesi günden geçerli yap",
        default=True,
        help="TCMB kurları her iş günü 15.30'da açıklanır ve uygulamada bir sonraki gün "
        "için kullanılır. Açıksa D gününün bülteni D+1 tarihli kur olarak kaydedilir; "
        "hafta sonu ve tatillerde son açıklanan kur geçerli kalır.",
    )
    tcmb_last_update = fields.Datetime(string="Son TCMB güncellemesi", readonly=True)

    @api.model
    def _tcmb_fetch(self):
        response = requests.get(
            TCMB_TODAY_URL,
            timeout=20,
            headers={"User-Agent": "Odoo l10n_tr_tcmb_rates (odoo-tr.com)"},
        )
        response.raise_for_status()
        return response.content

    @api.model
    def _tcmb_parse(self, content):
        """TCMB today.xml içeriğini çözümler.

        Dönüş: (bülten tarihi, {para birimi kodu: {kur türü: 1 birim için TL}})
        """
        root = ElementTree.fromstring(content)
        bulletin_date = datetime.strptime(root.attrib["Tarih"], "%d.%m.%Y").date()
        rates = {}
        for node in root.findall("Currency"):
            code = node.attrib.get("CurrencyCode") or node.attrib.get("Kod")
            unit = float((node.findtext("Unit") or "1").strip() or 1)
            values = {}
            for key, _label in TCMB_RATE_TYPES:
                text = (node.findtext(key) or "").strip()
                if text:
                    values[key] = float(text) / unit
            if code and values:
                rates[code] = values
        return bulletin_date, rates

    def _tcmb_try_per_unit(self, rates, code):
        """1 birim `code` için TL karşılığı; seçili kur türü yoksa döviz alışa düşer."""
        self.ensure_one()
        if code == "TRY":
            return 1.0
        values = rates.get(code) or {}
        return values.get(self.tcmb_rate_type) or values.get("ForexBuying")

    def _tcmb_apply(self, bulletin_date, rates):
        """Bülteni şirketlerin kur tablolarına yazar. Güncellenen kur sayısını döner."""
        Rate = self.env["res.currency.rate"].sudo()
        updated = 0
        for company in self:
            company_value = company._tcmb_try_per_unit(rates, company.currency_id.name)
            if not company_value:
                raise UserError(
                    self.env._(
                        "TCMB, %(company)s şirketinin para birimi (%(currency)s) için kur yayınlamıyor.",
                        company=company.name,
                        currency=company.currency_id.name,
                    )
                )
            rate_date = bulletin_date + timedelta(days=1) if company.tcmb_next_day else bulletin_date
            currencies = self.env["res.currency"].search(
                [("active", "=", True), ("id", "!=", company.currency_id.id)]
            )
            for currency in currencies:
                value = company._tcmb_try_per_unit(rates, currency.name)
                if not value:
                    continue
                rate = company_value / value
                existing = Rate.search(
                    [
                        ("currency_id", "=", currency.id),
                        ("company_id", "=", company.id),
                        ("name", "=", rate_date),
                    ],
                    limit=1,
                )
                if existing:
                    existing.rate = rate
                else:
                    Rate.create(
                        {
                            "currency_id": currency.id,
                            "company_id": company.id,
                            "name": rate_date,
                            "rate": rate,
                        }
                    )
                updated += 1
            company.tcmb_last_update = fields.Datetime.now()
        return updated

    def action_tcmb_update_rates(self):
        try:
            content = self._tcmb_fetch()
        except requests.RequestException as error:
            raise UserError(self.env._("TCMB kurlarına ulaşılamadı: %s", error)) from error
        bulletin_date, rates = self._tcmb_parse(content)
        return bulletin_date, self._tcmb_apply(bulletin_date, rates)

    @api.model
    def _tcmb_cron_update(self):
        companies = self.search([("tcmb_auto_update", "=", True)])
        if not companies:
            return
        try:
            content = self._tcmb_fetch()
        except requests.RequestException as error:
            _logger.warning("TCMB kurlarına ulaşılamadı: %s", error)
            return
        bulletin_date, rates = self._tcmb_parse(content)
        for company in companies:
            try:
                company._tcmb_apply(bulletin_date, rates)
            except UserError as error:
                _logger.warning("TCMB kurları %s için güncellenemedi: %s", company.name, error)
