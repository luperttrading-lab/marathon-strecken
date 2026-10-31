# Übergabe: Steigungsprofil PUMA Salzburg Marathon

Stand 31.10.2026, App-Version **2.6** (erste Fassung, angelegt mit `werkzeuge/kern/kern.py --neu` auf dem gemeinsamen Kern; die
Hauptsitzung zählt die Nummer beim Veröffentlichen hoch).
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/salzburg/.

Die App hat den gemeinsamen Kern aus `hamburg/` und eigene Felder (Texte, `const D`, Speicherschlüssel `szg-…`, Service-Worker-Cache
`szg-marathon-profil`, löscht nur Caches mit Präfix `szg-`; der Präfix war frei, `kern.py --neu` prüft das), ohne eigenes Manifest und
Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Startseite,
README, `version.json` und `karten.json` sind noch nicht angepasst (Hauptsitzung).

**Besonderheiten:** Der Marathon läuft **zweimal dieselbe Runde** (Halbmarathon = eine Runde ins selbe Ziel). Die Linie kommt aus der
**Google-Karte des Veranstalters** und ist eine **aufgezeichnete Spur** (1,9 % zu lang); die Kilometer sind über eine **Ideallinie**
verteilt (kürzeste Linie im Band von ±3 m, Daten 3). Höhen aus dem **Laser-Geländemodell des BEV** (ALS DTM 1 m, Befliegung 2022,
CC BY 4.0), an der **Straßenmitte** abgelesen (die Spur liegt bis 9 m daneben, am Salzachkai sonst auf der Böschung). **Staatsbrücke**
und **Lehener Brücke** aus dem Oberflächenmodell (ALS DSM) gemessen, die **Unterführung der Gaswerkgasse** geschätzt. Der Veranstalter
nennt „9 m maximale Höhendifferenz“; das Lasermodell misst **21 m** (417–438 m), siehe Ergebnis. **Echte Marathonstaffel** (Powerade
Staffel Marathon, vier Läufer auf derselben Strecke): drei Staffelwechsel in `D.marks`, Staffel-Schalter sichtbar.

## Termin und Start

Offizieller Name **„PUMA Salzburg Marathon“** (Namenssponsor PUMA; Veranstaltung „Lauffestspiele der Mozartstadt“, Veranstalter
SportImPuls Verlags- & Marketing GmbH, Salzburg). Halbmarathon „Sparkasse Halbmarathon“, Staffel „Powerade Staffel Marathon“.
Seite https://salzburg-marathon.at/de/ (`../dl/seiten/`). Nächste Austragung, der **24., am Sonntag, 23. Mai 2027, Start 8:30 Uhr auf der
Staatsbrücke** (Seite „PUMA Salzburg Marathon – 42,195km“: „Sonntag, 23. Mai 2027 … Start: Staatsbrücke … Der Startschuss für den 24.
PUMA Salzburg Marathon fällt am 23. Mai 2027 um 08:30 Uhr“; ebenso Fuß jeder Seite und salzburg.info). Der 23. war am **Sonntag, 17. Mai
2026** (Seite „Ergebnisse, Fotos und Video-Highlights 2026“, Pressemitteilung `PressInfo_SaM_20260517_english.pdf`). `D.termine`
`["2026-05-17", "2027-05-23"]` (2027 bestätigt, ohne „?“), `D.tz` Europe/Vienna, `D.ort` „Salzburg“, `D.ortKurz` „ Salzburg“ (die Zeitzone
hieße sonst „Vienna“), `D.start` = 510 (8:30). Kein `D.lage`, `D.mauer`, `D.tor`, `D.zielschluss`.

**Start** (`D.wellen`): Seite „Wichtige Informationen PUMA Salzburg Marathon“ (2026, `../dl/seiten/wi_wichtige-informationen-puma-salzburg-marathon.html`):
„Für einen flüssigen Ablauf wird das Starterfeld in vier Blöcken eingeteilt, der Start erfolgt in drei Wellen. Das Startsignal für die
Startblöcke Grün und Orange ertönt um 8:30 Uhr. … Rot … um 8:35 Uhr. … Blau … um 8:40 Uhr“; Aufstellung in der Schwarzstraße, Marathon und
Halbmarathon gemeinsam, Block laut Anmeldung (Farbe auf der Startnummer). Staffel 8:40 aus dem letzten Block (Seite „Powerade Staffel
Marathon“). In der App drei Knöpfe „Grün und Orange · 8:30“, „Rot · 8:35“, „Blau · 8:40“. Für 2027 nennt der Veranstalter nur „in mehreren
Wellen“; der Hinweis sagt das. **Zeitlimit** 5:45 h (Seite 2027; 2026 „Zielschluss … um 14:15 Uhr“); wer nach der ersten Runde ins
Halbmarathon-Ziel läuft, wird im Halbmarathon gewertet (Text unter „Deine Startzeit“).

**Ziel:** Am **Max-Reinhardt-Platz** (Google-Karte 2026 „FINISH LINE“, Verpflegungsplan „Ziel Max-Reinhardt-Platz | Philharmonikergasse“,
Streckenplan 2026, Sperrliste „Hofstallgasse | Max-Reinhardt-Platz“). Die Seiten für 2027 schreiben „Ziel: Residenzplatz“, die Seite
„Informationen“ „Zieleinlauf vor am Residenzplatz“ – vermutlich ein älterer Text; prüfen, sobald der Plan 2027 erscheint (Offen).

**Staffel** (Seite „Powerade Staffel Marathon“, 2027): Etappen 15,2 + 5,9 + 15,2 + 5,9 km; Wechsel 1 und 3 „vor der Stiegl Brauwelt“ (km 15,2
und 36,3), Wechsel 2 am Universitätsplatz (km 21,1, Halbmarathon-Zwischenzeit). Lage aus den Punkten „Relay Zone 1/2“ der Google-Karte:
App km 15,1 / 21,1 / 36,2. Ergebnislisten 2024–2026 zeigen dieselben Etappen („0-15,2km“, „15,2-21,1km“, „21,1-36,3km“, „36,3-42,19km“).

**Halbmarathon-Marke** bei 21 098 m (Universitätsplatz, wie Wechsel 2).

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Reihenfolge: `parse.py`, `osm.py`, `strassen.py`, `schnur_szg.py 3` (Ideallinie, mit `ideal.py`), `strecke.py`, `dtm.py` (mit `bev.py`,
`httpfile.py`), `clean.py`, `orte.py`, `build.py`, `route.py`, `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py salzburg`,
`salzburg/work/app.py` (beim ersten Mal über `kern.py --neu salzburg work/felder.json`, danach ersetzt es nur die Felder und lässt
Kartenbilder und `D.tiles` stehen), `tiles_rand.py salzburg 2`. Nur Abgleich/Ausgabe: `vergleich_km.py <w>`, `bev_meta.py` (Befliegungsjahr),
`glo30.py` (Gegenprobe Copernicus), `ergebnisse.py` (Finisher zählen), `karte.py` (Prüfbilder `shots/_*.png`), `text.py` (Text gespeicherter
Seiten). Prüfen: `pruefen.js` … `pruefen4.js` (Server auf Port 8792, `NODE_PATH=/opt/node-tools/node_modules node pruefen.js`).
`schnur_szg.py` heißt so (statt `ideal_w.py` wie in Freiburg), weil eine parallele Sitzung Läufe namens `ideal_w.py` beendet hat.

1. **Strecke** (`parse.py`): Google-Karte „Strecke Salzburg Marathon“ des Veranstalters, verlinkt im „Eventguide Lauffestspiele der
   Mozartstadt 2026“ (https://salzburg-marathon.at/de/eventguide-lauffestspiele-der-mozartstadt-2026/), als KML
   `https://www.google.com/maps/d/kml?mid=1vlZE3NUVGTzmIZemOiiAyM9z0kypvUw&forcekml=1` (`../dl/karten/`). Ordner „MARATHON Strecke“: eine
   Linie für beide Runden (900 Punkte, Beschreibung „Die Statistiken basieren auf importierten Daten. Mittwoch, 28. Februar 2024 …
   Entfernung: 43,1 km … Durchschnittsgeschwindigkeit: 26,0 km/h“, also eine Fahrrad- oder Autoaufzeichnung; die zweite Runde ist dieselbe
   Aufzeichnung, bis auf 1 m deckungsgleich), Start, Ziel, „Relay Zone 1/2“, fünf „Aid Station“, zwei „Water Station“, Cheering Zones und
   Musikspots 2026; Ordner „MARATHON KM PUNKTE“: KM 3 bis KM 42 (1 und 2 fehlen). Zwei weitere verlinkte Karten (Weg zu den Duschen,
   Staffel) sind nicht öffentlich (403). **Kurs:** Die Streckenpläne 2024 (`Streckenplan_Marathon_2024.pdf`), 2025 (`…_2025_NEU.pdf`) und
   2026 (`…_2026.pdf`, Dezember 2025; dieselbe Karte als `.webp`, April 2026; `../dl/plan/`) zeigen denselben Weg; die Straßenliste
   („Streckenverlauf“) des Plans und die Sperrliste 2026 (`2026_VERKEHRSINFOS_SPERREN.pdf`) decken sich mit der Linie. Plan 2027: „Streckenplan
   (in Kürze verfügbar)“. Eyebrow daher „Kurs 2026“. Linie vom Startpunkt (Nordostende der Staatsbrücke) bis zum Zielpunkt **42 988 m**.
2. `osm.py`: OSM-API in 70 Rechtecken zu 0,005° höchstens 150 m neben der Linie, eine Abfrage je Sekunde (mehrmals 509, gewartet) →
   `../dl/osm_netz.json` (9 375 Wege). `strassen.py`: je 10 Linienmeter der nächste Weg bis 25 m mit höchstens 35° Richtungsabweichung,
   Hauptstraßen bevorzugt; dazu der **Fußpunkt auf dem Weg**. Die Spur liegt im Median 3,2 m neben der Straßenmitte, 90 % bis 7,6 m, 99 % bis
   10,5 m.
3. **Kilometer** (`ideal.py`, `schnur_szg.py`, `strecke.py`, `common.py`): Die Spur ist 793 m (1,9 %) länger als 42 195 m (Rauschen der
   Aufzeichnung und Kurven). `ideal.py` (Kopie Freiburg) spannt eine Schnur im Band ±w m um die Spur (Punkte alle 2 m, 2 500 Runden):
   w = 3 m ergibt **42 200,5 m** (3,5 m: 42 104,0; 4 m: 42 014,9). Die Strecke besteht aus Runde (Start A bis Herbert-von-Karajan-Platz B,
   dort trennt sich die zweite Runde vom Weg ins Ziel F) und Schleife (B über Universitätsplatz, Residenzplatz, Mozartplatz und Runde 2 zurück
   nach B); der Halbmarathon läuft A–B–F, also messen A–B + B–F und B–B je genau 21 097,5 m. Auf der Ideallinie 21 074,1 m bzw. 21 126,4 m,
   je für sich gestreckt (Faktoren 1,0011 und 0,9986).
   **Abgleich** (`vergleich_km.py 3`): Staffelzonen und Verpflegung der Karte liegen nach dieser Zuordnung bei 15,12 / 21,05 / 36,23 km
   (Veranstalter 15,2 / 21,1 / 36,3) und 5,52 / 10,81 / 15,19 / 19,33 / 26,67 / 31,93 / 36,30 / 40,42 km (Verpflegungsplan 5,5 / 10,9 /
   15,2 / 19,4 / 26,6 / 32,0 / 36,3 / 40,5), also höchstens 0,09 km daneben; Wasser NaWi 23,31 (Plan 23,2), Wasser Gneis 10,13 / 31,24
   (Plan „Tennishalle/Berchtesgadener Straße 9,8 / 30,9“: anderer Ort, die Karte 2026 gilt). Die **Kilometerpunkte der Karte** liegen dagegen
   0,04 bis 0,24 km früher (Median 0,11 km) und passen nicht zusammen: Start bis KM 3 wären 2,9 km, KM 20 bis KM 21 1,1 km, KM 41 bis KM 42
   1,1 km; nicht verwendet. **Genauigkeit der Kilometer etwa ±0,1 km.**
4. `dtm.py`, `bev.py`, `httpfile.py`: **BEV ALS DTM** (Laser-Geländemodell, Höhenraster 1 m, Serie Stichtag 15.09.2025, Metadaten
   https://data.bev.gv.at/geonetwork/srv/metadata/ec12896e-1ecd-47ad-8d48-44d236e383cc, `../dl/bev/meta_dtm.xml`), Kacheln
   `https://data.bev.gv.at/download/ALS/DTM/20250915/ALS_DTM_CRS3035RES50000mN2700000E4500000.tif` und `…E4550000.tif` (4,4 bzw. 8,0 GB;
   die Strecke liegt auf beiden), EPSG 3035, Höhen EVRF2000 (EPSG 9274). `bev.py` liest je 512 × 512-m-Teilkachel eine HTTP-Range-Abfrage
   (`../dl/bev/DTM_*`, `DSM_*`, zusammen gut 300 MB in `../dl`). **Befliegung 2022** laut Metadatenübersicht des BEV (`bev_meta.py`,
   `Metadatenuebersicht_SHP_DTM_DSM_20250915.zip`: Gebiet „Salzburg“, Flugjahr 2022). **Lizenz** CC BY 4.0 („Für dieses Produkt gilt die
   Standardlizenz CC-BY-4.0“, Metadaten). Bilinear alle 10 Linienmeter an der Spur und am Fußpunkt auf der Straßenmitte (`strassen.py`, wo
   höchstens 15 m entfernt); die App nimmt die Straßenmitte (Unterschied im Median 0,0 m, 90 % bis 0,4 m; am Rudolfskai und in der Griesgasse
   lag die Spur 8–9 m daneben auf der Böschung, bis 2 m tiefer). Das Laser-Geländemodell der Stadt bzw. des Landes Salzburg (SAGIS) habe ich
   nicht gesucht; das BEV-Modell ist dieselbe Landesbefliegung.
   Dazu je Punkt das 25-%-Quantil des **ALS DSM** (Oberflächenmodell, gleiche Serie und Lizenz, `…/ALS/DSM/20250915/…`) im Umkreis von 2 m.
5. `clean.py`: **Brücken und Unterführung.**
   - **Staatsbrücke** (Start km 0,00–0,07, km 20,25–20,33, 41,35–41,42) und **Lehener Brücke** (km 18,61–18,72 und 39,72–39,82): Das
     Geländemodell misst die Salzach (412–413 m); dort gilt das Oberflächenmodell, wo es auf einer OSM-Straßenbrücke und je 3 Punkte davor und
     danach mehr als 1 m über dem Geländemodell und dieses mehr als 1 m unter beiden Enden liegt, an den Enden weiter, solange das
     Oberflächenmodell 0,5 m darüber liegt (Böschung). Staatsbrücke 422,2–422,9 m (fast eben), Lehener Brücke 420,0 → 421,0 → 420,2 m. Enden
     auf 0,1–0,3 m gleich. Gemessen, nicht schraffiert. Ein Punkt an der Berchtesgadner Straße (km 8,35 und 29,85, Bach) 1,4 m tief: ebenfalls
     Oberflächenmodell (auf Höhe der Enden). Kleine Brücken (Hellbrunner Allee, Nissenstraße, Zwieselweg, Berchtesgadner Straße km 8,74)
     ohne Senke; am Zwieselweg misst das Oberflächenmodell Bäume (bis 451 m) – deshalb die Bedingung „unter beiden Enden“.
   - **Unterführung Gaswerkgasse** unter der Bahn (km 17,92–18,11 und 39,03–39,21; OSM `tunnel=yes`, `layer=-1`, `maxheight=3.75`): Das
     Modell misst den Bahndamm (bis 429 m), danach fällt es in 10 m um 5,4 m auf die Straße in Lehen. **Geschätzt** als Gerade von 426,0 m
     (Müllner Hauptstraße) auf 418,4 m (−4 %, im 200-m-Fenster −3,7 %, die steilste Stelle bergab), in `D.bridges` (gestrichelt). Wie die
     Straße in der Unterführung wirklich verläuft (erst steil hinunter, dann flach?), ist nicht gemessen.
   - Übrige OSM-Tunnel: Durchgänge (Gstättentor, Ritzerbogen, Dreifaltigkeitsgasse) und der Elisabethkai unter der Eisenbahnbrücke – das
     Modell misst dort die Straße (keine Stufe). Danach nur zwei Einzelpunkte über 1,5 m (km 4,24 und 29,48, Gräben), die der Median glättet.
6. `orte.py`: **Stadtteil** alle 100 Linienmeter aus den Salzburger Stadtteilen (OSM `admin_level` 10, Namen wie in OSM: Altstadt, Nonntal,
   Salzburg Süd, Morzg, Hellbrunn, Gneis, Riedenburg, Leopoldskroner Moos, Maxglan, Mülln, Lehen, Elisabeth-Vorstadt, Neustadt), außerhalb
   die Gemeinde (`admin_level` 8: Anif, Grödig – die Keltenallee ist Stadtgrenze), je 40 m links und rechts, bei zwei „links / rechts“.
7. `build.py`: Höhen in cm im 10-m-Raster, Median über 30 m; Straßenstücke unter 80 m und Stadtteile unter 300 m dem Vorgänger zugeschlagen;
   der Fußgängerbereich am Schloss Hellbrunn ohne OSM-Namen heißt „Hellbrunn“ (Streckenverlauf des Veranstalters). **Verpflegung**: Lage aus
   der Karte („Aid Station …“, „Water Station …“), Inhalt und Seite aus dem Verpflegungsplan `Versorgungsaufbau25.pdf` (verlinkt auf der Seite
   „Wichtige Informationen“ 2026; PDF erstellt 2023): V1 Hellbrunn beidseitig, V2 Leopoldskron-Kobergerweg rechts, V3 Maxglan-Franz-Huemer-Straße
   links, V4 Arbeiterkammer-Markus-Sittikus-Straße rechts (je Wasser, Wasser mit Kohlensäure, Powerade, Coca-Cola, Bio-Bananen,
   Eigenverpflegung), V5 Universitätsplatz „Höhe Brunnen“ links nur in Runde 1 (ohne Coca-Cola; in der Karte fehlt V5, gelegt auf den
   Marktbrunnen am Universitätsplatz, OSM-Knoten 2377499299, km 21,10), W1 NaWi nur Runde 2, W2 Gneis (nur Wasser). Ziel-Verpflegung (u. a.
   Stiegl-Bier, Bio-Obst) nicht als Marke. Staffelwechsel 1–3 aus den „Relay Zone“-Punkten. 16 Marken mit Halbmarathon.
   `route.py` (lat0/lon0 47,8/13,0; Lage von der Straßenmitte, über ±20 m geglättet), `tiles.py` (z12–z15), `tiles_z11.py salzburg`, `app.py`,
   `tiles_rand.py salzburg 2`: 16 Kartenstücke, 1,2 MB.

## Ergebnis

↑ 91 m / ↓ 90 m mit 200-m-Fenster, ↑ 121 / ↓ 120 m mit 50 m, ↑ 108 / ↓ 107 m mit 100 m, ↑ 49 / ↓ 47 m mit 1 km; wie GPS-Uhren 96 (ab
0,5 m), 77 (ab 1 m), 43 (ab 3 m); Rohdaten ↑ 212 m (Geländemodell Punkt für Punkt, mit Salzach unter den Brücken und Bahndamm).
Start 422,2 m auf der Staatsbrücke, Ziel 423,3 m am Max-Reinhardt-Platz; tiefster Punkt **417,0 m** in Lehen (Joachim-Haspinger-Straße,
km 18,47 und 39,57), höchster **438,0 m** an der Berchtesgadner Straße bei Glanegg (km 7,66 und 28,80); **Höhenbereich 21 m**.
Verlauf je Runde: flach durch Altstadt und Nonntal (421–422 m), die Hellbrunner Allee leicht hinauf (428 m bei km 5), am Schloss Hellbrunn
über Fürstenweg und Morzger Straße hinauf (+3,2 % über 200 m bei km 5,8 und 26,9, die steilste Stelle bergauf) auf Keltenallee und
Berchtesgadner Straße (435–438 m), durch Gneis und Leopoldskron langsam hinunter (430–432 m), über die Moosstraße nach Maxglan (428 m), über
den Müllner Hügel an der Augustinergasse (431 m, km 17,35), durch die Unterführung der Gaswerkgasse nach Lehen (417 m), über Lehener Brücke (421 m)
und Elisabethkai (418 m), durch die Neustadt hinauf zum Mirabellplatz (424,5 m) und über die Staatsbrücke in die Altstadt.
**Veranstalter:** „9 m maximale Höhendifferenz“, „laut Vermessungsprotokoll flach“; Streckenplan „Start 425 m | Highest 431 m | Lowest 422 m |
Finish 428 m“. Das Lasermodell zeigt 21 m. **Gegenprobe** (`glo30.py`): Copernicus DEM GLO-30 (Oberflächenmodell, 30 m) an offenen Stellen
0–1,5 m über dem BEV-Modell (km 0,5: 421,2 / 420,7; km 9: 435,6 / 435,5; km 12: 431,5 / 430,8; km 14: 431,5 / 431,0; km 18,5: 418,7 /
417,2), unter Bäumen und Häusern höher; der Höhenbereich von rund 20 m bestätigt sich.
**Modellzeit:** Mit 4:00/km im Flachen ergibt das Modell **2:49:35** (das Profil kostet 48 s); **bei 2:50:00 kostet es 48 s, bei 4:00:00
68 s** (Flach-Pace 4:00,6 bzw. 5:39,7 /km; gemessen mit `pruefen.js` in der App 2.6). Zum Vergleich: Düsseldorf 37 s, Köln 48 s, München
48 s bei 4:00/km im Flachen (laut ihren Übergaben).

Geprüft mit Playwright (Chromium, 393 × 852, Faktor 2, Server auf Port 8792, `pruefen.js` … `pruefen4.js`): keine Konsolenfehler,
`APP_VERSION` 2.6 und Knopf v2.6, Service Worker installiert (22 Einträge im Cache `szg-marathon-profil`), Tipp auf die Version meldet
„Version 2.6 ist aktuell“; alle 16 Kartenstücke passen zu `D.tiles` und `sw.js` und laden; Tabellen bei 320/375/393/430 px ohne Überbreite,
Seite nicht breiter als das Fenster; Staffel-Einstellung sichtbar. Laufansicht am Start, km 5,8 (Fürstenweg), 7,7 (höchster Punkt), 12,5,
18,0 (Unterführung, gestrichelt), 18,7 (Lehener Brücke), 20,3 (Staatsbrücke), 21,1 (Universitätsplatz), 42,1 (Ziel), Staffelwechsel km 15,1
und die Kartenübersicht mit Verpflegung angesehen; Kopf, Zuschauer-Tabelle (drei Wellen) und „Woher die Zahlen kommen“ angesehen. Bilder in
`work/shots/` (Prüfbilder der Aufbereitung mit `_` davor). `kern.py` meldet alle Apps „gleich“, nur `karten.json` veraltet (neue Strecke,
Hauptsitzung).

## Offen

- Prüfung am iPhone.
- **Kurs 2027 und Ziel:** Streckenplan und interaktive Karte 2027 sind „in Kürze verfügbar“. Kommt eine neue Google-Karte, `parse.py`
  (Dateiname) und die Kette laufen lassen. Dabei prüfen, ob das Ziel 2027 am Residenzplatz liegt (so die Seiten 2027) statt am
  Max-Reinhardt-Platz (Plan, Karte und Verpflegungsplan 2026); dann ändern sich der Weg ab dem Herbert-von-Karajan-Platz und `strecke.py`
  (Punkt B).
- Startblöcke 2027 eintragen, sobald veröffentlicht (2026 stand es Anfang Mai auf der Seite „Wichtige Informationen“).
- Kilometer ±0,1 km (Ideallinie); die Kilometerpunkte der Google-Karte passen nicht zueinander. Ein Vermessungsprotokoll (AIMS) oder eine
  GPX-Datei des Veranstalters würde das klären. Lage der Wasserstelle Gneis (Karte 10,1 km, Plan 9,8 km).
- Unterführung Gaswerkgasse geschätzt (Gerade, 7,6 m auf 190 m).
- Der Veranstalter nennt 9 m Höhenunterschied, das Lasermodell 21 m (siehe Ergebnis); in der App steht das im Abgleich und unter „Höhe“.
- Startseite: Karte fehlt. Eyebrow „PUMA Salzburg Marathon“, Stadt „Salzburg“, „Kurs 2026“, `data-termine="2026-05-17 2027-05-23"`,
  `data-monat="5"`, Termintext „So., 23. Mai 2027“, ↑ 91 m / ↓ 90 m, Höhe 417–438 m, `data-land` Österreich, `data-such` z. B. „Salzburg
  Österreich Austria Mozartstadt Lauffestspiele Hellbrunn Salzach Staatsbrücke PUMA“. Mini-Profil: 21 m Höhenbereich passt in die Grundhöhe
  64 px (40 m = 56 px), keine eigene Klasse nötig. README-Tabelle und Liste der Präfixe (`szg-`), `karten.json`
  (`kern.py --version … --schreiben`). Fuß der Startseite: „BEV (Salzburg, ALS DTM und DSM, CC BY 4.0)“ (bisher „BEV (Wien, CC BY 4.0)“).
  **Teilnehmer 2026:** **1 703 Marathon-Finisher** (offizielle Ergebnisliste „23. PUMA Salzburg Marathon“, Zeitnehmung Datasport,
  verlinkt auf salzburg-marathon.at „Alle Ergebnisse“ → https://www.datasport.de/anmeldeservice/salzburgmarathon2026/ergebnisse, dort
  Race Result Ereignis 385271, Wettbewerb „PUMA Salzburg Marathon“, Liste „00 Ergebnisliste MW“: 1 744 Einträge, davon 1 703 mit Platz und
  Zeit, 33 DNF, 8 DNS; 1 270 Männer und 474 Frauen in der Liste; gezählt mit `ergebnisse.py`, keine Namen gespeichert). runinternational.eu
  nannte 1 700. 2025: 1 261 (Ereignis 325880), 2024: 773 (276167). Staffeln 2026: 119 im Ziel (2025: 91, 2024: 60). Veranstalter 2026:
  „Rund 2.500 Anmeldungen entfielen 2026 auf den PUMA Salzburg Marathon“, 14 273 Anmeldungen über alle Bewerbe.
- Termine 2028 ff.: jährlich nachtragen (Mai; 2025 am 18. Mai, 2026 am 17. Mai, 2027 am 23. Mai).
