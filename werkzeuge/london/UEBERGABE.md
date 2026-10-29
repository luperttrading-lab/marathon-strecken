# Übergabe: Steigungsprofil London-Marathon

Stand 28.10.2026, App-Version **1.11** (1.11: Knopfrahmen so hell wie die Räder, „Vollbild“ blau, im Vollbild führt ‹ zurück in die normale Ansicht; 1.10: Kopf eines offenen Abschnitts bleibt oben stehen, Zuklappen von überall; 1.9: beim Aufklappen bleibt der Kopf des Abschnitts an seiner Stelle; 1.8: Hinweis, wenn die eingestellte Startzeit zu keiner Welle passt; 1.7: Standard 5 km Ausschnitt und Tempo ×200, Menü-Knopf blau mit Beschriftung, Abschnitte unter dem Läuferblick aufklappbar; 1.6: Hinweis zu den Wellen (Zeiten nur per E-Mail) unter „Deine Startzeit“; 1.5: Pfeile in Bisher/Noch/Ganze Strecke und Rampe als Grafik, dreistellige Werte ohne „…“, zu breite Werte werden kleiner; 1.4: Bergab U-Kurve statt Grenze bei −4 %: am schnellsten bei −8 %, ab −16 % langsamer als flach, ohne Knick bei 0 %; 1.3: Tempo-Rad mit ×1 (Echtzeit), ×50 und ×100–×180 in 20er-Schritten; 1.2: Brücken-Beschriftungen überlappen nicht mehr; 1.1: Kästchen bunt/grau neben der Gesamtstrecke, Diagramm „So rechnet das Pace-Modell“; 1.0: Erstausgabe), live unter https://luperttrading-lab.github.io/marathon-strecken/london/.

Die App ist eine Kopie der Boston-App (Stand 1.0) mit eigenen Daten, Texten und Speicherschlüsseln (`ldn-…`), ohne eigenes
Manifest und Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in
[`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Änderungen am gemeinsamen Code in allen Apps nachziehen (README).

TCS London Marathon 2027 einmalig als „The Double“ an zwei Tagen: Samstag 24. und Sonntag 25. April 2027
(`D.termine` beide). Start der Masse 2026 um 9:35 Uhr (London Marathon Events), `D.start` = 575; für 2027 noch nicht
veröffentlicht. `D.tz` Europe/London, `D.ortKurz` „ London“. Strecke vom **Blue Start** (Shooters Hill Road, Blackheath).

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

1. **Strecke:** OSM-Relation „London Marathon (Blue Start)“ (13319641, route=running; `../dl/rel_13319641.json`, die Red-Start-
   Relation 2086183 liegt daneben). `parse.py`: Die Wege stehen fast in Laufrichtung, in Limehouse aber als Block an falscher
   Stelle (Narrow Street, Hinweg, Wege 702–728 hinter der Runde über die Isle of Dogs); Reihenfolge 0–493, 702–728, 494–701,
   729–Ende. Auf der Rückfahrt über The Highway fehlen Wege; Lücken über den kürzesten Weg im OSM-Straßennetz
   (`../dl/osm_wege.json`). Danach kurze Hin-und-zurück-Schleifen (unter 600 m, zurück zum selben Knoten) entfernt.
   Linie 42,950 km, 1,8 % länger als vermessen; `common.py` staucht gleichmäßig auf 42 195 m (Meilenmarken mit Lage gibt es nicht).
   The Highway zwischen Butcher Row und Tower wird in beiden Richtungen belaufen (Hinweg Meile 13, Rückweg Meile 22).
2. **Verpflegung** (`build.py`): Lucozade Sport an Meile 7, 15, 21, 23 und Gels an Meile 14 und 19 (London Marathon Events);
   Wasser laut Läuferguide 2026 an Meile 3, 6, 9, 12 und alle zwei Meilen bis 24 (nicht amtlich bestätigt).
3. `dgm.py`: **Environment Agency LIDAR Composite DTM 1 m** (Höhen über ODN, Open Government Licence) über den WCS-Dienst
   `environment.data.gov.uk/spatialdata/lidar-composite-digital-terrain-model-dtm-1m/wcs` (CoverageId in `dgm.py`), je 300 m
   ein Ausschnitt in EPSG:27700, bilinear. `dgm.py dsm` dasselbe aus dem **LZ-DSM** (last return) → `dsm2026_10m.json`.
4. `lidar.py`: Auf den Brücken (`ZONEN`) gilt das DSM, verworfen werden Werte unter dem Gelände oder über 5 m über den Enden
   (Türme und Stege der Tower Bridge). Tower Bridge 19,79–20,19: Fahrbahn 9,6 → 14,0 → 10,2 m. Nicht als Brücke: Trafalgar
   Way (darüber die DLR), Westferry Circus (Tunnel darunter), Upper Thames Street (Tunnel, Durchfahrten).
   `clean.py` (wie New York): übrige Stufen, darunter der Tunnel der Westferry Road unter dem Westferry Circus (km 23,95–24,23,
   in `build.py` als „Tunnel“) und kurze Brücken in Rotherhithe und Canary Wharf (geschätzt, gestrichelt).
5. `streets.py` (Nominatim alle 150 m, Ort = suburb), `build.py` (Orte unter 300 m dem Vorgänger zugeschlagen), `route.py`
   (lat0/lon0 51,45/−0,2), `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py london`, `work/app.py` (aus `boston/index.html`),
   `tiles_rand.py london 2`.

## Ergebnis

↑ 114 m / ↓ 147 m mit 200-m-Fenster, ↑ 162 / ↓ 195 m mit 50 m. Start 39,7 m, höchster Punkt 52,4 m (km 2,4), tiefster 0,9 m
(Isle of Dogs, km 26), Ziel 6,7 m. Steilste Stelle: −4,9 % über 200 m, Abfahrt nach Woolwich (km 5,0). Mit 4:00/km im Flachen
ergibt das Modell 2:49:34.

## Offen

- Prüfung am iPhone.
- Wasserstellen amtlich bestätigen (Course map 2027), ebenso die Startzeit 2027.
- Red und Green Start: andere erste 5 km; bei Bedarf als Schalter oder eigene Linie.
