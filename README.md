# DWZ (Schachbund) — Home Assistant Integration

Diese Integration stellt DWZ‑Daten (Deutscher Schachbund) als Home‑Assistant‑Sensoren bereit.

## Was es liefert
- Ein Sensor pro Konfigurationseintrag (pro Spieler/NU‑ID).
- Sensor‑State: die aktuelle DWZ‑Bewertung (`rating`).
- Weiteren Werte werden als Entity‑Attribute bereitgestellt:
  - `rating`: Die aktuelle DWZ (identisch mit dem `state`)
  - `rating_week`: Woche der letzten Auswertung (z.B. "202617"); wie in der Datenquelle
  - `rating_date`: letzter Tag dieser Woche im ISO-Format YYYY-MM-DD
  - `index`: Laufende Nummer der aktuellen DWZ-Auswertung
  - `active_club`: Im Deutschen Schachbund (DSB) darf eine Person nur eine einzige Spielberechtigung besitzen. Nur diese wird angezeigt.
  - `firstname`: Vorname des Spielers
  - `lastname`: Nachname des Spielers
  - `full_name`: Voller Name des Spielers
  - `gender`: Geschlecht (`MALE|FEMALE`)
  - `birth_year`: Geburtsjahr des Spielers
  - `fide_id`: FIDE-ID (falls vorhanden)
  - `nuliga_id`: Die nuLiga-ID des Spielers


## Installation
### Via HACS

1. Öffne HACS → Integrationen.
2. Klicke auf die drei Punkte oben rechts → "Custom repositories".
3. Wähle `Integration` als Kategorie und füge das Repository `f-zappa/ha-dwz` hinzu.
4. Suche in HACS nach "DWZ (Schachbund)" und installiere die Integration.
5. Nach Installation Home Assistant neu starten und die Integration über Einstellungen → Integrationen hinzufügen.

Hinweis: HACS ermöglicht automatische Updates und vereinfacht die Installation für Endnutzer.

### Manuell (Entwickler / lokale Installation)
1. Kopiere das Verzeichnis `custom_components/dwz` in dein HA‑`custom_components` Ordner.
2. Starte Home Assistant neu oder lade die Integration über die UI neu.

## Konfiguration
- Integration → Integration hinzufügen → `DWZ (Schachbund)`.
- In der Konfigurationsoberfläche die `NU`‑ID angeben (z. B. `NU4168433`).
- Die Config‑Flow validiert IDs und zeigt hilfreiche Fehlermeldungen (z. B. `not_found`).
