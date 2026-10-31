# Übergabe: Steigungsprofil Kleine Zeitung Graz Marathon

Stand 31.10.2026, App-Version **2.6** (erste Fassung, angelegt mit `werkzeuge/kern/kern.py --neu` auf dem gemeinsamen Kern; die
Hauptsitzung zählt die Nummer beim Veröffentlichen hoch).
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/graz/.

Die App hat den gemeinsamen Kern aus `hamburg/` und eigene Felder (Texte, `const D`, Speicherschlüssel `grz-…`, Service-Worker-Cache
`grz-marathon-profil`, löscht nur Caches mit Präfix `grz-`; der Präfix war frei, `kern.py --neu` prüft das), ohne eigenes Manifest und
Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Startseite,
README, `version.json` und `karten.json` sind noch nicht angepasst (Hauptsitzung).

**Besonderheiten:** Der Marathon läuft **zweimal dieselbe Runde** (Halbmarathon = eine Runde), mit zwei Wenden (Süd in der
Conrad-von-Hötzendorf-Straße, Nord bei Weinzödl). Die Linie kommt aus der **Garmin-Connect-Strecke**, die der Veranstalter auf seinen
Seiten einbettet (ohne Anmeldung als Seitentext abrufbar). Höhen aus dem **Laser-Geländemodell des BEV** (ALS DTM 1 m, Befliegung 2024),
nur die gebrauchten 512-m-Teilkacheln per HTTP-Range über das neue, **wiederverwendbare `work/bev.py`** (für Salzburg gedacht, siehe
unten); Brücken aus dem **ALS DSM** derselben Befliegung. Es gibt einen **Hyundai Staffelmarathon** auf derselben Strecke (vier
Läufer, drei Übergaben in `D.marks`, der Kern zeigt damit den Staffel-Schalter). Die Strecke ist flach: 19 m Höhenbereich,
↑ 73 / ↓ 73 m mit 200-m-Fenster.

## Termin und Start

Veranstalter MJK Sportmarketing GmbH („Graz Marathon – ein Produkt der MJK Sportmarketing GmbH“), Seite https://www.grazmarathon.at/.
Offizieller Name **„Kleine Zeitung Graz Marathon“** (Startseite, Seiten „Ergebnisse“ und „FAQ“; der Bewerb selbst heißt „Kleine Zeitung
Marathon“, dazu Hervis Halbmarathon, Hyundai Staffelmarathon, Energie Steiermark Viertelmarathon), Namenssponsor die Tageszeitung
Kleine Zeitung. Der **33. Graz Marathon** war am 9.–11. Oktober 2026, der Marathon am **Sonntag, 11. Oktober 2026** (Pressekonferenz vom
07.10.2026 „Der Startschuss für den 33ten Graz Marathon“, Straßensperren 2026, News „Graz Marathon Tag 2“ vom 11.10.2026; 15 000
Anmeldungen für alle Bewerbe). Nächste Austragung **8.–10. Oktober 2027**, Marathon am **Sonntag, 10. Oktober 2027** (Startseite
„08.-10. OKTOBER 2027“, Seite „Marathon“: „Datum: Sonntag, 10. Oktober 2027 Startzeit: 10.00 Uhr (Änderungen vorbehalten) Zielschluss:
16.00 Uhr Distanz: 42,195 km (AIMS Vermessen)“, News „Anmeldung 2027 geöffnet“ vom 29.10.2026; Anmeldeseite time2win.at/event/1152).
`D.termine` `["2026-10-11", "2027-10-10"]` (2027 bestätigt, ohne „?“), `D.tz` Europe/Vienna, `D.ort` „Graz“, `D.ortKurz` „ Graz“ (nach
der Zeitzone hieße es sonst „Vienna“), `D.start` = 600 (10:00). Kein `D.lage`, `D.mauer`, `D.tor`, `D.zielschluss`.

**Start** (`D.wellen`): Seite „Startblöcke Aufstellung“ (gleichlautend auf den Seiten „Marathon“ und „Staffelmarathon“ für 2027):
„Startblock 0 – Start 09:30 Uhr: Viertelmarathon, Startblock 1 – Start 10:00 Uhr: Elite, Marathon, Staffelmarathon, Halbmarathon,
Startblock 2 – Start 10:05 Uhr: Marathon, Staffelmarathon, Halbmarathon, Startblock 3 – 10:10 Uhr: Halbmarathon, Startblock 4 – 10:15 Uhr:
Halbmarathon“; eingereiht wird „gemäß Kennzeichnung auf der Startnummer“ (FAQ), Kriterien nennt der Veranstalter nicht. In der App zwei
Knöpfe „Block 1 · 10:00 mit Elite“ und „Block 2 · 10:05“. **Zielschluss** 16:00 Uhr für alle Bewerbe (Halbmarathon 14:00 Uhr), steht im
Text. Pacemaker 3:15 bis 4:30 (Seite „Pacemaker“).

**Start und Ziel** vor der Oper Graz am Opernring (Lageplan „Start-/Zielbereich“, `../dl/img/Eventgelaende_Grafik_GM26.png`: eine Marke
„Start/Ziel“, gestartet wird nach Südwesten, der Zieleinlauf kommt in einer abgetrennten Spur von Südwesten zurück). Die Garmin-Linie
beginnt am Opernring auf der Höhe der Burggasse und endet 34 m davor in der Zielspur. Wie die Marathonläufer nach der ersten Runde vor
der Oper wenden, zeigt kein Plan; `strecke.py` führt die Linie vom Ende der Runde gerade zurück zum Anfang (34 m).

**Halbmarathon-Marke** bei 21 098 m = Beginn der zweiten Runde. **Staffel** (Seite „Staffelmarathon“): „Start (Grazer Oper) bis
Staffelübergabe 1 (Korösistraße Ecke Wickenburggasse) = ca. 10km, … bis Staffelübergabe 2 (Schlossberghotel) = ca. 9,1km, … bis
Staffelübergabe 3 (Korösistraße Ecke Wickenburggasse) = ca. 12 km, … bis Ziel (Grazer Oper) = 11,1km“; Übersichtsgrafik: „10 km
Körösistraße“, „19,3 km Schloßbergplatz“, „31,1 km Körösistraße“. In der App (stationen.py): Übergabe 1 km 9,77 (Anfang der
Körösistraße nach der Keplerbrücke und Wickenburggasse), 2 km 19,02 (Kaiser-Franz-Josef-Kai am Schlossberghotel), 3 km 30,88.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Reihenfolge: `parse.py`, `osm.py`, `ideal_w.py 0.5 1 1.5 2` (mit `ideal.py`; Wahl in `ideal_wahl.json`), `strecke.py`, `strassen.py`,
`dgm.py` (mit `bev.py`), `deck.py`, `clean.py`, `orte.py`, `stationen.py` (mit `nominatim.py`), `build.py`, `route.py`, `tiles.py`, dann aus
`werkzeuge/`: `tiles_z11.py graz`, `graz/work/app.py` (beim ersten Mal über `kern.py --neu graz work/felder.json`, danach ersetzt es nur
die Felder und lässt Kartenbilder und `D.tiles` stehen), `tiles_rand.py graz 2`. Hilfen: `karte.py` (Prüfbilder `shots/_*.png`), `text.py`
(Text einer gespeicherten Seite). Prüfen: `pruefen.js` … `pruefen4.js` (Server auf Port 8791, `NODE_PATH=/opt/node-tools/node_modules
node pruefen.js`).

1. **Strecke** (`parse.py`): Die Seiten „Marathon“ und „Halbmarathon“ (https://www.grazmarathon.at/bewerbe/marathon/) betten unter
   „Strecke 2027“ die Garmin-Strecke **265629398** ein, „Graz Halb- und Marathon 2026 (21km Schleife) NEU“ (angelegt 01.05.2024,
   geändert 21.09.2026). Die Einbettung `https://connect.garmin.com/modern/course/embed/265629398` liefert ohne Anmeldung die ganze
   Strecke im Seitentext (Next.js-Daten, `../dl/garmin/`): 2548 Punkte mit Garmin-Höhen, **21 337 m**, eine Runde. Der Link „Höhenmeter:
   Siehe Garmin Connect“ führt zu einer alten Strecke („Graz Marathon 2018 Final“, 13489537, nicht genutzt). Eine GPX-Datei gibt es nicht.
   Die Linie folgt den OSM-Straßen (im Median 1,5 m daneben, 99 % bis 7 m; die längsten geraden Stücke bis 577 m sind gerade Straßen).
   **Bereinigt:** vier kurze Zacken, in denen die Linie über eine Kreuzung hinaus- und auf derselben Spur zurückläuft (Rest des
   Routenplaners: Joanneumring/Neutorgasse 24 m, Wielandgasse 8,5 m, Schönaugürtel/Conrad-von-Hötzendorf-Straße 33,5 m,
   Schönaugürtel/Schönaugasse 30 m Linie), genau am Fuß ausgeschnitten → **21 244 m**. Die Wende Nord (Hin- und Rückweg auf derselben
   Fahrbahn der Weinzöttlstraße) bleibt. Der Kurs 2026 deckt sich mit der Karte der Anrainerinformation 2026
   (`../dl/pdf/0001-2601-GM-Anrainer-Infofolder_A4-WEB.pdf`, Seite 3) und mit den Ortsmarken der Übersichtsgrafik 2025. **Kurs-Jahr:**
   Die Strecke heißt „2026“ und steht unter „Strecke 2027“; eine eigene Strecke 2027 gibt es nicht. Eyebrow daher „Kurs 2026“.
2. `osm.py` (Kopie Freiburg): OSM-API in 53 Rechtecken zu 0,005° höchstens 150 m neben der Runde, eine Abfrage je Sekunde, bei 509 gewartet
   und wiederholt (kam mehrmals, andere Sitzungen fragten gleichzeitig ab) → `../dl/osm_netz.json` (14 532 Wege).
3. **Kilometer** (`ideal.py`, `ideal_w.py`, `strecke.py`, `common.py`, wie Freiburg): Die bereinigte Runde ist 147 m (0,7 %) länger als
   21 097,5 m (Linie auf den Straßenmitten, Ecken). `ideal.py` spannt eine Schnur im Band ±w um die Linie; anders als in Freiburg
   stückweise mit festen Wendenspitzen (sonst zieht die Schnur die Wende Nord, wo Hin- und Rückweg auf derselben Linie liegen, bis 80 m
   zurück). w = 0,5 / 1 / 1,5 / 2 m ergibt 21 131 / **21 093** / 21 057 / 21 023 m; gewählt **w = 1 m**. Runde 1 samt 34 m zurück zum
   Start und Runde 2 je auf 21 097,5 m gestreckt (Faktoren 0,99862 und 1,00023). Ergebnis fast gleichmäßig (km 10 bei Linienmeter 10 103,
   gleichmäßig wäre 10 078). Gezeichnete Marathonlinie 42 522 m (`strecke2026.json`). **Genauigkeit der Kilometer etwa ±0,1 km**;
   Gegenprobe Staffelübergaben (Veranstalter ca. 10 / 19,1 / 31,1 km, Grafik 10 / 19,3 / 31,1): App 9,77 / 19,02 / 30,88.
4. `strassen.py` (Kopie Freiburg, UTM 33N): je 10 m der nächste OSM-Weg bis 20 m mit höchstens 35° Richtungsabweichung, Hauptstraßen
   bevorzugt; Straßentunnel zählen nicht (Kalvarien- und Grabengürtel laufen im Tunnel unter der Körösistraße). `build.py` nimmt kurze
   Querstraßen (Ella-Flesch-Platz, Evangelimanngasse, Weldenstraße, Sporgasse, Neue-Welt-Gasse, Zweiglgasse) heraus; Stücke unter 80 m
   übernehmen den Namen davor. Die Murbrücke von der Grazbachgasse zum Grieskai heißt in OSM seit 02.02.2026 **Alfred-Stingl-Brücke**
   (`old_name` Augartenbrücke; die Liste der Brückensperren 2026 nennt noch „Augartenbrücke“).
5. **`bev.py` – BEV-Abruf, wiederverwendbar** (auch für Salzburg): Laser-Höhenmodelle des BEV, **ALS DTM** und **ALS DSM**, Höhenraster
   1 m, CC BY 4.0, Stichtage 15.09.2019, 2021–2025 (ATOM-Feed, `../dl/bev/atom.xml`), Metadaten
   https://data.bev.gv.at/geonetwork/srv/metadata/ec12896e-1ecd-47ad-8d48-44d236e383cc. Dateien
   `https://data.bev.gv.at/download/ALS/<DTM|DSM>/<Stichtag>/ALS_<DTM|DSM>_CRS3035RES50000mN<N>E<E>.tif`: 55 Kacheln von 50 × 50 km
   (ETRS89/LAEA, EPSG 3035, N/E = linke untere Ecke), je 50 001 × 50 001 Zellen float32 (Zellmitte auf ganzen Metern), gekachelt 512 × 512,
   LZW mit Gleitkomma-Prädiktor, kein Wert −9999, **8,0 GB (DTM) bzw. 9,7 GB (DSM)** für Graz; das Verzeichnis selbst ist gesperrt
   (403), die Dateien nicht, HTTP-Range geht. `bev.py` liest über eine Range-Datei (`HttpFile`, Kopie aus `../../wien/work/httpfile.py`)
   mit `tifffile` nur Kopf und Kachelverzeichnis (≈ 150 KB) und dann die gebrauchten Teilkacheln (je ≈ 0,3–1 MB) und legt sie als `.npy`
   in `../dl/bev/<DTM|DSM>_<Stichtag>/` ab (danach ohne Netz). Kein GDAL nötig (in der Umgebung nicht vorhanden).
   Benutzung: `import bev; dtm = bev.Modell("DTM"); h = dtm.hoehe(lon, lat)` (bilinear, Arrays, NaN ohne Wert);
   `bev.Modell("DSM").quantil(lon, lat, r=2, q=25)` (Quantil der Zellen im Umkreis, Fahrbahn auf Brücken); `bev.flugjahr(lon, lat)` →
   `[(Gebiet, Flugjahr)]` aus der Aktualitätsübersicht des Stichtags (Shapefile im ZIP, eigener kleiner Leser); `bev.kachel_id(x, y)`.
   Kommandozeile zum Ausprobieren: `python3 bev.py <lat> <lon>`. Höhen über **EVRF2000** (EPSG 9274), nicht über Adria (in Wien liegen die
   Adria-Höhen der Stadt 0,51 m darüber, siehe Wien-Übergabe). Für Graz: Kachel N2650000 E4700000, 29 Teilkacheln je Modell
   (≈ 3 bzw. 4 min), Flugjahr Steiermark **2024** an Start, Wende Süd und Wende Nord.
6. `dgm.py`: DTM und DSM bilinear je 10 Linienmeter, 4254 Punkte, keiner ohne Wert → `dgm2026_10m.json`.
7. `deck.py`, `clean.py`: **Brücken.** Auf den OSM-Brücken samt 20 m Rand gilt das 25-%-Quantil des DSM im Umkreis von 2 m, wo es über
   dem DTM und höchstens 3 m über den Brückenenden liegt; einzelne Spitzen gekappt, nicht unter der Geraden zwischen den Enden.
   **Alfred-Stingl-Brücke** über die Mur km 5,69–5,76 (DTM 341,1 m im Fluss, Fahrbahn 347,9–349,1 m), **Keplerbrücke** über die Mur km
   9,59–9,66 (DTM 343,6, Fahrbahn 353,0–353,8 m, leicht gewölbt), Grabenstraße über die Straßenbahn km 12,02 (DTM 354,2, Fahrbahn 358,9),
   Weinzöttlstraße über den Andritzbach km 13,16 und 14,85 (Hin- und Rückweg); in Runde 2 dieselben. Gemessen, nicht schraffiert.
   **Geschätzt** (gerade, schraffiert, `D.bridges`): **Grabenstraße auf dem Rückweg** km 15,95–15,99 und 37,07–37,11: Die stadteinwärts
   führende Fahrbahn ist eine Brücke über den Straßenbahntunnel (OSM layer 2), die Linie liegt 11 m neben dem OSM-Weg, DTM und DSM
   messen dort bis 5 m tiefer (Rand des Decks); gerade 358,5 → 358,7 m (die Fahrbahn stadtauswärts misst das DSM mit 358,8–359,0 m).
   **Nur geglättet** (nicht gezeigt): Grieskai am Kopf der Tegetthoffbrücke km 6,35 (ein Punkt 5 m tief, wo Brücke und Widerlager aus
   dem Modell genommen sind) und Grabenstraße über dem verdolten Schöcklbach km 11,89 (ein Punkt 2,3 m tief).
   **Unterführung, gemessen** (das DTM kennt den Boden der Straße): **Lendkai unter der Keplerbrücke** km 7,2 (2,5 m Senke, die steilste
   Stelle der Strecke: +2,0 % über 200 m, +3,9 % über 50 m bei km 7,29). **Runde 2 = Runde 1:** die bereinigten Höhen von Runde 1 gelten an derselben Stelle der Runde auch in Runde 2
   (Unterschied zur eigenen Messung im Mittel 0,02 m; die größten an den geglätteten Stellen). Danach keine Stufe über 1,32 m je 10 m.
8. `orte.py` (Kopie Freiburg): **Stadtbezirk** alle 100 m aus den 17 Grazer Stadtbezirken (OSM `admin_level` 9, 9 Flächen an der
   Strecke über die OSM-API, `../dl/orte/`), je 40 m links und rechts, mit römischer Nummer wie in der Anrainerinformation des
   Veranstalters („XII. Andritz“, „IV. Lend“, „V. Gries“, „I. Innere Stadt“; „Sankt Leonhard“ → „II. St. Leonhard“). Die Katastralgemeinden
   (`admin_level` 10) sind Kataster. Am Kai ist die Mur die Bezirksgrenze; die kurzen Stücke „Lend / Innere Stadt“ fallen in `build.py`
   weg (unter 300 m), der Wechsel Gries → Lend liegt auf dem Straßenwechsel Grieskai → Lendkai. Folge je Runde: I. Innere Stadt,
   VI. Jakomini (auch an der Wende Süd), V. Gries, IV. Lend, III. Geidorf, XII. Andritz (Wende Nord), III. Geidorf, I. Innere Stadt.
9. `stationen.py`: **Labestationen** nach der Übersichtsgrafik „Auf einen Blick – der Graz-Marathon“ (Kleine Zeitung/MJK) auf der Seite
   „Labestationen“ (https://www.grazmarathon.at/laeuferinformation/serviceleistungen/labestationen/, Bild
   `2025-10-10-GM-Hoehenprofil-1.jpg`, im Oktober 2025 hochgeladen und zum Lauf 2026 unverändert auf der Seite): neun Stationen auf einer
   km-Skala mit Wasser, Peeroton Mineralvitamindrink, Cola, Bananen, Erste Hilfe, Eigenverpflegung, Gel, dazu Hotspots (Wende Süd, Styria
   Tower, Kunsthaus, Wiener Straße, Keplerbrücke, Maut Andritz, Wende Nord, Schloßbergplatz, Neutorgasse, Hauptplatz, Eisernes Tor). Die
   Grafik ist schematisch (dieselbe Stelle liegt in den zwei Runden bis 0,4 km verschieden weit vom Start); die Stationen sind deshalb
   zwischen den zwei nächsten Hotspots, deren Lage auf der Linie feststeht (Nominatim, `../dl/nominatim/`, bzw. Wenden und Keplerbrücke),
   linear eingehängt, Paare derselben Station (1/6, 2/7, 3/8, 4/9) auf die mittlere Lage in der Runde gesetzt. **Lage etwa ±0,2 km.**
   In der App: Getränke (Wasser, Peeroton) km 4,0 und 25,1 (Conrad-von-Hötzendorf-Straße am Styria Tower); Labestation km 9,4 und 30,5
   (Keplerstraße, mit Eigenverpflegung), 12,8 und 33,9 (Weinzöttlstraße, mit Gel), 17,4 und 38,5 (Theodor-Körner-Straße), 21,8 (Wielandgasse,
   nur Runde 2, Wasser, Peeroton, Bananen, Eigenverpflegung). **Widersprüche:** Text der Seite: „Peeroton Gel nur auf der Labestation auf
   Kilometer 35!!“ (Grafik: Gel bei km 13 und 34; in der App bei beiden mit Hinweis); „Labestation 2 & 8: Keplerstraße (ca. KM 10 und
   KM 31)“ und „Labestation 6: Radetzkystr. Höhe Pestalozzistr. – Marathon auf zweiter Runde (ca. KM 22)“ – Orte und Kilometer passen
   (km 9,4/30,5 und 21,8 an der Ecke Joanneumring/Radetzkystraße/Wielandgasse), die Nummern nicht zur Grafik (dort 2/7 und 5); in der App
   die Nummern der Grafik. Nicht übernommen: Hotspots, Erste Hilfe als eigene Marken, Ziellabestation.
10. `build.py`: Höhen in cm im 10-m-Raster, Median über 30 m; Straßen unter 80 m und Bezirke unter 300 m dem Vorgänger zugeschlagen,
    Bezirkswechsel auf den nächsten Straßenwechsel bis 150 m. `route.py` (lat0/lon0 47,0/15,4), `tiles.py` (z12–z15), `tiles_z11.py graz`,
    `app.py`, `tiles_rand.py graz 2`: 17 Kartenstücke.

## Ergebnis

↑ 73 m / ↓ 73 m mit 200-m-Fenster (je Runde 36), ↑ 98 / ↓ 99 m mit 50 m, ↑ 87 / ↓ 88 m mit 100 m, ↑ 44 m mit 1 km; wie GPS-Uhren 79
(ab 0,5 m), 64 (ab 1 m), 37 (ab 3 m); Rohdaten ↑ 207 m (DTM Punkt für Punkt, mit der Mur unter den Brücken). Start 353,5 m vor der Oper,
tiefster Punkt **343,4 m** an der Wende Süd (km 3,06 und 24,16), höchster **362,2 m** an der Wende Nord bei Weinzödl (km 14,17 und 35,29),
Ziel 352,9 m; **Höhenbereich 19 m** (Höhen über EVRF2000). Verlauf je Runde: von der Oper 10 m hinunter in den Süden zur Wende in der
Conrad-von-Hötzendorf-Straße, über Neuholdaugasse und die Alfred-Stingl-Brücke an die Mur und an Grieskai und Lendkai flussaufwärts
langsam hinauf (Senke unter der Keplerbrücke), durch Lend und über die Keplerbrücke, die Körösistraße und Grabenstraße gleichmäßig nach
Andritz hinauf (km 10–14: 351 → 362 m, im Schnitt 0,3 %), zurück über Theodor-Körner-Straße und Geidorf an den Kai und durch die
Altstadt (349–350 m an Murgasse, Raubergasse, Hauptplatz) zur Oper. Steilste Stelle über 200 m: +2,0 % am Lendkai nach der Unterführung
(km 7,30), bergab −1,4 % am Start (Opernring).
**Modellzeit:** Mit 4:00/km im Flachen ergibt das Modell **2:49:22** (das Profil kostet 35 s); **bei 2:50:00 kostet es 36 s, bei 4:00:00
50 s** (gemessen mit `pruefen.js` in der App 2.6). Zum Vergleich: Düsseldorf 37 s, Köln 48 s, Freiburg 116 s bei 4:00/km.

**Gegenprobe mit den Garmin-Höhen** der Strecke des Veranstalters (die Seite „Marathon“ verweist für die Höhenmeter auf Garmin Connect):
Korrelation 0,78, Garmin im Median 5,7 m höher, in der Altstadt bis 14,5 m (gröberes Modell mit Häusern); Garmin nennt je Runde 126
Höhenmeter bergauf (runinternational.eu: „109m of ascent“ je Runde, 218 für den Marathon). Das Lasermodell ergibt Punkt für Punkt (nach
den Brücken) 66 m je Runde, mit 200-m-Fenster 36 m.

Geprüft mit Playwright (Chromium, 393 × 852, Faktor 2, Server auf Port 8791, `pruefen.js` … `pruefen4.js`): keine Konsolenfehler,
`APP_VERSION` 2.6 und Knopf v2.6, Service Worker installiert (23 Einträge im Cache `grz-marathon-profil`), Tipp auf die Version meldet
„Version 2.6 ist aktuell“; alle 17 Kartenstücke passen zu `D.tiles` und `sw.js` und laden; Tabellen bei 320/375/393/430 px ohne Überbreite,
Seite nicht breiter als das Fenster; Staffel-Einstellung sichtbar. Laufansicht am Start, km 3,05 (Wende Süd), 5,72 (Alfred-Stingl-Brücke),
7,2 (Lendkai unter der Keplerbrücke), 9,6 (Keplerbrücke), 14,15 (Wende Nord), 15,97 (Grabenstraße, schraffiert), 20,3 (Hauptplatz),
21,05 (Rundenwechsel), 42,1 (Ziel) und die Kartenübersicht mit Labestationen angesehen; Kopf, Zuschauer-Tabelle mit Blöcken und nächstem
Termin 10. Oktober 2027 („Uhrzeiten in Ortszeit Graz“) und „Woher die Zahlen kommen“ angesehen. Bilder in `work/shots/` (Prüfbilder der
Aufbereitung mit `_` davor). `kern.py` meldet alle Apps „gleich“, nur `karten.json` veraltet (neue Strecke, Hauptsitzung).

## Offen

- Prüfung am iPhone.
- **Teilnehmer 2026 nicht nachgezählt:** Die offizielle Ergebnisliste liegt nur bei maxfunsports.com (Seite „Ergebnisse & Urkunden“ →
  https://www.maxfunsports.com/event/2026/graz-marathon-2026; Zeitnehmung Time2Win/MaxFun); der Abruf wird von Cloudflare gesperrt (403
  „Sorry, you have been blocked“, auch für alle Unterseiten), nicht umgangen. runinternational.eu (Seite „Graz Marathon“,
  https://www.runinternational.eu/2011-calendar/october/807) nennt für 42,2 km **1 077 Finisher 2026**, 1 145 (2025), 860 (2024), 708 (2023)
  – unbestätigt. Nachzählen, sobald die Liste erreichbar ist (keine Namen speichern).
- **Kurs 2027:** Die Garmin-Strecke heißt „2026“; kommt eine neue, `parse.py` mit der neuen Kennung laufen lassen (Kette oben).
- Wende der Marathonläufer nach Runde 1 vor der Oper und genaue Lage von Start- und Ziellinie nicht belegt (je ≈ 30 m, eben).
- Labestationen nur aus der schematischen Grafik 2025 (±0,2 km), Gel-Angabe widersprüchlich (Daten 9). Eine Liste mit Kilometern oder
  ein Streckenplan mit Symbolen würde das klären.
- Absolute Höhe: EVRF2000 statt Adria. Für Graz wird meist „353 m“ angegeben (OSM-Knoten „Graz“ ele 353 am Hauptplatz; das DTM misst dort
  350,5 m); den Unterschied EVRF2000/Adria in Graz habe ich nicht geprüft. Für die Steigungen ohne Bedeutung.
- Startseite: Karte fehlt. Eyebrow „Kleine Zeitung Graz Marathon“, Stadt „Graz“, „Kurs 2026“, `data-termine="2026-10-11 2027-10-10"`,
  `data-monat="10"`, Termintext „So., 10. Oktober 2027“, ↑ 73 m / ↓ 73 m, Höhe 343–362 m, `data-land` Österreich, `data-such` z. B. „Graz
  Steiermark Styria Österreich Austria Kleine Zeitung Mur Schlossberg Oper Andritz“. Mini-Profil: 19 m Höhenbereich passt in die Grundhöhe
  64 px (keine eigene Klasse). README-Tabelle und Liste der Präfixe (`grz-`), `karten.json` (`kern.py --version … --schreiben`). Fuß der
  Startseite: „Graz: ALS DTM und ALS DSM des BEV (Bundesamt für Eich- und Vermessungswesen), CC BY 4.0“.
- Termine 2028 ff.: jährlich nachtragen (zweites Oktoberwochenende; 2026 am 11., 2027 am 10. Oktober).
