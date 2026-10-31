# Übergabe: Steigungsprofil Gornergrat Zermatt Marathon

Stand 31.10.2026, App-Version **2.5** (erste Fassung, angelegt mit `werkzeuge/kern/kern.py --neu` auf dem gemeinsamen Kern; die
Hauptsitzung zählt die Nummer beim Veröffentlichen hoch).
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/zermatt/.

Die App hat den gemeinsamen Kern aus `hamburg/` und eigene Felder (Texte, `const D`, Speicherschlüssel `zgm-…`, Service-Worker-Cache
`zgm-marathon-profil`, löscht nur Caches mit Präfix `zgm-`; der Präfix war frei, `kern.py --neu` prüft das), ohne eigenes Manifest und
Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Startseite,
README, `version.json` und `karten.json` sind noch nicht angepasst (Hauptsitzung).

**Besonderheiten:** Erster Bergmarathon mit swisstopo-Daten, gebaut nach dem Muster Luzern/Zürich. Punkt-zu-Punkt von St. Niklaus
(1100 m) durch das Mattertal nach Zermatt und hinauf zum Riffelberg (2575 m im Ziel, höchster Punkt 2584,5 m kurz davor), Strasse,
Fahrweg und Bergweg; **Höhenbereich 1484 m**, das Zehnfache von Rennsteig. Höhen aus **swissALTI3D 0,5 m**, Brückenfahrbahnen aus
**swissSURFACE3D Raster**, beide über `work/swissalti.py` (Kopie von `../zuerich/work/swissalti.py`, nur der Zwischenspeicher liegt hier).
Die Linie ist die **GPX-Datei des Veranstalters** „GZM Marathon 2026“. Neu gegenüber Luzern: **41 Stichwege hin und zurück** in der
GPX-Datei entfernt (`parse.py`), Kilometer **gleichmässig gedehnt** (keine Kilometermarken), Brückensuche für steile Wege umgebaut
(`clean.py`), Orte am Berg aus **swissNAMES3D** (`namen3d.py`, `orte.py`), Wege ohne Namen nach ihrer Art (`build.py`).
Das Pace-Modell ist an Strassenmarathons geeicht und am Berg zu optimistisch (siehe „Modellzeit“); den Hinweis dazu baut die
Hauptsitzung in den Kern, die Texte hier sagen nur „Bergmarathon mit Gehpassagen“.

## Termin und Start

Offizieller Name **Gornergrat Zermatt Marathon** (Reglement, Datasport, Seite „Marathon“: „Der Gornergrat Zermatt Marathon gilt als einer
der schönsten …“; Titelpartner Gornergrat Bahn; Veranstalter Verein Zermatt Marathon; die Website heisst „Zermatt Marathon“). Zuletzt am
**Samstag, 4. Juli 2026** (Seite „Marathon“: „Am 4. Juli 2026 führt die Strecke von St. Niklaus …“; Datasport-Anlass
„gornergrat-zermatt-marathon-2026“, 03.–04.07.2026, Marathon am Samstag; Race Magazin „3. / 4. Juli 2026“). Nächster am **Samstag,
3. Juli 2027** (Seite „Startzeiten“ und Seite „Marathon“: „Startzeiten in St. Niklaus 1120 m ü. M · Samstag, 3. Juli 2027“; Startnummern
„Donnerstag 1. Juli … Samstag 3. Juli“, passt zu 2027; Anmeldung „registration.datasport.com/de/gornergrat-zermatt-marathon-2027“ auf der
Seite „Ranglisten & Urkunden“). Immer am ersten Juli-Wochenende. `D.termine` `["2026-07-04", "2027-07-03"]`, `D.tz` Europe/Zurich,
`D.ort` „Zermatt“ und `D.ortKurz` „ Zermatt“, `D.start` = 510 (8:30). Kein `D.lage`, `D.mauer`, `D.tor`, `D.zielschluss`. Seiten des
Veranstalters in `dl/seiten/` (lokal), Abruf mit `work/seite.py`; Race Magazin 2026 und Verpflegungsplan in `dl/pdf/`.

**Start** (`D.wellen`, zwei Knöpfe): 8:30 „Elite Runner sowie Block 1 für Marathon + ULTRA“, „ab 8:33 Uhr Blockstarts Marathon + ULTRA“
(Seite „Startzeiten“ für 2027); das Race Magazin 2026 (S. 27) zeigt dazu zwei Startfelder: 8:30 ELITE, MARATHON Block 1, ULTRA Block 1;
8:33 MARATHON Block 2, ULTRA Block 2. Ausser bei Elite und Block 1 zählt die Nettozeit ab der Startlinie (Seite „Start- und
Zielbereich“; Reglement Ziffer 28 sagt es umgekehrt herum: für Elite und Block 1 gilt der Startschuss). Start auf der Umfahrungsstrasse
in St. Niklaus; die GPX-Linie beginnt auf der Talstrasse im Norden des Dorfs auf 1100,5 m (Veranstalter: „Start in St. Niklaus 1’116 m“,
„Startzeiten in St. Niklaus 1120 m ü. M“; das sind wohl Höhen des Dorfs). Halbmarathon (Start Zermatt, Obere Matten, 10:12–10:27) und
TOP20RUN (Zermatt–Gornergrat) sind eigene Rennen; der **Ultra** (45,6 km) läuft dieselbe Strecke und am Riffelberg weiter auf den
Gornergrat (3089 m), er ist hier nur erwähnt.

**Zeitlimits** (Seite „Streckenverpflegung & Kontrollzeiten“, Reglement Ziffer 8, Race Magazin 2026), im Text unter „Deine Startzeit“:
Kontrollschluss Zermatt Bahnhofplatz 11:50 Uhr (Veranstalter km 21,1, hier km 20,6), Restaurant Sunnegga 13:45 Uhr (Veranstalter km
32,4, im Reglement 31,7, hier 32,0), Hotel Riffelalp Resort 14:55 Uhr (km 39,1, hier ebenso), Abzweigung Ultra 15:15 Uhr, Zielschluss
Marathon auf dem Riffelberg 15:45 Uhr. Wer später durchkommt, wird nicht mehr klassiert und hat keinen Anspruch auf Verpflegung, Sanität
und Auszeichnung; wer weiterläuft, bekommt eine Filzstift-Markierung auf die Startnummer. Stöcke verboten (Reglement Ziffer 4).

**Keine Staffel:** Die Karte im Race Magazin nennt am Riffelberg noch „Marathon-Staffel“ und in Zermatt „Staffelwechsel“, die
Rangliste 2026 hat aber keine Staffel (Wettbewerbe Marathon, Ultra, Halbmarathon, TOP20RUN, Kinderläufe). Also keine `relay`-Marken.
**Halbmarathon-Marke** bei 21 098 m.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Reihenfolge: `parse.py`, `osm.py`, `strassen.py`, `bedeckt.py`, `dgm.py` (mit `swissalti.py`), `deck.py`, `clean.py`, `namen3d.py`,
`orte.py`, `build.py`, `route.py`, `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py zermatt` (der Ordner `../zermatt/` muss es geben),
`zermatt/work/app.py` (beim ersten Mal über `kern.py --neu zermatt work/felder.json`, danach ersetzt es nur die Felder und lässt
Kartenbilder und `D.tiles` stehen), `tiles_rand.py zermatt 2`. Nur Abgleich: `vergleich.py`; zum Nachsehen `wege.py <von> <bis> [m]`
(OSM-Wege neben der Linie, Linienmeter), `seite.py` (Seiten des Veranstalters als Text). Prüfen: `pruefen.js`, `pruefen2.js`,
`pruefen3.js` (Server auf Port 8792 im Repo-Wurzelordner, `NODE_PATH=/opt/node-tools/node_modules node pruefen.js`).

1. **Strecke** (`parse.py`): Download „GZM Marathon 2026.gpx“ auf der Seite „Marathon“
   (`https://www.zermattmarathon.ch/writable/media/1757489222-GZM_Marathon_2026.gpx`, hochgeladen 10.09.2025; `?action=get_file&id=30`
   liefert dieselbe Datei), erstellt mit MySchweizMobil, 7199 Punkte mit Höhen, roh 42 620 m. Entfernt: doppelte und um bis 1 m versetzte
   Punkte wie in Zürich und Luzern, dazu **41 Stichwege**, die die Linie bis zu einem Zwischenpunkt und auf demselben Weg zurück geht
   (3–32 m lang, zusammen 636 m; Spitze b mit a ≈ c auf 1,5 m). Danach 4251 Punkte, **41 621 m**, keine Kehrtwenden mehr. Die
   Halbmarathon-Datei („GZM Halbmarathon 2026“) beginnt am Bahnhofplatz Zermatt und liegt bis ins Ziel auf derselben Linie (alle Punkte
   bis 15 m, Start 27 m daneben).
2. **Kilometer** (`common.py`): Kilometermarken veröffentlicht der Veranstalter nicht, und seine Kilometer widersprechen sich (Sunnegga
   31,7 im Reglement, 32,0 im Verpflegungsplan, 32,4 bei den Kontrollzeiten, 32,5 auf der Karte im Race Magazin). Mehrere seiner Werte
   folgen der **Länge der Rohdatei mit den Stichwegen** (Zermatt Bahnhofplatz dort genau 21,10, Sunnegga 32,36, Patrullarve 28,65), die
   insgesamt aber 42,62 km lang ist. Die Linie ohne Stichwege ist 41,62 km, also **gleichmässig um 1,38 % gedehnt** (wie Rennsteig).
   Damit treffen der Verpflegungsplan (Herbriggen 5,0 auf 1235 m, Randa 10,0 auf 1410, Zermatt 20,3 auf 1604, Sunnegga 32,0 auf 2262,
   Riffelalp 39,0 auf 2222: Linie dort 1234,8 / 1409,4 / 1604,9 / 2256 / 2218 m) und die Kontrolle Hotel Riffelalp (39,1; Haltestelle
   „Riffelalp, Hotel“ hier bei 39,10). Nicht passend: Zermatt Bahnhofplatz hier 20,6 statt 21,1, Grünsee 35,6 statt 36,7.
3. `osm.py`: OSM über die API in 139 Rechtecken zu 0,005° höchstens 150 m neben der Linie, eine Abfrage je Sekunde (`../dl/osmapi/`) →
   `../dl/osm_netz.json` (2485 Wege). `strassen.py` wie Luzern, mit Bergwegen (path, track, footway, bridleway). In OSM haben viele Wege
   keinen Namen; `build.py` benennt sie nach Art: „Nebenstrasse“ (Strasse mit Belag), „Fahrweg“ (track, Kiesstrasse), „Bergweg“ (Pfad mit
   `sac_scale` ab mountain_hiking), „Wanderweg“, „Fussweg“. Flurnamen als Wegname in OSM („Ried“, „Grüebe“, „Tuftra“, „Balmbrunnen“,
   „Aroleit“) zählen als Weg ohne Namen. Die letzten 100 m heissen „Ziel Riffelberg“ (in OSM ohne Weg). Kurze Stücke unter 80 m gehen im
   Vorgänger auf. Namen der Wanderrouten (5-Seenweg, Edelweissweg, Tour Monte Rosa) stehen nur in OSM-Relationen und sind nicht verwendet.
4. **Orte** (`namen3d.py`, `orte.py`): Gemeinden aus swissBOUNDARIES3D (St. Niklaus, Randa, Täsch, Zermatt; `../dl/orte/gem_*.json`),
   Orte aus **swissNAMES3D** (geo.admin.ch `identify`, Ebene `ch.swisstopo.swissnames3d`, 51 Kacheln zu 1 km, `../dl/orte/names3d_*.json`):
   Siedlungen („Ort“) höchstens 60 m neben der Linie (Mattsand, Herbriggen, Breitmatten, Riffelalp …), sonst der nächste Lokalname, See
   oder Bahnhalt bis 250 m (Ried, Patrullarve, In den Brüchen, Sunnegga, Leisee, Grindjesee, Grüensee, Bodmen, Riffelberg). Nur offizielle
   Namen (sonst stand „Praborgne“, das französische Exonym, für ganz Zermatt). Quartierteile zählen nicht. Angezeigt „Zermatt, Sunnegga“.
5. `swissalti.py`, `dgm.py`: **Höhe aus swissALTI3D 0,5 m**, alle 10 Linienmeter bilinear (4164 Punkte), dazu 2 m und die GPX-Höhen zum
   Vergleich (`dgm_vergleich.json`). 38 Kacheln, alle Jahrgang 2024. Höhen in m ü. M. (LN02). Die GPX-Höhen (MySchweizMobil) liegen im
   Median 7 cm darüber, 95 % innerhalb ±0,7 m, und laufen auch über Brücken richtig: Sie kommen offenbar aus dem 3D-Wegnetz von swisstopo.
6. **Überdeckt** (`bedeckt.py`, `clean.py`): Nur die Unterführung des Fusswegs in Randa (km 10,50–10,54, OSM `tunnel=yes`, `layer=-1`):
   Modell bis 1406,8 m, Gerade 1406,3 → 1406,4 m, schraffiert (`D.bridges`, „Unterführung Randa“). Die GPX-Höhen liegen dort 2 m tiefer
   (1404,1 m): Die Unterführung taucht wohl ab; als Gerade gezählt fehlen also bis 2 Höhenmeter. Tunnel und Galerien der Bahn und der
   Strasse liegen unter oder neben der Strecke.
7. **Brücken** (`deck.py`, `clean.py`): Am Hang taugt der Median der Umgebung (Luzern) nicht; Kandidaten sind OSM-Brücken und Senken unter
   der Geraden über ±60 m. Eine erste Fassung zog Geraden über ganze Senken und lag damit an der Gornera bis 9 m über der GPX-Höhe.
   Jetzt: Brücke = Stück bis 120 m, auf dem **swissSURFACE3D** (Jahrgang 2021/2022, 30 Kacheln, 25-%-Quantil von 5 × 5 Werten) glatt ist
   (Mitte und Quantil auf 1 m gleich), mehr als 0,8 m über dem Geländemodell liegt, auf 1,5 m auf der Geraden zwischen den Bodenpunkten
   davor und danach bleibt und das Geländemodell darunter mehr als 0,8 m absinkt; Enden bis zum nächsten Bodenpunkt verlängert. Gefunden
   **15 Brücken, alle gemessen und alle auch in OSM**: Matter Vispa sechsmal (km 3,3, 4,1, 6,7, 10,8, 11,6, 22,9), Spisszug (1,25),
   Blattbach (2,9), Dorfbächji in Randa (9,2), Zmuttbach (22,3), Gornera (22,45, Senke 9,6 m), Findelbach (22,7 und 34,75), dazu zwei
   Fahrwegbrücken an der Gornergratbahn (38,45 bei Riffelalp, 40,34 bei Riffelboden). Fahrbahn gegen GPX-Höhe höchstens 1 m daneben.
   Danach weichen App und GPX-Höhe nur noch an kurzen Stellen über 1,5 m ab (Wegrand am Hang, z. B. km 36,7–36,95 bis 3,7 m; eine Mauer
   bei km 20,02, die der 30-m-Median schluckt).
8. `build.py`: **Verpflegung** nach dem Verpflegungsplan (Seite „Streckenverpflegung & Kontrollzeiten“, Tabelle mit km, Höhe und Angebot;
   `../dl/pdf/Verpflegungsplan.pdf` ist ein Bild). Im Tal an der Plan-km: Herbriggen 5,0 (Wasser, ISO, Schwamm: „Getränke“), Randa 10,0,
   Täsch 14,3, Zermatt 20,3 und 24,5. Am Berg sagt die Höhe mehr als die km: Posten dort, wo die Linie höchstens 0,6 km neben der Plan-km
   die Planhöhe trifft: Chalet Ried 26,5 (Plan 26,8; nur Wasser, „zusätzlicher Wasserposten“), Patrullarve 28,3 (28,6), Sunnegga 31,9,
   Riffelalp 39,2 (39,0), Riffelboden 40,3 (40,4). **Grünsee** steht im Plan bei km 36,7 auf 2300 m; dort liegt die Linie auf 2239 m,
   unterhalb des Sees. Gesetzt am See (km 35,6, Linie 2289 m). Start (Wasser, Tee) und Riffelberg (km 42,0, Ziel) nicht als Marke.
   Angebot im Namen der Marke (Wasser, ISO, Cola, Tee, Bouillon, Banane, Gel, Riegel, Schwamm; Gel und Riegel von Powerbar). Höhen in cm im
   10-m-Raster, Median über 30 m; Orte unter 300 m dem Vorgänger zugeschlagen. `route.py` (lat0/lon0 46,0/7,7), `tiles.py` (z12–z15),
   `tiles_z11.py zermatt`, `app.py`, `tiles_rand.py zermatt 2`: 30 Kartenstücke, 2,1 MB.

   **Abgleich** (`vergleich.py`, Verfahren wie die App; vorletzte Spalte vor „gegen App“: einfache Summe aller Anstiege):

   | Quelle | Start | Ziel | min (km) | max (km) | ↑/↓ 200 m | ↑ 100 m | ↑ 50 m | ↑ 1 km | ↑ Punkt für Punkt | gegen App (Median) | r |
   |---|---|---|---|---|---|---|---|---|---|---|---|
   | App (swissALTI3D 0,5 m, Brücken aus swissSURFACE3D) | 1100,5 | 2574,6 | 1100,5 (0,00) | 2584,5 (41,98) | 1816/342 | 1879 | 1924 | 1641 | 2050 | – | – |
   | swissALTI3D 0,5 m ohne Bereinigung | 1100,5 | 2574,6 | 1100,5 (0,00) | 2584,5 (41,98) | 1818/344 | 1886 | 1939 | 1641 | 2125 | ±0,00 | 1,0000 |
   | swissALTI3D 2 m, gleiche Brücken | 1100,5 | 2574,6 | 1100,5 (0,00) | 2584,5 (41,98) | 1816/342 | 1879 | 1924 | 1641 | 2055 | +0,01 | 1,0000 |
   | GPX-Höhen des Veranstalters (MySchweizMobil, ohne Stichwege) | 1100,8 | 2574,7 | 1100,8 (0,00) | 2584,1 (41,97) | 1815/341 | 1878 | 1924 | 1641 | 2046 | +0,07 | 1,0000 |
   | GPX-Rohdatei mit Stichwegen | | | | | | | | | **2075** | | |

## Höhenmeter: 2075?

Der Veranstalter nennt „2'075 Höhenmeter Aufstieg“ (Seite „Marathon“). Das ist **genau die Summe Punkt für Punkt seiner GPX-Rohdatei
(2074,6 m)**, samt der 41 Stichwege. Ohne sie zählt die Datei 2046 m, das Laser-Modell 2050 m (10-m-Raster, bereinigt). Mit dem
Messfenster der App sind es **1816 m (200 m)**, 1879 m (100 m), 1924 m (50 m); wie GPS-Uhren (Anstieg ab 0,5 / 1 / 3 m) 1947 / 1921 /
1864 m. Die „1469 Höhenmeter“ auf der Seite „Start- und Zielbereich“ sind Ziel minus Start (2585 − 1116). Unten liegt die Grenze bei
1474 m (Ziel minus Start in der App), bergab kommen 342 m dazu.

## Ergebnis

↑ 1816 m / ↓ 342 m mit 200-m-Fenster, ↑ 1924 / ↓ 450 m mit 50 m, ↑ 1879 / ↓ 405 m mit 100 m, ↑ 1641 / ↓ 165 m mit 1 km; Rohdaten ↑ 2050 m.
Start 1100,5 m auf der Talstrasse in St. Niklaus, Ziel 2574,9 m auf dem Riffelberg, höchster Punkt 2584,5 m kurz vor dem Ziel (km 41,98),
tiefster der Start; **Höhenbereich 1484 m**. Steigung über 200 m: **6,75 km steiler als +10 %, 1,94 km steiler als +15 %**, 0,29 km steiler
als +20 % (bergab 0,70 km steiler als −10 %, keiner steiler als −15 %). Steilste Stellen +21,2 % bei km 39,3 und +21,0 % bei km 40,9 (beide
Riffelalp–Riffelberg), +19,1 % bei km 16,5 (Bergweg nach Täsch), +17,3 % bei km 32,85 (nach dem Leisee); bergab −14,3 % bei km 33,7.
Verlauf: an der Matter Vispa über Mattsand nach Herbriggen (1235 m, km 5; +2,7 %), auf der Alten Kantonsstrasse hinauf nach Randa (1418 m
bei km 9,2), fast eben bis Täsch (1435 m, km 14,3), ab km 16 auf dem Bergweg über zwei Kuppen hinauf auf 1632 m (km 19,9) und hinunter nach Zermatt (1605 m,
Bahnhofplatz km 20,6). Schleife durch Zermatt über Zmuttbach und Gornera (1646 m, km 22,1) zurück zur Kirche (1603 m, km 23,8), dann der
lange Anstieg über Ried (1803 m, km 26,5) und Patrullarve (2001 m, km 28,3) nach Sunnegga (2263 m, km 31,9): 660 m auf 8,1 km. Am Leisee
hinab auf 2209 m (km 32,6), steil hinauf auf 2362 m (km 33,6), Grünsee (2289 m, km 35,6), hinab nach Riffelalp (2209 m, km 38,7) und auf den
letzten 3,5 km 376 m hinauf zum Riffelberg.

**Modellzeit** (gemessen mit `pruefen.js` in der App 2.5): Mit 4:00/km im Flachen ergibt das Modell **3:24:31** (das Profil kostet
35:44 min); **bei 2:50:00 kostet es 29:43 min, bei 4:00:00 41:57 min** (Flach-Pace 3:19,5 bzw. 4:41,6 /km). Zum Vergleich mit
4:00/km im Flachen: Rennsteig 8:35 min, Luzern 108 s. Das Modell ist hier **zu optimistisch**: 2026 lief der Sieger 3:02:18, die Siegerin 3:35:59, der Median
der 355 Finisher 5:47:33 (Quartile 5:05 und 6:25, letzter 7:18). Die Zwischenzeiten zeigen, wo: Median-Anteile Start–Zermatt 39,8 %,
Zermatt–Sunnegga 29,5 %, Sunnegga–Riffelalp 17,2 %, Riffelalp–Ziel 13,3 %; das Modell verteilt 45,6 / 29,1 / 15,3 / 9,9 % (bei jeder
Zielzeit gleich). Die steilen Stücke oben kosten also deutlich mehr, als die Steigung allein sagt (Gehen, Höhe über 2000 m, Ermüdung).

Geprüft mit Playwright (Chromium, 393 × 852, Faktor 2, Server auf Port 8792, `pruefen.js`, `pruefen2.js`, `pruefen3.js`): keine
Konsolenfehler, `APP_VERSION` 2.5 und Knopf v2.5, Service Worker installiert (36 Einträge im Cache `zgm-marathon-profil`), Tipp auf die
Version meldet „Version 2.5 ist aktuell“; Tabellen bei 320/375/393/430 px ohne Überbreite, Seite nicht breiter als das Fenster.
Laufansicht am Start, km 5 (Herbriggen), 9 (Anstieg Randa), 16,5 (Bergweg), 20,6 (Bahnhofplatz), 22,4 (Gornera), 27,5 (Ried–Patrullarve),
31,9 (Sunnegga), 33,6 (Seenweg), 35,6 (Grünsee), 39,3 (steilste Stelle), 40,9 (Riffelboden), 42,1 (Ziel) und die Kartenübersicht mit
Verpflegung bei km 30 angesehen; Zuschauer-Tabelle mit „Ortszeit Zermatt“, 3. Juli 2027, den zwei Startknöpfen und dem Text zu den
Kontrollzeiten; „Woher die Zahlen kommen“. Bilder in `work/shots/`. `kern.py` meldet alle Apps „gleich“, dazu „karten.json veraltet“
(neue Strecke; Hauptsitzung mit `--schreiben`).

**Lesbarkeit des Profils (Kern):** Der Läuferblick nimmt den Höhenbereich der ganzen Strecke (1100–2590 m) als Achse, Hilfslinien alle
100 m (14 Beschriftungen, gut lesbar). Im Tal ist die Kurve dadurch flach: Die 130 m der ersten 5 km sind im 5-km-Ausschnitt etwa 40 px
hoch; Steigung zeigen dort vor allem die Farben. Ab Zermatt ist die Kurve deutlich. Gesamtstrecke unten und Vollbild ohne Überlappungen.

## Zwischenzeiten (Datasport, nur geprüft, nichts gespeichert)

Die Rangliste 2026 (`results.datasport.com/de/anlass/gornergrat-zermatt-marathon-2026/ranking`, Listen „Marathon Frauen“ und „Marathon
Männer“) hat je Läufer vier **Etappenzeiten**: „Start-Zermatt“, „Zermatt-Sunegga“, „Sunegga-Riffelalp“, „Riffelalp-Ziel“ (Summe =
Endzeit), sortierbar nach „@ Zermatt“, „@ Sunegga“, „@ Riffelalp“, „@ Ziel“. Messpunkte also Zermatt (Bahnhofplatz, Veranstalter km 21,1,
hier 20,6), Sunnegga (32,4 bzw. 31,7, hier 32,0) und Riffelalp (39,1). Alle 355 Finisher haben alle vier Werte. Gezählt in `/tmp` ohne Namen,
danach gelöscht.

## Offen

- Prüfung am iPhone.
- **Kilometer:** gleichmässig gedehnt; ob die Strecke vermessen ist, sagt der Veranstalter nicht (Reglement: „nach den Bestimmungen …
  AIMS“). Seine km widersprechen sich (siehe Daten 2). Wenn er Kilometermarken oder eine neue GPX veröffentlicht, `common.py` umstellen.
- **Start:** Die Linie beginnt auf 1100,5 m, der Veranstalter nennt 1116 bzw. 1120 m; der genaue Startpunkt auf der Umfahrungsstrasse
  ist nur aus der Karte im Race Magazin bekannt (ohne Koordinaten).
- **Ziel:** Linienende auf 2575 m, gut 200 m nach dem höchsten Punkt (2584,5 m); der Veranstalter nennt „Riffelberg 2’585 m“.
  Halbmarathon- und Marathon-Datei enden am selben Punkt.
- **Grünsee-Posten** am See gesetzt (km 35,6) statt bei der Plan-km 36,7 (dort 2239 m statt 2300 m). Lage der übrigen Posten am Berg nach
  der Planhöhe, im Tal nach der Plan-km; eine Karte der Posten gibt es nicht.
- **Unterführung Randa** als Gerade (GPX 2 m tiefer).
- **Höhe über dem Meer:** `D.lage` ist nicht gesetzt (Mexiko-Stadt: eine Höhe für die ganze Strecke). Hier 1100 bis 2585 m, die zweite
  Hälfte über 1600 m, ab km 30 über 2200 m. Ob und wie das Modell das zeigen soll, entscheidet die Hauptsitzung mit dem Berg-Hinweis.
- **Startseite:** Karte fehlt. Eyebrow „Gornergrat Zermatt Marathon“, Stadt „Zermatt“, „Kurs 2026“, `data-termine="2026-07-04 2027-07-03"`,
  `data-monat="7"`, Termintext „Sa., 3. Juli 2027“, ↑ 1816 m / ↓ 342 m, Höhe 1100–2585 m, `data-such` z. B. „Zermatt Gornergrat St. Niklaus
  Mattertal Matterhorn Riffelberg Sunnegga Riffelalp Täsch Randa Wallis Valais Schweiz Switzerland Suisse CH Bergmarathon Ultra“;
  Mini-Profil mit 1484 m Höhenbereich (eigene Grafikhöhe oder halber Maßstab wie Great Wall). README-Tabelle und Liste der Präfixe
  (`zgm-`). Fuss der Startseite: Höhen „swissALTI3D und swissSURFACE3D © swisstopo“ (wie Zürich und Luzern).
  **Teilnehmer 2026: 355 im Ziel** des Marathons (Datasport-Rangliste, gezählt: 87 Frauen und 268 Männer mit Rang und Zeit; Übersicht
  „Beendet“ ebenso 87 + 268). Angemeldet 437, gestartet 381. Nach Reglement Ziffer 26 stehen Ultra-Läufer, die am Riffelberg aufhören,
  ebenfalls in der Marathon-Rangliste; wie viele, zeigt die Liste nicht. Ultra 2026: 375 im Ziel.
- Gegenprobe mit dem privaten Eichdatensatz (`course_segments`) nicht gemacht: Die Datei lag in dieser Sitzung nicht vor.
