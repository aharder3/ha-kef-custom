# KEF LS50 Wireless for Home Assistant

Eine lokale, datensparsame Home-Assistant-Custom-Integration für KEF LS50 Wireless Lautsprecher. Das Projekt ist als offenes Community-Projekt ausgelegt und enthält weder persönliche Daten noch Cloud-Zugangsdaten, Tokens, IP-Adressen oder Netzwerkmitschnitte.

> Status: frühes Entwicklungsgerüst. Der Config Flow, der Coordinator und die Entity-Struktur sind vorhanden. Die tatsächliche lokale Steuerungs-API wird erst anhand bereinigter, reproduzierbarer Requests implementiert.

## Ziele

- Lokale Kommunikation mit dem Lautsprecher, ohne verpflichtende Cloud-Anbindung
- Unterstützung für mehrere LS50-Wireless-Geräte
- Status, Lautstärke, Mute, Quelle und Sound-Profile
- Dynamische Quellen und Profile: Die Integration übernimmt nur Werte, die ein Gerät tatsächlich meldet
- Kein Tracking und keine Übertragung von Telemetrie an Dritte

## Gefundene lokale Schnittstelle

Der Mitschnitt enthält eine Gerätebeschreibung des LS50 Wireless als UPnP MediaRenderer. Erkennbar sind Port `8080` sowie die Standarddienste `RenderingControl`, `ConnectionManager` und `AVTransport`. Die bereinigte Dokumentation steht in [`docs/protocol.md`](docs/protocol.md). Keine gerätespezifischen Daten werden gespeichert.

## Unterstützte Funktionen

| Bereich | Status | Home-Assistant-Abbildung |
| --- | --- | --- |
| Einrichtung per Hostname/IP | vorbereitet | Config Flow |
| Erreichbarkeit | vorbereitet | `media_player` availability |
| Gerätestatus | vorbereitet | `DataUpdateCoordinator` |
| Lautstärke | geplant | `media_player.volume_set` |
| Stummschalten | geplant | `media_player.volume_mute` |
| Quelle wechseln | geplant | `media_player.select_source` |
| Sound-Profil | geplant | `select.kef_ls50_sound_profile` |
| Wiedergabe/Standby | geplant | `media_player` |

Die Begriffe und Werte für Quellen und Sound-Profile werden nicht fest in den Code geschrieben. Sie müssen vom Gerät bzw. der verifizierten API stammen.

## Sicherheit

Keine Mitschnitte, Zugangsdaten, Cookies, Tokens, privaten IP-Adressen, MAC-Adressen, Seriennummern oder Webhooks committen. `*.mitm`, `*.har`, `*.pcap*`, `.env`, `secrets.yaml` und `.storage` werden durch `.gitignore` ausgeschlossen.

## Installation

1. Repository klonen.
2. `custom_components/kef_ls50_wireless` nach `/config/custom_components/kef_ls50_wireless` kopieren.
3. Home Assistant neu starten.
4. Unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** nach **KEF LS50 Wireless** suchen.
5. Hostname/IP des eigenen Lautsprechers eintragen.

## Debug-Logging

```yaml
logger:
  default: info
  logs:
    custom_components.kef_ls50_wireless: debug
```

Vor jedem öffentlichen Log-Auszug müssen lokale und geheime Werte entfernt werden.

## Lizenz

MIT. KEF und LS50 Wireless sind Marken ihrer jeweiligen Inhaber. Dieses Projekt ist nicht mit KEF verbunden oder von KEF unterstützt.
