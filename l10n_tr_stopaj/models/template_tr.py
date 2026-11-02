from odoo import models
from odoo.addons.account.models.chart_template import template


class AccountChartTemplate(models.AbstractModel):
    _inherit = "account.chart.template"

    @template("tr", "account.account")
    def _get_tr_stopaj_account_account(self):
        return self._parse_csv("tr", "account.account", module="l10n_tr_stopaj")

    @template("tr", "account.tax.group")
    def _get_tr_stopaj_account_tax_group(self):
        return self._parse_csv("tr", "account.tax.group", module="l10n_tr_stopaj")

    @template("tr", "account.tax")
    def _get_tr_stopaj_account_tax(self):
        return self._parse_csv("tr", "account.tax", module="l10n_tr_stopaj")
