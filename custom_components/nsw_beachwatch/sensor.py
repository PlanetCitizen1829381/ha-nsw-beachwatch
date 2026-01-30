import logging
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=30)

async def async_setup_entry(hass, entry, async_add_entities):
    beach_name = entry.data.get("beach_name")
    api = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([NSWBeachwatchSensor(api, beach_name, entry.entry_id)], True)

class NSWBeachwatchSensor(SensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Status"

    def __init__(self, api, beach_name, entry_id):
        self._api = api
        self._beach_name = beach_name
        self._attr_unique_id = f"bw_stat_{beach_name.lower().replace(' ', '_')}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, beach_name)},
            name=beach_name,
            manufacturer="NSW Beachwatch",
            model="Beach Safety Sensor",
            configuration_url="https://www.beachwatch.nsw.gov.au",
        )
        self._state = "Unknown"
        self._attr_extra_state_attributes = {}

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        state_lower = str(self._state).lower()
        if "unlikely" in state_lower: return "mdi:beach"
        if "possible" in state_lower: return "mdi:alert"
        return "mdi:alert-octagon"

    async def async_update(self):
        props = await self._api.get_beach_data(self._beach_name)
        if not props:
            self._state = "No Data"
            return

        forecast = props.get("pollutionForecast", "Unknown")
        forecast_lower = forecast.lower()

        if "unlikely" in forecast_lower:
            suitability, advice = "Suitable", "Enjoy your swim! Water quality is likely to be good."
        elif "possible" in forecast_lower:
            suitability, advice = "Caution", "Caution: Water quality is usually good, but pollution is possible."
        elif "likely" in forecast_lower:
            suitability, advice = "Unsuitable", "Avoid swimming: Pollution is likely."
        else:
            suitability, advice = "Unknown", "Check local signs."

        self._state = forecast
        self._attr_extra_state_attributes = {
            "swimming_suitability": suitability,
            "swimming_advice": advice,
            "star_rating": props.get("latestResultRating"),
            "latest_result": props.get("latestResult"),
            "last_sampled": props.get("latestResultObservationDate"),
        }
