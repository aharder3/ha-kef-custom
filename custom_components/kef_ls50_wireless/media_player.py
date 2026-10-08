"""Media player entity for KEF LS50 Wireless."""

from __future__ import annotations

from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerState,
)
from homeassistant.components.media_player.const import (
    MediaPlayerEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_HOST, DOMAIN
from .coordinator import SOURCE_DISPLAY_NAMES, KefLs50WirelessCoordinator


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
    _attr_supported_features = (
        MediaPlayerEntityFeature.VOLUME_SET
        | MediaPlayerEntityFeature.VOLUME_MUTE
        | MediaPlayerEntityFeature.PLAY_PAUSE
        | MediaPlayerEntityFeature.SELECT_SOURCE
        | MediaPlayerEntityFeature.STOP
    )

    def __init__(
        self,
        coordinator: KefLs50WirelessCoordinator,
        entry: ConfigEntry[KefLs50WirelessCoordinator],
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        host = entry.data[CONF_HOST]
        self._attr_unique_id = f"{DOMAIN}_{host.lower()}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, host.lower())},
            name="KEF LS50 Wireless",
            manufacturer="KEF",
            model="LS50 Wireless",
        )

    @property
    def available(self) -> bool:
        """Return whether the speaker is available."""
        return self.coordinator.last_update_success

    @property
    def state(self) -> MediaPlayerState:
        """Return a Home Assistant state from UPnP transport state."""
        transport_state = self.coordinator.data.get("transport_state")
        if transport_state == "PLAYING":
            return MediaPlayerState.PLAYING
        if transport_state in {"PAUSED_PLAYBACK", "PAUSED_RECORDING"}:
            return MediaPlayerState.PAUSED
        return MediaPlayerState.IDLE

    @property
    def source(self) -> str | None:
        """Return the currently selected source."""
        source_key = self.coordinator.data.get("source")
        return SOURCE_DISPLAY_NAMES.get(source_key)

    @property
    def source_list(self) -> list[str]:
        """Return the selectable sources."""
        return list(SOURCE_DISPLAY_NAMES.values())

    @property
    def is_volume_muted(self) -> bool | None:
        """Return mute state."""
        return self.coordinator.data.get("is_muted")

    @property
    def volume_level(self) -> float | None:
        """Return volume normalized to Home Assistant's zero-to-one range."""
        return self.coordinator.data.get("volume_level")

    async def async_set_volume_level(self, volume: float) -> None:
        """Set volume level."""
        await self.coordinator.client.async_set_volume(volume)
        await self.coordinator.async_request_refresh()

    async def async_mute_volume(self, mute: bool) -> None:
        """Set mute state."""
        await self.coordinator.client.async_set_mute(mute)
        await self.coordinator.async_request_refresh()

    async def async_select_source(self, source: str) -> None:
        """Select a speaker input."""
        await self.coordinator.async_select_source(source)
        await self.coordinator.async_request_refresh()

    async def async_media_play_pause(self) -> None:
        """Toggle playback using the verified KEF TCP command."""
        await self.coordinator.async_toggle_play_pause()
        await self.coordinator.async_request_refresh()

    async def async_media_stop(self) -> None:
        """Stop playback when transport supports it."""
        await self.coordinator.client.async_stop()
        await self.coordinator.async_request_refresh()
