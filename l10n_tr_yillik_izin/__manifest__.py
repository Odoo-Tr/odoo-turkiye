{
    "name": "Turkish Annual Leave",
    "summary": "Annual paid leave by seniority under Turkish Labour Law no. 4857, article 53",
    "version": "20.0.1.0.0",
    "category": "Human Resources/Time Off",
    "author": "Odoo Türkiye",
    "website": "https://odoo-tr.com",
    "support": "destek@odoo-tr.com",
    "license": "LGPL-3",
    "depends": ["hr_holidays"],
    "data": [
        "data/ir_cron.xml",
        "views/hr_employee_views.xml",
        "views/hr_leave_type_views.xml",
    ],
    "images": ["static/description/banner.png"],
    "post_init_hook": "post_init_hook",
    "installable": True,
}
