"""Update coordinator for KEF LS50 Wireless."""

from __future__ import annotations

import asyncio
import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import KefLs50WirelessApiClient
from .const import DEFAULT_SCAN_INTERVAL_SECONDS, DOMAIN
from .kef_tcp import KefTcpControlClient

_LOGGER = logging.getLogger(__name__)


class KefLs50WirelessCoordinator(
    DataUpdateCoordinator[dict[str, Any]]
):
    """Fetch and distribute LS50 Wireless status."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: KefLs50WirelessApiClient,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(
                seconds=DEFAULT_SCAN_INTERVAL_SECONDS
            ),
        )
        self.client = client
        self.tcp_client = KefTcpControlClient(client.host)

    async def _async_update_data(self) -> dict[str, Any]:
        """Read UPnP state and KEF TCP reachability."""
        try:
            state, tcp_available = await asyncio.gather(
                self.client.async_get_status(),
                self.tcp_client.async_check_available(),
            )
            state["tcp_control_available"] = tcp_available
            return state
        except Exception as err:
            raise UpdateFailed(
                f"Error communicating with KEF LS50 Wireless: {err}"
            ) from err
