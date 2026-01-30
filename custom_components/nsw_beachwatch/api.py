import aiohttp
import logging
import asyncio

_LOGGER = logging.getLogger(__name__)

class NSWBeachwatchAPI:
    """Interface to the NSW Beachwatch GeoJSON API."""

    def __init__(self):
        self.url = "https://api.beachwatch.nsw.gov.au/public/sites/geojson"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }

    async def get_all_beaches(self):
        """Fetch the list of all available beach names."""
        
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector, headers=self.headers) as session:
            try:
                async with asyncio.timeout(10):
                    async with session.get(self.url) as response:
                        if response.status == 200:
                            data = await response.json()
                            beaches = []
                            for feature in data.get("features", []):
                                name = feature["properties"].get("siteName") or feature["properties"].get("name")
                                if name:
                                    beaches.append(name)
                            return sorted(list(set(beaches)))
                        else:
                            _LOGGER.error("API returned status %s", response.status)
            except Exception as err:
                _LOGGER.error("Error fetching beaches: %s", err)
        return []

    async def get_beach_status(self, beach_name):
        """Fetch the current pollution status for a specific beach."""
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector, headers=self.headers) as session:
            try:
                async with asyncio.timeout(10):
                    async with session.get(self.url) as response:
                        if response.status == 200:
                            data = await response.json()
                            for feature in data.get("features", []):
                                props = feature["properties"]
                                if props.get("siteName") == beach_name or props.get("name") == beach_name:
                                    return {
                                        "pollution_status": props.get("latestResult", "Unknown"),
                                        "bacteria_level": props.get("bacteriaLevel", "N/A"),
                                        "last_updated": props.get("latestResultObservationDate"),
                                    }
            except Exception as err:
                _LOGGER.error("Error fetching status for %s: %s", beach_name, err)
        return None
