from odoo import fields, models, tools

from ..models.account_tax import STOPAJ_TYPES


class L10nTrStopajReport(models.Model):
    _name = "l10n_tr.stopaj.report"
    _description = "Income Tax Withholding List"
    _auto = False
    _order = "date desc, id desc"
    # Flush these fields before reading the SQL view
    _depends = {
        "account.move.line": [
            "date", "move_id", "partner_id", "company_id", "company_currency_id",
            "tax_line_id", "balance", "tax_base_amount", "parent_state",
        ],
        "account.tax": ["l10n_tr_stopaj_type", "type_tax_use"],
    }

    date = fields.Date(readonly=True)
    move_id = fields.Many2one("account.move", string="Document", readonly=True)
    move_type = fields.Selection(related="move_id.move_type", string="Document Type")
    partner_id = fields.Many2one("res.partner", string="Partner", readonly=True)
    partner_vat = fields.Char(related="partner_id.vat", string="Tax ID / TCKN")
    company_id = fields.Many2one("res.company", readonly=True)
    currency_id = fields.Many2one("res.currency", readonly=True)
    tax_id = fields.Many2one("account.tax", string="Tax", readonly=True)
    stopaj_type = fields.Selection(STOPAJ_TYPES, string="Withholding Type", readonly=True)
    direction = fields.Selection(
        [("purchase", "Withheld by us"), ("sale", "Withheld by customers")],
        readonly=True,
    )
    base_amount = fields.Monetary("Gross Amount", readonly=True)
    stopaj_amount = fields.Monetary("Withholding", readonly=True)

    def init(self):
        # Purchase side: we withhold and owe the tax office (credit). Sale side: the customer
        # withholds and we can offset it (debit). Credit notes come out negative.
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(f"""
            CREATE VIEW {self._table} AS (
                SELECT
                    aml.id,
                    aml.date,
                    aml.move_id,
                    aml.partner_id,
                    aml.company_id,
                    aml.company_currency_id AS currency_id,
                    aml.tax_line_id AS tax_id,
                    tax.l10n_tr_stopaj_type AS stopaj_type,
                    tax.type_tax_use AS direction,
                    s.amount AS stopaj_amount,
                    SIGN(s.amount) * ABS(aml.tax_base_amount) AS base_amount
                FROM account_move_line aml
                JOIN account_tax tax ON tax.id = aml.tax_line_id
                CROSS JOIN LATERAL (
                    SELECT CASE WHEN tax.type_tax_use = 'purchase' THEN -aml.balance ELSE aml.balance END AS amount
                ) s
                WHERE aml.parent_state = 'posted'
                  AND tax.l10n_tr_stopaj_type IS NOT NULL
            )
        """)
