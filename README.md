# Marathon-Strecken

Steigungsprofile von Marathonstrecken als Web-Apps für den Home-Bildschirm, ausgeliefert über GitHub Pages.
Inoffiziell, kein Angebot der Veranstalter.

**Startseite mit Auswahl:** https://luperttrading-lab.github.io/marathon-strecken/ – in Safari öffnen, *Teilen → Zum Home-Bildschirm*,
dann liegen alle Strecken in einer App.

| Strecke | App | Ordner | Aufbereitung |
|---|---|---|---|
| Hamburg (Kurs 2025/2026) | https://luperttrading-lab.github.io/marathon-strecken/hamburg/ | [`hamburg/`](hamburg/) | [`werkzeuge/hamburg/`](werkzeuge/hamburg/UEBERGABE.md) |
| Frankfurt (Kurs 2026) | https://luperttrading-lab.github.io/marathon-strecken/frankfurt/ | [`frankfurt/`](frankfurt/) | [`werkzeuge/frankfurt/`](werkzeuge/frankfurt/UEBERGABE.md) |

## Regeln für Änderungen

- Gearbeitet wird direkt in `<strecke>/index.html` bzw. `index.html` (Startseite). Die Skripte unter `werkzeuge/` sind nur die Herkunft.
- Hamburg und Frankfurt haben **denselben Code**; sie unterscheiden sich nur in den Daten (`const D`), den Texten zur Strecke
  und den Speicherschlüsseln (`hhm-…` bzw. `ffm-…`). Eine Änderung am Verhalten oder Aussehen in **beiden** Dateien nachziehen.
- Jede App und die Startseite haben ihre eigene Versionsnummer: bei jeder Änderung `APP_VERSION` in der `index.html` und
  `version.json` im selben Ordner gemeinsam hochzählen, sonst kommt das Update auf dem iPhone nicht an.
- Jeder Ordner hat einen eigenen Service Worker mit eigenem Cache-Präfix (`hh-`, `ffm-`, `start-`). Ein Service Worker löscht
  nur Caches mit seinem eigenen Präfix, weil sich alle Apps unter `luperttrading-lab.github.io` denselben Speicher teilen.
- Hell/Dunkel gilt für beide Strecken gemeinsam (`localStorage` `marathon-theme`). Die Startseite ist immer dunkel, in den
  Farben ihres App-Symbols „42,195“ (Schwarz, Blau #1b5bd0/#6a9cff), und hat keinen eigenen Umschalter.
- Neue Strecke: eigener Ordner neben den anderen, Karte auf der Startseite ergänzen.
