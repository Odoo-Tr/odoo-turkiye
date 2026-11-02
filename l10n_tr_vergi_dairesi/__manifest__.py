{
    "name": "Turkish Tax Offices",
    "summary": "List of Turkish tax offices (vergi dairesi) on contacts and companies",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations",
    "author": "Odoo Türkiye",
    "website": "https://odoo-tr.com",
    "support": "destek@odoo-tr.com",
    "license": "LGPL-3",
    "depends": ["contacts"],
    "data": [
        "security/ir.model.access.csv",
        "data/l10n_tr.tax.office.csv",
        "views/l10n_tr_tax_office_views.xml",
        "views/res_partner_views.xml",
    ],
    "images": ["static/description/banner.png"],
    "installable": True,
}
