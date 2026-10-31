# Übergabe: Steigungsprofil Jungfrau-Marathon

Stand 31.10.2026, App-Version **2.5** (erste Fassung, angelegt mit `werkzeuge/kern/kern.py --neu` auf dem gemeinsamen Kern; die
Hauptsitzung zählt die Nummer beim Veröffentlichen hoch).
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/jungfrau/.

Die App hat den gemeinsamen Kern aus `hamburg/` und eigene Felder (Texte, `const D`, `SHORT`, Speicherschlüssel `jfm-…`, Service-Worker-Cache
`jfm-marathon-profil`, löscht nur Caches mit Präfix `jfm-`; der Präfix war frei, `kern.py --neu` prüft das), ohne eigenes Manifest und
Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Startseite,
README, `version.json` und `karten.json` sind noch nicht angepasst (Hauptsitzung).

**Besonderheiten:** Erster Bergmarathon der Sammlung und dritte Schweizer Strecke, gebaut nach dem Muster Luzern. Punkt-zu-Punkt von
Interlaken (566,5 m) zum Eigergletscher (2330 m), ab Lauterbrunnen fast nur Wander- und Bergwege. Höhen aus **swissALTI3D 0,5 m**
(Laser-Geländemodell von swisstopo), Brückenfahrbahnen aus **swissSURFACE3D Raster**, beide über `work/swissalti.py` (Kopie von
`../zuerich/work/swissalti.py`, nur der Zwischenspeicher liegt hier). Auf Pfaden liegt der Weg auf dem Boden, dort gilt das Geländemodell
unverändert. Die Linie ist die **vermessene Strecke des Veranstalters** („Originalstrecke 2024“, GPX und KMZ auf der Seite „Strecke“); sie
ist in der Ebene genau 42,195 km lang, die Kilometer laufen gleichmäßig über sie. Höhenbereich **1768 m**, 7,3 km steiler als 10 %.
Unser Pace-Modell ist an Straßenmarathons geeicht und am Berg zu optimistisch; die Texte der Strecke stellen die Modellzeiten nicht als
realistisch dar, der Untertitel nennt die Gehpassagen (Hinweis im Kern: Hauptsitzung). Straßen- und Ortsnamen in Schweizer Schreibweise.

## Termin und Start

Offizieller Name **Jungfrau-Marathon** (so auf allen Seiten, im Reglement und in der Race-Info; Veranstalter Verein Jungfrau-Marathon,
Strandbadstrasse 44, Interlaken; auf der Startseite „Presented by“ mit Logo, kein Sponsor im Namen). Der **33.** war am **Samstag,
5. September 2026** (Rangliste Datasport „jungfrau-marathon-2026“, 05.09.2026; Bericht des Veranstalters „Überraschungssieg am 33.
Jungfrau-Marathon“ vom 06.09.2026; Freitagsrennen am 4.9.). Die Startseite nennt unter „Nächste Austragungen“: „34. Jungfrau-Marathon
10. / 11. September 2027“ (Anmeldung ab 14.02.2027, 8 Uhr), dann 8./9. September 2028 und 7./8. September 2029. Wie 2026 (Freitag
Freitagsrennen, Samstag Marathon) ist der Marathon am **Samstag, 11. September 2027**; ausdrücklich „Marathon am 11.“ steht dort nicht,
das Wochenende ist bestätigt. `D.termine` `["2026-09-05", "2027-09-11"]`, `D.tz` Europe/Zurich, `D.ort` „Interlaken“ und `D.ortKurz`
„ Interlaken“ (sonst nennte der Kern die Zeitzone „Zurich“), `D.start` = 510 (8:30). Kein `D.lage`, `D.mauer`, `D.tor`, `D.zielschluss`.
Seiten des Veranstalters in `dl/seiten/` (lokal), Abruf mit `work/seite.py`; die Race-Info 2026 (FlippingBook) als Text in
`dl/raceinfo_text.txt`, Seite 7 (Durchlaufzeiten) als Bild `dl/raceinfo/seite7.png`.

**Start** (`D.wellen`, ohne Wellenknöpfe, nur Text wie Zürich): „Massenstart um 08.30 Uhr Richtung Osten“ auf dem Höheweg in Interlaken
(Race-Info 2026, Seite „Lauf-Infos“). Startblöcke nach erwarteter Laufzeit, alle im selben Start: Elite (Nummern 1–200), Block 1 bis 4:40,
Block 2 4:40–5:10, Block 3 5:10–5:30, Block 4 5:30–5:50, Block 5 5:50–6:10, Block 6 6:10–6:30; vier Pacemaker mit „Beachflags“ für 5:00,
5:30, 6:00 und 6:30. Die Strecke führt nach einer Runde durch Interlaken bei km 3,3 noch einmal über den Startplatz.

**Kontrollschlüsse** (Reglement 2026, Seite „Strecke“; im Text unter „Deine Startzeit“, `D.tor` zeigt der Kern nur mit `D.mauer`):
„Wengen Bahnhof (km 30,7 km), nach 4 Std. 25 Min. Laufzeit. Die Strecke wird bei km 30,7 um 13.00 Uhr Ortszeit geschlossen.“ und
„Wengernalp, Abzweigung Wixi (km 38,5), nach 5 Std. 50 Min. Laufzeit … um 14.25 Uhr“ (beide Uhrzeiten 5 Minuten nach Start + Laufzeit).
Pace-Bike im Tempo der Kontrollschlüsse, dahinter das Besen-Bike; wer zu spät kommt, darf nicht weiter und wird nicht klassiert. Einen
Zielschluss nennt der Veranstalter nicht (die Spalte „Laufzeit 6.30 h“ der Durchlaufzeiten endet um 15.00 Uhr im Ziel; 2026 kamen
Läufer bis 7:35 h ins Ziel). Stöcke, Begleitfahrzeuge und Tiere sind verboten.

**Keine Staffel**, keine Halbmarathon-Wertung (Freitagsrennen sind eigene Läufe in Interlaken). **Halbmarathon-Marke** bei 21 098 m
(Zeitmessung „Staubbach – Halbmarathon“ km 21,1).

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Reihenfolge: `parse.py`, `osm.py`, `strassen.py`, `strassenverz.py`, `bedeckt.py`, `dgm.py` (mit `swissalti.py`), `deck.py`, `clean.py`,
`orte.py`, `build.py`, `route.py`, `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py jungfrau`, `jungfrau/work/app.py` (beim ersten Mal über
`kern.py --neu jungfrau work/felder.json`, danach ersetzt es nur die Felder und lässt Kartenbilder und `D.tiles` stehen),
`tiles_rand.py jungfrau 2`. Nur Abgleich: `vergleich.py`, `kmcheck.py`; zum Nachsehen `wege.py <von> <bis> [m]` (OSM-Wege neben der
Linie), `seite.py` (Seiten des Veranstalters als Text). Prüfen: `pruefen.js`, `pruefen2.js`, `pruefen3.js` (Server auf Port 8791 im
Repo-Wurzelordner, `NODE_PATH=/opt/node-tools/node_modules node pruefen.js`).

1. **Strecke** (`parse.py`): Seite „Strecke“ (`jungfrau-marathon.ch/de/strecke.html`), Downloads „GPX Daten Jungfrau-Marathon“
   (`Originalstrecke_2024.gpx`, 5,0 MB) und „KMZ Daten Jungfrau-Marathon“ (`Originalstrecke_2024.KMZ`), beide Track
   „ORIGINAL_STRECKE_2024_3D_DRAPED“ aus Global Mapper, 67 296 Punkte mit Höhen (`../dl/gpx/`, `../dl/kmz/`). Genommen wird die KMZ (10 statt 6
   Nachkommastellen, sonst gleich). Dazu „Vermessene Strecke“ (`Originalstrecke_Übersicht_2024.pdf`, Karte 1:40 000 von Flotron AG, 27.05.2024,
   mit Kilometermarken; `../dl/pdf/`). Länge **in der Ebene (LV95) 42 194,5 m**, geodätisch 42 193,5 m: Die Linie ist die vermessene Strecke
   selbst (3D gemessen wäre sie 42 431 m lang). Die Punkte liegen im Mittel 0,5 m auseinander und zittern seitlich (Ausdünnen auf 1 m
   kürzt um 21 m); gespeichert ist eine nach Douglas-Peucker (0,25 m) ausgedünnte Linie (1810 Punkte), je Punkt die Länge entlang der vollen
   Linie. **Kurs 2026 = Kurs 2024:** Die Seite bietet 2026 dieselben Dateien an, die Orte und Kilometer der Race-Info 2026 und der
   Verpflegung 2026 passen dazu (`kmcheck.py`). Bei viel Andrang öffnet der Veranstalter ab Wixi (km 38,9) eine „Entlastungsstrecke mit exakt
   gleicher Länge“; die Linie nimmt die „Strecke Süd“ (so heißt der Weg in OSM: „Junfrau-Marathon Teil Wixi–Haaregg (Strecke Süd)“).
2. `common.py`: **Kilometer gleichmäßig** über die Linie (Faktor 42 195 / 42 193,5). Abgleich mit den Orten der Durchlaufzeiten
   (`kmcheck.py`, OSM-Punkte): Interlaken West +0,14, Gsteig −0,07, Gsteigwiler +0,16, Zweilütschinen Bahnhof −0,06, Lauterbrunnen Bahnhof
   −0,02, Staubbach +0,07, Wengwald +0,02, Wengen −0,02, Wixi −0,04, Haaregg −0,09 km (Bahnhöfe und Weiler liegen bis 80 m neben der Linie).
3. `osm.py`: OSM über die API in 142 Rechtecken zu 0,005° höchstens 150 m neben der Linie, eine Abfrage je Sekunde (`../dl/osmapi/`) →
   `../dl/osm_netz.json` (3948 Wege). `strassen.py` wie Luzern (ohne Autobahnen), aber Wege und Pfade mit kleinerem Aufschlag (6 statt 14),
   dazu `sac_scale` und `surface`. `strassenverz.py`: **amtliches Strassenverzeichnis** (swisstopo, geo.admin.ch „identify“, 41 Rechtecke,
   `../dl/strassenverz/`) als zweite Namensquelle; es bringt kaum etwas (in Lauterbrunnen und Wengen werden Häuser über Gebiete adressiert,
   die Hauptstrasse hat dort keinen amtlichen Namen). Ab Wilderswil sind fast alle Wege ohne Namen. **Von Hand benannt** (`build.py`, nach
   offiziellen Metern): „Hauptstrasse“ in Lauterbrunnen hin (km 20,0–20,8) und zurück vom Trümmelbach (km 23,4–25,8) und in Zweilütschinen
   (Verkehrsinformation der Race-Info 2026: „Lauterbrunnen: Hauptstrasse, Zufahrt zum Parkhaus Lauterbrunnen sowie nach Stechelberg“;
   Kantonsstrassen 221/222), „Höheweg“ (Querung bei km 3,5), „Stocki“, „Zentrum Wengen“, „Waldschluecht“, „Wixi“ und „Eigergletscher“ (Fahrweg
   zur Station ab km 41,79) nach Orts- und Postennamen des Veranstalters bzw. OSM; beschreibend „Strasse über Gsteigwiler“, „Wanderweg an der
   Lütschine“, „Bahnhof Zweilütschinen“, „Wanderweg an der Weissen Lütschine“, „Wanderweg zum Trümmelbach“, „Bergweg nach Wengen“, „Strasse
   Wengen–Allmend“, „Weg zur Allmend“, „Bergweg Wixi–Haaregg“, „Bergweg über die Moräne“ (Wanderweg/Bergweg wie im Höhenprofil 2024 des
   Veranstalters: Asphaltstrasse bis km 8, Wanderwege bis Lauterbrunnen, Bergweg Stocki–Wengwald, Asphalt durch Wengen, Wanderweg bis Wixi,
   Bergweg bis ins Ziel). Aus OSM: Höheweg, Klosterstrasse, Alpenstrasse, Waldeggstrasse, Rugenparkstrasse, Bahnhofstrasse, Untere
   Bönigstrasse, Allmendstrasse, Lindenallee, Interlakenstrasse, In den Gärten, Am Quai, Seestrasse, Hauptstrasse und Gsteigstrasse
   (Bönigen), Bönigstrasse, Alte Staatsstrasse, Allmendstrasse (Wilderswil), Alter Tripfiweg, Alte Stechelbergstrasse, Wengwaldweg,
   Mendelssohnweg (Allmend–Wengernalp). **`SHORT`** kürzt die langen beschreibenden Namen nur für die Zeile unter dem Profil („Weisse
   Lütschine“, „Wixi–Haaregg“, „Moräne“ …), sonst passten sie dort oft nicht hin.
4. `orte.py`: **Gemeinde und Ortschaft** alle 100 m wie Luzern (swissBOUNDARIES3D über „find“ für zehn Gemeinden, Ortschaftenverzeichnis
   über „identify“, `../dl/orte/`), ohne Zusätze „b. Interlaken“. Folge: Interlaken (am Rand Matten bei Interlaken), Bönigen, an der Lütschine
   „Bönigen / Matten bei Interlaken“ und „Matten bei Interlaken / Wilderswil“ (der Fluss ist die Grenze), Gsteigwiler, „Gündlischwand,
   Zweilütschinen“, Lauterbrunnen, ab km 27,4 „Lauterbrunnen, Wengen“. Die Ortschaft Wengen (PLZ 3823) reicht bis zum Eigergletscher; darüber
   von Hand wie in den Durchlaufzeiten der Race-Info („Dorf“): „Lauterbrunnen, Wengernalp“ ab der Allmend (km 33,5) und „Lauterbrunnen,
   Eigergletscher“ ab Haaregg (km 40,2; Eigergletscher ist eine amtliche Ortschaft, PLZ 3823). Das Ziel liegt auf der Grenze zu Grindelwald.
5. `swissalti.py`, `dgm.py`: **Höhe aus swissALTI3D 0,5 m**, alle 10 Linienmeter bilinear (4221 Punkte), dazu 2 m und die Höhen der Linie
   zum Vergleich (`dgm_vergleich.json`). 38 Kacheln, alle Jahrgang 2025. 0,5 m und 2 m gleich bis auf Zentimeter.
6. **Überdeckte Stücke** (`bedeckt.py`): keine. OSM hat drei kurze Unterführungen (Lauterbrunnen km 25,9 und Wengen km 31,8 unter der Bahn,
   Mendelssohnweg km 34,6); dort misst das Geländemodell den Boden (nicht über den Höhen der Linie). Tunnel und Galerien hat die Strecke nicht.
7. **Brücken** (`deck.py`, `clean.py`): Kandidaten sind OSM-Brücken, Senken über 0,8 m unter der Geraden über ±40 m und Stellen, an denen die
   Höhen der Linie des Veranstalters (sie führen über die Brücken) mehr als 1 m über dem Geländemodell liegen. Kein Kriterium „Sprung je
   10 m“ wie in Luzern (am Berg bis 4 m je 10 m). Ersetzt nur, wo das Geländemodell zwischen den Rändern 0,8 m unter der Geraden liegt:
   **gemessen** aus **swissSURFACE3D Raster 0,5 m** (Jahrgang 2022, 24 Kacheln; 25-%-Quantil von 5 × 5 Werten), wo es glatt ist und über dem
   Gelände liegt: Interlakenstrasse Bönigen (km 6,04–6,10, über die Lütschine), Fahrweg vor Lauterbrunnen (km 19,69–19,77, 12,5 m über der
   Weissen Lütschine), Alte Stechelbergstrasse (km 21,18–21,22), Steg am Trümmelbach (km 23,32–23,37), Brücke über einen Bach oberhalb von Stocki (km 26,35–26,42),
   kleine Brücke vor der Allmend (km 32,98). **Geschätzt** (Gerade, schraffiert, `D.bridges`), wo Bäume oder Geländer das Oberflächenmodell
   stören, OSM eine Brücke hat und die Linie des Veranstalters die Senke nicht zeigt: Aegertenstrasse (km 8,95–9,01, Holzbrücke über die Lütschine), gedeckte
   Holzbrücke in Gsteig (km 10,35–10,40), Wanderweg an der Lütschine (km 14,04 Rindgrabe, km 14,88 Schwarze Lütschine), Wanderweg an der
   Weissen Lütschine (km 19,03 und 19,49, über den Fluss), Wanderweg zum Trümmelbach (km 23,00, Weisse Lütschine), Bergweg nach Wengen
   (km 26,70, über der Wengernalpbahn), Mendelssohnweg (km 33,81, Bach). Senken, in denen Linie des Veranstalters und Oberflächenmodell dieselbe Mulde zeigen (Bachgräben mit
   Durchlass, z. B. km 28,38 Innerer Brunnibach, km 39,70 und 39,79 am Weg Wixi–Haaregg), bleiben gemessen. Danach ist die Linie des
   Veranstalters im Median 5 cm höher, 95 % innerhalb −1,0/+0,5 m.
8. `build.py`: **Verpflegung** nach der „Wettkampfverpflegung 2026“ (`Marathon_Wettkampfverpflegung-Sponser_2026_WEB.pdf`, 25.03.2026,
   Download „Verpflegungsplan 2026“ auf der Seite „Strecke“; dazu die Karte „Verpflegungsposten 2026“), Selbstbedienung: Posten 1 Interlaken,
   im Moos km 5,5 (Wasser, Sponser Competition Orange und Citrus), 2 Wilderswil 10,0 (dazu Riegel, Banane), 3 Zweilütschinen, hinter der Egg
   16,0 (Riegel), 4 Lauterbrunnen 20,8 (Bouillon, Banane, Gel mit Koffein, Schwämme), 5 Trümmelbach 23,2 (Riegel, Gel mit Koffein),
   6 Lauterbrunnen «Stocki» 25,7 (Bouillon, Riegel, Banane), Wasserposten Undre Fuhren 27,9, 7 Wengen, Wengwald 29,2 (Bouillon, Riegel, Banane,
   Gel, Schwämme), 8 Wengen, Café Oberland 32,9 (dazu Cola), Wasser Baawald/Hannegg 34,7, 9 Mettla 36,3 (Cola, Bouillon, Riegel, Banane, Gel),
   10 Wixi 38,9 (alles, Schwämme), Wasser und Cola an Haaregg 40,3, Moräne 41,0 und Loucherflueh/«Schoggistei» 41,4. In der App 11 „Verpflegung“
   (food), 3 „Wasser“/„Getränke“ ohne Essen und 3 Cola-Stellen als „Getränke“ (water). Lage über die Kilometer des Plans. Höhen in cm im
   10-m-Raster, Median über 30 m; Straßenstücke unter 50 m und Orte unter 300 m dem Vorgänger zugeschlagen. `route.py` (lat0/lon0 46,6/7,9),
   `tiles.py` (z12–z15), `tiles_z11.py jungfrau`, `app.py`, `tiles_rand.py jungfrau 2`: 29 Kartenstücke, 2,1 MB.

   **Abgleich** (`vergleich.py`, offizielle km, Verfahren wie die App; „Punkt für Punkt“ der Linie: alle 67 296 Punkte):

   | Quelle | Start | Ziel | min (km) | max | ↑/↓ 200 m | ↑ 100 m | ↑ 50 m | ↑ 1 km | ↑ Punkt für Punkt | gegen App (Median) |
   |---|---|---|---|---|---|---|---|---|---|---|
   | App (swissALTI3D 0,5 m, Brücken aus swissSURFACE3D bzw. geschätzt) | 566,5 | 2330,1 | 562,6 (4,71) | 2330,1 | 1928/165 | 1975 | 2012 | 1815 | 2076 | – |
   | swissALTI3D 0,5 m ohne Bereinigung | 566,5 | 2330,1 | 562,6 (4,71) | 2330,1 | 1928/165 | 1977 | 2020 | 1815 | 2135 | ±0,00 |
   | swissALTI3D 2 m, gleiche Brücken | 566,5 | 2330,1 | 562,7 (1,95) | 2330,1 | 1928/165 | 1975 | 2012 | 1815 | 2082 | ±0,00 |
   | Höhen der Linie des Veranstalters („3D_DRAPED“) | 566,4 | 2329,7 | 562,8 (1,94) | 2329,7 | 1925/162 | 1967 | 1999 | 1814 | 2231 | +0,05 |

   In der App (Kern, Höhen in cm): ↑ 1929 / ↓ 165 m (200 m), 1976 (100 m), 2013 (50 m), 1816 (1 km); wie GPS-Uhren ab 0,5 / 1 / 3 m:
   2018 / 1997 / **1951** m. Die Brücken ändern am Berg kaum etwas an den Höhenmetern (die Senken sind kurz).

## Höhenmeter: 1953

Der Veranstalter nennt überall „1953 Höhenmeter“, den Start auf 567 m und das Ziel auf 2320 m. Ergebnis mit dem Laser-Modell: 1929 m mit
200-m-Fenster, 1976 m mit 100 m; die 1953 m liegen dazwischen und treffen fast genau das Verfahren einer GPS-Uhr, die einen Anstieg ab
3 m zählt (1951 m). Die 2320 m sind die Höhe der Station Eigergletscher; das Ende der Linie des Veranstalters liegt wie das Geländemodell auf
2330 m (das Zielgelände liegt über der Station). Die Linie des Veranstalters Punkt für Punkt ergäbe 2231 m (sie zittert um Zentimeter).

## Ergebnis

↑ 1929 m / ↓ 165 m mit 200-m-Fenster, Rohdaten ↑ 2076 m. Start 566,5 m auf dem Höheweg, Ziel 2330 m am Eigergletscher, tiefster Punkt 562,6 m
an der Lindenallee in Interlaken (km 4,7); **Höhenbereich 1768 m**. Die ersten 10 km flach (Runde durch Interlaken, Bönigen, an der Lütschine
nach Wilderswil, 584 m), dann über Gsteigwiler (+8,1 % bei km 10,7) nach Zweilütschinen (651 m, km 15) und an der Weissen Lütschine nach
Lauterbrunnen (800 m beim Halbmarathon, +7,7 % bei km 19,7). Fast flach zum Trümmelbach und zurück nach Stocki (789 m, km 25,9). **Anstieg
nach Wengen:** 4,8 km, +487 m, im Mittel +10,2 %, am steilsten +23,1 % über 200 m bei km 27,3 (Bergweg mit Kehren). Wengen 1276 m
(km 30,7), Allmend 1479 m (km 33,4), Mettla 1690 m (km 36,3), Abzweigung Wixi 1857 m (km 38,5), kurz hinunter zur Wixi (1827 m, km 38,9,
−11,9 % bei km 38,7, die steilste Stelle bergab), Haaregg 1990 m (km 40,2), über die Moräne auf 2196 m (km 41,5) und ins Ziel. **Steilste
Stelle +31,8 % über 200 m bei km 40,44** (Moräne; +35,4 % über 50 m bei km 40,42). Steiler als 10 %: 7,3 km, als 15 %: 3,6 km, als 20 %:
2,0 km (200-m-Fenster, wie die App rechnet).

Abschnitte zwischen den Zeitmesspunkten 2026 (↑/↓ mit 200-m-Fenster):

| Abschnitt | km | Höhe | ↑ / ↓ | Steigung im Mittel | steilste 200 m |
|---|---|---|---|---|---|
| Start – Runde Interlaken | 0–3,3 | 567 → 567 | 8 / 7 | 0 % | +1,4 % |
| Runde – ALDI | 3,3–5,0 | 567 → 567 | 4 / 4 | 0 % | +2,1 % |
| ALDI – Wilderswil | 5,0–10,4 | 567 → 588 | 26 / 5 | +0,4 % | +4,6 % |
| Wilderswil – Zweilütschinen | 10,4–15,1 | 588 → 651 | 101 / 37 | +1,3 % | +8,1 % |
| Zweilütschinen – Lauterbrunnen (Staubbach) | 15,1–21,1 | 651 → 800 | 161 / 13 | +2,5 % | +7,7 % |
| Lauterbrunnen – Stocki | 21,1–25,9 | 800 → 789 | 25 / 36 | −0,2 % | +4,5 % |
| Stocki – Wengen | 25,9–30,7 | 789 → 1276 | 502 / 13 | +10,2 % | +23,1 % |
| Wengen – Abzweigung Wixi | 30,7–38,5 | 1276 → 1857 | 590 / 13 | +7,5 % | +16,0 % |
| Wixi – Ziel | 38,5–42,195 | 1857 → 2330 | 511 / 36 | +12,8 % | +31,8 % |

**Modellzeit (nur für die Hauptsitzung, nicht in den Texten der Strecke):** Mit 4:00/km im Flachen ergibt das Modell 3:29:01 (das Profil
kostet 40:15 min); bei 2:50:00 kostet es 32:44 min, bei 4:00:00 46:12 min (gemessen mit `pruefen.js`). Vergleich mit den **Durchlaufzeiten
des Veranstalters** (Race-Info 2026, Seite 7, Richtzeiten): für 5:00 h rechnet er Halbmarathon 1:59, Wengen 3:11, Abzweigung Wixi 4:16;
das Modell verteilt dieselben 5:00 h als 2:08 / 3:20 / 4:22 (für 6:30 h: Veranstalter 2:35 / 4:10 / 5:33, Modell 2:47 / 4:19 / 5:40). Das
Modell schätzt den Berg also auch innerhalb einer Zielzeit zu billig. Die Spitze 2026: 3:08:27 (Männer), 3:20:56 (Frauen); Median aller
Finisher 5:40 h, Viertel 5:05 / 6:11 h.

Geprüft mit Playwright (Chromium, 393 × 852, Faktor 2, Server auf Port 8791, `pruefen.js`, `pruefen2.js`, `pruefen3.js`): keine
Konsolenfehler, `APP_VERSION` 2.5 und Knopf v2.5, Service Worker installiert (35 Einträge im Cache `jfm-marathon-profil`), Tipp auf die
Version meldet „Version 2.5 ist aktuell“; Tabellen bei 320/375/393/430 px ohne Überbreite, Seite nicht breiter als das Fenster.
Laufansicht am Start, km 3,3, 10,4 (Gsteig), 19,72 (Brücke), 21,1, 23,2 (Trümmelbach), 27,3 (Anstieg Wengen), 30,7 (Wengen), 36,5 (Mettla),
38,6 (Wixi), 40,44 (Moräne) und 42,1 (Ziel) und die Kartenübersicht mit Verpflegung bei km 30 angesehen; Zuschauer-Tabelle mit „Ortszeit
Interlaken“, 11. September 2027 und dem Text zu Start und Kontrollschlüssen; „Woher die Zahlen kommen“. Bilder in `work/shots/`. `kern.py`
meldet alle Apps „gleich“, dazu „karten.json veraltet“ (neue Strecke; Hauptsitzung mit `--schreiben`).

## Offen

- Prüfung am iPhone.
- **Profil mit 1768 m Höhenbereich (Kern):** Die Höhenachse hat höchstens 100-m-Schritte (`gstep` aus 5/10/25/50/100); hier 17 Linien
  im Abstand von etwa 17 px, die Beschriftungen „700 m … 2300 m“ stehen dicht und links über der Kurve (Bild `work/shots/start_profil.png`,
  `lauf_zahlen_km40_moraene_steilste.png`). Vorschlag: 200/250/500 in die Liste. Der Läuferblick ist dabei etwa 1-fach überhöht: Die ersten
  25 km liegen als fast gerade Linie am unteren Rand, die Anstiege ab Stocki sind gut lesbar.
- **Startseite:** Karte fehlt. Eyebrow „Jungfrau-Marathon“, Stadt „Jungfrau“, „Kurs 2026“, `data-termine="2026-09-05 2027-09-11"`,
  `data-monat="9"`, Termintext „Sa., 11. September 2027“, ↑ 1929 m / ↓ 165 m, Höhe 563–2331 m, `data-such` z. B. „Jungfrau Jungfraumarathon
  Interlaken Eigergletscher Eiger Lauterbrunnen Wengen Wengernalp Wixi Bönigen Wilderswil Zweilütschinen Berner Oberland Schweiz Switzerland
  Suisse CH Bergmarathon Berglauf Trail“. Mini-Profil: 1768 m Höhenbereich, im gemeinsamen Maßstab (40 m = 56 px) wären es 2475 px; braucht
  einen eigenen, deutlich kleineren Maßstab (Great Wall und Athen: halber Maßstab). Reihenfolge nach Teilnehmerzahl. README-Tabelle und Liste
  der Präfixe (`jfm-`). Fuß der Startseite: Höhen „swissALTI3D und swissSURFACE3D © swisstopo“ (wie Zürich und Luzern).
  **Teilnehmer 2026: 3604 im Ziel** des Marathons (Datasport-Rangliste `results.datasport.com/de/anlass/jungfrau-marathon-2026/ranking`,
  Listen „Frauen“ und „Männer“ mit `pageSize=200` gezählt: Rang und Endzeit; 898 Frauen und 2706 Männer, Ränge lückenlos 1–898 und
  1–2706). Gestartet 3925 (1021 Frauen, 2904 Männer) laut Übersicht der Rangliste; der Veranstalter schreibt von „4’000 Läuferinnen und
  Läufern“ (Startplätze). Keine Namen gespeichert (Zählung in `/tmp`, danach gelöscht).
- **Zwischenzeiten für die Eichung:** Datasport veröffentlicht 2026 für alle 3604 Finisher Zeiten an acht Messpunkten, als Abschnittszeiten
  in der Rangliste: „Runde Interlaken“ (km 3,3), „Interlaken km 5“, „Wilderswil km 10.4“, „Zweilütschinen km 15.1“, „Lauterbrunnen km 21.1“,
  „Lauterbrunnen km 25.9“, „Wengen km 30.7“, „Wixi km 38.5“, Ziel; dazu Summen Interlaken–Lauterbrunnen 21,1, –Wengen 30,7, –Wixi 38,5. Die
  Sortierung nennt außerdem „@ Preview“ (wohl ein Punkt kurz vor dem Ziel, ohne Kilometer). Messpunkte wie in der Race-Info („= Zeitmessung“).
  Nichts heruntergeladen. Mit den Abschnitten oben (Höhen und Steigung je Abschnitt) ließe sich das Modell am Berg eichen.
- **`D.lage`** nicht gesetzt: Die Strecke steigt von 567 auf 2330 m, eine einzige mittlere Höhe passt nicht; ob der Kern die Höhe am Berg
  berücksichtigen soll, entscheidet die Hauptsitzung.
- **Termin 2027:** Der Veranstalter nennt das Wochenende „10. / 11. September 2027“; der Samstag 11.09. als Marathontag folgt dem Muster
  2026, ausdrücklich steht er noch nicht da. Vor dem Rennen prüfen, ebenso Startblöcke und Kontrollschlüsse 2027 (Race-Info erscheint Ende
  August).
- **Wegnamen** ab Wilderswil sind großteils beschreibend (keine amtlichen Namen); die „Hauptstrasse“ in Lauterbrunnen stammt aus der
  Verkehrsinformation des Veranstalters. Die geschätzten Holzbrücken (9) sind Geraden zwischen den Ufern.
- Gegenprobe mit dem privaten Eichdatensatz (`course_segments`) nicht gemacht: Die Datei lag in dieser Sitzung nicht vor.
