import logging
from homeassistant.components.sensor import SensorEntity, EntityCategory
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    beach_name = entry.data.get("beach_name")
    api = hass.data[DOMAIN][entry.entry_id]
    
    sensors = [
        NSWBeachwatchSensor(api, beach_name, "Pollution Forecast", "status"),
        NSWBeachwatchSensor(api, beach_name, "Swimming Advice", "advice"),
        NSWBeachwatchSensor(api, beach_name, "Bacteria Level", "bacteria", EntityCategory.DIAGNOSTIC),
        NSWBeachwatchSensor(api, beach_name, "Beach Grade", "stars", EntityCategory.DIAGNOSTIC)
    ]
    async_add_entities(sensors, True)

class NSWBeachwatchSensor(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, api, beach_name, name_suffix, key, category=None):
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
        data = await self._api.get_beach_status(self._beach_name)
        if not data: return

        if self._key == "status":
            self._state = data.get("forecast")
        elif self._key == "bacteria":
            val = data.get("bacteria")
            self._state = f"{val} cfu/100mL" if val else "N/A"
        elif self._key == "advice":
            forecast = str(data.get("forecast", "")).lower()
            if "unlikely" in forecast:
                self._state = "Suitable for swimming"
            elif "possible" in forecast:
                self._state = "Caution advised"
            else:
                self._state = "Avoid swimming"
        elif self._key == "stars":
            rating = data.get("stars")
            self._state = f"{rating} Stars" if rating else "N/A"
