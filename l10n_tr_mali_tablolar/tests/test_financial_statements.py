import base64
import io
import zipfile
from datetime import date

from odoo.exceptions import AccessError
from odoo.release import version_info
from odoo.tests import TransactionCase, tagged

# Odoo 15 account types (user_type_id)
TYPES_15 = {
    "asset_current": "account.data_account_type_current_assets",
    "asset_fixed": "account.data_account_type_fixed_assets",
    "liability_current": "account.data_account_type_current_liabilities",
    "equity": "account.data_account_type_equity",
    "income": "account.data_account_type_revenue",
    "income_other": "account.data_account_type_other_income",
    "expense": "account.data_account_type_expenses",
    "off_balance": "account.data_account_off_sheet",
}


@tagged("post_install", "-at_install")
class TestFinancialStatements(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try_currency = cls.env.ref("base.TRY")
        try_currency.active = True
        cls.company = cls.env["res.company"].create({"name": "TR Mali Tablolar Test", "currency_id": try_currency.id})
        cls.company.external_report_layout_id = cls.env.ref("web.external_layout_standard")
        cls.env.user.company_ids |= cls.company
        cls.env = cls.env(context=dict(cls.env.context, allowed_company_ids=[cls.company.id]))
        cls.journal = cls.env["account.journal"].create({"name": "Mahsup", "code": "TMSC", "type": "general", "company_id": cls.company.id})
        cls.acc = {}
        for code, kind in [
            ("100", "asset_current"), ("120", "asset_current"), ("153", "asset_current"), ("191", "asset_current"),
            ("255", "asset_fixed"), ("257", "asset_fixed"),
            ("320", "liability_current"), ("370", "liability_current"), ("391", "liability_current"),
            ("500", "equity"), ("590", "equity"),
            ("600", "income"), ("610", "income"), ("621", "expense"), ("632", "expense"), ("642", "income_other"),
            ("656", "expense"), ("660", "expense"), ("690", "expense"), ("691", "expense"), ("692", "expense"),
            ("770", "expense"), ("900", "off_balance"), ("950", "off_balance"),
        ]:
            cls.acc[code] = cls._account(code, kind)
        cls._entry("2024-03-01", [("100", 100000), ("500", -100000)])
        cls._entry("2024-04-01", [("120", 12000), ("600", -10000), ("391", -2000)])
        cls._entry("2025-01-10", [("153", 5000), ("191", 1000), ("320", -6000)])
        cls._entry("2025-02-01", [("120", 24000), ("600", -20000), ("391", -4000)])
        cls._entry("2025-02-15", [("610", 1000), ("120", -1000)])
        cls._entry("2025-02-20", [("621", 4000), ("153", -4000)])
        cls._entry("2025-03-01", [("770", 3000), ("100", -3000)])
        cls._entry("2025-03-05", [("632", 500), ("100", -500)])
        cls._entry("2025-03-10", [("255", 8000), ("100", -8000)])
        cls._entry("2025-03-31", [("632", 800), ("257", -800)])
        cls._entry("2025-04-01", [("100", 300), ("642", -300)])
        cls._entry("2025-04-02", [("656", 200), ("120", -200)])
        cls._entry("2025-04-03", [("660", 100), ("100", -100)])
        cls._entry("2025-04-30", [("691", 1000), ("370", -1000)])
        cls._entry("2025-04-20", [("900", 50), ("950", -50)])
        cls._entry("2025-04-15", [("120", 999), ("600", -999)], post=False)

    @classmethod
    def _account(cls, code, kind):
        Account = cls.env["account.account"]
        vals = {"name": "Hesap %s" % code, "code": code}
        if "account_type" in Account._fields:
            vals["account_type"] = kind
        else:
            vals["user_type_id"] = cls.env.ref(TYPES_15[kind]).id
        if "company_ids" in Account._fields:
            vals["company_ids"] = [(6, 0, cls.company.ids)]
        else:
            vals["company_id"] = cls.company.id
        return Account.with_company(cls.company).create(vals)

    @classmethod
    def _entry(cls, day, lines, post=True):
        move = cls.env["account.move"].with_company(cls.company).create({
            "move_type": "entry",
            "date": day,
            "journal_id": cls.journal.id,
            "line_ids": [(0, 0, {
                "name": "Test",
                "account_id": cls.acc[code].id,
                "debit": amount if amount > 0 else 0.0,
                "credit": -amount if amount < 0 else 0.0,
            }) for code, amount in lines],
        })
        if post:
            move.action_post()
        return move

    def _build(self, report_type, **options):
        values = {
            "report_type": report_type,
            "company_id": self.company.id,
            "date_from": "2025-01-01",
            "date_to": "2025-04-30",
            "level": "main",
            "hide_zero": True,
            "compare": False,
            "include_draft": False,
        }
        values.update(options)
        return self.env["l10n_tr.financial.statement"].build(values)

    def _row(self, report, label_start, style=None):
        rows = [r for r in report["rows"] if r["label"].startswith(label_start) and (style is None or r["style"] == style)]
        self.assertEqual(len(rows), 1, "%s: %s" % (label_start, [r["label"] for r in report["rows"]]))
        return rows[0]["values"]

    def test_income_statement(self):
        report = self._build("gelir")
        self.assertEqual(self._row(report, "A. BRÜT SATIŞLAR"), [20000])
        self.assertEqual(self._row(report, "B. SATIŞ İNDİRİMLERİ"), [-1000])
        self.assertEqual(self._row(report, "C. NET SATIŞLAR"), [19000])
        self.assertEqual(self._row(report, "D. SATIŞLARIN MALİYETİ"), [-4000])
        self.assertEqual(self._row(report, "BRÜT SATIŞ KÂRI"), [15000])
        self.assertEqual(self._row(report, "E. FAALİYET GİDERLERİ"), [-4300])
        self.assertEqual(self._row(report, "Genel yönetim giderleri (7/A"), [-3000])
        self.assertEqual(self._row(report, "3. Genel Yönetim Giderleri"), [-1300])
        self.assertEqual(self._row(report, "FAALİYET KÂRI"), [10700])
        self.assertEqual(self._row(report, "OLAĞAN KÂR"), [10700])
        self.assertEqual(self._row(report, "DÖNEM KÂRI VEYA ZARARI"), [10700])
        self.assertEqual(self._row(report, "K. DÖNEM KÂRI VERGİ"), [-1000])
        self.assertEqual(self._row(report, "DÖNEM NET KÂRI"), [9700])
        self.assertEqual(report["rows"][-1]["style"], "total")
        self.assertFalse(report["warnings"])

    def test_draft_entries(self):
        self.assertEqual(self._row(self._build("gelir", include_draft=True), "A. BRÜT SATIŞLAR"), [20999])

    def test_balance_sheet(self):
        report = self._build("bilanco", compare=True)
        self.assertEqual(self._row(report, "1. Kasa"), [88700, 100000])
        self.assertEqual(self._row(report, "1. Alıcılar"), [34800, 12000])
        self.assertEqual(self._row(report, "8. Birikmiş Amortismanlar"), [-800, 0])
        self.assertEqual(self._row(report, "I. DÖNEN VARLIKLAR"), [125500, 112000])
        self.assertEqual(self._row(report, "AKTİF TOPLAMI"), [132700, 112000])
        self.assertEqual(self._row(report, "Previous years' profit without closing entries"), [10000, 0])
        self.assertEqual(self._row(report, "Net profit (loss) of the period without closing entries"), [9700, 10000])
        self.assertEqual(self._row(report, "PASİF TOPLAMI"), [132700, 112000])
        self.assertFalse(report["warnings"])
        # Memo accounts stay outside the balance sheet
        self.assertFalse([r for r in report["rows"] if r["code"].startswith("9")])

    def test_closing_entries(self):
        """After the closing entries the profit moves to 590; the income statement still shows the sales."""
        self._entry("2025-04-30", [("600", 20000), ("690", -20000)])
        self._entry("2025-04-30", [("690", 20000), ("692", -20000)])
        self._entry("2025-04-30", [("692", 20000), ("590", -20000)])
        self.assertEqual(self._row(self._build("gelir"), "A. BRÜT SATIŞLAR"), [20000])
        balance = self._build("bilanco")
        self.assertEqual(self._row(balance, "1. Dönem Net Kârı"), [20000])
        self.assertEqual(self._row(balance, "F. Dönem Net Kârı (Zararı)"), [9700])
        self.assertEqual(self._row(balance, "PASİF TOPLAMI"), [132700])
        self.assertFalse(balance["warnings"])

    def test_trial_balance(self):
        report = self._build("mizan", date_from="2025-02-01")
        totals = report["rows"][-1]["values"]
        self.assertAlmostEqual(totals[4], totals[5])
        self.assertAlmostEqual(totals[6], totals[7])
        self.assertFalse(report["warnings"])
        cash = [r for r in report["rows"] if r["code"] == "100"][0]["values"]
        # Opening 100.000 (2024), period credits 3.000 + 500 + 8.000 + 100, debit 300
        self.assertEqual(cash, [100000, 0, 300, 11600, 100300, 11600, 88700, 0])
        sales = [r for r in report["rows"] if r["code"] == "600"][0]["values"]
        # Income statement accounts start from the fiscal year: the 2024 sale is not carried
        self.assertEqual(sales, [0, 0, 0, 20000, 0, 20000, 0, 20000])
        undistributed = [r for r in report["rows"] if r["label"] == "Result of previous years without closing entries"][0]["values"]
        self.assertEqual(undistributed[:2], [0, 10000])

    def test_trial_balance_detail(self):
        bank = self._account("102001", "asset_current")
        self.env["account.move"].with_company(self.company).create({
            "move_type": "entry", "date": "2025-03-15", "journal_id": self.journal.id,
            "line_ids": [(0, 0, {"name": "Banka", "account_id": bank.id, "debit": 700.0, "credit": 0.0}),
                         (0, 0, {"name": "Banka", "account_id": self.acc["100"].id, "debit": 0.0, "credit": 700.0})],
        }).action_post()
        report = self._build("mizan", level="detail")
        main = [r for r in report["rows"] if r["code"] == "102"]
        sub = [r for r in report["rows"] if r["code"] == "102001"]
        self.assertEqual(main[0]["label"], "Bankalar")
        self.assertEqual(main[0]["style"], "line")
        self.assertEqual(sub[0]["style"], "sub")
        self.assertEqual(sub[0]["values"][6], 700)

    def test_format(self):
        fmt = self.env["l10n_tr.financial.statement"]._format
        self.assertEqual(fmt(1234567.891), "1.234.567,89")
        self.assertEqual(fmt(-800), "(800,00)")
        self.assertEqual(fmt(0), "0,00")
        self.assertEqual(fmt(0, blank_zero=True), "")

    def test_pdf_and_excel(self):
        wizard = self.env["l10n_tr.financial.report.wizard"].create({
            "report_type": "bilanco", "company_id": self.company.id, "date_from": date(2025, 1, 1), "date_to": date(2025, 4, 30), "compare": False,
        })
        action = wizard.action_print_pdf()
        self.assertEqual(action["report_name"], "l10n_tr_mali_tablolar.report_financial_statement")
        ref = "l10n_tr_mali_tablolar.action_report_financial_statement"
        if version_info[0] >= 16:
            html = self.env["ir.actions.report"]._render_qweb_html(ref, wizard.ids)[0]
            # As the web client does: PDF rendering adds report_type to data
            self.env["ir.actions.report"]._get_rendering_context(self.env.ref(ref), wizard.ids, {"report_type": "pdf"})
        else:  # Odoo 15: methods of the report record
            html = self.env.ref(ref)._render_qweb_html(wizard.ids)[0]
            self.env.ref(ref)._get_rendering_context(wizard.ids, {"report_type": "pdf"})
        html = html.decode()
        self.assertIn("BİLANÇO", html)
        self.assertIn("132.700,00", html)
        self.assertIn("(800,00)", html)

        result = wizard.action_export_xlsx()
        self.assertEqual(result["type"], "ir.actions.act_url")
        self.assertTrue(wizard.xlsx_name.endswith(".xlsx"))
        value = wizard.xlsx_file
        content = value.content if hasattr(value, "content") else base64.b64decode(value)  # Odoo 20: BinaryValue
        with zipfile.ZipFile(io.BytesIO(bytes(content))) as book:
            self.assertIn("xl/worksheets/sheet1.xml", book.namelist())

    def test_other_company_is_refused(self):
        other = self.env["res.company"].sudo().create({"name": "Erişilemeyen Şirket"})
        self.env.user.company_ids -= other
        with self.assertRaises(AccessError):
            self._build("bilanco", company_id=other.id)
