# Übergabe: Steigungsprofil Köln-Marathon

Stand 27.10.2026, App-Version **1.3** (1.3: Text über den Zwischenzeiten nennt auch die Kosten steiler Anstiege; 1.2: Höhenachse in gröberen Schritten bei großem Höhenbereich, hier ohne Wirkung; 1.1: Deutzer Brücke gemessen statt gerade), live unter https://luperttrading-lab.github.io/marathon-strecken/koeln/.

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
