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

    VERSION = 1

    async def _get_beaches(self):
        url = "https://api.beachwatch.nsw.gov.au/public/sites/geojson"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        beaches = sorted({
                            feature["properties"]["siteName"]
                            for feature in data.get("features", [])
                            if feature["properties"].get("siteName")
                        })
                        return beaches
        except Exception:
            return []
        return []

    async def async_step_user(self, user_input=None):
        errors = {}
        beaches = await self._get_beaches()

        if user_input is not None:
            selected_beach = user_input["beach_name"]
            
            if selected_beach not in beaches:
                errors["beach_name"] = "invalid_beach"
            else:
                await self.async_set_unique_id(selected_beach)
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title=selected_beach, 
                    data={"beach_name": selected_beach}
                )

        if not beaches:
            errors["base"] = "cannot_connect"
            beaches = ["Bondi Beach", "Manly Ocean Beach"]

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("beach_name"): SelectSelector(
                    SelectSelectorConfig(
                        options=beaches,
                        mode=SelectSelectorMode.DROPDOWN,
                        custom_value=True,
                    )
                ),
            }),
            errors=errors,
        )
