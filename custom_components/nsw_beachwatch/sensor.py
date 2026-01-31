async def async_update(self):
        data = await self._api.get_beach_status(self._beach_name)
        if not data:
            return

        
        forecast = str(data.get("forecast", "")).lower()
        self._attrs["last_sample_date"] = data.get("sample_date")

        if self._key == "status":
            self._state = data.get("forecast", "Unknown")
        elif self._key == "bacteria":
            val = data.get("bacteria")
            self._state = f"{val} cfu/100mL" if val else "N/A"
        elif self._key == "stars":
            self._state = f"{data.get('stars')} Stars" if data.get("stars") else "N/A"
        elif self._key == "advice":
            
            if "unlikely" in forecast:
                self._state = "Water quality is suitable for swimming. Enjoy your swim!"
            elif "possible" in forecast:
                self._state = "Caution advised for swimming. Children or elderly may be at risk."
            elif "likely" in forecast:
                self._state = "Water quality is unsuitable for swimming. Avoid swimming today."
            else:
                self._state = "Check local signs before swimming."
