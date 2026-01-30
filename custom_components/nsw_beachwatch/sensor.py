from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    api = hass.data[DOMAIN][entry.entry_id]
    beach_name = entry.data["beach_name"]
    
    async_add_entities([NSWBeachwatchSensor(api, beach_name, entry.entry_id)], True)

class NSWBeachwatchSensor(SensorEntity):
    def __init__(self, api, beach_name, entry_id):
        self._api = api
        self._beach_name = beach_name
        self._attr_unique_id = f"{entry_id}_pollution"
        self._attr_name = f"{beach_name} Pollution Status"
        self._attr_icon = "mdi:waves"
        self._state = None
        self._attributes = {}

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    async def async_update(self) -> None:
        data = await self._api.get_beach_status(self._beach_name)
        if data:
            self._state = data.get("pollution_status")
            self._attributes = {
                "bacteria_level": data.get("bacteria_level"),
                "last_updated": data.get("last_updated"),
            }
