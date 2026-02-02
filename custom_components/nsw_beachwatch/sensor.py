import logging
from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN, MANUFACTURER

_LOGGER = logging.getLogger(__name__)

ADVICE_MAP = {
    "unlikely": {
        "state": "Water quality is suitable for swimming. Enjoy a swim!",
        "risk": "Pollution Unlikely",
        "details": "Microbial levels are expected to be within safe guidelines.",
        "safety": "Safe"
    },
    "possible": {
        "state": "Caution advised for swimming. Water quality is usually suitable for swimming, but young children, elderly or those with certain health conditions may be at increased risk. Consider delaying swimming until water quality improves",
        "risk": "Pollution Possible",
        "details": "Recent rainfall may have caused temporary elevation in bacteria.",
        "safety": "Caution"
    },
    "likely": {
        "state": "Water quality is unsuitable for swimming. Avoid swimming today.",
        "risk": "Pollution Likely",
        "details": "Bacteria levels are likely to exceed safe limits.",
        "safety": "Unsafe"
    },
    "forecast not available": {
        "state": "This site does not currently have any forecast information for today. Check for signs of pollution before swimming.",
        "risk": "No Forecast",
        "details": "No predictive model is currently active for this site.",
        "safety": "Unknown"
    }
}

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    beach_name = entry.data.get("beach_name")
    
    sensors = [
        NSWBeachwatchSensor(coordinator, beach_name, "advice", "mdi:swim", 1),
        NSWBeachwatchSensor(coordinator, beach_name, "swimming_safety", "mdi:shield-check", 2),
        NSWBeachwatchSensor(coordinator, beach_name, "latest_results", "mdi:microscope", 3),
        NSWBeachwatchSensor(coordinator, beach_name, "water_quality_rating", "mdi:chart-line", 4),
    ]
    async_add_entities(sensors)

class NSWBeachwatchSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, beach_name, key, icon, sort_order):
        super().__init__(coordinator)
        self._beach_name = beach_name
        self._key = key
        self._attr_icon = icon
        self._attr_translation_key = key
        self._attr_unique_id = f"{beach_name}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, beach_name)},
            name=beach_name,
            manufacturer=MANUFACTURER,
        )
        self._sort_order = sort_order
        if key == "water_quality_rating":
            self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        data = self.coordinator.data
        if not data:
            return None

        forecast = str(data.get("forecast", "Unknown")).lower()

        if self._key == "advice":
            return ADVICE_MAP.get(forecast, {}).get("state", "Check local signs.")

        if self._key == "swimming_safety":
            return ADVICE_MAP.get(forecast, {}).get("safety", "Unknown")

        if self._key == "latest_results":
            stars = data.get("stars")
            return f"{stars} Stars" if stars is not None else "Awaiting Lab Results"

        if self._key == "water_quality_rating":
            return data.get("stars")

        return None

    @property
    def extra_state_attributes(self):
        attrs = {}
        data = self.coordinator.data
        if data:
            lat = data.get("latitude")
            lon = data.get("longitude")
            if lat is not None and lon is not None:
                attrs["latitude"] = float(lat)
                attrs["longitude"] = float(lon)

            forecast = str(data.get("forecast", "Unknown")).lower()
            advice_info = ADVICE_MAP.get(forecast, {})

            if self._key in ["advice", "swimming_safety"]:
                attrs["risk_level"] = advice_info.get("risk", "Unknown")
                attrs["risk_meaning"] = advice_info.get("details", "Check for signs of pollution.")
                
                raw_update = data.get("forecast_date")
                if raw_update:
                    attrs["last_official_update"] = raw_update.split("+")[0].replace("T", " ")

            if self._key == "latest_results":
                bacteria = data.get("bacteria")
                attrs["enterococci_level"] = f"{bacteria} cfu/100mL" if bacteria else "N/A"
                raw_date = data.get("sample_date")
                if raw_date:
                    attrs["last_sample_date"] = raw_date.split("T")[0]

        return attrs
