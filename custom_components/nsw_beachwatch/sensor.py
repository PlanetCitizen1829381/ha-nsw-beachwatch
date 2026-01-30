import logging
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity, EntityCategory
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up NSW Beachwatch sensors."""
    beach_name = entry.data.get("beach_name")
    api = hass.data[DOMAIN][entry.entry_id]
    interval = entry.options.get("update_interval", 30)
    
    sensors = [
        NSWBeachwatchSensor(api, beach_name, interval, "Status", "status"),
        NSWBeachwatchSensor(api, beach_name, interval, "Advice", "advice"),
        NSWBeachwatchSensor(api, beach_name, interval, "Bacteria Count", "bacteria", EntityCategory.DIAGNOSTIC),
        NSWBeachwatchSensor(api, beach_name, interval, "Star Rating", "stars", EntityCategory.DIAGNOSTIC)
    ]
    async_add_entities(sensors, True)

class NSWBeachwatchSensor(SensorEntity):
    """Representation of a NSW Beachwatch sensor."""
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
        self._attributes = {}
        self._update_interval = timedelta(minutes=interval)

    @property
    def extra_state_attributes(self):
        return self._attributes

    @property
    def state(self):
        return self._state

    async def async_update(self):
        """Fetch data and update state."""
        data = await self._api.get_beach_status(self._beach_name)
        if not data:
            return

        self._attributes = {"last_updated": data.get("last_updated")}

        if self._key == "status":
            self._state = data.get("pollution_status")
        elif self._key == "bacteria":
            self._state = data.get("bacteria_level")
        elif self._key == "advice":
            status = str(data.get("pollution_status", "")).lower()
            if "unlikely" in status:
                self._state = "Suitable for swimming"
            elif "possible" in status:
                self._state = "Caution advised"
            else:
                self._state = "Avoid swimming"
        elif self._key == "stars":
            # Mapping star rating if available in the API data
            self._state = data.get("star_rating", "N/A")
