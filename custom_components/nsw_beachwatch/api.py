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
                
                _LOGGER.warning(f"DEBUG {beach_name} - All property keys: {list(properties.keys())}")
                
                latest_result_raw = properties.get("latestResult")
                bacteria_count = None
                display_result = "Unknown"

                _LOGGER.warning(f"DEBUG {beach_name} - latestResult type: {type(latest_result_raw)}, value: {latest_result_raw}")

                if isinstance(latest_result_raw, dict):
                    _LOGGER.warning(f"DEBUG {beach_name} - latestResult dict keys: {list(latest_result_raw.keys())}")
                    bacteria_count = latest_result_raw.get("enterococci")
                    if bacteria_count is None:
                        bacteria_count = latest_result_raw.get("enterococciCount")
                    if bacteria_count is None:
                        bacteria_count = latest_result_raw.get("bacteria")
                    if bacteria_count is None:
                        bacteria_count = latest_result_raw.get("value")
                    if bacteria_count is None:
                        bacteria_count = latest_result_raw.get("enterococciBacteria")
                    if bacteria_count is None:
                        bacteria_count = latest_result_raw.get("cfu")
                    if bacteria_count is None:
                        bacteria_count = latest_result_raw.get("count")
                    display_result = latest_result_raw.get("result", "Unknown")
                elif isinstance(latest_result_raw, str):
                    display_result = latest_result_raw

                if bacteria_count is None:
                    bacteria_count = properties.get("enterococci")
                if bacteria_count is None:
                    bacteria_count = properties.get("latestResultEnterococci")
                if bacteria_count is None:
                    bacteria_count = properties.get("latestResultValue")
                if bacteria_count is None:
                    bacteria_count = properties.get("enterococciCount")
                if bacteria_count is None:
                    bacteria_count = properties.get("enterococciBacteria")
                if bacteria_count is None:
                    bacteria_count = properties.get("bacteriaCount")
                if bacteria_count is None:
                    bacteria_count = properties.get("cfuPer100ml")
                if bacteria_count is None:
                    bacteria_count = properties.get("cfu100ml")
                if bacteria_count is None:
                    bacteria_count = properties.get("latestResultCfu")
                if bacteria_count is None:
                    bacteria_count = properties.get("cfu")

                _LOGGER.warning(f"DEBUG {beach_name} - Final bacteria_count: {bacteria_count} (type: {type(bacteria_count)})")

                return {
                    "beach_name": properties.get("siteName"),
                    "forecast": properties.get("pollutionForecast"),
                    "forecast_date": properties.get("pollutionForecastTimeStamp"),
                    "stars": properties.get("latestResultRating"),
                    "latest_result": display_result,
                    "bacteria": bacteria_count,
                    "sample_date": properties.get("latestResultObservationDate"),
                    "latitude": coordinates[1],
                    "longitude": coordinates[0],
                    "region": properties.get("regionName"),
                    "council": properties.get("councilName")
                }
        except Exception as e:
            _LOGGER.error(f"Error fetching beach status for {beach_name}: {e}")
            return None
