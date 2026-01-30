import logging
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity, EntityCategory
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    beach_name = entry.data.get("beach_name")
    api = hass.data[DOMAIN][entry.entry_id]
    interval = entry.options.get("update_interval", 30)
    
    sensors = [
        NSWBeachwatchSensor(api, beach_name, interval, "Pollution", "status"),
        NSWBeachwatchSensor(api, beach_name, interval, "Advice", "advice"),
        NSWBeachwatchSensor(api, beach_name, interval, "Bacteria Count", "bacteria", EntityCategory.DIAGNOSTIC),
        NSWBeachwatchSensor(api, beach_name, interval, "Star Rating", "stars", EntityCategory.DIAGNOSTIC)
    ]
    async_add_entities(sensors, True)

class NSWBeachwatchSensor(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, api, beach_name, interval, name_suffix, key, category=None):
        self._api = api
        self._beach_name = beach_name
        self._key = key
        self._attr_name = name_suffix
        self._attr_entity_category = category
        self._attr_unique_id = f"bw_{key}_{beach_name.lower().replace(' ', '_')}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, beach_name)},
            name=beach_name,
            manufacturer="NSW Beachwatch",
            model="Beach Safety Sensor",
            configuration_url="https://www.beachwatch.nsw.gov.au",
        )
        self._state = None
        self._update_interval = timedelta(minutes=interval)

    @property
    def scan_interval(self):
        return self._update_interval

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        if self._key == "status":
            state_lower = str(self._state).lower()
            if "unlikely" in state_lower: return "mdi:beach"
            if "possible" in state_lower: return "mdi:alert"
            return "mdi:alert-octagon"
        if self._key == "advice": return "mdi:information"
        if self._key == "bacteria": return "mdi:microscope"
        if self._key == "stars": return "mdi:star"
        return "mdi:help-circle"

    async def async_update(self):
        props = await self._api.get_beach_data(self._beach_name)
        if not props:
            return

        forecast = props.get("pollutionForecast", "Unknown")
        forecast_lower = forecast.lower()

        if self._key == "status":
            self._state = forecast
        elif self._key == "advice":
            if "unlikely" in forecast_lower:
                self._state = "Suitable for swimming."
            elif "possible" in forecast_lower:
                self._state = "Caution advised."
            elif "likely" in forecast_lower:
                self._state = "Avoid swimming."
            else:
                self._state = "Check local signs."
        elif self._key == "bacteria":
            self._state = f"{props.get('latestResult')} cfu/100mL"
        elif self._key == "stars":
            rating = props.get("latestResultRating")
            self._state = f"{rating} Stars" if rating else "No Rating"
