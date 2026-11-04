from odoo import api, models


class ReportFinancialStatement(models.AbstractModel):
    _name = "report.l10n_tr_mali_tablolar.report_financial_statement"
    _description = "Turkish Balance Sheet and Income Statement"

    @api.model
    def _get_report_values(self, docids, data=None):
        engine = self.env["l10n_tr.financial.statement"]
        if "company_id" not in (data or {}):  # printed from the wizard record; Odoo adds its own keys to data
            data = self.env["l10n_tr.financial.report.wizard"].browse(docids)[:1]._options()
        report = engine.build(data)
        company = self.env["res.company"].browse(data["company_id"])
        return {
            "doc_ids": docids,
            "doc_model": "l10n_tr.financial.report.wizard",
            "docs": self.env["l10n_tr.financial.report.wizard"].browse(docids),
            "company": company,
            "report": report,
            "fmt": engine._format,
        }


class ReportTrialBalance(models.AbstractModel):
    _name = "report.l10n_tr_mali_tablolar.report_trial_balance"
    _inherit = "report.l10n_tr_mali_tablolar.report_financial_statement"
    _description = "Turkish Trial Balance"
