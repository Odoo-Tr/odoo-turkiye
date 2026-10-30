{
    "name": "Türkiye - TCMB Döviz Kurları",
    "summary": "Döviz kurlarını her gün TCMB gösterge kurları bülteninden otomatik günceller",
    "version": "20.0.1.0.0",
    "category": "Accounting/Localizations",
    "author": "Odoo Türkiye (odoo-tr.com)",
    "website": "https://github.com/Odoo-Tr/odoo-turkiye",
    "license": "LGPL-3",
    "depends": ["account"],
    "data": [
        "data/ir_cron.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
}
