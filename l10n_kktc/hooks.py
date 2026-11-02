def post_init_hook(env):
    """Odoo only installs a chart automatically for a country it knows, so do it for KKTC companies."""
    country = env.ref("l10n_kktc.ct")
    companies = env["res.company"].search([("chart_template", "=", False), ("parent_id", "=", False)])
    # country_id is not stored on companies, so it cannot be part of the search domain
    for company in companies.filtered(lambda c: c.country_id == country):
        env["account.chart.template"].try_loading("kktc", company)
