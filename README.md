# KEF LS50 Wireless for Home Assistant

Eine lokale, datensparsame Home-Assistant-Custom-Integration für KEF LS50 Wireless Lautsprecher. Das Projekt verwendet die lokale UPnP/SOAP-Schnittstelle des Lautsprechers und benötigt kein KEF-Konto, keinen Cloud-Token und keine externe Internetverbindung.

> Status: erste funktionsfähige lokale Steuerung für Lautstärke, Mute und UPnP-Transportbefehle.

## Funktionen

| Funktion | Status | Lokaler UPnP-Dienst |
| --- | --- | --- |
| Einrichtung per Hostname/IP | verfügbar | Config Flow |
| Verfügbarkeit und Polling | verfügbar | `DataUpdateCoordinator` |
| Lautstärke lesen/setzen | verfügbar | `RenderingControl:GetVolume` / `SetVolume` |
| Mute lesen/setzen | verfügbar | `RenderingControl:GetMute` / `SetMute` |
| Play/Pause/Stop | verfügbar | `AVTransport:Play` / `Pause` / `Stop` |
| Transportstatus | verfügbar | `AVTransport:GetTransportInfo` |
| Quellen wechseln | geplant | noch nicht verifiziert |
| KEF-Soundprofile | geplant | noch nicht verifiziert |
| UPnP-Presets | geplant | `ListPresets` / `SelectPreset`, Semantik offen |

Die Lautstärke wird vom Gerät als ganzzahliger Bereich 0 bis 100 geliefert und in Home Assistant als 0.0 bis 1.0 dargestellt.

## Installation

1. Repository klonen oder herunterladen.
2. Den Ordner `custom_components/kef_ls50_wireless` nach `/config/custom_components/kef_ls50_wireless` kopieren.
3. Home Assistant neu starten.
4. Zu **Einstellungen → Geräte & Dienste → Integration hinzufügen** gehen.
5. Nach **KEF LS50 Wireless** suchen.
6. Hostname oder IP-Adresse des eigenen Lautsprechers eingeben; der Standardport ist `8080`.

## Lokale Architektur

Das Gerät stellt sich als UPnP MediaRenderer bereit. Die Implementierung verwendet ausschließlich lokale HTTP/SOAP-Endpunkte:

```text
/description.xml
/RenderingControl/ctrl
/AVTransport/ctrl
```

Die verwendeten Services sind `RenderingControl:1` und `AVTransport:1`, jeweils mit `InstanceID` `0` und dem Kanal `Master` für Lautstärke/Mute.

## Debug-Logging

```yaml
logger:
  default: info
  logs:
    custom_components.kef_ls50_wireless: debug
```

## Sicherheit

Keine Mitschnitte, Zugangsdaten, Cookies, Tokens, privaten IP-Adressen, MAC-Adressen, Seriennummern oder Webhooks committen. `*.mitm`, `*.har`, `*.pcap*`, `.env`, `secrets.yaml` und `.storage` werden durch `.gitignore` ausgeschlossen.

## Lizenz

MIT. KEF und LS50 Wireless sind Marken ihrer jeweiligen Inhaber. Dieses Projekt ist nicht mit KEF verbunden oder von KEF unterstützt.
