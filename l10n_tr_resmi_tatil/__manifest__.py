{
    "name": "Turkish Public Holidays",
    "summary": "Turkish national, public and religious holidays 2025-2030 for time off and working calendars",
    "version": "17.0.1.0.0",
    "category": "Human Resources/Time Off",
    "author": "Odoo Türkiye",
    "website": "https://odoo-tr.com",
    "support": "destek@odoo-tr.com",
    "license": "LGPL-3",
    "depends": ["hr_holidays"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/l10n_tr_public_holiday_wizard_views.xml",
    ],
    "images": ["static/description/banner.png"],
    "post_init_hook": "post_init_hook",
    "installable": True,
}
