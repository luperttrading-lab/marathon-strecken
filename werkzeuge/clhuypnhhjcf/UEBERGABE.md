# Übergabe: Hausrunde Schiffenberg (versteckt)

Stand 01.11.2026, App-Version **2.8** (erste Fassung, angelegt mit `werkzeuge/kern/kern.py --neu` auf dem gemeinsamen Kern; nicht
committet). Private Runde des Nutzers, **versteckt**: Ordner `clhuypnhhjcf/` (absichtlich nicht erratbar), nicht auf der Startseite, nicht
im README, nicht in `karten.json` (`kern.py` meldet deshalb „karten.json veraltet“; erst mit dem nächsten `--schreiben` käme sie dort
hinein). Vor dem öffentlichen Start entfernen (siehe `../VORGEMERKT.md`). Speicherschlüssel `hrs-…`, Cache `hrs-marathon-profil`.
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/clhuypnhhjcf/.

**Besonderheiten:** Kein Rennen, 9,85 km statt 42,195 km: Prüfstein für den längenunabhängigen Kern (2.8). Kein `D.termine`, keine
`D.wellen`, keine Staffel, keine Halbmarathon-Marke, keine Verpflegung; `D.start` 1080 (18:00), `D.tz` Europe/Berlin. Marken (Klasse
`half`, immer sichtbar): „Höchster Punkt“ (km 5,37, 254 m) und „Schiffenberg“ (km 6,38, nächste Stelle zum Kloster, 0,3 km südlich).

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Reihenfolge: `parse.py`, `osm.py`, `strassen.py` (mit `namen.py`), `dgm.py`, `clean.py`, `orte.py` (nur Ausgabe), `build.py`, `route.py`,
`tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py clhuypnhhjcf` (Ordner `clhuypnhhjcf/` muss es geben), `clhuypnhhjcf/work/app.py` (beim
ersten Mal über `kern.py --neu`, danach ersetzt es nur die Felder), `tiles_rand.py clhuypnhhjcf 2`. Prüfbild der Linie: `karte.py`
(`shots/_karte.png`). Prüfen: `pruefen.js`, `pruefen2.js` (Bilder), `pruefen3.js` (Randfälle), Server auf Port 8791,
`NODE_PATH=/opt/node-tools/node_modules node pruefen.js`.

1. **Linie** (`parse.py`): GPX aus MapPlanner (`../dl/runde.gpx`, vom Nutzer; 206 Punkte, jeder zweite doppelt, 153 verschiedene),
   9 911,3 m, Ende 33 m neben dem Start (Rathenaustraße beim Philosophikum). Der Nutzer läuft 9,85 km (Ecken abgekürzt): `common.py`
   staucht gleichmäßig auf `L` = 9 850 m. Die Höhen der GPX (↑ 163 m, bis 278 m) liegen im Mittel 10 m, im Wald bis 27 m über dem DGM1
   und sind nicht benutzt.
2. `osm.py`: OSM-API in 30 Rechtecken (1 133 Wege). `strassen.py` (Kopie Hannover): Alter Steinbacher Weg, 1., 2., 6. Schneise,
   Rathenaustraße; Wege ohne Namen benennt `build.py` beschreibend (`ERSATZ`): Weg am Philosophikum, Weg am Gießener Ring, Weg am
   Schiffenberger Weg, Waldweg Richtung Schiffenberg, Weg am Brauhofsweiher, Waldweg am Weiher. Gegend: alles Stadt Gießen (OSM
   admin_level 8 und 9, `orte.py`); westlich der A 485 „Gießen“, östlich „Schiffenberger Wald“ (beschreibend, die Waldfläche hat in OSM
   keinen Namen). Flurnamen (OSM `place=locality`: Sauweide, Rabennest …) liegen 100–700 m neben der Linie und sind nicht benutzt.
3. `dgm.py`: **DGM1 Hessen** und **DOM1 Hessen** über den WCS des HVBG (wie `../frankfurt/work/dgm.py`, `dom.py`), alle 10 Linienmeter,
   31 Ausschnitte in `../dl/wcs/`. DGM 160,5–254,6 m. Lizenz laut WCS: Datenlizenz Deutschland – Zero – 2.0 (© HVBG, wie Frankfurt).
4. `clean.py`: **Unterführung A 485.** Die zwei +3-m-Spitzen bei km ≈ 1,0 und ≈ 9,1 sind dieselbe Stelle: Der Alte Steinbacher Weg
   (OSM `maxheight` 4) läuft unter den zwei Brücken des Gießener Rings (A 485, OSM `bridge=yes`, `layer` 1; am Weg ein Kreuz „A485
   Tunnel Alter Steinbacher Weg“). DGM bis 169,3 bzw. 169,8 m statt 166 m (unter Brücken keine Bodenpunkte), DOM 171,5–171,7 m =
   Autobahn, gut 5,5 m über dem Weg. Gerade zwischen den gemessenen Enden 12 m vor/nach den Brückenachsen: km 1,014–1,053
   (165,7 → 166,3 m) und km 9,034–9,083 (166,4 → 165,7 m), in `D.bridges` (schraffiert, „Unterführung A 485“). Keine Brücke auf der
   Runde. Größte Stufe danach 1,28 m je 10 m (km 0,98, Einmündung in den Alten Steinbacher Weg, echtes Gelände).
5. `build.py`: ↑/↓ 122 / 118 / **111** / 92 m (Fenster 50 / 100 / 200 / 1000 m), Rohdaten 141 m; steilste 6,0 % bergauf (km 4,9),
   −8,3 % bergab (km 6,8), keine Stelle über 10 % (kein Bergstrecken-Hinweis). Der Hauptanstieg: km 3,1–5,4, 170 → 254 m.

## Modell (Stand 2.8)

Voreinstellung 4:00 /km im Flachen → Zielzeit 0:40:37, Steigungen +73 s. Flache 10 km in 40:00 ergeben (Riegel wie der Kern) die Runde in
**40:34** (Faktor 1,0143); mit 200-m-Rechenfenster wären es 40:29 (1,0119, die Schätzung in `../eichung/README.md`). Der Kern rechnet
Zeiten seit 1.54 immer mit 100 m (118 Höhenmeter), daher die 5 s.

## Offen

- Befunde zum Kern bei 9,85 km (Liste in der Antwort an die Hauptsitzung vom 01.11.2026), u. a.: Tabelle „Ohne Höhenmeter“ ohne Zeile
  für die flache Runde selbst, letzte Zeile „9,85“ in Zwischenzeiten und Pace-Band zeigt die Zeit für 0,85 km (sieht aus wie eine Pace),
  „je 10 km“ ergibt eine Zeile, Untertitel „Für Zuschauer“ nennt 5-km-Marken, Dateiname des Pace-Bands enthält den Ordnernamen.
