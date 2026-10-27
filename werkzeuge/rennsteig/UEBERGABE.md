# Übergabe: Steigungsprofil Rennsteiglauf-Marathon

Stand 27.10.2026, App-Version **1.5** (1.5: Zeiger als Dreieck über der Skala, Varianten 1–4 mit Grün und Blauverlauf bergab; 1.4: Farbvarianten A, 1–4 und Schalter für flach; 1.3: Farbwahl auch im Vollbild; 1.2: Farbvarianten A–E zum Testen unter der Legende; 1.1: Text über den Zwischenzeiten nennt auch die Kosten steiler Anstiege; Untertitel nennt das 20-m-Raster), live unter https://luperttrading-lab.github.io/marathon-strecken/rennsteig/.

Die App ist eine Kopie der Hamburg-App (Stand 1.23) mit eigenen Daten, Texten und Speicherschlüsseln (`rsl-…`), ohne eigenes
Manifest und Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in
[`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Änderungen am gemeinsamen Code in allen Apps nachziehen (README).

Marathon beim GutsMuths-Rennsteiglauf, Punkt-zu-Punkt-Strecke fast ganz auf Forstwegen am Rennsteig: Start 9:00 Uhr am
Sportplatz an der Guts-Muths-Turnhalle in Neuhaus am Rennweg, über Steinheid, Friedrichshöhe, Masserberg, Neustadt am
Rennsteig und Frauenwald zum Sportplatz in Schmiedefeld am Rennsteig (711 m). 54. Lauf am 22. Mai 2027 (rennsteiglauf.de).
Verpflegung laut Veranstalter (`VP_Marathon.pdf`): Steinheider Hütte 5,8 (Getränke), Parkplatz Friedrichshöhe 12,0,
Turmbaude Masserberg 18,3, Schwalbenhauptwiese 22,2 (Getränke), Neustadt 28,3, Großer Dreiherrenstein 33,4 (Cut-off
16:30 Uhr), Frauenwald 37,1. Die Kilometer sind auf seine 42,2 km bezogen und in `build.py` auf 42,195 km umgerechnet.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

1. **Strecke:** Es gibt keine GPX zum Herunterladen. Die Seite des Veranstalters verlinkt die Outdooractive-Tour
   „Rennsteiglauf INTERSPORT Marathon v2“ (outdooractive.com/…/315838141); deren Linie steht im JSON-LD der Seite
   (GeoShape `line`, Reihenfolge „lat lon“) → `../dl/outdooractive_linie.json`: 416 Punkte, 42,5 km, im Mittel alle
   86 m, Lücken bis 570 m.
2. `osm.py`: OSM-Wege entlang der Linie über den Overpass-Spiegel maps.mail.ru (andere Spiegel und Geofabrik sind in der
   Cloud-Umgebung gesperrt). Der Spiegel antwortet meist mit 504: Stücke von ~700 m, viele Wiederholungen, fertige Stücke
   in `../dl/osm_teile/`; mit Argument `rueckwaerts` läuft ein zweiter Durchgang von hinten. Dauer ~40 min.
3. `match.py` → `gpx2026.json`: Linie auf die OSM-Wege gelegt (kürzester Weg, Kante kostet Länge × (1 + (Abstand/20 m)²),
   Anker alle 500 m). Median 2,6 m neben der Linie, höchstens 32 m. Zwei Schleifen der Linie kürzt der Weg ab, dort
   gilt die Linie selbst: durch Schmiedefeld bei km 41,1 und die Runde um den Sportplatz vor dem Ziel. Mit ihnen treffen
   die Verpflegungsstellen die Kilometer des Veranstalters auf 0,1 km (ohne sie bis 0,3 km daneben). Länge 42,65 km,
   `common.py` staucht gleichmäßig um 1,1 % auf 42,195 km.
4. **Höhe:** Das amtliche DGM1 Thüringen war nicht abrufbar (geoportal-th.de: Wartungsseite; geoportal.thueringen.de:
   Captcha; api.hoehendaten.de, Port 14444: vom Netzfilter gesperrt). Ersatz: **Sonnys „DTM Germany 20m v3b“**
   (sonny.4lima.de, CC BY 4.0) aus den Thüringer Laserdaten (DGM1 2014–2019, DGM2 2010–2013), eine GeoTIFF für
   Deutschland auf Google Drive (1,5 GB, Deflate, je Zeile ein Streifen). Per Range-Abruf nur die 809 Zeilen um die
   Strecke → `../dl/dtm20_streifen.bin/.json` (41 MB). `dtm20.py` liest sie (UTM32, PixelIsPoint), `dgm.py` alle 10 m
   bilinear. Abgleich: Ziel 710,7 m (Veranstalter 711), Turmbaude 841,8 m (841).
   Grenze des 20-m-Rasters: Kuppen und Mulden unter ~40 m Länge fehlen, Steigungen ab 200 m stimmen.
5. `streets.py` (Ort = Dorf bzw. Gemeinde statt Stadtteil), `clean.py` (**ohne Brückensuche**: das 20-m-Raster hat an
   steilen Hängen Stufen bis 2,2 m auf 10 m, Brücken gibt es auf der Strecke nicht), `build.py` (unbenannte Waldwege →
   „Rennsteig“; der Ort springt am Rennsteig als alter Grenze oft zur Nachbargemeinde, Läufe unter 600 m übernehmen den
   Ort davor), `route.py` (lat0/lon0 50,5/10,8), `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py rennsteig`,
   `work/app.py`, `tiles_rand.py rennsteig`.

## Ergebnis

↑ 688 m / ↓ 764 m mit 200-m-Fenster, ↑ 744 / ↓ 820 m mit 50 m, Rohdaten ↑ 780 m (Veranstalter nach Outdooractive:
↑ 769 / ↓ 844 m). Start 786,5 m, Ziel 710,7 m; höchster Punkt 846,4 m bei Steinheid (km 4,0; der Veranstalter nennt
die Turmbaude, hier 841,8 m), tiefster 680 m in Schmiedefeld (km 41,1; Veranstalter 687 m an der Einmündung Reitallee),
danach 35 m hinauf ins Ziel. Steilste 200 m: +14,6 % hinter Neustadt von der Ochsenbacher Mühle hinauf (km 30,4),
−13 % hinunter zur Steinheider Hütte (km 5,6). Bei 4:00 /km im Flachen: 2:57:22, das Profil kostet 8:35 min.
Höhenbereich 180 m: Hilfslinien alle 25 m (seit Hamburg 1.23), Startseite mit eigener Grafikhöhe (`.spark.berg`, 240 px).

## Offen

- Amtliches DGM1 Thüringen nachladen, sobald erreichbar (z. B. `api.hoehendaten.de` in den Netzwerk-Einstellungen
  der Umgebung freigeben), dann `dgm.py` umstellen und die Schritte ab `clean.py` wiederholen.
- Zwischen km 22,4 und 25,7 springt die gelegte Linie zwischen der L 2052 und dem Pfad daneben; für die Höhe ohne Belang.
- Prüfung am iPhone.
