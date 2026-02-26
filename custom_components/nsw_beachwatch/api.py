"""NSW Beachwatch API client with pollution alerts support - DEBUG VERSION."""
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
                    _LOGGER.error(f"GeoJSON endpoint returned status {response.status}")
                    return None
                data = await response.json()
                if not data or "features" not in data or not data["features"]:
                    _LOGGER.error(f"No features found in GeoJSON response for {beach_name}")
                    return None

                feature = data["features"][0]
                properties = feature.get("properties", {})
                geometry = feature.get("geometry", {})
                coordinates = geometry.get("coordinates", [None, None])

                # Extract site ID - try multiple possible fields
                site_id = (
                    feature.get("id") or
                    properties.get("id") or
                    properties.get("Identifier") or
                    properties.get("siteId")
                )

                _LOGGER.info(f"=== DEBUG INFO for {beach_name} ===")
                _LOGGER.info(f"Site ID extracted: {site_id}")
                _LOGGER.info(f"Site ID type: {type(site_id)}")
                _LOGGER.info(f"Feature keys: {list(feature.keys())}")
                _LOGGER.info(f"Properties keys: {list(properties.keys())}")

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

                # Try to get detailed information including alerts
                if site_id:
                    _LOGGER.info(f"Attempting to fetch site details for ID: {site_id}")
                    details = await self._get_site_details(site_id)
                    if details:
                        alerts = details.get("Alerts", [])
                        _LOGGER.info(f"Alerts found: {len(alerts)}")
                        if alerts:
                            _LOGGER.info(f"Alert details: {alerts}")
                        beach_data["alerts"] = alerts
                        beach_data["water_temp"] = details.get("WaterTemp")
                        beach_data["annual_grade"] = details.get("AnnualGrade")
                        beach_data["region"] = details.get("Region")
                        beach_data["council"] = details.get("Council")
                    else:
                        _LOGGER.warning(f"No site details returned for {site_id}")
                else:
                    _LOGGER.error(f"No site_id found for {beach_name} - cannot fetch alerts")

                _LOGGER.info(f"Final beach_data alerts: {beach_data['alerts']}")
                return beach_data

        except Exception as e:
            _LOGGER.error(f"Error fetching beach status for {beach_name}: {e}", exc_info=True)
            return None

    async def _get_site_details(self, site_id):
        """Get detailed site information including pollution alerts."""
        session = async_get_clientsession(self.hass)
        url = f"{self.base_url}/{site_id}"

        _LOGGER.info(f"Fetching site details from: {url}")

        try:
            async with session.get(url, headers=self.headers, timeout=15) as response:
                _LOGGER.info(f"Site details response status: {response.status}")
                
                if response.status != 200:
                    response_text = await response.text()
                    _LOGGER.error(f"Site details not available for {site_id}")
                    _LOGGER.error(f"Response status: {response.status}")
                    _LOGGER.error(f"Response text (first 500 chars): {response_text[:500]}")
                    return None

                details = await response.json()
                _LOGGER.info(f"Site details keys: {list(details.keys())}")
                
                # Check for alerts with various field names
                alerts = (
                    details.get("Alerts") or
                    details.get("alerts") or
                    details.get("SiteAlert") or
                    []
                )
                
                _LOGGER.info(f"Alerts in response: {alerts}")
                
                return details

        except Exception as e:
            _LOGGER.error(f"Exception fetching site details for {site_id}: {e}", exc_info=True)
            return None
