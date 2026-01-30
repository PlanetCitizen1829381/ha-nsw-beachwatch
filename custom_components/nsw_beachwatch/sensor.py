from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN, CONF_BEACH_NAME

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Beachwatch sensor platform."""
    beach_name = entry.data.get(CONF_BEACH_NAME)
    
    # We are creating a simple "placeholder" sensor first to make sure it displays
    async_add_entities([NSWBeachSensor(beach_name)], True)

class NSWBeachSensor(SensorEntity):
    """Representation of a NSW Beachwatch Sensor."""

    def __init__(self, beach_name):
        """Initialize the sensor."""
        self._beach_name = beach_name
        self._attr_name = f"Beachwatch {beach_name}"
        self._attr_unique_id = f"{beach_name}_pollution_level"
        self._attr_native_value = "Checking..." # Initial state

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return "mdi:beach"
