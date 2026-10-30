# Übergabe: Steigungsprofil Sydney-Marathon

Stand 28.10.2026, App-Version **1.36** (1.36: offline nur noch aus dem eigenen Speicher, Rückfallseite bei jedem Besuch erneuert (Service Worker); 1.35: im Ziel 42,195 statt 42,2 in Anzeige, Gesamtstrecke, Zwischenzeiten und Pace-Band; 1.34: Maßstab auf der Karte ohne Kasten, kleiner, in der freieren linken Ecke; 1.33: im Vollbild der Ort groß oben rechts statt am Pfeil, Maßstab auf der Karte; 1.32: Kopf mit Ort groß und „Streckenplan und Steigungsprofil“, Umschalter Karte | Zahlen statt Pünktchen, Karte zuerst, Name der Strecke im Vollbild; 1.31: zu breite Tabellen werden stufenweise enger statt rechts abgeschnitten; 1.30: Mauer-Beschriftung in einer freien Zeile über dem Profil, mittig über der Mauer, nur bei `D.mauer`; 1.29: Mauer-Beschriftung im Profil neben dem Gipfel statt darauf, nur bei `D.mauer`; 1.28: Mauer je Durchgang ein Rad mit Empfehlung nach Zielzeit, nur bei `D.mauer`; 1.27: Mauer-Zeit und Tor-Rechner für Strecken mit `D.mauer`, sonst unverändert; 1.26: Steigungskosten als große Zeile unter der Zielzeit; 1.25: Umschalter Höhe/Meereshöhe für die Tabelle „Ohne Höhenmeter“, nur bei `D.lage`; 1.24: Feld `D.lage` für hoch gelegene Strecken: Tabelle „Ohne Höhenmeter“ nennt dann die Höhe; 1.23: unter der Zielzeit Pace auf flachen Stücken und im Schnitt; 1.22: Pace im Flachen mit zwei Nachkommastellen; 1.21: weißer Punkt im Pace-Diagramm ist der Flachpunkt 0 % mit Flach-Pace statt der aktuellen Stelle; 1.20: Markierung im Pace-Diagramm stufenlos und ohne Wackeln, Tippen daneben nimmt sie weg, Punkt „hier“ mit km; 1.19: Markierung im Pace-Diagramm auch waagerecht zur Pace-Achse; 1.18: Pace-Diagramm ohne Laborlinie und graue Zone, −15 bis +10 %, Achse bei 0 %, Markierung zum Antippen; 1.17: Bergab fest „halb“ ohne Schalter, steiler als −8 % kein weiterer Gewinn statt U-Kurve; 1.16: flacher Halbmarathon in der Tabelle ohne Höhenmeter, Erklärung im Info-Fenster (i); 1.15: Kosten je Höhenmeter bei 4:00 /km mit wählbarer Bezugs-Pace, Bahnzeiten als Tabelle, größere Überschriften in den Einstellungen; 1.14: unter der Zielzeit flacher Marathon und Bahnzeiten 10 000 m / 5000 m; 1.13: Zeiten immer mit 100 m, „Pace hier“ über das Messfenster gemittelt; 1.12: Messfenster 50 / 100 / 200 m / 1 km statt 10 m, neuer Erklärtext; 1.11: Zwischenzeiten mit Halbmarathon-Zeile und „je 10 km“; 1.10: Knopfrahmen so hell wie die Räder, „Vollbild“ blau, im Vollbild führt ‹ zurück in die normale Ansicht; 1.9: Kopf eines offenen Abschnitts bleibt oben stehen, Zuklappen von überall; 1.8: beim Aufklappen bleibt der Kopf des Abschnitts an seiner Stelle; 1.7: Hinweis, wenn die eingestellte Startzeit zu keiner Welle passt; 1.6: Standard 5 km Ausschnitt und Tempo ×200, Menü-Knopf blau mit Beschriftung, Abschnitte unter dem Läuferblick aufklappbar; 1.5: Startwellen mit Uhrzeiten unter „Deine Startzeit“, Start 6:32 (Lila 1) statt 6:30; 1.4: Pfeile in Bisher/Noch/Ganze Strecke und Rampe als Grafik, dreistellige Werte ohne „…“, zu breite Werte werden kleiner; 1.3: Bergab U-Kurve statt Grenze bei −4 %: am schnellsten bei −8 %, ab −16 % langsamer als flach, ohne Knick bei 0 %; 1.2: Tempo-Rad mit ×1 (Echtzeit), ×50 und ×100–×180 in 20er-Schritten; 1.1: auf der Brücke stand in der Straßenleiste „Cahill Expressway“, jetzt „Harbour Bridge“; 1.0: Erstausgabe), live unter https://luperttrading-lab.github.io/marathon-strecken/sydney/.

Die App ist eine Kopie der Boston-App (Stand 1.2) mit eigenen Daten, Texten und Speicherschlüsseln (`syd-…`), ohne eigenes
Manifest und Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in
[`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Änderungen am gemeinsamen Code in allen Apps nachziehen (README).

TCS Sydney Marathon am Sonntag, 29. August 2027 (Seite des Veranstalters). Start der Läufer 6:30 Uhr (Rollstühle 6:15),
`D.start` = 392 (Startgruppe Lila 1 um 6:32, seit 1.5; alle zwölf Gruppen in `D.wellen`), `D.tz` Australia/Sydney, `D.ortKurz` „ Sydney“. Von der Miller Street in North Sydney zum Opernhaus. Seit 2025
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
