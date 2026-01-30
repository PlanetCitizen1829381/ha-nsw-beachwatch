from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the NSW Beachwatch binary sensor platform."""
    api = hass.data[DOMAIN][entry.entry_id]
    beach_name = entry.data["beach_name"]
    
    async_add_entities([NSWBeachwatchBinarySensor(api, beach_name, entry.entry_id)], True)

class NSWBeachwatchBinarySensor(BinarySensorEntity):
    """Binary sensor for swimming safety."""

    def __init__(self, api, beach_name, entry_id):
        """Initialize the binary sensor."""
        self._api = api
        self._beach_name = beach_name
        self._attr_unique_id = f"{entry_id}_safety"
        self._attr_name = f"{beach_name} Swimming Safety"
        self._attr_device_class = BinarySensorDeviceClass.SAFETY
        self._is_on = None  # In SAFETY class: ON = Unsafe, OFF = Safe

    @property
    def is_on(self) -> bool:
        """Return True if the beach is UNSAFE (Pollution likely)."""
        return self._is_on

    async def async_update(self) -> None:
        """Fetch new state data."""
        data = await self._api.get_beach_status(self._beach_name)
        if data:
            status = data.get("pollution_status", "").lower()
            # "likely" means pollution is present, so the SAFETY sensor turns ON (Unsafe)
            self._is_on = "likely" in status
