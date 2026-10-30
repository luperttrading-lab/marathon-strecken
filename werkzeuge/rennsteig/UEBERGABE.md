# Übergabe: Steigungsprofil Rennsteiglauf-Marathon

Stand 30.10.2026, App-Version **1.46** (1.46: Mauer je Durchgang ein Rad mit Empfehlung nach Zielzeit, nur bei `D.mauer`; 1.45: Mauer-Zeit und Tor-Rechner für Strecken mit `D.mauer`, sonst unverändert; 1.44: Steigungskosten als große Zeile unter der Zielzeit; 1.43: Umschalter Höhe/Meereshöhe für die Tabelle „Ohne Höhenmeter“, nur bei `D.lage`; 1.42: Feld `D.lage` für hoch gelegene Strecken: Tabelle „Ohne Höhenmeter“ nennt dann die Höhe; 1.41: unter der Zielzeit Pace auf flachen Stücken und im Schnitt; 1.40: Pace im Flachen mit zwei Nachkommastellen; 1.39: weißer Punkt im Pace-Diagramm ist der Flachpunkt 0 % mit Flach-Pace statt der aktuellen Stelle; 1.38: Markierung im Pace-Diagramm stufenlos und ohne Wackeln, Tippen daneben nimmt sie weg, Punkt „hier“ mit km; 1.37: Markierung im Pace-Diagramm auch waagerecht zur Pace-Achse; 1.36: Pace-Diagramm ohne Laborlinie und graue Zone, −15 bis +10 %, Achse bei 0 %, Markierung zum Antippen; 1.35: Bergab fest „halb“ ohne Schalter, steiler als −8 % kein weiterer Gewinn statt U-Kurve; 1.34: flacher Halbmarathon in der Tabelle ohne Höhenmeter, Erklärung im Info-Fenster (i); 1.33: Kosten je Höhenmeter bei 4:00 /km mit wählbarer Bezugs-Pace, Bahnzeiten als Tabelle, größere Überschriften in den Einstellungen; 1.32: unter der Zielzeit flacher Marathon und Bahnzeiten 10 000 m / 5000 m; 1.31: Zeiten immer mit 100 m, „Pace hier“ über das Messfenster gemittelt; 1.30: Messfenster 50 / 100 / 200 m / 1 km statt 10 m, neuer Erklärtext; 1.29: Zwischenzeiten mit Halbmarathon-Zeile und „je 10 km“; 1.28: Knopfrahmen so hell wie die Räder, „Vollbild“ blau, im Vollbild führt ‹ zurück in die normale Ansicht; 1.27: Kopf eines offenen Abschnitts bleibt oben stehen, Zuklappen von überall; 1.26: beim Aufklappen bleibt der Kopf des Abschnitts an seiner Stelle; 1.25: Hinweis, wenn die eingestellte Startzeit zu keiner Welle passt; 1.24: Standard 5 km Ausschnitt und Tempo ×200, Menü-Knopf blau mit Beschriftung, Abschnitte unter dem Läuferblick aufklappbar; 1.23: Hinweis: ein gemeinsamer Start unter „Deine Startzeit“; 1.22: Pfeile in Bisher/Noch/Ganze Strecke und Rampe als Grafik, dreistellige Werte ohne „…“, zu breite Werte werden kleiner; 1.21: Bergab U-Kurve statt Grenze bei −4 %: am schnellsten bei −8 %, ab −16 % langsamer als flach, ohne Knick bei 0 %; 1.20: Tempo-Rad mit ×1 (Echtzeit), ×50 und ×100–×180 in 20er-Schritten; 1.19: Brücken-Beschriftungen überlappen nicht mehr; 1.18: Kästchen bunt/grau neben der Gesamtstrecke, Diagramm „So rechnet das Pace-Modell“; 1.17: Ortsname bei Uhrzeiten aus `D.ort`, für Boston, sonst unverändert; 1.16: Seite springt beim Drehen an Zielzeit und Startzeit nicht mehr; 1.15: Höhenangaben mit dunklem Schein statt Kasten; 1.14: Höhenangaben auf Schildern lesbar, Straßennamen in eigener Zeile unter der km-Skala; 1.13: Gesamtstrecke unten mit feiner weißer Linie und Schalter farbig/einfarbig, die drei hellsten Bergab-Blau weniger türkis; 1.12: Farben fest (bergauf Rot bis Aubergine, bergab Blau), Dreieck unter der Skala, nur noch dunkel; 1.11: geschätzte Brücken schraffiert statt abgedunkelt; 1.10: Steigungszahl ohne Farbe; 1.9: Steigungszahl immer lesbar; 1.8: Schalter Blautöne bergab auto/tief/leicht; 1.7: Blauverlauf bergab dunkler beginnend, Ende Marineblau; 1.6: nur flach grün, bergab sieben Blautöne; 1.5: Zeiger als Dreieck über der Skala, Varianten 1–4 mit Grün und Blauverlauf bergab; 1.4: Farbvarianten A, 1–4 und Schalter für flach; 1.3: Farbwahl auch im Vollbild; 1.2: Farbvarianten A–E zum Testen unter der Legende; 1.1: Text über den Zwischenzeiten nennt auch die Kosten steiler Anstiege; Untertitel nennt das 20-m-Raster), live unter https://luperttrading-lab.github.io/marathon-strecken/rennsteig/.

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
