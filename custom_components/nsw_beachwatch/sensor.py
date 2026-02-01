import logging
import datetime
from homeassistant.components.sensor import SensorEntity, EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN, MANUFACTURER

_LOGGER = logging.getLogger(__name__)

GRADE_MEANINGS = {
    "Very Good": "Excellent water quality; suitable for swimming almost all the time.",
    "Good": "Generally good; suitable most of the time, but susceptible to pollution after rain.",
    "Fair": "Often suitable, but extra care should be taken after any rainfall.",
    "Poor": "Susceptible to pollution; water quality is not always suitable.",
    "Very Poor": "Very susceptible to pollution; avoid swimming almost all the time.",
    "Follow Up": "Used when the sanitary inspection and water data don't match, requiring further assessment."
}

POLLUTION_MAPPING = {
    "Pollution unlikely": {
        "meaning": "Water quality is predicted to be suitable for swimming.",
        "action": "Enjoy your swim."
    },
    "Pollution possible": {
        "meaning": "Caution advised; water quality is usually suitable, but high-risk groups (children, elderly) should be careful.",
        "action": "Consider delaying your swim."
    },
    "Pollution likely": {
        "meaning": "Water quality is predicted to be unsuitable for swimming.",
        "action": "Avoid swimming."
    },
    "Forecast unavailable": {
        "meaning": "No daily forecast is available for this specific site.",
        "action": "Check for signs of pollution manually."
    }
}

def get_microbial_meaning(stars):
    mapping = {
        4: "Good: Bacterial levels are safe for bathing.",
        3: "Fair: Bacterial levels indicate an increased risk of illness.",
        2: "Poor: Bacterial levels indicate a substantially increased risk of illness.",
        1: "Bad: Bacterial levels indicate a significant risk of illness."
    }
    return mapping.get(stars, "No assessment available.")

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    beach_name = entry.data.get("beach_name")
    
    sensors = [
        NSWBeachwatchSensor(coordinator, beach_name, "pollution_forecast", "pollutionForecast", "mdi:chart-bell-curve"),
        NSWBeachwatchSensor(coordinator, beach_name, "water_pollution", "status", "mdi:waves-arrow-up"),
        NSWBeachwatchSensor(coordinator, beach_name, "advice", "advice", "mdi:information-outline"),
        NSWBeachwatchSensor(coordinator, beach_name, "latest_water_quality", "latest_results", "mdi:star-check", EntityCategory.DIAGNOSTIC),
        NSWBeachwatchSensor(coordinator, beach_name, "annual_grade", "annual_grade", "mdi:star", EntityCategory.DIAGNOSTIC)
    ]
    async_add_entities(sensors)

class NSWBeachwatchSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, beach_name, translation_key, key, icon, category=None):
        super().__init__(coordinator)
        self._beach_name = beach_name
        self._key = key
        self._attr_translation_key = translation_key
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

        if self._key == "pollutionForecast":
            return data.get("pollutionForecast", "Forecast unavailable")

        if self._key == "status":
            return str(data.get("forecast", "Unknown"))
        
        if self._key == "latest_results":
            stars = data.get("stars")
            return f"{stars} Stars" if stars else "N/A"

        if self._key == "annual_grade":
            return data.get("beach_grade", "N/A")
            
        if self._key == "advice":
            forecast = str(data.get("forecast", "Unknown")).lower()
            if "unlikely" in forecast:
                return "Water quality is suitable for swimming. Enjoy a swim!"
            elif "possible" in forecast:
                return "Caution advised for swimming. Children or elderly may be at risk."
            elif "likely" in forecast:
                return "Water quality is unsuitable for swimming. Avoid swimming today."
            return "No forecast available."
            
        return None

    @property
    def extra_state_attributes(self):
        attrs = {}
        data = self.coordinator.data
        if not data:
            return attrs

        if self._key == "pollutionForecast":
            val = self.state
            details = POLLUTION_MAPPING.get(val, POLLUTION_MAPPING["Forecast unavailable"])
            attrs["meaning"] = details["meaning"]
            attrs["recommended_action"] = details["action"]
            attrs["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if self._key == "annual_grade":
            grade = data.get("beach_grade")
            attrs["meaning"] = GRADE_MEANINGS.get(grade, "No description available.")
        
        if self._key == "latest_results":
            stars = data.get("stars")
            bacteria = data.get("bacteria")
            attrs["enterococci_level"] = f"{bacteria} cfu/100mL" if bacteria else "N/A"
            attrs["health_advice"] = get_microbial_meaning(stars)
            attrs["last_sample_date"] = data.get("sample_date")
                
        return attrs
