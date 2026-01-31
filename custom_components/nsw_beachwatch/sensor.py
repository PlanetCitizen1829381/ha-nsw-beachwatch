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
        NSWBeachwatchSensor(api, beach_name, interval, "Water Pollution", "status"),
        NSWBeachwatchSensor(api, beach_name, interval, "Advice", "advice"),
        NSWBeachwatchSensor(api, beach_name, interval, "Bacteria Level", "bacteria", EntityCategory.DIAGNOSTIC),
        NSWBeachwatchSensor(api, beach_name, interval, "Beach Grade", "stars", EntityCategory.DIAGNOSTIC)
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
            manufacturer="NSW Government",
            model="Beachwatch Site",
            configuration_url="https://www.beachwatch.nsw.gov.au",
        )
        self._state = None
        self._update_interval = timedelta(minutes=interval)
        self._attrs = {}

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attrs

    async def async_update(self):
        data = await self._api.get_beach_status(self._beach_name)
        if not data:
            return

        forecast = str(data.get("forecast", "Unknown"))
        self._attrs["last_sample_date"] = data.get("sample_date")

        if self._key == "status":
            self._state = forecast
        elif self._key == "bacteria":
            val = data.get("bacteria")
            self._state = f"{val} cfu/100mL" if val else "N/A"
        elif self._key == "stars":
            val = data.get("stars")
            self._state = f"{val} Stars" if val else "N/A"
        elif self._key == "advice":
            forecast_lower = forecast.lower()
            if "unlikely" in forecast_lower:
                self._state = "Water quality is suitable for swimming. Enjoy your swim!"
            elif "possible" in forecast_lower:
                self._state = "Caution advised for swimming. Children or elderly may be at risk."
            elif "likely" in forecast_lower:
                self._state = "Water quality is unsuitable for swimming. Avoid swimming today."
            else:
                self._state = "Check local signs before swimming."
