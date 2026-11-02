"""Annual paid leave under 4857 sayılı İş Kanunu, madde 53 (mevzuat.gov.tr).

- More than 1 year up to and including 5 years: 14 days
- More than 5 and less than 15 years: 20 days
- 15 years and more: 26 days
- Workers aged 18 or younger, or 50 or older: at least 20 days
- Underground work: 4 more days (added by Law 6552 in 2014)
"""
from dateutil.relativedelta import relativedelta


def service_years(start, on):
    """Completed years of service between start and on."""
    return relativedelta(on, start).years if start and on and on >= start else 0


def annual_leave_days(years, age=None, underground=False):
    """Minimum days earned for a completed service year (years >= 1)."""
    if years < 1:
        return 0
    days = 14 if years <= 5 else 20 if years < 15 else 26
    if age is not None and (age <= 18 or age >= 50):
        days = max(days, 20)
    if underground:
        days += 4
    return days
