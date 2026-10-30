import logging
from datetime import datetime, timedelta
from xml.etree import ElementTree

import requests

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

TCMB_TODAY_URL = "https://www.tcmb.gov.tr/kurlar/today.xml"

# Rate types published in the TCMB bulletin for each currency (XML tag, label)
TCMB_RATE_TYPES = [
    ("ForexBuying", "Forex buying"),
    ("ForexSelling", "Forex selling"),
    ("BanknoteBuying", "Banknote buying"),
    ("BanknoteSelling", "Banknote selling"),
]


class ResCompany(models.Model):
    _inherit = "res.company"

    tcmb_auto_update = fields.Boolean(
        string="Update TCMB rates automatically",
        help="If enabled, currency rates are fetched daily from the indicative rates bulletin of the Central Bank of the Republic of Türkiye (TCMB).",
    )
    tcmb_rate_type = fields.Selection(
        TCMB_RATE_TYPES,
        string="TCMB rate type",
        default="ForexBuying",
        required=True,
    )
    tcmb_next_day = fields.Boolean(
        string="Apply rates from the next day",
        default=True,
        help="TCMB publishes its rates at 15:30 on business days and they are used for the "
        "following day. If enabled, the bulletin of day D is used from D+1; otherwise from D. "
        "On weekends and holidays the last published rate stays in effect.",
    )
    tcmb_last_update = fields.Datetime(string="Last TCMB update", readonly=True)

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
        """Parse the TCMB today.xml content.

        Returns: (bulletin date, {currency code: {rate type: TRY for 1 unit}})
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
        """TRY value of 1 unit of `code`; falls back to forex buying if the selected type is missing."""
        self.ensure_one()
        if code == "TRY":
            return 1.0
        values = rates.get(code) or {}
        return values.get(self.tcmb_rate_type) or values.get("ForexBuying")

    def _tcmb_apply(self, bulletin_date, rates):
        """Write the bulletin to the companies' rate tables. Returns the number of rates written."""
        Rate = self.env["res.currency.rate"].sudo()
        updated = 0
        for company in self:
            company_value = company._tcmb_try_per_unit(rates, company.currency_id.name)
            if not company_value:
                raise UserError(
                    self.env._(
                        "TCMB does not publish a rate for the currency of %(company)s (%(currency)s).",
                        company=company.name,
                        currency=company.currency_id.name,
                    )
                )
            # Odoo 20 applies a rate from the day after its date: the bulletin keeps its own date to be
            # used from the next day, or is dated the day before to be used on the bulletin day.
            rate_date = bulletin_date if company.tcmb_next_day else bulletin_date - timedelta(days=1)
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
            raise UserError(self.env._("Could not reach the TCMB rates service: %s", error)) from error
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
            _logger.warning("Could not reach the TCMB rates service: %s", error)
            return
        bulletin_date, rates = self._tcmb_parse(content)
        for company in companies:
            try:
                company._tcmb_apply(bulletin_date, rates)
            except UserError as error:
                _logger.warning("TCMB rates could not be updated for %s: %s", company.name, error)
