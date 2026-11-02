import re
from collections import defaultdict

from odoo import _, api, models

# Turkish-aware folding so that "KADIKÖY", "Kadikoy" and "Kadıköy" compare equal
_FOLD = str.maketrans("çğıöşü", "cgiosu")
_SEPARATORS = re.compile(r"\s*[/,\-]\s*")


def _tr_key(value):
    value = (value or "").replace("I", "ı").replace("İ", "i").lower().translate(_FOLD)
    return " ".join(value.split())


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.onchange("state_id")
    def _onchange_state_id_l10n_tr_address(self):
        if self.city_id.state_id and self.state_id and self.city_id.state_id != self.state_id:
            self.city_id = False
            self.city = False

    @api.model
    def _l10n_tr_unmatched_domain(self):
        return [
            ("country_id", "=", self.env.ref("base.tr").id),
            ("city_id", "=", False),
            ("city", "!=", False),
        ]

    def _l10n_tr_match_districts(self):
        """Set the district (and the province when missing) from the free-text city.

        Understands "Kadıköy", "KADIKOY" and "Kadıköy / İstanbul". A district name used in
        several provinces (e.g. "Merkez") is only matched when the province is known.
        Contacts that take their address from their company are left to the address sync.
        Returns the number of contacts updated.
        """
        country = self.env.ref("base.tr")
        provinces = {
            _tr_key(state.name): state
            for state in self.env["res.country.state"].search([("country_id", "=", country.id)])
        }
        by_province = defaultdict(dict)
        by_name = defaultdict(list)
        for city in self.env["res.city"].search([("country_id", "=", country.id)]):
            by_province[city.state_id.id][_tr_key(city.name)] = city
            by_name[_tr_key(city.name)].append(city)

        updated = 0
        for partner in self:
            if (
                partner.country_id != country
                or partner.city_id
                or not partner.city
                or (partner.type == "contact" and partner.parent_id)
            ):
                continue
            parts = [part for part in _SEPARATORS.split(partner.city.strip()) if part]
            if not parts:
                continue
            name = _tr_key(parts[0])
            state = partner.state_id
            if not state and len(parts) > 1:
                state = provinces.get(_tr_key(parts[-1]), state)

            if state:
                city = by_province[state.id].get(name)
            else:
                city = by_name[name][0] if len(by_name[name]) == 1 else None

            if city:
                partner.write({"city_id": city.id, "city": city.name, "state_id": city.state_id.id})
                updated += 1
            elif state and not partner.state_id:
                partner.state_id = state
                updated += 1
            elif not state and len(parts) == 1 and name in provinces:
                # Only the province was typed into the city field
                partner.state_id = provinces[name]
                updated += 1
        return updated

    def action_l10n_tr_match_districts(self):
        updated = self._l10n_tr_match_districts()
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "type": "success" if updated else "info",
                "message": _(
                    "%(updated)s of %(total)s contacts were matched to a district or province.",
                    updated=updated,
                    total=len(self),
                ),
                "next": {"type": "ir.actions.client", "tag": "soft_reload"},
            },
        }
