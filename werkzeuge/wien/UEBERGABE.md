# Übergabe: Steigungsprofil Vienna City Marathon

Stand 30.10.2026, App-Version **1.0** (1.0: erste Fassung).
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/wien/.

Die App ist eine Kopie der Tokio-App (Stand 1.30, aktueller gemeinsamer Code) mit eigenen Daten, Texten und Speicherschlüsseln
(`vie-…`, Service-Worker-Cache `vie-marathon-profil`, löscht nur Caches mit Präfix `vie-`), ohne eigenes Manifest und Symbol. Alle
Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Änderungen am
gemeinsamen Code in allen Apps nachziehen (README). Gegenüber `tokio/index.html` weichen genau dieselben Zeilen ab wie bei Amsterdam
(die Zeile „Glättung“ ist gleich geblieben).

## Termin und Start

44. Vienna City Marathon am Sonntag, 18. April 2027 laut Seite „Marathon“ des Veranstalters
(https://www.vienna-marathon.com/?go=marathon, ebenso die Startseite): „Startzeit: ab 9:00 Uhr in mehreren Wellen“, Start Wagramer
Straße/Reichsbrücke, Zielschluss 15:30 Uhr, Ziel Ringstraße/Burgtheater; AIMS-vermessen, World Athletics Elite Label. Der 43. VCM
war am 19. April 2026 (gelaufen). `D.termine` `["2026-04-19", "2027-04-18"]` (2027 vom Veranstalter bestätigt, daher ohne „?“),
`D.tz` Europe/Vienna, `D.ort` „Wien“ (nach der Zeitzone hieße es sonst „Vienna“), `D.ortKurz` „ Wien“, `D.start` = 540 (9:00).
Zielschluss 15:30 nur im Text (kein `D.tor`, daher kein `D.zielschluss`); im Zeitplan 2026 stehen „Letzte Finisher &
Schlussläufer*innen“ um 15:35 am Burgtheater.

**Startblöcke** (`D.wellen`): sechs Blöcke 2026 laut Seite „Dein Start am VCM-Sonntag“ (https://www.vienna-marathon.com/?go=start):
A 9:00, B 9:06, C 9:13, D 9:19, E 9:26, F 9:33, Startvorgang endet 9:40; dieselben Zeiten in der Google-Karte. Marathon, Halbmarathon
und Staffel starten gemeinsam, eingeteilt nach angegebener Zielzeit (Marathon unter 3:40 nur mit Leistungsnachweis), die Blöcke
sind gleich groß, Zeitspannen je Block nennt der Veranstalter nicht. Farben laut Startblockplan 2026
(https://www.vienna-marathon.com/var/upload/public/2026/startblock_2026_9uhr.pdf): A orange (davor Elite und „Superfast Runners /
Championships“, ebenfalls 9:00, Sektoren A1–A3), B blau, C schwarz, D rot, E lila, F gelb. Für 2027 noch nicht veröffentlicht; der
Hinweis in der App sagt das. Der Tchibo Coffee Run 10K startet um 8:00 an derselben Stelle.

Start auf der Wagramer Straße in Kaisermühlen (22. Bezirk) in zwei Fahrbahnen: Elite, A, C, E rechts (Karte: „START A, Blöcke 1, 3,
5“), B, D, F links und weiter hinten („START B, Blöcke 2, 4, 6“, eigene Linie über die andere Fahrbahn der Reichsbrücke, trifft die
Hauptlinie nach 2,6 km in der Lassallestraße; 2572 m gegen 2597 m bei A). Die App folgt Start A. Ziel auf dem Universitätsring vor
dem Burgtheater (Zielbereich Rathausplatz), nicht am Heldenplatz oder Burgring.

**Halbmarathon und Staffel** laufen gleichzeitig auf derselben Strecke; die App bildet nur den Marathon ab. Trennung bei km 20,3
an der Bellariastraße (Halbmarathon rechts ins Ziel, Marathon und Staffel geradeaus, Seite „Strecke“). Staffelwechsel laut
Streckenplan 2026 („location at K 15,5 / 23,5 / 30,5“): Linke Wienzeile/Schönbrunn, Roßauer Lände, Meiereistraße/Ernst-Happel-Stadion.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

1. **Strecke** aus der Google-Karte des Veranstalters „43. Vienna City Marathon 2026 Marathon und Halbmarathon“ (verlinkt auf
   https://www.vienna-marathon.com/?go=course als „Interaktiver Streckenplan – Sonntag“), als KML:
   `https://www.google.com/maps/d/kml?mid=1POyNKcbwqhpoS9gAsxzPgN4fyLDRwfQ&forcekml=1` (`../dl/karte_….kml`). Ordner
   „Marathon & Powerade Staffelmarathon“: Linie „Marathon 42,195 km“ (404 Punkte), 42 Kilometermarken, drei Staffelwechsel; „Start |
   Finish“: START A, START B, FINISH, Blöcke; „Streckenbereich – Verpflegungspunkte“. `parse.py` projiziert die Marken auf die Linie
   (höchstens 12 m daneben). **Start:** Die Karte setzt START A an die Spitze des Elite-Blocks; von dort bis zur Marke km 1 sind es
   928 m, zwischen allen übrigen Marken 961–1052 m (Median 1009), auf den geraden ersten 2 km 997 m. Die 10-km-Linie derselben Karte
   beginnt am selben Punkt und hat ebenfalls 927 m bis km 1. Die Kilometerschilder passen also zu einer Startlinie rund 70 m weiter
   hinten; die Linie ist geradeaus auf der Wagramer Straße um 70,1 m verlängert (erster Kilometer so lang wie der zweite). Der
   Startblockplan 2026 ist schematisch und bestätigt das nur ungefähr. Linie mit Verlängerung **42 593 m** geodätisch (GRS80), ohne
   42 523 m. → `gpx2026.json`, `marken.json`.
   **Gegenproben** (`vergleich.py`): Der Streckenplan 2027 („Sonntag, 18. April 2027“, `VCM-Streckenplaene_2027_SO_v1.pdf`, erstellt
   13.04.2026) und der Plan 2026 (`VCM-Streckenplaene_2026_SO-alleBewerbe_v4.pdf`) enthalten die Marathonlinie als Vektor; sie ist
   in beiden Punkt für Punkt gleich (0,000 pt Abstand), also **Kurs 2027 = Kurs 2026**. Plan 2026 affin auf die Linie eingepasst
   (13 m/pt): Median 11–12 m, 95 % bis 39 m (Linie → Plan); bis 160 m nur an der Wende am Lusthaus (km 32,5–33, im Plan schematisch).
   Das GPX des Veranstalters (`ViennaCityMarathon-PoweradeRelayMarathon.gpx`, mit dem Routenplaner von Strava auf OSM gezeichnet,
   731 Punkte, 42 724 m) liegt im Median 1,5 m neben der Linie, höchstens 29 m; seine Kilometer liegen gleich (km 1 ebenfalls bei
   927 m). Seine eingebetteten Höhen nimmt die App nicht.
2. `common.py`: **Kilometer stückweise linear** über die 42 Marken (Marke zu Marke 965–1049 Linienmeter, Median 1009; km 42 bis Ziel
   196 m), Start am Anfang der verlängerten Linie, Ziel am Ende (FINISH 3,6 m daneben). Zeitmatten liegen alle 5 km und beim
   Halbmarathon; ihre Lage veröffentlicht der Veranstalter nicht gesondert, die 5-km-Marken sind unter den 42. Genauigkeit: Einzelne
   Marken der Karte weichen bis etwa 45 m ab (km 27 am Praterstern: 1049 m davor, 965 m danach), dazwischen also auf etwa ±50 m.
   Die Verpflegungspunkte der Karte liegen nach der Eichung höchstens 0,1 km neben ihrer km-Angabe, nur Kärntner Ring „40,8“ bei
   40,6; wo Karte und Seite „Strecke“ sich widersprechen (Meiereistraße 29,8 / 29,4, Rustenschacherallee 37,4 / 37,7), passt die
   Seite (29,33 und 37,71 nach der Eichung).
3. `osm.py`: OSM-Wege (highway, railway) und Gewässer im Umkreis von 40 m um die Linie über den Overpass-Spiegel maps.mail.ru in
   Stücken (viele 504, Zwischenstand `../dl/osm_teil_*.json`); overpass-api.de brach die Verbindung ab, kumi.systems und
   private.coffee antworteten nicht. `strassen.py`: je 10 m der nächste Weg bis 35 m daneben, Hauptstraßen bevorzugt, Querstraßen
   und Wege ohne Namen mit Aufschlag (im Prater liegt die Linie auf dem Rückweg bis 30 m neben der Mitte der Hauptallee, auf Reit-
   und Radwegen). `namen.py`: Namen wie in OSM (z. B. „Weiskirchnerstraße“, der Veranstalter schreibt „Weißkirchnerstraße“).
4. `dgm.py`: **Geländemodell der Stadt Wien** („Geländemodell Raster Wien“, MA 41 Stadtvermessung, Open Government Data,
   https://www.data.gv.at/katalog/dataset/1eda4b16-05e3-43c3-b5b0-ef8276df0701, laut Katalog zuletzt geändert 20.11.2025, Lizenz
   CC BY 4.0, Quelle „Stadt Wien – data.wien.gv.at“): **1-m-Raster**, GeoTIFF float32 je Blatt der Mehrzweckkarte 1:5000 (2,5 ×
   2,5 km, EPSG 31256), Download `https://www.wien.gv.at/ma41datenviewer/downloads/geodaten/dgm_tif/<Blatt>_dgm_tif.zip`, Blattschnitt
   aus dem WFS der Stadt (`ogdwien:MZKBLATT5000OGD`); 10 Blätter (35/1–4, 36/1, 36/3, 44/2, 45/1, 46/1, 46/2), `../dl/dgm/`. Laut
   Produktinformation (https://www.wien.gv.at/stadtplanung/digitales-gelaendemodell-produktinformation) im Straßenraum aus den
   Höhenpunkten und Bruchkanten der Mehrzweckkarte gerechnet (±10 cm), wo die nicht reicht (Wald) aus Laserscans; **Brücken sind
   nicht enthalten**. Höhen über Wiener Null; + 156,68 m = Meter über Adria (laut Stadt Wien; im WFS der Höhenfestpunkte ist
   HOEHE_ADRIA − HOEHE_WIEN überall 156,68; die Nieten der 235 Festpunkte in Blatt 35/4 liegen im Median 0,3 m über dem Modell).
   Bilinear je 10-m-Punkt, 4261 Punkte, keine Lücke. → `dgm2026_10m.json`.
5. `als.py` (nur Gegenprobe): **Laser-Geländemodell des BEV** (ALS DTM, Höhenraster 1 m, Stichtag 15.09.2025, Kachel
   `ALS_DTM_CRS3035RES50000mN2800000E4750000.tif` von https://data.bev.gv.at/download/ALS/DTM/20250915/, CC BY 4.0). Die Kachel ist ein
   gekacheltes GeoTIFF von 7,9 GB; `httpfile.py` liest über HTTP-Range nur die 70 Teilkacheln entlang der Linie (`../dl/als/`).
   Ergebnis: ALS minus Stadt-Modell im Median −0,51 m, die Hälfte zwischen −0,54 und −0,48, 90 % zwischen −0,61 und −0,43 m, also
   dieselbe Form überall; der gleichmäßige Abstand ist der Höhenbezug (BEV: EVRF2000, EPSG 9274 laut Metadaten; Stadt: Adria).
   Die Steigungen sind damit lasergeprüft.
6. `dsm.py`: **Oberflächenmodell des BEV** (ALS DSM, 1 m, Stichtag 15.09.2025, gleiche Kachel unter `…/ALS/DSM/20250915/`) auf den
   OSM-Brücken und 80 m davor und danach, je Punkt das 25-%-Quantil im Umkreis von 2 m, + 0,51 m wie oben. → `dsm_10m.json`.
7. `clean.py`: Brücken aus OSM (bridge=yes auf der Linie, Straßen; aus mehreren OSM-Wegen zu einem Stück), Enden oben auf den
   Rampen (höchster Punkt bis 30 m vor der Brücke, dann weiter, solange das Modell auf dem Damm steigt). Das Modell fällt auf allen
   fünf Brücken der Strecke 8,5 bis 14 m ins Wasser bzw. auf Ufer und Donauinsel.
   **Reichsbrücke** (km 0,22–1,05, 832 m): Das Oberflächenmodell misst die Fahrbahn glatt von 171 m an den Enden auf 176,2 m bei km
   0,80, 5,2 m über der Geraden (an den Enden 0,1–0,2 m über dem Geländemodell); das Höhenbild des Veranstalters zeigt denselben
   Buckel (175 m bei km 0,8). Dort gilt das Oberflächenmodell, an den Enden angeglichen; die Brücke zählt als **gemessen** (nicht
   schraffiert, wie gemessene Brücken in Rom und Valencia). Grund: Die App zieht Schraffur und Strich einer geschätzten Brücke gerade
   von Ende zu Ende und würde den Buckel durchschneiden. Mit gerader Reichsbrücke wären es ↑ 103 / ↓ 92 m statt 108 / 97 m
   (`DSM_BRUECKEN` in `clean.py` leeren).
   **Geschätzt** (gerade, schraffiert): Aspernbrücke (km 8,99–9,11, Donaukanal), Friedensbrücke (km 23,71–23,80, Donaukanal),
   Franzensbrücke (km 38,31–38,40, Donaukanal), Stubenbrücke (km 39,53–39,57, Wienfluss); das Oberflächenmodell liegt dort
   höchstens 1,5 / 0,6 / 0,9 / 0,1 m über der Geraden. Keine weiteren Stufen über 1,5 m.
   **Unterführungen**, gemessen (das Modell kennt den Boden der Straße): Nordbahn über der Lassallestraße am Praterstern (km 2,2),
   Bahn über dem Eingang der Hauptallee (km 2,6), Bahn über der Schüttelstraße (km 8,25 und 38,2), U6 über der Linken Wienzeile
   (km 13,9), Verbindungsbahn über der Linken Wienzeile (km 14,9), Südosttangente A23 (Prater Hochstraße) über der Hauptallee
   (km 31,4 und 34,0), Laaer Ostbahn über der Hauptallee (km 32,4 und 33,0). Tunnel hat die Strecke nicht.
8. `orte.py`: **Bezirk** alle 100 m aus den Bezirksgrenzen der Stadt (WFS `ogdwien:BEZIRKSGRENZEOGD`,
   https://www.data.gv.at/katalog/dataset/2ee6b8bf-6292-413c-bb8b-bd22dbb2ad4b), Schreibweise „2. Bezirk, Leopoldstadt“. Begründung: In
   Wien orientiert man sich an den 23 Bezirken mit Nummer und Namen (die Nummer steht auf jedem Straßenschild und steckt in der
   Postleitzahl, 1020 = 2. Bezirk); Bezirksteile und Katastralgemeinden sind nicht amtlich bzw. kaum geläufig, die Zählbezirke sind
   Statistik. Auf Grenzstraßen (im Umkreis von 25 m beide Bezirke zu mindestens 4 von 13 Teilen) beide: Innere Mariahilfer Straße
   „6./7. Bezirk, Mariahilf/Neubau“, Auerspergstraße und Landesgerichtsstraße „1./8.“, Maria-Theresien-Straße „1./9.“. Die Strecke
   berührt den 22., 2., 1., 6., 15., 14., 7., 8., 9., 20. und 3. Bezirk; 14,4 km am Stück im 2. (Donaukanal und Prater).
9. `build.py`: Höhen in cm im 10-m-Raster, Median über 30 m; Straßen unter 80 m und Bezirke unter 300 m dem Vorgänger zugeschlagen.
   Marken laut Übersicht der Verpflegstationen auf der Seite „Strecke“ (2026), an ihrer km-Angabe: Getränke (Wasser im Becher,
   Powerade) km 4,8 / 9,5; Verpflegung (dazu Bananen) km 15 / 19,6 / 24,8 / 29,4, mit Coca-Cola km 34 / 39,6; Wasser (Becher, mit
   Helfern) km 31,4 / 38,6; Wasserhähne ohne Personal km 3,9 / 7,4 / 10,5 / 11,7 / 12,5 / 13,1 / 17,8 / 21,8 / 26,1 / 27,2 / 28,5 /
   37,7 / 40,8; Gel (ESN Hydro Energy Gel) km 33,5; Staffelwechsel km 15,5 / 23,5 / 30,5; Halbmarathon 21 098 m. Nicht übernommen:
   die Verpflegstellen nur für Staffelläufer (km 15,5 / 23,5 / 30,5), das Ziel und drei Wasserstellen, die nur die Karte zeigt
   (Schüttelstraße 101 km 6,5 / 36,5, Alserbachstraße km 23,7). `route.py` (lat0/lon0 48,2/16,3), `tiles.py`, dann aus
   `werkzeuge/`: `tiles_z11.py wien`, `work/app.py` (aus `tokio/index.html` und `tokio/sw.js`; Texte in `sub.html`,
   `quellen.html`, `strassennamen.html`, `imgnote.html`), `tiles_rand.py wien 2`.
10. `planprofil.py`: Höhenbild des Veranstalters (`profile.png`, auch im Streckenplan) ausgelesen; y-Maßstab über den Pfeil „44 m“
    (0,62 m/px). `gegenprobe.py <…>/course_segments.parquet`: Vergleich mit dem privaten Datensatz (siehe unten; liest nur diese
    Datei).

## Ergebnis

↑ 108 m / ↓ 97 m mit 200-m-Fenster (Tabelle in der App: 50 m 128, 100 m 120, 1 km 72), Rohdaten ↑ 223 m. Start 165,7 m auf der
Wagramer Straße, höchster Punkt 202,4 m auf der Mariahilfer Straße am Gürtel (km 17,9), tiefster 157,7 m an der Meiereistraße beim
Stadion (km 29,5), Ziel 176,5 m am Burgtheater (Höhen über Adria); Höhenbereich 44,7 m (Veranstalter: 44 m). Gleich nach dem Start
5 m hinauf auf die Reichsbrücke (176 m, km 0,8) und hinunter zum Praterstern, flach durch Prater und am Donaukanal (158–162 m), über
Ring und Linke Wienzeile stetig hinauf bis Schönbrunn (189 m, km 15,5) und auf der Mariahilfer Straße zum Gürtel, hinunter zum
Museumsquartier und an den Donaukanal (165 m, km 22,7), flach bis km 38, dann über Radetzkystraße und Ring 13 m hinauf bis zum
Burgring und leicht hinunter ins Ziel. Steilste Stellen über 200 m: −3,8 % auf der Mariahilfer Straße (km 19,9), −3,6 % von der
Reichsbrücke in die Lassallestraße (km 1,1); bergauf +2,6 % am Start, +2,2 % Schloßallee (km 16,1), +2,1 % Stadionallee (km 5,7
und 35,7). Mit 4:00/km im Flachen ergibt das Modell **2:49:48** (das Profil kostet 61 s); bei 2:50:00 kosten die Steigungen 61 s,
bei 4:00:00 86 s.

**Abgleich mit dem Höhenbild des Veranstalters** (`planprofil.py`): Korrelation 0,98, Bild minus App im Median −0,4 m, die Hälfte
zwischen −1,6 und +0,5 m, 95 % innerhalb 4,8 m; gleicher Buckel der Reichsbrücke, gleicher Anstieg Wienzeile und Mariahilfer
Straße. Der höchste Punkt liegt im Bild bei km 18,3 (Pfeil „44 m“), in der App bei 17,9; den Abstieg zum Museumsquartier zeichnet
das Bild knapp 500 m später (km 20,3 statt 19,8 auf halber Höhe).

**Gegenprobe mit dem Datensatz** (`course_segments`, city „Vienna“, aus dem GPX des Veranstalters mit dessen eingebetteten Höhen,
Schwelle 1 m auf Punkten alle ~100 m; nur gelesen). App wie in der App (200-m-Fenster) und nach dem Verfahren des Datensatzes:

| Abschnitt | Datensatz ↑/↓ | App 200 m ↑/↓ | App 100 m + 1-m-Schwelle ↑/↓ | Datensatz min–max | App min–max |
|---|---|---|---|---|---|
| 0–5 km | 9,7 / 14,9 | 11,6 / 18,4 | 10,6 / 17,3 | 158,7–173,7 | 158,9–176,0 |
| 5–10 km | 17,6 / 4,2 | 14,5 / 4,8 | 14,6 / 5,6 | 157,8–170,3 | 158,5–168,6 |
| 10–15 km | 18,6 / 4,0 | 21,8 / 4,2 | 18,6 / 2,0 | 170,3–186,8 | 168,6–186,1 |
| 15–20 km | 16,8 / 22,3 | 18,6 / 22,1 | 17,7 / 21,7 | 182,8–203,1 | 182,2–202,4 |
| 20–25 km | 10,3 / 29,9 | 7,6 / 28,0 | 7,4 / 27,6 | 163,0–187,2 | 162,0–185,6 |
| 25–30 km | 4,9 / 6,8 | 4,6 / 8,0 | 4,8 / 8,0 | 157,8–165,0 | 157,7–164,9 |
| 30–35 km | 1,3 / 0,0 | 2,7 / 2,6 | 0,0 / 0,0 | 157,9–159,3 | 157,8–159,4 |
| 35–40 km | 12,5 / 3,8 | 15,3 / 6,0 | 14,5 / 5,2 | 157,8–166,9 | 158,5–168,1 |
| 40–42,195 km | 12,6 / 3,7 | 11,1 / 2,7 | 10,2 / 1,3 | 166,4–180,2 | 168,1–179,3 |
| Summe | 104,3 / 89,6 | 107,8 / 97,1 | 98,5 / 88,5 | | |

Nach gleichem Verfahren liegen Datensatz und App in der Summe 6 bzw. 1 m auseinander; der Unterschied am Start ist die Reichsbrücke
(im Datensatz höchstens 173,7 m, im Oberflächenmodell 176,2 m). Höhenbereich beider 157,7/157,8 bis 202,4/203,1 m.

Geprüft mit Playwright (393 × 852, Faktor 2, Server auf Port 8778): keine Konsolenfehler, `APP_VERSION` 1.0, Service Worker
installiert (31 Dateien im Cache `vie-marathon-profil`), Tipp auf die Version meldet „Version 1.0 ist aktuell“, alle 25
Kartenstücke passen zu `D.tiles` und `sw.js` und laden, Tabellen ohne Überbreite (Seitenbreite 393 px), Zuschauer-Tabelle mit
Blöcken A–F und nächstem Termin 18. April 2027; Laufansicht am Start, km 0,8 (Reichsbrücke), 9,05, 17,9, 19,9, 29,5 und 41,5 sowie
die Karte (Schönbrunn, Lusthaus) angesehen.

## Offen

- Prüfung am iPhone.
- Startseite: Karte für Wien fehlt noch (Eyebrow „Vienna City Marathon“, Stadt „Wien“, „Kurs 2026“,
  `data-termine="2026-04-19 2027-04-18"`, `data-monat="4"`, ↑ 108 m / ↓ 97 m, Höhe 158–202 m, `data-such` z. B. „Vienna Wien
  Österreich Austria VCM“; Mini-Profil mit 44 m Höhenbereich etwa 70 px hoch, z. B. `.spark.wien { height: 70px; }`), README-Tabelle
  und Liste der Speicherschlüssel/Cache-Präfixe (`vie-`).
- **Startlinie**: um 70 m hinter START A der Karte angenommen (siehe Daten 1). Prüfen, sobald der Startblockplan 2027 erscheint
  oder eine Messung mit Koordinaten auftaucht; liegt die Linie doch an START A, in `parse.py` ohne Verlängerung rechnen (der erste
  Kilometer hätte dann nur 928 Linienmeter).
- Startblöcke und Zeiten 2027 eintragen, sobald veröffentlicht (2026 im März auf der Seite „Dein Start am VCM-Sonntag“).
- Die Google-Karte heißt noch „2026“. Erscheint eine Karte 2027 (neue Adresse auf der Seite „Strecke“), `parse.py` und
  `vergleich.py` erneut laufen lassen.
- Reichsbrücke nach dem Oberflächenmodell statt gerade (Daten 7): Entscheidung des Nutzers offen.
