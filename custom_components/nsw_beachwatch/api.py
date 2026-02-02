import logging
import asyncio
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

class NSWBeachwatchAPI:
    def __init__(self, hass):
        self.hass = hass
        self.base_url = "https://api.beachwatch.nsw.gov.au/public/sites/geojson"
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "HomeAssistant-Beachwatch-Integration"
        }

    async def get_all_beaches(self):
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(self.base_url, headers=self.headers, timeout=15) as response:
                if response.status != 200:
                    return []
                data = await response.json()
                beaches = []
                for feature in data.get("features", []):
                    name = feature.get("properties", {}).get("siteName")
                    if name:
                        beaches.append(name)
                return sorted(list(set(beaches)))
        except Exception:
            return []

    async def get_beach_status(self, beach_name):
        session = async_get_clientsession(self.hass)
        url = f"{self.base_url}?site_name={beach_name.replace(' ', '%20')}"
        try:
            async with session.get(url, headers=self.headers, timeout=15) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                if not data or "features" not in data or not data["features"]:
                    return None
                feature = data["features"][0]
                properties = feature.get("properties", {})
                geometry = feature.get("geometry", {})
                coordinates = geometry.get("coordinates", [None, None])
                
                bacteria = properties.get("enterococciValue")
                if bacteria is None:
                    bacteria = properties.get("enterococci_value")

                return {
                    "beach_name": properties.get("siteName"),
                    "forecast": properties.get("pollutionForecast"),
                    "forecast_date": properties.get("pollutionForecastTimeStamp"),
                    "stars": properties.get("latestResultRating"),
                    "latest_result": properties.get("latestResult"),
                    "bacteria": bacteria,
                    "sample_date": properties.get("latestResultObservationDate"),
                    "latitude": coordinates[1],
                    "longitude": coordinates[0],
                    "region": properties.get("regionName"),
                    "council": properties.get("councilName")
                }
        except Exception:
            return None
