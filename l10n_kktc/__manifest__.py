{
    "name": "TRNC Accounting (KKTC)",
    "summary": "Turkish Republic of Northern Cyprus: country, districts, chart of accounts and VAT rates",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations/Account Charts",
    "author": "Odoo Türkiye",
    "website": "https://odoo-tr.com",
    "support": "destek@odoo-tr.com",
    "license": "LGPL-3",
    "depends": ["l10n_tr"],
    "data": [
        "data/res_country_data.xml",
        "data/res.country.state.csv",
    ],
    "images": ["static/description/banner.png"],
    "post_init_hook": "post_init_hook",
    "installable": True,
}
