"""TCP transport scaffolding for first-generation KEF LS speakers."""

from __future__ import annotations

import asyncio

from .const import KEF_CONTROL_PORT


class KefTcpControlError(Exception):
    """Raised when the KEF TCP control service is unavailable."""


class KefTcpControlClient:
    """Manage reachability of KEF's local TCP control endpoint.

    Command frames are intentionally not activated until independently
    confirmed on this hardware generation.
    """

    def __init__(self, host: str, port: int = KEF_CONTROL_PORT) -> None:
        """Initialize the TCP control client."""
        self.host = host
        self.port = port

    async def async_check_available(self) -> bool:
        """Return whether the device accepts TCP connections."""
        try:
            _, writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port),
                timeout=3,
            )
        except (OSError, TimeoutError):
            return False

        writer.close()
        await writer.wait_closed()
        return True

    async def async_send_verified_command(self, command: bytes) -> None:
        """Send a command only after it has been verified."""
        if not command:
            raise KefTcpControlError("Empty TCP command")

        try:
            _, writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port),
                timeout=3,
            )
            writer.write(command)
            await writer.drain()
            writer.close()
            await writer.wait_closed()
        except (OSError, TimeoutError) as err:
            raise KefTcpControlError(
                f"TCP control connection failed: {err}"
            ) from err
