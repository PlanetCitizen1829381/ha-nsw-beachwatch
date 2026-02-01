import logging
from homeassistant.components.sensor import SensorEntity, EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN, MANUFACTURER

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    beach_name = entry.data.get("beach_name")
    
    sensors = [
        NSWBeachwatchSensor(coordinator, beach_name, "Water Pollution", "status", "mdi:waves-arrow-up"),
        NSWBeachwatchSensor(coordinator, beach_name, "Advice", "advice", "mdi:information-outline"),
        NSWBeachwatchSensor(coordinator, beach_name, "Bacteria Level", "bacteria", "mdi:microscope", EntityCategory.DIAGNOSTIC),
        NSWBeachwatchSensor(coordinator, beach_name, "Beach Grade", "stars", "mdi:star-circle", EntityCategory.DIAGNOSTIC)
    ]
    async_add_entities(sensors)

class NSWBeachwatchSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, beach_name, name_suffix, key, icon, category=None):
        super().__init__(coordinator)
        self._beach_name = beach_name
        self._key = key
        self._attr_name = name_suffix
        self._attr_icon = icon
        self._attr_entity_category = category
        self._attr_unique_id = f"{beach_name}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, beach_name)},
            name=beach_name,
            manufacturer=MANUFACTURER,
        )

    @property
    def state(self):
        data = self.coordinator.data
        if not data:
            return None

        forecast = str(data.get("forecast", "Unknown"))

        if self._key == "status":
            return forecast
        
        if self._key == "bacteria":
            val = data.get("bacteria")
            return f"{val} cfu/100mL" if val else "N/A"
            
        if self._key == "stars":
            val = data.get("stars")
            return f"{val} Stars" if val else "N/A"
            
        if self._key == "advice":
            forecast_lower = forecast.lower()
            if "unlikely" in forecast_lower:
                return "Water quality is suitable for swimming. Enjoy a swim!"
            elif "possible" in forecast_lower:
                return "Caution advised for swimming. Children or elderly may be at risk."
            elif "likely" in forecast_lower:
                return "Water quality is unsuitable for swimming. Avoid swimming today."
            return "No forecast available."
            
        return None

    @property
    def extra_state_attributes(self):
        if self.coordinator.data:
            return {"last_sample_date": self.coordinator.data.get("sample_date")}
        return {}
