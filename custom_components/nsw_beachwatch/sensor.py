"""Sensor platform for NSW Beachwatch."""
from __future__ import annotations

import logging
from datetime import datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORM_NAME = "NSW Beachwatch"
MANUFACTURER = "NSW Government"
MODEL = "Beachwatch API"


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensors from config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        BeachwatchSensor(coordinator, entry, "swimming_safety"),
        BeachwatchSensor(coordinator, entry, "swimming_advice"),
        BeachwatchSensor(coordinator, entry, "water_quality"),
        BeachwatchSensor(coordinator, entry, "water_quality_rating"),
    ]

    async_add_entities(sensors)


class BeachwatchSensor(CoordinatorEntity, SensorEntity):
    """Representation of NSW Beachwatch sensor."""

    def __init__(self, coordinator, entry, sensor_type):
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._beach_name = entry.data["beach_name"]

        self._attr_unique_id = f"{entry.entry_id}_{sensor_type}"
        self._attr_has_entity_name = True

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=self._beach_name,
            manufacturer=MANUFACTURER,
            model=MODEL,
        )

    @property
    def name(self):
        names = {
            "swimming_safety": "Swimming Safety",
            "swimming_advice": "Swimming Advice",
            "water_quality": "Water Quality Test",
            "water_quality_rating": "Water Quality History",
        }
        return names[self._sensor_type]

    @property
    def native_unit_of_measurement(self):
        if self._sensor_type == "water_quality_rating":
            return "Stars"
        return None

    @property
    def native_value(self):
        data = self.coordinator.data
        if not data:
            return None

        forecast = (data.get("forecast") or "").lower()

        if self._sensor_type == "swimming_safety":
            if forecast == "pollution unlikely":
                return "Safe"
            if forecast == "pollution possible":
                return "Caution"
            if forecast == "pollution likely":
                return "Unsafe"
            return "Unknown"

        if self._sensor_type == "swimming_advice":
            if forecast == "pollution unlikely":
                return "Water quality is suitable for swimming. Enjoy a swim!"
            if forecast == "pollution possible":
                return "Caution advised for swimming. Young children or elderly may be at increased risk."
            if forecast == "pollution likely":
                return "Water quality is unsuitable for swimming. Avoid swimming today."
            return "No forecast today. Check for signs of pollution before swimming."

        if self._sensor_type == "water_quality":
            return data.get("latest_result") or "Awaiting Lab Results"

        if self._sensor_type == "water_quality_rating":
            return data.get("stars")

        return None

    @property
    def extra_state_attributes(self):
        """Return extra attributes."""
        data = self.coordinator.data
        if not data:
            return {}

        attrs = {}

        # Common attributes
        if data.get("latitude") is not None and data.get("longitude") is not None:
            attrs["latitude"] = float(data["latitude"])
            attrs["longitude"] = float(data["longitude"])

        if data.get("forecast_date"):
            dt = dt_util.parse_datetime(data["forecast_date"])
            if dt:
                attrs["last_official_update"] = dt_util.as_local(dt).isoformat()

        # Swimming sensors attributes
        if self._sensor_type in ["swimming_safety", "swimming_advice"]:
            attrs["risk_level"] = data.get("forecast")

        # Water quality attributes
        if self._sensor_type == "water_quality":
            if data.get("bacteria") is not None:
                attrs["enterococci_level"] = f"{data['bacteria']} cfu/100mL"

            if data.get("sample_date"):
                try:
                    dt_obj = datetime.fromisoformat(
                        data["sample_date"].replace("Z", "+00:00")
                    )
                    attrs["last_sample_date"] = dt_obj.date().isoformat()
                except Exception:
                    attrs["last_sample_date"] = data["sample_date"]

        attrs["attribution"] = "Data provided by NSW Beachwatch"
        return attrs
