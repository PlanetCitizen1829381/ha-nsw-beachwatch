from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    beach_name = entry.data.get("beach_name")
    async_add_entities([NSWBeachwatchBinarySensor(beach_name)], True)

class NSWBeachwatchBinarySensor(BinarySensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Swimming Safety"

    def __init__(self, beach_name):
        self._beach_name = beach_name
        self._attr_unique_id = f"bw_safe_{beach_name.lower().replace(' ', '_')}"
        self._attr_device_class = BinarySensorDeviceClass.SAFETY
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, beach_name)},
            name=beach_name,
        )

    @property
    def is_on(self):
        entity_id = f"sensor.beachwatch_{self._beach_name.lower().replace(' ', '_')}_status"
        state = self.hass.states.get(entity_id)
        return state and "Likely" in state.state
