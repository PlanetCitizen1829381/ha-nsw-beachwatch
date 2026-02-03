import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.util import dt as dt_util
from datetime import datetime
from .const import DOMAIN, MANUFACTURER

_LOGGER = logging.getLogger(__name__)

STAR_RATING_MAP = {
    4: {
        "range": "<41 cfu/100mL",
        "description": "Good - bacterial levels are safe for bathing"
    },
    3: {
        "range": "41-200 cfu/100mL",
        "description": "Fair - bacterial levels indicate an increased risk of illness to bathers - particularly vulnerable persons"
    },
    2: {
        "range": "201-500 cfu/100mL",
        "description": "Poor - bacterial levels indicate a substantially increased risk of illness to bathers"
    },
    1: {
        "range": ">500 cfu/100mL",
        "description": "Bad - bacterial levels indicate a significant risk of illness to bathers"
    }
}

ADVICE_MAP = {
    "unlikely": {
        "state": "Water quality is suitable for swimming. Enjoy a swim!",
        "risk": "Pollution Unlikely",
        "details": "Microbial levels are expected to be within safe guidelines.",
        "safety": "Safe",
        "icon": "mdi:shield-check"
    },
    "possible": {
        "state": "Caution advised for swimming. Young children or elderly may be at increased risk.",
        "risk": "Pollution Possible",
        "details": "Recent rainfall may have caused temporary elevation in bacteria.",
        "safety": "Caution",
        "icon": "mdi:shield-alert"
    },
    "likely": {
        "state": "Water quality is unsuitable for swimming. Avoid swimming today.",
        "risk": "Pollution Likely",
        "details": "Bacteria levels are likely to exceed safe limits.",
        "safety": "Unsafe",
        "icon": "mdi:shield-off"
    },
    "forecast not available": {
        "state": "No forecast today. Check for signs of pollution before swimming.",
        "risk": "No Forecast",
        "details": "No predictive model is currently active for this site.",
        "safety": "Unknown",
        "icon": "mdi:shield-question"
    }
}

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = [
        BeachwatchSensor(coordinator, entry, "swimming_safety"),
        BeachwatchSensor(coordinator, entry, "advice"),
        BeachwatchSensor(coordinator, entry, "latest_results"),
        BeachwatchSensor(coordinator, entry, "water_quality_rating")
    ]
    async_add_entities(sensors)

class BeachwatchSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry, key):
        super().__init__(coordinator)
        self._key = key
        self._beach_name = entry.data["beach_name"]
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_has_entity_name = True
        self._attr_translation_key = key
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=self._beach_name,
            manufacturer=MANUFACTURER,
            model="NSW Beachwatch API",
            configuration_url="https://www.beachwatch.nsw.gov.au"
        )
        
        if key == "advice":
            self._attr_icon = "mdi:swim"
        elif key == "latest_results":
            self._attr_icon = "mdi:microscope"
        elif key == "water_quality_rating":
            self._attr_icon = "mdi:chart-line"

    @property
    def icon(self):
        if self._key == "swimming_safety":
            data = self.coordinator.data
            if data:
                forecast = str(data.get("forecast", "Unknown")).lower()
                return ADVICE_MAP.get(forecast, {}).get("icon", "mdi:shield-question")
        return self._attr_icon

    @property
    def native_unit_of_measurement(self):
        if self._key == "water_quality_rating":
            return "Stars"
        return None

    @property
    def native_value(self):
        data = self.coordinator.data
        if not data:
            return None
        forecast = str(data.get("forecast", "Unknown")).lower()
        if self._key == "swimming_safety":
            return ADVICE_MAP.get(forecast, {}).get("safety", "Unknown")
        if self._key == "advice":
            return ADVICE_MAP.get(forecast, {}).get("state", "Check local signs.")
        if self._key == "latest_results":
            result = data.get("latest_result")
            return result if result else "Awaiting Lab Results"
        if self._key == "water_quality_rating":
            return data.get("stars")
        return None

    @property
    def extra_state_attributes(self):
        attrs = {}
        data = self.coordinator.data
        if not data:
            return attrs
        
        if self._key in ["advice", "swimming_safety"]:
            lat = data.get("latitude")
            lon = data.get("longitude")
            if lat is not None and lon is not None:
                attrs["latitude"] = float(lat)
                attrs["longitude"] = float(lon)
            
            forecast = str(data.get("forecast", "Unknown")).lower()
            advice_info = ADVICE_MAP.get(forecast, {})
            attrs["risk_level"] = advice_info.get("risk", "Unknown")
            attrs["risk_meaning"] = advice_info.get("details", "Check for signs of pollution.")
            
            raw_update = data.get("forecast_date")
            if raw_update:
                dt = dt_util.parse_datetime(raw_update)
                if dt:
                    local_dt = dt_util.as_local(dt)
                    attrs["last_official_update"] = local_dt.strftime("%d-%m-%Y %I:%M:%S %p")
        
        if self._key == "latest_results":
            bacteria = data.get("bacteria")
            stars = data.get("stars")
            
            if bacteria is not None:
                try:
                    bacteria_num = float(bacteria)
                    attrs["enterococci_level"] = f"{bacteria_num} cfu/100mL"
                except (ValueError, TypeError):
                    attrs["enterococci_level"] = str(bacteria)
            elif stars is not None and stars in STAR_RATING_MAP:
                rating_info = STAR_RATING_MAP[stars]
                attrs["enterococci_level"] = rating_info["range"]
                attrs["water_quality_description"] = rating_info["description"]
            else:
                attrs["enterococci_level"] = "Not available"
            
            raw_date = data.get("sample_date")
            if raw_date:
                try:
                    date_obj = datetime.fromisoformat(raw_date.replace('Z', '+00:00'))
                    attrs["last_sample_date"] = date_obj.strftime("%d %B %Y")
                except:
                    attrs["last_sample_date"] = raw_date.split("T")[0]
        
        attrs["attribution"] = "Data provided by NSW Beachwatch"
        return attrs
