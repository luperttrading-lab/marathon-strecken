# Übergabe: Steigungsprofil Athens Marathon. The Authentic

Stand 30.10.2026, App-Version **1.1** (1.1: Kopf mit Ort groß und „Streckenplan und Steigungsprofil“, Umschalter Karte | Zahlen statt Pünktchen, Karte zuerst, Name der Strecke im Vollbild; 1.0: erste Fassung).
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/athen/.

Die App ist eine Kopie der Tokio-App (Stand 1.30, aktueller gemeinsamer Code) mit eigenen Daten, Texten und Speicherschlüsseln
(`ath-…`, Service-Worker-Cache `ath-marathon-profil`, löscht nur Caches mit Präfix `ath-`), ohne eigenes Manifest und Symbol. Alle
Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Änderungen am
gemeinsamen Code in allen Apps nachziehen (README). Gegenüber `tokio/index.html` weichen genau dieselben Zeilen ab wie bei Rom und
Barcelona. Startseite und README sind noch nicht angepasst.

**Wichtigster Unterschied zu den anderen Strecken: Es gibt kein frei zugängliches Laser- oder amtliches Geländemodell.** Die Höhen
kommen aus FABDEM, einem globalen 30-m-Modell (Copernicus ohne Gebäude und Bäume), in der Innenstadt zusätzlich geglättet. Das steht
in der App im Untertitel, unter „Woher die Zahlen kommen“ und im Hinweis darunter. Für die großen Anstiege (km 10–16, 18–31) reicht es:
Form und Höhenmeter stimmen mit dem Höhenbild des Veranstalters und mit Copernicus überein (siehe Daten 7).

## Termin und Start

43. Athens Marathon. The Authentic (SEGAS, Hellenic Athletics) am **Sonntag, 8. November 2026**: Seite „Marathon Race“ des
Veranstalters (https://www.athensauthenticmarathon.gr/en/c/agones-2-26/authentic-marathon-1/marathonios-dromos-33, `../dl/race_en.html`),
Wochenprogramm (`../dl/programm_en.html`) und Mitteilung „What’s New at the 2026 Athens Authentic Marathon: Race Schedule and Start
Times“ vom 16.10.2026 (`../dl/blog_334.html`). Start 8:30 in Marathonas (Marathon Run Historic Start Venue am Stadion), Ziel im
Panathinaiko-Stadion (Kallimarmaro), die letzten 170 m auf der Laufbahn. **Zeitlimit 8 Stunden**, alle Zieleinläufe bis 18:15 (nach dem
Start des letzten Blocks). Das Wochenprogramm nennt unter „Marathon Town“ einmal „8:00: Start of the Marathon Race“ (wohl ein
Versehen: der 10-km-Lauf startet um 8:00); Seite, Mitteilung und die erwarteten Zielzeiten der Spitze (10:39–10:42) sagen 8:30. 2027 ist nicht veröffentlicht; der
Lauf ist seit Jahren am zweiten Sonntag im November (2024: 10.11., 2025: 9.11., 2026: 8.11.), daher `2027-11-14?`.
`D.termine` `["2026-11-08", "2027-11-14?"]`, `D.tz` Europe/Athens, `D.ort` „Athen“ (nach der Zeitzone hieße es „Athens“), `D.ortKurz`
„ Athen“, `D.start` = 510. Kein `D.lage`, kein `D.mauer`, kein `D.tor`.

**Startblöcke** (`D.wellen`, belastbar): Tabelle „Starting blocks“ der Seite „Marathon Race“ („indicative, finalized two weeks before the
Marathon“), gleichlautend in der Mitteilung vom 16.10.2026: Block 1 8:30 (20 Elite, 180 der griechischen Meisterschaft, 600 schnellste,
laut Mitteilung davon etwa 300 unter 3 h), Block 2 8:32, 3 8:35, 4 8:39, 5 8:44, 6 8:49 (je die nächsten 1500), Sonderblock für Läufer
mit Behinderung 8:54, Block 7 9:00 (1700), 8 9:06, 9 9:12, 10 9:18 (je 1800); zweite Welle (eigene Busse 6:30–7:30) Block 11 9:45,
12 9:51 (je 1800), 13 9:57 und 14 10:03 (über 6 h oder ohne Zeit), 15 10:09 (ohne Zeit); 10:15 „last runner crosses the starting grid“.
Der Block richtet sich nach der Bestzeit 2024–2026 auf vermessener Strecke und steht auf der Startnummer; Blockwechsel waren bis
25.10.2026 möglich. In der App 16 Knöpfe (wie Sydney mit 12 passen sie in sieben Zeilen).

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Reihenfolge: `parse.py`, `osm.py`, `linie.py`, `marken.py`, `fabdem.py`, `dgm.py`, `planprofil.py`, `vergleich.py`, `strassen.py`,
`orte.py`, `clean.py`, `build.py`, `route.py`, `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py athen`, `athen/work/app.py` (aus
`tokio/index.html` und `tokio/sw.js`; Texte in `sub.html`, `quellen.html`, `strassennamen.html`, `imgnote.html`), `tiles_rand.py athen 2`.

1. **Strecke** (`parse.py`): GPX-Datei des Veranstalters von der Seite „Marathon Race“ („Download the route file“:
   `https://www.athensauthenticmarathon.gr/files/product/athens_marathon_the_authentic.gpx`, `../dl/`). Es ist eine Strava-Route des
   Veranstalters (strava.com/routes/3343870889182584480, Konto „Athens Marathon The Authentic“, auf OpenStreetMap gezeichnet), 644 Punkte
   von der Startlinie am Stadion in Marathonas bis zur Ziellinie im Panathinaiko-Stadion, **42 283 m** auf dem Ellipsoid (GRS80). Die
   KML-Datei derselben Seite (plotaroute.com) ist dieselbe Linie (0,0 m Abstand) mit Kilometerzeichen, die plotaroute selbst alle 1000
   Linienmeter setzt: keine Schilder. Die TCX-Datei ist dieselbe Linie mit Zeitstempeln. Dazu Streckenplan, Start- und Zielplan
   (`maratonia_diadrome.jpg`, `ekkinese_maratoniou_dromou.jpg`, `termatismos.jpg`, schematisch). → `gpx_veranstalter.json`.
2. `osm.py`: OSM über die API (`api.openstreetmap.org/api/0.6/map`) in 163 Rechtecken zu 0,005° höchstens 150 m neben der Linie, eine
   Abfrage je Sekunde (Rohantworten `../dl/osmapi/`) → `../dl/osm_netz.json` (8113 Wege). Overpass war wieder nicht nutzbar
   (overpass-api.de Verbindung abgebrochen, maps.mail.ru 504, kumi.systems und private.coffee Zeitüberschreitung).
3. `linie.py`: **Berichtigung.** Die Strava-Route bleibt bei km 38,3 auf der Mesogeion bis zu ihrem Ende an der Feidippidou. Laut
   Streckenbeschreibung des Veranstalters („Immediately after Henry Dunant Hospital, runners continue left on Michalakopoulou Avenue,
   until the traffic light at the intersection of Michalakopoulou & Feidippidou Streets. Then they follow Feidippidou Street on the
   right until Kifissias junction & Alexandras Ave.“) ist das Stück aus den OSM-Wegen ersetzt: Abzweig der Michalakopoulou (Knoten
   212974582), Michalakopoulou 305 m bis zur Ampel (212986858), Feidippidou 126 m, gerade über die Kreuzung (69 m, OSM trennt dort die
   Fahrbahnen), Feidippidou 141 m bis zum Knoten Kifissias/Alexandras/Vasilissis Sofias (6370114997). Angeschlossen am letzten Linienpunkt,
   von dem der Abzweig höchstens 45° neben der Laufrichtung liegt (die Linie liegt auf der Gegenfahrbahn). Linie jetzt **42 355 m**
   (+71 m). → `gpx2026.json` (mit `ersatz`: Linienmeter 38 481–39 122).
4. `marken.py`, `common.py`: **Kilometer.** Der Veranstalter veröffentlicht weder die Lage seiner Kilometerschilder noch der Zeitmatten
   (alle 5 km und bei 21,1 km; „There is an indication at every kilometer“). An der Strecke stehen aber feste Steine der „Κλασσική
   Διαδρομή Μαραθωνίου Δρόμου“ (Klassische Marathonstrecke, „Athens Classic Marathon Course“) mit Kilometerzahl; in OSM eingetragen sind
   33 (Agia Paraskevi, Mesogeion/Kapodistriou, Knoten 13476572295), 34 (Chalandri, 13580665683), 37 (Ampelokipoi, 13479112628) und 39
   (Vasilissis Sofias am Knoten Kifissias/Alexandras, 13476418218; eine Suche in Nominatim nach dem Namen fand keine weiteren). Auf der
   berichtigten Linie: Stein 33 bei Linienmeter 33 142 (11,6 m neben der Linie, Linie − km = +142 m), 34 bei 34 163 (6,3 m, +163),
   37 bei 37 162 (7,7 m, +162), 39 bei 39 162 (17,3 m, +162), Ziel 42 355 (+160). Ohne die Berichtigung lag die Linie ab dem Umweg nur
   noch 88–91 m über den Steinen; mit ihr ist die Überlänge ab km 33 gleich: Die 160 m stammen aus den ersten 33 km (Mittellinie der
   Straße statt Ideallinie auf gut 1800° Kurven, Schleife um den Tymvos). Stein 39 steht genau dort, wo die Beschreibung km 39 nennt
   („just around the corner“). Stützpunkte: Start, Mittel der Steine 33 und 34 (sie liegen 1022 Linienmeter auseinander; einer ist wohl
   gut 10 m versetzt eingetragen), 37, 39, Ziel = 42 195 m; dazwischen linear (Faktor 0,9955 bis km 33,5, dann 0,9974, 1,0000, 1,0008).
   **Genauigkeit:** Bis km 33,5 ist die Überlänge gleichmäßig verteilt. Verteilt man sie stattdessen nach den Kurven (Drehwinkel der
   Linie, 4,7 m je rad), verschieben sich die 5-km-Marken um +5 / +14 / +5 / +21 / +19 / +8 m (km 5 bis 30), höchstens 29 m (km 6,3);
   dazu die Lage der Steine (±10–15 m) und die des Startpunkts der GPX-Linie. **Kilometer bis km 33 auf etwa ±50 m, danach auf etwa
   ±15 m.** Gegenproben mit der Beschreibung: Abzweig in die Marathonomachon km 3,97 („until the 4th km“), zurück auf der Leoforos
   Marathonos km 6,24 (Schleife 2,27 km, „the next 2.2 km“), Unterführung an der Katechaki km 37,31–37,41 („37.5 km“ ist dort die
   Versorgung), Abzweig in die Irodou Attikou km 41,31 („41.2 km“), Stadioneinfahrt 170 m vor dem Ziel km 42,025: Linie überquert die
   Vasileos Konstantinou bei km 41,95, Vorplatz bis 42,02.
5. `fabdem.py`, `hoehen.py`, `dgm.py`: **Höhe.** **FABDEM V1-2** (Hawker u. a. 2022, „A 30 m global map of elevation with forests and
   buildings removed“, Environ. Res. Lett. 17 024016; University of Bristol / Fathom), 1″-Raster, Höhen über dem Geoid EGM2008, Lizenz
   **CC BY-NC-SA 4.0** (`../dl/dem/FABDEM_LICENSE.txt`; die Höhen der App stehen damit ebenfalls unter CC BY-NC-SA, gesagt in den Quellen).
   Öffentlich ohne Anmeldung auf data.bris.ac.uk in Zip-Dateien zu 10 × 10 Grad; `fabdem.py` holt aus
   `N30E020-N40E030_FABDEM_V1-2.zip` (838 MB) per Teilabruf (Accept-Ranges) nur das Inhaltsverzeichnis und die Kacheln N37E023 und
   N38E023. Bilinear alle 10 Linienmeter → `dgm2026_10m.json`, alle Modelle in `dgm_vergleich.json`. Die GeoTIFF sagen RasterPixelIsPoint
   (Mitte des ersten Pixels auf der Kachelecke), `hoehen.py` rechnet so.
   **Warum kein besseres Modell:**
   - Griechisches Kataster (Ελληνικό Κτηματολόγιο): Ein landesweites 5-m-Geländemodell (LSO 2007–2009, photogrammetrisch) gibt es, im
     INSPIRE-Geoportal als „offline“ und laut gov.gr nur auf Antrag. Aus dieser Umgebung: data.ktimatologio.gr „Access Denied“ (403),
     inspire.ktimatologio.gr und geoportal.ktimatologio.gr nicht erreichbar, der offene WMS `gis.ktimanet.gr/wms/wmsopen` hat nur die
     Grundkarte, die ArcGIS-Dienste des Katasters (Experience Builder maps.ktimatologio.gr) keine Höhen, data.gov.gr unter dem Kataster
     sieben Datensätze ohne Höhenmodell. Kein Laser-Modell für Attika frei. Das Geoportal des Umweltministeriums (geoportal.ypen.gr) hat
     als WCS nur eine Schummerung.
   - FathomDEM (Nachfolger von FABDEM) nur nach Anmeldung bei Zenodo; GEDTM30 (OpenLandMap, CC BY 4.0) laut Zenodo „use for testing
     purposes only“, nicht genommen. ALOS, NASADEM, TanDEM-X 90, EU-DEM nur mit Anmeldung.
6. `planprofil.py`: Höhenbild des Veranstalters aus dem Streckenplan (Rasterbild 2000 × 1380 px; Achsen aus den Hilfslinien: 32,06 px je
   km, 0,5 px je m, also 2 m je Pixel; Mitte des orangen Strichs je Spalte) → `planprofil.json`. Nennwerte im Bild: Start ~41 m, Gipfel
   245 m bei km 31, Ziel ~97 m.
7. `vergleich.py`: **Vergleich der Quellen** entlang der Linie (offizielle km; FABDEM hier noch ohne Glättung in der Innenstadt; Strava =
   Höhen in der GPX-Datei, Quelle unbekannt; Unruhe = mittlere |2. Differenz| je 10 m):

   | Quelle | Start | Ziel | min | max | ↑/↓ 200 m | ↑ 1 km | gegen Veranstalter (Median) | r | Unruhe |
   |---|---|---|---|---|---|---|---|---|---|
   | FABDEM | 32,5 | 85,3 | 4,0 | 241,4 | 335/282 | 281 | −6,6 m | 0,9994 | 0,082 |
   | Copernicus GLO-30 | 34,6 | 84,8 | 3,9 | 242,8 | 356/305 | 281 | −5,8 m | 0,9994 | 0,197 |
   | SRTM 1″ (2000) | 33,5 | 100,8 | 6,3 | 252,9 | 468/405 | 289 | −2,0 m | 0,9987 | 0,210 |
   | Strava (GPX) | 36,7 | 95,6 | 8,4 | 247,4 | 325/266 | 281 | −1,5 m | 0,9996 | 0,016 |
   | Veranstalter (Bild) | 41,0 | 97,0 | 9,0 | 245,0 | 322/266 | 276 | – | – | 0,066 |

   Je 5 km (↑/↓, 200-m-Fenster) FABDEM gegen Veranstalter: 0/28 – 3/30, 16/5 – 18/10, 53/10 – 52/8, 68/61 – 58/53, 92/1 – 94/0,
   59/8 – 53/3, 33/55 – 31/54, 2/73 – 10/75, 11/40 – 4/32. **Gewählt FABDEM:** Geländemodell statt Oberflächenmodell, am ruhigsten, gleiche
   Form wie Copernicus (im Mittel 0,9 m darunter) ohne dessen Buckel von Häusern, Bäumen und Brücken (bis 8 m in Athen, z. B. die
   Katechaki-Brücke über der Mesogeion); SRTM ist von Februar 2000, im Mittel 4,5 m höher und in der Stadt bis 22 m
   daneben. Das Höhenbild des Veranstalters hat fast dieselbe Form (r = 0,999) und dieselben Höhenmeter, liegt aber
   7 m höher (Hälfte 5–8 m), wohl aus einem Oberflächenmodell wie die Strava-Höhen; nicht angeglichen. Grenzen: Ein 30-m-Raster glättet
   Rampen unter etwa 100 m Länge weg; einzelne Höhen können einige Meter daneben liegen.
8. `strassen.py`, `namen.py`: Straße je 10 m: nächster OSM-Weg höchstens 20 m neben der Linie, dessen Richtung höchstens 35° abweicht
   (sonst nähme die Katechaki-Brücke den Platz der Mesogeion darunter ein), Hauptstraßen bevorzugt, Tunnel und Brücken zählen (die
   Strecke läuft durch zwei Unterführungen). **Namen in lateinischer Umschrift nach ELOT 743** (griechische Norm, gleich ISO 843,
   Transkription; so stehen sie auf den griechischen Straßenschildern), aus dem griechischen `name`, weil die lateinischen Namen in OSM
   uneinheitlich sind (`int_name` „Fidippidou“ statt „Feidippidou“, an der Marathonomachon steht „Kallinikou“, `name:en` fehlt meist).
   Regeln in `namen.py` (Akzente weg, αι ai, ει ei, οι oi, ου ou, αυ/ευ av/ev bzw. af/ef, μπ am Wortanfang b, sonst mp, ντ nt, γγ ng, γκ
   gk/nk, η i, υ y, χ ch, ψ ps …). „Leoforos“ (Allee) vor den Alleen (Marathonos, Mesogeion, Michalakopoulou, Alexandras, Vasilissis
   Sofias, Vasileos Konstantinou), wie der Veranstalter „Marathonos Avenue“ schreibt. Ohne Namen: am Start „Startgelände am Stadion“
   (gut 290 m Ring und Zufahrt), ab der Vasileos Konstantinou „Panathinaiko-Stadion“ (Vorplatz und Laufbahn).
9. `orte.py`: **Orte** alle 100 m: Gemeinde (Dimos, OSM admin_level 7) bzw. Gemeindebezirk (Dimotiki Enotita, admin_level 8: die
   früheren Gemeinden, heißen wie die Orte), Flächen einzeln über `api.openstreetmap.org/api/0.6/relation/<id>/full` (`../dl/orte/`).
   Viele Straßen der Strecke sind selbst die Grenze; deshalb je 40 m links und rechts nachgesehen, bei zwei Orten „links / rechts“. Ergebnis:
   Marathonas (km 0–7,7), Nea Makri (–15,6), Rafina (–18,7), Pikermi (–22,4), Spata / Pikermi (–23,4), Pallini (–28,2), Pallini /
   Anthousa, Glyka Nera / Gerakas (km 28,5–31,1), Agia Paraskevi, Agia Paraskevi / Chalandri, Cholargos / Chalandri, Cholargos / Neo
   Psychiko, Athen (ab km 36,4). Namen im Nominativ in Umschrift (`namen.ORTE`), Athen deutsch.
10. `clean.py`: **Brücken** aus OSM (bridge=yes auf der Linie, Enden oben auf den Rampen je bis 30 m außerhalb), gerade gezogen, wo das
    Modell innen mehr als 1,0 m unter der Geraden liegt (wie Valencia, Rom). **Geschätzt** (schraffiert): Leoforos Marathonos über den
    Valanaris (km 20,34–20,41, Modell 1,3 m darunter) und über die Attiki Odos und die Flughafenbahn im Einschnitt in Pallini (km 28,25–
    28,39, 1,3 m). **Gemessen:** die kurzen Bachbrücken bei km 13,2 (10 m) und 18,7 (20 m, Rema Agias Paraskevis), Modell glatt.
    **Unterführungen** (OSM tunnel=yes): am Knoten Stavros unter der Autobahn A621 (km 30,61–30,71, maxheight 6) und an der Katechaki
    unter der Brücke der Katechaki (km 37,31–37,41, „where the runners pass under the bridge“). FABDEM zeigt dort weder Brückendeck noch
    Senke, sondern die durchgehende Steigung (225 → 228 m) bzw. das Gefälle (156,5 → 154,6 m), höchstens 1,2 m neben der Geraden: bleiben
    gemessen. Ob die Fahrbahn unter den Brücken tiefer gelegt ist, verrät ein 30-m-Raster nicht.
    **Innenstadt** (ab km 38,3, Michalakopoulou bis Ziel): FABDEM zeigt an den Häuserblöcken Stufen und Buckel bis 10 m (z. B. 6 m auf
    der Vasilissis Sofias bei km 39,4, ein 10-m-Buckel am Kriegsmuseum bei km 41,1–41,3, wo die Straße eben ist; Copernicus zeigt sie noch
    stärker, das Höhenbild des Veranstalters nicht). Dort robust geglättet: lokal gewichtete Ausgleichsgerade über ±250 m (LOWESS,
    Tricube, drei Runden mit Bisquare-Gewichten), weicher Übergang auf 250 m davor; Abweichung vom Modell im Median 0,7 m, höchstens 9,1 m.
    Ohne diese Glättung fände die Stufensuche dort 13 Stufen über 1,5 m je 10 m und markierte sie als Brücken und Unterführungen. Auf den
    übrigen 38 km: keine Stufe über 1,5 m je 10 m.
11. `build.py`: Höhen in cm im 10-m-Raster, Median über 30 m; Straßenstücke unter 80 m und Orte unter 300 m dem Vorgänger zugeschlagen.
    **Marken** laut Tabelle der Seite „Marathon Race“ (15 Stationen alle 2,5 km, an ihrer Kilometerangabe): Wasser (AVRA) überall,
    Schwämme an 7,5 / 12,5 / … / 37,5, Isotonisch (Powerade) an 10 / 15 / … / 40, Gel (Maurten) an 10 und 20, Bananen (Dole) an 20 / 25 /
    30 / 35, Cola an 30 / 35 / 40, Salziges an 30 und 35, Physiotherapie an 25 und 30; mit Bananen oder Salzigem „Verpflegung“, sonst
    „Getränke“. Halbmarathon-Marke bei 21 098 m (Zeitnahme „21,1“). Keine Staffel. `route.py` (lat0/lon0 37,9/23,7), `tiles.py`
    (z12–z15), dann `tiles_z11.py athen`, `app.py`, `tiles_rand.py athen 2`: 40 Kartenstücke, 4,2 MB.

## Ergebnis

↑ 325 m / ↓ 272 m mit 200-m-Fenster, ↑ 349 / ↓ 296 m mit 50 m, ↑ 339 / ↓ 286 m mit 100 m, ↑ 281 / ↓ 230 m mit 1 km, Rohdaten ↑ 427 m.
Start 32,5 m am Stadion von Marathonas, tiefster Punkt 4,0 m in Nea Makri (km 8,0), höchster 241,3 m kurz hinter dem Knoten Stavros
(km 31,2, Grenze Agia Paraskevi / Glyka Nera), Ziel 85,8 m im Panathinaiko-Stadion. Die ersten 5 km fallen 28 m, bis km 10 bleibt die
Strecke um den Tymvos und durch Nea Makri unter 16 m. Von km 10 bis 16,2 geht es 70 m hinauf (steilste Stelle +7,0 % über 200 m bei
km 15,65), dann 56 m hinunter vor die Kreuzung nach Rafina (km 17,7; −7,3 % bei km 17,0). Von dort steigt die Strecke 13,5 km lang um 211 m
durch Pikermi, Pallini und Gerakas bis hinter den Knoten Stavros, am stärksten km 19–21, 24–26 und 30–31 (+3,2 % im 1-km-Fenster bei
km 30,5). Die letzten 11 km fallen 155 m nach Athen; ins Stadion geht es zum Schluss gut 2 m hinauf (Vorplatz und Laufbahn, siehe Offen).
Mit 4:00/km im Flachen ergibt das Modell **2:52:23** (das Profil kostet 216 s); **bei 2:50:00 kostet es 213 s, bei 4:00:00 300 s**
(Flach-Pace 3:56,69 bzw. 5:34,15 /km). Damit ist Athen die teuerste Straßenstrecke der App (bei 2:50:00 New York 162 s, Kapstadt
123 s, Sydney 97 s, Boston 88 s; gemessen mit derselben App-Fassung am 30.10.2026).

**Abgleich mit dem Veranstalter:** Sein Höhenbild zeigt dieselbe Form (r = 0,9994) und fast dieselben Höhenmeter (200-m-Fenster
322/266 gegen 325/272), liegt aber im Median 6,7 m höher (Hälfte 5,1–8,3 m; Start 41 statt 32 m, Gipfel 245 statt 241 m bei km 31,
Ziel 97 statt 86 m). Die Beschreibung des Veranstalters passt: „The first 4 kilometers are slightly downhill“, flach km 6–10, bergauf
km 11–17 mit steilem Gefälle vor der Kreuzung nach Rafina, ab dort bergauf „with the most intense section until the 20th km“, Pallini
km 27–28 bergauf, „the Stavros junction, 30th–31st km“ als schwerster Anstieg, danach bergab bis ins Ziel.

**Gegenprobe mit dem Eichdatensatz** (privat, `course_segments` für Athen: GoAndRace-GPX 2025, 42,265 km, Höhen „OpenTopoData mapzen
@ ~100 m“, 800 m geglättet, Schwelle 2 m; nur gelesen). Spalten: Datensatz ↑/↓/netto; App mit 200-m-Fenster; App mit 1-km-Fenster;
App nach dem Verfahren des Datensatzes (800 m gleitendes Mittel, 2 m Schwelle); App netto. Abschnitte nach offiziellen km (der Datensatz
nach seiner Linie, höchstens 70 m versetzt).

| km | Datensatz ↑/↓ | netto | App 200 m ↑/↓ | App 1 km ↑/↓ | App wie Datensatz ↑/↓ | App netto |
|---|---|---|---|---|---|---|
| 0–5 | 0,0/22,9 | −25,6 | 0/28 | 0/27 | 0/24 | −27,5 |
| 5–10 | 6,0/1,0 | +9,6 | 16/5 | 13/4 | 10/2 | +10,9 |
| 10–15 | 45,4/2,6 | +44,9 | 53/10 | 44/1 | 41/0 | +42,2 |
| 15–20 | 52,0/50,3 | +2,6 | 68/61 | 51/47 | 53/48 | +8,1 |
| 20–25 | 93,2/0,0 | +93,2 | 92/1 | 93/0 | 93/0 | +89,8 |
| 25–30 | 50,9/0,0 | +52,8 | 59/7 | 55/0 | 52/0 | +51,4 |
| 30–35 | 31,8/47,0 | −16,6 | 33/55 | 25/49 | 26/48 | −21,1 |
| 35–40 | 0,0/63,8 | −68,4 | 1/71 | 0/70 | 0/69 | −71,0 |
| 40–42,195 | 0,0/33,7 | −32,1 | 3/33 | 0/33 | 0/29 | −29,4 |
| Summe | 279,3/221,3 | | 325/272 | 281/230 | 275/220 | |

Nach demselben Verfahren stimmen die Abschnitte auf höchstens 6 m überein (Summe 275/220 gegen 279/221; größte Abweichung km 30–35
bergauf 26 gegen 32 m). Die Höhen des Datensatzes liegen im Median 4,3 m über der App (10–90 %: 2,0–8,9 m), wie SRTM.

Geprüft mit Playwright (Chromium, 393 × 852, Faktor 2, Server auf Port 8777): keine Konsolenfehler, `APP_VERSION` 1.0, Service Worker
installiert (46 Einträge im Cache `ath-marathon-profil`: Seite, Manifest, Symbole, `version.json`, 40 Kartenstücke), Tipp auf die Version
meldet „Version 1.0 ist aktuell“, offline lädt die Seite aus dem Cache; alle 40 Kartenstücke passen zu `D.tiles` und `sw.js` (Größen
geprüft), Kartenbilder laden in allen Stufen (Übersicht z11 bis z15). Laufansicht am Start, km 4,8 (Tymvos), 16,2, 31,2, 38,7, 41,5
und im Stadion angesehen; 16 Blockknöpfe unter „Für Zuschauer“; Tabellen ohne Überbreite (Zwischenzeiten, Für Zuschauer, Rampen,
Messarten je 359/331 px in 359/331 px), Seite nicht breiter als das Fenster.
`grep -n -i "tokio\|tokyo\|tyo-\|tyo\.\|GSI" athen/index.html athen/sw.js`: keine Treffer; Unterschiede zu `tokio/index.html` nur in den
streckenspezifischen Zeilen.

## Offen

- Prüfung am iPhone; Karte auf der Startseite (Eyebrow „Athens Marathon. The Authentic“, Stadt „Athen“, „Kurs 2026“,
  `data-termine="2026-11-08 2027-11-14?"`, `data-monat="11"`, ↑ 325 m / ↓ 272 m, Höhe 4–241 m; im gemeinsamen Maßstab 40 m = 56 px wären
  das 332 px, also eigene Höhe oder halber Maßstab wie Great Wall; `data-such` z. B. „Athens Athina Griechenland Greece Hellas Authentic
  Marathonas Kallimarmaro SEGAS allwyn“), README-Tabelle und Liste der Speicherschlüssel/Cache-Präfixe (`ath-`).
- **Laser- bzw. Kataster-Geländemodell nachziehen**, falls das 5-m-Modell des Katasters frei wird oder ein Laserscan Attikas erscheint;
  dann `dgm.py` darauf umstellen und FABDEM nur als Gegenprobe nutzen. Bis dahin sind kurze Rampen (Brückenauffahrten, Unterführungen am
  Stavros und an der Katechaki) nicht im Profil.
- Laufbahn im Stadion: In Wirklichkeit eben; das Profil steigt auf den letzten 170 m um gut 2 m (83,5 → 85,8 m; die Marmorränge liegen
  im 30-m-Raster mit drin, die Glättung der Innenstadt setzt den Anstieg vom Vorplatz fort). Nicht von Hand geändert, weil die Höhe der
  Laufbahn selbst unbekannt ist; kostet bei 2:50 wenige Sekunden.
- Kilometer bis km 33 nur über die Steine 33/34 und den Start geeicht (±50 m). Lage der Zeitmatten 5–30 km beim Veranstalter oder an
  weiteren Steinen der Klassischen Marathonstrecke (Straßenfotos) prüfen, sobald möglich; die Steine 33 und 34 widersprechen sich um gut
  20 m.
- Termin 2027 (`2027-11-14?`) und Startblöcke 2027 beim Veranstalter prüfen, sobald veröffentlicht; ebenso, ob die GPX-Datei für 2027
  den Umweg über Michalakopoulou und Feidippidou enthält (dann `linie.py` weglassen).
