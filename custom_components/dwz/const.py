"""Constants for dwz."""

from datetime import timedelta
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)


DOMAIN = "dwz"
ATTRIBUTION = "Data provided by https://schachbund.de/"
PLATFORMS = ["sensor"]
CONF_NULIGA_ID = "nuliga_id"
REFRESH_INTERVAL = timedelta(minutes=120)
