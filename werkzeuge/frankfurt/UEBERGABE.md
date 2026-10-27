# Übergabe: Steigungsprofil Frankfurt-Marathon

Stand 27.10.2026, App-Version **1.6** (seit 1.5 ohne eigenes Manifest und Symbol, siehe README; 1.6 Pace im Läuferblick), live unter https://luperttrading-lab.github.io/marathon-strecken/frankfurt/.

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
6. `build.py` → `data.json`; benennt „B 40“ in Schwanheimer Brücke und „F 1 Freifläche“ in Festhalle um.
7. `route.py`, `tiles.py` (wie Hamburg; z15 nur entlang der Strecke) → Kartenstücke in `../assets`.
8. `app.py`: hat aus `hamburg/index.html` die Erstausgabe von `frankfurt/` gebaut (Daten, Texte, Schlüssel, Symbol auf Weinrot, seit 1.5 nicht mehr verwendet).
   **Nur historisch**, gearbeitet wird direkt in `frankfurt/index.html`.

## Abgleich

Veranstalter: „Gesamthöhenunterschied 27,8 m“ und „83 Höhenmeter“. Laserscan: tiefster Punkt 90,0 m (Unterführung
Oeserstraße, km 28,7), höchster 118,1 m (Eschersheimer Landstraße, km 10,2), also 28,1 m; ↑ 82 m mit 200-m-Fenster.
Rohdaten Punkt für Punkt ↑ 178 m. Steilste Stelle über 200 m: 3,1 % bei km 9,96.

## Offen

- Prüfung am iPhone (Flugmodus, Tipp auf „v1.0“).
- Kurs 2027 noch nicht veröffentlicht.
