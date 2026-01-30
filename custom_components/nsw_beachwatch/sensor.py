import aiohttp
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

SCAN_INTERVAL = timedelta(minutes=30)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor from a config entry."""
    beach_name = entry.data["beach_name"]
    async_add_entities([NSWBeachwatchSensor(beach_name)], True)

class NSWBeachwatchSensor(SensorEntity):
    """Beachwatch sensor for a specific beach."""

    def __init__(self, beach_name):
        self._beach_name = beach_name
        self._attr_name = f"{beach_name} Pollution"
        self._attr_unique_id = f"nsw_beachwatch_{beach_name.lower().replace(' ', '_')}"
        self._state = None
        self._attributes = {}

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    async def async_update(self):
        """Fetch data for the specific beach."""
        # Use the site_name parameter to get exactly what we need
        url = f"https://api.beachwatch.nsw.gov.au/public/sites/geojson?site_name={self._beach_name}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        features = data.get("features", [])
                        
                        if not features:
                            self._state = "Unknown"
                            return

                        # Get the first match
                        props = features[0]["properties"]
                        self._state = f"Pollution {props.get('pollutionForecast', 'Unknown')}"
                        self._attributes = {
                            "latest_result": props.get("latestResult"),
                            "star_rating": props.get("latestResultRating"),
                            "last_updated": props.get("pollutionForecastTimeStamp"),
                            "site_name": props.get("siteName")
                        }
        except Exception:
            self._state = "Error"
