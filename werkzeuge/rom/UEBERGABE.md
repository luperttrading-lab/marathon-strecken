# Übergabe: Steigungsprofil Run Rome The Marathon

Stand 30.10.2026, App-Version **1.7** (1.7: Kopf mit Ort groß und „Streckenplan und Steigungsprofil“, Umschalter Karte | Zahlen statt Pünktchen, Karte zuerst, Name der Strecke im Vollbild; 1.6: zu breite Tabellen werden stufenweise enger statt rechts abgeschnitten; 1.5: Mauer-Beschriftung in einer freien Zeile über dem Profil, mittig über der Mauer, nur bei `D.mauer`; 1.4: Mauer-Beschriftung im Profil neben dem Gipfel statt darauf, nur bei `D.mauer`; 1.3: Mauer je Durchgang ein Rad mit Empfehlung nach Zielzeit, nur bei `D.mauer`; 1.2: Mauer-Zeit und Tor-Rechner für Strecken mit `D.mauer`, sonst unverändert; 1.1: Steigungskosten als große Zeile unter der Zielzeit; 1.0: erste Fassung).
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/rom/.

Die App ist eine Kopie der Tokio-App (Stand 1.24, aktueller gemeinsamer Code) mit eigenen Daten, Texten und Speicherschlüsseln
(`rom-…`, Service-Worker-Cache `rom-marathon-profil`, löscht nur Caches mit Präfix `rom-`), ohne eigenes Manifest und Symbol. Alle
Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Änderungen am
gemeinsamen Code in allen Apps nachziehen (README). Gegenüber `tokio/index.html` weichen genau dieselben Zeilen ab wie bei Valencia.

**Wichtigster Unterschied zu den anderen Strecken: Es gibt kein Laser-Höhenmodell.** Die Höhen sind ein 10-m-Modell (TINITALY),
angeglichen an Höhenpunkte der Regione Lazio (siehe Daten 6–7). Das steht in der App im Untertitel und unter „Woher die Zahlen
kommen“.

## Termin und Start

32. Run Rome The Marathon (Acea Run Rome The Marathon; Infront Italy, Corriere dello Sport, Rome Marathon Runners) am Sonntag,
14. März 2027 laut Reglement 2027 des Veranstalters
(https://www.runromethemarathon.com/wp-content/uploads/2026/09/RRTM27-regolamento-ITA.pdf, ebenso die Fassung vom 23.04.2026 und
die Seite „La Maratona“). Das Reglement nennt „partenza alle ore 8:30 circa“ und 7 Stunden Zielschluss; dieselbe Formel stand im
Reglement 2026, gestartet wurde 2026 dann ab 8:00. `D.termine` `["2027-03-14"]`, `D.tz` Europe/Rome, `D.ort` „Rom“ (nach der
Zeitzone hieße es sonst „Rome“), `D.ortKurz` „ Rom“, `D.start` = 490 (8:10, erste Welle 2026). Start auf der Via dei Fori Imperiali
„altezza Cartine Geografiche Antica Roma“ (an der Basilica di Massenzio), Ziel im Circo Massimo, wie 2026.

**Startwellen** (`D.wellen`): Wellen 2026 laut Event Guide
(https://www.runromethemarathon.com/wp-content/uploads/2026/03/Event-Guide_WEB_def.pdf) und Seite des Veranstalters: Rollstühle
und Schieber 8:00, Welle 1 Griglie TOP und A (orange) 8:10, Welle 2 Griglia B (grün) 8:20, Welle 3 Griglia C (blau) 8:30, Welle 4
Griglia D (weiß) 8:45, Welle 5 Griglia E (rot) 9:00, Staffel 9:15. Die Griglia richtet sich nach der angegebenen Bestzeit der
letzten vier Jahre und steht auf der Startnummer. Die englische Fassung des Guides nennt für Welle 1 8:15; die italienische, die
Seite und die Zeitlimits („calcolati dalla partenza della prima onda alle ore 08:10“) sagen 8:10. Der Wellenplan 2027 ist noch
nicht veröffentlicht („sarà comunicato successivamente“); der Hinweis in der App sagt das.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

1. **Quellen des Veranstalters** (`../dl/`): Infoblatt zum Renntag 2026 `RRTM26_MARATHON_22.03.pdf`
   (https://www.runromethemarathon.com/wp-content/uploads/2026/03/RRTM26_MARATHON_22.03.pdf), Seite 4: Liste aller 151 Straßen und
   Plätze in Laufrichtung mit „Km N“ an 42 Einträgen (km 1–41 und Halbmarathon) (`../dl/strassenliste.txt`), Streckenplan (Rasterbild 2263 × 2514 px mit
   Kilometerschildern, `../dl/img/x72.png`), Höhenbild „Altimetria“ (Vektorgrafik), Lagepläne Start und Ziel. Event Guide:
   Wellen, Ristori, Spugnaggi, Zeitlimits, Ausstiegspunkte (Piazza Montegrappa „km 23,300 circa“, Lungotevere Acqua Acetosa Ecke
   Via Venezuela „km 30,000 circa“, Piazza delle Belle Arti „km 35,000 circa“). Staffel: `staff_map.pdf` (Wechsel S1 km 11,000
   Piazza di Monte Savello, S2 km 23,500 Lungotevere Guglielmo Oberdan, S3 km 31,400 Viale XVII Olimpiade). **Eine GPX-Datei gibt
   es nur in der App des Veranstalters**; ENDU (Anmeldung) führt keine Strecke, eine Google-Karte gibt es nicht.
2. `osm.py`: OSM-Straßennetz über die OSM-API (`api.openstreetmap.org/api/0.6/map`) in 216 Rechtecken zu 0,005°, eine Abfrage je
   Sekunde (Rohantworten `../dl/osmapi/`, 266 MB) → `../dl/osm_netz.json` (40 377 Wege), `../dl/osm_wasser.json`. Overpass war
   wieder nicht nutzbar (overpass-api.de Verbindung abgebrochen, maps.mail.ru 504, kumi.systems und private.coffee Zeitüberschreitung).
3. `netz.py`, `linie.py`: eigenes Routing (Dijkstra) wie Mexiko-Stadt. Wegmarken sind die Kreuzungen je zweier aufeinanderfolgender
   Straßen der Liste (bei mehreren Knoten der günstigste von der vorigen Marke aus, das wählt die Fahrbahn in Laufrichtung);
   dazwischen kosten andere Straßen das Dreifache, gegen Einbahnstraßen × 2,5, Unterführungen × 4. Von Hand (`EXTRA`): Via del Teatro
   di Marcello am Vittoriano entlang (sonst Piazza di San Marco), Via del Tritone stadtauswärts auf der Busspur bis Largo Chigi
   (sonst Via della Mercede), die Unterführungen der Hauptfahrbahn des Lungotevere Arnaldo da Brescia („Sottopasso di Ripetta“,
   sonst die Nebenfahrbahnen oben). Start bei 41,89253/12,48853 (Startplan: gut 550 m vor der Piazza Venezia), Ziel im Circo Massimo
   gut 90 m hinter dem Westende an der Südseite (Lageplan „Finish Area“: über Via della Greca und Via dell'Ara Massima di Ercole
   hinein). OSM schreibt Ordnungszahlen aus („Via Leone Quarto“), die Liste in `linie.py` folgt OSM.
   → `gpx2026.json` (2842 Punkte, **43,21 km** auf dem Ellipsoid), `strassen.json`, `wegmarken.json`.
   `plan.py`: Plan des Veranstalters affin eingepasst (fünf Passpunkte von Hand, dann ICP über die roten Pixel; 6,3 m/px): Linie im
   Median 7 m, zu 90 % höchstens 33 m neben dem Plan. Bis 90 m nur um die Acqua Acetosa und die Schleife Viale Antonino di San
   Giuliano, wo der Plan gezeichnet verzerrt ist (Form und Straßen stimmen).
4. `marken.py`, `common.py`: Kilometer stückweise linear über acht Stützpunkte, an denen laut Liste und Plan eine Kilometermarke
   steht: km 5 Ecke Via Cristoforo Colombo / Circonvallazione Ostiense (Linie 5150 m), km 10 Piazza dell'Emporio (10 085), km 11
   Piazza di Monte Savello = Staffelwechsel S1 (11 145), km 15 Piazza Cavour (15 210), km 25 Piazzale Maresciallo Giardino (25 740),
   km 26 Piazza Lauro de Bosis (26 755), km 37 Piazza del Popolo (37 755), km 41 Piazza Venezia (41 935); Start und Ziel an den
   Linienenden. Faktor je Abschnitt 0,94–1,01 (Linie im Mittel 2,4 % länger: Straßenmitte, Plätze, Ecken). **Gegenprobe** mit der
   Liste: 38 der 42 Kilometer liegen danach auf der genannten Straße, km 23 (Via Oslavia) 127 m und km 33 (Via Giovanni Paolo
   Pannini) 115 m daneben, zwei weitere unter 15 m. Die Angaben „circa“ passen schlechter: Piazza Montegrappa „23,3“ → 23,75,
   Acqua Acetosa „30,0“ → 30,42, Belle Arti „35,0“ → 34,88; „23,3“ und „S2 23,5“ widersprechen der Liste selbst (km 24 liegt laut
   Liste auf dem Lungotevere Oberdan, der nach der Linie nur 0,4 km lang ist). Kilometer daher auf etwa ±100 m genau.
5. `dgm.py`, `tinitaly.py`: **TINITALY/1.1** des INGV (https://tinitaly.pi.ingv.it/, Blatt w46075_s10, 10-m-Raster, GeoTIFF in UTM 32,
   CC BY 4.0), bilinear alle 10 m → `dgm_tinitaly.json`. **Warum kein besseres Modell:**
   - Laser-Geländemodell des Umweltministeriums (MASE, Piano Straordinario di Telerilevamento, Lazio 1 m und 2 m, Flusskorridore):
     Der WMS `wms.pcn.minambiente.it/ogc?map=/ms_ogc/WMS_v1.3/servizi-LiDAR/LIDAR_LAZIO.map` (Ebenen `EL.LIDAR.LAZIO.1x1.DTM` usw.)
     liefert nur leere Bilder, GetFeatureInfo 503, der Blattschnitt (`QU_Lidar.map`) meldet eine abgebrochene Datenbank; der
     Download-Dienst (sim.mase.gov.it, laut Geoportale ohne Anmeldung) ist laut Hinweis vom 29.10. bis 06.11.2026 in Wartung. Ob
     Rom überhaupt abgedeckt ist, war deshalb nicht zu prüfen.
   - Regione Lazio: DTM 5 m aus der Carta Tecnica 2002/03 (photogrammetrisch, DXF) liegt in einem Datei-Browser, der nur nach einer
     Anmeldung (Token) liefert; nicht umgangen. Ein WCS mit Höhen gibt es dort nicht.
   - Roma Capitale (dati.comune.roma.it): kein Höhenmodell.
6. `curve.py`, `dbgt.py`: Topografische Datenbank **DBGT 2014 der Regione Lazio** (photogrammetrisch 1:5000, alle Geometrien mit
   Höhe über dem Meer, CC BY 4.0) über den WFS `geoportale.regione.lazio.it/geoserver/ows`: Höhenlinien (629 im Rechteck), Bauwerke
   der Verkehrswege (Typ 01: Verkehrsinseln, Fahrbahnteiler), Radwegflächen, Brücken, Kleinbauten (Kioske), Denkmäler.
   `vergleich.py`: TINITALY gegen die Höhenlinien, wo die Linie sie kreuzt (77 Stellen): im Mittel +4,4 m, 90 % bis 12,9 m daneben,
   größte +17,7 m. Das Modell zieht Straßen am Fuß von Hügeln hinauf (Via del Teatro di Marcello am Kapitol +18 m, Via Marmorata am
   Aventin +10 m, Testaccio am Monte Testaccio +8 m, Fori Imperiali am Vittoriano bis 39 m statt 22 m) und kennt Dämme und Rampen
   nicht (Via Cristoforo Colombo −11 m, Rampe des Ponte Settimia Spizzichino −8 m). Zum Höhenbild des Veranstalters passt es kaum
   (Korrelation 0,22).
7. `angleich.py`: **TINITALY an die DBGT angeglichen** → `dgm2026_10m.json`, `angleich.json`. 650 Passpunkte in 256 Abschnitten zu
   20 m: Höhenlinien-Kreuzungen (44, nicht auf Brücken und in Unterführungen), Verkehrsinseln (405, höchstens 10 m neben der
   Linie), Radwege (26), Brückenfahrbahnen (141, höchstens 15 m neben der Linie, 10–28 m hoch, ohne Pfeiler; auf Brücken nur
   diese), Kleinbauten (34, tiefster Eckpunkt). Vorher schmale Buckel aus TINITALY entfernt (graue Öffnung über 500 m). Höhe =
   Gerade zwischen den Passpunkten plus die halbe Form von TINITALY dazwischen. Probe durch Weglassen ganzer Abschnitte
   (Median/quadratisches Mittel bei Lücken 0,8 / 1,5 / 2,5 km): reine Gerade 1,1/2,2 · 2,1/3,5 · 2,5/4,4 m, volle TINITALY-Form
   1,2/2,4 · 2,0/3,0 · 2,7/3,8 m, halbe Form 1,0/2,1 · 1,6/3,0 · 2,4/3,9 m. Lücken über 1 km: km 10–13 (Lungotevere), 17–20 (Prati),
   33–37 (Flaminio bis Via del Corso), 38–41 (Altstadt); dort 2–4 m Unsicherheit. Ergebnis gegen TINITALY roh −17,9 bis +11,5 m,
   im Mittel 3,0 m.
8. `orte.py`: **Rione / Quartiere / Suburbio** alle 100 m aus den OSM-Relationen boundary=place mit ref „R. I“ … „Q. XX“ (die
   amtliche Gliederung Roms nach Ortsnamen), 39 Flächen einzeln über `api.openstreetmap.org/api/0.6/relation/<id>/full`
   (`../dl/orte/`). Gewählt statt der Municipi, weil das ganze Zentrum ein Municipio ist (Municipio I von Testaccio bis Prati);
   die Rioni stehen auf den Straßenschildern der Altstadt. Die Strecke berührt Monti, Campitelli, Ripa, Testaccio, Ostiense,
   Portuense, Regola, Ponte, Borgo, Prati, Campo Marzio, Trionfale, Della Vittoria, Flaminio, Parioli, Colonna, Trevi, Parione,
   Sant'Eustachio, Pigna und Sant'Angelo.
9. `namen.py`: Straßennamen wie in OSM (`name`); wo OSM eine Ordnungszahl ausschreibt und `alt_name` die römische Zahl trägt (wie auf
   den Schildern und in der Liste), gilt `alt_name`: Via Leone IV, Via San Pio X, Ponte Vittorio Emanuele II, Corso Vittorio Emanuele
   II, Piazza Pio XII, Piazza di Ponte Umberto I. Andere `alt_name` („Ponte di Ferro“, „Via Colombo“) bleiben unbeachtet.
10. `clean.py`: Auf allen Brücken der Strecke (Via Cristoforo Colombo, Ponte Settimia Spizzichino, Ponte dell'Industria, Ponte
    Testaccio, Ponte Vittorio Emanuele II, Ponte Cavour, Ponte Regina Margherita, Ponte della Musica) liegen Passpunkte der
    DBGT auf der Fahrbahn (Tiberbrücken 18,5–23,4 m); keine liegt mehr als 0,2 m unter der Geraden, alle bleiben **gemessen**. **Geschätzt**
    (schraffiert): die Unterführung „Sottopasso di Ripetta“ (km 35,52–35,95, Hauptfahrbahn des Lungotevere Arnaldo da Brescia,
    OSM tunnel=yes mit kurzen offenen Stücken) von Portal zu Portal gerade (18,9 → 17,8 m). Kein Modell kennt ihren Boden; das
    Höhenbild des Veranstalters zeigt dort eine Senke von einigen Metern. Die Durchfahrt der Via Portuense unter der Bahn (km 8,0,
    OSM tunnel=passage) bleibt gemessen. Weitere Stufen über 1,5 m je 10 m gab es nicht.
11. `build.py`: Höhen in cm im 10-m-Raster, Median über 30 m; Straßen unter 80 m und Ortsteile unter 300 m dem Vorgänger
    zugeschlagen. Marken laut Event Guide an ihrer Kilometerangabe: Getränke (Wasser) km 5,3 / 9,9 / 16,4 / 17,45 / 17,9 / 20,3 /
    22,4 / 25 / 30 / 31,6 / 33,8 / 35,5 / 38,6 / 39,6 / 40,25, ab km 15 mit Mineralsalzen (der Guide schreibt „dal rifornimento del
    km 15,500“, die Liste nennt km 15,000), Verpflegung km 15 (feste Nahrung); Schwämme km 7,4 / 10,1 / 13,9 / 16,5 / 19,4 / 23,9 /
    29,9 / 33,6 / 34 / 36,4 / 38,7 / 39,8 (Wasserbecken, eigener Schwamm aus dem Startbeutel). Staffelwechsel (Run4Rome): S1 km 11,
    S2 und S3 an ihrer Lage (Beginn des Lungotevere Oberdan, km 23,86; Viale XVII Olimpiade an der Viale Tiziano, km 31,44), weil
    „23,5“ nicht zur Liste passt. `route.py` (lat0/lon0 41,8/12,4), `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py rom`,
    `work/app.py` (aus `tokio/index.html` und `tokio/sw.js`; Texte in `sub.html`, `quellen.html`, `strassennamen.html`,
    `imgnote.html`), `tiles_rand.py rom 2`.
12. `planprofil.py`: Höhenbild des Veranstalters aus der Vektorgrafik (Achsen aus Rahmen und Hilfslinien) → `planprofil.json`.
    Seine Beschriftungen passen nicht zur eigenen Achse (Start „23 m“ bei 10 m gezeichnet, Tiefpunkt „12 m“ bei 6 m).

## Ergebnis

↑ 105 m / ↓ 107 m mit 200-m-Fenster, ↑ 125 / ↓ 126 m mit 50 m, ↑ 118 / ↓ 120 m mit 100 m, ↑ 53 / ↓ 55 m mit 1 km, Rohdaten ↑ 135 m.
Start 21,7 m auf der Via dei Fori Imperiali, höchster Punkt 30,7 m auf dem Viale Marco Polo an der Via Cristoforo Colombo (km 4,2),
tiefster 11,2 m an der Bocca della Verità (km 1,4; ebenso 11,6 m bei km 41,7), Ziel 20,0 m im Circo Massimo. Vom Start über die
Piazza Venezia auf 25 m an der Piazza d'Aracoeli, auf der Via del Teatro di Marcello hinab zum Fluss, in Ostiense knapp 20 m hinauf
auf den Rücken der Via Cristoforo Colombo und wieder hinab; danach bis zum Kapitol zwischen 12 und 24 m: am Fluss 13–21 m, in
Prati, Della Vittoria und Flaminio 15–24 m mit sanften Wellen (Circonvallazione Trionfale km 20,7, Brücken, Piazza di Spagna); am
Ende vom Kapitol 13 m hinab zur Bocca della Verità und 8 m hinauf in den Circo Massimo. Steilste Stelle −4,5 % über 200 m auf der
Via del Teatro di Marcello (km 41,3), bergauf +3,9 % in den Circo Massimo (km 41,9). Mit 4:00/km im Flachen ergibt das Modell
2:49:41 (das Profil kostet 54 s, bei 2:50:00 ebenso 54 s).

**Abgleich mit dem Veranstalter:** Das Infoblatt nennt Start 23 m, höchsten Punkt 31 m (km 4,5), tiefsten 12 m (um km 1,5 und vor
dem Ziel) und Ziel 17 m; die Seite „La Maratona“ Start 22 m, höchsten 31 m, tiefsten 8,1 m. Seine Kurve liegt im Median 4,4 m tiefer
als die App (Hälfte zwischen 2,7 und 5,8 m) und zeigt dieselben Wellen an denselben Stellen (Korrelation 0,85; TINITALY allein
0,22). Die Ziellinie: Die DBGT-Höhenlinie 20 m quert die Linie im Circo Massimo zweimal, TINITALY sagt 21–23 m; die 17 m des
Veranstalters sind damit nicht zu bestätigen.

Geprüft mit Playwright (393 × 852, Faktor 2, Server auf Port 8776): keine Konsolenfehler, `APP_VERSION` 1.0, Service Worker
installiert (23 Dateien im Cache `rom-marathon-profil`), Tipp auf die Version meldet „Version 1.0 ist aktuell“, alle 17 Kartenstücke
passen zu `D.tiles` und `sw.js`, Kartenbilder laden; Laufansicht am Start, km 4,2, 21,1, 35,7 (Unterführung schraffiert) und 41,8
sowie die Kartenseite angesehen.

## Offen

- Prüfung am iPhone.
- Startseite: Karte für Rom fehlt noch (Eyebrow „Run Rome The Marathon“, Stadt „Rom“, „Kurs 2026“, `data-termine="2027-03-14"`,
  `data-monat="3"`, ↑ 105 m / ↓ 107 m, Höhe 11–31 m, `data-such` z. B. „Roma Rome Italien Italia Lazio Acea“), README-Tabelle und
  Liste der Speicherschlüssel/Cache-Präfixe (`rom-`).
- **Laser-Modell nachziehen:** Sobald der Download-Dienst des MASE nach der Wartung (bis 06.11.2026) wieder läuft, prüfen, ob die
  LiDAR-Befliegung Lazio (1 m) Rom abdeckt; dann `dgm.py` darauf umstellen und `angleich.py` nur noch als Gegenprobe nutzen.
- Wellenplan 2027 und Startzeit eintragen, sobald veröffentlicht (2026: Event Guide Mitte März).
- GPX der offiziellen Strecke (App des Veranstalters) oder eine Karte mit allen Kilometermarken: Linie und Eichung damit ersetzen.
- Tiefe der Unterführung „Sottopasso di Ripetta“ (km 35,5–36) ist unbekannt; das Höhenbild des Veranstalters zeigt dort eine Senke.
