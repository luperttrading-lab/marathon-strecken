# Übergabe: Steigungsprofil OCHSNER SPORT Zürich Marathon

Stand 31.10.2026, App-Version **2.3** (erste Fassung, angelegt mit `werkzeuge/kern/kern.py --neu` auf dem gemeinsamen Kern; die
Hauptsitzung zählt die Nummer beim Veröffentlichen hoch).
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/zuerich/.

Die App hat den gemeinsamen Kern aus `hamburg/` und eigene Felder (Texte, `const D`, Speicherschlüssel `zrh-…`, Service-Worker-Cache
`zrh-marathon-profil`, löscht nur Caches mit Präfix `zrh-`; der Präfix war frei, `kern.py --neu` prüft das), ohne eigenes Manifest und
Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Startseite,
README, `version.json` und `karten.json` sind noch nicht angepasst (Hauptsitzung).

**Besonderheiten:** Erste Schweizer Strecke. Die Höhen kommen aus **swissALTI3D 0,5 m** (Laser-Geländemodell von swisstopo), die
Brückenfahrbahnen aus **swissSURFACE3D Raster** (Oberflächenmodell), beide über `work/swissalti.py`, das für Jungfrau, Zermatt und
Luzern wiederverwendbar ist (Abschnitt „swissalti.py“ unten). Die Linie ist die **GPX-Datei des Veranstalters** (entgegen der ersten
Recherche gibt es eine: Knopf „GPX Dateien“ auf der Marathon-Seite). Die flachste Strecke der Sammlung: Höhenbereich 10 m. Straßennamen
in Schweizer Schreibweise wie auf den Schildern („Seestrasse“, „General-Guisan-Quai“), kein „ß“ in Eigennamen.

## Termin und Start

Offizieller Name **OCHSNER SPORT Zürich Marathon** (Logo und Texte des Veranstalters ZH Marathon GmbH, Zürich). 24. Austragung am
**Sonntag, 11. April 2027** (https://www.zuerichmarathon.ch/, Seiten „Marathon“ `marathon-2/marathon`, „von A bis Z“ `infos/von-a-bis-z`:
„Die Austragung des 24. OCHSNER SPORT Zürich Marathon, 7. Halbmarathon und 15. On Z10 findet am Sonntag, 11. April 2027 statt.“; FAQ
ebenso; `../dl/seiten/`). Der 23. war am Sonntag, 12. April 2026 (Seite „Ranglisten“). Marathon 2027 ausverkauft, 23 000 Startplätze für
alle drei Läufe. `D.termine` `["2026-04-12", "2027-04-11"]` (2027 bestätigt, ohne „?“), `D.tz` Europe/Zurich, `D.ort` „Zürich“ und
`D.ortKurz` „ Zürich“ (sonst nennte der Kern die Zeitzone „Zurich“), `D.start` = 480 (8:00). Kein `D.lage`, `D.mauer`, `D.tor`,
`D.zielschluss`.

**Start** (`D.wellen`, ohne Wellenknöpfe, nur Text wie Honolulu): „Start: Quaibrücke, Zürich · Sonntag, 11. April 2027, 08.00 Uhr“;
„Der Start erfolgt als Massenstart mit rollendem Ablauf der einzelnen Blöcke“; Startblock nach angegebener Zielzeit, Farbe auf der
Startnummer; Block F bis knapp 2 km vom Start entfernt. Uhrzeiten je Block sind nicht veröffentlicht. Halbmarathon 13:15, On Z10 16:00,
beide eigene Rennen auf eigener Strecke.

**Zeitlimit 5:30 h netto**, Zielschluss 13:45 Uhr; „Läufer:innen die den Wendepunkt in Meilen bis 11.10 Uhr nicht erreichen, müssen ihre
Startnummer und den Transponder abgeben.“ (Seite „Marathon“); Besenwagen ab Meilen („von A bis Z“). Steht im Text unter „Deine
Startzeit“ (`D.tor` zeigt der Kern nur zusammen mit `D.mauer`).

**Keine Staffel:** Den „Teamrun“ gab es bis 2019 (Ranglisten-Archiv); die heutige „Teamwertung“ zählt die drei schnellsten von mindestens
sechs Läufern im Halbmarathon oder On Z10, keine Wechsel. Also keine `relay`-Marken, kein Staffel-Schalter.
**Halbmarathon-Marke** bei 21 098 m (Zwischenzeiten laut Veranstalter bei km 10, 20, 21,1, 30, 40).

**Start und Ziel:** Start mitten auf der Quaibrücke (Startstrich im Plan 7 m neben dem GPX-Anfang), Ziel auf dem Sechseläutenplatz
(über Utoquai und Schoeckstrasse; Zielstrich im Plan rund 20 m hinter dem GPX-Ende). Die Quaibrücke ist gewölbt: Start auf 410,8 m.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Reihenfolge: `parse.py`, `osm.py`, `strassen.py`, `dgm.py` (mit `swissalti.py`), `deck.py`, `clean.py`, `orte.py`, `plan.py`, `build.py`,
`route.py`, `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py zuerich`, `zuerich/work/app.py` (beim ersten Mal über
`kern.py --neu zuerich work/felder.json`, danach ersetzt es nur die Felder und lässt Kartenbilder und `D.tiles` stehen),
`tiles_rand.py zuerich 2`. Nur Abgleich: `vergleich.py`, `ansicht.py` (Linien über OSM-Kacheln zeichnen). Prüfen: `pruefen.js`,
`pruefen2.js`, `pruefen3.js` (Server auf Port 8793 im Repo-Wurzelordner, `NODE_PATH=/opt/node-tools/node_modules node pruefen.js`).

1. **Strecke** (`parse.py`): GPX-Datei des Veranstalters, Seite „Marathon“, Knopf „GPX Dateien“ → Google Drive
   `zhm2025marathon.gpx` (Abruf ohne Anmeldung: `https://drive.usercontent.google.com/download?id=1Jx980yCBl68NO58oTrm3Ks9aWOSZWRs8&export=download`,
   `../dl/gpx/`): Track „ZHM 2025 - Marathon“, erstellt mit MySchweizMobil, 980 Punkte mit Höhen. MySchweizMobil setzt an jedem
   Zwischenpunkt doppelte, um 0,2–1,4 m versetzte Punkte (Zickzack, zusammen 165 m): entfernt, bleiben 651 Punkte, **42 734,8 m**
   (geodätisch). Die Linie liegt im Median 1 m neben den OSM-Straßen, 99 % unter 4,3 m (nur die letzten 20 m auf dem Platz weiter):
   Neu zeichnen war nicht nötig. **Kurs 2026:** Der Streckenplan 2026 (`Marathon_ZHM.pdf`, Reygrafik, 17.12.2025, `../dl/pdf/`) und der
   Plan 2025 (`Streckenplan_Marathon.pdf`, 28.11.2024) zeigen denselben Weg, nur die Verpflegungssymbole sind verschoben; die Seite für
   2027 verlinkt den Plan von 2025/26 und dieselbe GPX („Aufgrund geplanter Baustellen … kann es zu punktuellen Anpassungen der
   Streckenführung kommen“). Der Text auf der Seite „Strassensperrungen“ nennt dieselbe Straßenfolge.
2. `common.py`: **Kilometer gleichmäßig** über die Linie (Faktor 42 195 / 42 734,8 = 0,98737), Start am Linienanfang, Ziel am Ende.
   `plan.py`: Strecke und Kilometertafeln liegen im PDF als Vektoren über einem Kartenbild (`pdftocairo -svg` → `../dl/pdf/p1.svg`
   Übersicht, `p2.svg` Detailplan City). Je Seite die gezeichnete Linie affin auf die GPX eingepasst (ICP; Detailplan 1 pt = 6,7 m,
   Abstand Plan–GPX im Median 5 m; Übersicht 1 pt = 25 m, 14 m), dann die Tafelmitten auf die GPX projiziert (welche Zahl in welcher
   Tafel steht, von Hand aus dem Bild). Tafeln stehen 35–60 m (Detail) bzw. 140–190 m (Übersicht) neben der Linie. Ergebnis
   (`marken_plan.json`): Detailplan km 3–8 im Mittel **0,09 km später** als in der App, km 35–41 **0,14 km früher**, km 9/10/42 dazwischen;
   Übersicht km 15–30 ±0,15 km ohne Richtung. Die gezeichnete Linie ist so lang wie die GPX (Verhältnis 1,013–1,016): Auch der Plan hilft
   nicht beim Eichen. Die 1,3 % Überlänge kommen von den Straßenmitten und den vielen Ecken in der Stadt (dort wohl mehr als am See).
   **Genauigkeit: Kilometer auf etwa ±0,2 km**, einzeln nicht belegt. Eine stückweise Eichung durch die Tafeln des Detailplans würde die
   Kilometer in der Stadt um rund 0,1 km verschieben; nicht gemacht, weil die Tafeln nur ±40 m genau stehen.
3. `osm.py`: OSM über die API in 77 Rechtecken zu 0,005° höchstens 150 m neben der Linie, eine Abfrage je Sekunde (`../dl/osmapi/`) →
   `../dl/osm_netz.json` (11 613 Wege). `strassen.py` (wie Honolulu, in LV95): je 10 m der nächste Weg bis 20 m neben der Linie,
   höchstens 35° Richtungsabweichung, Hauptstraßen bevorzugt; Namen wie in OSM (`namen.py`, Schweizer Schreibweise). Die letzten 70 m
   (Schoeckstrasse und die Fläche des Platzes, in OSM kein benannter Weg) heißen „Sechseläutenplatz“ (`build.py`).
4. `orte.py`: **Quartiere** alle 100 m, je 40 m links und rechts nachgesehen (bei zwei Gebieten „links / rechts“). In der Stadt die
   34 statistischen Quartiere mit Kreis (Stadt Zürich, Open Data, WFS `Statistische_Quartiere`, Ebene `adm_statistische_quartiere_map`,
   Lizenz CC0, `../dl/orte/quartiere.json`), angezeigt wie Wien „Kreis 8, Seefeld“. **Kreis 1 als „Kreis 1, Altstadt“** (so heißt er bei
   der Stadt und in OSM): seine vier Quartiere Rathaus, Hochschulen, Lindenhof und City treffen sich genau an Quaibrücke, Bürkliplatz und
   Bellevue, wo die Strecke fünfmal durchkommt; quartiersgenau wechselte die Anzeige dort alle 100 m. Am See die Gemeinden aus
   swissBOUNDARIES3D (geo.admin.ch, Dienst `find`, Ebene `ch.swisstopo.swissboundaries3d-gemeinde-flaeche.fill`, aktueller Stand,
   `../dl/orte/gem_*.json`), ohne „(ZH)“. Folge: Kreis 1 Altstadt, Kreis 8 Seefeld, Altstadt, Kreis 2 Enge, Altstadt, Seefeld, Zollikon,
   Küsnacht, Erlenbach, Herrliberg, Meilen und zurück, zum Schluss Altstadt.
5. `swissalti.py`, `dgm.py`: **Höhe aus swissALTI3D 0,5 m**, alle 10 Linienmeter bilinear (4275 Punkte), dazu swissALTI3D 2 m und die
   GPX-Höhen zum Vergleich (`dgm_vergleich.json`). 24 Kacheln entlang der Strecke, alle Jahrgang 2026 (daneben gibt es 2019/2020; der
   Jahrgang im Namen ist nicht sicher das Flugjahr). Höhen in m ü. M. (LN02). 0,5 m und 2 m unterscheiden sich im Median um 3 mm.
6. `deck.py`, `clean.py`: **Brücken.** swissALTI3D lässt Brücken weg und misst darunter Wasser bzw. Bachbett. Wo das Modell unter
   406,6 m fällt (Seespiegel 405,7 m) oder mehr als 0,8 m unter den Median der 60 m um die Stelle, gilt die Fahrbahn aus
   **swissSURFACE3D Raster 0,5 m** (Jahrgang 2024): je Punkt das 25-%-Quantil von 5 × 5 Werten im Abstand 1 m (darunter Wasser neben der
   Fahrbahn, darüber Fahrzeuge, Leuchten, Fahrleitung; Muster `werkzeuge/koeln/work/dom.py`). An Land stimmen beide Modelle auf ±0,05 m.
   - **Quaibrücke** (km 0–0,07 Start, 3,93–4,06, 8,39–8,52, 35,94–36,07, 41,87–42,00): Gelände 405,7 m, Fahrbahn gewölbt 409,5 → 410,8 m.
   - **Schanzengraben:** Dreikönigbrücke (km 6,12–6,15 und 38,99–39,02, 408,5 m) und General-Guisan-Quai (km 8,17–8,20 und 36,27–36,30, 408,0 m).
   - **Seestrasse** über den Dorfbach Küsnacht (km 14,75 und 29,69; Gelände 409,5 bzw. 411,6, Fahrbahn 412,5 m) und den Heslibach
     (km 15,97; 410,5 → 411,9 m; auf dem Rückweg zeigt das Modell dort keine Senke).
   - Nicht ersetzt: bei km 11,36 und 33,08 zeigt das Oberflächenmodell 418 m (Brücke der Dufourstrasse über die Bellerivestrasse, also
     über der Strecke); das Geländemodell fällt dort nicht ab.
   Alles gemessen, **nichts geschätzt**, `D.bridges` leer (wie Stockholm; Quellentext mit `<span id="bridges" hidden>`). Danach keine
   Stufe über 0,7 m je 10 m. Die GPX-Höhen (MySchweizMobil, wohl aus einem swisstopo-Modell mit Brücken) liegen im Median 1 cm, 95 %
   innerhalb −0,6/+0,3 m; auf der Quaibrücke flacher (409,3–410,1 m).
7. `plan.py`, `build.py`: **Verpflegung.** Der Veranstalter (Seite „Verpflegung“): „insgesamt 12 Verpflegungsposten … Wasser,
   isotonische Getränke und weitere Energiespender“, einseitig aufgebaut, mit WC und Sanität. Der Plan 2026 zeigt sechs Stellen
   (gelbe Becher) an Talstrasse, Mythenquai, Zürichhorn, Goldbach, Erlenbach und Feldmeilen, je auf Hin- und Rückweg passiert = 12.
   Lage: alle Durchgänge der Linie nahe beim Symbol; die Symbole stehen aber 60–170 m (Stadt) bzw. 240–600 m (am See, im See gezeichnet)
   neben der Strecke: **etwa ±0,2 km bzw. ±0,5 km**, in der App „ca.“. Am Zürichhorn läuft die Strecke dreimal vorbei (km 1,5, 9,9, 34,5);
   gezählt sind 9,9 und 34,5 (ein Posten nach 1,5 km wäre ungewöhnlich, mit ihm wären es 13; nicht belegt). In der App 12 Marken
   „Verpflegung“ (food): ca. km 5,6 / 7,4 / 9,9 / 13,0 / 16,6 / 19,6 / 24,8 / 27,8 / 31,4 / 34,5 / 37,2 / 39,5. Zum Vergleich: Die
   Marschtabelle des Halbmarathons 2023 (`../dl/pdf/hm2023_marsch.pdf`) nennt Posten „Bellerivestrasse (China Garden)“, „Küsnacht,
   Seestrasse 27, Parkplatz Terlinden“, „Erlenbach, Friedhof“, „Talstrasse (Basteiplatz)“; eine Marschtabelle für den Marathon habe ich
   nicht gefunden.
   Höhen in cm im 10-m-Raster, Median über 30 m; Straßenstücke unter 80 m und Quartiere unter 300 m dem Vorgänger zugeschlagen.
   `route.py` (lat0/lon0 47,3/8,5), `tiles.py` (z12–z15), `tiles_z11.py zuerich`, `app.py`, `tiles_rand.py zuerich 2`: 27 Kartenstücke,
   2,5 MB.

   **Abgleich** (`vergleich.py`, offizielle km, Verfahren wie die App):

   | Quelle | Start | Ziel | min (km) | max (km) | ↑/↓ 200 m | ↑ 50 m | ↑ 1 km | gegen App (Median) | r |
   |---|---|---|---|---|---|---|---|---|---|
   | App (swissALTI3D 0,5 m, Brücken aus swissSURFACE3D) | 410,8 | 408,0 | 407,2 (37,12) | 417,0 (22,36) | 72/75 | 93 | 27 | – | – |
   | swissALTI3D 0,5 m ohne Brücken | 405,7 | 408,0 | 405,7 (0,00) | 417,0 (22,36) | 74/72 | 104 | 28 | ±0,00 | 0,950 |
   | swissALTI3D 2 m, gleiche Brücken | 410,8 | 408,0 | 407,2 (0,53) | 417,0 (22,37) | 72/75 | 93 | 27 | ±0,00 | 1,000 |
   | GPX-Höhen (MySchweizMobil) | 410,1 | 408,0 | 407,3 (0,69) | 416,9 (22,36) | 66/68 | 79 | 26 | +0,01 | 0,993 |

   Das Höhenbild im Streckenplan (Seite 3) ist eine Skizze ohne Zahlen (Achse 400–450 m, zwei Buckel, die nicht zum Hin- und Rückweg
   passen); der Veranstalter schreibt „sehr flache Strecke“.

## swissalti.py (wiederverwendbar für Jungfrau, Zermatt, Luzern)

`work/swissalti.py` holt Höhen aus den freien swisstopo-Modellen für beliebige Punkte, ohne Anmeldung und ohne GDAL:

- **Modelle:** `Modell("swissalti3d", 0.5)` bzw. `gsd=2.0` (Gelände, Brücken weg), `Modell("swisssurface3d-raster")` (Oberfläche, 0,5 m).
  Optional `jahr=2020`: neuester Jahrgang bis dahin (sonst der neueste).
- **Aufruf:** `m.wgs84(lat, lon)` bzw. `m.lv95(E, N)` → Höhen (m ü. M., LN02), bilinear über die Pixelmitten, `nan` ohne Daten;
  `m.kacheln_info()` nennt die verwendeten Kacheln mit Jahrgang. Zum Ausprobieren: `python3 swissalti.py 47.36685 8.54314`.
- **Weg:** STAC-API `https://data.geo.admin.ch/api/stac/v0.9/collections/ch.swisstopo.<modell>/items?bbox=…` je Kachel (1 × 1 km in
  LV95, Name `…_<Jahr>_<E km>-<N km>`), Asset `…_0.5_2056_5728.tif` bzw. `…_2_2056_5728.tif` (Cloud-Optimized GeoTIFF, Float32, LZW,
  interne Kacheln 128 × 128, NoData −9999, PixelIsArea, Ecke links oben bei E·1000 / (N+1)·1000). Geladen werden nur Dateikopf und
  gebrauchte Innenkacheln per HTTP-Range; Zwischenspeicher `../dl/swisstopo/` (STAC-Antworten je Modell, Auflösung und Kachel,
  Bytebereiche nach MD5), ein zweiter Lauf braucht kein Netz. Zürich: 42,7 km Linie ≈ 13 MB für swissALTI3D 0,5 m in rund 3 Minuten; das
  Oberflächenmodell ist deutlich größer je Innenkachel (deshalb nur an den Brücken, `deck.py`).
- **Lizenz:** kostenlose Geodaten von swisstopo (OGD, seit 01.03.2021; „Nutzungsbedingungen … Version 1.3.2021“), nutzen und verbreiten
  erlaubt, **Quellenangabe Pflicht**: „© swisstopo“ bzw. „Bundesamt für Landestopografie swisstopo“
  (https://www.swisstopo.admin.ch/de/nutzungsbedingungen-kostenlose-geodaten-und-geodienste). Die STAC-API schreibt „proprietary“.
- **Fallstricke:** Seen und Flüsse sind im Geländemodell flach (Seespiegel), Brücken fehlen → Oberflächenmodell mit Quantil wie hier;
  Überführungen über der Strecke erscheinen im Oberflächenmodell als hohe Werte, dort das Geländemodell lassen. In Bergstrecken
  (Jungfrau, Zermatt) gibt es Tunnel und Galerien: Das Oberflächenmodell zeigt dort den Berg, Tunnel wie Hamburg als Gerade schätzen.
  Der Zwischenspeicher-Schlüssel enthält die Auflösung (ein früher Fehler: 2 m las die 0,5-m-Dateien).

## Ergebnis

↑ 72 m / ↓ 75 m mit 200-m-Fenster, ↑ 93 / ↓ 96 m mit 50 m, ↑ 85 / ↓ 88 m mit 100 m, ↑ 27 / ↓ 29 m mit 1 km; wie GPS-Uhren 70 (ab 0,5 m),
56 (ab 1 m), 22 (ab 3 m); Rohdaten ↑ 115 m (Punkt für Punkt, mit Brückenfahrbahnen). Start 410,8 m oben auf der Quaibrücke, Ziel 408,0 m
auf dem Sechseläutenplatz, tiefster Punkt 407,2 m am Utoquai und Mythenquai (km 0,5, 9,0, 35,5, 37,1), höchster 417,0 m in der
Wendeschlaufe in Meilen (Dorfstrasse, km 22,36); **Höhenbereich 9,8 m**. Flach am See durch das Seefeld, über die Dufourstrasse kurz
hinauf (412,5 m, km 2,5), Altstadt und Enge fast eben (407–411 m), auf der Seestrasse leicht wellig (Küsnacht 412,6 m, Erlenbach
415,8 m bei km 17,5), in Meilen über Winkel- und Dorfstrasse 9 m hinauf und hinunter: steilste Stellen +3,9 % / −4,1 % über 200 m
(km 22,2 / 22,5), +5,4 % / −6,0 % über 100 m. Rückweg spiegelbildlich (Wende bei km 22,3). Die gewölbte Quaibrücke (fünfmal, je 1,3 m Wölbung) trägt mit
200-m-Fenster rund 2 der 72 Höhenmeter bei (mit flacher Brücke 70/72).
**Modellzeit:** Mit 4:00/km im Flachen ergibt das Modell **2:49:23** (das Profil kostet 36 s); **bei 2:50:00 kostet es 36 s, bei 4:00:00
51 s** (Flach-Pace 4:00,9 bzw. 5:40,1 /km; gemessen mit `pruefen.js` in der App 2.3). Zum Vergleich bei 2:50:00: Wien 61 s, Honolulu
85 s, Boston 88 s, Stockholm 113 s.

Geprüft mit Playwright (Chromium, 393 × 852, Faktor 2, Server auf Port 8793, `pruefen.js`, `pruefen2.js`, `pruefen3.js`): keine
Konsolenfehler, `APP_VERSION` 2.3 und Knopf v2.3, Service Worker installiert (33 Einträge im Cache `zrh-marathon-profil`), Tipp auf die
Version meldet „Version 2.3 ist aktuell“; Tabellen bei 320/375/393/430 px ohne Überbreite, Seite nicht breiter als das Fenster.
Laufansicht am Start (Quaibrücke), km 2,5 (Dufourstrasse), 4,0 (Quaibrücke), 7,4 (Mythenquai), 17,5 (Erlenbach), 22,3 und 22,36
(Wendeschlaufe Meilen, höchster Punkt), 41,5 (Stadthausquai), 42,1 (Ziel) und die Kartenübersicht mit Verpflegung bei km 13 angesehen;
Zuschauer-Tabelle mit „Ortszeit Zürich“, 11. April 2027 und dem Text zu Start und Zeitlimit; „Woher die Zahlen kommen“ angesehen. Bilder
in `work/shots/`. `kern.py` meldet alle Apps „gleich“, dazu „karten.json veraltet“ (neue Strecke; Hauptsitzung mit `--schreiben`).

## Offen

- Prüfung am iPhone.
- **Kilometer** nur gleichmäßig gestaucht (Daten 2); die Tafeln des Detailplans deuten auf rund 0,1 km Verschiebung in der Stadt
  (Anfang später, Ende früher). Eine Liste der Kilometertafeln mit Koordinaten oder eine Marschtabelle des Marathons gibt es nicht.
- **Verpflegung** nur aus den Symbolen des Plans (±0,2 / ±0,5 km); welche der drei Durchfahrten am Zürichhorn einen Posten hat, ist
  angenommen (Daten 7). Race Booklet 2027 (digital, etwa eine Woche vorher per Race-Mail) prüfen.
- **Kurs 2027:** „punktuelle Anpassungen“ wegen Baustellen angekündigt; neue GPX bzw. neuen Plan abwarten, dann `parse.py` und die Kette
  erneut. Uhrzeiten der Startblöcke sind nicht veröffentlicht.
- **Startseite:** Karte fehlt. Eyebrow „OCHSNER SPORT Zürich Marathon“, Stadt „Zürich“, „Kurs 2026“,
  `data-termine="2026-04-12 2027-04-11"`, `data-monat="4"`, ↑ 72 m / ↓ 75 m, Höhe 407–417 m, `data-such` z. B. „Zürich Zuerich Zurich
  Schweiz Switzerland Suisse CH Ochsner Zürichsee Meilen Küsnacht Seefeld Quaibrücke Sechseläutenplatz“; Mini-Profil mit 10 m
  Höhenbereich passt in die Grundhöhe 64 px. README-Tabelle und Liste der Präfixe (`zrh-`). Fuß der Startseite: Höhen „swissALTI3D und
  swissSURFACE3D © swisstopo“.
  **Teilnehmer 2026: 5 173 im Ziel** des Marathons (Rangliste Race Result des Veranstalters, `my.raceresult.com/378478`, gezählt mit
  Rang und Zeit; in der Liste 7 086 Gemeldete, davon 1 493 nicht gestartet, 237 aufgegeben, 181 „n.a.“, 2 „a.k.“). 2025: 4 135 im Ziel
  (`my.raceresult.com/322778`; marathons.com nennt ≈ 4 130). Halbmarathon 2026 7 048, On Z10 5 600 im Ziel. Keine Namen gespeichert.
- Gegenprobe mit dem privaten Eichdatensatz (`course_segments`) nicht gemacht: Die Datei lag in dieser Sitzung nicht vor.
