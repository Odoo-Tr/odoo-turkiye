import base64
import io

from odoo import _, api, fields, models

try:
    import xlsxwriter
except ImportError:  # pragma: no cover - xlsxwriter ships with Odoo
    xlsxwriter = None


class FinancialReportWizard(models.TransientModel):
    _name = "l10n_tr.financial.report.wizard"
    _description = "Turkish Financial Statement"

    report_type = fields.Selection(
        [("mizan", "Trial Balance"), ("bilanco", "Balance Sheet"), ("gelir", "Income Statement")],
        required=True, default="mizan",
    )
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company)
    date_from = fields.Date("Start Date", required=True, default=lambda self: self._default_date_from())
    date_to = fields.Date("End Date", required=True, default=fields.Date.context_today)
    level = fields.Selection(
        [("main", "Main accounts"), ("detail", "Main and sub accounts")],
        string="Detail", required=True, default="main",
    )
    hide_zero = fields.Boolean("Hide accounts without movement", default=True)
    compare = fields.Boolean("Compare with the previous year", default=True)
    include_draft = fields.Boolean("Include draft entries")
    xlsx_file = fields.Binary(readonly=True, attachment=False)
    xlsx_name = fields.Char()

    @api.model
    def _default_date_from(self):
        today = fields.Date.context_today(self)
        return fields.Date.to_date(self.env.company.compute_fiscalyear_dates(today)["date_from"])

    def _options(self):
        self.ensure_one()
        return {
            "report_type": self.report_type,
            "company_id": self.company_id.id,
            "date_from": fields.Date.to_string(self.date_from),
            "date_to": fields.Date.to_string(self.date_to),
            "level": self.level,
            "hide_zero": self.hide_zero,
            "compare": self.compare,
            "include_draft": self.include_draft,
        }

    def _report_ref(self):
        if self.report_type == "mizan":
            return "l10n_tr_mali_tablolar.action_report_trial_balance"
        return "l10n_tr_mali_tablolar.action_report_financial_statement"

    def action_print_pdf(self):
        self.ensure_one()
        # Printed on the wizard record (no data), so that print_report_name gives the file name
        return self.env.ref(self._report_ref()).report_action(self)

    def action_export_xlsx(self):
        self.ensure_one()
        report = self.env["l10n_tr.financial.statement"].build(self._options())
        names = {"mizan": "Mizan", "bilanco": "Bilanco", "gelir": "Gelir_Tablosu"}
        self.write({
            "xlsx_file": base64.b64encode(self._xlsx(report)).decode(),  # base64 text works on every version
            "xlsx_name": "%s_%s.xlsx" % (names[self.report_type], fields.Date.to_string(self.date_to)),
        })
        return {
            "type": "ir.actions.act_url",
            "url": "/web/content/?model=%s&id=%s&field=xlsx_file&filename_field=xlsx_name&download=true" % (self._name, self.id),
            "target": "self",
        }

    def _xlsx(self, report):
        output = io.BytesIO()
        book = xlsxwriter.Workbook(output, {"in_memory": True})
        sheet = book.add_worksheet(report["title"][:31])
        number = "#,##0.00;(#,##0.00);\"\""
        base = {"font_name": "Arial", "font_size": 10}
        formats = {
            "title": book.add_format(dict(base, bold=True, font_size=14)),
            "meta": book.add_format(dict(base, font_color="#555555")),
            "head": book.add_format(dict(base, bold=True, bottom=1, text_wrap=True, valign="bottom")),
            "head_num": book.add_format(dict(base, bold=True, bottom=1, text_wrap=True, align="right", valign="bottom")),
        }
        for style in ("side", "section", "group", "line", "sub", "subtotal", "total"):
            text = dict(base)
            if style in ("side", "section", "group", "subtotal", "total"):
                text["bold"] = True
            if style == "sub":
                text["indent"] = 1
                text["font_color"] = "#444444"
            if style in ("total", "subtotal"):
                text["top"] = 1
            if style == "side":
                text["font_size"] = 12
            formats[style] = book.add_format(text)
            formats[style + "_num"] = book.add_format(dict(text, num_format=number))

        sheet.write(0, 0, report["title"], formats["title"])
        vat = "  %s: %s" % (_("Tax ID"), report["vat"]) if report["vat"] else ""
        sheet.write(1, 0, report["company_name"] + vat, formats["meta"])
        sheet.write(2, 0, "%s  (%s)" % (report["period"], report["currency"]), formats["meta"])
        row = 4
        sheet.write(row, 0, _("Code"), formats["head"])
        sheet.write(row, 1, "", formats["head"])
        for col, label in enumerate(report["columns"]):
            sheet.write(row, 2 + col, label, formats["head_num"])
        for line in report["rows"]:
            row += 1
            style = line["style"]
            sheet.write(row, 0, line["code"], formats[style])
            sheet.write(row, 1, line["label"], formats[style])
            for col, value in enumerate(line["values"]):
                if value is None:
                    sheet.write_blank(row, 2 + col, None, formats[style])
                else:
                    sheet.write_number(row, 2 + col, round(value, 2), formats[style + "_num"])
        for text in report["warnings"] + report["notes"]:
            row += 1
            sheet.write(row + 1, 0, text, formats["meta"])
        sheet.set_column(0, 0, 10)
        sheet.set_column(1, 1, 52)
        sheet.set_column(2, 1 + len(report["columns"]), 16)
        sheet.freeze_panes(5, 2)
        book.close()
        return output.getvalue()
