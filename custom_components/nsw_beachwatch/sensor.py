import aiohttp
import logging
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=30)

async def async_setup_entry(hass, entry, async_add_entities):
    beach_name = entry.data.get("beach_name")
    async_add_entities([NSWBeachwatchSensor(beach_name)], True)

class NSWBeachwatchSensor(SensorEntity):
    def __init__(self, beach_name):
        self._beach_name = beach_name
        self._attr_name = f"Beachwatch {beach_name}"
        self._attr_unique_id = f"beachwatch_{beach_name.lower().replace(' ', '_')}"
        self._state = "Unknown"
        self._attr_extra_state_attributes = {}

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        if "Unlikely" in str(self._state):
            return "mdi:beach"
        return "mdi:alert-circle"

    async def async_update(self):
        url = f"https://api.beachwatch.nsw.gov.au/public/sites/geojson?site_name={self._beach_name}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=15) as response:
                    if response.status == 200:
                        data = await response.json()
                        features = data.get("features", [])
                        
                        if not features:
                            self._state = "No Data"
                            return

                        props = features[0].get("properties", {})
                        raw_forecast = props.get("pollutionForecast", "Unknown")
                        
                        if "Unlikely" in raw_forecast:
                            suitability = "Suitable"
                            advice = "Enjoy your swim! Water quality is likely to be good."
                        elif "Possible" in raw_forecast:
                            suitability = "Caution"
                            advice = "Caution: Water quality is usually good, but pollution is possible."
                        elif "Likely" in raw_forecast:
                            suitability = "Unsuitable"
                            advice = "Avoid swimming: Pollution is likely. Water quality is expected to be poor."
                        else:
                            suitability = "Unknown"
                            advice = "No forecast available. Check local signs."

                        self._state = raw_forecast
                        self._attr_extra_state_attributes = {
                            "swimming_suitability": suitability,
                            "swimming_advice": advice,
                            "star_rating": props.get("latestResultRating"),
                            "latest_result": props.get("latestResult"),
                            "last_sampled": props.get("latestResultObservationDate"),
                            "forecast_updated": props.get("pollutionForecastTimeStamp"),
                            "beach_id": props.get("id")
                        }
                    else:
                        _LOGGER.error("API Error %s", response.status)
        except Exception as e:
            _LOGGER.error("Update failed: %s", e)
