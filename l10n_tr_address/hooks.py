from odoo import SUPERUSER_ID, api
# Address format of Türkiye in Odoo's base data, restored on uninstall
BASE_ADDRESS_FORMAT = "%(street)s\n%(street2)s\n%(city)s %(state_name)s %(zip)s\n%(country_name)s"


def _post_init(env):
    """Match the existing Turkish contacts to their district."""
    partners = env["res.partner"].with_context(active_test=False).search(
        env["res.partner"]._l10n_tr_unmatched_domain()
    )
    partners._l10n_tr_match_districts()


def uninstall_hook(env):
    env.ref("base.tr").write(
        {
            "enforce_cities": False,
            "state_required": False,
            "address_format": BASE_ADDRESS_FORMAT,
        }
    )


def post_init_hook(cr, registry):
    _post_init(api.Environment(cr, SUPERUSER_ID, {}))
