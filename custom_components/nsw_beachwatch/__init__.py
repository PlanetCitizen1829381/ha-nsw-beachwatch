"""The NSW Beachwatch integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up NSW Beachwatch from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # COMMENT OUT the line below until we actually create sensor.py
    # await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # COMMENT OUT the line below as well
    # return await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    return True
