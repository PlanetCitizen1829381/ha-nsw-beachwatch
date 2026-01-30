import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_BEACH_NAME

class NSWBeachwatchConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for NSW Beachwatch."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_BEACH_NAME], 
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_BEACH_NAME): str,
                }
            ),
            errors=errors,
        )
