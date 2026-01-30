"""Constants for the NSW Beachwatch integration."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "NSW Beachwatch"
DOMAIN = "nsw_beachwatch"
VERSION = "1.0.0"

# API Configuration
# This is the base URL for the NSW Beachwatch GeoJSON feed
API_URL = "https://api.beachwatch.nsw.gov.au/public/sites/geojson"

# Default polling interval in minutes
# We don't need to check every second; every 30 minutes is plenty for beach data
SCAN_INTERVAL_MINUTES = 30

CONF_BEACH_NAME = "beach_name"
