"""Config flow for NSW Beachwatch integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
)

from .api import NSWBeachwatchAPI
from .const import DOMAIN


class NswBeachwatchConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for NSW Beachwatch."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input["beach_name"])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=user_input["beach_name"],
                data=user_input
            )

        # Fetch available beaches
        try:
            api = NSWBeachwatchAPI(self.hass)
            beaches = await api.get_all_beaches()

            if not beaches:
                return self.async_abort(reason="cannot_connect")

        except Exception:
            errors["base"] = "cannot_connect"
            beaches = []

        if not errors:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("beach_name"): SelectSelector(
                        SelectSelectorConfig(
                            options=beaches,
                            mode=SelectSelectorMode.DROPDOWN,
                            sort=True,
                        )
                    ),
                }),
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return NswBeachwatchOptionsFlowHandler(config_entry)


class NswBeachwatchOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for NSW Beachwatch."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_interval = self.config_entry.options.get("update_interval", 120)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    "update_interval",
                    default=current_interval,
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=1,
                        max=1440,
                        unit_of_measurement="minutes",
                        mode=NumberSelectorMode.BOX,
                    )
                ),
            }),
        )
