from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, MANUFACTURER, MODEL


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([BeachwatchPollutionAlert(coordinator, entry)])


class BeachwatchPollutionAlert(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor for sewage / pollution alerts."""

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._beach_name = entry.data["beach_name"]

        self._attr_unique_id = f"{entry.entry_id}_pollution_alert"
        self._attr_has_entity_name = True
        self._attr_translation_key = "pollution_alert"
        self._attr_icon = "mdi:biohazard"
        self._attr_device_class = "problem"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=self._beach_name,
            manufacturer=MANUFACTURER,
            model=MODEL,
            configuration_url="https://www.beachwatch.nsw.gov.au"
        )

    @property
    def is_on(self):
        data = self.coordinator.data
        if not data:
            return False
        return data.get("pollution_alert", False)

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data
        if not data or not data.get("pollution_alert"):
            return {}

        return {
            "title": data.get("pollution_title"),
            "message": data.get("pollution_message"),
            "updated": data.get("pollution_updated"),
            "agency": data.get("pollution_agency"),
            "attribution": "Data provided by NSW Beachwatch",
        }
