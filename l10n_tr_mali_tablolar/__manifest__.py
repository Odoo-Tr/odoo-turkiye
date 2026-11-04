{
    "name": "TR Financial Statements",
    "summary": "Trial balance (mizan), balance sheet and income statement in the Turkish uniform format, as PDF and Excel",
    "version": "17.0.1.0.0",
    "category": "Accounting/Localizations",
    "author": "Odoo Türkiye",
    "website": "https://odoo-tr.com",
    "support": "destek@odoo-tr.com",
    "license": "LGPL-3",
    "depends": ["account"],
    "data": [
        "security/ir.model.access.csv",
        "report/financial_statement_templates.xml",
        "views/financial_report_wizard_views.xml",
    ],
    "images": ["static/description/banner.png"],
    "installable": True,
}
