"""Config flow for NSW Beachwatch integration."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)
from .api import NSWBeachwatchAPI
from .const import DOMAIN

class NSWBeachwatchConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for NSW Beachwatch."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        api = NSWBeachwatchAPI()
        
        # Fetch the real-time list of beaches from the API
        beaches = await api.get_all_beaches()

        if not beaches:
            return self.async_abort(reason="cannot_connect")

        if user_input is not None:
            return self.async_create_entry(
                title=user_input["beach"], 
                data={"beach": user_input["beach"]}
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("beach"): SelectSelector(
                    SelectSelectorConfig(
                        options=beaches,
                        mode=SelectSelectorMode.DROPDOWN,
                        # This enables the search/filter behavior
                        sort=True,
                    )
                ),
            }),
            errors=errors,
        )
