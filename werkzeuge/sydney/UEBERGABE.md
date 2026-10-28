# Übergabe: Steigungsprofil Sydney-Marathon

Stand 28.10.2026, App-Version **1.1** (1.1: auf der Brücke stand in der Straßenleiste „Cahill Expressway“, jetzt „Harbour Bridge“; 1.0: Erstausgabe), live unter https://luperttrading-lab.github.io/marathon-strecken/sydney/.

Die App ist eine Kopie der Boston-App (Stand 1.2) mit eigenen Daten, Texten und Speicherschlüsseln (`syd-…`), ohne eigenes
Manifest und Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in
[`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Änderungen am gemeinsamen Code in allen Apps nachziehen (README).

TCS Sydney Marathon am Sonntag, 29. August 2027 (Seite des Veranstalters). Start der Läufer 6:30 Uhr (Rollstühle 6:15),
`D.start` = 390, `D.tz` Australia/Sydney, `D.ortKurz` „ Sydney“. Von der Miller Street in North Sydney zum Opernhaus. Seit 2025
Abbott World Marathon Major.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

1. **Strecke:** offizielle GPX des Veranstalters (`../dl/sydney2026_offiziell.gpx`, verlinkt auf tcssydneymarathon.com/marathon
   als „TCS_Sydney_Marathon_2026_Course.gpx“; es ist die Datei von goandrace.com, 650 Punkte). `parse.py` übernimmt sie direkt:
   Die Strecke läuft oft auf derselben Straße hin und zurück, das Anlegen auf das OSM-Netz (`match_versuch.py`, wie Paris)
   verlor an den Wendepunkten Stücke und wurde 45 km lang. Die Linie liegt auf den Straßen (Median 2,9 m, 90 % unter 7 m).
   42,242 km, `common.py` staucht gleichmäßig.
2. `dgm.py`: **NSW 5m Elevation** (NSW Spatial Services, ImageServer `getSamples`, Multipoint je 100 Punkte, bilinear; Gelände
   aus 1-m/2-m-Laser und Photogrammetrie, Höhen über AHD). 4226 Punkte in 23 s.
3. **Brücken und Hochstraßen:** Ein offenes Oberflächenmodell gibt es nicht (Punktwolken nur über ELVIS, hier gesperrt;
   Copernicus 30 m liegt 5–15 m zu hoch und über Wasser auf 0, `../dl/cop_s34_e151.tif`). `clean.py`: Hochstraßen von Hand
   (`HOCH`, Linienmeter, wo die Fahrbahn den Boden verlässt und wieder aufsetzt), dazwischen gerade, gestrichelt: Harbour Bridge
   mit Rampen 1600–3300 (42,4 → 38,9 m; der Scheitel über dem Hafen fehlt, Angaben zur Fahrbahnhöhe widersprechen sich:
   49 m Durchfahrtshöhe, 53 oder 59 m Fahrbahn), Western Distributor nach Pyrmont 3550–5450 und zurück zur King Street
   7900–9050. Die automatische Suche über OSM-Brücken (wie Tokio) zerlegte sie falsch und hätte die Brücke auf 8 m gelegt.
   Übrige Stufen wie bei den anderen Strecken (Unterführungen am Hickson Road, unter dem Cahill Expressway am Opernhaus).
4. `osm.py` (BBBike-Auszug Sydney), `streets.py` (wie Tokio: nächster Weg je 10 m, Hauptstraßen bevorzugt, ohne Tunnel; auf der Brücke liegt die GPX
   zwischen Bradfield Highway und den Cahill-Spuren, dort gilt der Brückenname aus OSM, „Harbour Bridge“, wie in New York),
   `orte.py` (Vororte: Flächen admin_level 10), `build.py`, `route.py` (lat0/lon0 −34,0/151,1), `tiles.py`, dann aus
   `werkzeuge/`: `tiles_z11.py sydney`, `work/app.py` (aus `boston/index.html`), `tiles_rand.py sydney 2`.

## Ergebnis

↑ 220 m / ↓ 303 m mit 200-m-Fenster, ↑ 263 / ↓ 346 m mit 50 m, Rohdaten ↑ 447 m. Start 85,9 m (höchster Punkt), tiefster
2,0 m (Sussex Street, km 9,5), Ziel 3,3 m: 82,6 m Nettogefälle, der Veranstalter nennt 83 m. Seinen Anstieg von 313 m erreicht
nur die Zählweise mit kurzem Fenster (vermutlich GPS-Daten). Steilste Stellen über 200 m: −7,2 % in Pyrmont zur Pirrama Road
(km 6,4), +5,0 % die Bent Street hinauf (km 13,6). Mit 4:00/km im Flachen ergibt das Modell 2:50:23.

## Offen

- Prüfung am iPhone.
- Fahrbahn der Harbour Bridge und der Hochstraßen messen (NSW-Punktwolke über ELVIS, Kachel Sydney).
- Getränkestellen: Der Veranstalter zeigt sie nur in der TRACX-App; Strecke 2027 prüfen, sobald veröffentlicht.
