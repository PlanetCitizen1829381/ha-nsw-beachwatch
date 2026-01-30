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
        except Exception:
            errors["base"] = "cannot_connect"
            beaches = []

        if user_input is not None:
            await self.async_set_unique_id(user_input["beach_name"].lower().replace(" ", "_"))
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=user_input["beach_name"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("beach_name"): vol.In(beaches)
            }),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return NSWBeachwatchOptionsFlowHandler(config_entry)

class NSWBeachwatchOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    "update_interval",
                    default=self.config_entry.options.get("update_interval", 30),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=1440)),
            }),
        )
