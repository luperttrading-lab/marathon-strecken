# Übergabe: Steigungsprofil Köln-Marathon

Stand 27.10.2026, App-Version **1.44** (1.44: Feld `D.lage` für hoch gelegene Strecken: Tabelle „Ohne Höhenmeter“ nennt dann die Höhe; 1.43: unter der Zielzeit Pace auf flachen Stücken und im Schnitt; 1.42: Pace im Flachen mit zwei Nachkommastellen; 1.41: weißer Punkt im Pace-Diagramm ist der Flachpunkt 0 % mit Flach-Pace statt der aktuellen Stelle; 1.40: Markierung im Pace-Diagramm stufenlos und ohne Wackeln, Tippen daneben nimmt sie weg, Punkt „hier“ mit km; 1.39: Markierung im Pace-Diagramm auch waagerecht zur Pace-Achse; 1.38: Pace-Diagramm ohne Laborlinie und graue Zone, −15 bis +10 %, Achse bei 0 %, Markierung zum Antippen; 1.37: Bergab fest „halb“ ohne Schalter, steiler als −8 % kein weiterer Gewinn statt U-Kurve; 1.36: flacher Halbmarathon in der Tabelle ohne Höhenmeter, Erklärung im Info-Fenster (i); 1.35: Kosten je Höhenmeter bei 4:00 /km mit wählbarer Bezugs-Pace, Bahnzeiten als Tabelle, größere Überschriften in den Einstellungen; 1.34: unter der Zielzeit flacher Marathon und Bahnzeiten 10 000 m / 5000 m; 1.33: Zeiten immer mit 100 m, „Pace hier“ über das Messfenster gemittelt; 1.32: Messfenster 50 / 100 / 200 m / 1 km statt 10 m, neuer Erklärtext; 1.31: Zwischenzeiten mit Halbmarathon-Zeile und „je 10 km“; 1.30: Knopfrahmen so hell wie die Räder, „Vollbild“ blau, im Vollbild führt ‹ zurück in die normale Ansicht; 1.29: Kopf eines offenen Abschnitts bleibt oben stehen, Zuklappen von überall; 1.28: beim Aufklappen bleibt der Kopf des Abschnitts an seiner Stelle; 1.27: Hinweis, wenn die eingestellte Startzeit zu keiner Welle passt; 1.26: Standard 5 km Ausschnitt und Tempo ×200, Menü-Knopf blau mit Beschriftung, Abschnitte unter dem Läuferblick aufklappbar; 1.25: Startwellen mit Uhrzeiten unter „Deine Startzeit“; 1.24: Pfeile in Bisher/Noch/Ganze Strecke und Rampe als Grafik, dreistellige Werte ohne „…“, zu breite Werte werden kleiner; 1.23: Bergab U-Kurve statt Grenze bei −4 %: am schnellsten bei −8 %, ab −16 % langsamer als flach, ohne Knick bei 0 %; 1.22: Tempo-Rad mit ×1 (Echtzeit), ×50 und ×100–×180 in 20er-Schritten; 1.21: Brücken-Beschriftungen überlappen nicht mehr; 1.20: Kästchen bunt/grau neben der Gesamtstrecke, Diagramm „So rechnet das Pace-Modell“; 1.19: Ortsname bei Uhrzeiten aus `D.ort`, für Boston, sonst unverändert; 1.18: Seite springt beim Drehen an Zielzeit und Startzeit nicht mehr; 1.17: Höhenangaben mit dunklem Schein statt Kasten; 1.16: Höhenangaben auf Schildern lesbar, Straßennamen in eigener Zeile unter der km-Skala; 1.15: Gesamtstrecke unten mit feiner weißer Linie und Schalter farbig/einfarbig, die drei hellsten Bergab-Blau weniger türkis; 1.14: Farben fest (bergauf Rot bis Aubergine, bergab Blau), Dreieck unter der Skala, nur noch dunkel; 1.13: geschätzte Brücken schraffiert statt abgedunkelt; 1.12: Steigungszahl ohne Farbe; 1.11: Steigungszahl immer lesbar; 1.10: Schalter Blautöne bergab auto/tief/leicht; 1.9: Blauverlauf bergab dunkler beginnend, Ende Marineblau; 1.8: nur flach grün, bergab sieben Blautöne; 1.7: Zeiger als Dreieck über der Skala, Varianten 1–4 mit Grün und Blauverlauf bergab; 1.6: Farbvarianten A, 1–4 und Schalter für flach; 1.5: Farbwahl auch im Vollbild; 1.4: Farbvarianten A–E zum Testen unter der Legende; 1.3: Text über den Zwischenzeiten nennt auch die Kosten steiler Anstiege; 1.2: Höhenachse in gröberen Schritten bei großem Höhenbereich, hier ohne Wirkung; 1.1: Deutzer Brücke gemessen statt gerade), live unter https://luperttrading-lab.github.io/marathon-strecken/koeln/.

Die App ist eine Kopie der Hamburg-App (Stand 1.22) mit eigenen Daten, Texten und Speicherschlüsseln (`kln-…`), ohne eigenes
Manifest und Symbol (eine App für alle Strecken). Alle Entscheidungen zur Bedienung und zum Aussehen stehen in
[`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md) und gelten hier genauso. Änderungen am gemeinsamen Code in allen Apps
nachziehen (siehe README im Hauptordner).

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

1. `../dl/KM-2024.gpx`: GPX des Veranstalters von generali-koeln-marathon.de/strecken (Datei heißt 2024, Inhalt „KM 2023.08.14“).
   Dieselbe Linie (801 Punkte) steckt in seiner Google-Karte (`google.com/maps/d/kml?mid=1VSRHbQWK-fTfmrgj4nCoMigRHnXCblY`),
   die auf der Seite für 2026 eingebunden ist; der Faltplan 2026 zeigt dieselbe Führung. Länge 42,117 km, also 0,2 % zu kurz.
   **Kilometerpunkte gibt es nicht**: `proj.py` setzt nur Start und Ziel, `common.py` streckt gleichmäßig (bis ~80 m Versatz).
   Start 10:30 am Ottoplatz in Deutz, Ziel Komödienstraße am Dom. 11 Verpflegungsstellen und die Staffelwechsel stehen nur im
   Faltplan (`../dl/faltplan.pdf`), ohne Koordinaten: keine Marken außer Halbmarathon, Staffel-Einstellung ausgeblendet.
2. `parse.py` → `gpx2026.json`, `proj.py` → `kmproj.json`, `common.py` wie Frankfurt.
3. `dgm.py`: **DGM1 NRW** über WCS (`www.wcs.nrw.de/geobasis/wcs_nw_dgm`, Coverage `nw_dgm`, EPSG:25832, Achsen `x`/`y`),
   GeoTIFF-Ausschnitte je ~250 m, 32 s. Lizenz dl-de/zero-2-0.
4. `streets.py` (Nominatim alle 150 m; 48 Lücken durch HTTP 429 von Hand mit zoom 18 nachgeholt, eine bleibt),
   `dom.py` → `dom_deutz.json`: **Deutzer Brücke aus dem Oberflächenmodell DOM1 NRW** (WCS `wcs_nw_dom`, Coverage `nw_dom`,
   gleiche Achsen und Lizenz wie das DGM), km 0,50–1,10, je Punkt 25-%-Quantil der 5 × 5 m (darunter nur Rhein am Rand,
   darüber Fahrzeuge, Leuchten, Oberleitung). An Land stimmen DOM und DGM auf 0,1 m überein.
   `clean.py` (wie Berlin; setzt die DOM-Werte vor der Brückensuche ein, die Deutzer Brücke ist damit gemessen und nicht
   gestrichelt; bis 1.0 war sie von Hand eine Gerade 49,7 → 51,2 m, die Fahrbahn steigt aber bis 56,8 m), `build.py`, `route.py` (lat0/lon0 50,8/6,8), `tiles.py`,
   dann aus `werkzeuge/`: `tiles_z11.py koeln`, `work/app.py`, `tiles_rand.py koeln`.
5. `app.py`: hat aus `hamburg/index.html` die Erstausgabe von `koeln/` gebaut. **Nur historisch.**

## Ergebnis

↑ 83 m / ↓ 76 m mit 200-m-Fenster, ↑ 105 m mit 50-m-Fenster, Rohdaten ↑ 183 m. Start 45,5 m, Ziel 53,2 m; tiefster Punkt
42,3 m (Amsterdamer Straße, Riehl, km 36,4), höchster 56,7 m (Mitte der Deutzer Brücke, km 0,82). Steilste 200 m:
+2,9 % Auffahrt Deutzer Brücke (km 0,62), −2,8 % Abfahrt zum Heumarkt (km 1,01); +2,6 % Pipinstraße (km 13,7).
Geschätzt (gestrichelt): Brücken Bayenstraße, An Zint Jan, Universitätsstraße, Erftstraße, B 55a, Ebertplatz;
Unterführung Hansaring. Bei 4:00 /km im Flachen: 2:49:35, das Profil kostet 48 s.

## Offen

- Termin 2027: 3. Oktober laut Eventdatenbank, vom Veranstalter noch nicht bestätigt (`D.termine` mit „?“).
- Verpflegungsstellen und Staffelwechsel, falls der Veranstalter Koordinaten veröffentlicht.
- Prüfung am iPhone.
- Die übrigen kurzen Brücken ließen sich genauso aus dem DOM messen; bei 20–90 m Länge ändert das wenig.
