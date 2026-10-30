{
    "name": "TCMB Exchange Rates",
    "summary": "Update currency rates daily from the Central Bank of the Republic of Türkiye (TCMB) bulletin",
    "version": "18.0.1.1.0",
    "category": "Accounting/Localizations",
    "author": "Odoo Türkiye",
    "website": "https://odoo-tr.com",
    "support": "destek@odoo-tr.com",
    "license": "LGPL-3",
    "depends": ["account"],
    "data": [
        "data/ir_cron.xml",
        "views/res_config_settings_views.xml",
    ],
    "images": ["static/description/banner.png"],
    "installable": True,
}
