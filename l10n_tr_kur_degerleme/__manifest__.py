{
    "name": "TR FX Revaluation",
    "summary": "Period-end revaluation of foreign currency receivables, payables and bank accounts (VUK 280)",
    "version": "17.0.1.0.0",
    "category": "Accounting/Localizations",
    "author": "Odoo Türkiye",
    "website": "https://odoo-tr.com",
    "support": "destek@odoo-tr.com",
    "license": "LGPL-3",
    "depends": ["account"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/fx_revaluation_wizard_views.xml",
    ],
    "images": ["static/description/banner.png"],
    "installable": True,
}
