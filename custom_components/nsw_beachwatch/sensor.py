import aiohttp
import logging
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN, CONF_BEACH_NAME

_LOGGER = logging.getLogger(__name__)

# The Official API for NSW Beachwatch
API_URL = "https://api.beachwatch.nsw.gov.au/public/sites/geojson"

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Beachwatch sensor platform."""
    beach_name = entry.data.get(CONF_BEACH_NAME)
    async_add_entities([NSWBeachSensor(beach_name)], True)

class NSWBeachSensor(SensorEntity):
    """Representation of a NSW Beachwatch Sensor."""

    def __init__(self, beach_name):
        self._beach_name = beach_name
        self._attr_name = f"Beachwatch {beach_name}"
        self._attr_unique_id = f"beachwatch_{beach_name.lower().replace(' ', '_')}"
        self._state = "Checking..."
        self._attributes = {}

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    @property
    def icon(self):
        if "Unlikely" in str(self._state):
            return "mdi:beach"
        return "mdi:alert-circle"

    async def async_update(self):
        """Fetch data from the API."""
        try:
            async with aiohttp.ClientSession() as session:
                # We ask the API specifically for our beach name
                params = {"site_name": self._beach_name}
                async with session.get(API_URL, params=params, timeout=15) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("features"):
                            # The API returns a list of sites; we take the first match
                            site = data["features"][0]["properties"]
                            self._state = site.get("forecast_status", "Unknown")
                            self._attributes = {
                                "advice": site.get("forecast_advice"),
                                "last_updated": site.get("last_updated"),
                                "region": site.get("region_name"),
                                "full_site_name": site.get("site_name")
                            }
                        else:
                            self._state = "Beach Not Found"
                    else:
                        self._state = f"API Error {response.status}"
        except Exception as e:
            _LOGGER.error("Beachwatch Update Error: %s", e)
            self._state = "Update Failed"
