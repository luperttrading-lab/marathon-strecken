# Übergabe: Steigungsprofil TCS Amsterdam Marathon

Stand 30.10.2026, App-Version **1.0** (1.0: erste Fassung).
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/amsterdam/.

Die App ist eine Kopie der Tokio-App (Stand 1.24, aktueller gemeinsamer Code) mit eigenen Daten, Texten und Speicherschlüsseln
(`ams-…`, Service-Worker-Cache `ams-marathon-profil`, löscht nur Caches mit Präfix `ams-`), ohne eigenes Manifest und Symbol. Alle
Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Änderungen am
gemeinsamen Code in allen Apps nachziehen (README).

## Termin und Start

TCS Amsterdam Marathon 2026 (Veranstalter Le Champion) am Sonntag, 18. Oktober 2026, gelaufen (Programm 2026 auf
https://www.tcsamsterdammarathon.eu/program). Für 2027 nennt der Veranstalter auf Start- und Programmseite das Wochenende
Samstag 30. und Sonntag 31. Oktober 2027; der Marathon ist wie jedes Jahr am Sonntag (Samstag 7,5 km und Kinderläufe), daher
`2027-10-31` ohne „?“. `D.termine` `["2026-10-18", "2027-10-31"]`, `D.tz` Europe/Amsterdam, `D.ort` „Amsterdam“, `D.ortKurz`
„ Amsterdam“, `D.start` = 540 (9:00). Zielschluss 17:00 (6 Stunden).

**Startwellen** (`D.wellen`) laut Seiten „Start times“ (https://www.tcsamsterdammarathon.eu/start-times) und „TCS Marathon“
(https://www.tcsamsterdammarathon.eu/tcs-marathon), 2026, gleiche Uhrzeiten in Startbereich A (Olympiastadion, 16 000 Läufer) und
B (Stadionweg, 16 000), eingeteilt nach erwarteter Zielzeit, Farbe auf der Startnummer: Welle 1 Weiß 9:00 (Eingeladene und bis
2:40), Welle 2 Gelb 9:02 (2:40–3:15), Welle 3 Rosa 9:11 (3:15–3:45), Welle 4 Orange 9:24 (3:45–4:00), Welle 5 Grün 9:34
(4:00–4:30), Welle 6 Blau 9:43 (4:30–6:00). Für 2027 noch nicht veröffentlicht.

Start A auf der Bahn im Olympisch Stadion (Startplan „Start Area Sunday“, `../dl/start-2026-v7.png` von
https://do.occdn.net/p/75/f/start-tcs-amsterdam-marathon-2026-sunday-v7-web-1.png: Startstrich auf der Westgeraden, über die
Südkurve und die Ostgerade durch das Marathontor hinaus), Start B auf dem Stadionweg nach Osten und über den Marathonweg auf die
Amstelveenseweg. Die App folgt Start A. Ziel im Stadion vor der Tribüne.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Eine GPX- oder KML-Datei der Strecke veröffentlicht der Veranstalter nicht (Seiten durchsucht; die Race-App braucht eine
Anmeldung, Finishers.com zeigt nur ein Vorschaubild unbekannter Herkunft). Eine OSM-Relation der Strecke gibt es nicht. Die Linie
ist deshalb nach dem Streckenplan auf OpenStreetMap nachgezeichnet.

1. `pdflinie.py`: **Streckenplan 2026** des Veranstalters, Vektor-PDF aus InDesign
   (https://do.occdn.net/p/75/f/parcours-tcs-amsterdam-marathon-zondag-2026-v2.pdf, erstellt 08.09.2026, verlinkt auf der Seite
   „TCS Marathon“; `../dl/parcours-2026-v2.pdf`). Rote Linie (Marathon, 5 pt) in drei Stücken, Kilometerkreise: Kästchen „N km“
   mit Hinweislinie auf einen kleinen weißen Kreis auf der Linie, alle 41 gefunden. → `../dl/pdf_linie.json`, `../dl/pdf_marken.json`.
   Der Plan zeigt den bisherigen Kurs; die für 2026 angekündigte neue Führung über Rokin und Dam
   (https://www.tcsamsterdammarathon.eu/final-course-revealed-for-tcs-amsterdam-marathon-jubilee-edition) ist nicht darin.
2. `osm.py grob`: OSM-Daten über die OSM-API (`api.openstreetmap.org/api/0.6/map`) in 239 Rechtecken von 0,004° × 0,006° entlang
   der grob eingepassten Planlinie, eine Abfrage je Sekunde (Rohantworten `../dl/osmapi/`, gut 250 MB) → `../dl/osm_netz.json`
   (28 608 Wege). Overpass war am 30.10.2026 aus dieser Umgebung nicht nutzbar (maps.mail.ru und overpass.private.coffee 504,
   overpass-api.de Verbindung abgebrochen, overpass.kumi.systems Zeitüberschreitung). `wasser.py`: Uferlinien (auch die
   Multipolygone der Amstel) → `../dl/osm_wasser.json`.
3. `einpassen.py`, `plan.py`: Der Plan ist eine gezeichnete, verzerrte Stadtkarte (affin über acht Bahnhofssymbole bis 360 m
   daneben). ICP der weißen Straßenlinien und der Uferlinien des Plans auf OSM, global und lokal je Stützpunkt alle 60 pt,
   gaußförmig überblendet: in der Stadt meist 3–10 m, stellenweise aber 100–200 m daneben (Van der Madeweg, Zuidas), im Polder an
   der Amstel bis 300 m. Für die Linie taugt der eingepasste Plan deshalb nur im Vondelpark; sonst dient er als Bild.
4. `linie.py`: **Linie Straße für Straße** nach dem Plan: rund 40 Abschnitte von Kreuzung zu Kreuzung mit den Straßennamen laut Plan
   (Dijkstra, andere Namen kosten das Fünffache, Fuß-, Rad- und Wirtschaftswege das 1,3- bis 1,6-Fache, Einbahnstraßen gelten
   nicht), im Vondelpark entlang der eingepassten Planlinie (Hin- und Rückweg auf demselben Weg, wie im Plan nebeneinander
   gezeichnet). Stiche (hin und zurück zu einem Wegpunkt neben der Straße) werden entfernt (53 m). Stadion: innerer Rand der
   Laufbahn aus OSM (Relation 1717342, 399,5 m), Start 25 m nach dem Nordende der Westgeraden, durch die Südkurve bis zur Mitte
   der Ostgeraden und 40 m nach Osten durch das Marathontor; Ziel am selben Strich auf demselben Weg zurück.
   Ouderkerk aan de Amstel: hin auf der Amsteldijk Noord am Fuß des Damms der Oranjebaan (im Plan liegt der Hinweg nördlich),
   Wende am Westende der zweibahnigen Oranjebaan 260 m hinter der Brücke (im Plan ≈ 230 m), zurück auf dem Damm und über die
   Brücke der Burgemeester Stramanweg; das Höhenbild des Veranstalters zeigt genau diese Senke (gut 200 m auf −1,5 m, dann
   hinauf zur Brücke). → `gpx2026.json` (5442 Punkte, **42 879 m** auf dem Ellipsoid), `linie_wege.json` (OSM-Weg je Stück).
   Straßenfolge: Stadionplein, Amstelveenseweg, Vondelpark, Stadhouderskade, Museumstraat (Passage unter dem Rijksmuseum),
   Hobbemastraat, Hobbemakade, Stadionweg, Beethovenstraat, Gustav Mahlerlaan, Parnassusweg, De Boelelaan, Beethovenstraat,
   Stadionweg, Apollolaan, Muzenplein, Churchill-laan, Victorieplein, Rijnstraat, President Kennedylaan, De Mirandalaan,
   Zuidelijke Wandelweg, Amsteldijk, Amsteldijk Noord, Oranjebaan, Burgemeester Stramanweg, Hoger Einde-Noord, Binnenweg,
   Ouderkerkerdijk, Jan Vroegopsingel, Joan Muyskenweg, Van der Madeweg, Randweg, Rozenburglaan, Kruislaan, Maxwellstraat,
   Hugo de Vrieslaan, Wethouder Frankeweg, Galileïplantsoen, Archimedesweg, Molukkenstraat, Borneostraat, Zeeburgerdijk,
   Mauritskade, Torontobrug, Stadhouderskade, Vondelpark, Amstelveenseweg, Stadionplein.
5. `common.py`: **Kilometer gleichmäßig** über die ganze Linie (Faktor 0,9840; 2,0 % Linie über 42,195 km, entlang der
   Straßenmitte). Begründung: Das Höhenbild des Veranstalters (`../dl/hoogteprofiel-marathon.png` von
   https://www.tcsamsterdammarathon.nl/uploads/hoogteprofiel-marathon.png, x-Achse bis 42,9 km) deckt sich Kilometer für Kilometer
   mit der Linie (1 km → 1,00, 26 → 26,06, 30 → 30,02, 34 → 34,08, 38 → 38,06, 42 → 42,18 km Linie); der Veranstalter rechnet also
   selbst mit einer gleich langen Linie. `marken.py` legt die 41 Kilometerkreise des Plans über eine Zuordnung Planlinie ↔ Linie
   (dynamic time warping) auf die Linie: sie liegen danach im Mittel 109 m, höchstens 382 m neben der gleichmäßigen Eichung, mit
   Gang (km 1–17 rund 100 m früher, km 30–41 bis 380 m später); einzelne Abschnitte hätten 820 bis 1280 m Linie je km. Für
   eine Eichung über die Marken ist der gezeichnete Plan zu ungenau. → `marken.json` (nur Abgleich).
6. `dgm.py`: **AHN4** (Actueel Hoogtebestand Nederland, Laserbefliegung 2020–2022), Geländemodell **DTM 0,5 m** („maaiveld“, nur
   Bodenpunkte, quadratisch-IDW) über den WCS von PDOK (`https://service.pdok.nl/rws/ahn/wcs/v1_0`, Coverage `dtm_05m`, GeoTIFF
   float32 in RD New), 177 Kacheln von 250 × 250 m entlang der Linie (`../dl/ahn/`). Je 10 m der Median der gültigen Zellen im
   Umkreis von 1 m (13 Zellen, mindestens 4). Höhen in m über NAP. 4289 Punkte, 160 ohne Boden (Brücken, Viadukte, Passage,
   Tribüne). In diesen Lücken zum Vergleich das Oberflächenmodell `dsm_05m` (40 Kacheln). Lizenz CC0.
7. `strassen.py`: Name, Brücke, Tunnel je 10 m aus den OSM-Wegen der Linie (Namen niederländisch wie in OSM; die Torontobrug
   ist in OSM ohne Namen). `orte.py`: **Wijk** aus der Wijk- en Buurtkaart 2024 des CBS (WFS von PDOK,
   `service.pdok.nl/cbs/wijkenbuurten/2024/wfs/v1_0`, `../dl/cbs_wijken_2024.json`): in Amsterdam die Wijken der Stadt
   (Stadionbuurt, Museumkwartier, Zuidas, Oude Pijp, Indische Buurt-Oost …, „ e.o.“ entfällt). Stadsdelen wären zu grob (Zuid allein
   km 0–15 und ab km 37), Buurten zu fein (die Strecke läuft oft auf ihren Grenzstraßen). Außerhalb Amsterdams der Ort: Amstelveen;
   in Ouder-Amstel (das CBS hat dort nur „Wijk 00“) nach der Buurt Ouderkerk aan de Amstel bzw. Duivendrecht, sonst „Ouder-Amstel“.
8. `clean.py`: Brücken aus OSM (bridge=yes auf der Linie): Enden oben auf den Rampen (höchster gemessener Punkt bis 50 m
   außerhalb), gerade gezogen, wo innen eine Lücke ist oder das Modell mehr als 0,3 m darunter liegt. Übrige Lücken gerade zwischen
   den gemessenen Enden, Art nach OSM (Tunnel, Passage) bzw. Oberflächenmodell (mehr als 2,5 m darüber: Unterführung, sonst
   Brücke); Lücken von einem Punkt ohne Kennzeichnung. Uferkanten an Widerlagern (Delle über 1 m je 10 m bis 50 m neben einem
   Stück) gerade gezogen. Benachbarte Stücke gleicher Art bis 60 m Abstand zusammengefasst. **Geschätzt** (schraffiert): 21 Brücken
   (u. a. Torontobrug, Brücke der Burgemeester Stramanweg in Ouderkerk, sechs Brücken und Viadukte der Van der Madeweg, Kanalbrücken
   der Zuid), 12 Unterführungen (Bahnhof Zuid und A10 an der Beethovenstraat auf Hin- und Rückweg, A10 und Bahn an der Amstel auf
   beiden Ufern, Nieuwe Utrechtseweg und Autobahnkreuz Amstel an der Joan Muyskenweg, A10 an der Rozenburglaan, Bahn an der
   Zeeburgerdijk, Vondelbrug der Van Baerlestraat im Vondelpark auf Hin- und Rückweg, Marathontor unter der Tribüne), 3 Tunnel (Passage unter dem Rijksmuseum, Molukkenstraat unter der Bahn, Mauritskade unter der Wibautstraat) und
   1 Rampe: In Ouderkerk fällt das Modell von der Deichstraße zur Amsteldijk Noord neben einer Böschung auf 10 m um 2,4 m; dort
   über 50 m verteilt. **Gemessen** bleiben die Rampen vor allen Brücken und die Einschnitte der Unterführungen bis an die Decke
   (Mauritskade bis 3,3 m unter NAP). Auf der Torontobrug misst das DSM die Fahrbahn bis 5,1 m, 1,7 m über der Geraden.
   An der Beethovenstraat vor dem Bahnhof Zuid (Großbaustelle Zuidasdok) misst das AHN einen Buckel von 3,5 m (km 6,7 und 9,2);
   das Höhenbild des Veranstalters zeigt ihn nur auf dem Rückweg.
9. `build.py`: Höhen in cm im 10-m-Raster, Median über 30 m; Straßenstücke unter 80 m und Wijken unter 300 m dem Vorgänger
   zugeschlagen. Getränke laut Tabelle „Refreshment stations“ der Seite „TCS Marathon“ (2026) an ihrer km-Angabe: Wasser bei
   5, 8, 11, 16, 20, 25, 27, 31, 33, 35, 38, 40,5 km, dazu Maurten-Getränk (5, 11, 16, 20, 27, 31, 35, 38), Bananen (11, 16, 20,
   27, 31, 35, 38, 40,5), Schwämme (11, 20, 27, 33, 38); Maurten-Gel bei km 18 und 30. Halbmarathon bei 21 098 m.
   `route.py` (lat0/lon0 52,3/4,8), `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py amsterdam`, `work/app.py` (aus
   `tokio/index.html` und `tokio/sw.js`; Texte in `sub.html`, `quellen.html`, `strassennamen.html`, `imgnote.html`),
   `tiles_rand.py amsterdam 2`.

## Ergebnis

↑ 59 m / ↓ 59 m mit 200-m-Fenster (Tabelle in der App: 50 m 85, 100 m 74, 1 km 23), Rohdaten ↑ 119 m. Start und Ziel 1,0 m über
NAP auf der Bahn, höchster Punkt 3,75 m auf dem Damm der Van der Madeweg (km 28,9), tiefster −4,17 m im Polder der
Watergraafsmeer (Rozenburglaan, km 30,9; der Polder liegt von km 30,9 bis 33,2 auf −3,5 bis −4,2 m). Vondelpark bis
−1,9 m (km 1,7–3,6 und 38,6–40,5), die Amstel-Deiche um 0 bis +0,5 m. Steilste Stelle +3,3 % über 200 m von der Unterführung
der Mauritskade hinauf zur Torontobrug (km 36,6), bergab −2,4 % auf der Rozenburglaan in den Polder (km 30,5). Mit 4:00/km im
Flachen ergibt das Modell 2:49:20 (das Profil kostet 33 s, bei 2:50:00 33,5 s).

Abgleich mit dem Höhenbild des Veranstalters: gleiche Senken und Buckel an denselben Stellen (Vondelpark, Rijksmuseum, Ouderkerk,
Van der Madeweg, Polder, Mauritskade und Torontobrug), dort meist gut 0,5 m höher und die Brücken als Spitzen. Abweichend: der
Buckel an der Beethovenstraat (siehe oben) und die Brücke der President Kennedylaan (App km 12,6), die das Bild nicht zeigt; das
Bild hat dafür eine Spitze bei seinem km 12,0, wo AHN und Linie flach sind.

Geprüft mit Playwright (393 × 852, Faktor 2, Server auf Port 8774): keine Konsolenfehler, `APP_VERSION` 1.0, Service Worker
installiert (28 Dateien im Cache `ams-marathon-profil`), Tipp auf die Version meldet „Version 1.0 ist aktuell“, alle 22
Kartenstücke passen zu `D.tiles`, nächster Termin 2027-10-31; Laufansicht, Rijksmuseum, Ouderkerk, Torontobrug und Übersicht auf
der Karte angesehen.

## Offen

- Prüfung am iPhone.
- Startseite: Karte für Amsterdam fehlt noch (Eyebrow „TCS Amsterdam Marathon“, Stadt „Amsterdam“, „Kurs 2026“,
  `data-termine="2026-10-18 2027-10-31"`, `data-monat="10"`, ↑ 59 m / ↓ 59 m, Höhe −4–4 m, `data-such` z. B. „Niederlande Holland
  Nederland Netherlands TCS“), README-Tabelle und Liste der Speicherschlüssel/Cache-Präfixe (`ams-`).
- **Kurs 2027**: Die neue Führung über Rokin und Dam war für 2026 angekündigt, der Plan 2026 zeigt sie nicht. Sobald der Plan
  2027 erscheint (2026 im September), mit `pdflinie.py` vergleichen; bei Änderungen die Abschnitte in `linie.py` anpassen und die
  Kette ab `strassen.py` neu laufen lassen.
- **Kilometer**: gleichmäßig über die Linie. Ein GPX oder Kilometermarken mit Koordinaten (z. B. AIMS-Vermessung) gibt es nicht
  öffentlich. Start und Ziel im Stadion nach Startplan und Plan; der Gang der Kilometerkreise (Anfang zu früh, Ende bis 380 m zu
  spät) passt auch zu einem Start und Ziel näher am Marathontor. Nach dem Startplan sind es von Start B über Stadionweg und
  Marathonweg bis zur Amstelveenseweg gut 0,9 km (aus dem Bild geschätzt), von Start A nach dieser Linie knapp 1,1 km; beide
  Starts müssten gleich weit davon liegen.
- Wellen 2027 prüfen, sobald veröffentlicht (2026 Seite „Start times“).
- Buckel an der Beethovenstraat (Zuidasdok, AHN 2020–2022) kann durch den Umbau überholt sein; neueres AHN (AHN5 ab 2026) prüfen.
- Torontobrug gerade gezogen; das Oberflächenmodell zeigt einen Buckel von 1,7 m über der Geraden.
