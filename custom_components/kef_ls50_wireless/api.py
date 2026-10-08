"""Local UPnP/SOAP API client for KEF LS50 Wireless."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from xml.etree import ElementTree as ET

from aiohttp import ClientError, ClientSession

from .const import DEFAULT_PORT

_SOAP_ENV = "http://schemas.xmlsoap.org/soap/envelope/"
_RENDERING_CONTROL = "urn:schemas-upnp-org:service:RenderingControl:1"
_AV_TRANSPORT = "urn:schemas-upnp-org:service:AVTransport:1"


class KefLs50WirelessApiError(Exception):
    """Raised when the LS50 Wireless cannot process an API request."""


class KefLs50WirelessApiClient:
    """Communicate with a KEF LS50 Wireless through its local UPnP services."""

    def __init__(self, session: ClientSession, host: str, port: int | None = None) -> None:
        """Initialize the local API client."""
        self._session = session
        self.host = host
        self.port = port or DEFAULT_PORT
        self._base_url = f"http://{host}:{self.port}"

    async def async_get_status(self) -> dict[str, Any]:
        """Return the current local speaker state."""
        volume, muted, transport = await self._async_get_state()
        transport_state = transport.get("CurrentTransportState", "UNKNOWN")
        return {
            "available": True,
            "host": self.host,
            "port": self.port,
            "name": "KEF LS50 Wireless",
            "volume_level": volume / 100,
            "is_muted": muted,
            "transport_state": transport_state,
            "transport_status": transport.get("CurrentTransportStatus"),
            "transport_speed": transport.get("CurrentSpeed"),
        }

    async def async_set_volume(self, volume_level: float) -> None:
        """Set volume using the LS50's verified 0–100 range."""
        desired_volume = max(0, min(100, round(volume_level * 100)))
        await self._async_soap_action(
            "RenderingControl/ctrl",
            _RENDERING_CONTROL,
            "SetVolume",
            {
                "InstanceID": "0",
                "Channel": "Master",
                "DesiredVolume": str(desired_volume),
            },
        )

    async def async_set_mute(self, is_muted: bool) -> None:
        """Set mute state."""
        await self._async_soap_action(
            "RenderingControl/ctrl",
            _RENDERING_CONTROL,
            "SetMute",
            {
                "InstanceID": "0",
                "Channel": "Master",
                "DesiredMute": "1" if is_muted else "0",
            },
        )

    async def async_play(self) -> None:
        """Start playback when transport supports it."""
        await self._async_soap_action(
            "AVTransport/ctrl",
            _AV_TRANSPORT,
            "Play",
            {"InstanceID": "0", "Speed": "1"},
        )

    async def async_pause(self) -> None:
        """Pause playback when transport supports it."""
        await self._async_soap_action(
            "AVTransport/ctrl",
            _AV_TRANSPORT,
            "Pause",
            {"InstanceID": "0"},
        )

    async def async_stop(self) -> None:
        """Stop playback when transport supports it."""
        await self._async_soap_action(
            "AVTransport/ctrl",
            _AV_TRANSPORT,
            "Stop",
            {"InstanceID": "0"},
        )

    async def _async_get_state(self) -> tuple[int, bool, dict[str, str]]:
        """Fetch independent rendering and transport state concurrently."""
        volume_data = await self._async_soap_action(
            "RenderingControl/ctrl",
            _RENDERING_CONTROL,
            "GetVolume",
            {"InstanceID": "0", "Channel": "Master"},
        )
        mute_data = await self._async_soap_action(
            "RenderingControl/ctrl",
            _RENDERING_CONTROL,
            "GetMute",
            {"InstanceID": "0", "Channel": "Master"},
        )
        transport_data = await self._async_soap_action(
            "AVTransport/ctrl",
            _AV_TRANSPORT,
            "GetTransportInfo",
            {"InstanceID": "0"},
        )
        try:
            return (
                int(volume_data["CurrentVolume"]),
                mute_data["CurrentMute"] in {"1", "true", "True"},
                transport_data,
            )
        except (KeyError, ValueError) as err:
            raise KefLs50WirelessApiError("Unexpected SOAP response") from err

    async def _async_soap_action(
        self,
        control_path: str,
        service_type: str,
        action: str,
        arguments: Mapping[str, str],
    ) -> dict[str, str]:
        """Execute one SOAP action and return direct response child elements."""
        body = self._build_envelope(service_type, action, arguments)
        headers = {
            "Content-Type": 'text/xml; charset="utf-8"',
            "SOAPACTION": f'"{service_type}#{action}"',
        }
        try:
            async with self._session.post(
                f"{self._base_url}/{control_path}",
                data=body,
                headers=headers,
            ) as response:
                payload = await response.text()
                if response.status != 200:
                    raise KefLs50WirelessApiError(
                        f"SOAP {action} failed with HTTP {response.status}"
                    )
        except ClientError as err:
            raise KefLs50WirelessApiError(f"Connection error: {err}") from err

        return self._parse_response(payload, action)

    @staticmethod
    def _build_envelope(
        service_type: str,
        action: str,
        arguments: Mapping[str, str],
    ) -> str:
        """Build a SOAP 1.1 envelope."""
        envelope = ET.Element(f"{{{_SOAP_ENV}}}Envelope")
        envelope.set(f"{{{_SOAP_ENV}}}encodingStyle", "http://schemas.xmlsoap.org/soap/encoding/")
        body = ET.SubElement(envelope, f"{{{_SOAP_ENV}}}Body")
        command = ET.SubElement(body, f"{{{service_type}}}{action}")
        for key, value in arguments.items():
            ET.SubElement(command, key).text = value
        return ET.tostring(envelope, encoding="unicode", xml_declaration=True)

    @staticmethod
    def _parse_response(payload: str, action: str) -> dict[str, str]:
        """Parse a SOAP response and surface explicit SOAP faults."""
        try:
            root = ET.fromstring(payload)
        except ET.ParseError as err:
            raise KefLs50WirelessApiError("Invalid SOAP XML response") from err

        fault = root.find(f".//{{{_SOAP_ENV}}}Fault")
        if fault is not None:
            fault_text = fault.findtext("faultstring", default="Unknown SOAP fault")
            raise KefLs50WirelessApiError(f"SOAP {action} fault: {fault_text}")

        response_element = next(iter(root.findall(f".//{{*}}{action}Response")), None)
        if response_element is None:
            raise KefLs50WirelessApiError(f"SOAP {action} response element missing")
        return {
            child.tag.rsplit("}", 1)[-1]: child.text or ""
            for child in response_element
        }
