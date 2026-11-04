from collections import defaultdict
from datetime import timedelta

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError

from .tdhp import (
    ACCOUNTS,
    BALANCE_SECTIONS,
    CLOSING_PREFIXES,
    COST_GROUP_LABELS,
    GROUPS,
    INCOME_LAYOUT,
    account_number,
    line_number,
)

LETTERS = "ABCDEFGHIJ"
# Gelir tablosunda yeri olan 6/7 hesapları; geri kalanı (690, 692, 697, 698, 70x) not olarak gösterilir.
INCOME_GROUPS = {g for _letter, _label, sources in INCOME_LAYOUT if sources for g in sources if len(g) == 2}


def _is_income_mapped(prefix):
    return prefix[:2] in INCOME_GROUPS or prefix == "691"


def _fmt_date(value):
    return fields.Date.to_date(value).strftime("%d.%m.%Y")


class FinancialStatement(models.AbstractModel):
    _name = "l10n_tr.financial.statement"
    _description = "Turkish Financial Statements"

    # ------------------------------------------------------------------ data
    def _flush(self):
        if hasattr(self.env, "flush_all"):
            self.env.flush_all()
        else:  # Odoo 15
            self.env["base"].flush()

    def _sums(self, company, date_from, date_to, states, exclude_accounts=None):
        """{account_id: (debit, credit)} of the journal items between the two dates (date_from may be None)."""
        query = """
            SELECT l.account_id, SUM(l.debit), SUM(l.credit)
              FROM account_move_line l
             WHERE l.company_id = %s
               AND l.account_id IS NOT NULL
               AND l.parent_state IN %s
               AND l.date <= %s
        """
        params = [company.id, tuple(states), date_to]
        if date_from:
            query += " AND l.date >= %s"
            params.append(date_from)
        if exclude_accounts:
            query += " AND l.move_id NOT IN (SELECT x.move_id FROM account_move_line x WHERE x.account_id IN %s)"
            params.append(tuple(exclude_accounts))
        query += " GROUP BY l.account_id"
        self.env.cr.execute(query, params)
        return {account_id: (debit or 0.0, credit or 0.0) for account_id, debit, credit in self.env.cr.fetchall()}

    def _account_info(self, company, account_ids):
        accounts = self.env["account.account"].with_company(company).browse(list(account_ids))
        info = {}
        for account in accounts:
            if "include_initial_balance" in account._fields:
                carried = account.include_initial_balance
            else:  # Odoo 15
                carried = account.user_type_id.include_initial_balance
            info[account.id] = {"code": account.code or "", "name": account.name or "", "carried": carried}
        return info

    def _balances_by_prefix(self, company, sums):
        """Net balances (debit - credit) by 3-digit account, plus the accounts outside the uniform chart."""
        info = self._account_info(company, sums)
        by_prefix = defaultdict(float)
        names = {}
        others = []
        for account_id, (debit, credit) in sums.items():
            code = info[account_id]["code"]
            prefix = account_number(code)
            if prefix:
                by_prefix[prefix] += debit - credit
                names.setdefault(prefix, info[account_id]["name"])
            elif company.currency_id.round(debit - credit):
                others.append((code, info[account_id]["name"], debit - credit))
        return by_prefix, names, others

    def _check_company(self, company):
        if company not in self.env.user.company_ids:
            raise AccessError(_("You are not allowed to access the accounting of %s.", company.name))

    def _states(self, include_draft):
        return ("posted", "draft") if include_draft else ("posted",)

    def _fiscal_year_start(self, company, day):
        return fields.Date.to_date(company.compute_fiscalyear_dates(day)["date_from"])

    def _label(self, prefix, fallback):
        return ACCOUNTS.get(prefix) or fallback or prefix

    # ------------------------------------------------------------- reports
    @api.model
    def build(self, options):
        company = self.env["res.company"].browse(options["company_id"])
        self._check_company(company)
        self._flush()
        builder = {
            "mizan": self._trial_balance,
            "bilanco": self._balance_sheet,
            "gelir": self._income_statement,
        }[options["report_type"]]
        report = builder(company, options)
        report.update({
            "company_name": company.name,
            "vat": company.vat or "",
            "currency": company.currency_id.name,
        })
        return report

    def _trial_balance(self, company, options):
        date_from = fields.Date.to_date(options["date_from"])
        date_to = fields.Date.to_date(options["date_to"])
        if date_from > date_to:
            raise UserError(_("The start date must be before the end date."))
        states = self._states(options.get("include_draft"))
        fy_start = self._fiscal_year_start(company, date_from)
        before_year = self._sums(company, None, fy_start - timedelta(days=1), states)
        opening = self._sums(company, fy_start, date_from - timedelta(days=1), states) if date_from > fy_start else {}
        period = self._sums(company, date_from, date_to, states)
        info = self._account_info(company, set(before_year) | set(opening) | set(period))

        rows_by_key = {}
        undistributed = 0.0
        for account_id, account in info.items():
            prefix = account_number(account["code"])
            if prefix:
                profit_and_loss = prefix[0] in "67"
            else:
                profit_and_loss = not account["carried"]
            open_debit, open_credit = opening.get(account_id, (0.0, 0.0))
            old_debit, old_credit = before_year.get(account_id, (0.0, 0.0))
            if profit_and_loss:
                undistributed += old_debit - old_credit
            else:
                open_debit += old_debit
                open_credit += old_credit
            values = [open_debit, open_credit, *period.get(account_id, (0.0, 0.0))]
            main_key = prefix or account["code"]
            main = rows_by_key.setdefault(main_key, {
                "code": main_key,
                "label": self._label(prefix, account["name"]) if prefix else account["name"],
                "values": [0.0] * 4,
                "subs": [],
            })
            main["values"] = [a + b for a, b in zip(main["values"], values)]
            if prefix and account["code"] != prefix:
                main["subs"].append({"code": account["code"], "label": account["name"], "values": values})

        if company.currency_id.round(undistributed):
            rows_by_key["~"] = {
                "code": "",
                "label": _("Result of previous years without closing entries"),
                "values": [max(undistributed, 0.0), max(-undistributed, 0.0), 0.0, 0.0],
                "subs": [],
            }

        def complete(values):
            total_debit = values[0] + values[2]
            total_credit = values[1] + values[3]
            balance = total_debit - total_credit
            return values + [total_debit, total_credit, max(balance, 0.0), max(-balance, 0.0)]

        rounding = company.currency_id.round
        rows = []
        totals = [0.0] * 8
        for key in sorted(rows_by_key):
            main = rows_by_key[key]
            values = complete(main["values"])
            if options.get("hide_zero", True) and not any(rounding(v) for v in values):
                continue
            totals = [a + b for a, b in zip(totals, values)]
            rows.append({"style": "line", "code": main["code"], "label": main["label"], "values": values})
            if options.get("level") == "detail":
                for sub in sorted(main["subs"], key=lambda s: s["code"]):
                    sub_values = complete(sub["values"])
                    if options.get("hide_zero", True) and not any(rounding(v) for v in sub_values):
                        continue
                    rows.append({"style": "sub", "code": sub["code"], "label": sub["label"], "values": sub_values})
        rows.append({"style": "total", "code": "", "label": _("TOTAL"), "values": totals})

        warnings = []
        if rounding(totals[4] - totals[5]):
            warnings.append(_("Total debit and total credit differ by %s.", self._format(totals[4] - totals[5])))
        return {
            "kind": "mizan",
            "title": "MİZAN",
            "period": "%s - %s" % (_fmt_date(date_from), _fmt_date(date_to)),
            "columns": [
                _("Opening Debit"), _("Opening Credit"), _("Period Debit"), _("Period Credit"),
                _("Total Debit"), _("Total Credit"), _("Debit Balance"), _("Credit Balance"),
            ],
            "rows": rows,
            "notes": [],
            "warnings": warnings,
            "opening_note": _("Opening amounts of income statement accounts start from the fiscal year start (%s).", _fmt_date(fy_start)),
        }

    def _period_balances(self, company, date_to, states):
        """Balance sheet figures at date_to: balances by prefix, the unclosed results and the unclassified items."""
        fy_start = self._fiscal_year_start(company, date_to)
        by_prefix, names, others = self._balances_by_prefix(company, self._sums(company, None, date_to, states))
        before, _names, _others = self._balances_by_prefix(company, self._sums(company, None, fy_start - timedelta(days=1), states))
        profit_loss = [p for p in set(by_prefix) | set(before) if p[0] in "67" and _is_income_mapped(p)]
        prior = -sum(before.get(p, 0.0) for p in profit_loss)
        current = -sum(by_prefix.get(p, 0.0) for p in profit_loss) - prior
        unmapped = [(p, self._label(p, names.get(p)), by_prefix[p]) for p in sorted(by_prefix)
                    if p[0] not in "12345" and not _is_income_mapped(p) and company.currency_id.round(by_prefix[p])]
        return {"prefix": by_prefix, "names": names, "prior": prior, "current": current,
                "others": others + unmapped, "fy_start": fy_start}

    def _balance_sheet(self, company, options):
        date_to = fields.Date.to_date(options["date_to"])
        states = self._states(options.get("include_draft"))
        dates = [date_to] + ([date_to - relativedelta(years=1)] if options.get("compare") else [])
        periods = [self._period_balances(company, day, states) for day in dates]
        rounding = company.currency_id.round
        width = len(periods)

        def synthetic(prefix_group):
            """Unclosed results shown inside the equity groups."""
            if prefix_group == "57":
                return [("", _("Previous years' profit without closing entries"), [max(p["prior"], 0.0) for p in periods])]
            if prefix_group == "58":
                return [("", _("Previous years' loss without closing entries"), [min(p["prior"], 0.0) for p in periods])]
            if prefix_group == "59":
                return [("", _("Net profit (loss) of the period without closing entries"), [p["current"] for p in periods])]
            return []

        rows = []
        side_totals = {}
        for side, side_label in (("aktif", "AKTİF (VARLIKLAR)"), ("pasif", "PASİF (KAYNAKLAR)")):
            sign = 1 if side == "aktif" else -1
            rows.append({"style": "side", "code": "", "label": side_label, "values": [None] * width})
            side_total = [0.0] * width
            for section_side, section_label, class_digit, groups in BALANCE_SECTIONS:
                if section_side != side:
                    continue
                found = {p[:2] for period in periods for p in period["prefix"] if p[0] == class_digit}
                ordered = groups + sorted(found - set(groups))
                section_rows = []
                section_total = [0.0] * width
                for group in ordered:
                    letter = LETTERS[groups.index(group)] + "." if group in groups else ""
                    prefixes = sorted({p for period in periods for p in period["prefix"] if p[:2] == group})
                    lines = []
                    for prefix in prefixes:
                        values = [sign * period["prefix"].get(prefix, 0.0) for period in periods]
                        if any(rounding(v) for v in values):
                            number = line_number(prefix)
                            label = self._label(prefix, periods[0]["names"].get(prefix))
                            lines.append((prefix, "%s. %s" % (number, label) if number else label, values))
                    lines += [line for line in synthetic(group) if any(rounding(v) for v in line[2])]
                    if not lines:
                        continue
                    group_total = [sum(line[2][i] for line in lines) for i in range(width)]
                    section_total = [a + b for a, b in zip(section_total, group_total)]
                    section_rows.append({"style": "group", "code": group, "label": "%s %s" % (letter, GROUPS.get(group, group)) if letter else GROUPS.get(group, group), "values": group_total})
                    section_rows += [{"style": "line", "code": code, "label": label, "values": values} for code, label, values in lines]
                rows.append({"style": "section", "code": class_digit, "label": section_label, "values": section_total})
                rows += section_rows
                side_total = [a + b for a, b in zip(side_total, section_total)]
            side_totals[side] = side_total
            rows.append({"style": "total", "code": "", "label": {"aktif": "AKTİF TOPLAMI", "pasif": "PASİF TOPLAMI"}[side], "values": side_total})

        warnings = []
        notes = []
        for index, period in enumerate(periods):
            difference = side_totals["aktif"][index] - side_totals["pasif"][index]
            if rounding(difference):
                warnings.append(_("Assets and liabilities differ by %(amount)s at %(date)s; see the balances outside the balance sheet below.",
                                  amount=self._format(difference), date=_fmt_date(dates[index])))
            for code, name, balance in period["others"]:
                notes.append("%s  %s %s: %s" % (_fmt_date(dates[index]), code, name, self._format(balance)))
        return {
            "kind": "bilanco",
            "title": "BİLANÇO",
            "period": _fmt_date(date_to),
            "columns": [_("Current Period (%s)", _fmt_date(dates[0]))] + ([_("Previous Period (%s)", _fmt_date(dates[1]))] if width > 1 else []),
            "rows": rows,
            "notes": notes,
            "warnings": warnings,
        }

    def _income_sums(self, company, date_from, date_to, states):
        sums = self._sums(company, date_from, date_to, states)
        info = self._account_info(company, sums)
        closing = [a for a in sums if (account_number(info[a]["code"]) or "") in CLOSING_PREFIXES]
        if closing:
            sums = self._sums(company, date_from, date_to, states, exclude_accounts=closing)
        return self._balances_by_prefix(company, sums)

    def _income_statement(self, company, options):
        date_from = fields.Date.to_date(options["date_from"])
        date_to = fields.Date.to_date(options["date_to"])
        if date_from > date_to:
            raise UserError(_("The start date must be before the end date."))
        states = self._states(options.get("include_draft"))
        ranges = [(date_from, date_to)]
        if options.get("compare"):
            ranges.append((date_from - relativedelta(years=1), date_to - relativedelta(years=1)))
        periods = [self._income_sums(company, start, end, states) for start, end in ranges]
        rounding = company.currency_id.round
        width = len(periods)

        rows = []
        running = [0.0] * width
        for letter, label, sources in INCOME_LAYOUT:
            title = "%s. %s" % (letter, label) if letter else label
            if sources is None:
                rows.append({"style": "subtotal", "code": "", "label": title, "values": list(running)})
                continue
            lines = []
            for source in sources:
                if len(source) == 3 or source[0] == "6":
                    prefixes = sorted({p for by_prefix, _n, _o in periods for p in by_prefix if p.startswith(source)})
                    for prefix in prefixes:
                        values = [-by_prefix.get(prefix, 0.0) for by_prefix, _n, _o in periods]
                        if any(rounding(v) for v in values):
                            number = line_number(prefix)
                            name = self._label(prefix, periods[0][1].get(prefix))
                            lines.append({"style": "line", "code": prefix, "label": "%s. %s" % (number, name) if number else name, "values": values})
                else:  # 7/A and 7/B groups: one line with the balance not yet transferred
                    values = [-sum(v for p, v in by_prefix.items() if p[:2] == source) for by_prefix, _n, _o in periods]
                    if any(rounding(v) for v in values):
                        lines.append({"style": "line", "code": source, "label": COST_GROUP_LABELS[source], "values": values})
            total = [sum(line["values"][i] for line in lines) for i in range(width)]
            running = [a + b for a, b in zip(running, total)]
            rows.append({"style": "group", "code": "", "label": title, "values": total})
            rows += lines
        rows[-1]["style"] = "total"

        notes = []
        warnings = []
        for index, (by_prefix, names, others) in enumerate(periods):
            outside = others + [(p, self._label(p, names.get(p)), by_prefix[p]) for p in sorted(by_prefix)
                                if p[0] in "67" and not _is_income_mapped(p) and rounding(by_prefix[p])]
            for code, name, balance in outside:
                notes.append("%s - %s  %s %s: %s" % (_fmt_date(ranges[index][0]), _fmt_date(ranges[index][1]), code, name, self._format(balance)))
        if notes:
            warnings.append(_("Some balances have no place in the income statement form and are listed below."))
        return {
            "kind": "gelir",
            "title": "GELİR TABLOSU",
            "period": "%s - %s" % (_fmt_date(date_from), _fmt_date(date_to)),
            "columns": [_("Current Period")] + ([_("Previous Period")] if width > 1 else []),
            "column_periods": ["%s - %s" % (_fmt_date(a), _fmt_date(b)) for a, b in ranges],
            "rows": rows,
            "notes": notes,
            "warnings": warnings,
        }

    # ------------------------------------------------------------ helpers
    @api.model
    def _format(self, value, blank_zero=False):
        """Turkish number format: 1.234.567,89; negatives in parentheses."""
        if value is None:
            return ""
        if abs(value) < 0.005:
            return "" if blank_zero else "0,00"
        text = "{:,.2f}".format(abs(value)).replace(",", " ").replace(".", ",").replace(" ", ".")
        return "(%s)" % text if value < 0 else text
