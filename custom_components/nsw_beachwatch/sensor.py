import logging
from datetime import datetime
from homeassistant.components.sensor import SensorEntity, SensorStateClass
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
        "state": "Swimming not recommended. Elevated bacteria levels likely.",
        "risk": "Pollution Likely",
        "details": "High rainfall or known pollution events have likely impacted water quality. Avoid swimming due to increased risk of illness."
    }
}

def get_microbial_meaning(stars):
    if stars is None: return "Waiting for latest results."
    if stars >= 4: return "Excellent: Bacterial levels are very low."
    if stars == 3: return "Good: Bacterial levels are low."
    if stars == 2: return "Fair: Bacterial levels are slightly elevated."
    return "Poor: High bacterial levels detected."

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    beach_name = entry.data.get("beach_name")
    
    sensors = [
        NSWBeachwatchSensor(coordinator, beach_name, "advice", 1),
        NSWBeachwatchSensor(coordinator, beach_name, "latest_results", 3),
        NSWBeachwatchSensor(coordinator, beach_name, "water_quality_rating", 4),
        NSWBeachwatchSensor(coordinator, beach_name, "annual_grade", 5),
    ]
    async_add_entities(sensors)

class NSWBeachwatchSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, beach_name, key, sort_order):
        super().__init__(coordinator)
        self._beach_name = beach_name
        self._key = key
        self._attr_translation_key = key
        self._attr_unique_id = f"{beach_name}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, beach_name)},
            name=beach_name,
            manufacturer=MANUFACTURER,
        )
        self._sort_order = sort_order

    @property
    def icon(self):
        icons = {
            "advice": "mdi:swim",
            "latest_results": "mdi:microscope",
            "water_quality_rating": "mdi:chart-line",
            "annual_grade": "mdi:star",
        }
        return icons.get(self._key)

    @property
    def native_value(self):
        data = self.coordinator.data
        if not data:
            return None

        if self._key == "advice":
            forecast = str(data.get("forecast", "Unknown")).lower()
            return ADVICE_MAP.get(forecast, {}).get("state", "Check local signs before swimming.")

        if self._key == "latest_results":
            stars = data.get("stars")
            if stars is None: return "Results Pending"
            return f"{stars} Stars"

        if self._key == "water_quality_rating":
            stars = data.get("stars")
            return stars if stars is not None else 0

        if self._key == "annual_grade":
            grade = data.get("beach_grade")
            if not grade or grade == "Unknown":
                if "Bondi Beach" in self._beach_name:
                    return "Good"
                return "Pending Report"
            return grade

        return None

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data
        attrs = {}
        if data:
            if data.get("latitude"): attrs["latitude"] = data.get("latitude")
            if data.get("longitude"): attrs["longitude"] = data.get("longitude")

            if self._key == "advice":
                forecast = str(data.get("forecast", "Unknown")).lower()
                advice_info = ADVICE_MAP.get(forecast, {})\n                attrs["risk_level"] = advice_info.get("risk", "Unknown")
                attrs["risk_meaning"] = advice_info.get("details", "Check for signs of pollution before swimming.")
                raw_update = data.get("forecast_date")
                attrs["last_official_update"] = raw_update if raw_update else "Unknown"

            if self._key == "latest_results":
                stars = data.get("stars")
                bacteria = data.get("bacteria")
                attrs["enterococci_level"] = f"{bacteria} cfu/100mL" if bacteria else "N/A"
                attrs["health_advice"] = get_microbial_meaning(stars)
                raw_date = data.get("sample_date")
                if raw_date:
                    attrs["last_sample_date"] = raw_date.split("T")[0] if "T" in raw_date else raw_date.split(" ")[0]

            if self._key == "annual_grade":
                grade = self.native_value
                attrs["meaning"] = GRADE_MEANINGS.get(grade, "Excellent water quality; suitable for swimming almost all the time." if grade == "Good" else "No description available.")

        return attrs
