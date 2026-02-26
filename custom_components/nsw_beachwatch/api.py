"""NSW Beachwatch API client with pollution alerts support."""
import logging
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)


class NSWBeachwatchAPI:
    """NSW Beachwatch API client."""

    def __init__(self, hass):
        """Initialize the API client."""
        self.hass = hass
        self.base_url = "https://api.beachwatch.nsw.gov.au/public/sites"
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "HomeAssistant-Beachwatch-Integration"
        }

    async def get_all_beaches(self):
        """Get list of all beaches."""
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(
                f"{self.base_url}/geojson",
                headers=self.headers,
                timeout=15
            ) as response:
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
        """Get comprehensive beach status including pollution alerts."""
        session = async_get_clientsession(self.hass)

        # Get basic data from GeoJSON endpoint
        url = f"{self.base_url}/geojson?site_name={beach_name.replace(' ', '%20')}"
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

                # Extract site ID
                site_id = (
                    feature.get("id") or
                    properties.get("id") or
                    properties.get("Identifier") or
                    properties.get("siteId")
                )

                # Get basic data
                latest_result_raw = properties.get("latestResult")
                bacteria_count = None
                display_result = "Unknown"

                if isinstance(latest_result_raw, dict):
                    bacteria_count = latest_result_raw.get("enterococci")
                    display_result = latest_result_raw.get("result", "Unknown")
                elif isinstance(latest_result_raw, str):
                    display_result = latest_result_raw

                beach_data = {
                    "beach_name": properties.get("siteName"),
                    "site_id": site_id,
                    "forecast": properties.get("pollutionForecast"),
                    "forecast_date": properties.get("pollutionForecastTimeStamp"),
                    "stars": properties.get("latestResultRating"),
                    "latest_result": display_result,
                    "bacteria": bacteria_count,
                    "sample_date": properties.get("latestResultObservationDate"),
                    "latitude": coordinates[1],
                    "longitude": coordinates[0],
                    "alerts": [],
                    "water_temp": None,
                    "annual_grade": None,
                    "region": None,
                    "council": None
                }

                # Get detailed information including alerts
                if site_id:
                    details = await self._get_site_details(site_id)
                    if details:
                        beach_data["alerts"] = details.get("Alerts", [])
                        beach_data["water_temp"] = details.get("WaterTemp")
                        beach_data["annual_grade"] = details.get("AnnualGrade")
                        beach_data["region"] = details.get("Region")
                        beach_data["council"] = details.get("Council")

                return beach_data

        except Exception as e:
            _LOGGER.error(f"Error fetching beach status for {beach_name}: {e}")
            return None

    async def _get_site_details(self, site_id):
        """Get detailed site information including pollution alerts."""
        session = async_get_clientsession(self.hass)
        url = f"{self.base_url}/{site_id}"

        try:
            async with session.get(url, headers=self.headers, timeout=15) as response:
                if response.status != 200:
                    _LOGGER.debug(f"Site details not available for {site_id}")
                    return None
                return await response.json()
        except Exception as e:
            _LOGGER.debug(f"Could not fetch site details for {site_id}: {e}")
            return None
