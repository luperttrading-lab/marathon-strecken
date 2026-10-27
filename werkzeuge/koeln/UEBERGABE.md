# Übergabe: Steigungsprofil Köln-Marathon

Stand 27.10.2026, App-Version **1.0**, live unter https://luperttrading-lab.github.io/marathon-strecken/koeln/.

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
   `clean.py` (wie Berlin; **Deutzer Brücke von Hand** km 0,54–1,06: das Modell fällt schon vor dem Widerlager zur Böschung
   am Rheinufer ab, sonst −6,8 % „Abfahrt“ vor der Brücke), `build.py`, `route.py` (lat0/lon0 50,8/6,8), `tiles.py`,
   dann aus `werkzeuge/`: `tiles_z11.py koeln`, `work/app.py`, `tiles_rand.py koeln`.
5. `app.py`: hat aus `hamburg/index.html` die Erstausgabe von `koeln/` gebaut. **Nur historisch.**

## Ergebnis

↑ 78 m / ↓ 70 m mit 200-m-Fenster, ↑ 100 m mit 50-m-Fenster, Rohdaten ↑ 189 m. Start 45,5 m, Ziel 53,2 m; tiefster Punkt
42,3 m (Amsterdamer Straße, Riehl, km 36,4), höchster 54,5 m (Hohe Straße kurz vor dem Ziel, km 41,9). Steilste 200 m:
+2,6 % Pipinstraße (km 13,7, vom Heumarkt zur Cäcilienstraße). Brücken: Deutzer Brücke (49,7 → 51,2 m, gerade),
Bayenstraße, An Zint Jan, Universitätsstraße, Erftstraße, B 55a, Ebertplatz; Unterführung Hansaring. Bei 4:00 /km im
Flachen: 2:49:32, das Profil kostet 45 s.

## Offen

- Termin 2027: 3. Oktober laut Eventdatenbank, vom Veranstalter noch nicht bestätigt (`D.termine` mit „?“).
- Verpflegungsstellen und Staffelwechsel, falls der Veranstalter Koordinaten veröffentlicht.
- Prüfung am iPhone.
