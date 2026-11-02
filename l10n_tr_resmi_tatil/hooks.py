from odoo import SUPERUSER_ID, api
from datetime import date

from .models.holidays import YEARS


def _post_init(env):
    """Load the holidays from this year on for companies located in Türkiye."""
    turkey = env.ref("base.tr")
    companies = env["res.company"].search([]).filtered(lambda c: c.country_id == turkey)
    years = [year for year in YEARS if year >= date.today().year]
    env["resource.calendar.leaves"]._l10n_tr_create_public_holidays(companies, years)


def post_init_hook(cr, registry):
    _post_init(api.Environment(cr, SUPERUSER_ID, {}))
