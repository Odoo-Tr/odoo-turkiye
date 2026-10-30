{
    "name": "Income Withholding (TR)",
    "summary": "Turkish income tax withholding (stopaj) on self-employment fees and rent",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations",
    "author": "Odoo Türkiye",
    "website": "https://odoo-tr.com",
    "support": "destek@odoo-tr.com",
    "license": "LGPL-3",
    "depends": ["l10n_tr"],
    "data": [
        "security/ir.model.access.csv",
        "security/stopaj_security.xml",
        "report/stopaj_report_views.xml",
    ],
    "images": ["static/description/banner.png"],
    "post_init_hook": "post_init_hook",
    "installable": True,
}
