"""Config flow for NSW Beachwatch integration."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import CONF_BEACH_NAME, DOMAIN

class NSWBeachwatchConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for NSW Beachwatch."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Here we create the entry. The title will be the Beach Name.
            return self.async_create_entry(
                title=user_input[CONF_BEACH_NAME], 
                data=user_input
            )

        # This defines the form the user sees
        data_schema = vol.Schema(
            {
                vol.Required(CONF_BEACH_NAME): selector.TextSelector(
                    selector.TextSelectorConfig(
                        type=selector.TextSelectorType.TEXT,
                        placeholder="e.g. Bondi Beach"
                    ),
                ),
            }
        )

        return self.async_show_form(
            step_id="user", 
            data_schema=data_schema, 
            errors=errors
        )
