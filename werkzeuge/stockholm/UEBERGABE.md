# Übergabe: Steigungsprofil adidas Stockholm Marathon

Stand 31.10.2026, App-Version **2.1** (erste Fassung, veröffentlicht als Marathon 2.1, angelegt mit `werkzeuge/kern/kern.py --neu` auf dem gemeinsamen Kern; die
Hauptsitzung zählt die Nummer beim Veröffentlichen hoch).
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/stockholm/.

Die App hat den gemeinsamen Kern aus `hamburg/` und eigene Felder (Texte, `const D`, Speicherschlüssel `sth-…`, Service-Worker-Cache
`sth-marathon-profil`, löscht nur Caches mit Präfix `sth-`; der Präfix war frei, `kern.py --neu` prüft das), ohne eigenes Manifest und
Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Startseite,
README und `version.json` sind noch nicht angepasst (Hauptsitzung).

**Wichtigster Unterschied zu den anderen Strecken: Die Höhen kommen nicht aus einem Geländemodell, sondern aus der GPX-Datei des
Veranstalters** (Herkunft der Höhen nicht angegeben). Das Laser-Geländemodell von Lantmäteriet gibt es nur nach Anmeldung, und das
nächstbeste freie Modell (FABDEM, 30 m) ist in Stockholm zu ungenau (Daten 5). Das steht in der App im Untertitel, unter „Woher die
Zahlen kommen“ und im Hinweis darunter. Mit FABDEM statt GPX-Höhen: `python3 clean.py fabdem` (Daten 6).

## Termin und Start

48. adidas Stockholm Marathon am **Samstag, 29. Mai 2027**: Seite „About the race 2027“ des Veranstalters
(https://stockholmmarathon.se/eng/eng-lopare/, `../dl/lopare_en.html`: „DATE May 29 2027 | Prel. Start at 12:00 · PLACE Stockholm Olympic
Stadium“), Startseite „29 Maj 2027 – slutsålt“ (`../dl/start_sv.html`). Der 47. war am Samstag, 30. Mai 2026 (gelaufen). Veranstalter
Marathongruppen (Hässelby SK, Spårvägens FK). **Zeitlimit 6:30 h** laut Genehmigung der Polizei; vier Kontrollen mit Schlusszeit,
unabhängig vom eigenen Start (Participant Information 2026): km 21,1 Slussen 15:35, km 27 Heleneborgsgatan 16:25, km 32 Fleminggatan
17:15, km 35,5 Vasagatan/Tegelbacken 17:45 Uhr. Die Uhren an der Strecke laufen ab 12:00. Die Schlusszeiten stehen nur im Text der
Wellen (`D.tor` zeigt der Kern nur zusammen mit `D.mauer`, daher kein `D.tor`/`D.zielschluss`).
`D.termine` `["2026-05-30", "2027-05-29"]` (2027 vom Veranstalter bestätigt, ohne „?“), `D.tz` Europe/Stockholm (die Zeitzone nennt den
Ort, daher kein `D.ort`), `D.start` = 720 (12:00, für 2027 „preliminary“). Kein `D.lage`, `D.mauer`, `D.tor`.

**Starts** (`D.wellen`, Stand 2026): „Participant Information 2026“ (https://stockholmmarathon.se/participant-information-2026/,
`../dl/participant_2026.html`): drei Starts auf dem Lidingövägen vor dem Östermalms IP, Start 1 12:00 (Startgruppen A–C; A = gesetzte
Elite, Startnummern 1–400), Start 2 12:08 (D–F), Start 3 12:16 (G, H, J). Die Startgruppe richtet sich nach früheren Ergebnissen
(Halbmarathon/Marathon bei der Anmeldung) und steht als Buchstabe auf der Startnummer. Für 2027 noch nicht veröffentlicht; der
Hinweis in der App sagt das.

**Halbmarathon-Marke** bei 21 098 m (Zeitnahme „21,1 km“ an Slussen; Zwischenzeiten 5, 10, 15, 20, 21,1, 25, 30, 35, 40 km). Kein
Halbmarathon und keine Staffel im selben Rennen (der adidas Stockholm Halvmarathon ist im August).

**Ziel im Stadion:** Die Linie verlässt bei Linienmeter 41 890 (km 41,92) Drottning Sofias Väg und läuft durch das Tor ins
Stockholms Stadion (Olympiastadion 1912); die letzten 280 m sind Laufbahn. In den Straßennamen heißt das Stück „Stockholms Stadion“
(wie Athen „Panathinaiko-Stadion“). Höhe dort 21 m, eben.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Reihenfolge: `parse.py`, `osm.py`, `strassen.py`, `fabdem.py`, `dgm.py`, `vergleich.py` (nur Abgleich), `clean.py`, `orte.py`, `build.py`,
`marken.py` (nur Abgleich), `route.py`, `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py stockholm`, `stockholm/work/app.py`
(beim ersten Mal über `kern.py --neu stockholm work/felder.json`, danach ersetzt es nur die Felder und lässt Kartenbilder und
`D.tiles` stehen), `tiles_rand.py stockholm 2`. Nur Ausgabe: `carto_info.py`, `ziel.py`. Prüfen: `pruefen.js`, `pruefen2.js`,
`pruefen3.js` (Server auf Port 8781, `node pruefen.js`).

1. **Strecke** (`parse.py`): GPX-Datei des Veranstalters von der Seite „Banan“/„The course“ (Knopf „GPX-FIL“,
   `https://stockholmmarathon.se/wp-content/uploads/2026/05/SM26h.gpx_.zip`, `../dl/gpx/SM26h.gpx`): Track „SM26h“, erstellt mit GPS
   Visualizer, 3713 Punkte (nach Entfernen doppelter), Abstand im Median 8 m, **42 166,6 m** auf dem Ellipsoid (GRS80), vom Start auf dem
   Lidingövägen bis zur Ziellinie im Stadion. Kurs 2026 („The course of 2026“: neue Reihenfolge, Gamla stan zweimal umrundet, SoFo,
   Norr Mälarstrand bis zum Rathaus, Hantverkargatan; vermessen im Mai 2026 von Mikael Hill nach World-Athletics-Regeln). Für 2027 gibt es
   noch keine eigene Datei; die Seite „The course“ zeigt weiter 2026. Gegenprobe: die Linie der „dynamischen Karte“ des Veranstalters
   (CARTO-Konto „marathon“, Tabelle `bana`, Karte „SM“, Stand 04.05.2026, über die öffentliche SQL-API `marathon.carto.com/api/v2/sql`
   als GeoJSON, `../dl/carto/`) liegt im Median 4 m neben der GPX-Linie, 95 % bis 10 m, höchstens 19 m: derselbe Weg. Der Streckenplan
   als PDF (`ASM2026-bankarta_uppdate_May11.pdf`) zeigt ihn ebenso, mit Kilometermarken alle 5 km.
2. `common.py`: **Kilometer gleichmäßig** über die Linie (Faktor 42 195 / 42 166,6 = 1,00067), Start am Linienanfang, Ziel am Ende.
   Die dynamische Karte hat Kilometermarken 1–41 (Tabelle `km`, „4 km. Löparna passerar 12.12 - 12.46.“; 34 davon mit Stand 2026, die
   übrigen von 2023/2025 an Stellen, die der neue Kurs auch hat). Sie sind von Hand gesetzt und taugen nicht zum Eichen: Abstand Marke zu
   Marke 855–1164 Linienmeter. Gegen die gestreckte Linie (`marken.py`): Abweichung im Median −3 m (keine systematische Verschiebung),
   |Abweichung| im Median 21 m, 90 % bis 105 m, höchstens 200 m (km 38). Gegenproben mit den Orten, die der Veranstalter zu einer
   Kilometerangabe nennt (nach der Streckung, Straßen aus `strassen.py`): Schlusskontrollen km 21,1 Slussen (Slussbron 20,95–21,10),
   27 Heleneborgsgatan (ab 27,00), 32 Fleminggatan (31,84–32,56), 35,5 Vasagatan/Tegelbacken (Tegelbacken 35,20–35,32); Getränke km 3,5
   Östra Järnvägsgatan (3,43–3,68), 5,7 Skeppsbron (5,40–6,12), 8,6 Karlaplan (Narvavägen bis 8,85), 12,9 Sjöhistoriska
   (Djurgårdsbrunnsvägen ab 12,83), 24,2 Magnus Ladulåsgatan (ab 24,42), 26,9 Varvsgatan (26,81–27,00), 28,6 Rålambshovsparken
   (Rålambshovsleden ab 28,91), 31,8 Fleminggatan (ab 31,84), 34,5 Östra Järnvägsgatan (34,29–34,66), 36 Kornhamnstorg (Mälartorget
   35,98), 39,8 Karlaplan (ab 39,83). Alle passen auf höchstens 0,3 km (19,9 „Skeppsbron“: Skeppsbron beginnt erst bei 20,18, davor
   Strömbron). **Genauigkeit: Kilometer auf etwa ±0,1 km**, einzeln nicht belegt; die Linie folgt nicht überall der Ideallinie
   (28 m kürzer als vermessen).
3. `osm.py`: OSM über die API (`api.openstreetmap.org/api/0.6/map`) in 132 Rechtecken zu 0,005° höchstens 150 m neben der Linie, eine
   Abfrage je Sekunde (`../dl/osmapi/`) → `../dl/osm_netz.json` (18 417 Wege). Overpass war nicht nutzbar (overpass-api.de Verbindung
   abgebrochen, maps.mail.ru 22 s für eine Mini-Abfrage, kumi.systems und private.coffee Zeitüberschreitung).
   `strassen.py` (wie Athen): je 10 m der nächste Weg bis 20 m neben der Linie mit höchstens 35° Richtungsabweichung, Hauptstraßen
   bevorzugt; Namen wie in OSM, schwedisch wie auf den Schildern (`namen.py`).
4. `orte.py`: **Stadtteil** alle 100 m: Stadsdelar der Stadt Stockholm (OSM `admin_level` 10; 16 Flächen über
   `api.openstreetmap.org/api/0.6/relation/<id>/full`, `../dl/orte/`), je 40 m links und rechts nachgesehen, bei zwei Stadtteilen
   „links / rechts“ (Lidingövägen „Ladugårdsgärdet / Norra Djurgården“, Valhallavägen „Ladugårdsgärdet / Östermalm“ bzw.
   „Östermalm / Norra Djurgården“). Riddarhusgränd und Riddarhustorget („Gamla stan / Riddarholmen“) als Gamla stan (`build.py`).
   Begründung: Man orientiert sich in Stockholm an den Stadtteilen (Östermalm, Södermalm, Kungsholmen …); die Stadsdelsområden darüber
   sind Verwaltung. Folge: Ladugårdsgärdet/Norra Djurgården, Östermalm, Vasastaden, Norrmalm, Gamla stan, Norrmalm, Östermalm,
   Ladugårdsgärdet, Djurgården, Östermalm, Norrmalm, Gamla stan, Södermalm (km 21–27,4), Långholmen, Marieberg, Kungsholmen, Vasastaden,
   Norrmalm, Gamla stan, Norrmalm, Östermalm, Norra Djurgården (Stadion).
5. `fabdem.py`, `hoehen.py`, `dgm.py`, `vergleich.py`: **Höhe.**
   **Lantmäteriet nur mit Anmeldung:** Das Markhöjdmodell (1-m-Raster aus Laserscans, „Markhöjdmodell Nedladdning, grid 1+“) ist laut
   STAC-Katalog von Lantmäteriet (`https://api.lantmateriet.se/stac-hojd/v1/collections/dtm-cog`, ohne Anmeldung lesbar) „avgiftsfri“ unter
   **CC BY 4.0** (nicht CC0). Die Kacheln selbst (`https://dl1.lantmateriet.se/hojd/data/grid/mhm/65_6/m658_67.tif`, COG 10 × 10 km,
   Laserscan 2020/2021) antworten aber mit **401 Unauthorized** („Basic realm“): Man braucht ein Konto bei Geotorget. Nicht angemeldet. Frei
   abrufbar sind nur Metadaten (`…/pub/…_info.json`) und ein Vorschaubild 256 × 256 px (`../dl/lm/`). Der WMS „Höjdmodell Visning“
   (`minkarta.lantmateriet.se/map/hojdmodell`) liefert nur Schummerung und Neigungsbilder, keine Höhenwerte. Die Stadt Stockholm hat ein
   eigenes Höhenraster aus Laserscans 2024 („SBK Höjdgrid“, Dataportalen), aber nur über die Geodatabutiken bzw. mit API-Schlüssel.
   **Frei abrufbar und verglichen** (alle 10 Linienmeter, `dgm_vergleich.json`; offizielle km; Unruhe = mittlere |2. Differenz| je 10 m):

   | Quelle | Start | Ziel | min | max (km) | ↑/↓ 200 m | ↑ 1 km | gegen GPX (Median, Hälfte) | r | Unruhe |
   |---|---|---|---|---|---|---|---|---|---|
   | GPX-Höhen des Veranstalters | 21,2 | 20,9 | 1,6 | 36,2 (26,47) | 194/194 | 101 | – | – | 0,039 |
   | FABDEM V1-2 (30 m) | 26,0 | 23,5 | 0,0 | 39,4 (26,46) | 388/391 | 138 | +3,7 (+1,2 bis +8,0) | 0,80 | 0,283 |
   | Copernicus GLO-30 | 29,1 | 21,1 | −0,8 | 45,7 (19,80) | 570/577 | 170 | +5,9 (+2,3 bis +11,5) | 0,75 | 0,443 |
   | SRTM 1″ (2000) | 30,8 | 26,4 | 4,2 | 54,5 (24,13) | 427/432 | 140 | +12,7 (+9,0 bis +16,2) | 0,77 | 0,219 |

   Je 5 km (↑/↓, 200-m-Fenster) GPX gegen FABDEM: 10/29 – 35/56, 24/9 – 49/26, 28/32 – 30/44, 15/26 – 46/58, 34/12 – 59/32,
   31/53 – 43/69, 19/18 – 67/65, 23/12 – 50/31, 9/3 – 8/10.
   **Gewählt: die GPX-Höhen des Veranstalters.** Sie sind die Höhen in der offiziellen Streckendatei (GPS Visualizer übernimmt Höhen aus
   der Eingabedatei; woher sie stammen, sagt der Veranstalter nicht; vielleicht ein Messgerät mit Luftdruck oder ein Routenplaner). Gründe:
   - **Kais:** Skeppsbron, Strandvägen, Norr Mälarstrand liegen in der GPX auf 2–3 m über dem Meer, wie zu erwarten; FABDEM zeigt auf
     Strandvägen 7–13 m (Alleebäume), Copernicus noch mehr.
   - **Offenes Gelände** (wo FABDEM und das Oberflächenmodell Copernicus auf 1 m übereinstimmen, also weder Häuser noch Bäume stehen,
     22 % der Punkte: Gärdet, Djurgården, Norr Mälarstrand): GPX und FABDEM haben dieselbe Form, GPX im Median 2,3 m tiefer (Hälfte
     0,7–4,2 m; ob Höhenbezug oder Restfehler, ist offen). Zwischen Häusern liegt FABDEM bis 15 m höher (Sveavägen, Vasagatan,
     Karlavägen, Södermalm, Kungsholmen: Gebäude im 30-m-Raster nicht ganz herausgerechnet) und ist siebenmal so unruhig.
   - **Beschreibung des Veranstalters** („Kilometer für Kilometer“ auf der Seite „The course“): Auf allen 17 Stücken, die sie bergauf
     oder bergab nennt, hat die GPX die richtige Richtung, FABDEM nur auf 12 (falsch: Kungsgatan „fast downhill“, Sturegatan zweimal
     „uphill“, Djurgårdsvägen „steep descent from the top of Manilla“, Scheelegatan „continue the climb“). Narvavägen „nearly 600 m,
     gradient about 2–3 %“: GPX +1,9 %, FABDEM +3,0 %. Höchster Punkt laut Beschreibung an der Lundagatan: GPX (36,2 m, km 26,47) wie
     FABDEM.
   - **Brücken:** Die GPX enthält die Fahrbahnen (Vasabron 4–5,5 m, Strömbron 3–4 m, Djurgårdsbron 5 m, Sankt Eriksbron eben auf 17 m,
     Västerbron steigt von 15 m auf 30,7 m über Riddarfjärden, Durchfahrtshöhe der Brücke 26 m); die Modelle messen dort Wasser (0 m).
   **Grenzen:** Herkunft und Messverfahren der GPX-Höhen sind unbekannt. Sie sind sehr glatt (Unruhe 0,039, Athen FABDEM 0,08, Wien
   Laser 1 m); kurze steile Rampen erscheinen wohl flacher, als sie sind (Katarinavägen: steilstes 100-m-Stück +2,7 %, FABDEM +9,8 %;
   der Veranstalter sagt „steepest at the beginning“, nennt aber keine Zahl). Die Höhenmeter könnten deshalb eher zu niedrig sein als zu
   hoch.
   FABDEM: data.bris.ac.uk, Zip `N50E010-N60E020_FABDEM_V1-2.zip` per Teilabruf, nur Kachel N59E018 (`../dl/dem/`); Copernicus GLO-30 von
   AWS (`copernicus-dem-30m`, nördlich 50° 1″ × 1,5″), SRTM von AWS Terrain Tiles (skadi), alle ohne Anmeldung. `hoehen.py` liest die
   GeoTIFF mit tifffile (RasterPixelIsPoint), bilinear.
6. `clean.py`: Standard `python3 clean.py` (GPX): Stufen über 1,5 m je 10 m gibt es keine (größte 1,25 m), Brücken bleiben, wie die
   Datei sie zeigt; **nichts geschätzt**, `D.bridges` leer (wie Boston). OSM-Brücken auf der Linie (nur Ausgabe): Vasabron (km 4,36 und
   35,33, 210 m), Norrbro (km 6,2–6,4 und 37,2–37,4, kurz), Djurgårdsbrunnsbron (14,47), Djurgårdsbron (18,25), Strömbron (20,04, 140 m),
   Slussbron (20,96, 140 m, steigt in der GPX von 6 auf 12 m), Rosenlundsgatan über die Bahn (25,21), Västerbron (27,44–28,39, 950 m),
   Gjörwellsgatan (28,82), Sankt Eriksbron (32,83, 150 m). Keine Tunnel auf der Linie.
   **Gegenprobe mit FABDEM** (`python3 clean.py fabdem [Halbbreite]`, danach `build.py`): Brücken gerade zwischen den Rampenenden
   (geschätzt, schraffiert; Västerbron 15,7 → 11,7 m statt Buckel auf 31 m, Sankt Eriksbron 22 → 21 m), Wasserpunkte unter 1 m ersetzt,
   dann robust geglättet (LOWESS ±150 m wie Athen-Innenstadt). Ergebnis ↑ 252 / ↓ 255 m (±100 m: 289/291, ±250 m: 202/205), r = 0,87
   gegen die GPX, im Median 3,8 m höher. Nicht genommen (siehe 5).
7. `build.py`: Höhen in cm im 10-m-Raster, Median über 30 m; Straßenstücke unter 80 m und Stadtteile unter 300 m dem Vorgänger
   zugeschlagen. **Marken** laut „Participant Information 2026“, „Hydration & energy“ (an der km-Angabe): 13 Getränkestellen, an 1, 3, 5,
   7, 8, 9 und 12 nur Wasser, an den übrigen zuerst Enervit G Sport (Orange) und dahinter Wasser: km 3,5 Östra Järnvägsgatan, 5,7
   Skeppsbron, 8,6 Karlaplan, 12,9 Sjöhistoriska, 16,9 Skansen, 19,9 Skeppsbron, 24,2 Magnus Ladulåsgatan, 26,9 Varvsgatan, 28,6
   Rålambshovsparken, 31,8 Fleminggatan, 34,5 Östra Järnvägsgatan, 36,7 Skeppsbron, 39,8 Karlaplan. Zehn Energiestellen („shortly before a
   fluid station“): 8,6 Bananen, 16,9 Enervit-Gel (Cola), 24,2 Salzgurken, 26,1 Hornsgatan Apfelschnitze, 28,6 Traubenzucker, 31,8
   Gemüsebrühe, 34,5 Bananen, 36 Kornhamnstorg Red Bull, 36,7 Kaffee, 39,8 Cola. In der App: Getränkestelle mit Energie = „Verpflegung“
   (food), ohne = „Wasser“ bzw. „Getränke“ (water), die zwei Energiestellen ohne Getränke als „Verpflegung“; 16 Marken mit Halbmarathon.
   Nicht übernommen: Enervits persönlicher Verpflegungsdienst (km 6,6 / 15 / 37,6, nur mit gebuchtem Armband), Getränke in den
   Startfeldern, Kühlduschen vor den Stationen. `route.py` (lat0/lon0 59,3/18,0), `tiles.py` (z12–z15), `tiles_z11.py stockholm`,
   `app.py`, `tiles_rand.py stockholm 2`: 23 Kartenstücke, 2,6 MB.

## Ergebnis

↑ 194 m / ↓ 194 m mit 200-m-Fenster, ↑ 232 / ↓ 232 m mit 50 m, ↑ 218 / ↓ 218 m mit 100 m, ↑ 101 / ↓ 102 m mit 1 km; wie GPS-Uhren
209 (ab 0,5 m), 189 (ab 1 m), 139 (ab 3 m); Rohdaten ↑ 256 m. Start 21,2 m auf dem Lidingövägen, Ziel 20,9 m im Stadion, tiefster Punkt
1,7 m an der Nybrokajen (km 19,6), höchster 36,2 m an der Lundagatan (km 26,47); Höhenbereich 34,5 m. Vom Stadion über Odengatan und
Sveavägen 15 m hinunter zum Hauptbahnhof, flach am Wasser um Gamla stan und über Strandvägen (2–5 m), Narvavägen hinauf (+11 m), über
Karlavägen und Sturegatan zum Stadion (22 m, km 10), über Gärdet hinunter an den Kanal, auf Djurgården zweimal kurz hinauf (Manilla
15 m), ab Slussen (km 21) die Katarinavägen hinauf nach Södermalm (26 m), wellig zum höchsten Punkt an der Lundagatan, hinunter zur
Västerbron und über die Brücke (31 m), steil hinunter nach Kungsholmen, Hantverkargatan/Fleminggatan 14 m hinauf, über Torsgatan hinunter,
ein zweites Mal um Gamla stan und zum Schluss Narvavägen und Sturegatan hinauf ins Stadion. Steilste Stellen über 200 m: −5,6 % von der
Västerbron hinunter (km 28,6), +4,7 % von Slussen in die Katarinavägen (km 21,0); über 100 m −6,9 % bei km 28,6.
**Modellzeit:** Mit 4:00/km im Flachen ergibt das Modell **2:50:40** (das Profil kostet 113 s); **bei 2:50:00 kostet es 113 s, bei 4:00:00
160 s** (Flach-Pace 3:59,1 bzw. 5:37,5 /km; gemessen mit `pruefen.js` in der App 2.0). Zum Vergleich bei 2:50:00: Wien 61 s, Boston 88 s,
Athen 213 s. Mit den FABDEM-Höhen wären es mehr (↑ 252 statt 194 m).

Geprüft mit Playwright (Chromium, 393 × 852, Faktor 2, Server auf Port 8781, `pruefen.js`, `pruefen2.js`, `pruefen3.js`): keine
Konsolenfehler, `APP_VERSION` 2.0 und Knopf v2.0, Service Worker installiert (29 Einträge im Cache `sth-marathon-profil`), Tipp auf die
Version meldet „Version 2.0 ist aktuell“; alle 23 Kartenstücke passen zu `D.tiles` und `sw.js`; Tabellen bei 320/375/393/430 px ohne
Überbreite, Seite nicht breiter als das Fenster. Laufansicht am Start, km 8,6 (Narvavägen), 21,3 (Katarinavägen), 26,5 (Lundagatan), 28,1
(Västerbron), 42,05 (Stadion) und die Kartenübersicht mit Verpflegung angesehen; Zuschauer-Tabelle mit drei Starts und nächstem Termin
29. Mai 2027; „Woher die Zahlen kommen“ angesehen. Bilder in `work/shots/`. `kern.py` meldet „Alle gleich“.

## Offen

- Prüfung am iPhone.
- **Höhenquelle** (Daten 5): Entscheidung des Nutzers. GPX-Höhen des Veranstalters (jetzt, Herkunft unbekannt, glatt) oder FABDEM
  (`clean.py fabdem`, dann `build.py`, `app.py`; deutlich unruhiger, ↑ 252 m). Besser wäre Lantmäteriets Laser-Modell: Wenn der Nutzer
  ein (kostenloses) Geotorget-Konto anlegen und die zwei Kacheln `m657_67.tif` und `m658_67.tif` (1 m, zusammen 550 MB, als COG auch
  teilweise lesbar) bereitstellen will, ließe sich die Strecke wie Wien rechnen; die Brücken dann aus den GPX-Höhen oder als Gerade.
  Laserdaten als Punktwolke (Brücken) gibt es dort ebenfalls nur mit Anmeldung.
- Startseite: Karte fehlt (Eyebrow „adidas Stockholm Marathon“, Stadt „Stockholm“, „Kurs 2026“, `data-termine="2026-05-30 2027-05-29"`,
  `data-monat="5"`, ↑ 194 m / ↓ 194 m, Höhe 2–36 m, `data-such` z. B. „Stockholm Schweden Sverige Sweden adidas Stockholms Stadion“;
  Mini-Profil mit 34,5 m Höhenbereich passt in die Grundhöhe 64 px), README-Tabelle und Liste der Präfixe (`sth-`). Teilnehmer:
  18 921 im Ziel 2026 (20 302 am Start, beides Rekord; TT-Meldung vom 30.05.2026, z. B. tv4.se „En allvarlig sjukvårdshändelse under
  maran“), 24 722 angenommene Anmeldungen.
- Kurs 2027: Die Seite „The course“ zeigt noch 2026, eine GPX-Datei 2027 gibt es nicht. Erscheint eine neue Datei oder ein geänderter
  Plan, `parse.py` und die Kette erneut laufen lassen; `D.wellen` und die Marken (Getränke/Energie 2026) für 2027 prüfen
  (Participant Information erscheint etwa im Mai).
- Kilometer: nur gleichmäßig gestreckt (Daten 2). Eine Liste der Kilometerschilder mit Koordinaten gibt es nicht; die Marken der
  dynamischen Karte sind von Hand gesetzt.
- Västerbron: In den GPX-Höhen steigt die Brücke auf 30,7 m; ob die Fahrbahn genau so verläuft, ist ohne Oberflächenmodell nicht
  geprüft (Durchfahrtshöhe 26 m macht es plausibel).
- Gegenprobe mit dem privaten Eichdatensatz (`course_segments`) nicht gemacht: Die Datei lag in dieser Sitzung nicht vor.
