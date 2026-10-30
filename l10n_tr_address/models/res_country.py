from odoo import models


class ResCountry(models.Model):
    _inherit = "res.country"

    def _enforce_city_choice(self):
        # Odoo offers the city list on website and portal address forms only for a few countries
        if len(self) == 1 and self.code == "TR":
            return self.enforce_cities and bool(
                self.env["res.city"].search_count([("country_id", "=", self.id)], limit=1)
            )
        return super()._enforce_city_choice()
