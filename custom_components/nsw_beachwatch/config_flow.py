import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .api import NSWBeachwatchAPI
from .const import DOMAIN

class NSWBeachwatchConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        api = NSWBeachwatchAPI()

        try:
            beaches = await api.get_all_beaches()
            if not beaches:
                errors["base"] = "cannot_connect"
        except Exception:
            errors["base"] = "cannot_connect"

        if user_input is not None:
            return self.async_create_entry(
                title=user_input["beach_name"],
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("beach_name"): vol.In(beaches)
            }),
            errors=errors
        )
