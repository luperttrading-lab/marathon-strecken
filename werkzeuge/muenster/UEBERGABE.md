# Übergabe: Steigungsprofil Volksbank-Münster-Marathon

Stand 31.10.2026, App-Version **2.4** (erste Fassung, angelegt mit `werkzeuge/kern/kern.py --neu` auf dem gemeinsamen Kern; die
Hauptsitzung zählt die Nummer beim Veröffentlichen hoch).
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/muenster/.

Die App hat den gemeinsamen Kern aus `hamburg/` und eigene Felder (Texte, `const D`, Speicherschlüssel `mst-…`, Service-Worker-Cache
`mst-marathon-profil`, löscht nur Caches mit Präfix `mst-`; der Präfix war frei, `kern.py --neu` prüft das), ohne eigenes Manifest und
Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Startseite,
README, `version.json` und `karten.json` sind noch nicht angepasst (Hauptsitzung).

**Besonderheiten:** Eine GPX-Datei veröffentlicht der Veranstalter nicht. Die Linie kommt wie in Düsseldorf aus dem **Streckenplan 2026
als Vektorkarte** (orange Linie in zehn Teilstücken, eingepasst an die OSM-Straßen). Die gezeichnete Linie ist 2,0 % zu lang; die
Kilometer sind deshalb **stückweise zwischen den Kilometerkreisen des Plans** gestreckt (5, 10 … 40 km und „HM“, alle auf der Linie).
Höhen aus **DGM1 NRW**, anders als in Düsseldorf nicht auf der gezeichneten Linie, sondern **auf dem OSM-Weg darunter** gemessen (die
Linie liegt bis 18 m neben der Fahrbahn). Brücken aus dem **DOM1 NRW**. Es gibt einen **Staffelmarathon** auf derselben Strecke (vier
Läufer, drei Wechsel in `D.marks`, der Kern zeigt damit den Staffel-Schalter).

## Termin und Start

Veranstalter Münster-Marathon e.V. (Windthorststraße 32, Münster; überwiegend ehrenamtlich, gegründet 2001), Namenssponsor Volksbank (seit
dem ersten Lauf 2002; die Zielbühne heißt „Volksbank im Münsterland“). Offizieller Name **„Volksbank-Münster-Marathon“** (so im Text der
Seiten, in FAQ und Marathonguide; Seitentitel „Volksbank Münster Marathon“), Seite https://www.volksbank-muenster-marathon.de/
(`muenster-marathon.de` hat nur ein abgelaufenes, selbst ausgestelltes Zertifikat). Nächste Austragung, der **25.**, am **Sonntag,
12. September 2027** (Startseite: Countdown „12.09.2027“ bis „2027-09-12T09:00:00“, „Online-Anmeldestart am 2. November 2026 … zu unserem
Jubiläumslauf, dem 25. Volksbank-Münster-Marathon“, `../dl/seiten/start.html`; Marathonguide 2026: „12.09.2027 SAVE THE DATE“). Der 24.
war am Sonntag, 13. September 2026 (Dauerregen laut Dank an die Helfer). `D.termine` `["2026-09-13", "2027-09-12"]` (2027 bestätigt, ohne
„?“), `D.tz` Europe/Berlin, `D.start` = 540 (9:00). Kein `D.lage`, `D.mauer`, `D.tor`, `D.zielschluss`.

**Start** (`D.wellen` ohne Wellenknöpfe, nur Text): „Der Marathon-Start erfolgt um 9.00 Uhr“, Startblöcke nach Bestzeit: „Gruppe 1 …
bis 3:00 h, Gruppe 2 … bis 3:30 h, Gruppe 3 … bis 4:00 h, Gruppe 4 … ab 4:00 h und alle Erstteilnehmer:innen“ (FAQ „Stand 23.10.2026“,
Datei `FAQ_Webseite_2027_…`, also schon für 2027; ebenso Marathonguide 2026, `../dl/pdf/`). Ein Start, keine Wellen. Atruvia
Staffelmarathon 9:15 Uhr („15 Minuten nach dem Marathonstart“, aus dem letzten Block), Wecker-28 (28 km) 10:10 Uhr am
Kardinal-von-Galen-Ring. **Zielschluss** „Nach 6:00 Stunden (Marathon) bzw. um 15.00 Uhr“; „Teilnehmer:innen, die über den jeweiligen
Sollzeiten liegen, werden aus dem Rennen genommen“, am Ende des Feldes fährt ein Bus. Steht im Text unter „Deine Startzeit“.
Brems- und Zugläufer 3:00 bis 6:00 (FAQ).

**Start und Ziel:** Start auf dem Schlossplatz (Straße östlich des Schlossgartens, Linienanfang am Schild „START“ des Plans), Ziel auf
dem Prinzipalmarkt am Rathaus (Linienende am Schild „ZIEL“, 70 m nach der Ecke Rothenburg/Ludgeristraße).

**Halbmarathon-Marke** bei 21 098 m (Kreis „HM“ des Plans an der Altenberger Straße in Nienberge). **Staffel** mit vier Etappen „ca. 10,5 /
11,0 / 10,0 / 10,7 km“ (Marathonguide 2026, S. 42–43), Wechsel „Weseler Str./Ecke Bismarckallee“, „in Nienberge / Altenberger Straße“,
„Roxeler Straße / Nähe Dingbängerweg“. Etappe 2 läuft nach dem ersten Wechsel „direkt in die Scharnhorststraße und kommt an der Ecke
Richard-Schirrmann-Weg wieder auf die Originalstrecke“ (blaue Linie im Plan, etwa gleich lang).

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Reihenfolge: `parse.py`, `grob.py`, `osm.py`, `georef.py`, `strecke.py`, `eichung.py`, `strassen.py`, `dgm.py`, `dom.py`, `clean.py`,
`orte.py`, `build.py`, `route.py`, `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py muenster`, `muenster/work/app.py` (beim ersten Mal über
`kern.py --neu muenster work/felder.json`, danach ersetzt es nur die Felder und lässt Kartenbilder und `D.tiles` stehen),
`tiles_rand.py muenster 2`. Nur Abgleich: `marken.py`. Hilfe: `text.py` (Text einer gespeicherten Seite). Prüfen: `pruefen.js` …
`pruefen4.js` (Server auf Port 8791, `NODE_PATH=/opt/node-tools/node_modules node pruefen.js`).

1. **Strecke** (`parse.py`): **Streckenplan 2026** des Veranstalters, `marathon_streckenplan_verlauf_2026_02.pdf` (InDesign 23./24.07.2026,
   A3 quer, Kartengrund „Streckenplan ©Stadt Münster“), verlinkt auf der Seite „Infos“ unter „Streckenverlauf … (Amtliche Vermessung vom
   02.09.2025)“: https://www.volksbank-muenster-marathon.de/_data/marathon_streckenplan_verlauf_2026_02.pdf (`../dl/pdf/`). Ganz aus
   Vektoren; die Strecke ist ein oranger Pfad (0,91/0,30/0,06, 2 pt) aus zehn Teilstücken, dazu drei dünnere Linien (1,5 pt) in der
   Aegidiistraße, durch die die Strecke dreimal läuft (km 0,7, 10,1, 41,4), und fünf gepunktete Stücke („Unter-, Überführungen“). Die
   Reihenfolge der Teilstücke ist in `FOLGE` von Hand festgelegt (Pfeile, Kilometerkreise, Verpflegungstabelle) und per Anfangs- und
   Endpunkt geprüft; die gepunkteten Stücke sind Geraden. Dazu die Marken: neun Kilometerkreise (05 … 40, HM), 14 Verpflegungssymbole (01–15,
   „05, 15“ gemeinsam), drei Staffelwechsel, 25 Pfeile. Eine GPX-Datei, eine Tour (wie Visit Düsseldorf) oder eine OSM-Relation habe ich
   nicht gefunden (Overpass nicht erreichbar). Die Strecke 2026 entspricht laut Veranstalter der Vermessung vom 02.09.2025.
2. `grob.py`: grobe Einpassung über zehn Ortsbeschriftungen der Karte (Schloss, Dom, Hauptbahnhof, Zentralfriedhof, Mühlenhof, Buddenturm,
   Lepramuseum, Picassomuseum, Botanischer Garten; Nominatim, eine Abfrage je Sekunde, `../dl/nominatim/`), affin, im Median 69 m genau.
   `osm.py` (Kopie Düsseldorf): OSM-API in 167 Rechtecken zu 0,005° höchstens 300 m neben dieser Linie, eine Abfrage je Sekunde, keine
   Fehler → `../dl/osm_netz.json` (12 247 Wege).
3. `georef.py`: **Einpassung** affin an allen OSM-Wegen (ICP, Fangradius 150 → 60 → 30 → 20 m): Planlinie **im Median 2,1 m neben einer
   OSM-Straße, 90 % bis 7,1 m**, 99 % bis 18 m; nur die Gerade durch die Unterführung am Coesfelder Kreuz liegt bis 65 m daneben (die
   Domagkstraße ist dort in OSM `highway=construction`). Maßstab 6,96 m/pt in beiden Richtungen, Achsen rechtwinklig (90,09°): Die Karte ist
   ein Stadtplan in UTM, anders als in Düsseldorf nicht verzerrt.
4. `strecke.py` → `strecke2026.json` (1 936 Punkte, **43 021,6 m** geodätisch, 2,0 % zu lang; Douglas-Peucker mit 2 m kürzt nur 43 m, es
   sind also keine Zacken). `eichung.py`, `common.py`: **Kilometer stückweise** zwischen den Kilometerkreisen des Plans (Mitte 0–20 m neben
   der Linie), Start am Linienanfang, Ziel am Ende. Linienmeter je Meter: 0–5 km 0,989, 5–10 1,023, 10–15 0,997, 15–20 1,066, 20–21,1
   0,962, 21,1–25 1,016, 25–30 1,038, 30–35 1,018, 35–40 1,013, 40–Ziel 1,040. `marken.py`: Gegenprobe mit den Verpflegungssymbolen (der
   kleine Punkt jedes Symbols auf der Linie) gegen die km der Tabelle: stückweise |Abweichung| im Median 0,12 km, gleichmäßig über die ganze
   Linie 0,17 km; Ausreißer in beiden Fällen Kanonierplatz (+0,45), Gievenbecker Reihe (−0,45) und Wulfertstraße (−0,88). Gegen
   gleichmäßiges Strecken spricht auch die Lage der Straßen: Scharnhorststraße/Platz der Weißen Rose 11,71 (Tabelle 11,8), Vesaliusweg
   14,40–14,55 (14,5), Mergelberg/Nünningweg 34,99 (35,0). **Genauigkeit der Kilometer etwa ±0,2 km.** Für den Wecker-28 (Start
   Kardinal-von-Galen-Ring, 28 km) passt keine der beiden Eichungen genau (nach Linie sind es von dort 27,6 km bzw. 27,9 km gleichmäßig).
5. `strassen.py` (Kopie Düsseldorf ohne Rheinufertunnel): je 10 m der nächste OSM-Weg bis 20 m mit höchstens 35° Richtungsabweichung,
   Hauptstraßen bevorzugt.
6. `dgm.py` (Kopie Düsseldorf/Köln): **DGM1 NRW** über WCS (`www.wcs.nrw.de/geobasis/wcs_nw_dgm`, Coverage `nw_dgm`, EPSG:25832), 4 304
   Punkte in 130 Ausschnitten, keiner fehlt. Lizenz dl-de/zero-2-0. **Neu:** gemessen am Lotfußpunkt auf dem OSM-Weg von `strassen.py`
   (4 242 Punkte, Versatz im Median 2,8 m, 90 % 9,8 m); ohne Weg (Unterführungen) auf der Linie. Das senkte die Rohdaten von 229 auf 200 m
   bergauf; das 200-m-Fenster blieb bei 133 m (die Wellen sind Gelände). In der Aegidiistraße stimmen Hin- und Rückweg jetzt überein
   (Senke der Aa 56,4 m in der Mitte der Straße, 59,5 m an der Rothenburg).
7. `dom.py` (Kopie Düsseldorf): **Brücken aus dem DOM1 NRW** (WCS `wcs_nw_dom`), je 10-m-Punkt Lotfußpunkt auf den OSM-Weg, dort das
   25-%-Quantil der 5 × 5 m. Neu: Werte mehr als 1 m über dem höheren Ende oder 0,5 m unter dem tieferen gelten als Baum und werden
   zwischen den Nachbarn ersetzt (Promenade 6 von 9 Werten, roh bis 73 m; Twerenfeldweg, Arnheimweg, Roxeler Straße am Gievenbach je 1). An
   allen Enden DOM gleich DGM (±0,1 m), größte Stufe 0,43 m je 10 m (`dom.log`). Achtmal über die **Aa**: Am Stadtgraben km 0,51–0,59,
   Bispinghof 1,25–1,33, Neubrückenstraße 2,84–2,92, Promenade 6,73–6,82, Kardinal-von-Galen-Ring 11,95–12,17 (DGM 54,1 = Wasser, Deck
   60,0–60,7), Twerenfeldweg 26,37–26,44, Roxeler Straße 31,96–32,03, Adenauerallee 41,12–41,20; **Haus Uhlenkotten (K 12) über die B 54**
   19,78–19,89 (DGM 75,7, Deck bis 81,8), **Steinfurter Straße (L 510) über die A 1** 21,00–21,10 (bis 82,4), **Roxeler Straße (L 843) über
   die A 1** 30,80–30,92 (DGM 68,0, Deck 74,2); dazu Bredeheide über einen Graben 28,16–28,22, Arnheimweg 36,70–36,76 und Roxeler Straße
   37,53–37,60 über den Gievenbach. Alle gelten als gemessen (nicht schraffiert).
8. `clean.py` (Kopie Düsseldorf): setzt die DOM-Werte ein, dann Stufen über 1,5 m je 10 m → Gerade. Ausgenommen (`GEMESSEN`) die
   **Unterführung der Promenade unter dem Servatiiplatz** (km 7,36–7,54, OSM `tunnel=yes`): Die Straße darüber ist eine Brücke und im DGM
   entfernt, gemessen ist die Rampe 4 m hinunter und wieder hinauf (60,7 → 56,4 → 61,4 m). Übrig bleiben zwei **Unterführungen, geschätzt**
   (`D.bridges`, schraffiert): **Domagkstraße unter dem Coesfelder Kreuz** (km 15,41–15,45; DGM misst die Von-Esmarch-Straße darüber, 64,6 m;
   Gerade 61,6 → 58,8 m, davor und danach die Rampen gemessen) und **Am Rüschhaus unter der B 54** (km 23,24–23,27; 79,4 m → Gerade
   75,7 → 76,1 m). Zwei weitere Stellen werden nur geglättet und nicht gezeigt: Sprung zwischen den Wegen am Aegidiitor (km 10,42–10,54) und
   ein Punkt in einer Rinne an der Ecke Ahausweg/Rüschhausweg (km 35,87).
9. `orte.py` (Kopie Düsseldorf): Münster ist in OSM dreistufig (9 Stadtbezirke, 10 Stadtteile/Zählgebiete, 11 statistische Bezirke). Innerhalb
   des Rings die Bezirke der Stufe 11 (Kreuzviertel, Schlachthof, Bahnhof, Pluggendorf, Josef, Aaseestadt, Schloss), sonst Stufe 10
   (Altstadt, Sentruper Höhe, Gievenbeck, Kinderhaus, Nienberge, Roxel); 29 Flächen über die OSM-API (`../dl/orte/`), je 40 m links und
   rechts. „Schloss“ ist der amtliche Name des Bezirks westlich des Schlosses (Annette-Allee bis Vesaliusweg), nicht das Gebäude.
10. **Verpflegung** (in `build.py`, Tabelle des Veranstalters im Streckenplan und im Marathonguide 2026, S. 14): 8 Erfrischungspunkte (nur
    Wasser) und 7 Verpflegungspunkte (Wasser, sanotact Elektrolyte Plus, Bananen und Apfelsinen, Eigenverpflegung; Salvus Cola laut Tabelle
    ab km 20,3, laut Text „ab km 25,3“). In der App: EP „Wasser“ (water), VP „Verpflegung“ (food), Nummern der Reihe nach je Art. Lage nach
    den km der Tabelle, außer wo sie dem genannten Ort widersprechen: **Kanonierplatz** (Tabelle 4,3) liegt an der Linie bei km 4,74, das
    Symbol bei 4,75 → 4,7; **Wulfertstraße** (Tabelle 30,0) liegt bei 28,95–29,17, das Symbol bei 29,1, der Kreis „30“ 0,9 km weiter an der
    Schelmenstiege → 29,1. Beide nennen im Text die Tabelle mit. Gievenbecker Reihe bleibt bei 37,5 (Symbol 37,05; die Straße endet bei
    37,47). Zielverpflegung (VP 8) liegt hinter dem Ziel und fehlt. Nicht übernommen: Power Points (10), Medical Points, Toiletten.
11. **Staffelwechsel** (`build.py`): Wechsel 1 an der Kreuzung Weseler Straße/Bismarckallee km 10,71 (der Punkt des Symbols 10,77),
    Wechsel 2 Altenberger Straße km 21,15 (Symbol direkt über dem Kreis „HM“; die Straße reicht von 21,07 bis 21,61), Wechsel 3
    Roxeler Straße/Dingbängerweg km 31,29 (Symbolpunkt 31,28). Etappen auf der Linie 10,7 / 10,4 / 10,1 / 10,9 km (Veranstalter „ca. 10,5
    / 11,0 / 10,0 / 10,7“).
12. `build.py`: Höhen in cm im 10-m-Raster, Median über 30 m; Straßenstücke unter 80 m und Stadtteile unter 300 m dem Vorgänger
    zugeschlagen, nur die letzten 70 m auf dem Prinzipalmarkt bleiben. Ohne Namen in OSM (asphaltierte Wege, `highway=path`): km 12,40–12,70
    vom Kardinal-von-Galen-Ring durch die Wiesen am Aasee zur Annette-Allee und km 27,41–27,92 zwischen Stodtbrockweg und Bredeheide, beide
    „Fuß- und Radweg“. `route.py` (lat0/lon0 51,96/7,58), `tiles.py` (z12–z15), `tiles_z11.py muenster`, `app.py`,
    `tiles_rand.py muenster 2`: 21 Kartenstücke, 2,2 MB.

## Ergebnis

↑ 133 m / ↓ 131 m mit 200-m-Fenster, ↑ 162 / ↓ 159 m mit 50 m, ↑ 152 / ↓ 149 m mit 100 m, ↑ 72 / ↓ 70 m mit 1 km; wie GPS-Uhren 141 (ab
0,5 m), 117 (ab 1 m), 72 (ab 3 m); Rohdaten ↑ 200 m. Start 57,5 m am Schlossplatz, Ziel 60,3 m auf dem Prinzipalmarkt; tiefster Punkt
52,2 m in der Kanalstraße an der Aa (km 6,28), höchster 83,7 m an der Altenberger Straße in Nienberge (km 21,3); **Höhenbereich 31,5 m**.
Der Veranstalter schreibt „Unsere Strecke ist im Grunde ohne Anstieg“ und zeigt ein Profil von etwa 57 bis 76 m (`../dl/pdf/Streckenprofil_neu.png`);
das DGM reicht weiter (Nienberge liegt höher, die Aa tiefer).
Verlauf: Altstadt 54–60 m mit der Aa-Senke in der Aegidiistraße, im Kreuzviertel 8 m hinauf (62,6 m bei km 4,7) und 10 m hinunter an die
Aa (km 6,3), über die Promenade wieder hinauf, Unterführung am Servatiiplatz (4 m), eben durch die Altstadt (59–61 m), am Aasee 57–63 m,
Coesfelder Kreuz (Unterführung, 58,5 m), dann von km 15,5 bis 19,7 durch Gievenbeck und über den Horstmarer Landweg 17 m hinauf, über die
Brücke über die B 54 (**+4,1 % über 200 m bei km 19,73, die steilste Stelle**), über die A 1 nach Nienberge (83,7 m), 23 m hinunter an die
Aa am Twerenfeldweg (km 26,4), in Roxel 15 m hinauf (75,7 m bei km 28,9), über die A 1 und 15 m hinunter an die Aa (km 32,0), nach
Gievenbeck 12 m hinauf (71,6 m bei km 33,5), wellig bis km 39 (65–72 m), hinunter an den Aasee (58 m) und zuletzt die Aegidiistraße 4 m
hinauf ins Ziel. Steilste Stelle bergab −2,9 % über 200 m bei km 15,42 (Unterführung Coesfelder Kreuz, geschätzt).
**Modellzeit:** Mit 4:00/km im Flachen ergibt das Modell **2:50:01** (das Profil kostet 74 s); **bei 2:50:00 kostet es 74 s, bei 4:00:00
104 s** (Flach-Pace 4:00,0 bzw. 5:38,8 /km; gemessen mit `pruefen.js` in der App 2.4). Zum Vergleich bei 4:00/km im Flachen: Hannover
18 s, Düsseldorf 37 s, Köln 48 s (laut ihren Übergaben).

Geprüft mit Playwright (Chromium, 393 × 852, Faktor 2, Server auf Port 8791, `pruefen.js` … `pruefen4.js`): keine Konsolenfehler,
`APP_VERSION` 2.4 und Knopf v2.4, Service Worker installiert (27 Einträge im Cache `mst-marathon-profil`), Tipp auf die Version meldet
„Version 2.4 ist aktuell“; alle 21 Kartenstücke passen zu `D.tiles` und `sw.js`; Tabellen bei 320/375/393/430 px ohne Überbreite, Seite
nicht breiter als das Fenster. Laufansicht am Start, km 4,7 (Kanonierplatz), 7,43 (Servatiiplatz), 15,43 (Coesfelder Kreuz), 19,85
(Brücke über die B 54), 21,3 (höchster Punkt), 26,36 (Aa), 30,85 (A 1), 41,6 (Aegidiistraße), 42,1 (Ziel) und die Kartenübersicht mit
Verpflegung und Staffel bei km 21 angesehen; Zuschauer-Tabelle mit „So., 12. September 2027“ und „Ortszeit Berlin“; Kopf und „Woher die
Zahlen kommen“ angesehen. Bilder in `work/shots/`. `kern.py` meldet alle Apps „gleich“, dazu „karten.json veraltet“ (neue Strecke,
Hauptsitzung).

## Offen

- Prüfung am iPhone.
- **Kilometer:** Die gezeichnete Linie ist 2 % zu lang, die Kreise des Plans strecken sie ungleichmäßig (15–20 km um 6,6 %). Ob die Kreise
  oder die Verpflegungstabelle stimmen, lässt sich ohne GPX oder Vermessungsprotokoll nicht klären; Kanonierplatz, Gievenbecker Reihe und
  Wulfertstraße passen nicht zu ihren Tabellen-km. Bei einer GPX-Datei oder Liste der Kilometerschilder (Veranstalter fragen)
  `eichung.py` ersetzen.
- **Kurs 2027:** Plan noch nicht veröffentlicht (Anmeldestart 2. November 2026; Ausschreibung 2027 „in Kürze“). Kommt ein neuer Plan,
  `parse.py` (Dateiname, `FOLGE`) und die Kette erneut laufen lassen, Farben der Symbole und `VP`/`SW` in `build.py` prüfen.
- Der Plan ist eine Zeichnung (keine Vermessung); die drei Linien in der Aegidiistraße liegen nebeneinander, die Höhen dort kommen von
  den Wegen darunter.
- Unterführungen Coesfelder Kreuz und Am Rüschhaus geschätzt; die Domagkstraße am Coesfelder Kreuz ist in OSM eine Baustelle
  (`highway=construction`), ob dort 2027 anders gelaufen wird, ist offen.
- Staffelwechsel 2 nur nach dem Symbol (direkt beim Halbmarathon); Etappe 2 wäre damit 10,4 statt „ca. 11,0“ km.
- Startseite: Karte fehlt. Eyebrow „Volksbank-Münster-Marathon“, Stadt „Münster“, „Kurs 2026“, `data-termine="2026-09-13 2027-09-12"`,
  `data-monat="9"`, Termintext „So., 12. September 2027“, ↑ 133 m / ↓ 131 m, Höhe 52–84 m, `data-such` z. B. „Muenster Munster
  Münsterland Westfalen Nordrhein-Westfalen NRW Deutschland Volksbank Aasee Prinzipalmarkt“; Mini-Profil mit 31,5 m Höhenbereich passt in
  die Grundhöhe 64 px (Hamburg 36 m ohne eigene Klasse). README-Tabelle und Liste der Präfixe (`mst-`). Höhenquelle im Fuß: „DGM1 … NRW“
  steht schon (Köln, Düsseldorf), DOM1 NRW für die Brücken wie Düsseldorf (© Geobasis NRW, dl-de/zero-2-0).
  **Teilnehmer 2026:** **3 370 im Ziel** des Marathons (offizielle Ergebnisliste „24. Volksbank-Münster-Marathon“ bei RaceTime/datacapo,
  verlinkt auf der Seite „Ergebnisse“ des Veranstalters: https://datacapo.racetime.net/e/24-volksbank-munster-marathon/results; Rangliste
  „Einzel“, „3370 Ergebnisse · Wertung nach Nettozeit“, letzte Seite Platz 3361–3370, letzte Zeit 5:59:13, Stand 24.09.2026; nur Platz und
  Zeit gelesen, keine Namen gespeichert). Die Übersicht der Veranstaltung nennt „3.371 im Ziel“ und 4 447 angemeldet. Staffel 1 521
  Teams im Ziel, Wecker-28 501. **2025:** 3 114 (Ergebnisliste bei xivado, „23. Volksbank-Münster-Marathon“, 21.09.2025, letzter Platz
  3 114, dazu 2 disqualifiziert).
- Termine 2028 ff.: jährlich nachtragen (September, 2026 und 2027 jeweils am zweiten Sonntag).
