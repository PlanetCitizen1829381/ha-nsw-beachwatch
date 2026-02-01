import aiohttp
import logging
import asyncio

_LOGGER = logging.getLogger(__name__)

class NSWBeachwatchAPI:
    def __init__(self):
        self.url = "https://api.beachwatch.nsw.gov.au/public/sites/geojson"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }

    async def get_all_beaches(self):
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector, headers=self.headers) as session:
            for attempt in range(2):
                try:
                    async with asyncio.timeout(15):
                        async with session.get(self.url) as response:
                            if response.status == 429:
                                await asyncio.sleep(5)
                                continue
                            
                            response.raise_for_status()
                            data = await response.json()
                            beaches = []
                            for feature in data.get("features", []):
                                props = feature.get("properties", {})
                                name = props.get("siteName") or props.get("name")
                                if name:
                                    beaches.append(name)
                            return sorted(list(set(beaches)))
                except Exception:
                    continue
        return []

    async def get_beach_status(self, beach_name):
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector, headers=self.headers) as session:
            try:
                async with asyncio.timeout(15):
                    async with session.get(self.url) as response:
                        if response.status == 429:
                            return None
                            
                        response.raise_for_status()
                        data = await response.json()
                        for feature in data.get("features", []):
                            props = feature.get("properties", {})
                            if props.get("siteName") == beach_name or props.get("name") == beach_name:
                                return {
                                    "id": props.get("id"),
                                    "forecast": props.get("pollutionForecast", "Unknown"),
                                    "forecast_date": props.get("pollutionForecastTimeStamp"),
                                    "bacteria": props.get("latestResult"),
                                    "stars": props.get("latestResultRating"),
                                    "beach_grade": props.get("beachGrade"),
                                    "sample_date": props.get("latestResultObservationDate"),
                                    "latitude": props.get("lat"),
                                    "longitude": props.get("lon"),
                                }
            except Exception:
                return None
        return None
