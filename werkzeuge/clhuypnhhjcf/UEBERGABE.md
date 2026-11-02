# Übergabe: Hausrunde Schiffenberg (versteckt)

Stand 01.11.2026, App-Version **2.8** (erste Fassung, angelegt mit `werkzeuge/kern/kern.py --neu` auf dem gemeinsamen Kern; nicht
committet). Private Runde des Nutzers, **versteckt**: Ordner `clhuypnhhjcf/` (absichtlich nicht erratbar), nicht auf der Startseite, nicht
im README, nicht in `karten.json` (`kern.py` meldet deshalb „karten.json veraltet“; erst mit dem nächsten `--schreiben` käme sie dort
hinein). Vor dem öffentlichen Start entfernen (siehe `../VORGEMERKT.md`). Speicherschlüssel `hrs-…`, Cache `hrs-marathon-profil`.
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/clhuypnhhjcf/.

**Straff gezogen 02.11.2026 (Marathon 2.15):** Der Nutzer läuft auf der Wegbreite die kürzeste Linie, nicht die Schlangenlinie der
Wegmitte (und schätzt die Runde auf 9,8 km). `korrektur.py` zieht die korrigierte Linie deshalb zuletzt wie ein Gummiband straff, jeder
Punkt höchstens 1,5 m neben seiner Lage (`korridor_m` in `korrektur.json`, vom Nutzer gewählt; gerechnet 0,5 m −19 m, 1 m −35 m,
1,5 m −53 m, 2 m −63 m). Länge **9 792 m** (die App zeigt „9,79“). Die Ersparnis verteilt sich über viele kleine Bögen, am meisten bei
km 6,3–7,0 und am Kreisel vor dem Ziel (km 9,5–9,75). Wegnamen ohne OSM-Namen hängen jetzt an Punkten (`GRENZEN` in `build.py`),
nicht an Metern. Unterführung km 0,970–1,020 und 8,980–9,030; ↑ 111 m (200 m); höchster Punkt km 5,45 (Kuppe flach, vorher 5,34);
Zielzeit bei 4:00 /km flach 40:22, Gelände +72 s. Nutzergefühl dazu: Die Runde kostet ihn 55–60 s; gegen 9,85 km gerechnet wären das
bei 9,79 km etwa 69–74 s, also wie das Modell (Antwort vom 02.11.2026).

**Korrektur 02.11.2026 (Marathon 2.14):** Der Nutzer hat auf Luftbildern (DOP20 Hessen, frei, Datenlizenz Deutschland Zero) den echten
Start markiert (20 m nach dem Linienanfang) und vier Kurven, die er abkürzt (km 0,67 und 2,29 Kehren, km 1,00 und 1,19 am Weg unter
dem Gießener Ring). Zwei Haken von je gut 2 m (km 3,34 und 3,64) waren Zeichenfehler von MapPlanner, wo die Runde hin und zurück
denselben Weg nimmt (Linienmeter 1 005–1 205 / 8 950–9 145 und 3 055–4 205 / 7 465–8 600). Neuer Schritt `korrektur.py` (Eingabe
`linie_roh.json` aus `parse.py` und `korrektur.json`): Linie 9 911,3 → **9 845,5 m**, praktisch die 9,85 km der Uhr des Nutzers;
daher keine Stauchung mehr (`common.py`: `L` = gemessene Länge, 9 846 m). Beschreibende Wegnamen (`ERSATZ` in `build.py`) über die
Lage umgerechnet. Unterführung jetzt km 0,980–1,020 und 9,030–9,070; ↑ 111 m (200-m-Fenster), steilste 6,4 % bergauf (100 m);
Zielzeit bei 4:00 /km flach 40:36 (vorher 40:37). Ziel unverändert am Linienende (33 m neben dem alten, 38 m neben dem neuen Start).

**Besonderheiten:** Kein Rennen, 9,85 km statt 42,195 km: Prüfstein für den längenunabhängigen Kern (2.8). Kein `D.termine`, keine
`D.wellen`, keine Staffel, keine Halbmarathon-Marke, keine Verpflegung; `D.start` 1080 (18:00), `D.tz` Europe/Berlin. Marken (Klasse
`half`, immer sichtbar): „Höchster Punkt“ (km 5,37, 254 m) und „Schiffenberg“ (km 6,38, nächste Stelle zum Kloster, 0,3 km südlich).

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Reihenfolge: `parse.py`, `korrektur.py`, `osm.py`, `strassen.py` (mit `namen.py`), `dgm.py`, `clean.py`, `orte.py` (nur Ausgabe), `build.py`, `route.py`,
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
