from odoo import SUPERUSER_ID, api


def create_account_groups(env, company):
    """Create the groups of the Turkish chart that the company does not have yet. Returns them."""
    Group = env["account.group"].with_company(company)
    templates = env["account.group.template"].search(
        [("chart_template_id", "=", env.ref("l10n_tr.l10ntr_tek_duzen_hesap").id)]
    ).sorted(lambda t: (len(t.code_prefix_start), t.code_prefix_start))  # parents first
    groups = {}
    created = Group
    for template in templates:
        group = Group.search(
            [
                ("company_id", "=", company.id),
                ("code_prefix_start", "=", template.code_prefix_start),
                ("code_prefix_end", "=", template.code_prefix_end),
            ],
            limit=1,
        )
        if not group:
            group = Group.create(
                {
                    "name": template.name,
                    "code_prefix_start": template.code_prefix_start,
                    "code_prefix_end": template.code_prefix_end,
                    "parent_id": groups.get(template.parent_id.id, Group).id,
                    "company_id": company.id,
                }
            )
            created |= group
        groups[template.id] = group
    return created


def _post_init(env):
    """Companies that already use the Turkish chart get its groups; new ones get them with the chart."""
    template = env.ref("l10n_tr.l10ntr_tek_duzen_hesap")
    for company in env["res.company"].search([("chart_template_id", "=", template.id)]):
        create_account_groups(env, company)


def post_init_hook(cr, registry):
    _post_init(api.Environment(cr, SUPERUSER_ID, {}))
