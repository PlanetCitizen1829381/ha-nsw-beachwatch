import aiohttp
import asyncio

class NSWBeachwatchAPI:
    def __init__(self):
        self.url = "https://www.beachwatch.nsw.gov.au/api/sites"

    async def get_all_beaches(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                if response.status == 200:
                    data = await response.json()
                    return sorted([site["name"] for site in data if "name" in site])
                return []

    async def get_beach_status(self, beach_name):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                if response.status == 200:
                    data = await response.json()
                    for site in data:
                        if site.get("name") == beach_name:
                            return {
                                "pollution_status": site.get("pollutionStatus", "Unknown"),
                                "bacteria_level": site.get("bacteriaLevel", "N/A"),
                                "last_updated": site.get("lastUpdated"),
                            }
        return None
