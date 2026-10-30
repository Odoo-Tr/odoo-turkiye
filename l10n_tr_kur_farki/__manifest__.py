{
    "name": "TR FX Difference Invoice",
    "summary": "Turkish exchange difference (kur farkı) invoices with VAT for foreign currency invoices",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations",
    "author": "Odoo Türkiye",
    "website": "https://odoo-tr.com",
    "support": "destek@odoo-tr.com",
    "license": "LGPL-3",
    "depends": ["account"],
    "data": [
        "views/account_move_views.xml",
        "data/ir_actions_server.xml",
    ],
    "images": ["static/description/banner.png"],
    "installable": True,
}
