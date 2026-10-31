# Übergabe: Steigungsprofil LGT Alpin Marathon

Stand 31.10.2026, App-Version **2.6** (erste Fassung, angelegt mit `werkzeuge/kern/kern.py --neu` auf dem gemeinsamen Kern; die
Hauptsitzung zählt die Nummer beim Veröffentlichen hoch).
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/liechtenstein/.

Die App hat den gemeinsamen Kern aus `hamburg/` und eigene Felder (Texte, `const D`, Speicherschlüssel `lgt-…`, Service-Worker-Cache
`lgt-marathon-profil`, löscht nur Caches mit Präfix `lgt-`; der Präfix war frei, `kern.py --neu` prüft das), ohne eigenes Manifest und
Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Startseite,
README, `version.json` und `karten.json` sind noch nicht angepasst (Hauptsitzung).

**Besonderheiten:** Erste Strecke in Liechtenstein und **erste ohne Linie des Veranstalters**: Eine GPX-Datei gibt es nicht (die Seite
verweist auf eine Aufzeichnung bei AllTrails, Download nur mit Konto, nicht genutzt; Run the Alps, Datasport, finishers.com haben keine).
Die Linie ist aus dem **Streckenplan des Veranstalters** (Programm 2027) und den **Wegen von OpenStreetMap** nachgezeichnet (`plan.py`,
`route_osm.py`), in Vaduz und Malbun ergänzt nach Postenliste, Lageplänen und einem Laufbericht. Punkt-zu-Punkt von Bendern im Rheintal
(441 m) nach Malbun (1611 m), höchster Punkt Sassförkle (1785 m); Höhenbereich **1346 m**. Höhen aus **swissALTI3D 0,5 m** (deckt
Liechtenstein mit ab, Kacheln Jahrgang 2026), Brücken aus **swissSURFACE3D** (Jahrgang 2024), über `work/swissalti.py` (Kopie von
`../zuerich/work/swissalti.py`, nur Kopfkommentar und Zwischenspeicher hier). Das Pace-Modell ist am Berg zu optimistisch (siehe
„Modellzeit“); den Hinweis zeigt der Kern seit 2.6 selbst (hier 8,9 km über 10 %), die Texte sagen nur „Bergmarathon mit Gehpassagen“.
Straßen- und Ortsnamen in Schweizer bzw. Liechtensteiner Schreibweise („Schaaner Strasse“ wie in OSM).

## Termin und Start

Offizieller Name **LGT Alpin Marathon** (Seite „LGT Alpin Marathon“ auf lgt-alpin-marathon.li, Programm 2027, Reglement; Logo „LGT Alpin
Marathon Liechtenstein“; Titelsponsor LGT, Veranstalter LGT Alpin-Marathon-Verein; Datasport schreibt „LGT Alpin-Marathon Bendern-Malbun“
als Wettbewerb). Der **25.** war am **Samstag, 13. Juni 2026** (Datasport „25. LGT Alpin Marathon 2026“, 13.06.2026). Der **26.** ist am
**Samstag, 12. Juni 2027, 9:00 Uhr** – fest, nicht nur geschätzt: Seite „LGT Alpin Marathon“ („Herzlich willkommen zum 26. LGT Alpin Marathon
im Fürstentum Liechtenstein am 12. Juni 2027 … Start: 9.00 Uhr, 12. Juni 2027“), Programm 2027 (`Programm_26_LGT_Alpine_Marathon_2027_GzD.pdf`,
„Samstag, 12. Juni 2027 · 42,195 km · 1870 m HD“), Countdown der Startseite (`main.js`: `new Date("2027-06-12T09:00:00")`), Datasport
„26. LGT Alpin Marathon 2027“ mit Startliste 12.06.2027. `D.termine` `["2026-06-13", "2027-06-12"]`, `D.tz` Europe/Vaduz (der Kern nennt
dann „Ortszeit Vaduz“, kein `D.ort` nötig), `D.start` = 540 (9:00). Kein `D.lage`, `D.mauer`, `D.tor`, `D.zielschluss`. Seiten des
Veranstalters in `dl/seiten/` (lokal; die Seite lädt ihre Unterseiten per Skript nach, `seite.py <name> https://www.lgt-alpin-marathon.li/<name>`
holt sie direkt), Downloads in `dl/dateien/` (`f_<FileID>`: 12659 Programm 2027, 12554 Postenliste, 12440 Reglement 2018, 12328 Streckenplan
2023, 9019 Höhenprofil, 9244 Marschtabelle, 9137/9141 Lagepläne Steg/Malbun, 12316 Startbereich).

**Start** (`D.wellen`, ohne Knöpfe, nur Text): 9:00 Uhr bei der LGT Bank, Schaanerstrasse 19, Bendern, gemeinsam für Marathon, LGT
Halbmarathon PLUS (Ziel in Steg, „km 25“) und LGT Staffel 25 + 17 (Wechsel in Steg). Seit 2022 dort („NEU“; die alte Marschtabelle nennt
noch „Bendern Ospelt Anstalt“, rund 600 m weiter südlich).

**Zeitlimits** (im Text unter „Deine Startzeit“, kein `D.tor`): Programm 2027 und Seite „Durchgangszeiten“: **Vaduz (km 10) 10:15 Uhr,
Steg (km 25) 13:00 Uhr, Zielschluss Malbun 16:00 Uhr**. Das Reglement (Seite und PDF 2018) nennt abweichend „Kontrollschluss in Vaduz ist
10:10 Uhr, in Steg 13:00 Uhr“ und die Messpunkte Vaduz km 10,3 und Steg km 25,4. Wer später durchkommt, wird aus dem Rennen genommen
bzw. läuft mit markierter Startnummer auf eigene Verantwortung weiter. Pacemaker 4:30, 5:00, 6:00 h. Stöcke verboten.

**Staffel:** Ja, LGT Staffel 25 + 17 (zwei Läufer über die Marathonstrecke) → eine `relay`-Marke „Wechsel“ bei km 25,5, wo die Linie in
Steg die Malbunstrasse quert (Lageplan Steg: Ziel Halbmarathon PLUS an der Strasse, Wechselzone gleich nördlich; Laufbericht 2023: „bei der
Kapelle Steg (km 26) trennen sich die Strecken … Marathonläufer überqueren die Hauptstraße“). Der Staffel-Schalter erscheint damit.
**Halbmarathon-Marke** bei 21 098 m (auf dem Wissfläckaweg kurz vor der Silumer Kulm).

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Reihenfolge: `plan.py`, `osm.py`, `route_osm.py` (mit `via.json`), `strassen.py`, `bedeckt.py`, `dgm.py` (mit `swissalti.py`), `deck.py`,
`clean.py`, `namen3d.py`, `orte.py`, `build.py`, `route.py`, `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py liechtenstein` (der Ordner
`../liechtenstein/` muss es geben), `liechtenstein/work/app.py` (beim ersten Mal über `kern.py --neu liechtenstein work/felder.json`, danach
ersetzt es nur die Felder und lässt Kartenbilder und `D.tiles` stehen), `tiles_rand.py liechtenstein 2`. Nur Abgleich: `vergleich.py`,
`kmcheck.py`, `planbild.py`; zum Nachsehen `wege.py <von> <bis> [m]`, `seite.py`. Prüfen: `pruefen.js`, `pruefen2.js`, `pruefen3.js`
(Server auf Port 8793 im Repo-Wurzelordner, `NODE_PATH=/opt/node-tools/node_modules node pruefen.js`).

1. **Plan** (`plan.py`): Programm 2027, Seite 1, bei 500 dpi gerastert (`pdftoppm`), die violette Linie (RGB 114/34/131) ausgelesen,
   Beschriftungskästen weg. Lage auf LV95 über eine affine Abbildung aus sechs Passpunkten (Bahnhofssymbole Haag-Gams, Nendeln, Schaan-Vaduz,
   Buchs SG, Sevelen, Schlosssymbol Vaduz; Koordinaten geo.admin.ch), Reste bis 140 m.
2. `osm.py`: OSM über die API in 275 Rechtecken zu 0,005° höchstens 450 m neben der Plan-Linie, eine Abfrage je Sekunde, bei 509 gewartet
   (kam oft: drei Agenten teilten sich die Adresse; Dauer rund 75 min) → `../dl/osm_netz.json` (5865 Wege, mit Routen-Relationen). Overpass
   und Geofabrik waren aus dieser Umgebung nicht erreichbar (Verbindung abgebrochen).
3. **Linie** (`route_osm.py`): Plan-Linie im Bild geordnet (Anker in Laufrichtung: Start, Nordspitze der Schleife in Vaduz, Steg, Nordende
   Valorsch, Turna, zwei Punkte am Pfeil auf der Südwestseite von Malbun, Westspitze, Ziel), dann die affine Lage iterativ an das OSM-Wegnetz
   angepasst (Median Plan–Weg danach 12 m). Route auf dem Wegnetz: kürzester Weg mit Kosten Länge × (1 + ((Abstand zur Plan-Linie − 15 m) /
   35 m)²), ein schon gelaufenes Stück kostet das Vierfache. **Feste Zwischenpunkte** (`via.json`, je mit Begründung): Vaduz Äulestrasse,
   Marktplatzgarage (Posten 2), Städtle, Beckagässli, Rotes Haus, Park-Hotel Sonnenhof, Letziweg (Laufbericht 2023 von marathon4you.de: „Auf
   der Lettstraße … Verpflegung im Obergeschoss der Marktplatzgarage. Über die Hauptstraße ins Städtle, dann rechts ins Beckagässli … Mitteldorf
   zum Roten Haus, dann bis zum Parkhotel Sonnenhof (km 11). Auf dem Letziweg durch den Schlosswald … zum Schloss“); Malbun Kehrplatz unter dem
   Turna-Stall (Posten 13) und der Weg zurück auf der Südwestseite (wie im Plan). Zwischen zwei festen Punkten zählt nur die Länge. Ergebnis:
   3249 Punkte, **42 938 m**; der Plan selbst zeigt in Vaduz dieselbe Schleife zur Marktplatzgarage (`planbild.py`, Bild
   `work/shots/plan_vergleich_vaduz.png`). Gegenprobe Wegarten: auf den OSM-Wegen 9,1 km Pfade, laut Programm 9,2 km „Bergweg“ (22 %);
   Asphalt/Naturstrasse lassen sich aus OSM nicht sauber trennen (OSM 12,4/21,8 km, Programm 15,2/17,8 km).
4. **Kilometer** (`common.py`): Eine vermessene Linie oder Kilometermarken gibt es nicht; die Linie ist 1,8 % länger als 42,195 km und wird
   **gleichmäßig gestaucht**. Abgleich (`kmcheck.py`, Ort → km hier): Marktplatzgarage 10,07 (Postenliste 10), Park-Hotel Sonnenhof 11,4
   (Laufbericht 11), Schloss 12,6 (12 bzw. Posten 3 12,5), Rotenboden 15,4 (15), Masescha 17,6 (17,5), Silum 20,9 (20), Sücka 22,8
   (Marschtabelle 24), Gänglesee 24,65 (Laufbericht 25), Rietle 30,6 (31), Güschglehötta 32,3 (33), Sassförkle 34,4 (Laufbericht „kurz vor 34“,
   Posten 11 35), Friedenskapelle Malbun 36,95 (Laufbericht 37, Posten 12 37), Kehrplatz Turna 38,8 (38,5). Die Kilometer der Postenliste sind
   runde Werte (5, 10, 12,5 …). Die Kilometerkästen im Plan liegen dagegen bis 1,4 km daneben (Plan „30 km“ hier 31,5, „35 km“ hier 36,2); die
   sind nur ungefähr gesetzt. „Kilometerschild acht am Rheinpark-Stadion“ (Laufbericht) liegt hier bei 8,9.
5. `strassen.py`: Name und Art je 10 m vom OSM-Weg der Linie; Gehwege ohne Namen tragen den Namen der Straße höchstens 20 m daneben.
   `bedeckt.py`: keine Tunnel (die Strecke geht am alten Kulmtunnel vorbei, nicht hindurch).
6. `swissalti.py`, `dgm.py`: **swissALTI3D 0,5 m**, alle 10 Linienmeter bilinear (4295 Punkte), dazu 2 m zum Vergleich. 36 Kacheln, alle
   Jahrgang 2026. Höhen in m ü. M. (LN02).
7. **Brücken** (`deck.py`, `clean.py`, Verfahren wie Zermatt, ohne GPX-Höhen): fünf gemessen aus swissSURFACE3D (km 0,85 Binnenkanal bei
   Bendern, 9,2 Lettstrasse in Vaduz, 21,3 Wissfläckaweg, 24,9 Steg, 36,9 Malbun), zwei geschätzt unter Bäumen (km 25,45 Kleinsteg, km 32,7
   Bergweg nach der Güschglehötta; `D.bridges`, schraffiert). Am Ergebnis ändern sie fast nichts (Rohmodell 1900/732 statt 1899/732).
8. **Orte** (`namen3d.py`, `orte.py`): Gemeinden aus swissBOUNDARIES3D (Gamprin, Eschen, Schaan, Vaduz, Triesenberg, Balzers u. a.,
   `../dl/orte/gem_*.json`), Orte aus swissNAMES3D (51 Kacheln), nur eine Auswahl bekannter Namen (swissNAMES3D hat hier fast nur Flurnamen).
   **Exklaven:** Valorsch, Güschgle und Sass sind Alpen von Schaan, Vaduz und Balzers, Täli und Pradamee in Malbun gehören zu Vaduz; dort steht
   statt der Gemeinde „Valorsch“ bzw. „Malbun“ (sonst stünde „Balzers“ mitten in den Bergen). Folge: Gamprin, Bendern – Gamprin – Eschen –
   Schaan – Vaduz (Rheinpark-Stadion, Städtle, Schloss) – Triesenberg (Frommenhaus, Rotenboden, Fari, Masescha, Silum, Kulm, Sücka, Steg) –
   Valorsch (Vordervalorsch, Rietle, Güschgle, Sassförkle) – Malbun (Täli, Pradamee).
9. `build.py`: Wege ohne Namen nach Art wie Zermatt („Fahrweg“, „Wanderweg“, „Bergweg“ mit `sac_scale` ab mountain_hiking, „Fussweg“,
   „Nebenstrasse“); die ersten 90 m (Zufahrt der Bank) heißen „Schaaner Strasse“. Nicht von Hand benannt: der Weg vom Sassförkle nach
   Malbun heißt im Laufbericht „Forscherweg“, die Wege um Malbun in der Marschtabelle „Panoramaweg“ – beides nicht in OSM, in der App
   „Wanderweg“, im Text erwähnt. **Verpflegung** nach der Postenliste (13 Posten; Programm: „8 Verpflegungsposten und 5 Wasserstellen“) am
   genannten Ort (Lage aus OSM bzw. swissNAMES3D), Posten 1 „Sportplatz Schaan“ an der Listen-km 5,0 (im Plan „5 km“ am Damm). Essen (Brot,
   Bananen, Orangen, Riegel, Gels) → „Verpflegung“ (Posten 4, 6, 8, 9, 11); Wasserposten der Liste → „Wasser“ (3, 5, 7, 10, 12; Posten 12 mit
   Bouillon); übrige nur Getränke → „Getränke“ (1, 2, 13). Höhen in cm im 10-m-Raster, Median über 30 m. `route.py` (lat0/lon0 47,1/9,5),
   `tiles.py` (z12–z15), `tiles_z11.py liechtenstein`, `app.py`, `tiles_rand.py liechtenstein 2`: 30 Kartenstücke, 2,8 MB.

   **Abgleich** (`vergleich.py`, Verfahren wie die App):

   | Quelle | Start | Ziel | min (km) | max (km) | ↑/↓ 200 m | ↑/↓ 100 m | ↑/↓ 50 m | ↑/↓ 1 km | ↑/↓ Punkt für Punkt |
   |---|---|---|---|---|---|---|---|---|---|
   | App (swissALTI3D 0,5 m, Brücken aus swissSURFACE3D) | 440,8 | 1610,5 | 439,6 (0,69) | 1785,3 (34,44) | 1899/732 | 1964/795 | 2003/833 | 1648/484 | 2129/959 |
   | swissALTI3D 0,5 m ohne Bereinigung | 440,8 | 1610,5 | 437,9 (0,85) | 1785,3 (34,44) | 1900/732 | 1965/796 | 2004/835 | 1648/484 | 2142/971 |
   | swissALTI3D 2 m, gleiche Brücken | 440,8 | 1610,4 | 439,6 (0,72) | 1785,3 (34,44) | 1899/732 | 1964/795 | 2002/833 | 1648/484 | 2135/964 |

   Wie GPS-Uhren (Anstieg ab 0,5 / 1 / 3 / 5 m): ↑ 2020 / 1993 / 1947 / 1892 m.

## Höhenmeter: 1870?

Der Veranstalter nennt „Steigung 1870 Meter, Gefälle 720 Meter“ (Höhenprofil, Programm 2027: „1870 m HD“, „Höhenunterschied Bendern /
Malbun: 1870 Meter (Gefälle 720 Meter)“). Das Laser-Modell ergibt mit dem 200-m-Messfenster der App **1900 / 732 m**, also auf 30 bzw. 12 m
dasselbe; mit 100 m 1964, mit 50 m 2003, Punkt für Punkt 2129. Bestätigte Höhen: Silumer Kulm 1540 m (Plan „1539“), Sassförkle 1785 m
(Laufbericht und OSM 1785), Masescha 1229 m (Haltestelle 1234), Schloss 580 m (Laufbericht 570). Das Reglement schreibt „Höhenlagen zwischen
450 m und 1800 m“.

## Ergebnis

↑ 1900 m / ↓ 732 m mit 200-m-Fenster, Rohdaten ↑ 2129 m. Start 440,8 m an der Schaanerstrasse in Bendern, tiefster Punkt 439,6 m bei km 0,7,
Ziel 1610,9 m in Malbun, höchster Punkt 1785,3 m am Sassförkle (km 34,4); **Höhenbereich 1346 m**. Steigung über 200 m: **8,92 km steiler als
+10 %, 2,69 km steiler als +15 %**, 0,30 km steiler als +20 % (bergab 2,51 km steiler als −10 %, 0,24 km steiler als −15 %). Steilste Stelle
**+22,0 % bei km 32,9** (Bergweg Güschglehötta–Sassförkle; +26,9 % über 50 m bei km 32,6), steilste bergab −17,7 % bei km 21,9 (Abstieg von
der Silumer Kulm zur Sücka). Verlauf: 10 km flach auf Binnendamm und Rheindamm (441 → 455 m), in Vaduz durch Städtle und Mitteldorf zum
Park-Hotel Sonnenhof und auf dem Letziweg zum Schloss (580 m, km 12,6), in Kehren nach Triesenberg (Rotenboden 956 m, km 15,4; Masescha
1229 m, km 17,6), auf dem Philosophenweg nach Silum (1477 m, km 20,9) und auf die Silumer Kulm (1540 m, km 21,5): von 455 auf 1540 m zwischen
km 10 und 21,5. Hinunter über Sücka nach Steg (1312 m, km 24,65), durch Saminatal und Valorsch sanft hinauf (1409 m, km 30,8), ab der Güschglehötta
(1482 m, km 32,3) 300 m auf 2,1 km zum Sassförkle, hinunter nach Malbun (1622 m, km 37,0), um Malbun über den Turna-Stall (1729 m, km 38,8)
und die Pradamee ins Ziel.

| Abschnitt (Messpunkte Datasport) | km | Höhe | ↑ / ↓ (200 m) | steilste 200 m |
|---|---|---|---|---|
| Start – Vaduz (Marktplatzgarage) | 0–10,07 | 441 → 455 | 30 / 15 | +3,4 % |
| Vaduz – Steg (Wechsel) | 10,07–25,48 | 455 → 1317 | 1130 / 268 | +19,2 % |
| Steg – Ziel | 25,48–42,195 | 1317 → 1611 | 740 / 448 | +22,0 % |

**Modellzeit (nur für die Hauptsitzung, nicht in den Texten):** Mit 4:00/km im Flachen ergibt das Modell 3:25:32 (das Profil kostet 36:45 min);
bei 2:50:00 kostet es 30:24 min, bei 4:00:00 42:55 min (gemessen mit `pruefen.js`). 2026 lief der Sieger 3:06:17, die Siegerin 3:57:54, der
Median der 287 Finisher 5:23:43 (Viertel 4:53:56 und 5:51:29, letzte 7:15:44). Die Zwischenzeiten zeigen, wo das Modell danebenliegt:
Median-Anteile Start–Vaduz 17,4 %, Vaduz–Steg 38,9 %, Steg–Ziel 43,6 %; das Modell verteilt (Messpunkte km 10,3 und 25,4 laut Reglement)
20,3 / 40,4 / 39,4 % bei jeder Zielzeit. Im Flachen sind die Läufer also schneller, am Berg nach Steg langsamer, als das Modell sagt
(Median Vaduz 0:56, Steg 3:03; Modell bei 5:23:43 1:06 und 3:16).

Geprüft mit Playwright (Chromium, 393 × 852, Faktor 2, Server auf Port 8793, `pruefen.js`, `pruefen2.js`, `pruefen3.js`): keine
Konsolenfehler, `APP_VERSION` 2.6 und Knopf v2.6, Service Worker installiert (36 Einträge im Cache `lgt-marathon-profil`), Tipp auf die
Version meldet „Version 2.6 ist aktuell“; Tabellen bei 320/375/393/430 px ohne Überbreite, Seite nicht breiter als das Fenster. Berg-Hinweis
des Kerns erscheint („Bergstrecke: 8,9 km mit mehr als 10 % Steigung …“). Laufansicht am Start, km 5, 10,1 (Marktplatzgarage), 11,3, 12,6
(Schloss), 15,4, 17,6, 21,5 (Silumer Kulm), 21,9, 25,5 (Wechsel), 30,8, 32,9 (steilste), 34,4 (Sassförkle), 37,0, 38,8, 40,8, 42,1 und die
Kartenübersicht mit Verpflegung bei km 30; Zuschauer-Tabelle mit „Ortszeit Vaduz“, Sa., 12. Juni 2027 und dem Text zu Start und Zeitlimits;
„Woher die Zahlen kommen“. Bilder in `work/shots/`, dazu `plan_vergleich*.png` (Linie über dem Plan des Veranstalters). `kern.py` meldet alle
Apps „gleich“, dazu „karten.json veraltet“ (neue Strecke; Hauptsitzung mit `--schreiben`).

## Zwischenzeiten (Datasport, nur geprüft, nichts gespeichert)

Die Rangliste 2026 (`results.datasport.com/de/anlass/lgt-alpin-marathon-2026/ranking`, Listen „Marathon Frauen“ und „Marathon Männer“) hat
je Läufer drei **Etappenzeiten**: „Start-Vaduz“, „Vaduz-Steg“, „Steg-Ziel“ (Summe = Endzeit), sortierbar nach „@ Vaduz“, „@ Steg“, „@ Ziel“.
Messpunkte also Vaduz (Reglement km 10,3, hier Marktplatzgarage km 10,07) und Steg (Reglement km 25,4, hier Wechsel km 25,48). 286 der 287
Finisher haben alle drei Werte. Gezählt in `/tmp` ohne Namen, danach gelöscht.

## Offen

- Prüfung am iPhone.
- **Linie nachgezeichnet:** Wo Plan und OSM mehrere Wege zulassen, kann die Linie um einzelne Gassen danebenliegen (Vaduz Zentrum, Kehren in
  Triesenberg, Silum, die Westspitze in Malbun). Die Höhenmeter treffen den Veranstalter trotzdem auf 2 %. Sobald der Veranstalter eine GPX-Datei
  veröffentlicht (oder der Nutzer die AllTrails-Aufzeichnung selbst lädt), `route_osm.py` durch ein `parse.py` wie in Zermatt ersetzen.
- **Kilometer:** gleichmäßig gestaucht (Faktor 0,983); einzelne Orte bis etwa 0,7 km neben den runden Kilometern der Postenliste.
- **Zeitlimit Vaduz:** Programm 2027 und Seite „Durchgangszeiten“ 10:15 Uhr, Reglement 10:10 Uhr; im Text stehen beide.
- **Posten 11 „Saas Fürkle“:** am Sattel gesetzt (Laufbericht: Verpflegung am Sassförkle); im Plan steht das Becher-Symbol mit „35 km“ etwas
  tiefer Richtung Malbun.
- **Startseite:** Karte fehlt. Eyebrow „LGT Alpin Marathon“, Stadt **„Liechtenstein“** (die Strecke quert das Land von Bendern über Schaan,
  Vaduz und Triesenberg nach Malbun, kein einzelner Ort trifft es; Logo „LGT Alpin Marathon Liechtenstein“, Facebook „LiechtensteinMarathon“;
  „Malbun“ und „Vaduz“ über `data-such`), „Kurs 2026“ (Plan seit 2023 unverändert, im Programm 2027 derselbe), `data-termine="2026-06-13
  2027-06-12"`, `data-monat="6"`, Termintext „Sa., 12. Juni 2027“, `data-land="Liechtenstein"`, ↑ 1900 m / ↓ 732 m, Höhe 440–1785 m,
  `data-such` z. B. „Liechtenstein LGT Alpin Bendern Gamprin Schaan Vaduz Triesenberg Malbun Steg Silum Masescha Valorsch Sassförkle Rheintal
  Fürstentum FL Bergmarathon Berglauf Trail Staffel“. Mini-Profil: 1346 m Höhenbereich (Bergmaßstab 7 px je 40 m: rund 236 px). README-Tabelle
  und Liste der Präfixe (`lgt-`). Fuß der Startseite: Höhen „swissALTI3D und swissSURFACE3D © swisstopo“ (wie Zürich, Luzern, Jungfrau, Zermatt).
  **Teilnehmer 2026: 287 im Ziel** des Marathons (Datasport-Rangliste, gezählt: 56 Frauen und 231 Männer mit Rang und Zeit, Ränge lückenlos;
  Übersicht „Im Ziel“ ebenso 56 + 231). Angemeldet 315, gestartet 292. Wer für den Marathon gemeldet nur bis Steg läuft, kommt laut
  Veranstalter in die Halbmarathon-Wertung. Halbmarathon PLUS 2026: 251 im Ziel (69 + 182); Staffeln laut Übersicht 31 Mixed, 12 Frauen, 21 Herren (dort nur eine Zahl je Kategorie).
- Gegenprobe mit dem privaten Eichdatensatz (`course_segments`) nicht gemacht: Die Datei lag in dieser Sitzung nicht vor.
