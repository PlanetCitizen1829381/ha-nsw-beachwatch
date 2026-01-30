import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import SelectSelector, SelectSelectorConfig, SelectSelectorMode
from .api import BeachwatchAPI
from .const import DOMAIN

class BeachwatchConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        api = BeachwatchAPI(async_get_clientsession(self.hass))
        beaches = await api.get_all_beaches()

        if user_input is not None:
            await self.async_set_unique_id(user_input["beach_name"])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=user_input["beach_name"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("beach_name"): SelectSelector(
                    SelectSelectorConfig(options=beaches, mode=SelectSelectorMode.DROPDOWN, custom_value=True)
                ),
            }),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return BeachwatchOptionsFlowHandler(config_entry)

class BeachwatchOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional("update_interval", default=30): vol.All(vol.Coerce(int), vol.Range(min=1, max=1440)),
            })
        )
