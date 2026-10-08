# LS50 Wireless protocol notes

The captured traffic identifies the LS50 Wireless as a UPnP MediaRenderer exposing HTTP on port 8080. The device description advertises the standard services `RenderingControl`, `ConnectionManager`, and `AVTransport`. The implementation must use sanitized, device-independent values only.

Known generic paths:

- `/description.xml`
- `/RenderingControl/desc.xml`
- `/RenderingControl/ctrl`
- `/RenderingControl/evt/event`
- `/AVTransport/desc.xml`
- `/AVTransport/ctrl`
- `/AVTransport/evt/event`
- `/ConnectionManager/desc.xml`
- `/ConnectionManager/ctrl`
- `/ConnectionManager/evt/event`

The captured description also identifies the product family as KEF LS50 Wireless. Device-specific IP addresses, serial numbers, UUIDs, and MAC addresses are intentionally omitted.

## Next extraction step

Parse the service descriptions and record only SOAP action names, argument names, and state-variable types. Do not store raw captures or credentials. Input switching and sound profiles may be proprietary extensions and should be added only after their SOAP actions are verified.
