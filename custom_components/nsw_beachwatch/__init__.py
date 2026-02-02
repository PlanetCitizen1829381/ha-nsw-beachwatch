from datetime import timedelta
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.exceptions import ConfigEntryNotReady

from .api import NSWBeachwatchAPI
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor", "binary_sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    api = NSWBeachwatchAPI(hass)
    beach_name = entry.data.get("beach_name")
    update_interval = entry.options.get("update_interval", 120)

    async def async_update_data():
        try:
            data = await api.get_beach_status(beach_name)
            if data is None:
                raise UpdateFailed(f"Unable to fetch data for {beach_name}")
            return data
        except Exception as err:
            _LOGGER.error(f"Error fetching Beachwatch data for {beach_name}: {err}")
            raise UpdateFailed(f"Error communicating with API: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"Beachwatch {beach_name}",
        update_method=async_update_data,
        update_interval=timedelta(minutes=update_interval),
    )

    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        _LOGGER.error(f"Failed to initialize Beachwatch integration for {beach_name}: {err}")
        raise ConfigEntryNotReady(f"Failed to connect to Beachwatch API: {err}")

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    entry.async_on_unload(entry.add_update_listener(update_listener))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    _LOGGER.info(f"Successfully initialized NSW Beachwatch for {beach_name}")
    return True

async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
