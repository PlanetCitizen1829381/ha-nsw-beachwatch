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
        self._target_beach = beach_name
        self._attr_name = f"Beachwatch {beach_name}"
        self._attr_unique_id = f"beachwatch_{beach_name.lower().replace(' ', '_')}"
        self._state = "Unknown"
        self._attr_extra_state_attributes = {}

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        if self._state == "Pollution Unlikely":
            return "mdi:beach"
        return "mdi:alert-circle"

    async def async_update(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(API_URL, timeout=15) as response:
                    if response.status == 200:
                        data = await response.json()
                        for feature in data.get("features", []):
                            props = feature.get("properties", {})
                            site_name = props.get("siteName", "")
                            if self._target_beach.lower() in site_name.lower():
                                self._state = props.get("pollutionForecast")
                                self._attr_extra_state_attributes = {
                                    "latest_rating": props.get("latestResult"),
                                    "star_count": props.get("latestResultRating"),
                                    "last_sampled": props.get("latestResultObservationDate"),
                                    "forecast_updated": props.get("pollutionForecastTimeStamp"),
                                    "full_site_name": site_name
                                }
                                break
        except Exception as e:
            _LOGGER.error("Beachwatch update failed: %s", e)
