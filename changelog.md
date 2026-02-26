# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2026-02-27

### Added
- **New Sensor: Pollution Alerts** - Real-time pollution warnings and sewage overflow notifications
- Dynamic icon for pollution alerts (red when active, green when clear)
- Detailed alert attributes including type, source, text, and last updated timestamp
- Enhanced API client now fetches site details from `/sites/{site_id}` endpoint
- Additional data: region, council, water temperature, annual grade
- Better error handling in config flow
- Modern number selector UI for update interval setting

### Changed
- API now makes two calls per update: GeoJSON for basic data + site details for alerts
- Improved config flow with better exception handling
- Enhanced user experience during beach selection

### Technical
- Added `_get_site_details()` method to API client
- Expanded coordinator data structure to include alerts and metadata
- Updated translations in `en.json` for new sensor

## [1.2.0] - 2026-02-26

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

## Future Plans

### Planned Features
- Additional sensor for water temperature
- Annual grade history sensor
- Weather forecast integration
- Tide and swell information
- Nearby beaches suggestions
- Custom alert automations
- Notification templates

### Under Consideration
- Historical data trending
- Comparative beach analysis
- Weekly digest notifications
- Integration with weather services
- Beach conditions dashboard card

---

[1.3.0]: https://github.com/PlanetCitizen1829381/ha-nsw-beachwatch/releases/tag/v1.3.0
[1.2.0]: https://github.com/PlanetCitizen1829381/ha-nsw-beachwatch/releases/tag/v1.2.0
