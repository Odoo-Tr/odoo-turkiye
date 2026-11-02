def post_init_hook(env):
    """Add the withholding accounts and taxes to companies that already use the Turkish chart."""
    companies = env["res.company"].search(
        [("chart_template", "=", "tr"), ("parent_id", "=", False)], order="parent_path"
    )
    for company in companies:
        Template = env["account.chart.template"].with_company(company)
        data = {
            "account.account": Template._get_tr_stopaj_account_account(),
            "account.tax.group": Template._get_tr_stopaj_account_tax_group(),
            "account.tax": Template._get_tr_stopaj_account_tax(),
        }
        Template._pre_reload_data(company, {}, data)
        Template._load_data(data)
        Template._load_translations(companies=company)
