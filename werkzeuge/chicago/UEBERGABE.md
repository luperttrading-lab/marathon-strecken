# Übergabe: Steigungsprofil Chicago-Marathon

Stand 28.10.2026, App-Version **1.21** (1.21: Markierung im Pace-Diagramm stufenlos und ohne Wackeln, Tippen daneben nimmt sie weg, Punkt „hier“ mit km; 1.20: Markierung im Pace-Diagramm auch waagerecht zur Pace-Achse; 1.19: Pace-Diagramm ohne Laborlinie und graue Zone, −15 bis +10 %, Achse bei 0 %, Markierung zum Antippen; 1.18: Bergab fest „halb“ ohne Schalter, steiler als −8 % kein weiterer Gewinn statt U-Kurve; 1.17: flacher Halbmarathon in der Tabelle ohne Höhenmeter, Erklärung im Info-Fenster (i); 1.16: Kosten je Höhenmeter bei 4:00 /km mit wählbarer Bezugs-Pace, Bahnzeiten als Tabelle, größere Überschriften in den Einstellungen; 1.15: unter der Zielzeit flacher Marathon und Bahnzeiten 10 000 m / 5000 m; 1.14: Zeiten immer mit 100 m, „Pace hier“ über das Messfenster gemittelt; 1.13: Messfenster 50 / 100 / 200 m / 1 km statt 10 m, neuer Erklärtext; 1.12: Zwischenzeiten mit Halbmarathon-Zeile und „je 10 km“; 1.11: Knopfrahmen so hell wie die Räder, „Vollbild“ blau, im Vollbild führt ‹ zurück in die normale Ansicht; 1.10: Kopf eines offenen Abschnitts bleibt oben stehen, Zuklappen von überall; 1.9: beim Aufklappen bleibt der Kopf des Abschnitts an seiner Stelle; 1.8: Hinweis, wenn die eingestellte Startzeit zu keiner Welle passt; „Blöcke“ statt „Corrals“; 1.7: Standard 5 km Ausschnitt und Tempo ×200, Menü-Knopf blau mit Beschriftung, Abschnitte unter dem Läuferblick aufklappbar; 1.6: Startwellen mit Uhrzeiten unter „Deine Startzeit“, Start 7:35 (Welle 1) statt 7:30 (Profis); 1.5: Pfeile in Bisher/Noch/Ganze Strecke und Rampe als Grafik, dreistellige Werte ohne „…“, zu breite Werte werden kleiner; 1.4: Bergab U-Kurve statt Grenze bei −4 %: am schnellsten bei −8 %, ab −16 % langsamer als flach, ohne Knick bei 0 %; 1.3: Tempo-Rad mit ×1 (Echtzeit), ×50 und ×100–×180 in 20er-Schritten; 1.2: Brücken-Beschriftungen überlappen nicht mehr; 1.1: Kästchen bunt/grau neben der Gesamtstrecke, Diagramm „So rechnet das Pace-Modell“; 1.0: Erstausgabe), live unter https://luperttrading-lab.github.io/marathon-strecken/chicago/.

Die App ist eine Kopie der Boston-App (Stand 1.0) mit eigenen Daten, Texten und Speicherschlüsseln (`chi-…`), ohne eigenes
Manifest und Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in
[`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Änderungen am gemeinsamen Code in allen Apps nachziehen (README).

49. Chicago Marathon am Sonntag, 10. Oktober 2027 (Bank of America, Pressemitteilung), Start der Profis 7:30, Welle 1 7:35 Uhr Ortszeit
(`D.start` = 455, `D.tz` America/Chicago, `D.ortKurz` „ Chicago“). Start und Ziel im Grant Park am Columbus Drive.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

1. **Quellen des Veranstalters 2026:** `../dl/pdf/26-BACM-STREET-CLOSURE-BROCHURE.pdf` (Abbiegeliste: je Meile Straße von … bis …)
   und `../dl/pdf/26-BACM-COURSE-MAP-PRINT.pdf` (Karte als Vektor-PDF). Eine GPX gibt es nicht.
2. `strecke.py`: die 38 Abschnitte der Abbiegeliste über das OSM-Straßennetz (`../dl/osm_wege.json`, Overpass maps.mail.ru):
   Kanten der genannten Straße kosten ihre Länge, andere das Sechsfache, untere Ebenen („Lower …“, level −1, unter der Erde ohne
   Tunnel-Tag) das Fünfzigfache. Echte kurze Tunnel bleiben erlaubt (Grand Avenue unter der Michigan Avenue). Lücken im Netz
   einer Straße unter 25 m (mehrstöckige Kreuzungen am Columbus Drive) werden mit Verbindern geschlossen. Ziel jedes Abschnitts
   ist die nächste Kreuzung mit der folgenden Straße, nicht die, an der man steht (Sheridan Road und Lake Shore Drive treffen
   sich zweimal). Ergebnis: Straßenfolge genau wie die Liste.
3. `geo.py` + `marken.py`: Die Streckenlinie der Karte (Pfad in #00226A, `../dl/pdf/kurs_pt.json`) ist von Ziel nach Start
   gezeichnet; affin georeferenziert über 24 Ecken (Rest 15 m RMS, `../dl/karte_affin.json`). Daraus Start (Columbus Drive an
   der Monroe Drive), 26 Meilen- und 8 Fünf-Kilometer-Marken (Beschriftungen per `pdftotext -bbox`). `parse.py` schneidet die
   Linie am Start; das Ziel liegt 352 m (vermessen) hinter Meile 26, gut 180 m nördlich der Ecke Roosevelt Road (das Ende der
   Kartenlinie läuft rund 90 m darüber hinaus). Linie 42,874 km.
4. **Eichung** (`common.py`): Die Linie ist 1,6 % länger als die vermessene Strecke (Straßenmitte statt Ideallinie, 37 Abbiegungen
   auf breiten Straßen; die Kartenlinie selbst misst ebenso viel). Stückweise linear über die Marken, Stützstellen alle 5 km,
   kleinste Quadrate; Ausreißer über 80 m verworfen (Meile 4, 5, 15K, Meile 16, 17, 22, 23: Marken an Wendepunkten und auf der
   doppelt belaufenen Michigan Avenue). Reste der übrigen Marken ±70 m.
5. `verpflegung.py`: 20 Verpflegungsstationen (orange Symbole der Karte) und 2 Gel-Depots (Maurten, schwarz), georeferenziert und
   projiziert. Abgleich mit dem Veranstalter: Nachfüllstellen „kurz vor Station 4, 7, 12, 16“ bei Meile 5,7 / 10,1 / 15,7 / 20,3,
   gefunden bei 5,88 / 10,21 / 15,97 / 20,33. Auf der Michigan Avenue (26th–31st Street, zweimal belaufen) liegen zwei Symbole
   gut 60 m neben der Linie: Station 17 an der 26th Street (Hinweg), Station 19 weiter südlich (Rückweg).
6. `dgm.py`: **USGS 3DEP** 1-m-Laser-Geländemodell (Projekt IL_4_County_QL1_LiDAR_2016_B16, Befliegung 2017), NAVD88.
   **Keine Punktwolke:** Die USGS hat für Cook County keine EPT-Punktwolke auf AWS (geprüft: alle IL_-Projekte). Brücken und
   Hochstraßen deshalb mit `clean.py` (wie New York, `lidar.json` = Geländemodell) zwischen den Auflagern gerade gezogen und
   gestrichelt: obere Ebene des Columbus Drive (das Geländemodell zeigt dort eine Plattform 7 m höher), Grand Avenue unter der
   Michigan Avenue, die Brücken über den Chicago River (Dearborn, LaSalle, Wells, Adams/Wacker), Halsted über die I-290,
   Cermak, Wentworth über die I-55, Michigan Avenue und die Roosevelt Road („Mount Roosevelt“).
7. `streets.py` (Nominatim alle 150 m, Ort = Community Area), `build.py` (Straßennamen ohne Himmelsrichtung und Ebene wie auf der
   Karte, Orte unter 600 m dem Vorgänger zugeschlagen, Start und Ziel „Grant Park“), `route.py` (lat0/lon0 41,8/−87,7),
   `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py chicago`, `work/app.py` (aus `boston/index.html`), `tiles_rand.py chicago 2`.

## Ergebnis

↑ 43 m / ↓ 41 m mit 200-m-Fenster, ↑ 59 / ↓ 58 m mit 50 m; Höhe 177,3–186,9 m. Start 182,9 m, Ziel 183,9 m.
Einziger echter Anstieg: „Mount Roosevelt“ (Roosevelt Road über die Gleise, 180,7 → 186,9 m, bis +3,1 % über 200 m, km 41,8).
Mit 4:00/km im Flachen ergibt das Modell 2:49:10.

## Offen

- Prüfung am iPhone.
- Höhen der Brücken und der oberen Ebenen sind geschätzt; eine Punktwolke (Cook County 2017) wäre beim Illinois State
  Geological Survey zu suchen.
- Die App zeigt den Kurs 2026. Für 2027 die Abbiegeliste des Veranstalters prüfen, sobald sie erscheint.
