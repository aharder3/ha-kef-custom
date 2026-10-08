# KEF LS50 Wireless for Home Assistant

Eine lokale, datensparsame Home-Assistant-Custom-Integration für die erste Generation der KEF LS50 Wireless. Sie benötigt kein KEF-Konto, keinen Cloud-Token und keine externe Internetverbindung.

> Status: Lautstärke und Mute funktionieren über verifizierte lokale UPnP/SOAP-Aufrufe. Automatische SSDP-Erkennung und die sichere Vorbereitung des lokalen KEF-TCP-Control-Ports sind enthalten.

## Funktionen

| Funktion | Status | Protokoll |
| --- | --- | --- |
| Manuelle Einrichtung per Hostname/IP | verfügbar | Config Flow |
| Automatische Erkennung für SP3903 | verfügbar | SSDP / UPnP MediaRenderer |
| Verfügbarkeit und Polling | verfügbar | `DataUpdateCoordinator` |
| Lautstärke lesen/setzen | verfügbar | `RenderingControl:GetVolume` / `SetVolume` |
| Mute lesen/setzen | verfügbar | `RenderingControl:GetMute` / `SetMute` |
| UPnP-Transportstatus | verfügbar | `AVTransport:GetTransportInfo` |
| UPnP Play/Pause/Stop | verfügbar für aktive DLNA-URI | `AVTransport` |
| KEF TCP-Port-Prüfung | verfügbar | TCP `50001` |
| Play/Pause bei KEF-/Spotify-/Bluetooth-Quellen | vorbereitet, noch nicht aktiviert | KEF TCP `50001` |
| Quelle wechseln | vorbereitet, noch nicht aktiviert | KEF TCP `50001` |
| KEF-Soundprofile | geplant | noch nicht verifiziert |

Die Lautstärke wird vom Gerät als ganzzahliger Bereich 0 bis 100 geliefert und in Home Assistant als 0.0 bis 1.0 dargestellt.

## Automatische Erkennung

Die Integration erkennt die erste LS50 Wireless-Generation mit `modelName` `SP3903` per SSDP. Nach dem Fund erscheint sie unter **Einstellungen → Geräte & Dienste** zur Bestätigung. Wenn SSDP in einem getrennten VLAN blockiert wird, kann das Gerät weiterhin manuell über Hostname/IP und Port `8080` hinzugefügt werden.

## Warum Quelle/Play noch vorbereitet sind

Die erste LS50 Wireless stellt zusätzlich zur UPnP-Schnittstelle eine lokale TCP-Steuerung auf Port `50001` bereit. Dieser Port wird geprüft, aber keine unbestätigten Binärbefehle werden automatisch gesendet. Erst wenn ein Befehl auf dieser Modellgeneration reproduzierbar getestet ist, wird er als Home-Assistant-Button oder Quellenwahl aktiviert.

Die UPnP-Presetliste wird absichtlich nicht als Soundprofil-Steuerung gezeigt: Sie enthält nur `FactoryDefaults` und `InstallationDefaults`, nicht die KEF-App-Soundprofile.

## Installation

1. Repository klonen oder herunterladen.
2. Den Ordner `custom_components/kef_ls50_wireless` nach `/config/custom_components/kef_ls50_wireless` kopieren.
3. Home Assistant neu starten.
4. Zu **Einstellungen → Geräte & Dienste** gehen.
5. Die automatisch entdeckte KEF LS50 Wireless bestätigen oder **Integration hinzufügen** wählen und Hostname/IP manuell eingeben.
6. Den Standardport `8080` beibehalten.

## Lokale Architektur

```text
UPnP/SOAP (8080)
├── /description.xml
├── /RenderingControl/ctrl
└── /AVTransport/ctrl

KEF TCP control (50001)
└── Verfügbarkeit geprüft; Befehle erst nach Gerätevalidierung aktivieren
```

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
