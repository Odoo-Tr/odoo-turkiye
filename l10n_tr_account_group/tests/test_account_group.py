from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.addons.l10n_tr_account_group.hooks import create_account_groups


@tagged("post_install_l10n", "post_install", "-at_install")
class TestAccountGroup(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref="l10n_tr.l10ntr_tek_duzen_hesap"):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.company = cls.company_data["company"]

    def _groups(self):
        return self.env["account.group"].search([("company_id", "=", self.company.id)])

    def test_templates(self):
        templates = self.env["account.group.template"].search(
            [("chart_template_id", "=", self.env.ref("l10n_tr.l10ntr_tek_duzen_hesap").id)]
        )
        self.assertEqual(len(templates), 64)
        self.assertEqual(len(templates.filtered(lambda t: not t.parent_id)), 8)
        self.assertTrue(all(templates.mapped("name")))

    def test_chart_creates_the_groups(self):
        groups = self._groups()
        self.assertEqual(len(groups), 64)
        cash = self.env["account.account"].search([("company_id", "=", self.company.id), ("code", "=like", "100%")], limit=1)
        self.assertEqual(cash.group_id.name, "HAZIR DEĞERLER")
        self.assertEqual(cash.group_id.parent_id.name, "DÖNEN VARLIKLAR")

    def test_hook_is_idempotent(self):
        self.assertFalse(create_account_groups(self.env, self.company))
        self.assertEqual(len(self._groups()), 64)

    def test_existing_company_gets_the_groups(self):
        self._groups().unlink()
        created = create_account_groups(self.env, self.company)
        self.assertEqual(len(created), 64)
        payables = created.filtered(lambda g: g.code_prefix_start == "32")
        self.assertEqual(payables.parent_id.code_prefix_start, "3")
        payable = self.env["account.account"].search([("company_id", "=", self.company.id), ("code", "=like", "320%")], limit=1)
        self.assertEqual(payable.group_id, payables)
