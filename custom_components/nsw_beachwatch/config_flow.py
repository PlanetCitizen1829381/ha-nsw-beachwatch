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
        """Fetch the list of beaches from the NSW Beachwatch API."""
        url = "https://api.beachwatch.nsw.gov.au/public/sites/geojson"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    # Extract site names and sort them alphabetically
                    beaches = [
                        feature["properties"]["siteName"]
                        for feature in data.get("features", [])
                    ]
                    return sorted(beaches)
        return []

    async def async_step_user(self, user_input=None):
        """Handle the initial step where the user selects a beach."""
        errors = {}

        if user_input is not None:
            # Set a unique ID based on the beach name to prevent duplicates
            await self.async_set_unique_id(user_input["beach_name"])
            self._abort_if_unique_id_configured()
            
            return self.async_create_entry(
                title=user_input["beach_name"], 
                data=user_input
            )

        # Fetch the list of beaches to populate the dropdown
        beaches = await self._get_beaches()
        
        if not beaches:
            errors["base"] = "cannot_connect"
            beaches = ["Bondi Beach"]  # Fallback if API fails

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("beach_name"): SelectSelector(
                    SelectSelectorConfig(
                        options=beaches,
                        mode=SelectSelectorMode.DROPDOWN,
                        translation_key="beach_name"
                    )
                ),
            }),
            errors=errors,
        )
