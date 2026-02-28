# Changelog
All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] - 01-03-2026
### Known Issues
- Sensor attributes are no longer visible in the sensor UI detail card due to a breaking change in HA Core 2026.2.3. Attributes remain accessible via Developer Tools > States and can still be used in frontend dashboard cards.
- Example Card yaml has been updated to reflect this change also.

## [1.2.0] - 26-02-2026
### Added
- Initial public release
- Swimming Safety sensor with dynamic safety icons
- Swimming Advice sensor with detailed guidance
- Water Quality Test sensor showing lab results
- Water Quality History sensor with star ratings
- Real-time pollution forecasts (Unlikely/Possible/Likely)
- Bacteria level monitoring (enterococci counts)
- Geographic coordinates for map integration
- Device registry integration
- Configurable update intervals (1-1440 minutes)
- Support for 200+ NSW beaches
### Data Features
- Twice-daily pollution forecasts (6:00 AM & 1:30 PM AEST/AEDT)
- Weekly water quality lab results
- Historical 1-5 star ratings
- Detailed swimming recommendations
- Risk level classifications
### Integration
- Full config flow support
- Options flow for update interval
- Unique ID prevention of duplicate beaches
- Device info with manufacturer and model
- Translation support (en.json)
### Documentation
- Comprehensive README with examples
- Installation instructions (HACS + Manual)
- Dashboard card examples
- Automation examples
- Data update schedule
- Attribution and disclaimers
- Beach conditions dashboard card

---
[1.2.1]: https://github.com/PlanetCitizen1829381/ha-nsw-beachwatch/releases/tag/v1.2.1
[1.2.0]: https://github.com/PlanetCitizen1829381/ha-nsw-beachwatch/releases/tag/v1.2.0
