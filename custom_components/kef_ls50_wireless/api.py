"""Local API client for KEF LS50 Wireless."""

from __future__ import annotations

from typing import Any

from .const import DEFAULT_PORT


class KefLs50WirelessApiClient:
    """Represent the verified-to-be-implemented local LS50 Wireless API."""

    def __init__(self, host: str, port: int | None = None) -> None:
        """Initialize the client without making a network connection."""
        self.host = host
        self.port = port or DEFAULT_PORT

    async def async_get_status(self) -> dict[str, Any]:
        """Get device status.

        This deliberate placeholder prevents unverified control requests.
        Replace it only with documented or reproducibly verified local calls.
        """
        return {
            "available": False,
            "host": self.host,
            "port": self.port,
            "name": f"KEF LS50 Wireless ({self.host})",
            "message": "Local API endpoint not implemented yet.",
            "source": None,
            "source_list": [],
            "sound_profile": None,
            "sound_profile_list": [],
            "is_muted": None,
            "volume_level": None,
        }

    async def async_set_volume(self, volume_level: float) -> None:
        """Set volume after a verified API implementation exists."""
        raise NotImplementedError("KEF volume API is not implemented yet")

    async def async_set_mute(self, is_muted: bool) -> None:
        """Set mute state after a verified API implementation exists."""
        raise NotImplementedError("KEF mute API is not implemented yet")

    async def async_select_source(self, source: str) -> None:
        """Select an input after a verified API implementation exists."""
        raise NotImplementedError("KEF source API is not implemented yet")

    async def async_set_sound_profile(self, profile: str) -> None:
        """Set the sound profile after a verified API implementation exists."""
        raise NotImplementedError("KEF sound-profile API is not implemented yet")
