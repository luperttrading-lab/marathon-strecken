# Übergabe: Steigungsprofil JAL Honolulu Marathon

Stand 31.10.2026, App-Version **2.2** (erste Fassung, angelegt mit `werkzeuge/kern/kern.py --neu` auf dem gemeinsamen Kern; die
Hauptsitzung zählt die Nummer beim Veröffentlichen hoch).
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/honolulu/.

Die App hat den gemeinsamen Kern aus `hamburg/` und eigene Felder (Texte, `const D`, Speicherschlüssel `hnl-…`, Service-Worker-Cache
`hnl-marathon-profil`, löscht nur Caches mit Präfix `hnl-`; der Präfix war frei, `kern.py --neu` prüft das), ohne eigenes Manifest und
Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Startseite,
README und `version.json` sind noch nicht angepasst (Hauptsitzung).

**Besonderheiten:** Die Höhen kommen aus einem **Laser-Geländemodell 1 m** (USGS 3DEP, NOAA-Befliegung 2023), die Linie aus einer
**Strava-Route, die der Veranstalter auf seiner Streckenseite einbettet**. Honolulu hat **kein Zeitlimit**. Straßennamen auf Oʻahu
tragen ʻokina und Kahakō (ʻ ā ī); in OSM uneinheitlich, hier ist das ʻokina vereinheitlicht (Daten 3).

## Termin und Start

54. JAL Honolulu Marathon am **Sonntag, 13. Dezember 2026**, Start **5:00 Uhr** mit Feuerwerk auf dem Ala Moana Boulevard
(https://www.honolulumarathon.org/our-events/jal-honolulu-marathon, `../dl/seiten/our-events_jal-honolulu-marathon.html`: „Date Sunday
December 13, 2026“, „The race begins at 5:00AM on Ala Moana Boulevard“). 2027 am Sonntag, 12. Dezember (FAQ
https://www.honolulumarathon.org/key-information/faqs: „When is the 2027 Honolulu Marathon Weekend? December 11 & 12, 2027 … always on the
second Sunday in December“). Der 53. war am 14.12.2025 (Regen; 23 131 Starter im Marathon laut Bericht von Race Results Weekly auf der
Seite des Veranstalters, `../dl/seiten/hauger-thackery-…html`). Veranstalter Honolulu Marathon Association.
`D.termine` `["2025-12-14", "2026-12-13", "2027-12-12"]` (2026 und 2027 bestätigt, ohne „?“), `D.tz` Pacific/Honolulu (der Kern nennt
damit „Ortszeit Honolulu“, kein `D.ort` nötig), `D.start` = 300 (5:00). Kein `D.lage`, `D.mauer`, `D.tor`, `D.zielschluss`.

**Start** (`D.wellen`, ohne Wellenknöpfe, nur Text wie Tokio): ein gemeinsamer Start für alle; Startgruppen nach erwarteter Zielzeit
als Farbe auf der Startnummer (https://www.honolulumarathon.org/key-information/getting-to-the-start: „Note that all start groups start
at 5:00 AM“). Die Grenzen der Gruppen stehen zweimal etwas verschieden: Text der Seite Grün 2:30–3:59 und Lila „6:00 +“, Startlinien-Karte
Grün 2:00–3:59 und Lila 6:00–6:59; in der App daher nur „Grün unter 4 h, Blau 4–5 h, Orange 5–6 h, Lila ab 6 h“, Weiß Elite. „The start
line closes at 5:30AM and all participants must have crossed the line by that time“ (Seite „JAL Honolulu Marathon“).

**Zeitlimit: keines, belegt.** FAQ: „The JAL Honolulu Marathon is the only world-class marathon that allows ALL participants to
finish. There is no cut-off time! All participants must remain in motion throughout and race officials reserve the right to remove any
participant from the course for their safety“. Seite „Finish Area“: „The finish line at Kapiolani Park remains open until the last person
has finished“; „What to expect“: „There is no time limit … all finishers receive a medal and an official time“. Die Verkehrsinfo 2025
(`../dl/pdf/Traffic-Advisory-2025.pdf`) nennt Sperrungen von 0:30 bis 17:00 Uhr, „Roadways will be progressively opened as the athletes
clear each area“; feste Schlusszeiten an der Strecke gibt der Veranstalter nicht an. In der App steht das im Text unter „Deine Startzeit“.

**Halbmarathon-Marke** bei 21 098 m (Zeitnahme laut „What to expect“ an Start, 5, 10, 20 km, Halbmarathon, 25, 30, 35, 40 km und Ziel).
Im selben Rennen läuft nur der „Start to Park 10k“ (erste 10 km, Ziel im Kapiʻolani Park); kein Halbmarathon, keine Staffel.

**Start und Ziel:** Startlinie auf dem Ala Moana Boulevard an der Piʻikoi Street (Ecke 8 m neben dem Linienanfang), die Startgruppen
dahinter nach Osten bis Atkinson Drive, Feuerwerk westlich an der Queen Street: „2026 HM Start Line Map R6“ vom 13.08.2026
(https://www.honolulumarathon.org/wp-content/uploads/2026/10/2026-HM-Start-Line-Map-R6.pdf, `../dl/pdf/`). Die Texte der Seiten nennen
noch „Ala Moana Boulevard/Queen Street Extension“ (300 m weiter westlich, wohl vom alten Kurs). Ziel auf der Kalākaua Avenue am
Kapiʻolani Park (Bandstand).

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Reihenfolge: `parse.py`, `osm.py`, `strassen.py`, `dgm.py` (mit `cog.py`), `deck.py` (mit `ept.py`), `clean.py`, `orte.py`,
`stationen.py`, `build.py`, `route.py`, `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py honolulu`, `honolulu/work/app.py` (beim ersten
Mal über `kern.py --neu honolulu work/felder.json`, danach ersetzt es nur die Felder und lässt Kartenbilder und `D.tiles` stehen),
`tiles_rand.py honolulu 2`. Nur Abgleich: `vergleich.py`, `planprofil.py`, `marken.py`. Prüfen: `pruefen.js`, `pruefen2.js`, `pruefen3.js`
(Server auf Port 8791, `NODE_PATH=/opt/node-tools/node_modules node pruefen.js`).

1. **Strecke** (`parse.py`): Die Streckenseite des Veranstalters (https://www.honolulumarathon.org/key-information/course-description)
   bettet die Strava-Route **„JAL Honolulu Marathon 2026“** ein (Route 3517891324308402546). Die Einbettung
   `https://strava-embeds.com/route/3517891324308402546?…` liefert ohne Anmeldung die Linie als JSON („__ROUTE_DATA__“, 2349 Punkte mit
   Strava-Höhen, 64 Stücke zwischen Klickpunkten; `../dl/strava/`). An 39 Klickpunkten läuft die Linie ein paar Meter vor und zurück
   (zusammen rund 200 m); ohne diese Zacken **42 610,8 m** auf dem Ellipsoid, wie Strava sie angibt (42 596,9 m, „26.4 mi“). Die Linie
   folgt den Straßenmitten; am Ende der H-1 bei Kāhala ist sie auf den Gehweg 5 m neben der Auffahrt eingerastet (gleiche Höhe).
   Den Garmin-Kurs derselben Seite (`connect.garmin.com/app/course/510207014`) habe ich nicht abgerufen (nur über Garmins
   Anmeldung bzw. interne Schnittstelle).
   **Gegenprobe Streckenplan 2026** (`../dl/pdf/2026-HM-Course-Map.pdf` = `2026-HM-course-map_OPTION-1-R15.pdf`, Illustrator, 02.10.2026):
   gleicher Weg. Neu gegenüber 2025 (Verkehrsinfo 2025: Nimitz Highway, Nuuanu Avenue, Piikoi Street, Ala Moana Boulevard): Ala Moana
   Boulevard, Punchbowl, Queen, Bishop, Merchant, Bethel Street, South King Street, Kapiolani Boulevard bis zur Kalākaua Avenue (Plan:
   die Linie liegt neben der Kona Street, auf dem Kapiolani Boulevard), über den Ala-Wai-Kanal nach Waikīkī. Danach wie bisher.
2. `common.py`: **Kilometer gleichmäßig** über die Linie (Faktor 42 195 / 42 610,8 = 0,99024), Start am Linienanfang, Ziel am Ende.
   Kilometermarken mit Lage gibt es nicht. `marken.py`: Die 40 Kilometermarken des Plans (Texte „1k“ … „42k“ im PDF, `pdftotext -bbox`)
   gegen die Linie, affin eingepasst (West- und Ostteil getrennt): mittlerer Abstand 250 m; der Plan ist eine Zeichnung, nicht
   maßstäblich. Eine Verschiebung aller km um −125 bis −200 m passte etwas besser (242 statt 260 m im Westen, 168 statt 251 m im Osten),
   ist bei dieser Streuung aber nicht belegt; die Startlinien-Karte 2026 bestätigt den Start an der Piʻikoi Street. Eindeutig im Plan: „3k“ auf der Queen Street kurz vor der Bishop Street und „2m“
   (3219 m) kurz danach auf der Merchant Street; in der Linie liegt km 3,0 auf der Queen Street 50–80 m vor der Bishop Street, Meile 2
   90 m nach ihr auf der Merchant Street. Mit Start an der Queen Street lägen beide 300 m weiter (Merchant Street bzw. King Street).
   **Genauigkeit: Kilometer auf etwa ±0,2 km**, einzeln nicht belegt. Die Linie ist 1,0 % länger als vermessen (Straßenmitten,
   rechtwinklige Ecken).
3. `osm.py`: OSM über die API (`api.openstreetmap.org/api/0.6/map`) in 103 Rechtecken zu 0,005° höchstens 150 m neben der Linie, eine
   Abfrage je Sekunde (`../dl/osmapi/`, anfangs zweimal „509 Bandwidth Limit Exceeded“, das Skript wiederholt) →
   `../dl/osm_netz.json` (6930 Wege). `strassen.py` (wie Stockholm): je 10 m der nächste Weg bis 20 m neben der Linie, höchstens 35°
   Richtungsabweichung, Hauptstraßen bevorzugt; Auffahrten zugelassen. Namen wie in OSM, das ʻokina (in OSM als ʻ, ’ oder ') einheitlich
   als ʻ (`namen.py`): „Kalanianaʻole Highway“, „Hawaiʻi Kai Drive“; OSM schreibt „Kalākaua Avenue“ mit, „Kapiolani Boulevard“ ohne
   Zeichen (so übernommen). Unbenannte Autobahnstücke am Ende der H-1 (Lunalilo Freeway) heißen „H-1“ (km 17,56–17,98 und 34,93–35,33).
4. `orte.py`: **Viertel** alle 100 m aus den Bezirken der Neighborhood Boards der Stadt (Unterbezirke laut Neighborhood Plan 2008,
   City and County of Honolulu, Open Data HOLIS: `https://services.arcgis.com/tNJpAOha4mODLkXz/arcgis/rest/services/AdministrativePolitical/
   FeatureServer/5`, `../dl/orte/nb.geojson`), je 40 m links und rechts, bei zwei Vierteln „links / rechts“. OSM hat Grenzen nur für
   Ost-Honolulu. Angezeigt werden die geläufigen Namen (Tabelle `NAME` in `orte.py`; wie in der Streckenbeschreibung des Veranstalters):
   Ala Moana, Kakaʻako, Downtown, Waikīkī, Kapiʻolani Park (Monsarrat, Paki und Kalākaua Avenue am Park, `build.py`), Diamond Head,
   Kaimukī, Kāhala, Waiʻalae, Waiʻalae Iki, ʻĀina Haina, Niu Valley, Kuliʻouʻou, Hawaiʻi Kai.
5. `dgm.py`, `cog.py`: **Höhe aus dem USGS-3DEP-Geländemodell 1 m**, Projekt HI_NOAAMauiOahu_2020_B20, Arbeitseinheit
   HI_NOAAMauiOahu_2_B20: NOAA-Laserscan QL1 (8 Punkte/m², Abstand 0,35 m), Oʻahu beflogen 11.01.–07.07.2023, Genauigkeitsklasse
   10 cm RMSEz; Bodenmodell (ohne Gebäude, Bäume, Brücken; Gewässer flach); NAD83(PA11) / UTM 4N, Höhen „NAVD88 (GEOID12B)“, auf Hawaii
   also über dem Geoid, rund Meereshöhe. Gefunden über die TNM-API (`tnmaccess.nationalmap.gov/api/v1/products`, Datensatz „Digital
   Elevation Model (DEM) 1 meter“); drei Kacheln 10 × 10 km `USGS_1M_4_x6{1,2,3}y236_HI_NOAAMauiOahu_2020_B20.tif` auf
   `prd-tnm.s3.amazonaws.com` (zusammen 626 MB, COG). `cog.py` liest nur Kopf und gebrauchte interne Kacheln per HTTP-Teilabruf (72 Stück,
   `../dl/dem/blocks/`). Metadaten und Bericht: `prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/metadata/HI_NOAAMauiOahu_2020_B20/
   HI_NOAAMauiOahu_2_B20/reports/`. Bilinear alle 10 Linienmeter, 4263 Punkte, 13 ohne Wert (Wasser unter Brücken, Daten 6).
   FABDEM war nicht nötig.
6. `deck.py`, `ept.py`, `clean.py`: **Brücken.** Die Punktwolke desselben Flugs liegt als EPT auf AWS (`usgs-lidar-public/
   HI_NOAAMauiOahu_2_B20`, EPSG:3857). Höhenbezug gleich: Bodenpunkte und Modell an drei Stellen (km 7, 20, 41) auf 1 cm gleich.
   Je 10-m-Punkt um die OSM-Brücken das 10-%-Quantil der Punkte ohne Boden, Wasser und Rauschen im Umkreis von 4 m (`deck.log`).
   - **Kalākaua Avenue über den Ala-Wai-Kanal** (km 7,23–7,28): Modell 0,6 m (Wasserfläche), Fahrbahn 2,7–3,9 m aus der Punktwolke;
     gilt als gemessen (nicht schraffiert).
   - Die übrigen acht OSM-Brücken (Kalanianaʻole Highway km 21,0, 22,4, 24,15, 28,75, 30,5, 31,9; Hawaiʻi Kai Drive 26,06) hat das Modell
     als Durchlass mit Fahrbahn: Punktwolke und Modell auf 0,1 m gleich.
   - **Vier Lücken** (Modell ohne Wert, auch die Punktwolke hat im Umkreis von 10 m keine Punkte): Kalanianaʻole Highway km 24,47–24,52
     (50 m) und 28,41–28,44, Hawaiʻi Kai Drive 24,79–24,81, Keahole Street 27,29–27,33. Gerade zwischen den gemessenen Enden (die sich um
     höchstens 0,17 m unterscheiden); **geschätzt**, in `D.bridges` (schraffiert).
   Sonst keine Glättung und keine Stufe über 1,5 m je 10 m (größte 1,27 m an der Ecke 18th/Kilauea Avenue, echt, Daten 8).
7. `stationen.py`: **Verpflegung** laut Streckenplan 2026: 18 nummerierte Stationen, 1 ist der Startbereich. Lage: Die Spitze jedes
   Zeigers ist von Hand aus dem Plan abgelesen (Kontaktbögen `../dl/pdf/stationen_bogen1.png`, `…2.png`) und über die Kilometermarken
   des Plans in km umgerechnet; der Plan ist schematisch, **etwa ±0,3 km**, in der App „ca.“. Symbole im Plan: Wasser überall,
   „Precision Fuel & Hydration“ (Sportgetränk) an 4–10, 12–15, 17; Gel an 6, 8, 10, 14. Gegenproben: „What to expect“: „The first Aid
   Station is at approximately 2.5 miles (3.5K) from the start, and then every 2 to 3 miles“ (hier Station 2 bei km 3,5); FAQ: „PF&H PF
   30 Gels will be available at four of the aid stations, at 9 miles, 12 miles, 15 miles 20 miles (exact location may vary by up to half a
   mile)“ (hier Meile 8,8 / 12,7 / 15,5 / 20,6). Die Texte sprechen von 16 Stationen, der Plan zeigt 17 an der Strecke.
   In der App: mit Gel „Verpflegung“ (food), mit Sportgetränk „Getränke“, sonst „Wasser“ (water); 17 Marken und Halbmarathon. Nicht
   übernommen: Sanitäter, Toiletten, Musik, Anfeuern, Elite-Stationen (EAS), Duschen und Essen im Ziel.
8. `build.py`: Höhen in cm im 10-m-Raster, Median über 30 m; Straßenstücke unter 80 m und Viertel unter 300 m dem Vorgänger
   zugeschlagen. `route.py` (lat0/lon0 21,3/−157,8), `tiles.py` (z12–z15), `tiles_z11.py honolulu`, `app.py`, `tiles_rand.py honolulu 2`:
   26 Kartenstücke, 1,7 MB.
   **Abgleich** (`vergleich.py`, `planprofil.py`): Das Höhenbild im Streckenplan 2026 („Elevation start 14 ft, max 132 ft, gain 641 ft“),
   aus dem PDF digitalisiert, passt ohne Verschiebung und Streckung (Korrelation 0,991; Bild minus App im Median −1,6 m, 95 % innerhalb
   3,3 m; höchster Punkt Bild 39,3 m bei km 14,85, App 38,8 m bei km 14,82; zweiter Gipfel beide 35,8 m bei km 39,6–39,7). FAQ: „The
   highest point on the course is 124 feet above sea level near mile 9“ (37,8 m, Meile 9 = km 14,5). Auch die Senke auf der 18th Avenue
   und die Kuppe an der Kilauea Avenue (km 15,0–15,4) zeigen Bild und Strava. Die 641 ft (195 m) des Veranstalters entsprechen den
   Rohdaten ohne Messfenster (193 m).

   | Quelle | Start | Ziel | min | max (km) | ↑/↓ 200 m | ↑ 1 km | gegen App (Median) | r |
   |---|---|---|---|---|---|---|---|---|
   | App (Laser 1 m, bereinigt) | 2,0 | 2,6 | 1,5 | 39,1 (14,82) | 143/143 | 89 | – | – |
   | Strava-Höhen der Linie | 3,1 | 3,0 | 1,9 | 40,3 (14,74) | 140/140 | 91 | +1,0 | 0,975 |
   | Höhenbild im Plan | 0,5 | 0,6 | −0,5 | 39,3 (14,83) | 132/132 | 90 | −1,6 | 0,991 |

## Ergebnis

↑ 143 m / ↓ 142 m mit 200-m-Fenster, ↑ 176 / ↓ 176 m mit 50 m, ↑ 165 / ↓ 165 m mit 100 m, ↑ 89 / ↓ 89 m mit 1 km; wie GPS-Uhren
149 (ab 0,5 m), 135 (ab 1 m), 111 (ab 3 m); Rohdaten ↑ 193 m. Start 2,0 m auf dem Ala Moana Boulevard, Ziel 2,6 m am Kapiʻolani Park,
tiefster Punkt 1,5 m am Kalanianaʻole Highway bei Maunalua Bay (km 28,2), höchster 38,8 m an der Diamond Head Road / 18th Avenue
(km 14,8); Höhenbereich 37,3 m. Flach durch Downtown, Kakaʻako und Waikīkī (2–6 m), über die Ala-Wai-Brücke (4 m), ab dem Kapiʻolani
Park die Diamond Head Road hinauf (+5,4 % über 200 m bei km 12,3), um den Krater zum höchsten Punkt, über die 18th Avenue steil
hinunter (−9 % über 100 m), kurz hinauf an die Kilauea Avenue (33 m) und hinunter nach Kāhala (−6,6 % über 200 m bei km 15,5, steilste
Stelle). Über das Ende der H-1 (15 m) auf den Kalanianaʻole Highway, nach Hawaiʻi Kai und zurück fast eben am Meer (1,5–7 m). Über Kāhala
ein zweites Mal um Diamond Head (36 m, km 39,6), hinunter zum Park (−5,4 % bei km 40,3) und flach ins Ziel.
**Modellzeit:** Mit 4:00/km im Flachen ergibt das Modell **2:50:12** (das Profil kostet 85 s); **bei 2:50:00 kostet es 85 s, bei 4:00:00
121 s** (Flach-Pace 3:59,7 bzw. 5:38,4 /km; gemessen mit `pruefen.js` in der App 2.2). Zum Vergleich bei 2:50:00: Wien 61 s, Boston
88 s, Stockholm 113 s.

Geprüft mit Playwright (Chromium, 393 × 852, Faktor 2, Server auf Port 8791, `pruefen.js`, `pruefen2.js`, `pruefen3.js`): keine
Konsolenfehler, `APP_VERSION` 2.2 und Knopf v2.2, Service Worker installiert (32 Einträge im Cache `hnl-marathon-profil`), Tipp auf die
Version meldet „Version 2.2 ist aktuell“; alle 26 Kartenstücke passen zu `D.tiles` und `sw.js`; Tabellen bei 320/375/393/430 px ohne
Überbreite, Seite nicht breiter als das Fenster. Laufansicht am Start, km 7,25 (Ala-Wai-Brücke), 12,3 (Diamond Head Road), 14,8
(höchster Punkt), 26 (Hawaiʻi Kai), 39,6 (zweiter Gipfel), 42,05 (Ziel) und die Kartenübersicht mit Verpflegung bei km 33 angesehen;
Zuschauer-Tabelle mit „Ortszeit Honolulu“ und 13. Dezember 2026; „Woher die Zahlen kommen“ angesehen. Bilder in `work/shots/`.
`kern.py` meldet „Alle gleich“.

## Offen

- Prüfung am iPhone (ʻokina in der Schrift: erscheint als schmales ‘, lesbar).
- Kilometer nur gleichmäßig gestaucht (Daten 2); Marken mit Koordinaten gibt es nicht. Verpflegung aus dem schematischen Plan (±0,3 km).
- Die Strava-Linie ist eine geplante Route, keine Vermessung; der Garmin-Kurs derselben Seite ist nicht verglichen.
- Startseite: Karte fehlt. Eyebrow „JAL Honolulu Marathon“, Stadt „Honolulu“, „Kurs 2026“, `data-termine="2025-12-14 2026-12-13
  2027-12-12"`, `data-monat="12"`, ↑ 143 m / ↓ 142 m, Höhe 2–39 m, `data-such` z. B. „Honolulu Hawaii Hawaiʻi Oahu Oʻahu USA JAL Waikiki
  Waikīkī Diamond Head Kapiolani“; Mini-Profil mit 37 m Höhenbereich passt in die Grundhöhe 64 px. README-Tabelle und Liste der
  Präfixe (`hnl-`). **Teilnehmer 2025:** 22 703 im Ziel (runningwithrock.com, „The 25 Largest Marathons in the United States in 2025“,
  Januar 2026, eigene Zählung des Autors aus den Ergebnissen; fünftgrößter Marathon der USA), 23 131 am Start (Race Results Weekly,
  auf honolulumarathon.org), 28 746 Anmeldungen zum Marathon (Veranstalter laut japanischer Presse; 42 962 an allen drei Läufen des
  Wochenendes, Seite „Entry Statistics“). Eine Zielzahl des Veranstalters selbst habe ich nicht gefunden.
- Termine 2028 ff.: zweiter Sonntag im Dezember (FAQ), jährlich nachtragen.
