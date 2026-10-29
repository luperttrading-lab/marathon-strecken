# Übergabe: Steigungsprofil Boston-Marathon

Stand 28.10.2026, App-Version **1.17** (1.17: flacher Halbmarathon in der Tabelle ohne Höhenmeter, Erklärung im Info-Fenster (i); 1.16: Kosten je Höhenmeter bei 4:00 /km mit wählbarer Bezugs-Pace, Bahnzeiten als Tabelle, größere Überschriften in den Einstellungen; 1.15: unter der Zielzeit flacher Marathon und Bahnzeiten 10 000 m / 5000 m; 1.14: Zeiten immer mit 100 m, „Pace hier“ über das Messfenster gemittelt; 1.13: Messfenster 50 / 100 / 200 m / 1 km statt 10 m, neuer Erklärtext; 1.12: Zwischenzeiten mit Halbmarathon-Zeile und „je 10 km“; 1.11: Knopfrahmen so hell wie die Räder, „Vollbild“ blau, im Vollbild führt ‹ zurück in die normale Ansicht; 1.10: Kopf eines offenen Abschnitts bleibt oben stehen, Zuklappen von überall; 1.9: beim Aufklappen bleibt der Kopf des Abschnitts an seiner Stelle; 1.8: Hinweis, wenn die eingestellte Startzeit zu keiner Welle passt; 1.7: Standard 5 km Ausschnitt und Tempo ×200, Menü-Knopf blau mit Beschriftung, Abschnitte unter dem Läuferblick aufklappbar; 1.6: Startwellen mit Uhrzeiten unter „Deine Startzeit“; 1.5: Pfeile in Bisher/Noch/Ganze Strecke und Rampe als Grafik, dreistellige Werte ohne „…“, zu breite Werte werden kleiner; 1.4: Bergab U-Kurve statt Grenze bei −4 %: am schnellsten bei −8 %, ab −16 % langsamer als flach, ohne Knick bei 0 %; 1.3: Tempo-Rad mit ×1 (Echtzeit), ×50 und ×100–×180 in 20er-Schritten; 1.2: Brücken-Beschriftungen überlappen nicht mehr; 1.1: Kästchen bunt/grau neben der Gesamtstrecke, Diagramm „So rechnet das Pace-Modell“; 1.0: Erstausgabe), live unter https://luperttrading-lab.github.io/marathon-strecken/boston/.

Die App ist eine Kopie der New-York-App (Stand 1.26) mit eigenen Daten, Texten und Speicherschlüsseln (`bos-…`), ohne
eigenes Manifest und Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in
[`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Änderungen am gemeinsamen Code in allen Apps nachziehen (README).
`D.ort` / `D.ortKurz` („Boston“): Boston liegt in derselben Zeitzone wie New York, der Ortsname bei den Uhrzeiten kommt
deshalb aus den Daten (gemeinsamer Code seit Hamburg 1.40).

131. Boston Marathon am Montag, 19. April 2027 (Patriots' Day, laut B.A.A.). Start der ersten Welle 10:00 Uhr Ortszeit
(2026: Wellen 10:00 bis 11:21, Rollstühle ab 9:02), `D.start` = 600. Punkt-zu-Punkt von der Main Street in Hopkinton über
Ashland, Framingham, Natick, Wellesley, Newton und Brookline zur Boylston Street in Boston.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

1. **Strecke:** Die B.A.A. bietet keine Linie zum Herunterladen an. Quelle ist die OSM-Relation „Boston Marathon“
   (11680552, route=running, Rollen start/end an Start- und Ziellinie) über den Overpass-Spiegel maps.mail.ru
   (`../dl/relation.json`, `../dl/wege.json` mit Brücken-Tags). `parse.py`: die Wege sind nicht geordnet, ein Graph aus allen
   Wegpunkten, kürzester Weg vom Start- zum Zielknoten → `gpx2026.json`, 2135 Punkte, 42,417 km (Haversine), also 0,5 % zu
   lang (Straßenmitte statt Ideallinie). Meilenpunkte mit Lage gibt es nicht; `common.py` staucht gleichmäßig auf 42 195 m.
2. **Getränkestellen** aus dem Streckenheft der B.A.A. 2026 (`../dl/pdf/race-course-2026.pdf`, Spalte „Hydration Stations“):
   Meile 2,1 · 3,1 · 4,4 · 5,2 · 6,01 · 7,1 · 8,01 · 8,9 · 10,1 · 11,2 · 12,1 · 13,3 · 14,1 · 15,01 · 16,01 · 17,1 · 18,1 · 19,1 ·
   20,1 · 21,1 · 22,01 · 23,1 · 24,1 · 25,1; Maurten-Gel zusätzlich bei 12,1, 17,1 und 22,01 (in `build.py`, Art „food“).
3. `dgm.py`: **USGS 3DEP**, 1-m-Laser-Geländemodell (NAVD88), ImageServer `getSamples`, je 100 Punkte, alle 10 m.
4. **Brücken** aus der USGS-Punktwolke `MA_CentralEastern_1_2021` (EPT auf AWS, `ept.py`): `deck.py` misst in Fenstern um
   die OSM-Brücken je Punkt das 10-%-Quantil der Laserpunkte im Umkreis von 4 m, die mehr als 1 m über dem Gelände liegen
   (`deck.json`, `deck.log`). `lidar.py` setzt die Fahrbahn nur auf den in `ZONEN` genannten Spannen ein, wo mindestens 100
   Punkte sie tragen: Union Street über den Sudbury River (zweimal, km 6,3 und 6,6), Washington Street über die Route 9
   (km 23,8), über den Charles River (25,55), über die I-95 / Route 128 (26,2), über die Green Line D (27,05), Beacon Street
   über Mass Pike und Bahn (40,13–40,27), Commonwealth Avenue über den Muddy River (40,94). Nicht automatisch: unter der
   Bowker-Überführung (Charlesgate, km 40,9) und unter den Bäumen am Commonwealth Avenue lägen die Punkte über der Strecke.
   `clean.py` (wie New York) findet danach keine Stufe mehr: nichts ist geschätzt.
   Die Unterführung unter der Massachusetts Avenue (km 41,2, tiefster Punkt −0,3 m) ist echt und bleibt.
5. `streets.py` (Nominatim alle 150 m; Ort = Stadt bzw. Gemeinde, in Boston der Stadtteil), `build.py` (neuer Abschnitt
   auch beim Ortswechsel), `route.py` (lat0/lon0 42,2/−71,6), `tiles.py` (z14 nur entlang der Strecke), dann aus
   `werkzeuge/`: `tiles_z11.py boston`, `work/app.py` (aus `newyork/index.html`), `tiles_rand.py boston 2`.

## Ergebnis und Abgleich

↑ 238 m / ↓ 377 m mit 200-m-Fenster, ↑ 296 / ↓ 435 m mit 50 m, Rohdaten ↑ 310 m. Start 142,8 m, Ziel 3,4 m:
139,5 m Gefälle, üblich genannt werden 459 ft (140 m). Die Meilentabelle von boston.com (Höhen in ft, auf 5 ft gerundet,
ältere Vermessung) weicht je Meile im Mittel um 3,0 m ab (Median 2,1 m), höchstens 8,8 m (Meile 24 im Gefälle nach
Brookline: 100 m Versatz längs der Strecke machen dort mehrere Meter aus).
Newton Hills: km 25,7–26,6 über die Route 128 (+20 m), 28,1–28,75 nach dem Feuerwehrhaus (+20,5 m), 30,8–31,3 (+15 m),
Heartbreak Hill 32,5–33,3 (+28 m auf 870 m, Ø 3,2 %, max. 5,1 % über 200 m). Steilste Stelle: −6,9 % über 200 m am
Start (km 0,4). Mit 4:00/km im Flachen ergibt das Modell 2:50:09; das Profil kostet 1:22 min, weil der Bergab-Gewinn
nur halb und nur bis −4 % angerechnet wird.

## Offen

- Prüfung am iPhone.
- Kilometer sind gleichmäßig geeicht: örtlich können sie bis etwa 100 m von den offiziellen Meilen abweichen. Bessere
  Quelle wären die Meilenmarken mit Lage (B.A.A.-App oder Vermessungsprotokoll MA…JK von certifiedroadraces.com).
