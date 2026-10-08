# KEF LS50 Wireless for Home Assistant

Eine lokale, datensparsame Home-Assistant-Custom-Integration für KEF LS50 Wireless Lautsprecher. Das Projekt verwendet die lokalen UPnP/SOAP- und KEF-TCP-Schnittstellen des Lautsprechers und benötigt kein KEF-Konto, keinen Cloud-Token und keine externe Internetverbindung.

**Status:** lokale Steuerung für Lautstärke, Mute, Quellenwahl und Play/Pause verfügbar.

## Funktionen

| Funktion | Status | Lokaler Dienst / Protokoll |
| --- | --- | --- |
| Einrichtung per Hostname/IP | verfügbar | Config Flow |
| Automatische Lautsprechersuche | verfügbar | SSDP/UPnP-Erkennung für KEF SP3903 |
| Verfügbarkeit und Polling | verfügbar | `DataUpdateCoordinator` |
| Lautstärke lesen/setzen | verfügbar | `RenderingControl:GetVolume` / `SetVolume` |
| Mute lesen/setzen | verfügbar | `RenderingControl:GetMute` / `SetMute` |
| Play/Pause | verfügbar | KEF TCP-Frame `53 31 81 81` |
| Stopp | verfügbar | `AVTransport:Stop` |
| Transportstatus | verfügbar | `AVTransport:GetTransportInfo` |
| Quellen wechseln | verfügbar | KEF TCP über `aiokef` |
| Aktive Quelle anzeigen | verfügbar | KEF TCP über `aiokef` |
| KEF-Soundprofile | geplant | noch nicht verifiziert |
| UPnP-Presets | geplant | `ListPresets` / `SelectPreset`, Semantik offen |

Die auswählbaren Quellen sind **WiFi**, **Bluetooth**, **AUX**, **Optical** und **USB**. Die Lautstärke wird vom Gerät als ganzzahliger Bereich 0 bis 100 geliefert und in Home Assistant als 0.0 bis 1.0 dargestellt.

## Installation

1. Repository klonen oder herunterladen.
2. Den Ordner `custom_components/kef_ls50_wireless` nach `/config/custom_components/kef_ls50_wireless` kopieren.
3. Home Assistant neu starten.
4. Zu **Einstellungen → Geräte & Dienste → Integration hinzufügen** gehen.
5. Nach **KEF LS50 Wireless** suchen.
6. Einen automatisch via SSDP gefundenen Lautsprecher bestätigen oder Hostname/IP manuell eingeben.

## Bedienung

Nach der Einrichtung steht ein `media_player` für den Lautsprecher zur Verfügung. Über Home Assistant kannst du Lautstärke und Mute steuern, eine Quelle auswählen und Play/Pause auslösen.

Die Quellenwahl berechnet die korrekten KEF-TCP-Codes anhand der Standby-Zeit und Lautsprecherorientierung. Play/Pause nutzt einen Toggle-Befehl; je nach aktiver Quelle kann der UPnP-Transportstatus den tatsächlichen Wiedergabezustand nicht immer zuverlässig widerspiegeln.

## Entwicklung

Die Integration nutzt nur lokale Gerätezugriffe:

- UPnP/SOAP auf Port 8080 für Lautstärke, Mute und Transportstatus.
- KEF TCP auf Port 50001 für Quellenwahl und Play/Pause.

Die getesteten KEF-TCP-Befehle wurden mit einer LS50 Wireless erfolgreich verifiziert.