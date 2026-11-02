def paid_time_off(env):
    """Odoo's "Paid Time Off" time type (code 016.00): the Turkish one if any, else the generic one."""
    types = env["hr.work.entry.type"].search([("code", "=", "016.00")])
    turkey = env.ref("base.tr")
    return types.filtered(lambda t: t.country_id == turkey)[:1] or types.filtered(lambda t: not t.country_id)[:1] or None


def post_init_hook(env):
    leave_type = paid_time_off(env)
    if leave_type:
        leave_type.l10n_tr_annual_leave = True
