import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)
from .const import DOMAIN

class BeachwatchConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for NSW Beachwatch."""

    VERSION = 1

    async def _get_beaches(self):
        """Fetch the current list of beaches from NSW Beachwatch."""
        url = "https://api.beachwatch.nsw.gov.au/public/sites/geojson"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Extract and sort unique site names
                        beaches = sorted({
                            feature["properties"]["siteName"]
                            for feature in data.get("features", [])
                        })
                        return beaches
        except Exception:
            return []
        return []

    async def async_step_user(self, user_input=None):
        """Handle the beach selection step."""
        errors = {}

        if user_input is not None:
            # Prevent adding the same beach twice
            await self.async_set_unique_id(user_input["beach_name"])
            self._abort_if_unique_id_configured()
            
            return self.async_create_entry(
                title=user_input["beach_name"], 
                data=user_input
            )

        # Get the list for the dropdown
        beaches = await self._get_beaches()
        
        if not beaches:
            errors["base"] = "cannot_connect"
            # Fallback so the user isn't stuck if the API is down
            beaches = ["Bondi Beach", "Manly Ocean Beach"]

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("beach_name"): SelectSelector(
                    SelectSelectorConfig(
                        options=beaches,
                        mode=SelectSelectorMode.DROPDOWN,
                    )
                ),
            }),
            errors=errors,
        )
