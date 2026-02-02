import aiohttp
import logging
import asyncio

_LOGGER = logging.getLogger(__name__)

class NSWBeachwatchAPI:
    def __init__(self):
        self.url = "https://www.beachwatch.nsw.gov.au/data/rest/sites/geomedium"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.beachwatch.nsw.gov.au/sites/sydney-ocean-beaches",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }

    async def get_all_beaches(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url, headers=self.headers, timeout=20) as response:
                    if response.status != 200:
                        _LOGGER.error("Beachwatch list error: %s", response.status)
                        return []
                    
                    data = await response.json(content_type=None)
                    beaches = []
                    for feature in data.get("features", []):
                        name = feature.get("properties", {}).get("siteName")
                        if name:
                            beaches.append(name)
                    return sorted(list(set(beaches)))
            except Exception as e:
                _LOGGER.error("Beachwatch connection failed: %s", e)
                return []

    async def get_beach_status(self, beach_name):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url, headers=self.headers, timeout=20) as response:
                    if response.status != 200:
                        _LOGGER.error("Beachwatch status error: %s", response.status)
                        return None
                    
                    raw_text = await response.text()
                    if not raw_text or "<!DOCTYPE html>" in raw_text:
                        _LOGGER.error("Beachwatch blocked request (received HTML instead of data)")
                        return None

                    try:
                        data = await response.json(content_type=None)
                    except Exception:
                        _LOGGER.error("JSON Error. Server sent: %s", raw_text[:300])
                        return None
                    
                    if not data or "features" not in data:
                        return None

                    for feature in data.get("features", []):
                        properties = feature.get("properties", {})
                        if properties.get("siteName") == beach_name:
                            geometry = feature.get("geometry", {})
                            coords = geometry.get("coordinates", [None, None])
                            
                            return {
                                "beach_name": properties.get("siteName"),
                                "forecast": properties.get("pollutionForecast"),
                                "forecast_date": properties.get("pollutionForecastTimeStamp"),
                                "stars": properties.get("siteGradeNumerical"),
                                "bacteria": properties.get("enterococciValue"),
                                "sample_date": properties.get("sampleDate"),
                                "latitude": coords[1],
                                "longitude": coords[0],
                                "region": properties.get("regionName"),
                                "council": properties.get("councilName")
                            }
                    return None

            except Exception as e:
                _LOGGER.error("Unexpected Beachwatch error: %s", e)
                return None
