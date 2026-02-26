"""NSW Beachwatch API client with pollution alerts support - FIXED VERSION."""
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
        # Cache site IDs to avoid repeated lookups
        self._site_id_cache = {}

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

    async def _find_site_id(self, beach_name):
        """Find site ID by searching all sites."""
        # Check cache first
        if beach_name in self._site_id_cache:
            return self._site_id_cache[beach_name]
        
        session = async_get_clientsession(self.hass)
        url = f"{self.base_url}/geojson"
        
        try:
            async with session.get(url, headers=self.headers, timeout=15) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                
                for feature in data.get("features", []):
                    props = feature.get("properties", {})
                    if props.get("siteName") == beach_name:
                        # Try multiple possible ID fields
                        site_id = (
                            props.get("Identifier") or
                            props.get("identifier") or
                            props.get("id") or
                            props.get("siteId") or
                            props.get("site_id") or
                            feature.get("id")
                        )
                        if site_id:
                            self._site_id_cache[beach_name] = site_id
                            _LOGGER.info(f"Found site ID for {beach_name}: {site_id}")
                            return site_id
                
                _LOGGER.warning(f"No site ID found for {beach_name} in GeoJSON")
                return None
                
        except Exception as e:
            _LOGGER.error(f"Error finding site ID for {beach_name}: {e}")
            return None

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

                # Try to extract site ID from multiple possible fields
                site_id = (
                    properties.get("Identifier") or
                    properties.get("identifier") or
                    properties.get("id") or
                    properties.get("siteId") or
                    properties.get("site_id") or
                    feature.get("id")
                )

                # If not found in GeoJSON response, search all sites
                if not site_id:
                    _LOGGER.info(f"Site ID not in GeoJSON for {beach_name}, searching all sites...")
                    site_id = await self._find_site_id(beach_name)

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
                    details = await self._get_site_details(site_id)
                    if details:
                        beach_data["alerts"] = details.get("Alerts", [])
                        beach_data["water_temp"] = details.get("WaterTemp")
                        beach_data["annual_grade"] = details.get("AnnualGrade")
                        beach_data["region"] = details.get("Region")
                        beach_data["council"] = details.get("Council")
                        
                        if beach_data["alerts"]:
                            _LOGGER.info(f"Found {len(beach_data['alerts'])} alert(s) for {beach_name}")
                else:
                    _LOGGER.warning(f"No site_id available for {beach_name} - pollution alerts unavailable")

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
                    _LOGGER.debug(f"Site details endpoint returned {response.status} for {site_id}")
                    return None
                
                details = await response.json()
                return details

        except Exception as e:
            _LOGGER.debug(f"Could not fetch site details for {site_id}: {e}")
            return None
