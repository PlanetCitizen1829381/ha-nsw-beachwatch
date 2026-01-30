import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)

class NSWBeachwatchAPI:
    """Interface to the NSW Beachwatch GeoJSON API."""

    def __init__(self):
        self.url = "https://api.beachwatch.nsw.gov.au/public/sites/geojson"

    async def get_all_beaches(self):
        """Fetch the list of all available beach names."""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url) as response:
                    if response.status == 200:
                        data = await response.json()
                        beaches = []
                        for feature in data.get("features", []):
                            name = feature["properties"].get("name")
                            if name:
                                beaches.append(name)
                        return sorted(beaches)
            except Exception as err:
                _LOGGER.error("Error fetching beaches: %s", err)
        return []

    async def get_beach_status(self, beach_name):
        """Fetch the current pollution status for a specific beach."""
        async with aiohttp.ClientSession() as session:
            try:
                # Query specific beach using the API parameter
                params = {"site_name": beach_name}
                async with session.get(self.url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        # The API returns a feature collection
                        for feature in data.get("features", []):
                            props = feature["properties"]
                            if props.get("name") == beach_name:
                                return {
                                    "pollution_status": props.get("pollutionStatus", "Unknown"),
                                    "bacteria_level": props.get("bacteriaLevel", "N/A"),
                                    "last_updated": props.get("lastUpdated"),
                                }
            except Exception as err:
                _LOGGER.error("Error fetching status for %s: %s", beach_name, err)
        return None
