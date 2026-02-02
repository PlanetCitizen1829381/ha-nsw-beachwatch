import aiohttp
import logging
import asyncio

_LOGGER = logging.getLogger(__name__)

class NSWBeachwatchAPI:
    def __init__(self):
        self.url = "https://www.beachwatch.nsw.gov.au/data/rest/sites/geomedium"
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "HomeAssistant-Beachwatch-Integration"
        }

    async def get_beach_status(self, beach_name):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url, headers=self.headers, timeout=15) as response:
                    if response.status != 200:
                        _LOGGER.error("NSW Beachwatch API returned status code %s", response.status)
                        return None
                    
                    data = await response.json()
                    
                    if not data or "features" not in data:
                        _LOGGER.error("NSW Beachwatch API returned malformed or empty data")
                        return None

                    for feature in data.get("features", []):
                        properties = feature.get("properties", {})
                        
                        if properties.get("siteName") == beach_name:
                            geometry = feature.get("geometry", {})
                            coordinates = geometry.get("coordinates", [None, None])
                            
                            longitude = coordinates[0]
                            latitude = coordinates[1]

                            return {
                                "beach_name": properties.get("siteName"),
                                "forecast": properties.get("pollutionForecast"),
                                "forecast_date": properties.get("pollutionForecastTimeStamp"),
                                "stars": properties.get("siteGradeNumerical"),
                                "bacteria": properties.get("enterococciValue"),
                                "sample_date": properties.get("sampleDate"),
                                "latitude": latitude,
                                "longitude": longitude,
                                "region": properties.get("regionName"),
                                "council": properties.get("councilName")
                            }
                            
                    _LOGGER.warning("Beach '%s' not found in NSW Beachwatch data", beach_name)
                    return None

            except asyncio.TimeoutError:
                _LOGGER.error("Timeout connecting to NSW Beachwatch API")
                return None
            except aiohttp.ClientError as e:
                _LOGGER.error("Client error connecting to NSW Beachwatch API: %s", e)
                return None
            except Exception as e:
                _LOGGER.error("Unexpected error fetching NSW Beachwatch data: %s", e)
                return None
