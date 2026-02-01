<div align="center">

# 🌊 NSW Beachwatch for Home Assistant
**Water pollution monitoring and swimming safety for New South Wales beaches.**

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://hacs.xyz/)
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg?style=for-the-badge)](https://my.home-assistant.io/redirect/hacs_repository/?owner=PlanetCitizen1829381&repository=ha-nsw-beachwatch&category=integration)

[Features](#-features) • [Installation](#-installation) • [Configuration](#-configuration) • [Entities](#-entities) • [Data Refresh Rates](#-data-refresh-rates)

---
</div>

## ✨ Features
* **Pollution Sensor:** Direct forecast states (Unlikely, Possible, or Likely).
* **Smart Advice:** Simplified swimming recommendations based on current water quality.
* **Annual Beach Grade:** Long-term suitability assessments with descriptive meanings.
* **Diagnostic Data:** Tracking of bacteria counts (Enterococci) and Star Ratings.
* **Device-Centric:** All sensors grouped under a single Beach device for a clean UI.
* **Configurable Polling:** Control how often the API is checked via integration options.

---

## 🚀 Installation

### Option 1: HACS (Recommended)
1. Ensure [HACS](https://hacs.xyz/) is installed.
2. Click the **My Home Assistant** badge above or go to HACS > Integrations > Explore.
3. Search for `NSW Beachwatch` and install.
4. Restart Home Assistant.

### Option 2: Manual
1. Download the `nsw_beachwatch` folder from `custom_components`.
2. Copy it into your Home Assistant `config/custom_components/` directory.
3. Restart Home Assistant.

---

## ⚙️ Configuration
1. Go to **Settings** > **Devices & Services**.
2. Click **Add Integration** and search for **NSW Beachwatch**.
3. Select your beach from the dropdown list.
4. (Optional) Adjust the **Update Interval** (default is 120 minutes) by clicking **Configure** on the integration card.

---

## 📊 Entities
Each beach added creates a device with the following sensors:

| Entity Name | Icon | Type | Description |
| :--- | :--- | :--- | :--- |
| **Water Pollution** | `mdi:waves-arrow-up` | State | The current pollution forecast (e.g., Unlikely, Possible). |
| **Advice** | `mdi:information-outline` | State | A simple recommendation (e.g., "Suitable for swimming"). |
| **Annual Beach Grade**| `mdi:star` | Diagnostic | Long-term grade (e.g., "Very Good"). Includes a `meaning` attribute. |
| **Star Rating** | `mdi:star-circle` | Diagnostic | Short-term rating (1–4 stars) based on the latest sample. |
| **Bacteria Level** | `mdi:microscope` | Diagnostic | The physical count of Enterococci per 100mL. |

### 💡 Smart Advice Logic
The **Advice** sensor interprets the raw forecast to give you peace of mind:
* **Unlikely:** "Water quality is suitable for swimming. Enjoy a swim!"
* **Possible:** "Caution advised for swimming. Children or elderly may be at risk."
* **Likely:** "Water quality is unsuitable for swimming. Avoid swimming today."



---

## ⏱️ Data Refresh Rates
The integration polls the Beachwatch API every **2 hours** by default. However, the underlying data is updated by the NSW Government at different frequencies:

| Data Type | Update Frequency (Source) | Details |
| :--- | :--- | :--- |
| **Pollution Forecast** | **Twice Daily** | Usually updated at **6:00 AM** and **1:30 PM**. |
| **Bacteria Level** | **Weekly** | Water samples are typically collected every 6 days. |
| **Star Rating** | **Weekly** | Updated as new laboratory results are available. |
| **Annual Grade** | **Annually** | Published in the yearly *State of the Beaches* report (October). |

> **Tip:** You can see the exact date of the latest physical water sample by checking the `last_sample_date` attribute on any of the beach sensors.

---

<div align="center">
  <sub>Data provided by <a href="https://www.beachwatch.nsw.gov.au">Beachwatch NSW</a>. This integration is not officially affiliated with the NSW Government.</sub>
</div>

