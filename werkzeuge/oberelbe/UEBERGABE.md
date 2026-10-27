# Übergabe: Steigungsprofil Oberelbe-Marathon

Stand 27.10.2026, App-Version **1.5** (1.5: Farbvarianten A, 1–4 und Schalter für flach; 1.4: Farbwahl auch im Vollbild; 1.3: Farbvarianten A–E zum Testen unter der Legende; 1.2: Text über den Zwischenzeiten nennt auch die Kosten steiler Anstiege; 1.1: Höhenachse in gröberen Schritten bei großem Höhenbereich, hier ohne Wirkung), live unter https://luperttrading-lab.github.io/marathon-strecken/oberelbe/.

Die App ist eine Kopie der Hamburg-App (Stand 1.22) mit eigenen Daten, Texten und Speicherschlüsseln (`oem-…`), ohne eigenes
Manifest und Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in
[`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Änderungen am gemeinsamen Code in allen Apps nachziehen (README).

VVO Oberelbe-Marathon, Punkt-zu-Punkt-Strecke: Start 9:20 Uhr auf der Elbwiese in Königstein, auf dem linken Elbufer über
Pirna und Heidenau (vorbei an Schloss Pillnitz und dem Blauen Wunder auf der anderen Seite) ins Heinz-Steyer-Stadion in
Dresden. 2026 am 26. April, 2027 laut Laufkalendern am 25. April (vom Veranstalter noch nicht bestätigt, `D.termine` mit „?“).

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

1. `../dl/strecke2026.gpx`: GPX des Veranstalters (oberelbe-marathon.de/deine-strecke/marathon, mit komoot erstellt,
   806 Punkte, 42,206 km). Keine Kilometerpunkte: `proj.py` nur Start/Ziel, `common.py` streckt gleichmäßig (−0,03 %).
2. `dgm.py`: **DGM1 Sachsen** (GeoSN, CC BY 4.0) als 2-km-Kacheln (ZIP mit GeoTIFF, ETRS89/UTM33) aus der GeoCloud:
   `geocloud.landesvermessung.sachsen.de/public.php/dav/files/JCcXyifaNdLDnxZ/dgm1_33<E km gerade>_<N km gerade>_2_sn_tiff.zip`
   (Muster aus dem „Batch Download“ auf geodaten.sachsen.de). 25 Kacheln à 13 MB, werden nur gelesen, nicht gespeichert.
   Messpunkte auf OSM-Wege gelegt (`../dl/osm_wege.json`, Overpass-Spiegel maps.mail.ru); die GPX liegt schon gut
   (im Mittel 0,7 m Versatz).
3. `streets.py`, `clean.py` (wie Berlin/Köln, ohne Handkorrektur), `build.py`, `route.py` (lat0/lon0 50,8/13,6),
   `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py oberelbe`, `work/app.py`, `tiles_rand.py oberelbe`. Die Strecke ist
   lang und schmal: 110 Kartenstücke, App 12 MB.

## Ergebnis

↑ 114 m / ↓ 123 m mit 200-m-Fenster, Rohdaten ↑ 232 m. Start 118,5 m, Ziel 108,9 m; tiefster Punkt 107,3 m (Dresden,
km 40,9), höchster 140,7 m (Rathener Weg bei Pötzscha, km 7,8). Steilste 200 m: +7,5 % Pötzschaer Weg (km 6,7). Die
Wellen zwischen Kurort Rathen und Wehlen (km 6–10) zeigt auch das Höhenprofil des Veranstalters. Bei 4:00 /km im
Flachen: 2:49:47, das Profil kostet 1:01 min.

## Offen

- Termin 2027 bestätigen; Verpflegungsstellen (nur im Text: große Verpflegung Dresden-Zschieren km 26, Fährgarten Johannstadt).
- Prüfung am iPhone.
