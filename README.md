<div align="center">

# 🌊 NSW Beachwatch for Home Assistant
**Water pollution monitoring and swimming safety for New South Wales beaches.**

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://hacs.xyz/)
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg?style=for-the-badge)](https://my.home-assistant.io/redirect/hacs_repository/?owner=PlanetCitizen1829381&repository=ha-nsw-beachwatch&category=integration)

[Features](#-features) • [Installation](#-installation) • [Configuration](#-configuration) • [Entities](#-entities) • [Data Refresh Rates](#-data-refresh-rates)

---
</div>

## ✨ Features
* **Pollution Sensor:** Direct forecast states with detailed meanings and recommended actions.
* **Swimming Advice:** Human-readable recommendations based on daily forecasts.
* **Latest Water Quality:** Consolidated laboratory results (Stars & Bacteria) in one entity.
* **Annual Beach Grade:** Long-term suitability assessment with descriptive meanings.
* **Device-Centric:** All sensors grouped under a single Beach device for a clean UI.

---

## 🚀 Installation

### Option 1: HACS (Recommended)
1. Ensure [HACS](https://hacs.xyz/) is installed.
2. Search for `NSW Beachwatch` and install.
3. Restart Home Assistant.

---

## 📊 Entities & Attributes
Each beach added creates a device with the following sensors:

### 1. Pollution Forecast & Advice
* **Pollution Forecast:** Current state (e.g., Unlikely, Possible, Likely).
    * **Attribute (`meaning`):** Full description of the predicted water quality.
    * **Attribute (`recommended_action`):** Specific guidance (e.g., "Enjoy your swim" or "Avoid swimming").
    * **Attribute (`last_updated`):** Timestamp of the latest update.
* **Swimming Advice:** Clear instruction (e.g., "Water quality is suitable for swimming. Enjoy a swim!").

### 2. Latest Water Quality (Weekly Results)
This sensor provides the results from the most recent physical water sample.
* **State:** Star Rating (e.g., `4 Stars`).
* **Attribute (`enterococci_level`):** Raw bacteria count in cfu/100mL.
* **Attribute (`health_advice`):** Official health risk meaning (e.g., "Good: Bacterial levels are safe for bathing.").
* **Attribute (`last_sample_date`):** The date the sample was collected.

### 3. Annual Beach Grade (Long-term)
This sensor provides the yearly suitability classification.
* **State:** Grade (e.g., `Very Good`, `Poor`).
* **Attribute (`meaning`):** Descriptive assessment (e.g., "Excellent water quality; suitable for swimming almost all the time.").

---

## 🔍 Pollution Forecast Reference
The real-time predictive model provides the following states:

| Response Value | Meaning | Recommended Action |
| :--- | :--- | :--- |
| **Pollution unlikely** | Water quality is predicted to be suitable for swimming. | Enjoy your swim. |
| **Pollution possible** | Caution advised; water quality is usually suitable, but high-risk groups (children, elderly) should be careful. | Consider delaying your swim. |
| **Pollution likely** | Water quality is predicted to be unsuitable for swimming. | Avoid swimming. |
| **Forecast unavailable** | No daily forecast is available for this specific site. | Check for signs of pollution manually. |

---

## ⏱️ Data Refresh Rates
| Data Type | Update Frequency | Details |
| :--- | :--- | :--- |
| **Forecasts** | **Twice Daily** | Updated at **6:00 AM** and **1:30 PM**. |
| **Lab Results** | **Weekly** | Updated as laboratory results become available. |
| **Annual Grade** | **Annually** | Updated every October in the [State of the Beaches](https://www.beachwatch.nsw.gov.au/stateOfTheBeaches) report. |

---

## 🌐 Translations
The integration uses a translation file to ensure all entities have human-readable names. You can find the latest version in `translations/en.json`. 

---

<div align="center">
  <sub>Data provided by <a href="https://www.beachwatch.nsw.gov.au">Beachwatch NSW</a>. Not officially affiliated with the NSW Government.</sub>
</div>
