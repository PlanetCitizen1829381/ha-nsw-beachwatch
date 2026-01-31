<div align="center">

# 🌊 NSW Beachwatch for Home Assistant
**Water pollution monitoring and swimming safety for New South Wales beaches.**

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://hacs.xyz/)
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg?style=for-the-badge)](https://my.home-assistant.io/redirect/hacs_repository/?owner=PlanetCitizen1829381&repository=ha-nsw-beachwatch&category=integration)

[Features](#-features) • [Installation](#-installation) • [Configuration](#-configuration) • [Entities](#-entities)

---
</div>

## ✨ Features
* **Pollution Sensor:** Direct forecast states (Unlikely, Possible, or Likely).
* **Smart Advice:** Simplified swimming recommendations based on current water quality.
* **Diagnostic Data:** Tracking of bacteria counts (Enterococci) and Star Ratings.
* **Automation Ready:** Dedicated binary sensor for safety alerts.
* **Device-Centric:** All sensors grouped under a single Beach device for a clean UI.

---

## 🚀 Installation

### Option 1: HACS (Recommended)
1. Ensure [HACS](https://hacs.xyz/) is installed.
2. Click the **Open in HACS** button above, or manually add this URL as a **Custom Repository**:
   `https://github.com/PlanetCitizen1829381/ha-nsw-beachwatch`
3. Download and restart Home Assistant.

### Option 2: Manual
1. Download the `custom_components/nsw_beachwatch` folder.
2. Paste it into your Home Assistant `/config/custom_components/` directory.
3. Restart Home Assistant.

---

## ⚙️ Configuration
1. Go to **Settings** > **Devices & Services**.
2. Click **+ Add Integration** and search for **NSW Beachwatch**.
3. Select your beach from the list.
4. Use the **Configure** button on the device page to adjust the update interval (default is 30 mins).

---

## 📊 Entities
| Icon | Entity Name | Category | Description |
| :---: | :--- | :---: | :--- |
| 🧪 | **Pollution** | Primary | Current pollution forecast state. |
| ℹ️ | **Advice** | Primary | Human-readable swimming recommendation. |
| 🛡️ | **Swimming Safety** | Binary | `Safe` or `Unsafe` (Pollution Likely). |
| 🔬 | **Bacteria Count** | Diagnostic | Enterococci cfu/100mL levels. |
| ⭐ | **Star Rating** | Diagnostic | Official Beachwatch star rating (1-4). |

---

<div align="center">
  <sub>Data provided by <a href="https://www.beachwatch.nsw.gov.au">Beachwatch NSW</a>. This integration is not officially affiliated with the NSW Government.</sub>
</div>


## Next steps

These are some next steps you may want to look into:
- Add tests to your integration, [`pytest-homeassistant-custom-component`](https://github.com/MatthewFlamm/pytest-homeassistant-custom-component) can help you get started.
- Add brand images (logo/icon) to https://github.com/home-assistant/brands.
- Create your first release.
- Share your integration on the [Home Assistant Forum](https://community.home-assistant.io/).
- Submit your integration to [HACS](https://hacs.xyz/docs/publish/start).




