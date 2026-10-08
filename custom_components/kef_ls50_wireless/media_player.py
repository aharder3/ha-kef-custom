"""Media player entity for KEF LS50 Wireless."""

from __future__ import annotations

from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import MediaPlayerEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_HOST, DOMAIN
from .coordinator import KefLs50WirelessCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry[KefLs50WirelessCoordinator],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the KEF LS50 Wireless media player."""
    async_add_entities([KefLs50WirelessMediaPlayer(entry.runtime_data, entry)])


class KefLs50WirelessMediaPlayer(
    CoordinatorEntity[KefLs50WirelessCoordinator], MediaPlayerEntity
):
    """Represent a KEF LS50 Wireless loudspeaker."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_supported_features = MediaPlayerEntityFeature(0)

    def __init__(
        self, coordinator: KefLs50WirelessCoordinator, entry: ConfigEntry[KefLs50WirelessCoordinator]
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        host = entry.data[CONF_HOST]
        self._attr_unique_id = f"{DOMAIN}_{host.lower()}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, host.lower())},
            name=f"KEF LS50 Wireless ({host})",
            manufacturer="KEF",
            model="LS50 Wireless",
        )

    @property
    def available(self) -> bool:
        """Return whether the speaker is available."""
        return bool(self.coordinator.last_update_success and self.coordinator.data.get("available"))

    @property
    def state(self) -> str:
        """Return the current player state."""
        if not self.available:
            return STATE_UNAVAILABLE
        return super().state

    @property
    def source(self) -> str | None:
        """Return the active source."""
        return self.coordinator.data.get("source")

    @property
    def source_list(self) -> list[str]:
        """Return sources supplied by the device."""
        return self.coordinator.data.get("source_list", [])

    @property
    def is_volume_muted(self) -> bool | None:
        """Return mute state."""
        return self.coordinator.data.get("is_muted")

    @property
    def volume_level(self) -> float | None:
        """Return volume from zero to one."""
        return self.coordinator.data.get("volume_level")
