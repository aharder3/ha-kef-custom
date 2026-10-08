"""KEF LS50 Wireless integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .api import KefLs50WirelessApiClient
from .const import CONF_HOST, CONF_PORT
from .coordinator import KefLs50WirelessCoordinator

PLATFORMS: list[Platform] = [Platform.MEDIA_PLAYER, Platform.SELECT]

type KefLs50WirelessConfigEntry = ConfigEntry[KefLs50WirelessCoordinator]


async def async_setup_entry(
    hass: HomeAssistant, entry: KefLs50WirelessConfigEntry
) -> bool:
    """Set up KEF LS50 Wireless from a config entry."""
    client = KefLs50WirelessApiClient(
        host=entry.data[CONF_HOST],
        port=entry.data.get(CONF_PORT),
    )
    coordinator = KefLs50WirelessCoordinator(hass, client)

    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: KefLs50WirelessConfigEntry
) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
