import logging
from datetime import datetime
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

ADVICE_MAP = {
    "unlikely": {
        "state": "Water quality is suitable for swimming. Enjoy a swim!",
        "risk": "Pollution Unlikely",
        "details": "Microbial levels are expected to be within safe guidelines. No significant pollution predicted."
    },
    "possible": {
        "state": "Caution advised for swimming. Children or elderly may be at risk.",
        "risk": "Pollution Possible",
        "details": "Recent rainfall or events may have caused temporary elevation in bacteria. Water quality is usually suitable, but vulnerable groups should take care."
    },
    "likely": {
        "state": "Water quality is unsuitable for swimming. Avoid swimming today.",
        "risk": "Pollution Likely",
        "details": "High probability of faecal contamination and illness transmission. Significant risk of illness."
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

        if self._key == "advice":
            forecast = str(data.get("forecast", "Unknown")).lower()
            return ADVICE_MAP.get(forecast, {}).get("state", "No forecast available.")

        if self._key == "latest_results":
            stars = data.get("stars")
            return f"{stars} Stars" if stars else "N/A"

        if self._key == "annual_grade":
            return data.get("beach_grade", "N/A")
            
        return None

    @property
    def extra_state_attributes(self):
        attrs = {}
        data = self.coordinator.data
        if data:
            if self._key == "advice":
                forecast = str(data.get("forecast", "Unknown")).lower()
                advice_info = ADVICE_MAP.get(forecast, {})
                attrs["risk_level"] = advice_info.get("risk", "Unknown")
                attrs["risk_meaning"] = advice_info.get("details", "Check for signs of pollution before swimming.")
                attrs["last_official_update"] = data.get("forecast_date", "Unknown")

            if self._key == "latest_results":
                stars = data.get("stars")
                bacteria = data.get("bacteria")
                attrs["enterococci_level"] = f"{bacteria} cfu/100mL" if bacteria else "N/A"
                attrs["health_advice"] = get_microbial_meaning(stars)
                
                raw_date = data.get("sample_date")
                if raw_date and "T" in raw_date:
                    attrs["last_sample_date"] = raw_date.split("T")[0]
                elif raw_date and " " in raw_date:
                    attrs["last_sample_date"] = raw_date.split(" ")[0]
                else:
                    attrs["last_sample_date"] = raw_date

            if self._key == "annual_grade":
                grade = data.get("beach_grade")
                attrs["meaning"] = GRADE_MEANINGS.get(grade, "No description available.")
                
        return attrs
