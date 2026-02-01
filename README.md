# 🌊 NSW Beachwatch for Home Assistant
**Stop guessing. Start swimming!** Bring real-time water quality forecasts and official safety advice for your favorite New South Wales beaches directly into your smart home dashboard.

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://hacs.xyz/)
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg?style=for-the-badge)](https://my.home-assistant.io/redirect/hacs_repository/?owner=PlanetCitizen1829381&repository=ha-nsw-beachwatch&category=integration)

---

## ✨ What is this?
This integration connects to the **NSW Beachwatch API** to help you make informed decisions about hitting the water. Whether it's a quick morning dip or a weekend surf, you’ll know exactly what the experts are saying before you even leave the house.

### 🔍 How it Works
The integration pulls data from the official GeoJSON feed provided by the NSW Government. It organizes information into three distinct reporting categories:

1.  **Daily Predictions:** Real-time models based on rainfall and local pollution events.
2.  **Weekly Science:** Actual physical water samples tested in a laboratory.
3.  **Annual Performance:** The long-term health grade of the beach over the last year.

---

## 🚀 Installation

### 💎 Option 1: Automatic (HACS)
1. Click the button below to open the repository directly in HACS:
   [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg?style=for-the-badge)](https://my.home-assistant.io/redirect/hacs_repository/?owner=PlanetCitizen1829381&repository=ha-nsw-beachwatch&category=integration)
2. Click **Download**.
3. **Restart** Home Assistant.
4. Go to **Settings > Devices & Services > Add Integration** and search for `NSW Beachwatch`.

### 🛠️ Option 2: Manual
1. Download the `custom_components/nsw_beachwatch` folder from this repository.
2. Copy it into your Home Assistant `/config/custom_components/` directory.
3. **Restart** Home Assistant.
4. Add the integration via the UI: **Settings > Devices & Services > Add Integration**.

---

## 📊 Sensor Breakdown
Each beach you add creates a dedicated device containing three specialized sensors.

### 1. 🛟 Swimming Advice (The Daily Forecast)
This is your primary dashboard sensor. It translates complex pollution forecasts into a simple, human-readable recommendation.

| Feature | Details |
| :--- | :--- |
| **Main State** | Actionable advice (e.g., *"Water quality is suitable for swimming. Enjoy a swim!"*) |
| **Attribute: `risk_level`** | The predictive category: **Pollution Unlikely**, **Possible**, or **Likely**. |
| **Attribute: `risk_meaning`** | A deep-dive explanation of the current environmental risk. |
| **Attribute: `last_updated`** | Timestamp of when Home Assistant last fetched data. |
| **Update Frequency** | **Twice Daily** (Issued at 6:00 AM and 1:30 PM). |

### 2. 🧪 Latest Water Quality (The Lab Results)
This sensor reports the findings from the most recent physical water sample tested for Enterococci bacteria.

| Rating | Advice | Meaning |
| :--- | :--- | :--- |
| ⭐⭐⭐⭐ | **Good** | Bacterial levels are safe for bathing. |
| ⭐⭐⭐ | **Fair** | Increased risk of illness; take care. |
| ⭐⭐ | **Poor** | Substantially increased risk; not recommended. |
| ⭐ | **Bad** | High risk of illness; avoid swimming. |

**Additional Attributes:**
* **`enterococci_level`**: The raw bacteria count (cfu/100mL) from the laboratory.
* **`health_advice`**: The official health interpretation.
* **`last_sample_date`**: The specific date/time the water was physically sampled.
* **Update Frequency**: **Weekly** (whenever new lab results are processed).

### 3. 🏆 Annual Beach Grade (The Big Picture)
This provides the long-term suitability classification of the beach based on the previous year's performance.

| Grade | Description |
| :--- | :--- |
| **Very Good** | Suitable for swimming almost all the time. |
| **Good** | Suitable most of the time; susceptible after rain. |
| **Fair** | Often suitable; take care after rain or if water is murky. |
| **Poor** | Often unsuitable; always avoid swimming after rain. |
| **Very Poor** | Generally avoid swimming almost all the time. |

**Additional Attributes:**
* **`meaning`**: A summary of the beach's overall water quality performance.
* **Update Frequency**: **Annually** (Updated every October).

---

## 📡 Data Source & Legal
* **Data Provider:** Real-time monitoring data is provided through the official **NSW Beachwatch API**.
* **Official Reports:** Long-term grading and assessments are sourced from the NSW Government [State of the Beaches](https://www.beachwatch.nsw.gov.au/stateOfTheBeaches) report page.
* **Affiliation:** This integration is **not officially affiliated with or endorsed by the NSW Government**. It is an independent, community-driven tool.

---

<div align="center">
  <sub>Check the water, stay safe, and enjoy the surf! 🌊</sub>
</div>
