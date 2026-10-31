# Übergabe: Steigungsprofil Uniper Düsseldorf Marathon

Stand 31.10.2026, App-Version **2.3** (erste Fassung, angelegt mit `werkzeuge/kern/kern.py --neu` auf dem gemeinsamen Kern; die
Hauptsitzung zählt die Nummer beim Veröffentlichen hoch).
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/duesseldorf/.

Die App hat den gemeinsamen Kern aus `hamburg/` und eigene Felder (Texte, `const D`, Speicherschlüssel `dus-…`, Service-Worker-Cache
`dus-marathon-profil`, löscht nur Caches mit Präfix `dus-`; der Präfix war frei, `kern.py --neu` prüft das), ohne eigenes Manifest und
Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Startseite,
README, `version.json` und `karten.json` sind noch nicht angepasst (Hauptsitzung).

**Besonderheiten:** Eine GPX-Datei veröffentlicht der Veranstalter nicht. Die Linie kommt aus dem **Streckenplan 2026 als Vektorkarte**
(die rote Linie ist in der PDF-Datei ein einziger Pfad), eingepasst an die OSM-Straßen; eine Tour von Visit Düsseldorf bestätigt sie.
Höhen wie Köln aus **DGM1 NRW**, alle **Brücken aus dem Oberflächenmodell DOM1 NRW** gemessen (Köln nur die Deutzer Brücke). Gut
6 400 liefen 2026 in der **Staffel** (Runner's World, 26.04.2026); die drei Wechsel stehen in `D.marks`, der Kern zeigt damit den Staffel-Schalter.

## Termin und Start

Veranstalter D.SPORTS (D.LIVE GmbH & Co. KG, Düsseldorf), Namenssponsor Uniper seit 2025 (Comeback nach fünf Jahren Pause), offizieller
Name „Uniper Düsseldorf Marathon“ (https://www.uniper-duesseldorfmarathon.de/; `duesseldorfmarathon.de` leitet dorthin,
`duesseldorf-marathon.de` ist eine geparkte Domain). Nächste Austragung **Sonntag, 18. April 2027** (Seite „Wettbewerbe Marathon“,
`../dl/seiten/wettbewerbe_marathon.html`: „Datum: Sonntag, 18. April 2027 · Startzeit: 9:45 Uhr“; Startseite „am 18. April 2027“; Recap
vom 26.04.2026: „Im Jahr 2027 geht es … am 18. April erneut durch das Düsseldorfer Stadtgebiet“). Die letzte war am Sonntag, 26. April 2026.
`D.termine` `["2026-04-26", "2027-04-18"]` (2027 bestätigt, ohne „?“), `D.tz` Europe/Berlin, `D.start` = 585 (9:45). Kein `D.lage`,
`D.mauer`, `D.tor`, `D.zielschluss`.

**Start** (`D.wellen` ohne Wellenknöpfe, nur Text wie Honolulu): ein Start um 9:45 am Joseph-Beuys-Ufer, 2026 („Countdown“-Artikel von
D.SPORTS vom 24.04.2026, `../dl/seiten/dsports_der-countdown-…html`, und Vorbericht `../dl/pdf/2026-04-24-Preview.pdf`) wie 2027.
Startblöcke für den Marathon nennt der Veranstalter nicht. Halbmarathon 8:00/8:20/8:40 in drei Wellen (eigene Strecke), Staffel 10:15.
runinternational.eu nannte 9:30, das stimmt nicht. **Zielschluss** 15:45 Uhr (6 Stunden), Halbmarathon 11:40, Staffel 16:15 (2027;
2026 laut Countdown-Artikel 16:00); hinter dem Feld fährt ein Besenwagen. Steht im Text unter „Deine Startzeit“.

**Start und Ziel:** Start laut Plan auf dem Joseph-Beuys-Ufer am Ehrenhof (Kunstpalast), 190 m südlich der Cecilienallee; der
Veranstalter schreibt „auf Höhe der Tonhalle“ (die liegt 300 m weiter südlich am selben Ehrenhof). Ziel auf der Unteren Rheinwerft
„in Höhe der Adresse Rathausufer 19“ (Countdown-Artikel): der Zielpunkt des Plans liegt 42 m daneben unten am Fluss.

**Halbmarathon-Marke** bei 21 098 m (Zeitmessung laut Veranstalter an Start, 5, 10, 15, 21,0975, 25, 30, 35, „40,195“ km und Ziel; die
Halbmarathonmarke liegt in Oberkassel an der Luegallee). **Staffel** mit vier Etappen „ca. 11,2 / 13,1 / 9,2 / 9 km“, Wechselzonen
Fischerstraße, Steinstraße, Jacobistraße (Seite „Strecke Marathon-Staffel“).

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Reihenfolge: `parse.py`, `osm.py`, `georef.py`, `strecke.py`, `dgm.py`, `strassen.py`, `dom.py`, `clean.py`, `orte.py`, `stationen.py`,
`build.py`, `route.py`, `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py duesseldorf`, `duesseldorf/work/app.py` (beim ersten Mal über
`kern.py --neu duesseldorf work/felder.json`, danach ersetzt es nur die Felder und lässt Kartenbilder und `D.tiles` stehen),
`tiles_rand.py duesseldorf 2`. Nur Abgleich: `marken.py`. Prüfen: `pruefen.js` … `pruefen4.js` (Server auf Port 8792,
`NODE_PATH=/opt/node-tools/node_modules node pruefen.js`).

1. **Strecke** (`parse.py`): **Streckenplan Marathon 2026** des Veranstalters (A1, InDesign „Streckenplan.indd“ vom 15.04.2026, Logo
   „uniper DÜSSELDORF MARATHON“, Legende mit Kilometern, Erste Hilfe, Erfrischungs- und Verpflegungspunkten, Staffelwechselzonen, DJs,
   Cheering Zones, Umfahrung). Auf der Seite des Veranstalters steht heute nur noch die Beschreibung (`/strecke/marathon`, ohne Karte);
   die Datei kommt von einer Ergebnisseite, die sie im April 2026 übernommen hat
   (https://www.sportsidioten.no/wp-content/uploads/2026/04/Streckenplan_Marathon.pdf, `../dl/pdf/Streckenplan_Marathon_sportsidioten.pdf`).
   Die Karte ist ganz aus Vektoren; die Strecke ist **ein roter Pfad** (Farbe 0,93/0,11/0,14, 3,62 pt, 783 Geraden, durchgehend vom
   START-Punkt bis zum ZIEL-Punkt), daneben 42 Kilometerschilder. **Gegenprobe:** Tour „Uniper Düsseldorf Marathon 2026“ von Visit
   Düsseldorf (Düsseldorf Tourismus GmbH, toubiz; angelegt 08.04.2025, geändert 20.04.2026, „free_draw“, 945 Punkte, 42 233 m laut Tour,
   https://www.visitduesseldorf.de/poi/detail/uniper-duesseldorf-marathon-2026-fcc86d8a2e, Linie als GeoJSON in der Seite,
   `../dl/toubiz/`). Ein Wayback-Abruf der früheren Streckenseite war nicht möglich (web.archive.org: Verbindung abgebrochen).
2. `osm.py` (wie Stockholm): OSM-API in 117 Rechtecken zu 0,005° höchstens 150 m neben der Tour, eine Abfrage je Sekunde, keine
   Fehler → `../dl/osm_netz.json` (15 611 Wege).
3. `georef.py`: **Einpassung** der PDF-Punkte nach ETRS89/UTM 32N, affin (die Karte im PDF ist nicht winkeltreu: 4,068 m/pt waagerecht,
   4,252 m/pt senkrecht): erst an der Tour, dann ICP an allen OSM-Wegen (jeder Planpunkt zum nächsten Straßenpunkt bis 20 m). Ergebnis:
   Planlinie **im Median 2,1 m neben einer OSM-Straße, 90 % bis 5,0 m**, 99 % bis 8,3 m; einzelne gerundete Ecken bis 16 m (km 5,8,
   28,3). Die Tour liegt im Median 1,2 m neben dem eingepassten Plan (90 % 3,1 m; nur ihr Anfang 54 m weiter nördlich): sie ist offenbar
   nach dem Plan gezeichnet, bestätigt aber Lage und Weg.
   Verworfen: die Linie über das OSM-Netz auf die Straßenmitten legen (Kartenabgleich mit Wegpunkten alle 120 m): 43,31 km, Zickzack über
   Rad- und Gehwege und eckige Kreuzungen. Die gezeichnete Linie rundet Ecken wie die vermessene Ideallinie.
4. `strecke.py` → `strecke2026.json` (784 Punkte, **42 392,7 m** geodätisch, also 0,47 % zu lang; Hin- und Rückweg auf derselben Straße
   sind im Plan zwei parallele Linien). `common.py`: **Kilometer gleichmäßig** (Faktor 0,99534), Start am Linienanfang, Ziel am Ende.
   `marken.py`: Die 42 Kilometerschilder stehen ohne Strich 15–40 pt neben der Linie; Lotfußpunkt der Kastenmitte gegen die gestreckte
   Linie: Abweichung im Median −6 m, |Abweichung| im Median 16 m, 90 % bis 54 m, höchstens 136 m; keine Drift über die Strecke
   (km 1–10 −21 m, 11–21 +3, 22–31 −37, 32–42 −2). **Genauigkeit der Kilometer etwa ±0,1 km.**
5. `dgm.py` (Kopie Köln): **DGM1 NRW** über WCS (`www.wcs.nrw.de/geobasis/wcs_nw_dgm`, Coverage `nw_dgm`, EPSG:25832), 4241 Punkte in 140
   Ausschnitten, 32 s, keiner fehlt. Lizenz dl-de/zero-2-0.
6. `strassen.py` (Kopie Stockholm, UTM 32N): je 10 m der nächste OSM-Weg bis 20 m mit höchstens 35° Richtungsabweichung, Hauptstraßen
   bevorzugt. Der **Rheinufertunnel** ist ausgenommen: Die Strecke läuft am Ende oben auf der Promenade, der Tunnel liegt darunter.
7. `dom.py`: **Brücken aus dem DOM1 NRW** (WCS `wcs_nw_dom`, Coverage `nw_dom`) wie die Deutzer Brücke in Köln, aber für alle elf Stellen,
   an denen das DGM springt; je 10-m-Punkt Lotfußpunkt auf den OSM-Weg von `strassen.py` (die gezeichnete Linie liegt bis 16 m daneben),
   dort das 25-%-Quantil der 5 × 5 m. An allen Enden DOM gleich DGM (±0,2 m), größte Stufe 0,44 m je 10 m (`dom.log`):
   **Oberkasseler Brücke** zweimal (km 13,03–13,76 nach Westen, 22,02–22,74 nach Osten; DGM 28 m = Rhein, DOM 40,3–46,9 m),
   Jülicher Brücke über die Bahn (27,35–27,60; DGM 31,9, DOM bis 46,1), Am Wehrhahn über die Bahn (32,16–32,32; DOM bis 44,5),
   Benrather Straße über den Kö-Graben (23,97–24,07 und 40,38–40,47), Jacobistraße über die Nördliche Düssel (33,32–33,50),
   Maximilian-Weyhe-Allee über die Fußgängerunterführung Weyhepassage (12,46–12,56 und 24,93–25,04), Hofgartenrampe über eine
   Fußgängerunterführung neben der Stadtbahnrampe (12,86–12,95 und 22,82–22,91). Alle gelten als gemessen (nicht schraffiert).
   Die Strecke führt über **keine** weitere Rheinbrücke: Die Rheinkniebrücke kreuzt sie nur (Reichsstraße läuft bei km 35,8 unter der
   Rampe durch), die Theodor-Heuss-Brücke berührt sie an ihrem Westende (Daten 9).
8. `clean.py` (Kopie Köln): setzt die DOM-Werte ein, dann Stufen über 1,5 m je 10 m → Gerade. Übrig bleibt eine Stelle: **Unterführung
   der Ernst-Gnoß-Straße unter dem Stadttor** (km 38,46–38,52, OSM `tunnel=yes`, `layer=-1`; das DGM misst den Platz darüber, 43,8 m),
   Gerade 37,1 → 36,5 m, **geschätzt** (`D.bridges`, schraffiert).
9. `orte.py` (Kopie Stockholm): **Stadtteile** alle 100 m aus den 50 Düsseldorfer Stadtteilen (OSM `admin_level` 10, 20 Flächen über die
   OSM-API, `../dl/orte/`), je 40 m links und rechts, bei zwei Stadtteilen „links / rechts“: Pempelfort, Golzheim, Stockum, Derendorf,
   Altstadt, Oberkassel, Lörick, Niederkassel, Stadtmitte, Düsseltal, Friedrichstadt, Unterbilk, Hafen, Carlstadt.
10. `stationen.py`: **Marken aus dem Plan**: Kreise in den Farben der Legende (Verpflegungspunkt dunkelblau 0,13/0,17/0,36,
    Erfrischungspunkt blau 0,22/0,46/0,73, Staffelwechselzone grün 0,27/0,72/0,36), Lotfußpunkt der Kreismitte. Wo die Strecke
    mehrmals in Reichweite liegt, ist der Durchgang von Hand gewählt (Liste `WAHL`): Luegallee km 22,0 statt 13,8 oder 19,3 (Symbol auf
    der Seite der Fahrbahn nach Osten, Wechsel Verpflegung/Erfrischung etwa alle 2,5 km), Heinrich-Heine-Allee 24,7 statt 23,4,
    Königsallee 40,1 statt 34,6, Kaiserstraße 12,2 statt 25,1, Fischerstraße 11,3 statt Klever Straße 7,3. Die Bilder dazu lagen der
    Entscheidung zugrunde (Ausschnitte des PDF). **Lage etwa ±0,2 km**, in der App „ca.“.
    - 8 Verpflegungspunkte (food): km 4,5 Kaiserswerther Straße (am Aquazoo, wie der Veranstalter schreibt: „nach ca. 5 Kilometern in
      Höhe des Aquazoos“), 10,0 Ulmenstraße, 14,9 Hansaallee, 19,9 Düsseldorfer Straße, 24,7 Heinrich-Heine-Allee, 30,5 Lindemannstraße,
      35,4 Herzogstraße, 40,1 Königsallee.
    - 6 Erfrischungspunkte (water, „Erfrischung“): km 12,2 Kaiserstraße, 16,4 Am Seestern, 22,0 Luegallee, 27,0 Jülicher Straße,
      32,5 Adlerstraße, 37,5 Gladbacher Straße.
    - 3 Staffelwechsel (relay): km 11,3 Fischerstraße, 24,2 Steinstraße/Königsallee, 33,3 Jacobistraße (Etappen danach 11,3 / 12,8 /
      9,2 / 8,9 km; Veranstalter „ca. 11,2 / 13,1 / 9,2 / 9“).
    Was es an den Punkten gibt, sagt der Veranstalter nicht („Eine genaue Übersicht stellen wir Dir rechtzeitig vor dem Event zur
    Verfügung“). Nicht übernommen: Erste Hilfe, DJs (39), Cheering Zones, Spendentor, Diabetespunkte, Hotspots der Sponsoren.
11. `build.py`: Höhen in cm im 10-m-Raster, Median über 30 m; Straßenstücke unter 80 m und Stadtteile unter 300 m dem Vorgänger
    zugeschlagen. Die Fahrbahnen der Oberkasseler Brücke heißen in OSM nicht (Wege 142750745, 369744127) → „Oberkasseler Brücke“; ab
    km 41,76 (Weg ohne Namen von der Promenade hinunter an den Fluss) und auf der OSM-„Rheinwerft“ steht „Untere Rheinwerft“ wie beim
    Veranstalter. `route.py` (lat0/lon0 51,2/6,7), `tiles.py` (z12–z15), `tiles_z11.py duesseldorf`, `app.py`,
    `tiles_rand.py duesseldorf 2`: 19 Kartenstücke, 2,1 MB.

## Ergebnis

↑ 79 m / ↓ 81 m mit 200-m-Fenster, ↑ 95 / ↓ 98 m mit 50 m, ↑ 89 / ↓ 92 m mit 100 m, ↑ 39 / ↓ 41 m mit 1 km; wie GPS-Uhren 73 (ab 0,5 m),
62 (ab 1 m), 31 (ab 3 m); Rohdaten ↑ 131 m. Start 35,3 m am Joseph-Beuys-Ufer, Ziel 32,7 m auf der Unteren Rheinwerft; tiefster Punkt
32,5 m auf der Rheinwerft kurz vor dem Ziel (km 41,94), höchster 46,9 m in der Mitte der Oberkasseler Brücke (km 22,41; nach Westen
46,8 m bei km 13,4); **Höhenbereich 14,4 m**. Fast eben (34–38 m) am Rhein nach Norden bis Stockum und zurück durch Derendorf; spürbar
sind nur die Bauwerke: Oberkasseler Brücke vom Hofgarten 9 m hinauf und nach Oberkassel hinunter (km 12,9–13,9), am Westende der
Theodor-Heuss-Brücke über die Rampen von Lütticher und Brüsseler Straße 6 m hinauf und wieder hinunter (km 16,8–17,5, −3,1 % über 200 m
bei km 17,3, die steilste Stelle bergab), zurück über die Oberkasseler Brücke 11 m hinauf (**+2,9 % über 200 m bei km 22,0, die
steilste Stelle**), Jülicher Brücke (km 27,4) und Am Wehrhahn (km 32,2) über die Bahn je etwa 5 m, zuletzt von der Promenade 4 m hinunter
auf die Untere Rheinwerft (−5,6 % über 50 m bei km 41,8).
**Modellzeit:** Mit 4:00/km im Flachen ergibt das Modell **2:49:24** (das Profil kostet 37 s); **bei 2:50:00 kostet es 37 s, bei 4:00:00
52 s** (Flach-Pace 4:00,9 bzw. 5:40,0 /km; gemessen mit `pruefen.js` in der App 2.3). Zum Vergleich bei 4:00/km im Flachen: Köln 48 s.

Geprüft mit Playwright (Chromium, 393 × 852, Faktor 2, Server auf Port 8792, `pruefen.js` … `pruefen4.js`): keine Konsolenfehler,
`APP_VERSION` 2.3 und Knopf v2.3, Service Worker installiert (25 Einträge im Cache `dus-marathon-profil`), Tipp auf die Version meldet
„Version 2.3 ist aktuell“; alle 19 Kartenstücke passen zu `D.tiles` und `sw.js`; Tabellen bei 320/375/393/430 px ohne Überbreite, Seite
nicht breiter als das Fenster. Laufansicht am Start, km 4,5 (Aquazoo), 13,3 (Oberkasseler Brücke), 17,1 (Rampe Lütticher Straße), 22,4
(höchster Punkt), 27,5 (Jülicher Brücke), 38,48 (Stadttor), 41,85 (Rheinwerft), 42,1 (Ziel) und die Kartenübersicht mit Verpflegung und
Staffel bei km 24 angesehen; Zuschauer-Tabelle mit 18. April 2027 und „Ortszeit Berlin“; Kopf und „Woher die Zahlen kommen“ angesehen.
Bilder in `work/shots/`. `kern.py` meldet alle Apps „gleich“, dazu „karten.json veraltet“ (neue Strecke, Hauptsitzung).

## Offen

- Prüfung am iPhone.
- **Kurs 2027:** Plan noch nicht veröffentlicht. Die Beschreibung auf der Seite „Strecke Marathon“ (Stand 2027: Oberkasseler Brücke
  nach etwa 13 km, Schleife durch Oberkassel mit der Halbmarathonmarke, Königsallee, Zoopark, Medienhafen, zweite Kö-Schleife, Ziel
  Untere Rheinwerft) und die Etappen der Staffel passen zum Plan 2026. Kommt ein neuer Plan, `parse.py` (Pfad der Datei) und die Kette
  erneut laufen lassen; die Farbe des Pfads und die Liste `WAHL` in `stationen.py` prüfen.
- Die Linie ist eine Zeichnung (kein GPX, keine Vermessung); der Streckenplan stammt aus einer Kopie auf sportsidioten.no, nicht direkt
  vom Veranstalter (Logo, Sponsoren und Datum passen; Visit Düsseldorf zeigt dieselbe Linie).
- Start: Plan am Ehrenhof (Kunstpalast), Veranstalter „auf Höhe der Tonhalle“ (300 m weiter südlich). Ob die Startlinie 2027 anders
  liegt, steht noch nicht fest.
- Verpflegung: nur Lage und Art aus dem Plan, kein Angebot; die Erfrischung an der Luegallee (km 22,0) könnte auch zum Durchgang bei
  km 13,8 oder 19,3 gehören.
- Startseite: Karte fehlt. Eyebrow „Uniper Düsseldorf Marathon“, Stadt „Düsseldorf“, „Kurs 2026“, `data-termine="2026-04-26 2027-04-18"`,
  `data-monat="4"`, Termintext „So., 18. April 2027“, ↑ 79 m / ↓ 81 m, Höhe 32–47 m, `data-such` z. B. „Duesseldorf Dusseldorf
  Nordrhein-Westfalen NRW Deutschland Uniper Rhein“; Mini-Profil mit 14 m Höhenbereich passt in die Grundhöhe 64 px. README-Tabelle und
  Liste der Präfixe (`dus-`). Höhenquelle im Fuß: „DGM1 … NRW“ steht dort schon (Köln); neu ist nur das DOM1 NRW für die Brücken
  (gleiche Quelle und Lizenz, © Geobasis NRW, dl-de/zero-2-0).
  **Teilnehmer 2026:** **4 145 im Ziel** des Marathons (offizielle Ergebnisliste „Uniper Düsseldorf Marathon 2026“, RaceResult-Veranstaltung
  387844, eingebunden über den Anmeldedienst des Veranstalters datasport: `datasport.de/module/ergebnisse_iframe.php?id=3009`;
  Liste „Ergebnisliste MW“ mit 4 297 Einträgen, davon 4 145 mit Zielzeit und 152 DNF; ausgezählt ohne Namen zu speichern), gleiche Zahl
  bei runinternational.eu; Runner's World nannte „etwa 4.300“. Halbmarathon 9 548 im Ziel, Staffel 1 590 Teams
  (beides runinternational). 2025: 3 270 im Ziel (runinternational).
- Termine 2028 ff.: jährlich nachtragen (Frühjahr, 2026 und 2027 jeweils im April).
