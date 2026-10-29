# Übergabe: Steigungsprofil Frankfurt-Marathon

Stand 27.10.2026, App-Version **1.47** (1.47 Kosten je Höhenmeter bei 4:00 /km mit wählbarer Bezugs-Pace, Bahnzeiten als Tabelle, größere Überschriften in den Einstellungen; 1.46 unter der Zielzeit flacher Marathon und Bahnzeiten 10 000 m / 5000 m; 1.45 Zeiten immer mit 100 m, „Pace hier“ über das Messfenster gemittelt; 1.44 Messfenster 50 / 100 / 200 m / 1 km statt 10 m, neuer Erklärtext; 1.43 Zwischenzeiten mit Halbmarathon-Zeile und „je 10 km“; 1.42 Knopfrahmen so hell wie die Räder, „Vollbild“ blau, im Vollbild führt ‹ zurück in die normale Ansicht; 1.41 Kopf eines offenen Abschnitts bleibt oben stehen, Zuklappen von überall; 1.40 beim Aufklappen bleibt der Kopf des Abschnitts an seiner Stelle; 1.39 Hinweis, wenn die eingestellte Startzeit zu keiner Welle passt; 1.38 Standard 5 km Ausschnitt und Tempo ×200, Menü-Knopf blau mit Beschriftung, Abschnitte unter dem Läuferblick aufklappbar; 1.37 Startwellen mit Uhrzeiten unter „Deine Startzeit“; 1.36 Pfeile in Bisher/Noch/Ganze Strecke und Rampe als Grafik, dreistellige Werte ohne „…“, zu breite Werte werden kleiner; 1.35 Bergab U-Kurve statt Grenze bei −4 %: am schnellsten bei −8 %, ab −16 % langsamer als flach, ohne Knick bei 0 %; 1.34 Tempo-Rad mit ×1 (Echtzeit), ×50 und ×100–×180 in 20er-Schritten; 1.33 Brücken-Beschriftungen überlappen nicht mehr; 1.32 Kästchen bunt/grau neben der Gesamtstrecke, Diagramm „So rechnet das Pace-Modell“; 1.31 Ortsname bei Uhrzeiten aus `D.ort`, für Boston, sonst unverändert; 1.30 Seite springt beim Drehen an Zielzeit und Startzeit nicht mehr; 1.29 Höhenangaben mit dunklem Schein statt Kasten; 1.28 Höhenangaben auf Schildern lesbar, Straßennamen in eigener Zeile unter der km-Skala; 1.27 Gesamtstrecke unten mit feiner weißer Linie und Schalter farbig/einfarbig, die drei hellsten Bergab-Blau weniger türkis; 1.26 Festhalle ebenerdig zum Vorplatz; 1.25 Farben fest (bergauf Rot bis Aubergine, bergab Blau), Dreieck unter der Skala, nur noch dunkel; 1.24 geschätzte Brücken schraffiert statt abgedunkelt; 1.23 Steigungszahl ohne Farbe; 1.22 Steigungszahl immer lesbar; 1.21 Schalter Blautöne bergab auto/tief/leicht; 1.20 Blauverlauf bergab dunkler beginnend, Ende Marineblau; 1.19 nur flach grün, bergab sieben Blautöne; 1.18 Zeiger als Dreieck über der Skala, Varianten 1–4 mit Grün und Blauverlauf bergab; 1.17 Farbvarianten A, 1–4 und Schalter für flach; 1.16 Farbwahl auch im Vollbild; 1.15 Farbvarianten A–E zum Testen unter der Legende; 1.14 Brücken über Main und Nidda gemessen statt gerade; 1.13 Text über den Zwischenzeiten nennt auch die Kosten steiler Anstiege; 1.12 Höhenachse in gröberen Schritten bei großem Höhenbereich, hier ohne Wirkung; seit 1.5 ohne eigenes Manifest und Symbol, siehe README; 1.6 Pace im Läuferblick; 1.7 Start bei km 0, Knopf zum Start; 1.8 Zuschauerplan und Pace-Band; 1.9 Uhrzeit im Läuferblick; 1.10 Ziffern ruhig; 1.11 Feld deckend), live unter https://luperttrading-lab.github.io/marathon-strecken/frankfurt/.

Die App ist eine Kopie der Hamburg-App (Stand 1.11) mit eigenen Daten, Texten und Speicherschlüsseln (`ffm-…`).
Alle Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md) und gelten
hier genauso. Änderungen am gemeinsamen Code in beiden Apps nachziehen (siehe README im Hauptordner).

## Daten (`work/`, aus `work/` heraus starten, Geschwisterordner `../dl` und `../assets` bleiben lokal)

1. `../dl/strecke.gpx`: offizielle GPX 2026 von frankfurt-marathon.com (Seite *Dein Lauf → Marathon → Strecke*), eine Route
   mit 610 Punkten ohne Höhen, 42,37 km gezeichnet. `../dl/locations.json`: die Marken der offiziellen Google-Karte auf
   derselben Seite (im Quelltext `var locations = [...]`): 41 KM-Punkte, Start, Ziel, 8 Verpflegungs- und 6 Wasserstellen,
   3 Staffel-Wechselzonen, Musik, Highlights.
2. `parse.py` → `gpx2026.json`; `proj.py` projiziert die KM-Punkte (Suchfenster 2,5 km nach dem vorigen Punkt, sonst
   landet KM 24 auf einem früheren Durchlauf bei Schwanheim) → `kmproj.json`; `common.py` eicht stückweise linear
   (Start = 0, Ziel = 42 195; die Linie ist 0,35 % zu lang).
3. `dgm.py`: **DGM1 Hessen** über den WCS des HVBG (`inspire-hessen.de/raster/dgm1/ows`, Coverage `he_dgm1`,
   EPSG:25832, 1 m), je ~250 m Strecke ein GeoTIFF-Ausschnitt, bilinear alle 10 m. 135 Abrufe, ~25 s. Braucht `pyproj`.
4. `streets.py`: Nominatim alle 150 m → `streets2026.json`.
5. `clean.py`: Stufen > 1,5 m auf 10 m. Gegenstufe innerhalb 600 m → Bereich; ohne Gegenstufe der kürzeste Bereich, an dessen
   Enden die Höhe wieder gleich ist (`spike`). Senke = **Brücke** (Wasser darunter), Buckel = **Unterführung** (Bahndamm oder
   A5 darüber). Ergebnis: Alte Brücke, Schwanheimer Brücke, zwei Brücken in Nied/Höchst (Mainzer Landstraße, Bolongarostraße),
   Unterführungen Goldsteinstraße (2×), Oeserstraße, Mainzer Landstraße unter der A5; dazu der Buckel des Modells am
   Zieleinlauf in die Festhalle (geglättet, nicht gelistet). Die echte Senke der Unterführung Oeserstraße (km 28,6–28,7,
   rund −3 m) bleibt, nur die Bahnbrücke darüber ist entfernt.
   **Seit 1.14** setzt `clean.py` vorher die Fahrbahn der vier Brücken aus `dom.py` ein (**DOM1 Hessen**, WCS
   `inspire-hessen.de/raster/dom1/ows`, Coverage `dom1`, Achsen E/N, je Punkt 25-%-Quantil der 5 × 5 m, nur zwischen den
   Brückenköpfen, weil das DOM daneben Bäume und Häuser misst). Sie sind damit gemessen und nicht mehr gestrichelt:
   Alte Brücke bis 103,3 m (Gerade bisher 99,7 m in der Mitte), Schwanheimer Brücke 101,4 m (bisher 99,5 m), die Nidda-
   Brücken Mainzer Landstraße und Bolongarostraße je ~0,5 m höher als die Gerade.
6. `build.py` → `data.json`; benennt „B 40“ in Schwanheimer Brücke und „F 1 Freifläche“ in Festhalle um.
7. `route.py`, `tiles.py` (wie Hamburg; z15 nur entlang der Strecke) → Kartenstücke in `../assets`.
8. `app.py`: hat aus `hamburg/index.html` die Erstausgabe von `frankfurt/` gebaut (Daten, Texte, Schlüssel, Symbol auf Weinrot, seit 1.5 nicht mehr verwendet).
   **Nur historisch**, gearbeitet wird direkt in `frankfurt/index.html`.

## Abgleich

Veranstalter: „Gesamthöhenunterschied 27,8 m“ und „83 Höhenmeter“. Laserscan: tiefster Punkt 90,0 m (Unterführung
Oeserstraße, km 28,7), höchster 118,1 m (Eschersheimer Landstraße, km 10,2), also 28,1 m; ↑ 85 m mit 200-m-Fenster (bis 1.13 mit geraden Brücken 82 m, 1.14–1.25 86 m).
Zieleinlauf (seit 1.26): Friedrich-Ebert-Anlage eben (97,2 ±0,1 m auf 500 m); vom Abbiegen aufs Messegelände (km 42,01)
bis vor die Festhalle (km 42,12) +1,2 m, gemessen auf freiem Grund (DOM = DGM auf 0,05 m), also echt, ~1 %. In der Halle
flach auf Höhe des Vorplatzes (98,4 m); bis 1.25 stieg die Linie dort an der Gebäudekante bis 99,2 m.
Rohdaten Punkt für Punkt ↑ 148 m (bis 1.13: 178 m, darin das Auf und Ab ins Wasser unter den Brücken). Steilste Stelle über 200 m: 3,1 % bei km 9,96.

## Offen

- Prüfung am iPhone (Flugmodus, Tipp auf „v1.0“).
- Kurs 2027 noch nicht veröffentlicht.
