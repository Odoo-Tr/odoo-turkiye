{
    "name": "Amount in Words (TR)",
    "summary": "Print the Turkish \"Yalnız: ...\" amount in words line on invoices",
    "version": "15.0.1.1.0",
    "category": "Accounting/Localizations",
    "author": "Odoo Türkiye",
    "website": "https://odoo-tr.com",
    "support": "destek@odoo-tr.com",
    "license": "LGPL-3",
    "depends": ["account"],
    "data": [
        "views/res_config_settings_views.xml",
        "report/report_invoice.xml",
    ],
    "images": ["static/description/banner.png"],
    "installable": True,
}
