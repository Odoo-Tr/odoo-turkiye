{
    "name": "Türkiye - Faturada Yazıyla Tutar",
    "summary": "Fatura çıktısına \"Yalnız: ... Türk Lirası ... Kuruş\" satırını ekler",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations",
    "author": "Odoo Türkiye (odoo-tr.com)",
    "website": "https://github.com/Odoo-Tr/odoo-turkiye",
    "license": "LGPL-3",
    "depends": ["account"],
    "data": [
        "views/res_config_settings_views.xml",
        "report/report_invoice.xml",
    ],
    "installable": True,
}
