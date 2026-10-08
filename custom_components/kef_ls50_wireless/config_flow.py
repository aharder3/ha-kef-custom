"""Config flow for KEF LS50 Wireless."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components import ssdp
from homeassistant.data_entry_flow import FlowResult

from .const import CONF_HOST, CONF_PORT, DEFAULT_PORT, DOMAIN

_LS50_WIRELESS_MODEL = "SP3903"


class KefLs50WirelessConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the configuration flow."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Handle manual setup."""
        if user_input is not None:
            return await self._async_create_host_entry(
                user_input[CONF_HOST],
                user_input[CONF_PORT],
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Optional(
                        CONF_PORT,
                        default=DEFAULT_PORT,
                    ): vol.Coerce(int),
                }
            ),
        )

    async def async_step_ssdp(
        self,
        discovery_info: ssdp.SsdpServiceInfo,
    ) -> FlowResult:
        """Handle discovery of a first-generation LS50 Wireless."""
        manufacturer = (
            discovery_info.upnp.get("manufacturer") or ""
        ).strip()
        model_name = (
            discovery_info.upnp.get("modelName") or ""
        ).strip()
        host = discovery_info.ssdp_headers.get("_host")

        if (
            manufacturer.casefold() != "kef"
            or model_name.casefold()
            != _LS50_WIRELESS_MODEL.casefold()
            or not host
        ):
            return self.async_abort(reason="not_supported")

        unique_id = (
            discovery_info.upnp.get("UDN")
            or f"{host}:{DEFAULT_PORT}"
        )
        await self.async_set_unique_id(unique_id.casefold())
        self._abort_if_unique_id_configured(
            updates={CONF_HOST: host}
        )

        self.context["discovered_host"] = host
        self.context["title_placeholders"] = {
            "name": "KEF LS50 Wireless"
        }

        return self.async_show_form(
            step_id="ssdp_confirm",
            description_placeholders={"host": host},
        )

    async def async_step_ssdp_confirm(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Confirm a discovered LS50 Wireless."""
        if user_input is not None:
            return self.async_create_entry(
                title="KEF LS50 Wireless",
                data={
                    CONF_HOST: self.context["discovered_host"],
                    CONF_PORT: DEFAULT_PORT,
                },
            )

        return self.async_show_form(step_id="ssdp_confirm")

    async def _async_create_host_entry(
        self,
        host: str,
        port: int,
    ) -> FlowResult:
        """Create one config entry from a manually provided host."""
        host = host.strip()
        await self.async_set_unique_id(f"{host.lower()}:{port}")
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=f"KEF LS50 Wireless ({host})",
            data={CONF_HOST: host, CONF_PORT: port},
        )
