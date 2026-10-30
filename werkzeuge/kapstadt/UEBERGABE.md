# Übergabe: Steigungsprofil Kapstadt-Marathon

Stand 28.10.2026, App-Version **1.33** (1.33: Maßstab auf der Karte ohne Kasten, kleiner, in der freieren linken Ecke; 1.32: im Vollbild der Ort groß oben rechts statt am Pfeil, Maßstab auf der Karte; 1.31: Kopf mit Ort groß und „Streckenplan und Steigungsprofil“, Umschalter Karte | Zahlen statt Pünktchen, Karte zuerst, Name der Strecke im Vollbild; 1.30: zu breite Tabellen werden stufenweise enger statt rechts abgeschnitten; 1.29: Mauer-Beschriftung in einer freien Zeile über dem Profil, mittig über der Mauer, nur bei `D.mauer`; 1.28: Mauer-Beschriftung im Profil neben dem Gipfel statt darauf, nur bei `D.mauer`; 1.27: Mauer je Durchgang ein Rad mit Empfehlung nach Zielzeit, nur bei `D.mauer`; 1.26: Mauer-Zeit und Tor-Rechner für Strecken mit `D.mauer`, sonst unverändert; 1.25: Steigungskosten als große Zeile unter der Zielzeit; 1.24: Umschalter Höhe/Meereshöhe für die Tabelle „Ohne Höhenmeter“, nur bei `D.lage`; 1.23: Feld `D.lage` für hoch gelegene Strecken: Tabelle „Ohne Höhenmeter“ nennt dann die Höhe; 1.22: unter der Zielzeit Pace auf flachen Stücken und im Schnitt; 1.21: Pace im Flachen mit zwei Nachkommastellen; 1.20: weißer Punkt im Pace-Diagramm ist der Flachpunkt 0 % mit Flach-Pace statt der aktuellen Stelle; 1.19: Markierung im Pace-Diagramm stufenlos und ohne Wackeln, Tippen daneben nimmt sie weg, Punkt „hier“ mit km; 1.18: Markierung im Pace-Diagramm auch waagerecht zur Pace-Achse; 1.17: Pace-Diagramm ohne Laborlinie und graue Zone, −15 bis +10 %, Achse bei 0 %, Markierung zum Antippen; 1.16: Bergab fest „halb“ ohne Schalter, steiler als −8 % kein weiterer Gewinn statt U-Kurve; 1.15: flacher Halbmarathon in der Tabelle ohne Höhenmeter, Erklärung im Info-Fenster (i); 1.14: Kosten je Höhenmeter bei 4:00 /km mit wählbarer Bezugs-Pace, Bahnzeiten als Tabelle, größere Überschriften in den Einstellungen; 1.13: unter der Zielzeit flacher Marathon und Bahnzeiten 10 000 m / 5000 m; 1.12: Zeiten immer mit 100 m, „Pace hier“ über das Messfenster gemittelt; 1.11: Messfenster 50 / 100 / 200 m / 1 km statt 10 m, neuer Erklärtext; 1.10: Zwischenzeiten mit Halbmarathon-Zeile und „je 10 km“; 1.9: Knopfrahmen so hell wie die Räder, „Vollbild“ blau, im Vollbild führt ‹ zurück in die normale Ansicht; 1.8: Kopf eines offenen Abschnitts bleibt oben stehen, Zuklappen von überall; 1.7: beim Aufklappen bleibt der Kopf des Abschnitts an seiner Stelle; 1.6: Hinweis, wenn die eingestellte Startzeit zu keiner Welle passt; „Blöcke“ statt „Batches“; 1.5: Standard 5 km Ausschnitt und Tempo ×200, Menü-Knopf blau mit Beschriftung, Abschnitte unter dem Läuferblick aufklappbar; 1.4: Startwellen mit Uhrzeiten unter „Deine Startzeit“, Start 8:10 (Welle 1) statt 8:00 (Elite); 1.3: Pfeile in Bisher/Noch/Ganze Strecke und Rampe als Grafik, dreistellige Werte ohne „…“, zu breite Werte werden kleiner; 1.2: Bergab U-Kurve statt Grenze bei −4 %: am schnellsten bei −8 %, ab −16 % langsamer als flach, ohne Knick bei 0 %; 1.1: Tempo-Rad mit ×1 (Echtzeit), ×50 und ×100–×180 in 20er-Schritten; 1.0: Erstausgabe), live unter https://luperttrading-lab.github.io/marathon-strecken/kapstadt/.

Die App ist eine Kopie der Boston-App (Stand 1.2) mit eigenen Daten, Texten und Speicherschlüsseln (`cpt-…`), ohne eigenes
Manifest und Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in
[`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Änderungen am gemeinsamen Code in allen Apps nachziehen (README).

Sanlam Cape Town Marathon am Sonntag, 23. Mai 2027, erste Ausgabe als Abbott World Marathon Major (bestätigt am 10. Juni 2026
nach dem Rennen vom 24. Mai 2026; das Rennen im Oktober 2025 fiel am Renntag wegen Sturm aus). Start 2026: Elite 8:00 Uhr
(Rollstühle 7:50, Wellen bis 9:06), `D.start` = 490 (Welle 1 um 8:10, seit 1.4; Wellen in `D.wellen`), `D.tz` Africa/Johannesburg, `D.ort` „Kapstadt“. Im Mai gilt in Deutschland
dieselbe Uhrzeit (UTC+2), die App zeigt deshalb keinen Zeitunterschied.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

1. **Strecke:** Der Veranstalter veröffentlicht die Strecke nur als Bild (`../dl/route.jpg`, Profil `profil.webp`, Landmarken-PDF).
   Linie von goandrace.com (`../dl/kapstadt2025_goandrace.gpx`, für 2025 veröffentlicht, 1436 Punkte, 42,25 km). `osm.py`:
   OSM-Wege aus dem BBBike-Auszug Kapstadt (`../dl/CapeTown.osm.pbf`, 24.10.2026; die Overpass-Spiegel antworteten nicht),
   `match.py` (wie Paris, ohne Pflichtpunkte, Autobahnen erlaubt: die Strecke läuft über den Nelson Mandela Boulevard).
   Linie 42,940 km, 1,8 % länger als vermessen, `common.py` staucht gleichmäßig.
2. **Abgleich mit der Karte 2026** (`karte.py`): gelbe Streckenpixel des Bildes affin auf die Linie gelegt (Startwert aus drei
   Stellen, dann iterativ). Median 8 m, jedes Stück der Linie hat Kartenpixel in 80 m Nähe: Die Strecke 2026 ist die Linie.
   Alle zehn Kontrollpunkte (Cut-off 1–10) liegen auf denselben Straßen. Die 15 Getränkestellen (Becher-Symbole, von Hand
   abgelesen) daraus auf die Linie projiziert, in Reihenfolge der Nummern; die Symbole stehen 50–170 m neben der Strecke,
   Lage deshalb etwa ±100 m. Laut Läuferguides Wasser und Powerade, ab km 25 auch Cola (nicht amtlich bestätigt).
3. `dgm.py`: **Ground Level Map 2019** der Stadt (5 m, Laser, bare earth, ±0,3 m) über GetFeatureInfo des WMS
   (`cityimg.capetown.gov.za/erdas-iws/ogc/wms/GeoSpatial Datasets`, Ebene `Elevation_CCT_GLM2019_5m_DEM`, `info_format=
   application/json`: „raw“ Band 0 = Höhe). Der ArcGIS-Dienst derselben Ebene liefert nur Graustufen. 1,7 s je Abfrage,
   8 parallel, 4296 Punkte in 13 min.
4. `lidar.py`: **Hochstraßen gemessen**: auf OSM-Brücken Fahrbahn = DTM 2025 (`Elevation_DTM_2m`) + Höhe über Grund
   (`Elevation_Height_Map_1m`, LiDAR 2025), Median über 50 m; auf den Rampen (100 m davor und danach) nur das DTM 2025, das
   die aufgeschütteten Rampen zeigt (GLM 2019 nicht). Helen Suzman Boulevard: Überführung bis 24,5 m; Nelson Mandela
   Boulevard: 8 m über dem Foreshore, steigt bis 21 m. `clean.py` (wie London): übrige kurze Stufen geschätzt.
5. `orte.py`: Stadtteil aus OSM (place=suburb, Fläche, sonst nächster Punkt bis 2 km). `build.py` (Stadtteile unter 400 m dem
   Vorgänger zugeschlagen), `route.py` (lat0/lon0 −34,0/18,3), `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py kapstadt`,
   `work/app.py` (aus `boston/index.html`), `tiles_rand.py kapstadt 2`.

## Ergebnis

↑ 213 m / ↓ 211 m mit 200-m-Fenster (Veranstalter: 215 / 209 m), ↑ 241 / ↓ 240 m mit 50 m, Rohdaten ↑ 282 m. Start 8,6 m,
höchster Punkt 36,2 m (Gardens, Orange Street, km 31,5), tiefster 4,0 m (Foreshore, km 28), Ziel 10,3 m. Steilste Stellen über
200 m: +4,2 % auf dem Nelson Mandela Boulevard (km 6,3), −6,6 % die Searle Street hinunter (km 6,7). Mit 4:00/km im Flachen
ergibt das Modell 2:50:52 (Profil kostet 2:06 min).

## Offen

- Prüfung am iPhone.
- Strecke 2027 prüfen, sobald der Veranstalter sie zeigt; Getränkestellen genauer, falls es eine Karte mit Koordinaten gibt.
