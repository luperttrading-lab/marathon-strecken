# Marathon-Strecken

Steigungsprofile von Marathonstrecken als Web-Apps für den Home-Bildschirm, ausgeliefert über GitHub Pages.
Inoffiziell, kein Angebot der Veranstalter.

**Startseite mit Auswahl:** https://luperttrading-lab.github.io/marathon-strecken/ – in Safari öffnen, *Teilen → Zum Home-Bildschirm*,
dann liegen alle Strecken in einer App.

| Strecke | App | Ordner | Aufbereitung |
|---|---|---|---|
| Hamburg (Kurs 2025/2026) | https://luperttrading-lab.github.io/marathon-strecken/hamburg/ | [`hamburg/`](hamburg/) | [`werkzeuge/hamburg/`](werkzeuge/hamburg/UEBERGABE.md) |
| Berlin (Kurs 2026) | https://luperttrading-lab.github.io/marathon-strecken/berlin/ | [`berlin/`](berlin/) | [`werkzeuge/berlin/`](werkzeuge/berlin/UEBERGABE.md) |
| Frankfurt (Kurs 2026) | https://luperttrading-lab.github.io/marathon-strecken/frankfurt/ | [`frankfurt/`](frankfurt/) | [`werkzeuge/frankfurt/`](werkzeuge/frankfurt/UEBERGABE.md) |
| New York (Kurs 2026) | https://luperttrading-lab.github.io/marathon-strecken/newyork/ | [`newyork/`](newyork/) | [`werkzeuge/newyork/`](werkzeuge/newyork/UEBERGABE.md) |
| Köln (Kurs 2026) | https://luperttrading-lab.github.io/marathon-strecken/koeln/ | [`koeln/`](koeln/) | [`werkzeuge/koeln/`](werkzeuge/koeln/UEBERGABE.md) |

## Regeln für Änderungen

- Gearbeitet wird direkt in `<strecke>/index.html` bzw. `index.html` (Startseite). Die Skripte unter `werkzeuge/` sind nur die Herkunft.
- Hamburg, Berlin, Frankfurt, New York und Köln haben **denselben Code**; sie unterscheiden sich nur in den Daten (`const D`), den Texten zur
  Strecke und den Speicherschlüsseln (`hhm-…`, `bln-…`, `ffm-…`, `nyc-…`, `kln-…`). Eine Änderung am Verhalten oder Aussehen in **allen** Dateien nachziehen.
- Jede App und die Startseite haben ihre eigene Versionsnummer: bei jeder Änderung `APP_VERSION` in der `index.html` und
  `version.json` im selben Ordner gemeinsam hochzählen, sonst kommt das Update auf dem iPhone nicht an.
- Jeder Ordner hat einen eigenen Service Worker mit eigenem Cache-Präfix (`hh-`, `bln-`, `ffm-`, `nyc-`, `kln-`, `start-`). Ein Service Worker löscht
  nur Caches mit seinem eigenen Präfix, weil sich alle Apps unter `luperttrading-lab.github.io` denselben Speicher teilen.
- Hell/Dunkel gilt für alle Strecken gemeinsam (`localStorage` `marathon-theme`). Die Startseite ist immer dunkel, in den
  Farben ihres App-Symbols „42,195“ (Schwarz, Blau #1b5bd0/#6a9cff), und hat keinen eigenen Umschalter.
- **Renntermine** auf der Startseite: `data-termine` an jeder Karte (ISO-Daten, durch Leerzeichen getrennt, `?` = vom
  Veranstalter noch nicht bestätigt, angezeigt als „ca. 31. Oktober 2027“). Die Seite zeigt selbst den nächsten Termin ab heute
  mit Countdown; ist keiner mehr bekannt, nur den üblichen Monat (`data-monat`). Einmal im Jahr neue Termine nachtragen,
  **auch in jeder Strecke** in `D.termine` (gleiche Schreibweise, steuert „Live nach Plan“ am Renntag). Dort stehen außerdem
  `D.tz` (Zeitzone der Uhrzeiten) und `D.start` (Startzeit der ersten Welle in Minuten ab Mitternacht).
- Neue Strecke: eigener Ordner neben den anderen, Karte auf der Startseite ergänzen. Reihenfolge: New York als Highlight oben
  (Klasse `card top`), danach die deutschen Strecken alphabetisch. Alle Strecken liegen in **einer** App: installiert wird
  die Startseite, ihr Scope umfasst alle Unterordner. Die Strecken haben **kein eigenes Manifest und Symbol**, sie verweisen auf
  `../manifest.webmanifest`, `../apple-touch-icon.png` und `../icon-192.png`; *Zum Home-Bildschirm* aus einer Strecke
  installiert so ebenfalls die ganze App.
  Übersichtskarte: `cd werkzeuge && python3 tiles_z11.py <strecke>`, Ergebnis in `D.tiles["11"]` und in die Kartenliste von `sw.js`.
  Danach `python3 tiles_rand.py <strecke>` (New York: `tiles_rand.py newyork 2`): baut z11–z13 mit einem Kachelrand entlang der Strecke
  neu, damit die mitlaufende Karte an Start, Ziel und Außenkurven nicht ins Graue schaut, und trägt `D.tiles` und `sw.js` selbst ein.
