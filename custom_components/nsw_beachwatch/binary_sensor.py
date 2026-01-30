from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    beach_name = entry.data.get("beach_name")
    async_add_entities([NSWBeachwatchBinarySensor(beach_name)], True)

class NSWBeachwatchBinarySensor(BinarySensorEntity):
    def __init__(self, beach_name):
        self._beach_name = beach_name
        self._attr_name = f"{beach_name} Swimming Safety"
        self._attr_unique_id = f"bw_safety_{beach_name.lower().replace(' ', '_')}"
        self._attr_device_class = BinarySensorDeviceClass.SAFETY
        self._state = False

    @property
    def is_on(self):
        entity_id = f"sensor.beachwatch_{self._beach_name.lower().replace(' ', '_')}"
        main_sensor = self.hass.states.get(entity_id)
        
        if main_sensor:
            if "Likely" in main_sensor.state:
                return True
        return False

    async def async_update(self):
        pass
