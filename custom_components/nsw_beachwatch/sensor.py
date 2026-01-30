import logging
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN
from .api import BeachwatchAPI

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=30)

async def async_setup_entry(hass, entry, async_add_entities):
    beach_name = entry.data.get("beach_name")
    # Pull the API client created in __init__.py
    api = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([NSWBeachwatchSensor(api, beach_name)], True)

class NSWBeachwatchSensor(SensorEntity):
    def __init__(self, api, beach_name):
        self._api = api
        self._beach_name = beach_name
        self._attr_name = f"Beachwatch {beach_name}"
        self._attr_unique_id = f"bw_{beach_name.lower().replace(' ', '_')}"
        self._state = "Unknown"
        self._attr_extra_state_attributes = {}

    async def async_update(self):
        props = await self._api.get_beach_data(self._beach_name)
        
        if not props:
            self._state = "No Data"
            return

        forecast = props.get("pollutionForecast", "Unknown")
        self._state = forecast

        # Determine advice based on the API response
        if "Unlikely" in forecast:
            suitability, advice = "Suitable", "Enjoy your swim!"
        elif "Possible" in forecast:
            suitability, advice = "Caution", "Pollution is possible."
        elif "Likely" in forecast:
            suitability, advice = "Unsuitable", "Avoid swimming today."
        else:
            suitability, advice = "Unknown", "No forecast available."

        self._attr_extra_state_attributes = {
            "swimming_suitability": suitability,
            "swimming_advice": advice,
            "star_rating": props.get("latestResultRating"),
            "latest_result": props.get("latestResult"),
            "last_sampled": props.get("latestResultObservationDate"),
        }
