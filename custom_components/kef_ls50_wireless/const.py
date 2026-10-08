"""Constants for the KEF LS50 Wireless integration."""

from typing import Final

DOMAIN: Final = "kef_ls50_wireless"
CONF_HOST: Final = "host"
CONF_PORT: Final = "port"
DEFAULT_PORT: Final = 8080
DEFAULT_SCAN_INTERVAL_SECONDS: Final = 30

PLATFORMS: Final = ["media_player"]
