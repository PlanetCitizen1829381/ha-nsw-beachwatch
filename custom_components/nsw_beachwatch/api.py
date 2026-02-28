import aiohttp
import logging
import asyncio

_LOGGER = logging.getLogger(__name__)

class NSWBeachwatchAPI:
    def __init__(self):
        self.url = "https://api.beachwatch.nsw.gov.au/public/sites/geojson"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }

    async def get_all_beaches(self):
        """Fetch all beaches for the config flow with retry and rate-limit backoff."""
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector, headers=self.headers) as session:
            for attempt in range(2):
                try:
                    async with asyncio.timeout(15):
                        async with session.get(self.url) as response:
                            if response.status == 429:
                                _LOGGER.warning("Rate limited (429) by Beachwatch API. Attempt %s failed. Waiting...", attempt + 1)
                                await asyncio.sleep(5)
                                continue
                                
                            response.raise_for_status()
                            data = await response.json()
                            beaches = []
                            for feature in data.get("features", []):
                                props = feature.get("properties", {})
                                name = props.get("siteName") or props.get("name")
                                if name:
                                    beaches.append(name)
                            
                            if beaches:
                                return sorted(list(set(beaches)))
                except (aiohttp.ClientError, asyncio.TimeoutError) as err:
                    _LOGGER.warning("Attempt %s failed to fetch beaches: %s", attempt + 1, err)
                    if attempt == 0:
                        await asyncio.sleep(2)
                except Exception as err:
                    _LOGGER.error("Unexpected error in get_all_beaches: %s", err)
                    break
        return []

    async def get_beach_status(self, beach_name):
        """Fetch status for a specific beach with network error handling."""
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector, headers=self.headers) as session:
            try:
                async with asyncio.timeout(15):
                    async with session.get(self.url) as response:
                        if response.status == 429:
                            _LOGGER.warning("Rate limited (429) while updating %s. Skipping this cycle.", beach_name)
                            return None
                            
                        response.raise_for_status()
                        data = await response.json()
                        for feature in data.get("features", []):
                            props = feature.get("properties", {})
                            if props.get("siteName") == beach_name or props.get("name") == beach_name:
                                return {
                                    "forecast": props.get("pollutionForecast", "Unknown"),
                                    "bacteria": props.get("latestResult"),
                                    "stars": props.get("latestResultRating"),
                                    "sample_date": props.get("latestResultObservationDate"),
                                }
            except asyncio.TimeoutError:
                _LOGGER.warning("Timeout fetching status for %s (API slow to respond)", beach_name)
            except aiohttp.ClientError as err:
                _LOGGER.warning("Connection error for %s: %s", beach_name, err)
            except Exception as err:
                _LOGGER.error("Unexpected error fetching status for %s: %s", beach_name, err)
        return None
