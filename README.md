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
| London (Kurs 2026, Blue Start) | https://luperttrading-lab.github.io/marathon-strecken/london/ | [`london/`](london/) | [`werkzeuge/london/`](werkzeuge/london/UEBERGABE.md) |
| Paris (Kurs 2025) | https://luperttrading-lab.github.io/marathon-strecken/paris/ | [`paris/`](paris/) | [`werkzeuge/paris/`](werkzeuge/paris/UEBERGABE.md) |
| Chicago (Kurs 2026) | https://luperttrading-lab.github.io/marathon-strecken/chicago/ | [`chicago/`](chicago/) | [`werkzeuge/chicago/`](werkzeuge/chicago/UEBERGABE.md) |
| Tokio (Kurs 2026) | https://luperttrading-lab.github.io/marathon-strecken/tokio/ | [`tokio/`](tokio/) | [`werkzeuge/tokio/`](werkzeuge/tokio/UEBERGABE.md) |
| Boston (Kurs 2026) | https://luperttrading-lab.github.io/marathon-strecken/boston/ | [`boston/`](boston/) | [`werkzeuge/boston/`](werkzeuge/boston/UEBERGABE.md) |
| Köln (Kurs 2026) | https://luperttrading-lab.github.io/marathon-strecken/koeln/ | [`koeln/`](koeln/) | [`werkzeuge/koeln/`](werkzeuge/koeln/UEBERGABE.md) |
| München (Kurs 2026) | https://luperttrading-lab.github.io/marathon-strecken/muenchen/ | [`muenchen/`](muenchen/) | [`werkzeuge/muenchen/`](werkzeuge/muenchen/UEBERGABE.md) |
| Oberelbe (Kurs 2026) | https://luperttrading-lab.github.io/marathon-strecken/oberelbe/ | [`oberelbe/`](oberelbe/) | [`werkzeuge/oberelbe/`](werkzeuge/oberelbe/UEBERGABE.md) |
| Rennsteiglauf-Marathon (Kurs 2026) | https://luperttrading-lab.github.io/marathon-strecken/rennsteig/ | [`rennsteig/`](rennsteig/) | [`werkzeuge/rennsteig/`](werkzeuge/rennsteig/UEBERGABE.md) |

## Regeln für Änderungen

- Gearbeitet wird direkt in `<strecke>/index.html` bzw. `index.html` (Startseite). Die Skripte unter `werkzeuge/` sind nur die Herkunft.
- Hamburg, Berlin, Frankfurt, New York, London, Paris, Chicago, Tokio, Boston, Köln, München, Oberelbe und Rennsteig haben **denselben Code**; sie unterscheiden sich nur in den Daten (`const D`), den Texten zur
  Strecke und den Speicherschlüsseln (`hhm-…`, `bln-…`, `ffm-…`, `nyc-…`, `ldn-…`, `par-…`, `chi-…`, `tyo-…`, `bos-…`, `kln-…`, `muc-…`, `oem-…`, `rsl-…`). Eine Änderung am Verhalten oder Aussehen in **allen** Dateien nachziehen.
- Jede App und die Startseite haben ihre eigene Versionsnummer: bei jeder Änderung `APP_VERSION` in der `index.html` und
  `version.json` im selben Ordner gemeinsam hochzählen, sonst kommt das Update auf dem iPhone nicht an.
- Jeder Ordner hat einen eigenen Service Worker mit eigenem Cache-Präfix (`hh-`, `bln-`, `ffm-`, `nyc-`, `ldn-`, `par-`, `chi-`, `tyo-`, `bos-`, `kln-`, `muc-`, `oem-`, `rsl-`, `start-`). Ein Service Worker löscht
  nur Caches mit seinem eigenen Präfix, weil sich alle Apps unter `luperttrading-lab.github.io` denselben Speicher teilen.
- **Nur dunkel** (seit Hamburg 1.35 in allen Strecken): kein Hell/Dunkel-Umschalter mehr, keine hellen Kartenbilder.
  Die Startseite ist ebenfalls immer dunkel, in den
  Farben ihres App-Symbols „42,195“ (Schwarz, Blau #1b5bd0/#6a9cff), und hat keinen eigenen Umschalter.
- **Renntermine** auf der Startseite: `data-termine` an jeder Karte (ISO-Daten, durch Leerzeichen getrennt, `?` = vom
  Veranstalter noch nicht bestätigt, angezeigt als „ca. 31. Oktober 2027“). Die Seite zeigt selbst den nächsten Termin ab heute
  mit Countdown; ist keiner mehr bekannt, nur den üblichen Monat (`data-monat`). Einmal im Jahr neue Termine nachtragen,
  **auch in jeder Strecke** in `D.termine` (gleiche Schreibweise, steuert „Live nach Plan“ am Renntag). Dort stehen außerdem
  `D.tz` (Zeitzone der Uhrzeiten; `D.ort`/`D.ortKurz` nennen den Ort dazu, wenn die Zeitzone ihn nicht verrät, z. B. Boston) und `D.start` (Startzeit der ersten Welle in Minuten ab Mitternacht).
- Neue Strecke: eigener Ordner neben den anderen, Karte auf der Startseite ergänzen. Reihenfolge: New York als Highlight oben
  (Klasse `card top`), danach London, Paris, Chicago, Tokio und Boston (nach Teilnehmerzahl), dann die deutschen Strecken alphabetisch. Alle Strecken liegen in **einer** App: installiert wird
  die Startseite, ihr Scope umfasst alle Unterordner. Die Strecken haben **kein eigenes Manifest und Symbol**, sie verweisen auf
  `../manifest.webmanifest`, `../apple-touch-icon.png` und `../icon-192.png`; *Zum Home-Bildschirm* aus einer Strecke
  installiert so ebenfalls die ganze App.
- Kartenzeile der Startseite: Höhenmeter bergauf und bergab mit 200-m-Fenster (Werte wie „Ganze Strecke“ in der App), Pfeile als
  gezeichnete Linien (`.pf`, SVG), nicht als Textzeichen ↑: das saß auf dem iPhone klein und tief (seit Startseite 1.16).
- Hinweis-Kasten unter einer Karte (`div.hinweis` direkt nach dem `<a class="card">`, Überschrift in `.kopf`): seit Startseite 1.18
  für Paris (neuer Veranstalter ab 2027, neue Strecke erst Anfang 2027; die App zeigt den Kurs 2025). Entfernen bzw. neu
  schreiben, sobald die Strecke 2027 da ist.
- Mini-Profile der Startseite: gemeinsamer Höhenmaßstab 40 m = 56 px (Weg je Karte gleich breit), Grundhöhe 64 px;
  mehr Höhenbereich bekommt eine höhere Grafik statt eines anderen Maßstabs (`.spark.hoch` New York 112 px,
  `.spark.berg` Rennsteig 240 px, `.spark.boston` 208 px, `.spark.london` 80 px). Pfad: 200 Punkte, je Punkt das Maximum der letzten 100 m.
  Übersichtskarte: `cd werkzeuge && python3 tiles_z11.py <strecke>`, Ergebnis in `D.tiles["11"]` und in die Kartenliste von `sw.js`.
  Danach `python3 tiles_rand.py <strecke>` (New York, London, Paris, Chicago, Tokio und Boston: `tiles_rand.py <strecke> 2`): baut z11–z13 mit einem Kachelrand entlang der Strecke
  neu, damit die mitlaufende Karte an Start, Ziel und Außenkurven nicht ins Graue schaut, und trägt `D.tiles` und `sw.js` selbst ein.
