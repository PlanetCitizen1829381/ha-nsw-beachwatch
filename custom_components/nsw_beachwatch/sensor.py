import aiohttp
import logging
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN, CONF_BEACH_NAME

_LOGGER = logging.getLogger(__name__)

API_URL = "https://api.beachwatch.nsw.gov.au/public/sites/geojson"

async def async_setup_entry(hass, entry, async_add_entities):
    beach_name = entry.data.get(CONF_BEACH_NAME)
    async_add_entities([NSWBeachSensor(beach_name)], True)

class NSWBeachSensor(SensorEntity):
    def __init__(self, beach_name):
        self._beach_name = beach_name
        self._attr_name = f"Beachwatch {beach_name}"
        self._attr_unique_id = f"beachwatch_{beach_name.lower().replace(' ', '_')}"
        self._state = "Discovery Mode"
        self._attr_extra_state_attributes = {}

    @property
    def state(self):
        return self._state

    async def async_update(self):
        """Fetch data and log beach names."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(API_URL, timeout=15) as response:
                    if response.status == 200:
                        data = await response.json()
                        all_names = []
                        found = False

                        for feature in data.get("features", []):
                            props = feature.get("properties", {})
                            name = props.get("siteName") or props.get("site_name")
                            all_names.append(name)

                            # Check if the name matches
                            if name and self._beach_name.lower() in name.lower():
                                self._state = props.get("pollutionForecast") or props.get("forecast_status", "Clean")
                                self._attr_extra_state_attributes = {"full_name": name}
                                found = True
                                break
                        
                        # This is the "Detective" part - it prints the list to your logs
                        if not found:
                            _LOGGER.warning("Beach '%s' not found. Available sites: %s", self._beach_name, all_names)
                            self._state = "Beach Not Found"
                    else:
                        self._state = f"API Error {response.status}"
        except Exception as e:
            _LOGGER.error("Update failed: %s", e)
            self._state = "Error"
