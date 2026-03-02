"""The NSW Beachwatch integration."""
from __future__ import annotations

from datetime import timedelta
import asyncio
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.exceptions import ConfigEntryNotReady

from .api import NSWBeachwatchAPI
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor"]
API_BATCH_SIZE = 24
API_BATCH_WAIT = 60  # seconds between batches


async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Set up the NSW Beachwatch component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up NSW Beachwatch from a config entry."""
    api = NSWBeachwatchAPI(hass)
    beach_name = entry.data.get("beach_name")
    update_interval = entry.options.get("update_interval", 120)

    # Work out which batch slot this beach belongs to based on all configured entries
    all_entries = hass.config_entries.async_entries(DOMAIN)
    all_beach_names = [e.data.get("beach_name") for e in all_entries]
    try:
        beach_index = all_beach_names.index(beach_name)
    except ValueError:
        beach_index = 0

    batch_number = beach_index // API_BATCH_SIZE
    batch_delay = batch_number * API_BATCH_WAIT  # seconds to delay before first fetch

    async def async_update_data():
        """Fetch data from API with retry on failure."""
        data = await api.get_beach_status(beach_name)
        if data is not None:
            return data

        # First attempt failed — wait 60 seconds and retry once
        _LOGGER.warning(f"First attempt failed for {beach_name}, retrying in {API_BATCH_WAIT}s")
        await asyncio.sleep(API_BATCH_WAIT)
        data = await api.get_beach_status(beach_name)
        if data is not None:
            return data

        raise UpdateFailed(f"Unable to fetch data for {beach_name} after retry")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"Beachwatch {beach_name}",
        update_method=async_update_data,
        update_interval=timedelta(minutes=update_interval),
    )

    # Stagger startup fetches so beaches in later batches wait before their first call
    if batch_delay > 0:
        _LOGGER.debug(f"Delaying first fetch for {beach_name} by {batch_delay}s (batch {batch_number + 1})")
        await asyncio.sleep(batch_delay)

    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        _LOGGER.error(f"Failed to initialize Beachwatch for {beach_name}: {err}")
        raise ConfigEntryNotReady(f"Failed to connect to Beachwatch API: {err}")

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    entry.async_on_unload(entry.add_update_listener(update_listener))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.info(f"Successfully initialized NSW Beachwatch for {beach_name}")
    return True


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
