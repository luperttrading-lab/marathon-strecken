# Übergabe: Steigungsprofil SwissCityMarathon – Lucerne

Stand 31.10.2026, App-Version **2.4** (erste Fassung, angelegt mit `werkzeuge/kern/kern.py --neu` auf dem gemeinsamen Kern; die
Hauptsitzung zählt die Nummer beim Veröffentlichen hoch).
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/luzern/.

Die App hat den gemeinsamen Kern aus `hamburg/` und eigene Felder (Texte, `const D`, Speicherschlüssel `lzn-…`, Service-Worker-Cache
`lzn-marathon-profil`, löscht nur Caches mit Präfix `lzn-`; der Präfix war frei, `kern.py --neu` prüft das), ohne eigenes Manifest und
Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Startseite,
README, `version.json` und `karten.json` sind noch nicht angepasst (Hauptsitzung).

**Besonderheiten:** Zweite Schweizer Strecke, gebaut nach dem Muster Zürich. Höhen aus **swissALTI3D 0,5 m** (Laser-Geländemodell von
swisstopo), Brückenfahrbahnen aus **swissSURFACE3D Raster**, beide über `work/swissalti.py` (Kopie von `../zuerich/work/swissalti.py`,
nur der Zwischenspeicher liegt hier). Die Linie ist die **GPX-Datei des Veranstalters** („SCML_42KM_DEFINITIV“, entgegen der ersten
Recherche offiziell: Sie steckt in der Karte von TrackMaxx auf der Seite „Streckenpläne“), die Kilometer sind über die **42
Kilometermarken derselben Karte** geeicht. Neu gegenüber Zürich: **überdeckte Straßenstücke** (Hergiswil, Tunnel der
Hergiswilerstrasse), in denen das Geländemodell die Decke misst; sie sind wie in Hamburg zwischen den Portalen geschätzt
(`work/bedeckt.py`, `work/clean.py`). Straßennamen in Schweizer Schreibweise wie auf den Schildern („Haldenstrasse“, „Seestrasse“),
kein „ß“ in Eigennamen.

## Termin und Start

Offizieller Name **SwissCityMarathon – Lucerne** (so auf allen Seiten des Veranstalters und in den Medienmitteilungen; kein
Titelsponsor im Namen, Coop ist „Presenting Partner“; Veranstalter Verein SwissCityMarathon – Lucerne, Würzenbachstrasse 13, Luzern;
seit 2007, bis dahin „Lucerne Marathon“). Der **19.** war am **Sonntag, 25. Oktober 2026** (Medienmitteilung „Lauffest mit
Rekordbeteiligung und Marathon-SM“ vom 25./28.10.2026: „des 19. SwissCityMarathon vom Sonntag, 25. Oktober 2026“; Schweizer
Meisterschaft im Marathon). Der **20.** ist am **Sonntag, 31. Oktober 2027** (Startseite „Sonntag 31. Oktober 2027“, Seite „Zahlen und
Fakten“: „Der nächste SwissCityMarathon – Lucerne findet am 31. Oktober 2027 statt. Es ist die 20. Austragung“; dazu die European
Masters Marathon Running Championships). Immer am letzten Sonntag im Oktober. `D.termine` `["2026-10-25", "2027-10-31"]`, `D.tz`
Europe/Zurich, `D.ort` „Luzern“ und `D.ortKurz` „ Luzern“ (sonst nennte der Kern die Zeitzone „Zurich“), `D.start` = 505 (8:25). Kein
`D.lage`, `D.mauer`, `D.tor`, `D.zielschluss`. Seiten des Veranstalters in `dl/seiten/` (lokal), Abruf mit `work/seite.py`.

**Start** (`D.wellen`, sieben Knöpfe): Startslots laut Seiten „Start und Startzeiten“ und „Marathon“ (Stand Oktober 2026, ohne
Jahresangabe, mit den Kategorien 2027 daneben): Performance-Slot 8:25 (Frauen unter 3:30, Männer unter 3:00, Nachweis der letzten drei
Jahre), dann 8:26 (Pacemaker 3:00, 3:15, 3:30), 8:29 (3:40, 3:50), 8:32 (4:00), 8:34 (4:15), 8:36 (4:30, 4:45), 8:38 (5:00). Den Slot
wählt man bei der Anmeldung nach Wunsch und Verfügbarkeit, **nicht nach Leistung**, höchstens 500 je Slot; Buchstabe (A bis U, über
alle Läufe) und Startzeit stehen auf der Startnummer, später starten geht immer. Startadresse laut Veranstalter „Haldenstrasse 28“;
der Anfang der GPX-Linie liegt auf der Haldenstrasse am See, 13 m neben dem Startpunkt der Karte und gut 0,8 km Luftlinie westlich
vom Ziel im **Verkehrshaus der Schweiz**. Halbmarathon 9:58–12:00 (eigene Slots) und CityRun 10 km (Start in Horw) sind eigene Rennen
auf eigener Strecke.

**Zeitlimit:** Maximale Laufzeit Marathon 6:15 h, Zielschluss 15:00 Uhr; „Das Schlussfahrzeug startet hinter dem letzten Startslot
der jeweiligen Kategorie, Läufer:innen die überholt werden, sind nicht mehr Teil des offiziellen Wettkampfs.“ (Seite „Zielschluss“).
Steht im Text unter „Deine Startzeit“.

**Keine Staffel:** Distanzen sind Marathon, Halbmarathon, CityRun und CharityRun 10 km, Kinderläufe; die „Teamwertung“ zählt
Einzelzeiten ab fünf Läufern, ohne Wechsel. Also keine `relay`-Marken. **Halbmarathon-Marke** bei 21 098 m.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Reihenfolge: `parse.py`, `kmmarken.py`, `osm.py`, `strassen.py`, `bedeckt.py`, `dgm.py` (mit `swissalti.py`), `deck.py`, `clean.py`,
`orte.py`, `build.py`, `route.py`, `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py luzern`, `luzern/work/app.py` (beim ersten Mal über
`kern.py --neu luzern work/felder.json`, danach ersetzt es nur die Felder und lässt Kartenbilder und `D.tiles` stehen),
`tiles_rand.py luzern 2`. Nur Abgleich: `vergleich.py`; zum Nachsehen `wege.py <von> <bis> [m]` (OSM-Wege neben der Linie),
`seite.py` (Seiten des Veranstalters als Text). Prüfen: `pruefen.js`, `pruefen2.js`, `pruefen3.js` (Server auf Port 8792 im
Repo-Wurzelordner, `NODE_PATH=/opt/node-tools/node_modules node pruefen.js`).

1. **Strecke** (`parse.py`): Die Seite „Streckenpläne“ (`swisscitymarathon.ch/event-guide/strecke/streckenplaene/`) bettet die
   Karte `trackmaxx.ch/maps/?m=092b4c28-cd0c-4d0b-b4e4-965d0c5cfcbc` ein (Bemerkung „Neue Strecke 2025“). Ihre Einstellungen
   (`trackmaxx.ch/maps/api.ashx?action=getmap&mapoid=…&view=alle`, `../dl/trackmaxx/getmap.json`) nennen für „42.2 km“ die Datei
   `https://tmxx-static.s3.amazonaws.com/ous/swisscitymarathon/mapstudio/gpx/scml_42km_definitiv.gpx?v=2503121124` (Fassung
   12.03.2025, `../dl/gpx/`): Track „SCML_42KM_DEFINITIV“, erstellt mit MySchweizMobil, 1773 Punkte mit Höhen. Doppelte, versetzte
   Punkte von MySchweizMobil entfernt wie in Zürich: 1208 Punkte, **42 808,0 m** (geodätisch, 1,45 % zu lang). Vermessen nach World
   Athletics/AIMS am 09.03.2025 (Zertifikat SUI/2025/078/JFD2850 A, Messer Roger Kaufmann, gültig bis 31.12.2029, „Separation 2.10 %“,
   „Elevation Change 0 m/km“; Seite „Offiziell vermessen“, `../dl/pdf/`). **Kurs 2026 = Kurs 2025:** Die Strassensperrungen 2026
   (PDF, Stand August 2026) nennen genau die Straßen der Linie, die Zeitmesspunkte 2026 (TrackMaxx: St. Niklausen km 5, Spissen km 10,
   Hergiswil km 15, Wendepunkt km 22,3, Niederstad km 23,5, Hergiswil km 29,6, Horw km 33,4, Stadion km 35,6) passen dazu.
2. `kmmarken.py`, `common.py`: Die Karte hat für den Marathon 42 Punkte „KM 1“ … „KM 42“ genau auf der Linie, im Abstand von 1008 bis
   1020 Linienmetern (nicht gleichmäßig, also wohl die Marken der Vermessung; belegt ist das nicht). **Kilometer stückweise linear**
   über diese Marken, Start am Linienanfang, Ziel am Linienende (letzte 195 m: 197,7 m Linie). Gegenüber gleichmäßigem Stauchen höchstens
   24 m Unterschied (km 31). Die Wende in Alpnachstad liegt so bei km 22,24 (Zeitmessung: „Wendepunkt (KM 22.3)“).
3. `osm.py`: OSM über die API in 123 Rechtecken zu 0,005° höchstens 150 m neben der Linie, eine Abfrage je Sekunde (`../dl/osmapi/`)
   → `../dl/osm_netz.json` (10 680 Wege). `strassen.py` wie Zürich, aber **ohne Autobahnen und Rampen** (sonst nahm der A2-Tunnel
   „Spier“ unter dem Veloweg nach Hergiswil den Platz ein). Kurze Stücke unter **50 m** (Zürich 80 m) gehen im Vorgänger auf, damit in
   der Altstadt Krongasse, Reussbrücke und Kramgasse einzeln erscheinen. Von Hand benannt (`build.py`, nach Linienmetern): „Veloweg
   Horw–Hergiswil“ (hin) und „Hergiswilerstrasse“ (zurück; in OSM ohne Namen, Namen aus der Sperrliste des Veranstalters), „Fuss- und
   Radweg“ (Horw Brändi bis Horwerstrasse, ohne Namen), „thermoplan arena“ (km 35,43–35,66, die Linie läuft durch die OSM-Fläche des
   Stadions, früher swissporarena/Stadion Allmend), „KKL“ (km 38,59–38,70, Durchlauf) und „Verkehrshaus“ (Zielgelände ab km 42,05).
4. `orte.py`: **Gemeinde und Ortschaft** alle 100 m, je 40 m links und rechts nachgesehen. Gemeinden aus swissBOUNDARIES3D (geo.admin.ch
   `find`, `../dl/orte/gem_*.json`), Ortschaften aus dem amtlichen Ortschaftenverzeichnis (Ebene `ch.swisstopo-vd.ortschaftenverzeichnis_plz`,
   `../dl/orte/plz_bbox.json`), ohne Kantonskürzel; angezeigt „Horw, St. Niklausen“, „Horw, Kastanienbaum“, „Alpnach, Alpnachstad“, sonst
   nur die Gemeinde (PLZ-Gebiete von Nachbargemeinden, etwa 6052 Hergiswil in Horw, zählen nicht). Folge: Luzern, Horw (St. Niklausen,
   Kastanienbaum), Horw, Hergiswil, Stansstad (Lopper), Alpnach (Alpnachstad) und zurück bis Luzern. **Quartiere der Stadt Luzern fehlen:**
   Die Stadt veröffentlicht sie (opendata.swiss „Einteilung statistische Quartiere und Stadtkreise“), aber nur über `map.stadtluzern.ch`,
   und das war aus dieser Umgebung nicht erreichbar (Verbindung abgebrochen; opendata.swiss antwortete 403).
5. `swissalti.py`, `dgm.py`: **Höhe aus swissALTI3D 0,5 m**, alle 10 Linienmeter bilinear (4282 Punkte), dazu 2 m und die GPX-Höhen zum
   Vergleich (`dgm_vergleich.json`). 30 Kacheln, alle Jahrgang 2022. Höhen in m ü. M. (LN02); 0,5 m und 2 m gleich bis auf Zentimeter.
6. **Überdeckte Stücke** (`bedeckt.py`, `clean.py`): OSM-Wege mit `tunnel=*` oder `covered=yes` höchstens 4 m neben der Linie und in
   gleicher Richtung; wo das Geländemodell dort mehr als 1,5 m über der GPX-Höhe liegt, misst es die Decke. Die Fahrbahn ist dann eine
   Gerade zwischen den Portalen (bis das Modell wieder auf 0,5 m bei der GPX-Höhe liegt), schraffiert, `D.bridges`:
   - **Seestrasse in Hergiswil**, hin km 16,80–16,87 (Unterführung unter einer überdeckten Autobahnrampe, Modell 455 m, Fahrbahn 435,7 m) und km 17,24–17,51 (`covered=yes`, 270 m, Modell 443,5–444,5 m, Fahrbahn 436,5 → 437,2 m), zurück km 26,98–27,24 und
     27,61–27,68. Was genau darüber liegt (A2-Anschluss Hergiswil/Lopper), habe ich nicht bestimmt; die GPX-Höhen dort (436,2–436,9 m)
     bestätigen die Gerade auf 0,4 m.
   - **Tunnel der Hergiswilerstrasse** km 31,14–31,29 (150 m, OSM `tunnel=yes`, `layer=-1`, Kantonsstrasse 4; Modell 452 m, Fahrbahn
     443,6 → 444,0 m). Nur auf dem Rückweg: Hin läuft die Linie 13 m daneben auf dem Veloweg an der Oberfläche (441–445 m), zurück
     0,7 m neben der Tunnelachse. Die Sperrliste nennt beide Wege („Veloweg Horw-Hergiswil ab Seerosenweg bis Kreisel Schlüssel“ und
     „Hergiswilerstrasse ab Kreisel Hinterbach bis Kreisel Schlüssel“).
   Unterführungen unter Brücken misst das Modell richtig (Brücke weg, Boden sichtbar): Velotunnel unter der Langensandbrücke (km 37,45),
   Durchgang unter der Bahn bei Horw (km 34,66). Über der Tiefgarage an der Rösslimatt (km 37,81, `layer=-2`) läuft die Strecke oben.
7. **Brücken** (`deck.py`, `clean.py`): Kandidaten sind Stellen, an denen **swissSURFACE3D Raster 0,5 m** (Jahrgang 2020, 15 Kacheln;
   25-%-Quantil von 5 × 5 Werten im Abstand 1 m) mehr als 0,5 m über dem Geländemodell liegt, Punkte unter 434,2 m (Vierwaldstättersee
   433,6 m) und Senken über 0,8 m unter dem Median der 120 m um die Stelle. Ersetzt wird nur, wo das Geländemodell zwischen den Rändern
   mehr als 0,5 m unter der Geraden liegt (sonst führt eine Brücke über die Strecke: A2-Rampen in Hergiswil, A8 in Alpnachstad,
   Vordach am Bahnhof, Verkehrshaus). Gemessen (Oberflächenmodell glatt): **Seebrücke** (km 1,46–1,63, Fahrbahn 435,9–437,0 m über dem
   See), **Europaplatz** vor dem KKL (km 1,81–1,86, 435,4 m über dem Wasserlauf), **Bahnbrücke der Kantonsstrasse in Horw** hin
   (km 12,14–12,26) und zurück (km 32,20–32,34), bis 444 m, Rampen 6–7 %, **Reussbrücke** (km 39,38–39,44, 436,0–436,2 m) und zehn kleine
   Brücken über Bäche und Wege (St. Niklausenstrasse km 6,1, Kantonsstrasse km 11,8 und 32,7, Veloweg km 12,75 und 13,25, Seestrasse
   km 14,9, Brünigstrasse km 21,9, 22,6 und 22,8, Fuss- und Radweg km 34,6). **Geschätzt** (Bäume über der Fahrbahn, Modell 7 m tiefer):
   St. Niklausenstrasse km 6,53–6,58, Gerade 453,5 → 452,7 m (GPX dort 453,2/453,1). Eine flache Mulde im Wald (Stutzstrasse km 5,95,
   0,7 m) bleibt gemessen. Danach keine Stufe über 1,3 m je 10 m (Zielgelände km 42,12, auch in der GPX).
8. `build.py`: **Verpflegung** nach dem Verpflegungsplan des Veranstalters (`SwissCityMarathon-Lucerne_Verpflegungsplan.pdf`, InDesign
   03.07.2025, verlinkt auf der Seite „Verpflegung“, `../dl/pdf/`): Marathon bei km 4, 8, 11, 15, 17,5, 21, 23,5, 27, 30, 34, 35, 37, 39
   (15/30, 17,5/27 und 21/23,5 dieselben Stellen hin und zurück). Inhalt je Stelle aus den Symbolen: km 4 und 39 Wasser und SPONSER
   Competition („Getränke“, `water`), km 11 nur Wasser („Wasser“), km 35 Wasser und Cola („Getränke“), km 8 und 34 dazu Riegel und
   Banane, km 15, 17,5, 21, 23,5, 27, 30 und 37 zusätzlich Gel („Verpflegung“, `food`). Lage nur als Kilometerzahl, eine Karte der
   Posten gibt es nicht. Höhen in cm im 10-m-Raster, Median über 30 m; Straßenstücke unter 50 m und Orte unter 300 m dem Vorgänger
   zugeschlagen. `route.py` (lat0/lon0 47,0/8,3), `tiles.py` (z12–z15), `tiles_z11.py luzern`, `app.py`, `tiles_rand.py luzern 2`:
   22 Kartenstücke, 1,9 MB.

   **Abgleich** (`vergleich.py`, offizielle km, Verfahren wie die App; letzte Spalte vor „gegen App“: einfache Summe aller Anstiege):

   | Quelle | Start | Ziel | min (km) | max (km) | ↑/↓ 200 m | ↑ 100 m | ↑ 50 m | ↑ 1 km | ↑ Punkt für Punkt | gegen App (Median) | r |
   |---|---|---|---|---|---|---|---|---|---|---|---|
   | App (swissALTI3D 0,5 m, Brücken aus swissSURFACE3D, Tunnel geschätzt) | 436,8 | 434,9 | 434,6 (39,17) | 471,6 (7,65) | 167/169 | 197 | 216 | 80 | 248 | – | – |
   | swissALTI3D 0,5 m ohne Bereinigung | 436,8 | 434,9 | 433,4 (39,40) | 471,6 (7,65) | 188/189 | 232 | 270 | 86 | 356 | ±0,00 | 0,982 |
   | swissALTI3D 2 m, gleiche Brücken und Tunnel | 436,7 | 434,9 | 434,6 (39,12) | 471,6 (7,65) | 167/169 | 197 | 216 | 80 | 255 | ±0,00 | 1,000 |
   | GPX-Höhen des Veranstalters (MySchweizMobil) | 436,8 | 434,9 | 434,6 (39,16) | 471,5 (7,64) | 156/157 | 178 | 194 | 79 | 220 | +0,01 | 0,998 |
   | Höhenprofil der TrackMaxx-Karte (100 Punkte, ganze Meter) | 437,0 | 435,0 | 435,0 (1,10) | 468,9 (5,15) | 106/108 | 112 | 114 | 70 | 118 | +0,10 | 0,940 |

## Höhenmeter: 175 oder 220?

Der Veranstalter schreibt auf der Seite „Marathon“ (Reiter „Streckenplan“): „Höhenmeter +175m / -175m. Diverse GPX-Files sowie
Webdienste zeigen fälschlich einen Wert von 220m an. Diese Angabe ist aufgrund von digitalen Messungen nicht zutreffend & um 45m zu
hoch.“ Ergebnis mit dem Laser-Modell:

- Die **220 m** sind genau die Summe aller Anstiege Punkt für Punkt in **seiner eigenen GPX-Datei** (1773 Punkte: ↑ 220,2 m, ↓ 222,1 m).
  Dasselbe Verfahren ergibt im Laser-Modell (10-m-Raster, bereinigt) sogar **248 m**, ohne Bereinigung der Brücken und Tunnel 356 m.
  Die 220 m sind also nicht „falsch“, sondern zählen jede kurze Welle mit.
- Die **175 m** liegen zwischen dem App-Standard (Messfenster 200 m: **↑ 167 m / ↓ 169 m**) und dem 100-m-Fenster (197 m). Wie GPS-Uhren
  (Anstieg zählt ab 0,5 / 1 / 3 m) ergäben sich 190 / 169 / 122 m. Mit welchem Verfahren der Veranstalter auf 175 m kommt, schreibt er
  nicht.
- Start und Ziel liegen 1,9 m auseinander (436,8 m Haldenstrasse, 434,9 m Verkehrshaus); deshalb ist bergab etwas mehr als bergauf.
- Das Höhenbild der TrackMaxx-Karte (nur 100 Punkte, ganze Meter) ist zu grob: 118 m, und es verpasst den höchsten Punkt (469 statt
  471,6 m).

## Ergebnis

↑ 167 m / ↓ 169 m mit 200-m-Fenster, ↑ 216 / ↓ 218 m mit 50 m, ↑ 197 / ↓ 198 m mit 100 m, ↑ 80 / ↓ 81 m mit 1 km; Rohdaten ↑ 248 m.
Start 436,8 m auf der Haldenstrasse, Ziel 434,9 m im Verkehrshaus, tiefster Punkt 434,6 m an der Reuss (km 39,2), höchster 471,6 m auf
der St. Niklausenstrasse über Kastanienbaum (km 7,65); **Höhenbereich 37 m**. Flach durch die Stadt, in Tribschen kurz auf 445 m
(km 3,7), dann der Anstieg über Langensand- und Stutzstrasse auf den Stutz (471,1 m, km 5,2): **steilste Stelle +7,9 % über 200 m bei
km 5,0** (+8,0 % über 100 m bei km 5,1). Über die Horwer Halbinsel wellig, zweiter Gipfel 471,6 m (km 7,65), steil hinunter an den See
bei Kastanienbaum (−5,7 % über 200 m bei km 8,0). Flach um die Halbinsel nach Horw, über die Bahnbrücke (444 m, km 12,2) und den
Veloweg über einen Hügel nach Hergiswil (447 m, km 13,7). Von km 14 bis 30 fast eben am See (435–442 m; kleiner Buckel um die Wende in
Alpnachstad, 442 m bei km 22,0 und 22,5). Zurück auf der Hergiswilerstrasse auf 447 m (km 30,8), Bahnbrücke Horw (−7,1 % über 100 m
bei km 32,3, die steilste Stelle bergab bei diesem Fenster), dann über Krienser- und Brändistrasse 17 m hinauf bis vor das Stadion
(453 m, km 34,8), fast eben durch die thermoplan arena und ab km 36 hinunter durch Tribschen an den See (435 m, km 38). Flach durch
KKL, Altstadt und über die Haldenstrasse ins Ziel.
**Modellzeit:** Mit 4:00/km im Flachen ergibt das Modell **2:50:35** (das Profil kostet 108 s); **bei 2:50:00 kostet es 108 s, bei
4:00:00 152 s** (Flach-Pace 3:59,2 bzw. 5:37,7 /km; gemessen mit `pruefen.js` in der App 2.4). Zum Vergleich bei 2:50:00: Zürich 36 s,
Wien 61 s, Boston 88 s, Stockholm 113 s.

Geprüft mit Playwright (Chromium, 393 × 852, Faktor 2, Server auf Port 8792, `pruefen.js`, `pruefen2.js`, `pruefen3.js`): keine
Konsolenfehler, `APP_VERSION` 2.4 und Knopf v2.4, Service Worker installiert (28 Einträge im Cache `lzn-marathon-profil`), Tipp auf die
Version meldet „Version 2.4 ist aktuell“; Tabellen bei 320/375/393/430 px ohne Überbreite, Seite nicht breiter als das Fenster.
Laufansicht am Start, km 1,5 (Seebrücke), 5,0 (Stutz), 7,65 (höchster Punkt), 13,6 (Veloweg), 17,4 (Seestrasse überdeckt),
22,24 (Wende), 31,2 (Tunnel Hergiswilerstrasse), 35,5 (Stadion), 38,65 (KKL), 39,4 (Reussbrücke), 42,1 (Ziel) und die
Kartenübersicht mit Verpflegung bei km 22 angesehen; Zuschauer-Tabelle mit „Ortszeit Luzern“, 31. Oktober 2027, Startslot-Knöpfen und
dem Text zu Zielschluss; „Woher die Zahlen kommen“ mit der Liste der geschätzten Stücke. Bilder in `work/shots/`. `kern.py` meldet
alle Apps „gleich“, dazu „karten.json veraltet“ (neue Strecke; Hauptsitzung mit `--schreiben`).

## Offen

- Prüfung am iPhone.
- **Startslots:** Die Seite nennt keine Jahreszahl; ob 2026 dieselben Zeiten galten, ist nicht belegt (Starterguide 2026 nur per
  E-Mail, Marathonzeitung 2026 bei Flowpaper nicht mehr abrufbar). Für 2027 vor dem Rennen prüfen.
- **Verpflegung** nur als Kilometerzahl aus dem Plan vom Juli 2025; die genaue Lage der Tische ist nicht veröffentlicht.
- **Rückweg durch den Tunnel der Hergiswilerstrasse** nur aus der GPX-Linie (hin Veloweg, zurück Strasse); bei Gelegenheit mit Bildern
  oder Strava-Spuren 2026 gegenprüfen. Die überdeckten Stücke in Hergiswil sind geschätzt (Gerade, GPX bestätigt auf 0,4 m).
- **Kilometermarken:** Dass die Punkte der TrackMaxx-Karte die Marken der Vermessung sind, ist eine Annahme (ungleiche Abstände).
- **Quartiere Luzern** fehlen (siehe Daten 4); mit Zugang zu `map.stadtluzern.ch` (WFS „Einteilung statistische Quartiere und
  Stadtkreise“) in `orte.py` ergänzen wie in Zürich.
- **Kurs 2027:** European Masters Marathon Running Championships; ob sich die Strecke ändert, ist nicht angekündigt.
- **Startseite:** Karte fehlt. Eyebrow „SwissCityMarathon – Lucerne“, Stadt „Luzern“, „Kurs 2026“, `data-termine="2026-10-25 2027-10-31"`,
  `data-monat="10"`, Termintext „So., 31. Oktober 2027“, ↑ 167 m / ↓ 169 m, Höhe 435–472 m, `data-such` z. B. „Luzern Lucerne Lucerna
  Schweiz Switzerland Suisse CH SwissCityMarathon Swiss City Vierwaldstättersee Horw Hergiswil Alpnachstad Lopper KKL Verkehrshaus“;
  Mini-Profil mit 37 m Höhenbereich. README-Tabelle und Liste der Präfixe (`lzn-`). Fuß der Startseite: Höhen „swissALTI3D und
  swissSURFACE3D © swisstopo“ (wie Zürich).
  **Teilnehmer 2026: 3 375 im Ziel** des Marathons (TrackMaxx-Rangliste `trackmaxx.ch/results/?race=scm26`, über
  `api.trackmaxx.ch/resultlist/race/57528459-…/list/…` gezählt: Zeit und kein Vermerk eines letzten Messpunkts; 766 Frauen und 2 310
  Männer rangiert = 3 076, dazu 299 „Marathon (ohne Rangierung)“, die ohne Rang im Ziel sind; 1 Disqualifizierter mit Zeit nicht
  gezählt). Die Medienmitteilung nennt „3’376 Finisher“ (mit dem Disqualifizierten). Gemeldet 4 176, nicht gestartet 705, aufgegeben 90
  (am häufigsten nach Niederstad km 23,5 und Hergiswil km 29,6), 5 nur mit Startzeit. Keine Namen gespeichert (Zählung in `/tmp`, danach gelöscht).
- Gegenprobe mit dem privaten Eichdatensatz (`course_segments`) nicht gemacht: Die Datei lag in dieser Sitzung nicht vor.
