"""Select entity for KEF LS50 Wireless sound profiles."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_HOST, DOMAIN
from .coordinator import KefLs50WirelessCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry[KefLs50WirelessCoordinator],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sound-profile selector."""
    async_add_entities([KefLs50WirelessSoundProfile(entry.runtime_data, entry)])


class KefLs50WirelessSoundProfile(
    CoordinatorEntity[KefLs50WirelessCoordinator], SelectEntity
):
    """Represent device-provided sound profiles."""

    _attr_has_entity_name = True
    _attr_name = "Sound profile"

    def __init__(
        self, coordinator: KefLs50WirelessCoordinator, entry: ConfigEntry[KefLs50WirelessCoordinator]
    ) -> None:
        """Initialize the sound-profile selector."""
        super().__init__(coordinator)
        host = entry.data[CONF_HOST]
        self._attr_unique_id = f"{DOMAIN}_{host.lower()}_sound_profile"

    @property
    def current_option(self) -> str | None:
        """Return the active sound profile."""
        return self.coordinator.data.get("sound_profile")

    @property
    def options(self) -> list[str]:
        """Return sound profiles supplied by the device."""
        return self.coordinator.data.get("sound_profile_list", [])

    async def async_select_option(self, option: str) -> None:
        """Select a sound profile after API support is implemented."""
        await self.coordinator.client.async_set_sound_profile(option)
        await self.coordinator.async_request_refresh()
