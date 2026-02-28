<div align="center">

![NSW Beachwatch Logo](custom_components/nsw_beachwatch/logo@2x.png)

# NSW Beachwatch Integration for Home Assistant

🌊 Real-time water quality forecasts and swimming safety advice for New South Wales beaches

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://hacs.xyz/)
[![GitHub Release](https://img.shields.io/github/v/release/PlanetCitizen1829381/ha-nsw-beachwatch?style=for-the-badge)](https://github.com/PlanetCitizen1829381/ha-nsw-beachwatch/releases)
[![License](https://img.shields.io/github/license/PlanetCitizen1829381/ha-nsw-beachwatch.svg?style=for-the-badge)](LICENSE)
[![Validate](https://img.shields.io/github/actions/workflow/status/PlanetCitizen1829381/ha-nsw-beachwatch/validate.yaml?branch=main&style=for-the-badge&label=Validate)](https://github.com/PlanetCitizen1829381/ha-nsw-beachwatch/actions/workflows/validate.yaml)

[Features](#-features) • [Installation](#-installation) • [Configuration](#%EF%B8%8F-configuration) • [Sensors](#-sensors) • [Examples](#dashboard-examples) • [Support](#-support)

</div>

---

## 🌟 Features

- **Pollution Forecasts** - Daily predictions based on rainfall and pollution events
- **Laboratory Water Quality Results** - Bacterial testing with safety ratings (1-5 stars)
- **4 Sensors Per Beach** - Comprehensive monitoring for each location
- **Dynamic Safety Icons** - Visual indicators that change based on conditions
- **GPS Coordinates** - Location data for map integrations
- **Smart Bacteria Mapping** - Converts star ratings to enterococci ranges
- **200+ NSW Beaches** - Extensive coverage across New South Wales

---

## 📦 Installation

<details>
<summary><b>Option 1: HACS (Recommended)</b></summary>

### Prerequisites
- [Home Assistant Community Store (HACS)](https://hacs.xyz/) installed

### Steps
1. Open HACS in your Home Assistant instance
2. Click on **Integrations**
3. Click the **+** button in the bottom right
4. Search for **"NSW Beachwatch"**
5. Click **Download**
6. Restart Home Assistant
7. Go to **Settings** → **Devices & Services**
8. Click **+ Add Integration**
9. Search for **"NSW Beachwatch"**
10. Follow the configuration steps

**Or use this button:**

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=PlanetCitizen1829381&repository=ha-nsw-beachwatch&category=integration)

</details>

<details>
<summary><b>Option 2: Manual Installation</b></summary>

### Steps
1. Download the latest release from the [releases page](https://github.com/PlanetCitizen1829381/ha-nsw-beachwatch/releases)
2. Extract the contents
3. Copy the `custom_components/nsw_beachwatch` folder to your Home Assistant `config/custom_components/` directory
4. Your directory structure should look like:
   ```
   config/
   └── custom_components/
       └── nsw_beachwatch/
           ├── __init__.py
           ├── api.py
           ├── config_flow.py
           ├── const.py
           ├── sensor.py
           ├── manifest.json
           ├── en.json
           └── logo@2x.png
   ```
5. Restart Home Assistant
6. Go to **Settings** → **Devices & Services**
7. Click **+ Add Integration**
8. Search for **"NSW Beachwatch"**
9. Follow the configuration steps

</details>

---

## ⚙️ Configuration

<details>
<summary><b>Adding a Beach</b></summary>

### Steps
1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **"NSW Beachwatch"**
4. Select your beach from the dropdown list (200+ beaches available)
5. Click **Submit**

The integration will create a device with 4 sensors for your selected beach.

</details>

<details>
<summary><b>Configuring Update Interval</b></summary>

### Steps
1. Go to **Settings** → **Devices & Services**
2. Find your **NSW Beachwatch** integration
3. Click **Configure**
4. Adjust the **Update Interval** (default: 120 minutes)
   - Minimum: 1 minute
   - Maximum: 1440 minutes (24 hours)
   - Recommended: 120 minutes (2 hours)
5. Click **Submit**

**Note:** NSW Beachwatch updates forecasts twice daily (6:00 AM & 1:30 PM). More frequent polling won't provide newer data.
Requests are limited to 24 per minute or you may be temporarily blocked using the API.

</details>

---

## 📊 Sensors

Each beach provides 4 sensors:

### 1. 🛟 Swimming Safety
**State Values:** `Safe` | `Caution` | `Unsafe` | `Unknown`

**Dynamic Icons:**
- `mdi:shield-check` - Safe (Pollution Unlikely)
- `mdi:shield-alert` - Caution (Pollution Possible)
- `mdi:shield-off` - Unsafe (Pollution Likely)
- `mdi:shield-off-outline` - Unknown (No Forecast Available)

**Attributes:**
- Risk Level
- Risk Meaning
- Last Official Update
- Latitude / Longitude

---

### 2. 🏊 Swimming Advice
**State:** Detailed text guidance on current swimming conditions

**Examples:**
- "Water quality is suitable for swimming. Enjoy a swim!"
- "Caution advised for swimming. Young children or elderly may be at increased risk."
- "Water quality is unsuitable for swimming. Avoid swimming today."
- "No forecast today. Check for signs of pollution before swimming."

**Attributes:**
- Risk Level
- Risk Meaning
- Last Official Update
- Latitude / Longitude

---

### 3. 🧪 Water Quality Test
**State Values:** `Good` | `Fair` | `Poor` | `Bad` | `Awaiting Lab Results`

**Attributes:**
- **Enterococci Level** - Bacteria range based on star rating
- **Water Quality Description** - Official NSW interpretation
- **Last Sample Date** - When water was tested

**Note:** Tests for water quality can take 2-4 days be processed & published. As such, the results will always be in the past.

#### Star Rating to Bacteria Mapping

| Stars | Bacteria Range | Description |
|-------|---------------|-------------|
| ⭐⭐⭐⭐ (4) | <41 cfu/100mL | Good - bacterial levels are safe for bathing |
| ⭐⭐⭐ (3) | 41-200 cfu/100mL | Fair - increased risk, particularly for vulnerable persons |
| ⭐⭐ (2) | 201-500 cfu/100mL | Poor - substantially increased risk of illness |
| ⭐ (1) | >500 cfu/100mL | Bad - significant risk of illness to bathers |


---

### 4. 📈 Water Quality History
**State:** 1-5 star rating based on latest sample

**Unit:** Stars

This sensor provides the numerical star rating (1-5) for historical tracking and graphing.

---

## 📅 Data Update Schedule

| Data Type | Update Frequency | Details |
|-----------|-----------------|---------|
| **Forecasts** | Twice Daily | 6:00 AM & 1:30 PM AEST/AEDT |
| **Lab Results** | As Available | Typically weekly, varies by beach |
| **Annual Grades** | Yearly | October - See [State of the Beaches Report](https://www.beachwatch.nsw.gov.au/stateOfTheBeaches) |

---
<a id="dashboard-examples"></a>
## 🖼️ Dashboard Examples


<details>
<summary><b>Short Advice Card</b></summary>

Compact view showing essential swimming safety information.

![Short Advice Example](images/NSWBW%20Advice%20Short%20-%20Example.png)

**Code Example:** [beach_advice_short_code_example.yaml](docs/examples/beach_advice_short_code_example.yaml)

</details>

<details>
<summary><b>Extended Advice Card</b></summary>

Display comprehensive swimming advice with all safety information.

![Extended Advice Example](images/NSWBW_Advice_Extende_Example.png)

**Code Example:** [beach_advice_extended_code_example.yaml](docs/examples/beach_advice_extended_code_example.yaml)

</details>

<details>
<summary><b>Flat Summary Card</b></summary>

Clean, horizontal layout showing key beach metrics.

![Flat Summary Example](images/NSWBW%20Flat%20Summary%20-%20Example.png)

**Code Example:** [flat_beach_summary_code_example.yaml](docs/examples/flat_beach_summary_code_example.yaml)

</details>

<details>
<summary><b>Map Card Integration</b></summary>

Display beach locations with safety status on an interactive map.

![Map Card Example](images/NSWBW%20Swim%20Safety%20Map%20-%20Example.png)

**Code Example:** [ha_map_card_code_example.yaml](docs/examples/ha_map_card_code_example.yaml)

</details>

---

## 🗺️ Available Beaches

The integration supports **200+ beaches** across NSW, including:

- **Sydney Region:** Bondi, Manly, Coogee, Bronte, Maroubra, Cronulla, and many more
- **Central Coast:** Terrigal, Avoca, Copacabana, etc.
- **Hunter:** Newcastle, Stockton, Redhead, etc.
- **Mid North Coast:** Port Macquarie, Forster, etc.
- **Far North Coast:** Byron Bay, Ballina, etc.
- **South Coast:** Wollongong, Kiama, Batemans Bay, etc.

The complete beach list is available in the dropdown when adding the integration.

---

## 📡 Data Source & Attribution

### Official Data Provider
Real-time monitoring data is provided by the **NSW Beachwatch program**, operated by the NSW Department of Planning and Environment.

- **API:** [NSW Beachwatch Public API](https://api.beachwatch.nsw.gov.au/public/sites/geojson)
- **Website:** [NSW Beachwatch](https://www.beachwatch.nsw.gov.au/)
- **Annual Reports:** [State of the Beaches](https://www.beachwatch.nsw.gov.au/stateOfTheBeaches)

### License
The NSW Beachwatch data is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

### Disclaimer
This integration is **not officially affiliated with or endorsed by the NSW Government**. It is an independent, community-developed tool created by [@PlanetCitizen1829381](https://github.com/PlanetCitizen1829381).

Always check official signage at the beach and follow local advice before swimming.

---

## 🐛 Support

### Reporting Issues
Found a bug? Please report it!

1. Check [existing issues](https://github.com/PlanetCitizen1829381/ha-nsw-beachwatch/issues) first
2. Create a [new issue](https://github.com/PlanetCitizen1829381/ha-nsw-beachwatch/issues/new/choose) using the bug report template
3. Include:
   - Home Assistant version
   - Integration version
   - Beach(es) affected
   - Error logs (Settings → System → Logs)

### Feature Requests
Have an idea? [Submit a feature request](https://github.com/PlanetCitizen1829381/ha-nsw-beachwatch/issues/new/choose)!

### Community Discussion
- [Home Assistant Community Forum](https://community.home-assistant.io/)
- [GitHub Discussions](https://github.com/PlanetCitizen1829381/ha-nsw-beachwatch/discussions)

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **NSW Department of Planning and Environment** - For providing the Beachwatch API and data

---

<div align="center">

**🌊 Stay safe and enjoy the surf! 🏖️**

Made with ❤️ for the Home Assistant community

[![Star this repository](https://img.shields.io/github/stars/PlanetCitizen1829381/ha-nsw-beachwatch?style=social)](https://github.com/PlanetCitizen1829381/ha-nsw-beachwatch/stargazers)

</div>







