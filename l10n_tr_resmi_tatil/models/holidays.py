"""Turkish holidays.

Fixed dates: 2429 sayılı Ulusal Bayram ve Genel Tatiller Hakkında Kanun (mevzuat.gov.tr).
Religious holidays: Diyanet İşleri Başkanlığı "Dini Günler" lists (vakithesaplama.diyanet.gov.tr).
Arife and 28 Ekim start at 13:00 (Kanun 2429, madde 1 and 2/B).
"""
from datetime import date, datetime, time, timedelta

import pytz

from odoo import api, models

TZ = pytz.timezone("Europe/Istanbul")

# (month, day, name)
FIXED = [
    (1, 1, "Yılbaşı"),
    (4, 23, "Ulusal Egemenlik ve Çocuk Bayramı"),
    (5, 1, "Emek ve Dayanışma Günü"),
    (5, 19, "Atatürk'ü Anma, Gençlik ve Spor Bayramı"),
    (7, 15, "Demokrasi ve Milli Birlik Günü"),
    (8, 30, "Zafer Bayramı"),
    (10, 29, "Cumhuriyet Bayramı"),
]

# year: (Ramazan Bayramı arife, Kurban Bayramı arife); the holiday runs 3 and 4 days after the arife
RELIGIOUS = {
    2025: (date(2025, 3, 29), date(2025, 6, 5)),
    2026: (date(2026, 3, 19), date(2026, 5, 26)),
    2027: (date(2027, 3, 8), date(2027, 5, 15)),
    2028: (date(2028, 2, 25), date(2028, 5, 4)),
    2029: (date(2029, 2, 13), date(2029, 4, 23)),
    2030: (date(2030, 2, 3), date(2030, 4, 12)),
}
YEARS = sorted(RELIGIOUS)


def _utc(day, at):
    return TZ.localize(datetime.combine(day, at)).astimezone(pytz.utc).replace(tzinfo=None)


def holidays_for_year(year):
    """[(name, start, end)] in naive UTC, as Odoo stores datetimes."""
    end_of_day = time(23, 59, 59)
    result = [(name, _utc(date(year, m, d), time(0, 0)), _utc(date(year, m, d), end_of_day)) for m, d, name in FIXED]
    result.append(("Cumhuriyet Bayramı Arifesi (yarım gün)", _utc(date(year, 10, 28), time(13, 0)), _utc(date(year, 10, 28), end_of_day)))
    if year in RELIGIOUS:
        ramazan, kurban = RELIGIOUS[year]
        result.append(("Ramazan Bayramı", _utc(ramazan, time(13, 0)), _utc(ramazan + timedelta(days=3), end_of_day)))
        result.append(("Kurban Bayramı", _utc(kurban, time(13, 0)), _utc(kurban + timedelta(days=4), end_of_day)))
    # Odoo does not allow overlapping public holidays (e.g. Kurban Bayramı over 19 Mayıs in 2027):
    # merge them into one period
    merged = []
    for name, start, end in sorted(result, key=lambda h: h[1]):
        if merged and start <= merged[-1][2]:
            prev_name, prev_start, prev_end = merged[-1]
            merged[-1] = (f"{prev_name} / {name}", prev_start, max(prev_end, end))
        else:
            merged.append((name, start, end))
    return merged


class ResourceCalendarLeaves(models.Model):
    _inherit = "resource.calendar.leaves"

    @api.model
    def _l10n_tr_create_public_holidays(self, companies, years):
        """Create the company-wide public holidays that do not exist yet. Returns the new records."""
        created = self.browse()
        for company in companies:
            for year in years:
                for name, start, end in holidays_for_year(year):
                    # Skip periods already covered by a company-wide holiday, ours or entered by hand
                    exists = self.search_count(
                        [
                            ("company_id", "=", company.id),
                            ("resource_id", "=", False),
                            ("date_from", "<=", end),
                            ("date_to", ">=", start),
                        ]
                    )
                    if not exists:
                        # company_id is computed from the active company when there is no calendar
                        created |= self.with_company(company).create(
                            {
                                "name": name,
                                "company_id": company.id,
                                "calendar_id": False,
                                "resource_id": False,
                                "date_from": start,
                                "date_to": end,
                            }
                        )
        return created

    def _prepare_public_holidays_data(self, start_date, end_date):
        """Odoo 20 ships a Turkish list without the half days of 28 Ekim and the arife, and with
        dates marked tentative; for Turkish companies load this module's list instead."""
        result = super()._prepare_public_holidays_data(start_date, end_date)
        turkey = self.env.ref("base.tr")
        for company in self.env.companies.filtered(lambda c: c.country_id == turkey):
            result["prepared_public_holidays"].pop(company.id, None)
            years = [year for year in YEARS if start_date.year <= year <= end_date.year]
            self._l10n_tr_create_public_holidays(company, years)
            result["companies_with_all_existing_holidays"] |= company
            result["companies_without_public_holidays"] -= company
        return result
