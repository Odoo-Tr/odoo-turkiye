from odoo import _, models
from odoo.addons.account.models.chart_template import template


class AccountChartTemplate(models.AbstractModel):
    _inherit = "account.chart.template"

    # The official KKTC uniform chart of accounts (Gelir ve Vergi Dairesi) uses the same codes as
    # Türkiye's, so the accounts come from l10n_tr; only the VAT taxes are specific to KKTC.

    def _kktc_from_tr(self, method):
        """Data of a Turkish template method; its name differs between Odoo versions."""
        method = getattr(self, method, None)
        return method() if method else {}

    def _guess_chart_template(self, country):
        if country and country.code == "CT":
            return "kktc"
        return super()._guess_chart_template(country)

    @template("kktc")
    def _get_kktc_template_data(self):
        # Odoo reads this for every chart module, installed or not, so it must not call other methods.
        # Same values as l10n_tr's template data.
        return {
            "name": _("KKTC Uniform Chart of Accounts"),
            "country": "ct",
            "code_digits": "6",
        }

    @template("kktc", "res.company")
    def _get_kktc_res_company(self):
        values = dict(self._kktc_from_tr("_get_tr_res_company").get(self.env.company.id, {}))
        values.update(
            {
                "account_fiscal_country_id": "l10n_kktc.ct",
                "account_sale_tax_id": "kktc_s_16",
                "account_purchase_tax_id": "kktc_p_16",
            }
        )
        return {self.env.company.id: values}

    @template("kktc", "account.journal")
    def _get_kktc_account_journal(self):
        return self._kktc_from_tr("_get_tr_account_journal")

    @template("kktc", "account.account")
    def _get_kktc_account_account(self):
        accounts = self._parse_csv("tr", "account.account", module="l10n_tr")
        for xmlid, values in self._kktc_from_tr("_get_tr_account_account").items():
            accounts.setdefault(xmlid, {}).update(values)
        return accounts
