"""NSW Beachwatch sensors."""
import logging
from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.util import dt as dt_util
from datetime import datetime
from .const import DOMAIN, MANUFACTURER, MODEL

_LOGGER = logging.getLogger(__name__)

STAR_RATING_MAP = {
    4: {
        "state": "Good",
        "range": "<41 cfu/100mL",
        "description": "Good - bacterial levels are safe for bathing"
    },
    3: {
        "state": "Fair",
        "range": "41-200 cfu/100mL",
        "description": "Fair - bacterial levels indicate an increased risk of illness to bathers - particularly vulnerable persons"
    },
    2: {
        "state": "Poor",
        "range": "201-500 cfu/100mL",
        "description": "Poor - bacterial levels indicate a substantially increased risk of illness to bathers"
    },
    1: {
        "state": "Bad",
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
        "icon": "mdi:shield-off-outline"
    }
}


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up NSW Beachwatch sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = [
        BeachwatchSensor(coordinator, entry, "swimming_safety"),
        BeachwatchSensor(coordinator, entry, "advice"),
        BeachwatchSensor(coordinator, entry, "latest_results"),
        BeachwatchSensor(coordinator, entry, "water_quality_rating"),
    ]
    async_add_entities(sensors)


class BeachwatchSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Beachwatch sensor."""

    def __init__(self, coordinator, entry, key):
        """Initialize the sensor."""
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
            model=MODEL,
            configuration_url="https://www.beachwatch.nsw.gov.au"
        )

        # water_quality_rating is a numeric sensor - give it a state class so HA graphs it
        if key == "water_quality_rating":
            self._attr_state_class = SensorStateClass.MEASUREMENT

        if key == "advice":
            self._attr_icon = "mdi:swim"
        elif key == "latest_results":
            self._attr_icon = "mdi:microscope"
        elif key == "water_quality_rating":
            self._attr_icon = "mdi:chart-line"
        elif key == "swimming_safety":
            self._attr_icon = "mdi:shield-off-outline"

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        data = self.coordinator.data

        if self._key == "swimming_safety":
            if data:
                forecast = str(data.get("forecast", "")).lower()
                return ADVICE_MAP.get(forecast, {}).get("icon", "mdi:shield-off-outline")
            return "mdi:shield-off-outline"

        return self._attr_icon

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement."""
        if self._key == "water_quality_rating":
            return "Stars"
        return None

    @property
    def native_value(self):
        """Return the state of the sensor."""
        data = self.coordinator.data
        if not data:
            return None

        forecast = str(data.get("forecast", "")).lower()

        if self._key == "swimming_safety":
            return ADVICE_MAP.get(forecast, {}).get("safety", "Unknown")

        if self._key == "advice":
            return ADVICE_MAP.get(forecast, {}).get("state", "Check local signs.")

        if self._key == "latest_results":
            stars = data.get("stars")
            if stars is not None:
                try:
                    stars_int = int(stars)
                    return STAR_RATING_MAP.get(stars_int, {}).get("state", "Awaiting Lab Results")
                except (ValueError, TypeError):
                    pass
            return "Awaiting Lab Results"

        if self._key == "water_quality_rating":
            return data.get("stars")

        return None

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
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

            forecast = str(data.get("forecast", "")).lower()
            advice_info = ADVICE_MAP.get(forecast, {})
            attrs["risk_level"] = advice_info.get("risk", "Unknown")
            attrs["risk_meaning"] = advice_info.get("details", "Check for signs of pollution.")

            raw_update = data.get("forecast_date")
            if raw_update:
                dt = dt_util.parse_datetime(raw_update)
                if dt:
                    local_dt = dt_util.as_local(dt)
                    day = local_dt.day
                    month = local_dt.strftime("%B")
                    year = local_dt.year
                    hour = local_dt.hour % 12
                    if hour == 0:
                        hour = 12
                    minute = local_dt.strftime("%M")
                    second = local_dt.strftime("%S")
                    period = local_dt.strftime("%p")
                    attrs["last_official_update"] = f"{day} {month} {year} {hour}:{minute}:{second} {period}"

        if self._key == "latest_results":
            stars = data.get("stars")
            bacteria = data.get("bacteria")

            if stars is not None:
                try:
                    stars_int = int(stars)
                    rating_info = STAR_RATING_MAP.get(stars_int, {})
                    if bacteria is not None:
                        try:
                            bacteria_num = float(bacteria)
                            attrs["enterococci_level"] = f"{bacteria_num} cfu/100mL"
                        except (ValueError, TypeError):
                            attrs["enterococci_level"] = rating_info.get("range", "Not available")
                    else:
                        attrs["enterococci_level"] = rating_info.get("range", "Not available")
                    attrs["water_quality_description"] = rating_info.get("description", "Not available")
                except (ValueError, TypeError):
                    attrs["enterococci_level"] = "Not available"
                    attrs["water_quality_description"] = "Not available"
            else:
                attrs["enterococci_level"] = "Not available"
                attrs["water_quality_description"] = "Not available"

            raw_date = data.get("sample_date")
            if raw_date:
                try:
                    date_obj = datetime.fromisoformat(raw_date.replace('Z', '+00:00'))
                    attrs["last_sample_date"] = date_obj.strftime("%d %B %Y")
                except Exception:
                    attrs["last_sample_date"] = raw_date.split("T")[0]

        attrs["attribution"] = "Data provided by NSW Beachwatch"
        return attrs
