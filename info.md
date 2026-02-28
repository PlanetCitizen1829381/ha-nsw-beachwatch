# NSW Beachwatch Integration

🌊 Swimming safety advice and Water quality forecasts for NSW beaches.

## Features

- **Pollution Forecasts** - Daily predictions based on rainfall and pollution events
- **Laboratory Water Quality Results** - Bacterial testing with safety ratings (1-5 stars)
- **4 Sensors Per Beach** - Comprehensive monitoring for each location
- **Dynamic Safety Icons** - Visual indicators that change based on conditions
- **GPS Coordinates** - Location data for map integrations
- **Smart Bacteria Mapping** - Converts star ratings to enterococci ranges
- **200+ NSW Beaches** - Extensive coverage across New South Wales

## Sensors

Each beach provides:

1. **Swimming Safety** - Safe / Caution / Unsafe / Unknown with dynamic icons
2. **Swimming Advice** - Detailed text guidance on swimming conditions
3. **Water Quality Test** - Latest lab results (Good/Fair/Poor/Bad)
4. **Water Quality History** - 1-5 star rating based on latest sample

## Installation

1. Click the button in HACS or search for "NSW Beachwatch"
2. Download the integration
3. Restart Home Assistant
4. Add via Settings → Devices & Services → Add Integration
5. Select your beach from the dropdown

## Configuration

- **Beach Selection** - Choose from 200+ NSW beaches
- **Update Interval** - Configurable (default: 2 hours, range: 1-1440 minutes)

## Data Updates

- **Forecasts**: Updated twice daily (6:00 AM & 1:30 PM)
- **Lab Results**: Updated as results become available from NSW Beachwatch

## Water Quality Ratings

| Stars | Bacteria Range | Safety |
|-------|---------------|--------|
| ⭐⭐⭐⭐ | <41 cfu/100mL | Good - safe for bathing |
| ⭐⭐⭐ | 41-200 cfu/100mL | Fair - increased risk |
| ⭐⭐ | 201-500 cfu/100mL | Poor - substantial risk |
| ⭐ | >500 cfu/100mL | Bad - significant risk |

## Attributes Available in the overflow menu of the sensor and in Developer Tools > State

- Risk Level & Meaning
- GPS Coordinates (latitude/longitude)
- Last Official Update timestamp
- Enterococci bacterial levels
- Water Quality Description
- Last Sample Date
- Attribution to NSW Beachwatch

## Data Source

Data provided by the official **NSW Beachwatch API** operated by the NSW Department of Planning and Environment.

Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).

**Note:** This is a community-developed integration and is not officially affiliated with or endorsed by the NSW Government.

## Support

- [Report Issues](https://github.com/PlanetCitizen1829381/ha-nsw-beachwatch/issues)
- [View Documentation](https://github.com/PlanetCitizen1829381/ha-nsw-beachwatch)

---

🌊 Stay safe and enjoy the surf! 🏖️
