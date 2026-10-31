# Übergabe: Steigungsprofil Brocken-Marathon (Harz-Gebirgslauf)

Stand 31.10.2026, App-Version **2.5** (erste Fassung, angelegt mit `werkzeuge/kern/kern.py --neu` auf dem gemeinsamen Kern; die
Hauptsitzung zählt die Nummer beim Veröffentlichen hoch).
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/brocken/.

Die App hat den gemeinsamen Kern aus `hamburg/` und eigene Felder (Texte, `const D`, Speicherschlüssel `brk-…`, Service-Worker-Cache
`brk-marathon-profil`, löscht nur Caches mit Präfix `brk-`; der Präfix war frei, `kern.py --neu` prüft das), ohne eigenes Manifest und
Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Startseite,
README, `version.json` und `karten.json` sind noch nicht angepasst (Hauptsitzung).

**Besonderheiten:** Der erste **Berglauf** der App mit einem amtlichen 1-m-Laser-Geländemodell: Rundkurs ab Wernigerode-Hasserode über
den **Brocken** (1141 m), ↑ 1146 m / ↓ 1143 m mit 200-m-Fenster, Höhenbereich 874 m (Rennsteig: 180 m). Die Linie kommt aus der
**GPX-Datei des Veranstalters** (Strava-Route, hinter „Streckenkarte anzeigen“ auf der Seite „Strecken“), auf die OSM-Wege gelegt. Höhen
aus dem **DGM1 Sachsen-Anhalt** (LVermGeo, Laserscan April 2019, dl-de/by-2-0). Steinige Wald- und Forstwege, an den steilen Stücken mit
Gehpassagen: Das Pace-Modell (an Straßenmarathons geeicht) ist hier zu optimistisch; den Hinweis dazu baut die Hauptsitzung in den Kern.
Die Texte der Strecke stellen die Modellzeiten nirgends als realistisch dar. Keine Staffel (Schalter bleibt aus).

## Termin und Start

Offizieller Name: **Brocken-Marathon** beim **Harz-Gebirgslauf** (Veranstalter Harz-Gebirgslauf 1978 e.V. Wernigerode, Seite
https://harz-gebirgslauf.de/; „Brocken-Marathon 42,2 km“, „Norddeutschlands schwerster Marathon“), ohne Namenssponsor. Der 48. war am
**Samstag, 10. Oktober 2026** (Startseite „Alle Infos zum 48. Harz-Gebirgslauf am 10.10.2026“, Zeitplan auf „Wissenswertes“). **2027
ist noch nicht veröffentlicht** (Stand 31.10.2026: weder Seite noch Veranstaltungsliste nennen ihn). Der Verein schreibt „Seit 1978 kommen
am zweiten Wochenende im Oktober …“ und „jährlich am zweiten Samstag im Oktober“ (Seite „Verein“); 2025 war es der 11.10., 2026 der 10.10.,
beides der zweite Samstag. Daraus **9. Oktober 2027, unbestätigt**: `D.termine` `["2026-10-10", "2027-10-09?"]`, `D.tz` Europe/Berlin,
`D.start` = 540 (9:00). Kein `D.lage`, `D.mauer`, `D.tor`, `D.zielschluss`.

**Start** (`D.wellen`, `w` leer, nur Text): Zeitplan 2026 „09:00 Uhr Brocken-Marathon“, Start und Ziel an der Himmelpforte (Start-/Zielgebiet
an der Hochschule Harz). **Zeitlimits** (Seite „Strecken“, „Zielschluss“): „Teilnehmer des Brocken-Marathons, die bis 12:00 Uhr den Brocken
nicht passiert haben, werden aus der Wertung genommen. Zielschluss für alle Läufer und Wanderer auf allen Strecken ist 15:00 Uhr.“ Also 3 h
bis zum Gipfel (hier km 19,2), 6 h bis ins Ziel. Teilnehmerlimit 1000 (Nationalpark). Alles im Text unter „Deine Startzeit“, dazu die
festen Öffnungszeiten der Verpflegung und der Halb-Marathon (22,5 km, 10:15 Uhr; laut seiner GPX bis ins Ilsetal, km 9,3, und ab der
Mönchsbuche, km 36,5, auf derselben Strecke, dazwischen über die Plessenburg). Die
**Halbmarathon-Marke** steht wie überall bei 21 098 m (Brockenstraße, unter der Knochenbrecherkurve); sie ist nicht der Halb-Marathon des
Laufs.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Reihenfolge: `parse.py`, `osm.py`, `match.py`, `georef.py` (nur Abgleich), `strassen.py`, `vorladen.py` (mit `lvermgeo.py`), `dgm.py`,
`clean.py`, `orte.py`, `stationen.py`, `build.py`, `route.py`, `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py brocken`,
`brocken/work/app.py` (beim ersten Mal über `kern.py --neu brocken work/felder.json`, danach ersetzt es nur die Felder und lässt
Kartenbilder und `D.tiles` stehen), `tiles_rand.py brocken 2`. Nur Abgleich/Ausgabe: `auswertung.py`, `ergebnisse.py` (Finisher zählen).
Prüfen: `pruefen.js` … `pruefen4.js` (Server auf Port 8793 aus dem Repo-Wurzelordner, `NODE_PATH=/opt/node-tools/node_modules node pruefen.js`).

1. **Strecke** (`parse.py`): Die Seite „Strecken“ (https://harz-gebirgslauf.de/strecken.html) lädt beim Klick auf „Streckenkarte anzeigen“
   per Leaflet-GPX `https://harz-gebirgslauf.de/files/GPX/HGL_Brocken_Marathon_1180_HM.gpx` (Last-Modified 29.02.2024,
   `../dl/gpx/`): eine **Strava-Route** „Brockenmarathon 1180 Hm“ (Routenplaner, © OSM-Mitwirkende 2020), 1163 Punkte, Abstand im Median
   30 m, höchstens 100 m, **42 253 m**, Start und Ziel 113 m auseinander an der Himmelpforte. Die Höhen der Datei (Strava) liegen im Median
   6,7 m über dem DGM und werden nicht benutzt. Ebenso liegen GPX-Dateien für 22,5, 11 und 4,8 km dort (nur die des Halb-Marathons geladen).
   Eine Ausschreibung als PDF gibt es nicht; alles steht auf den Seiten „Strecken“, „Wissenswertes“ und der Veranstaltungsseite
   (`../dl/seiten/`). **Kurs:** Die Datei liegt seit Februar 2024 dort und hängt an der Seite für 2026; die Streckenkarte (Grafik „© Passeck &
   Wernecke 2016“, Datei „HGL_Streckenkarte_2024“) zeigt denselben Weg. Eyebrow daher „Kurs 2026“.
2. `osm.py`: OSM-API in 181 Rechtecken zu 0,005° höchstens 150 m neben der Linie, eine Abfrage je Sekunde, keine 509/429 →
   `../dl/osm_netz.json` (2083 Wege). Die GPX liegt schon auf OSM-Wegen: im Median 0,8 m daneben, 99 % bis 4,6 m.
3. `match.py` → `gelegt.json`: kürzester Weg im OSM-Netz, Kante kostet Länge × (1 + (Abstand / 8 m)²), Anker alle 200 m (Muster Rennsteig).
   Ergebnis **42 284 m** (+0,07 % gegen die GPX), im Median 0,8 m neben ihr, höchstens 11 m (letzte Meter ins Ziel). Kein Stück musste aus
   der GPX übernommen werden.
4. **Kilometer** (`common.py`): gleichmäßig auf 42 195 m (Faktor 0,9979). `georef.py` legt die Streckenkarte des Veranstalters
   (`../dl/bilder/HGL_Streckenkarte_2024.jpg`, 2000 × 1533 px) affin auf die Linie (vier Passpunkte von Hand, dann ICP über die roten
   Linienpixel; 8,5 m/px, Linie zur Kartenlinie im Median 6 m, 90 % bis 42 m, höchstens 145 m). Die **Kilometerdreiecke** der Karte (von Hand
   abgelesen) liegen hier bei km 5,27 / 9,92 / 15,28 / 19,68 / **23,63** / 30,14 / 35,33 / 40,25: alle bis 0,33 km daneben, nur „25 km“ steht
   1,4 km zu früh (am Brockenbett). Dazu passt die Verpflegung „Brockenbett bei km 24“, die hier bei km 23,1 liegt. Da die Linie überall zur
   Karte passt und km 30 wieder stimmt, halte ich die Angaben dort für ungenau (offen). **Genauigkeit der Kilometer etwa ±0,3 km.**
5. `strassen.py` (Kopie Freiburg, kleine Aufschläge je Wegklasse, weil die Linie schon auf den Wegen liegt): Weg je 10 m. Viele Wald- und
   Forstwege haben in OSM keinen Namen; `build.py` benennt längere Stücke nach Orten aus Streckenkarte und OSM (`ERSATZ`): Waldweg am
   Haidknüll, Waldweg Öhrenfeld – Tänntal, Waldweg nach Ilsenburg, Waldweg am Gelben Brink, Brockenplateau, Waldweg zum Hanneckenbruch,
   Waldweg über die Mönchsbuche, Waldweg über den Schwengskopf, Waldweg am Kuhbornteich; die Straße „Ilsetal“ heißt auch zwischen Waldhotel
   und Schutzhütte so. Mit OSM-Namen: Himmelpforte, Lindenallee, Klosterholz, Ilsetal, Rote Brücke, Gelber Brink, Hermannstraße,
   Hirtenstieg, Brockenstraße, Glashüttenweg, Eschwegestraße, Ellenbogen-Chaussee, Thumkuhlental, Bielsteinchaussee (29 Abschnitte).
6. `lvermgeo.py`, `vorladen.py`, `dgm.py`: **DGM1 Sachsen-Anhalt** (LVermGeo, Open Data). Die Seite
   https://www.lvermgeo.sachsen-anhalt.de/de/gdp-dgm1.html enthält das Kachelverzeichnis als GeoJSON (2 × 2 km, 5469 Kacheln,
   `../dl/lvermgeo/dgm1_kacheln.geojson`); der Download läuft ohne Anmeldung über
   `…/de/mod/2,2913,501/ajax/1/prepare/?items=<id>&format=zip` → Link `…/ajax/1/download/?file=mapdownloader-<hash>.zip` (DOM1 entsprechend
   `mod/3,2926,501`, nicht genutzt). Im ZIP GeoTIFF (Float32, LZW, 2000 × 2000, NoData −9999, EPSG:25832, NHN DHHN2016, GCG2016), `.meta` und die
   Nutzungsbedingungen. 23 Kacheln (≈ 270 MB in `../dl/dgm1/`), Metadaten in `../dl/dgm1/meta.json`: **Aktualität 07./08.04.2019**
   (Laserbefliegung), **Fortführung 28.08.2024**, Genauigkeit 0,15 m (Landesamt: ±0,15 m flach, ±0,30 m steil mit dichter Vegetation).
   Bilinear alle 10 Linienmeter, 4230 Punkte, alle mit Wert. Gipfel 1140,7 m (amtlich 1141,2 m), also keine Schneedecke im Modell.
   **Lizenz:** Nutzungsbedingungen des LVermGeo (Version 5.0, im ZIP): offene Daten „dürfen frei genutzt werden unter der Lizenz
   ‚Datenlizenz Deutschland - Namensnennung - Version 2.0‘ … Der Bereitsteller … ist mit ‚© GeoBasis-DE / LVermGeo ST‘ zu bezeichnen.“ Im
   Untertitel „Datenquelle: © GeoBasis-DE / LVermGeo ST, dl-de/by-2-0, Daten geändert“, unter „Woher die Zahlen kommen“ dasselbe mit Jahr
   (2025, Copyright-Vermerk der Kacheln), Link auf die Lizenz und auf die Open-Data-Seite (dl-de/by-2-0 verlangt einen Hinweis auf Änderungen).
7. `clean.py`: **Brücken.** Zehn kleine Brücken (20–50 m) unter der Linie: sechsmal über die Ilse (Blochhauer km 7,9, Blankschmiedebrücke
   9,1, 9,4, 9,8, 11,9, Rote Brücke 12,8, 13,8), Sandtalbach 3,7, Schlüsiebach 13,6, Holtemme 33,9. Das DGM misst das Bachbett (bis 4,9 m
   tiefer); dort gilt eine Gerade zwischen den Brückenenden. Wo sie mehr als 1 m über dem Modell liegt (8 Brücken), steht sie in `D.bridges`
   (geschätzt, schraffiert). Das Oberflächenmodell hilft im Wald nicht (Baumkronen). Danach keine Stufe über 3 m je 10 m außer dem echten
   Abhang zur Ilse am Blochhauer (km 7,87, 4,0 m; Querprofile bestätigen ihn); eine einzelne Senke von 2,7 m auf der Bielsteinchaussee (km 35,2,
   wohl ein Durchlass) nimmt der Median weg. Am Berg sind 1,5–2,3 m je 10 m echtes Gelände.
8. `orte.py`: **Ort** alle 100 m aus den Ortschaften (OSM `admin_level` 9, sonst Gemeinde 8): Wernigerode, Drübeck, Ilsenburg, Schierke (der
   Brocken gehört zu Schierke, Ortsteil von Wernigerode), an Grenzen beide (Schierke / Ilsenburg, Wernigerode / Elbingerode).
9. `stationen.py`: **Verpflegung** laut Seite „Strecken“ (Tabelle mit km und Ausgabezeit): Ilsetal 9 (9:00–10:30), Stempelsbuche 15
   (9:30–11:30), Eiserner Tisch (Tränke) 17 (10:00–12:00), Knochenbrecher 21 (10:15–12:30), Brockenbett 24 (10:30–13:00), Skihütte Hohnekopf
   30 (10:30–13:30), Steinerne Renne 34 (10:45–14:00), Mönchsbuche 37 (11:00–14:15), Kastanienplatz (Tränke) 39 (11:00–14:30). Lage aus dem Ort:
   OSM-Wegweiser Stempelsbuche (km 14,6), Ort Knochenbrecherkurve (20,3), Wegweiser Brockenstraße/Glashüttenweg = Brockenbett (23,1; OSM-Wanderweg
   „Brockenbett – Glashüttenweg – Drei Annen Hohne“ beginnt dort), Hohnepfahl an den Skihütten (30,0), Naturdenkmal Mönchsbuche (36,5), Ort
   Kastanienplatz (38,5); aus dem „V“ der Streckenkarte (±0,2 km): Ilsetal (9,1), Eiserner Tisch (17,3), Steinerne Renne (33,9, am Forsthaus
   Hanneckenbruch). „Tränke“ = nur Getränke (`water`, „Getränke“). Am Eisernen Tisch gibt der Veranstalter bei schlechtem Wetter gelbe
   Schutzjacken für die Brockenpassage aus (Rückgabe am Knochenbrecher); steht im Namen der Marke. Zielverpflegung nicht als Marke.
10. `build.py`: Höhen in cm im 10-m-Raster, Median über 30 m; Wege unter 80 m und Orte unter 300 m dem Vorgänger zugeschlagen. `route.py`
    (lat0/lon0 51,8/10,7, direkt aus `gelegt.json`), `tiles.py` (z12–z15), `tiles_z11.py brocken`, `app.py`, `tiles_rand.py brocken 2`:
    36 Kartenstücke, 2,6 MB.

## Ergebnis

↑ 1146 m / ↓ 1143 m mit 200-m-Fenster (Veranstalter: 1180 Höhenmeter, „über 1000“), ↑ 1202 / ↓ 1198 m mit 50 m, ↑ 1183 / ↓ 1179 m mit 100 m,
↑ 1005 / ↓ 1004 m mit 1 km; wie GPS-Uhren 1203 (ab 0,5 m), 1191 (ab 1 m), 1148 (ab 3 m); Rohdaten ↑ 1256 m. Start 266,4 m (zugleich der
tiefste Punkt), Ziel 270,1 m an der Himmelpforte, höchster Punkt 1140,6 m am Gipfel (km 19,2); **Höhenbereich 874 m**.
Verlauf: 8 km wellig (bis 349 m im Klosterholz, Gegenanstiege bis +54 m), steil hinunter zur Ilse in Ilsenburg (269 m, km 7,9; −11,7 % über
200 m bei km 7,8, die steilste Stelle bergab), dann **11 km ohne Pause bergauf, +869 m** (km 8,0–19,2): Ilsetal im Schnitt 6 %, ab Stempelsbuche
steiler, Hirtenstieg am Eisernen Tisch vorbei mit 15–20 % (**+18,1 % über 200 m bei km 17,6**, +22,6 % über 50 m bei km 16,3) zum Gipfel;
dann 23 km fast nur bergab über Brockenstraße und Glashüttenweg, Gegenanstiege am Ottofelsen (km 32,0–32,9, +59 m) und an der Mönchsbuche
(km 36,0–36,9, +43 m). Je 5 km bergauf/bergab: 105/67, 124/83, 320/0, 472/59, 1/243, 11/222, 64/168, 49/178, 0/123.
**Steiler als 10 % (200-m-Fenster):** bergauf 3,5 km (km 11,8–12,3, 13,9–14,2, 14,9–15,3, 16,2–17,9, 18,4–19,0, 32,3–32,4), bergab 0,8 km;
**steiler als 15 %:** bergauf 1,3 km (km 16,2–17,2, 17,4–17,7, 18,8–18,9), bergab keine.
**Modellzeit** (nur zum Vergleich, am Berg zu optimistisch): Mit 4:00/km im Flachen ergibt das Modell 3:04:24 (das Profil kostet 15:37 min);
bei 2:50:00 kostet es 14:24 min, bei 4:00:00 20:20 min, bei 4:42:00 23:53 min (gemessen mit `pruefen.js` in der App 2.5). Wirklich gelaufen
2026: schnellste 2:53:39, Median 4:42:12 (Ergebnisliste, siehe unten).

Geprüft mit Playwright (Chromium, 393 × 852, Faktor 2, Server auf Port 8793, `pruefen.js` … `pruefen4.js`): keine Konsolenfehler,
`APP_VERSION` 2.5 und Knopf v2.5, Service Worker installiert (42 Einträge im Cache `brk-marathon-profil`), Tipp auf die Version meldet
„Version 2.5 ist aktuell“; alle 36 Kartenstücke passen zu `D.tiles` und `sw.js` und laden; Tabellen bei 320/375/393/430 px ohne Überbreite,
Seite nicht breiter als das Fenster; kein Staffel-Schalter. Laufansicht am Start, km 7,9 (Ilsebrücke), 12,8 (Rote Brücke), 16,8 (Hirtenstieg),
19,2 (Gipfel, Karte und Zahlen), 20,4 (Knochenbrecher), 23,1 (Brockenbett), 32,4 (Ottofelsen), 42,1 (Ziel) und die Kartenübersicht mit
Verpflegung bei km 17,3 angesehen; Kopf, Zuschauer und „Woher die Zahlen kommen“ angesehen. Bilder in `work/shots/`. `kern.py` meldet alle
Apps „gleich“, nur `karten.json` veraltet (neue Strecke, Hauptsitzung).

## Zwischenzeiten

Nicht veröffentlicht: Die Ergebnisliste (davengo) hat je Läufer nur Netto- und Bruttozeit, die Detailansicht Videos von Start und Ziel. Am
Brocken wird zwar der Cut-off (12:00 Uhr) kontrolliert, eine Zeit dort steht nirgends. Nichts gespeichert.

## Offen

- Prüfung am iPhone.
- **Termin 2027** nachtragen, sobald der Verein ihn nennt (hier 9. Oktober 2027 mit „?“), in `app.py` (`D.termine`) und auf der Startseite.
- **Kilometer um km 23–25:** Streckenkarte („25 km“ am Brockenbett) und Verpflegungstabelle („Brockenbett km 24“) liegen 1–1,4 km vor dieser
  Linie, alle anderen Kilometer passen auf 0,3 km. Eine Rückfrage beim Veranstalter würde es klären.
- Die Brücken über die Ilse sind geschätzt (Gerade, ±1 m); die Ortsnamen der unbenannten Waldwege sind beschreibend, keine amtlichen Namen.
- Bei Unwetter am Brocken kann der Veranstalter die Strecke ändern („operativ eine Streckenveränderung“); nicht abgebildet.
- Startseite: Karte fehlt. Eyebrow „Harz-Gebirgslauf · Brocken-Marathon“, Ort **„Brocken“** (wie „Rennsteig“: der Lauf heißt nach dem Berg,
  Start und Ziel in Wernigerode-Hasserode, Wernigerode über `data-such` auffindbar), „Kurs 2026“, `data-termine="2026-10-10 2027-10-09?"`,
  `data-monat="10"`, Termintext „ca. 9. Oktober 2027“, ↑ 1146 m / ↓ 1143 m, Höhe 266–1141 m, `data-such` z. B. „Brockenmarathon Harz-Gebirgslauf
  Wernigerode Hasserode Ilsenburg Harz Nationalpark Sachsen-Anhalt Deutschland“. Mini-Profil: 874 m Höhenbereich bräuchten beim gemeinsamen
  Maßstab (40 m = 56 px) gut 1200 px; also eigener kleinerer Maßstab wie Great Wall und Athen (halber Maßstab ≈ 610 px, Viertel ≈ 310 px).
  README-Tabelle und Liste der Präfixe (`brk-`), `karten.json` (`kern.py --version … --schreiben`). Fuß der Startseite: „Brocken: DGM1
  Sachsen-Anhalt, © GeoBasis-DE / LVermGeo ST, dl-de/by-2-0“. Reihenfolge der deutschen Strecken alphabetisch: Brocken vor Düsseldorf.
  **Teilnehmer:** **616 Marathon-Finisher 2026** (offizielle Ergebnisliste „48. Harz-Gebirgslauf 2026“ bei davengo, verlinkt auf
  https://harz-gebirgslauf.de/ergebnisse-ehrungen.html, Wettbewerb „Brocken-Marathon“: 616 Einträge, alle mit Platz und Nettozeit; die Liste
  führt keine DNF; gezählt mit `ergebnisse.py`, keine Namen gespeichert). 2025: 676 (wie runinternational.eu), 2024: 560. Insgesamt 2026 3951
  Meldungen auf allen Strecken (Veranstalter, 09.10.2026), 2025 3169 Finisher.
