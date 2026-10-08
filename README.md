# KEF LS50 Wireless for Home Assistant

Eine lokale, datensparsame Home-Assistant-Custom-Integration für KEF LS50 Wireless Lautsprecher. Das Projekt ist als offenes Community-Projekt ausgelegt und enthält weder persönliche Daten noch Cloud-Zugangsdaten, Tokens, IP-Adressen oder Netzwerkmitschnitte.

> Status: frühes Entwicklungsgerüst. Der Config Flow, der Coordinator und die Entity-Struktur sind vorhanden. Die tatsächliche lokale Steuerungs-API wird erst anhand bereinigter, reproduzierbarer Requests implementiert.

## Ziele

- Lokale Kommunikation mit dem Lautsprecher, ohne verpflichtende Cloud-Anbindung
- Unterstützung für mehrere LS50-Wireless-Geräte
- Status, Lautstärke, Mute, Quelle und Sound-Profile
- Dynamische Quellen und Profile: Die Integration übernimmt nur Werte, die ein Gerät tatsächlich meldet
- Kein Tracking und keine Übertragung von Telemetrie an Dritte

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

Die Begriffe und Werte für Quellen und Sound-Profile werden nicht fest in den Code geschrieben. Sie müssen vom Gerät bzw. der verifizierten API stammen, damit verschiedene Hardware-Revisionen und Firmware-Versionen funktionieren.

## Installation

### Manuell

1. Dieses Repository klonen oder herunterladen.
2. Den Ordner `custom_components/kef_ls50_wireless` nach `/config/custom_components/kef_ls50_wireless` kopieren.
3. Home Assistant neu starten.
4. Zu **Einstellungen → Geräte & Dienste → Integration hinzufügen** gehen.
5. Nach **KEF LS50 Wireless** suchen und die lokale IP-Adresse oder den Hostnamen des eigenen Lautsprechers eingeben.

### Entwicklung mit Git

```bash
git clone https://github.com/aharder3/ha-kef-custom.git
cd ha-kef-custom
ln -s "$(pwd)/custom_components/kef_ls50_wireless" /config/custom_components/kef_ls50_wireless
```

Danach Home Assistant neu starten. Bei Home Assistant OS kann der Ordner stattdessen über das Samba-Share oder ein Add-on in `/config/custom_components/` kopiert werden.

## Debug-Logging

Für die Entwicklung kann gezielt Debug-Logging aktiviert werden:

```yaml
logger:
  default: info
  logs:
    custom_components.kef_ls50_wireless: debug
```

Danach Home Assistant neu starten oder die Integration neu laden. Vor einem öffentlichen Log-Auszug müssen IP-Adressen, Gerätekennungen, Cookies, Autorisierungs-Header und Tokens entfernt werden.

## API-Erfassung

Die lokale API wird ausschließlich mit Geräten im eigenen Netzwerk untersucht. Für jede Aktion sind nur bereinigte Daten erforderlich:

- HTTP-Methode und Pfad
- Request-Header ohne Geheimnisse
- Request- und Response-Body mit ersetzten IDs/Tokens
- Die ausgeführte Aktion, etwa Mute an/aus oder Quelle wechseln

Beispiel einer sicheren Dokumentation:

```text
Aktion: Quelle wechseln
Methode: POST
Pfad: /api/<REDACTED>/source
Request: {"source": "<SOURCE_NAME>"}
Response: {"source": "<SOURCE_NAME>"}
```

### Niemals committen

- API-Tokens, Passwörter, Cookies oder Authorization-Header
- Private IP-Adressen, MAC-Adressen und Seriennummern
- Vollständige mitmproxy-, HAR-, PCAP- oder Debug-Log-Dateien
- Home-Assistant-Dateien wie `secrets.yaml`, `.storage/` oder `.env`

`.gitignore` ignoriert die häufigsten dieser Artefakte bereits. Ein Mitschnitt bleibt lokal und wird vor jeder Weitergabe manuell bereinigt.

## Architektur

```text
custom_components/kef_ls50_wireless/
├── __init__.py       # Setup/Unload des Config Entry
├── api.py            # Asynchroner lokaler API-Client
├── config_flow.py    # Eingabe und Validierung des Hosts
├── const.py          # Domain, Optionen und Konstanten
├── coordinator.py    # Zentraler Polling- und Fehlerbehandlungsmechanismus
├── manifest.json     # Home-Assistant-Metadaten
├── media_player.py   # Lautsprecher-Entity
├── select.py         # Sound-Profile, sobald API bekannt ist
├── strings.json      # Englische Konfigurations-Texte
└── translations/
    └── de.json       # Deutsche Übersetzung
```

Der `DataUpdateCoordinator` fragt einen gemeinsamen Status ab. Entities lesen ausschließlich diesen Zustand und lösen über den API-Client gezielte Befehle aus. Dies vermeidet paralleles Polling und hält Updates konsistent.

## Entwicklung

```bash
python -m venv .venv
source .venv/bin/activate
pip install ruff pytest pytest-homeassistant-custom-component
ruff check custom_components
pytest
```

Die konkrete Testkonfiguration wird erweitert, sobald stabile API-Fixtures ohne sensible Informationen vorliegen.

## Mitwirken

1. Fork erstellen.
2. Branch für eine Änderung anlegen.
3. Keine privaten Daten einchecken.
4. Linting und Tests ausführen.
5. Pull Request mit Gerätegeneration, Firmware-Version und bereinigten Beispielantworten erstellen.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. KEF und LS50 Wireless sind Marken ihrer jeweiligen Inhaber. Dieses Projekt ist nicht mit KEF verbunden oder von KEF unterstützt.
