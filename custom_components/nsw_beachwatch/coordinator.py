from datetime import timedelta
import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import NSWBeachwatchAPI

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=15)


class NSWBeachwatchDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator to manage fetching Beachwatch data."""

    def __init__(self, hass, beach_name):
        self.api = NSWBeachwatchAPI(hass)
        self.beach_name = beach_name

        super().__init__(
            hass,
            _LOGGER,
            name=f"NSW Beachwatch ({beach_name})",
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            data = await self.api.get_beach_status(self.beach_name)
            if not data:
                raise UpdateFailed("No data returned from Beachwatch API")
            return data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
