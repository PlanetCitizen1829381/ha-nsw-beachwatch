import aiohttp
import asyncio

class BeachwatchAPI:
    def __init__(self, session: aiohttp.ClientSession):
        self._session = session
        self._base_url = "https://api.beachwatch.nsw.gov.au/public/sites/geojson"

    async def get_all_beaches(self):
        try:
            async with self._session.get(self._base_url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return sorted({
                        f["properties"]["siteName"]
                        for f in data.get("features", [])
                        if f["properties"].get("siteName")
                    })
        except Exception:
            return []
        return []

    async def get_beach_data(self, beach_name):
        url = f"{self._base_url}?site_name={beach_name}"
        try:
            async with self._session.get(url, timeout=15) as response:
                if response.status == 200:
                    data = await response.json()
                    features = data.get("features", [])
                    return features[0].get("properties") if features else None
        except Exception:
            return None
        return None
