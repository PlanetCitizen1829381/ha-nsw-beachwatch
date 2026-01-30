"""NSW Beachwatch API Client."""
from __future__ import annotations

import aiohttp
import async_timeout

from .const import LOGGER, API_URL

class NSWBeachwatchApiClient:
    """Class to handle the API communication."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialize the API client."""
        self._session = session

    async def async_get_data(self, beach_name: str) -> dict:
        """Get data from the API for a specific beach."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.get(API_URL)
                response.raise_for_status()
                data = await response.json()
                
                # We search the GeoJSON features for the matching beach name
                for feature in data.get("features", []):
                    props = feature.get("properties", {})
                    if props.get("site_name").lower() == beach_name.lower():
                        return props
                
                # If we get here, the beach wasn't found
                LOGGER.error("Beach '%s' not found in NSW Beachwatch data", beach_name)
                return {}

        except Exception as exception:
            LOGGER.error("Error fetching data from NSW Beachwatch: %s", exception)
            raise
