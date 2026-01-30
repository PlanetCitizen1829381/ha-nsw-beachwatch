NSW Beachwatch for Home Assistant
This integration provides real-time pollution forecasts, swimming suitability advice, and bacteria counts for New South Wales beaches, sourced directly from the NSW Beachwatch API.

Features
Pollution Sensor: Real-time forecast (Unlikely, Possible, or Likely).
Swimming Advice: Human-readable swimming recommendations.
Diagnostic Data: Star ratings and bacteria counts (Enterococci).
Binary Sensor: Simple "Safe/Unsafe" binary state for automations.
Unified Device: All entities for a single beach are grouped into one device screen.

Installation
Option 1: HACS (Recommended)

Ensure HACS is installed and configured.
Click the Open in HACS button at the top of this page, or:
Go to HACS > Integrations > Custom Repositories (under the three-dot menu).
Paste https://github.com/PlanetCitizen1829381/ha-nsw-beachwatch into the Repository field.
Select Integration as the Category and click Add.
Find NSW Beachwatch and click Download.
Restart Home Assistant.

Option 2: Manual Installation

Use the Code button on this GitHub page to download the ZIP file.
Extract the ZIP and locate the custom_components/nsw_beachwatch folder.
Copy the nsw_beachwatch folder into your Home Assistant /config/custom_components/ directory.
Your folder structure should look like this:

config/
└── custom_components/
    └── nsw_beachwatch/
        ├── manifest.json
        ├── sensor.py
        └── ...
Restart Home Assistant.

Configuration
In Home Assistant, navigate to Settings > Devices & Services.
Click + Add Integration in the bottom right.
Search for NSW Beachwatch and select it.
Select your preferred beach from the dropdown list and click Submit.
To change the update frequency, click Configure on the Beachwatch device page.

Entities
Each configured beach provides the following entities:

Entity Name	Type	Description
Pollution	Sensor	Current pollution forecast state.
Advice	Sensor	Swimming suitability recommendation.
Swimming Safety	Binary Sensor	Off (Safe) or On (Pollution Likely).
Bacteria Count	Diagnostic	Enterococci cfu/100mL from the last sample.
Star Rating	Diagnostic	1-4 star rating for the beach.
Troubleshooting
If the integration does not appear in the "Add Integration" list:

Ensure the files are in the correct custom_components/nsw_beachwatch/ directory.

Restart Home Assistant.

Clear your browser cache or force-refresh (Ctrl + F5).

## How?

1. Create a new repository in GitHub, using this repository as a template by clicking the "Use this template" button in the GitHub UI.
1. Open your new repository in Visual Studio Code devcontainer (Preferably with the "`Dev Containers: Clone Repository in Named Container Volume...`" option).
1. Rename all instances of the `integration_blueprint` to `custom_components/<your_integration_domain>` (e.g. `custom_components/awesome_integration`).
1. Rename all instances of the `Integration Blueprint` to `<Your Integration Name>` (e.g. `Awesome Integration`).
1. Run the `scripts/develop` to start HA and test out your new integration.

## Next steps

These are some next steps you may want to look into:
- Add tests to your integration, [`pytest-homeassistant-custom-component`](https://github.com/MatthewFlamm/pytest-homeassistant-custom-component) can help you get started.
- Add brand images (logo/icon) to https://github.com/home-assistant/brands.
- Create your first release.
- Share your integration on the [Home Assistant Forum](https://community.home-assistant.io/).
- Submit your integration to [HACS](https://hacs.xyz/docs/publish/start).

