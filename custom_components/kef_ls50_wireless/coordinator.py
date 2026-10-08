"""Update coordinator for KEF LS50 Wireless."""

from __future__ import annotations

import asyncio
import logging
from datetime import timedelta
from typing import Any

from aiokef import AsyncKefSpeaker
from aiokef.aiokef import COMMANDS, INPUT_SOURCES

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import KefLs50WirelessApiClient
from .const import DEFAULT_SCAN_INTERVAL_SECONDS, DOMAIN

_LOGGER = logging.getLogger(__name__)

SOURCE_DISPLAY_NAMES = {
    "Wifi": "WiFi",
    "Bluetooth": "Bluetooth",
    "Aux": "AUX",
    "Opt": "Optical",
    "Usb": "USB",
}
SOURCE_KEYS_BY_DISPLAY_NAME = {
    display_name: key for key, display_name in SOURCE_DISPLAY_NAMES.items()
}
PLAY_PAUSE_FRAME = bytes.fromhex("53 31 81 81")
COMMAND_TIMEOUT_SECONDS = 5


class KefLs50WirelessCoordinator(DataUpdateCoordinator[dict[str, Any]]):
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
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL_SECONDS),
        )
        self.client = client
        self.kef_client = AsyncKefSpeaker(client.host)

    async def _async_update_data(self) -> dict[str, Any]:
        """Read UPnP state and active source through KEF TCP."""
        try:
            state, kef_state = await asyncio.gather(
                self.client.async_get_status(),
                self.kef_client.get_state(),
            )
            state["tcp_control_available"] = True
            state["source"] = kef_state.source
            return state
        except Exception as err:
            raise UpdateFailed(
                f"Error communicating with KEF LS50 Wireless: {err}"
            ) from err

    async def async_select_source(self, display_name: str) -> None:
        """Select a speaker input using the verified KEF TCP protocol."""
        source_key = SOURCE_KEYS_BY_DISPLAY_NAME.get(display_name)
        if source_key is None:
            raise ValueError(f"Unsupported source: {display_name}")

        state = await asyncio.wait_for(
            self.kef_client.get_state(),
            timeout=COMMAND_TIMEOUT_SECONDS,
        )
        standby_time = state.standby_time or 60
        orientation_index = 0 if state.orientation == "L/R" else 1

        source_codes = INPUT_SOURCES[source_key][standby_time]
        source_code = source_codes[orientation_index] % 128
        command = COMMANDS["set_source"](source_code)

        await asyncio.wait_for(
            self.kef_client._comm.send_message(command),
            timeout=COMMAND_TIMEOUT_SECONDS,
        )

    async def async_toggle_play_pause(self) -> None:
        """Toggle playback using the verified KEF TCP play/pause frame."""
        await asyncio.wait_for(
            self.kef_client._comm.send_message(PLAY_PAUSE_FRAME),
            timeout=COMMAND_TIMEOUT_SECONDS,
        )
