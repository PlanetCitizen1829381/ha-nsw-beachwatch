"""Sensor platform for NSW Beachwatch."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import NSWBeachwatchApiClient
from .const import CONF_BEACH_NAME, DOMAIN, NAME

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform."""
    beach_name = entry.data.get(CONF_BEACH_NAME)
    session = async_get_clientsession(hass)
    client = NSWBeachwatchApiClient(session)
    
    async_add_entities([BeachwatchSensor(client, beach_name, entry)], True)

class BeachwatchSensor(SensorEntity):
    """Representation of a Beachwatch sensor."""

    def __init__(self, client, beach_name, entry):
        """Initialize the sensor."""
        self._client = client
        self._beach_name = beach_name
        self._attr_name = f"{beach_name} Water Quality"
        self._attr_unique_id = f"{entry.entry_id}_water_quality"
        self._state = None
        self._extra_attributes = {}

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._extra_attributes

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        if "Likely" in str(self._state):
            return "mdi:alert-circle"
        return "mdi:waves"

    async def async_update(self):
        """Fetch new state data for the sensor."""
        data = await self._client.async_get_data(self._beach_name)
        if data:
            self._state = data.get("forecast_title")
            self._extra_attributes = {
                "summary": data.get("forecast_summary"),
                "beach_grade": data.get("beach_grade"),
                "last_tested": data.get("last_tested"),
                "site_name": data.get("site_name"),
            }
