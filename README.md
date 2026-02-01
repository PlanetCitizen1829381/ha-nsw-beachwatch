<div align="center">

<img src="custom_components/nsw_beachwatch/logo%402x.png" width="400" alt="NSW Beachwatch Logo">

# Built to work in Home Assistant
**Know before you go!** Bring real-time water quality forecasts and official safety advice for your favorite New South Wales beaches directly into your smart home dashboard.

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://hacs.xyz/)

[Features](#-features) • [Installation](#-installation) • [Configuration](#-configuration) • [Entities](#-entities) • [Data Refresh Rates](#-data-refresh-rates) • [Visual Examples](#-visual-examples)

</div>

---

## ✨ What is this?
This integration connects to the **NSW Beachwatch API** to help you make informed decisions about hitting the water.

### 🔍 How it Works
The integration pulls data from the official GeoJSON feed provided by the NSW Government. It organizes information into three distinct reporting categories:
1. **Daily Predictions:** Real-time models based on rainfall and local pollution events.
2. **Weekly Science:** Actual physical water samples tested in a laboratory.
3. **Annual Performance:** The long-term health grade of the beach over the last year.

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

---

## 📊 Sensor Breakdown
Each beach you add creates a dedicated device containing specialized sensors.

### 1. 🛟 Pollution Forecast & Advice
This sensor provides the real-time predictive model based on recent rainfall and reported pollution incidents.

| Response Value | Meaning | Recommended Action |
| :--- | :--- | :--- |
| **Pollution unlikely** | Water quality is predicted to be suitable for swimming. | Enjoy your swim. |
| **Pollution possible** | Caution advised; high-risk groups (children, elderly) should be careful. | Consider delaying your swim. |
| **Pollution likely** | Water quality is predicted to be unsuitable for swimming. | Avoid swimming. |
| **Forecast unavailable** | No daily forecast is available for this specific site. | Check for signs of pollution manually. |

### 2. 🧪 Latest Water Quality (The Lab Results)
This sensor reports the findings from the most recent physical water sample tested for Enterococci bacteria.

| Rating | Advice | Meaning |
| :--- | :--- | :--- |
| ⭐⭐⭐⭐ | **Good** | Bacterial levels are safe for bathing. |
| ⭐⭐⭐ | **Fair** | Increased risk of illness; take care. |
| ⭐⭐ | **Poor** | Substantially increased risk; not recommended. |
| ⭐ | **Bad** | High risk of illness; avoid swimming. |

### 3. 🏆 Annual Beach Grade (The Big Picture)
This provides the long-term suitability classification of the beach based on the previous year's performance.

| Grade | Description |
| :--- | :--- |
| **Very Good** | Suitable for swimming almost all the time. |
| **Good** | Suitable most of the time; susceptible after rain. |
| **Fair** | Often suitable; take care after rain or if water is murky. |
| **Poor** | Often unsuitable; always avoid swimming after rain. |
| **Very Poor** | Generally avoid swimming almost all the time. |

---

## ⏱️ Data Refresh Rates
| Data Type | Update Frequency | Details |
| :--- | :--- | :--- |
| **Forecasts** | **Twice Daily** | Updated at **6:00 AM** and **1:30 PM**. |
| **Lab Results** | **Weekly** | Updated as laboratory results become available. |
| **Annual Grade** | **Annually** | Updated every October in the [State of the Beaches](https://www.beachwatch.nsw.gov.au/stateOfTheBeaches) report. |

---

## 🖼️ Visual Examples
Here are a few ways you can display the Beachwatch data using popular custom cards like Bubble Card and Button Card.

### Bubble Card Layout
Use Bubble Cards to create a sleek, mobile-friendly overview of your local beaches.
![Bubble Card Example](https://github.com/PlanetCitizen1829381/ha-nsw-beachwatch/blob/4ce721942cec84f3910ffaee33de1b7b7d0c0a29/images/NSWBW%20-%20Bubble-Card%20Examples.png)

### Button Card Layout
Custom Button Cards are perfect for detailed grids showing bacterial levels and annual grades.
![Button Card Example](https://github.com/PlanetCitizen1829381/ha-nsw-beachwatch/blob/4ce721942cec84f3910ffaee33de1b7b7d0c0a29/images/NSWBW%20-%20Button-Card-Examples.png)

---

## 📡 Data Source & Legal
* **Data Provider:** Real-time monitoring data is provided through the official **NSW Beachwatch API**.
* **Official Reports:** Long-term grading and assessments are sourced from the NSW Government [State of the Beaches](https://www.beachwatch.nsw.gov.au/stateOfTheBeaches) report page.
* **Affiliation:** This integration is **not officially affiliated with or endorsed by the NSW Government**. It is an independent, community-driven tool.

---

<div align="center">
  <sub>🌊 Check the water, stay safe, and enjoy the surf! 🌊</sub>
</div>
