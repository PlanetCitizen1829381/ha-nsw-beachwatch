import aiohttp
import logging
import asyncio

_LOGGER = logging.getLogger(__name__)

class NSWBeachwatchAPI:
    def __init__(self):
        self.url = "https://www.beachwatch.nsw.gov.au/data/rest/sites/geomedium"
        self.headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Referer": "https://www.beachwatch.nsw.gov.au/",
        }

    async def get_all_beaches(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url, headers=self.headers, timeout=15) as response:
                    if response.status != 200:
                        return []
                    
                    data = await response.json(content_type=None)
                    beaches = []
                    for feature in data.get("features", []):
                        name = feature.get("properties", {}).get("siteName")
                        if name:
                            beaches.append(name)
                    return sorted(list(set(beaches)))
            except Exception:
                return []

    async def get_beach_status(self, beach_name):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url, headers=self.headers, timeout=15) as response:
                    if response.status != 200:
                        _LOGGER.error("Beachwatch API error: Status %s", response.status)
                        return None
                    
                    text = await response.text()
                    if not text or not text.strip():
                        _LOGGER.error("Beachwatch API returned an empty response body")
                        return None

                    try:
                        data = await response.json(content_type=None)
                    except Exception as json_err:
                        _LOGGER.error("Failed to decode JSON. Raw response: %s", text[:500])
                        return None
                    
                    if not data or "features" not in data:
                        return None

                    for feature in data.get("features", []):
                        properties = feature.get("properties", {})
                        if properties.get("siteName") == beach_name:
                            geometry = feature.get("geometry", {})
                            coordinates = geometry.get("coordinates", [None, None])
                            
                            return {
                                "beach_name": properties.get("siteName"),
                                "forecast": properties.get("pollutionForecast"),
                                "forecast_date": properties.get("pollutionForecastTimeStamp"),
                                "stars": properties.get("siteGradeNumerical"),
                                "bacteria": properties.get("enterococciValue"),
                                "sample_date": properties.get("sampleDate"),
                                "latitude": coordinates[1],
                                "longitude": coordinates[0],
                                "region": properties.get("regionName"),
                                "council": properties.get("councilName")
                            }
                    return None

            except Exception as e:
                _LOGGER.error("Unexpected error in Beachwatch API: %s", e)
                return None
