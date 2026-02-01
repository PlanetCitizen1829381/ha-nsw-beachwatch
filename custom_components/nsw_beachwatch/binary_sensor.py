from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN, MANUFACTURER

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    beach_name = entry.data.get("beach_name")
    async_add_entities([NSWBeachwatchBinarySensor(coordinator, beach_name)])

class NSWBeachwatchBinarySensor(CoordinatorEntity, BinarySensorEntity):
    _attr_has_entity_name = True
    _attr_translation_key = "swimming_safety"
    _attr_icon = "mdi:check-circle-outline"

    def __init__(self, coordinator, beach_name):
        super().__init__(coordinator)
        self._beach_name = beach_name
        self._attr_unique_id = f"{beach_name}_swimming_safety"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, beach_name)},
            name=beach_name,
            manufacturer=MANUFACTURER,
        )
        self._sort_order = 2

    @property
    def is_on(self):
        data = self.coordinator.data
        if not data:
            return None
        forecast = str(data.get("forecast", "")).lower()
        return forecast == "unlikely"
