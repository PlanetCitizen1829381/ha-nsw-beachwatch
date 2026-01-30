import logging
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=30)

async def async_setup_entry(hass, entry, async_add_entities):
    beach_name = entry.data.get("beach_name")
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

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        state_lower = str(self._state).lower()
        if "unlikely" in state_lower:
            return "mdi:beach"
        if "possible" in state_lower:
            return "mdi:alert"
        if "likely" in state_lower:
            return "mdi:alert-octagon"
        return "mdi:help-circle"

    async def async_update(self):
        props = await self._api.get_beach_data(self._beach_name)
        
        if not props:
            self._state = "No Data"
            return

        forecast = props.get("pollutionForecast", "Unknown")
        forecast_lower = forecast.lower()

        if "unlikely" in forecast_lower:
            suitability = "Suitable"
            advice = "Enjoy your swim! Water quality is likely to be good."
        elif "possible" in forecast_lower:
            suitability = "Caution"
            advice = "Caution: Water quality is usually good, but pollution is possible. High-risk groups should consider delaying."
        elif "likely" in forecast_lower:
            suitability = "Unsuitable"
            advice = "Avoid swimming: Pollution is likely. Water quality is expected to be poor."
        else:
            suitability = "Unknown"
            advice = "Forecast not available. Always check local signs before swimming."

        self._state = forecast
        self._attr_extra_state_attributes = {
            "swimming_suitability": suitability,
            "swimming_advice": advice,
            "star_rating": props.get("latestResultRating"),
            "latest_result": props.get("latestResult"),
            "last_sampled": props.get("latestResultObservationDate"),
            "forecast_updated": props.get("pollutionForecastTimeStamp"),
            "beach_id": props.get("id")
        }
