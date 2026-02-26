import logging
import asyncio
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

class NSWBeachwatchAPI:
    def __init__(self, hass):
        self.hass = hass
        self.base_url = "https://api.beachwatch.nsw.gov.au/public/sites/geojson"
        self.details_url = "https://api.beachwatch.nsw.gov.au/public/sites"
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

    async def _get_pollution_notifications(self, site_id):
        """Fetch sewage/pollution alerts from the site details endpoint"""
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(f"{self.details_url}/{site_id}", headers=self.headers, timeout=15) as response:
                if response.status != 200:
                    return None

                data = await response.json()
                notifications = data.get("pollutionNotifications", [])

                if not notifications:
                    return None

                alert = notifications[0]

                return {
                    "pollution_alert": True,
                    "pollution_title": alert.get("title"),
                    "pollution_message": alert.get("message"),
                    "pollution_updated": alert.get("lastUpdated"),
                    "pollution_agency": alert.get("agency"),
                }

        except Exception as e:
            _LOGGER.debug(f"No pollution alert data for site {site_id}: {e}")
            return None

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

                site_id = properties.get("siteId")

                latest_result_raw = properties.get("latestResult")
                bacteria_count = None
                display_result = "Unknown"

                if isinstance(latest_result_raw, dict):
                    bacteria_count = latest_result_raw.get("enterococci")
                    display_result = latest_result_raw.get("result", "Unknown")
                elif isinstance(latest_result_raw, str):
                    display_result = latest_result_raw

                # --- NEW: Fetch sewage alerts ---
                pollution_data = None
                if site_id:
                    pollution_data = await self._get_pollution_notifications(site_id)

                if not pollution_data:
                    pollution_data = {
                        "pollution_alert": False,
                        "pollution_title": None,
                        "pollution_message": None,
                        "pollution_updated": None,
                        "pollution_agency": None,
                    }

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
                    **pollution_data,
                }

        except Exception as e:
            _LOGGER.error(f"Error fetching beach status for {beach_name}: {e}")
            return None
