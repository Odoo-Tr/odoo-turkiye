# Odoo's "Paid Time Off" type; its XML id changed in Odoo 19
PAID_TIME_OFF = ("hr_holidays.leave_type_paid_time_off", "hr_holidays.holiday_status_cl")


def paid_time_off(env):
    for xmlid in PAID_TIME_OFF:
        record = env.ref(xmlid, raise_if_not_found=False)
        if record:
            return record
    return None


def post_init_hook(env):
    leave_type = paid_time_off(env)
    if leave_type:
        leave_type.l10n_tr_annual_leave = True
