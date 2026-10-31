# Übergabe: Steigungsprofil Mein Freiburg Marathon

Stand 31.10.2026, App-Version **2.4** (erste Fassung, angelegt mit `werkzeuge/kern/kern.py --neu` auf dem gemeinsamen Kern; die
Hauptsitzung zählt die Nummer beim Veröffentlichen hoch).
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/freiburg/.

Die App hat den gemeinsamen Kern aus `hamburg/` und eigene Felder (Texte, `const D`, Speicherschlüssel `fbg-…`, Service-Worker-Cache
`fbg-marathon-profil`, löscht nur Caches mit Präfix `fbg-`; der Präfix war frei, `kern.py --neu` prüft das), ohne eigenes Manifest und
Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Startseite,
README, `version.json` und `karten.json` sind noch nicht angepasst (Hauptsitzung).

**Besonderheiten:** Der Marathon läuft **zweimal dieselbe Runde** (Halbmarathon = eine Runde). Die Linie kommt aus der **Online-Karte
des Veranstalters** (RaceDayMap, als JSON abrufbar). Sie folgt den Straßenmitten und ist je Runde 2,6 % zu lang; die Kilometer sind
deshalb über eine **Ideallinie** verteilt (kürzeste Linie im Band von ±2 m, schneidet jede Ecke; Daten 3). Höhen aus dem **DGM1
Baden-Württemberg** (LGL, Laserscan März 2017, dl-de/by-2-0), alle Brücken aus dem **DOM1** derselben Befliegung gemessen, zwei
Fußgängerunterführungen geschätzt. Mit 197 Höhenmetern (200-m-Fenster) passt das Profil zu den „200 HM“ des Veranstalters. Eine
Marathonstaffel gibt es nicht mehr (2019: 7-14-7-14 km; 2026 nur noch als leerer Wettbewerb bei Race Result). Die Wechselstellen
des **badenova Schülermarathons** (Staffel aus sieben Schülern über eine Runde) standen in der ersten Fassung als Staffel in `D.marks`;
die Hauptsitzung hat sie am 31.10.2026 herausgenommen (`build.py` überspringt sie), weil der Staffel-Schalter sonst eine
Marathonstaffel vortäuscht. Kein Staffel-Schalter in Freiburg.

## Termin und Start

Offizieller Name **„Mein Freiburg Marathon“** (Schreibweise des Veranstalters auch „MEIN FREIBURG MARATHON“), ohne Namenssponsor
(Premium-Sponsoren AOK Südlicher Oberrhein, Sparkasse Freiburg-Nördlicher Breisgau, Bäckerei Heitzmann, Brauerei Ganter, ahg/bhg;
Pressemitteilung vom 07.04.2026). Veranstalter Freiburg Wirtschaft Touristik und Messe GmbH & Co. KG (FWTM) mit dem Badischen
Leichtathletik-Verband. Seite https://mein-freiburgmarathon.de/ (`mein-freiburg-marathon.de` hat ein ungültiges Zertifikat,
`www.mein-freiburgmarathon.de` leitet um). Nächste Austragung, der 22., am **Sonntag, 4. April 2027** (Startseite „Save the Date
4. April 2027“, Seite „Marathon“: „4. April 2027 · Start 9:00 Uhr, 9:10 Uhr · Cut-off-Zeit 5:45 h“, FAQ: „Veranstaltungswochenende
(02-04.04.2027)“; `../dl/seiten/`). Der 21. war am Sonntag, 12. April 2026 (Starterinformation 2026, Pressemitteilung der FWTM vom
12.04.2026). `D.termine` `["2026-04-12", "2027-04-04"]` (2027 bestätigt, ohne „?“), `D.tz` Europe/Berlin, `D.start` = 540 (9:00). Kein
`D.lage`, `D.mauer`, `D.tor`, `D.zielschluss` (`D.tor` zeigt der Kern nur zusammen mit `D.mauer`; der Cut-off steht im Text).

**Start** (`D.wellen`): Starterinformation 2026 (`../dl/pdf/Startinfo-2026-web.pdf`): „Marathon 09:00 Uhr / 09:10 Uhr … Aufteilung in
zwei Startblöcke mit einem Abstand von 10 Minuten“, „Die Einteilung der Startblöcke orientiert sich an der angegebenen Finisher-Zeit“,
Start „auf dem Freigelände der Messe Freiburg“. Für 2027 nennt die Seite „Marathon“ wieder 9:00 und 9:10 Uhr. In der App zwei Knöpfe
„1. Block · 9:00 nach Zielzeit“ und „2. Block · 9:10 nach Zielzeit“. **Zeitlimit** 5:45 h; **Cut-off** (FAQ „Zeitbegrenzung“): „Wer die
erste Runde nicht innerhalb von 2:45 Std. (bis ca. 12:00 Uhr) beendet, wird nicht auf die zweite Runde gelassen, sondern ins Ziel
umgeleitet.“ Halbmarathon 10:30 Uhr in vier Blöcken (A–D, je 15 min), Schülermarathon 11:00/11:15, AOK-Gesundheitslauf (10 km, kürzt
ab) 9:40/9:50. Steht im Text unter „Deine Startzeit“.

**Halbmarathon-Marke** bei 21 098 m = Beginn der zweiten Runde (Race Result misst den Marathon bei 1, 5, 10, 15, „21,1“, „22,1“,
„26,1“, „31,1“, „36,1“ km und im Ziel, also an denselben Stellen der Runde; der Halbmarathon läuft genau die Runde, Linie in der
RaceDayMap identisch).

**Start und Ziel:** beide auf dem Neuen Messplatz (Freigelände der Messe); Start am Westrand (Anfang der Linie), Ziel 200 m weiter
östlich (Ende der Linie). Wie der Marathon nach der ersten Runde in die zweite geführt wird, zeigt kein Plan (2019: „Der Zieleinlauf
befindet sich auf dem Messegelände beziehungsweise für die Marathonläufer_innen geht es hier in die zweite Runde“); `strecke.py` biegt
am Punkt der Linie, der dem Start am nächsten liegt (Südrand des Platzes, 124 m vor dem Ziel), gerade über den Platz zum Start ab (133 m).

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Reihenfolge: `parse.py`, `osm.py`, `georef.py` (nur Abgleich), `ideal_w.py 2` (mit `ideal.py`), `strecke.py`, `strassen.py`, `dgm.py`
(mit `lgl.py`), `deck.py`, `clean.py`, `orte.py`, `stationen.py`, `build.py`, `route.py`, `tiles.py`, dann aus `werkzeuge/`:
`tiles_z11.py freiburg`, `freiburg/work/app.py` (beim ersten Mal über `kern.py --neu freiburg work/felder.json`, danach ersetzt es nur die
Felder und lässt Kartenbilder und `D.tiles` stehen), `tiles_rand.py freiburg 2`. Nur Abgleich/Ausgabe: `marken.py`, `auswertung.py`,
`ergebnisse.py` (Finisher zählen), `karte.py` (Prüfbilder `shots/_*.png`), `rdm_abruf.js` (RaceDayMap im Browser abrufen). Prüfen:
`pruefen.js` … `pruefen4.js` (Server auf Port 8793, `NODE_PATH=/opt/node-tools/node_modules node pruefen.js`).

1. **Strecke** (`parse.py`): Die Seite „Marathon“ (https://mein-freiburgmarathon.de/lauf/marathon/) bettet nach Zustimmung zu Cookies
   `https://app.racedaymap.com/2027-marathon` ein (Dienst racemaps.se). Die Daten liefert ohne Anmeldung
   `https://app.racedaymap.com/api/map/2027-marathon` (`../dl/racedaymap/api_2027-marathon.json`, geändert 18.08.2026): Linien
   „Marathon“, „Halbmarathon“, „Badenova Schülermarathon“ identisch, je **eine Runde**, 396 Punkte (Abstand im Median 34,5 m, gerade
   Stücke bis 610 m), **21 654,3 m**; dazu Wasser-, Verpflegungs- und Wechselstellen. Die Linie folgt den OSM-Wegen (im Median 0,9 m
   daneben, 90 % bis 1,8 m, höchstens 8,8 m). Die Karte „2027“ der Programmseite (`api/map/2027`) hat dieselbe Runde, dazu
   AOK-Gesundheitslauf, Mini-Marathon und 39 Bands, aber offenbar unfertige Verpflegungspunkte (nicht genutzt). Eine GPX-Datei gibt es
   nicht. **Kurs:** Die Karte heißt „2027“, zeigt aber den Kurs 2026; der Veranstalter schreibt „Die genaue Streckenführung für 2027 wird
   zu einem späteren Zeitpunkt bekannt gegeben“. Eyebrow daher „Kurs 2026“.
   **Gegenprobe Streckenplan 2026** (`georef.py`): Anwohnerinformation 2026 (`../dl/pdf/Druck_Marathon_Anwohnerinformation_2026.pdf`,
   Seite 2, Rasterbild 3570 × 3079 px, `pdfimages` → `../dl/render/awkarte-000.jpg`; dieselbe Karte als `MFM_Streckenplan_20263.png`
   auf der Seite „Läuferinformation 2026“): blaue Linienpixel affin auf die RaceDayMap-Linie gelegt (1,70 m/px), Linie der RaceDayMap
   im Median 7,4 m neben der Planlinie, 90 % bis 13 m; gleicher Weg überall (Bild `../dl/render/plan_mit_rdm.jpg`). Die Reihenfolge der
   Straßen deckt sich mit der Sperrliste der Anwohnerinformation.
2. `osm.py`: OSM-API in 83 Rechtecken zu 0,005° höchstens 150 m neben der Runde, eine Abfrage je Sekunde, keine Fehler →
   `../dl/osm_netz.json` (15 506 Wege).
3. **Kilometer** (`ideal.py`, `ideal_w.py`, `strecke.py`, `common.py`): Die Runde ist 556 m (2,6 %) länger als 21 097,5 m. Ursache sind
   die vielen rechtwinkligen Ecken (Wiehre, Altstadt, Stühlinger, Parkwege): Die Linie läuft über die Straßenmitten, vermessen wird die
   kürzeste Linie. `ideal.py` spannt eine Schnur in einem Band von ±w m um die Linie (Punkte alle 2 m, 2500 Runden Glätten und Zurücksetzen
   ins Band). w = 2 m ergibt **21 090,7 m** (w = 3 m 20 932,7, w = 4 m 20 789,2), also fast genau die Runde; gestreckt um 1,0003. Jeder
   Linienmeter bekommt die Länge der Ideallinie bis dorthin. Ergebnis: fast gleichmäßig (höchstens 30 m Unterschied zur gleichmäßigen
   Streckung). Runde 1 samt Rückweg über den Platz und Runde 2 je auf 21 097,5 m. Die gezeichnete Linie (`strecke2026.json`, 43 318 m)
   bleibt für Karte und Lage.
   `marken.py`: Die Kilometerkästen des Plans (17 von 20 erkannt) liegen dagegen bis km 17 im Median 130 m **früher** (−74 bis −333 m),
   km 19 286 m später, km 20 passt (+6 m). Die Kästen stehen 85–115 m neben der Linie, ihr Lot ist unsicher; ein Muster, das sich mit der
   Linie erklären ließe, fand ich nicht. Die Verpflegung der RaceDayMap passt zur Starterinformation („KM 5 | KM 10 | KM 15“, Wasser
   „KM 17,5“): App 5,1 / 10,2 / 14,8 / 17,2 km. **Genauigkeit der Kilometer etwa ±0,3 km**, einzeln nicht belegt.
4. `strassen.py` (Kopie Hannover): je 10 m der nächste OSM-Weg bis 20 m mit höchstens 35° Richtungsabweichung, Hauptstraßen bevorzugt;
   Tunnel von Bundes- und Hauptstraßen zählen nicht (die B 31 im Tunnel unter der Schützenallee gewann sonst). Wege ohne Namen benennt
   `build.py` nach der Lage (`ERSATZ`): Neuer Messplatz, Seepark, Radweg an der Emma-Herwegh-Straße (Sperrliste: „Fahrradweg parallel zur
   Emma-Herwegh-Straße“), Radweg an der Dreisam (Sperrliste: „FR1 – Radweg“), Dietenbachpark („Verschiedene Wege im Dietenbachpark“),
   Weg am Dorfbach, Andlawstraße (Radweg davor), Alter Messplatz („Vorplatz“), Hirzbergstraße, Wiwilíbrücke.
5. `dgm.py`, `lgl.py`: **DGM1 Baden-Württemberg** (LGL, Open GeoData, https://opengeodata.lgl-bw.de/). Kacheln 2 × 2 km als ZIP offen
   unter `https://opengeodata.lgl-bw.de/data/dgm/dgm1_32_<E>_<N>_2_bw.zip` bzw. `…/data/dom1/dom1_32_<E>_<N>_2_bw.zip` (E ungerade, N gerade,
   km; Muster aus der Produktliste des Portals `assets/config/local/odp-products.json`), je vier 1-km-Kacheln, DGM als XYZ-Text, DOM als
   GeoTIFF, EPSG:25832, Höhen NHN (DHHN2016, GCG2016). 10 ZIPs je Modell (≈ 13 MB), einmal als `.npy` abgelegt (`../dl/*/npy/`, zusammen
   rund 0,9 GB in `../dl`). Metadaten je Kachel (`../dl/dgm1/meta.json`): Aktualität **23.03.2017** (Laserbefliegung) für alle, Genauigkeit
   0,15 m. Bilinear alle 10 Linienmeter, 4333 Punkte, alle mit Wert.
   **Lizenz:** LGL-Seite „Open GeoData“ (https://www.lgl-bw.de/Produkte/Open-Data/, `../dl/lgl/`), Abschnitt „Rechtliches“: „Die offenen
   Geobasisdaten und Geodatendienste der Vermessungsverwaltung Baden-Württemberg können unter den Bedingungen der Datenlizenz Deutschland -
   Namensnennung - Version 2.0 … unentgeltlich genutzt werden. Die Namensnennung hat in folgender Weise zu erfolgen: ‚Datenquelle: LGL,
   www.lgl-bw.de, dl-de/by-2-0‘.“ Steht so im Untertitel und unter „Woher die Zahlen kommen“ (die Lizenz-PDF liegt in jedem ZIP).
6. `deck.py`, `clean.py`: **Brücken und Unterführungen.**
   - **Brücken aus dem DOM1** (gleiche Befliegung, Quelle und Lizenz): je 10-m-Punkt der OSM-Brücken 25-%-Quantil der 5 × 5 DOM-Werte,
     übernommen, wo es über dem DGM und höchstens 3 m über den Brückenenden liegt; einzelne Spitzen (Leuchte, Fahrzeug) auf den höheren
     Nachbarn gekappt; auf schmalen Stegen, wo die Linie das Deck verfehlt, nicht unter der Geraden zwischen den Enden. Runde 1:
     Betzenhauser Brücke km 3,73 (DGM 235,1 → 239,4 m), Betzenhauser Steg km 3,97–4,02 (237,7 → 245,2 m), Binzengrün km 5,74 (242,3 → 245,3),
     Steg über die Güterumgehungsbahn km 6,59 (251,6 → 257,5; Rampen davor und danach im DGM), Uffhauser Straße über Güterumgehungsbahn und
     Guildfordallee km 7,98–8,01 (245,7 → 252,6), Oberaubrücke (Fabrikstraße) über die Dreisam km 15,13–15,16 (279,3 → 284,4),
     **Wiwilíbrücke** über die Gleise am Hauptbahnhof km 17,44–17,60 (266,7 → bis 275,4, gewölbt 3 m über den Rampen), Kaiserstuhlstraße
     über die Güterumgehungsbahn km 20,77–20,85 (250,5 → 257,2). Gemessen, nicht schraffiert.
   - **Unterführungen, geschätzt** (`D.bridges`, schraffiert): OSM-Wege `tunnel=yes`, `layer` < 0 höchstens 6 m neben der Linie, wo das
     DGM einen Buckel über 1,5 m zeigt (es misst die Straße darüber): **Unterführung Sundgauallee** km 3,01–3,09 (Gerade 234,4 → 232,5 m;
     Modell bis 235,9) und **Unterführung Schwarzwaldstraße** an der Musikhochschule km 13,96–14,04 (292,2 → 291,3 m; Modell bis 295,4),
     in Runde 2 km 24,10–24,19 und 35,07–35,15. Beide Straßen fehlen in der Sperrliste der Anwohnerinformation, das passt. Die Strecke
     unter den Gleisen an der Mathildenstraße (km 18,7) misst das DGM ohne Buckel.
   - **Runde 2 = Runde 1:** Die bereinigten Höhen von Runde 1 gelten an derselben Stelle der Runde auch in Runde 2 (Unterschied zur eigenen
     Messung im Mittel 0,02 m, höchstens 1,9 m am Betzenhauser Steg); nur die letzten 124 m ins Ziel sind eigens gemessen.
   Danach keine Stufe über 1,0 m je 10 m.
7. `orte.py`: **Stadtteil** alle 100 m aus den Freiburger Stadtteilen (OSM `admin_level` 10, 16 Flächen über die OSM-API, `../dl/orte/`),
   je 40 m links und rechts, bei zwei Stadtteilen „links / rechts“; „Sankt Georgen“ heißt wie bei der Stadt „St. Georgen“. Folge je Runde:
   Brühl, Mooswald, Betzenhausen, Weingarten, Haslach, St. Georgen, Haslach, Wiehre, Oberau, Altstadt, Stühlinger, Brühl (Kandelstraße:
   Brühl / Herdern). Die Stadtbezirke (`admin_level` 11) sind Verwaltung.
8. `stationen.py`: **Verpflegung und Wechselstellen** aus der RaceDayMap, je Runde einmal; Inhalt laut Starterinformation 2026: „ca. alle
   2,5km im Wechsel Verpflegungs- und Wasserstellen … An den Verpflegungsstellen (KM 5 | KM 10 | KM 15 | KM 21) werden neben Wasser, Bananen
   auch isotonische Getränke … angeboten. Bei KM 15 gibt es zudem Gele. Bei KM 17,5 … alkoholfreies Bier und Weizen von GANTER und Cola“;
   Eigenverpflegung an den Verpflegungsstellen. Die Verpflegung bei km 21 fehlt in der RaceDayMap; im Plan steht sie neben dem Start
   (Symbol bei Bildpunkt 1950/860 auf die Linie gelotet, 117 m daneben → km 21,0 und 42,1). In der App (Runde 1, Runde 2 + 21,1 km):
   Wasser km 2,8 Husserlstraße, 7,7 Uffhauser Straße, 12,4 Urachstraße, 17,2 Wilhelmstraße (Ganter); Verpflegung km 5,1 Dietenbachpark,
   10,2 Langemarckstraße, 14,8 Otto-Wels-Straße (mit Gelen), 21,0 Messplatz. Wechselstellen A–F des Schülermarathons (Namen laut seiner
   Starterinformation): A km 2,9 Husserlstraße / Wilhelm-von-Möllendorff-Straße, B 6,0 Unterer Mühlenweg / Gilgenmatten, C 8,7
   „Wiehre-Stadion / Wiesentalstraße“, D 12,3 Peter-Sprung-Straße / Dreikönigstraße, E 15,1 Otto-Wels-Straße / Fabrikstraße, F 18,6
   Kreuzstraße / Mathildenstraße. 29 Marken mit Halbmarathon. **Lage etwa ±0,2 km** (dazu die Unsicherheit der Kilometer).
   Nicht übernommen: Bands (34–39), Toiletten, Spendentor am Platz der Alten Synagoge.
9. `build.py`: Höhen in cm im 10-m-Raster, Median über 30 m; Straßenstücke unter 80 m und Stadtteile unter 300 m dem Vorgänger
   zugeschlagen. `route.py` (lat0/lon0 48,0/7,8), `tiles.py` (z12–z15), `tiles_z11.py freiburg`, `app.py`, `tiles_rand.py freiburg 2`:
   17 Kartenstücke, 2,2 MB.

## Ergebnis

↑ 197 m / ↓ 199 m mit 200-m-Fenster, ↑ 242 / ↓ 244 m mit 50 m, ↑ 224 / ↓ 226 m mit 100 m, ↑ 123 / ↓ 123 m mit 1 km; wie GPS-Uhren 225
(ab 0,5 m), 209 (ab 1 m), 164 (ab 3 m); Rohdaten ↑ 366 m (DGM Punkt für Punkt, mit den Senken unter den Brücken und den Buckeln über den
Unterführungen). Start 251,5 m, Ziel 249,6 m auf dem Neuen Messplatz, tiefster Punkt 232,7 m an der Unterführung der Sundgauallee
(km 3,08, geschätzt; gemessen 232,5 m am Ausgang), höchster 294,0 m am Alten Messplatz (km 13,81); **Höhenbereich 61 m**.
Verlauf je Runde: vom Messplatz über Mooswald und den Seepark 17 m hinunter zur Dreisam, über den Betzenhauser Steg in den Dietenbachpark,
durch Weingarten, über die Rampe zum Steg über die Güterumgehungsbahn (+4,3 % über 200 m bei km 6,49, die steilste Stelle über 200 m)
nach Haslach und St. Georgen (252 m), dann gleichmäßig im Zickzack durch die Wiehre hinauf (km 9–14: 255 → 294 m, im Schnitt 0,7 %),
über Oberau, das Schwabentor und die Altstadt hinunter, über die Wiwilíbrücke (+6,8 % über 50 m bei km 17,42, −4,7 % über 200 m bei
km 4,15 ist die steilste Stelle bergab) und durch Stühlinger und Brühl zurück zur Messe.
**Modellzeit:** Mit 4:00/km im Flachen ergibt das Modell **2:50:42** (das Profil kostet 116 s); **bei 2:50:00 kostet es 115 s, bei 4:00:00
162 s** (Flach-Pace 3:59,0 bzw. 5:37,4 /km; gemessen mit `pruefen.js` in der App 2.4). Zum Vergleich bei 4:00/km im Flachen: Düsseldorf
37 s, Köln 48 s, München 48 s (laut ihren Übergaben).

Geprüft mit Playwright (Chromium, 393 × 852, Faktor 2, Server auf Port 8793, `pruefen.js` … `pruefen4.js`): keine Konsolenfehler,
`APP_VERSION` 2.4 und Knopf v2.4, Service Worker installiert (23 Einträge im Cache `fbg-marathon-profil`), Tipp auf die Version meldet
„Version 2.4 ist aktuell“; alle 17 Kartenstücke passen zu `D.tiles` und `sw.js` und laden; Tabellen bei 320/375/393/430 px ohne Überbreite,
Seite nicht breiter als das Fenster; Staffel-Einstellung sichtbar. Laufansicht am Start, km 3,05 (Sundgauallee), 6,5 (Steg Güterumgehungsbahn),
12,5 (Wiehre), 13,8 (höchster Punkt), 14,0 (Unterführung Schwarzwaldstraße, schraffiert), 17,5 (Wiwilíbrücke), 21,05 (Rundenwechsel),
38,6, 42,1 (Ziel) und die Kartenübersicht mit Verpflegung bei km 17 angesehen; Kopf, Zuschauer-Tabelle und „Woher die Zahlen kommen“
angesehen. Bilder in `work/shots/` (Prüfbilder der Aufbereitung mit `_` davor). `kern.py` meldet alle Apps „gleich“, nur
`karten.json` veraltet (neue Strecke, Hauptsitzung).

## Offen

- Prüfung am iPhone.
- **Kurs 2027:** Der Veranstalter gibt die Strecke 2027 später bekannt. Kommt sie, `api/map/2027-marathon` neu laden (Datei in `parse.py`)
  und die Kette laufen lassen; prüfen, ob die Linie dann zwei Runden oder weiter eine zeigt, und den Rundenwechsel am Messplatz.
- Kilometer: über die Ideallinie verteilt, ±0,3 km; die Kilometerkästen des Plans liegen bis km 17 bis 0,3 km früher (Daten 3). Ein
  Vermessungsprotokoll oder eine GPX-Datei des Veranstalters würde das klären.
- Rundenwechsel des Marathons auf dem Messplatz und die Lage der Startlinie nicht belegt (je ≈ 130 m, eben).
- Wechselstellen: nur der Schülermarathon (sieben Schüler über die Runde, startet um 11:00/11:15, wenn die Marathonläufer in der zweiten
  Runde sind); bei Bedarf aus `D.marks` nehmen, dann entfällt der Staffel-Schalter.
- Startseite: Karte fehlt. Eyebrow „Mein Freiburg Marathon“, Stadt „Freiburg“, „Kurs 2026“, `data-termine="2026-04-12 2027-04-04"`,
  `data-monat="4"`, Termintext „So., 4. April 2027“, ↑ 197 m / ↓ 199 m, Höhe 233–294 m, `data-such` z. B. „Freiburg im Breisgau
  Baden-Württemberg Deutschland Breisgau Schwarzwald Messe Dreisam Wiwilibrücke Mein Freiburg Marathon“. Mini-Profil: 61 m Höhenbereich
  braucht beim gemeinsamen Maßstab (40 m = 56 px) etwa 86 px statt 64 (eigene Klasse wie `.spark.wien`). README-Tabelle und Liste der
  Präfixe (`fbg-`), `karten.json` (`kern.py --version … --schreiben`). Fuß der Startseite: „Freiburg: DGM1 und DOM1 Baden-Württemberg,
  Datenquelle: LGL, www.lgl-bw.de, dl-de/by-2-0“.
  **Teilnehmer 2026:** **1 570 Marathon-Finisher** (offizielle Ergebnisliste „MEIN FREIBURG MARATHON 2026“, Race Result Ereignis 351479,
  eingebunden auf https://mein-freiburgmarathon.de/ergebnisse/, Wettbewerb „Marathon“, Liste „Gesamtergebnisliste“: 1 597 Einträge, davon
  1 570 mit Platz und Zeit, 17 DSQ, 8 DNF, 2 DNS; gezählt mit `ergebnisse.py`, keine Namen gespeichert). runinternational.eu nannte
  1 560. 2025: 1 477 (Ereignis 298890), 2024: 1 124 (251383). Insgesamt 2026 rund 13 200 Läufer auf allen Strecken (FWTM).
- Termine 2028 ff.: jährlich nachtragen (Frühjahr; 2025 am 6. April, 2026 am 12. April, 2027 am 4. April).
