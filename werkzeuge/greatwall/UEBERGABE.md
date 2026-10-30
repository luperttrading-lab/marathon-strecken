# Übergabe: Steigungsprofil Great Wall Marathon

Stand 30.10.2026, App-Version **1.15** (1.15: Zielkarte beim Zieleinlauf „42,2 km“ statt „42,195 km“; 1.14: im Ziel wieder 42,2 statt 42,195 (Anzeige, Gesamtstrecke, Zwischenzeiten, Pace-Band); 1.13: Offline-Hinweis orange und stehend, bis man ihn antippt; 1.12: Offline-Laden aller Strecken aus 1.78 zurückgenommen (Nutzer: erstmal nur die Meldung), dafür Meldung „Offline: gespeicherte Fassung, vielleicht nicht die neueste“; 1.11: alle Strecken offline: Seiten beim Öffnen der Startseite, Kartenbilder beim Öffnen der Strecke oder per Knopf; 1.10: offline nur noch aus dem eigenen Speicher, Rückfallseite bei jedem Besuch erneuert (Service Worker); 1.9: im Ziel 42,195 statt 42,2 in Anzeige, Gesamtstrecke, Zwischenzeiten und Pace-Band; 1.8: Maßstab auf der Karte ohne Kasten, kleiner, in der freieren linken Ecke; 1.7: im Vollbild der Ort groß oben rechts statt am Pfeil, Maßstab auf der Karte; 1.6: Kopf mit „Great Wall“ groß und „Streckenplan und Steigungsprofil“, Umschalter Karte | Zahlen statt Pünktchen, Karte zuerst, Name der Strecke im Vollbild; 1.5: zu breite Tabellen werden stufenweise enger statt rechts abgeschnitten, Zwischenzeiten mit „+268 s“ passen jetzt; 1.4: Profil beginnt 24 px tiefer, die Mauer-Beschriftung steht in der freien Zeile darüber mittig über ihrer Mauer; 1.3: Mauer-Beschriftung im Profil neben dem Gipfel statt darauf, im 10-km-Ausschnitt 1. Mal danach, 2. Mal davor; 1.2: Erklärung der Mauerzeiten berichtigt: dieselbe Mauer in Gegenrichtung, beim 1. Mal überwiegend bergab, beim 2. Mal überwiegend bergauf; der Stau beim 1. Mal erklärt die gleichen Zeiten, nicht die Länge; 1.1: je Mauerdurchgang ein Rad mit Empfehlung nach Zielzeit, Erklärung der Unterschiede, Voreinstellung 5:00:00; 1.0: erste Fassung).
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/greatwall/.

Die App ist eine Kopie der Tokio-App (aktueller gemeinsamer Code, Tokio 1.26 mit Mauer- und Tor-Logik) mit eigenen Daten, Texten und
Speicherschlüsseln (`gwm-…`, Service-Worker-Cache `gwm-marathon-profil`, löscht nur Caches mit Präfix `gwm-`), ohne eigenes Manifest
und Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md).
Gegenüber `tokio/index.html` unterscheiden sich nur die streckenspezifischen Zeilen (wie bei Rom und Barcelona) und die Kartenzeile
unter der Karte („© OpenStreetMap-Mitwirkende · Relief Copernicus DEM“). **`work/app.py` liest bei jedem Lauf `tokio/index.html` und
`tokio/sw.js` frisch**: Nach Änderungen am gemeinsamen Code genügt `cd werkzeuge/greatwall/work && python3 app.py` (gleiches Ergebnis
bei gleichem Stand, geprüft). Startseite und README sind noch nicht angepasst.

**Diese Strecke ist anders als alle anderen:** zweimal über die Große Mauer (5164 Stufen, beide Durchgänge zusammen), Dorf- und Feldwege,
die OpenStreetMap kaum kennt, kein Laser-Höhenmodell, keine GPX-Datei. Es geht hier vor allem um die Strecke; das Höhenprofil ist
**grob**, das sagen Untertitel, „Woher die Zahlen kommen“ und der Hinweis darunter.

## Termin und Start

Great Wall Marathon (Albatros Adventure Marathons, Kopenhagen; in Deutschland über interAir) in Huangyaguan, Bezirk Jizhou, Tianjin, am
**Samstag, 15. Mai 2027**: Seite „The race“ des Veranstalters („Future race dates are: 2027: May 15th, 2028: May 20th“,
https://great-wall-marathon.com/the-race, `../dl/race.html`) und Countdown der Startseite (`2027-05-15T01:30:00+0200` = 7:30 Uhr Pekinger
Zeit, `../dl/home.html`). 2026 war es der 16.05.2026. `D.termine` `["2027-05-15"]`, `D.tz` Asia/Shanghai, `D.ort` „Huangyaguan“ (die
Zeitzone allein hieße „Shanghai“), `D.ortKurz` „ Peking“ (Pekinger Zeit, so nennt man die chinesische Einheitszeit), `D.start` = 450.
Start und Ziel aller Strecken auf dem Yin-&-Yang-Platz (八卦关城) in der Festung Huangyaguan.

**Startwellen** (`D.wellen`): Runners Guide 2026 (`../dl/guide.pdf`, Seite 18–19): Welle 1 7:30 (rosa), Welle 2 7:40 (gelb), Welle 3
7:50 (blau), jeweils Marathon und Halbmarathon gemischt, Welle 1 mit den schnelleren, Welle 3 mit den langsameren oder ohne gemeldeten
Zeiten; Fun Run (Welle 4, grün) 8:00. Wechsel nur in eine spätere Welle. Die Startschüsse fielen 2026 laut Zeitnahme um 7:32:09,
7:40:06 und 7:49:38 (Teilnehmerdaten des Zeitnehmers, siehe Daten 12). Der Runners Guide 2027 erscheint erst mit den Startunterlagen.

**Tor und Zielschluss:** Runners Guide 2026: „At 13:50 (6 hours after the last runner in wave 3 has crossed the start line), the gate
leading to the wall will be closed. Marathon runners, who have not reached 35 km (21.75 mi) at 13:50, will not be allowed to finish“;
„At 15:50 (8 hours after …) the Great Wall Marathon ends.“ → `D.tor` = `{"m": 35000, "uhr": 830, "name": "Tor zur Mauer"}`,
`D.zielschluss` = 950. Die Seite „The race“ nennt allgemeiner 14:00 („the gate leading to the wall will be closed (KM 35)“) und
16:00; die Zeiten des Guides hängen am Start der Welle 3 und gelten, solange der Plan gleich bleibt.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Reihenfolge: `osm.py`, `plan.py`, `georef.py`, `linie.py`, `dgm.py`, `planprofil.py`, `marken.py`, `form.py`, (`common.py`),
`vergleich.py`, `build.py`, `splits.py`, `mauer.py`, `route.py`, `tiles.py relief`, `app.py`. `tiles_z11.py` und `tiles_rand.py` **nicht**
laufen lassen: Sie holen OSM-Kacheln und überschrieben das Relief; `tiles.py` baut alle Stufen z11–z15 mit denselben Flächen.

1. **Quellen des Veranstalters** (`../dl/`): Streckenkarte „Great Wall Marathon Route map“ (`route.pdf`, Illustrator, 08.05.2026,
   https://great-wall-marathon.com/sites/default/files/2026-05/Great%20Wall%20Marathon%20Route%20map.pdf), Höhenkurven
   (`hoehe.pdf`, „GWM Elevation curves_all_2026“), Runners Guide 2026 (`guide.pdf`, Text `guide.txt`), Seiten `home.html`,
   `race.html`, `partner.html`. Eine GPX-Datei, eine Google-Karte oder eine Strava-Route bietet der Veranstalter nicht an.
2. `plan.py`: Die Karte ist eine **Vektorgrafik mit Ebenen** auf einem Satellitenbild: „Rute“ (der Marathon als *eine* durchgehende
   schwarze Linie in Laufrichtung, 801 Punkte; Hin- und Rückweg nebeneinander gezeichnet), Halbmarathon und Fun Run gestrichelt
   darüber, „Roads“ (Main Roads, Tarmac streets, Feldwege), „Rivers“, „KM skilte“ (Kilometerschilder mit Linie zur Strecke),
   „Water stations“ (Symbole mit Linie zur Strecke; Inhalt aus den Symbolen gelesen), „First Aid“. Die zwei Ausschnitte (Platz, Mauer)
   sind Rasterbilder. → `plan2026.json`.
3. `osm.py`: OSM über die API (`api.openstreetmap.org/api/0.6/map`) in 143 Rechtecken zu 0,02°, 40,10–40,32° N, 117,33–117,59° O
   (Overpass war nicht erreichbar) → `../dl/osm_all.json` (993 Wege). Die Mauer ist gut eingetragen (historic=citywalls, Türme als
   man_made=tower, Treppen, Mauerbrücke 90229118, Festungsmauer 90229198), Straßen nur die großen und einige Dorfstraßen.
4. `georef.py`: **Einpassung** der Karte auf OSM (WGS 84). Chinesische Kartendienste verschieben um gut 500 m (GCJ-02); woher das
   Satellitenbild der Karte stammt, ist offen. Eine affine Abbildung schluckt die fast gleichförmige Verschiebung samt Maßstab und
   Drehung (die GCJ-02-Verschiebung ändert sich über die 10 km der Karte um weniger als 1 m), deshalb nur gegen OSM eingepasst:
   Startwert aus neun Dorfnamen (Namen stehen neben den Dörfern, Median 465 m daneben), dann ICP mit den gezeichneten Straßen
   (5697 Punkte) gegen OSM-Straßen und Flüsse (halbes Gewicht, das Flussbett ist breit), Huber-Gewichte, Fangradius 400 → 60 m.
   Ergebnis: 9,147 / 9,103 m je pt, um 0,78° gedreht, Achsen 89,83° (`georef.json`). **Restfehler: gezeichnete Straßen gegen OSM im
   Median 9 m** (Norden 11, Mitte 9, Süden 8 m; 75 % unter 24 m; die übrigen sind Straßen, die OSM nicht kennt). Die Mauer ist nicht
   eingepasst: Die Karte zeichnet die Strecke dort schematisch neben das Mauersymbol, 30–100 m von der OSM-Mauer (Median 55 m).
5. `linie.py`: **Linie**, Stück für Stück nach dem Aufbau der Strecke (Karte, Ausschnitte, Guide): Platz → Straße über Xiaoping'an und
   Huayuan zum Fuß der Treppe am Wall point 1 → Mauer nach Westen (Tower 1, Beacon Tower, Tower 2–4, hinab zum Wall point 2, weiter auf
   der Mauer, „Goat Track“ = OSM-Treppe 90229166 hinab zu Tower 5) → Mauerbrücke (Wasserpass über den Ju He) → Tower 6 → einmal auf der
   Festungsmauer rund um den Platz (Tower 7, Tempel 3, Tempel 4) → Nordmauer bis Tempel 1 (das Tor) → über den Platz zur Talstraße
   G233 → Tal hinab und Schleife im Süden → Tal hinauf → über den Platz zum Tor (km 35) → Nordmauer, Mauerbrücke, Mauer in Gegenrichtung
   bis zum Wall point 1 → derselbe Weg zurück → Ziel. Die Höhenkurve des Veranstalters bestätigt den Aufbau: km 0–5,1 und 37,1–42,2 sind
   spiegelgleich, Getränkestellen 1–7 liegen auf dem Rückweg in umgekehrter Folge. Jedes Stück wird einmal gebaut und für den Rückweg
   umgedreht. Straßen: Korridor-Suche entlang der eingepassten Linie (Abschnitte zu 200 m, Dijkstra im Netz aus OSM-Wegen mit Kosten
   Länge · (1 + (d/45 m)²), der gezeichneten Linie mit Länge · 2,5 und Übergängen bis 30 m mit Länge · 2 + 150 m; teuer, sonst springt
   der Weg an der engsten Stelle über Haarnadelkurven, wie es die Karte zeichnet). Mauer: nur OSM-Mauer und -Treppen. Platz: Wege aus
   dem Ausschnitt der Karte, affin auf die vier Festungsecken in OSM (Restfehler bis 15 m). Von Hand (`EXTRA`): Am Talausgang bei
   Duanzhuang ist Hin- und Rückweg ohne OSM-Weg 30–50 m nebeneinander gezeichnet; dort gilt ihre Mitte. → `linie.json` (UTM 50N und
   WGS 84, je Punkt Art, OSM-Weg und Teilstück), **42,97 km**. Davon OSM-Straßen 23,6 km (G233 7,4, X590 5,9 …), Mauer und Treppen
   5,1 km (beide Durchgänge, mit Festungsmauer), **gezeichnete Linie der Karte 12,1 km** (Feld- und Dorfwege um Zhongying, Xiaying,
   Dongjiafen, Beichedaoyu und Da Ping'an, die Schleife bei km 21–22), Mitte am Talausgang 0,8 km, Übergänge 0,7 km, Platz 0,55 km.
   Plausibilität: keine Wenden über 150° auf 10–20 m, keine Stichwege; die gezeichnete Linie selbst ist 42,45 km lang und passt
   zwischen den Bezugspunkten auf wenige Prozent zu den Kilometern des Veranstalters (er hat maßstäblich gezeichnet).
6. `marken.py`, `form.py`, `common.py`: **Kilometer.** Bezugspunkte: Kilometerschilder der Karte (4, 10, 15, 21, 32, 38; die Linie des
   Schilds zeigt auf die Strecke), Tor zur Mauer = 35 000 m (fester Knoten), die 21 Getränkestellen mit ihren Kilometern aus der
   Höhenkurve (Lage aus der Karte; auf der Mauer 30–150 m Abstand, dort halbes Gewicht) und die **Form der Höhenkurve** (`form.py`:
   Dynamic Time Warping zwischen SRTM entlang der Linie und der Kurve des Veranstalters, Zuordnung nur an Hängen ab 3 %, alle 500 m,
   27 Punkte). Stückweise linear, Knoten alle 3 km, Huber. Restabweichung: Schilder ±43 m (Median 34 m), Formpunkte Median 16 m
   (max. 108 m), Getränkestellen Median 53 m (max. 162 m, zweiter Mauerdurchgang). **Kilometer auf etwa ±0,1 km, auf der Mauer
   ±0,15 km.** Nicht verwendet: Schild „27 KM“ und Getränkestelle 13 („26,9“): Beide stehen in der Karte dicht beieinander, nach Linie,
   Getränkestellen 12 und 14 und dem Gipfel der Höhenkurve (km 27,4) aber bei km 27,4 bzw. 27,3. Die Marke für Stelle 13 steht trotzdem
   bei 26,9 (Zahl des Veranstalters).
7. `dgm.py`, `vergleich.py`: **Höhe.** Kein Laser-Modell; verglichen: Copernicus GLO-30 (TanDEM-X 2011–2015, AWS
   `copernicus-dem-30m`, Kachel N40E117) und **SRTM 1″** (Radar Februar 2000, AWS Terrain Tiles `elevation-tiles-prod/skadi/N40/
   N40E117.hgt.gz`, echte 1″-Auflösung geprüft), beide alle 10 m, gegen die Kurve des Veranstalters (`planprofil.py`: aus der
   Vektorgrafik, y-Achse aus den Hilfslinien 200–500 m, 0,4019 pt je m; Nennwerte 193–515 m, 1340 Höhenmeter):

   | Modell | Start | Ziel | min | max | ↑ 200 m | ↑ 50 m | gegen Veranstalter |
   |---|---|---|---|---|---|---|---|
   | Veranstalter (Kurve) | 246 | 247 | 194 | 514 | 988 | 1253 | – |
   | SRTM 1″ | 242 | 245 | 193 | 511 | 1005 | 1347 | Median −1,0 m, MAD 1,4 m, r = 0,995 |
   | Copernicus GLO-30 | 240 | 243 | 191 | 524 | 1043 | 1379 | Median −1,8 m, MAD 2,2 m, r = 0,994 |

   **Gewählt SRTM 1″:** näher an der Kurve, Tiefpunkt 193 m wie genannt, Gipfel 511 m (Veranstalter 515); Copernicus ist als
   Oberflächenmodell auf dem bewaldeten Grat mit Mauer und Türmen 10 m zu hoch (524 m) und unruhiger. Beide sind Oberflächenmodelle
   (SRTM sieht als C-Band-Radar etwas durch Laub); schmale Grate werden im 30-m-Raster geglättet, Stufen und Türme fehlen. Die Kurve des
   Veranstalters hat fast dieselbe Form (wohl aus einem ähnlichen Modell); **nicht angeglichen**, weil sie nur ein gezeichnetes Bild
   ist (2,5 m je pt, Achse ±0,3 km) und schon auf 1–2 m stimmt. Seine 1340 Höhenmeter entsprechen etwa einem Messfenster von 30–50 m;
   die Seite „The race“ nennt 1282 m. Vergleichsbild `../dl/vergleich.png`.
8. `build.py`: Höhen in cm im 10-m-Raster, Median über 30 m. **Brücken** (OSM bridge=yes, Modell innen über 1 m unter der Geraden →
   Gerade, gestrichelt): Brücke Changcheng Lu (km 0,8 und 41,4), Mauerbrücke (km 7,1 und 35,1), Qingnian-Brücke in Xiaying (km 15,4),
   Brücke bei Duanzhuang (km 30,0); Absenkungen 1,6–3,1 m. **Namen** (`namen.py`): Abschnitt und Ort. Straßen aus OSM in Pinyin
   (Kehuang Xian (G233), Changcheng Lu (X590), Maying Gonglu (X583)), sonst nach Art: Dorfstraße, Landstraße, Feldweg, „Weg“ (nur in
   der Karte des Veranstalters). Mauer: Treppe am Wall point 1, Große Mauer, Goat Track, Mauerbrücke, Festungsmauer, Yin-&-Yang-Platz.
   Ort: Dörfer mit den Namen und an der Stelle der Beschriftung der Karte (Huangyaguan, Xiaoping'an, Huayuan, Shipaogou aus OSM,
   Duanzhuang, Zhongying, Xiaying, Dongjiafen, Baitan, Beichedaoyu, Da Ping'an), nächste Beschriftung, Wechsel unter 400 m geglättet und
   auf Straßenwechsel gelegt. Auf der Mauer statt des Dorfs die Türme des Ausschnitts, zugeordnet zu den OSM-Turmknoten nach ihrem Anteil
   am Weg Tower 1 → Tower 4 (passt auf 2 % zu den Getränkestellen 3 = Tower 1 bei 5,5 und 4 = Tower 3 bei 6,1): Tower 1 km 5,52, Beacon
   Tower 5,71, Tower 2 5,85, Tower 3 6,04, Tower 4 (Ecke) 6,21, Wall point 2 6,4 (Getränke 5, Mitte des Abstiegs), Tower 5 7,10,
   Tower 6 7,23; im zweiten Durchgang dieselben Stellen (Tower 5 35,20 … Tower 1 36,72, Wall point 1 36,93). Kurze Turmstücke sind
   paarweise zusammengelegt („Tower 3, Tower 4“): Die App fasst Abschnitte unter 250 m mit dem Vorgänger zusammen, bevor sie gleiche
   Namen vereint, sonst fiele „Große Mauer“ in der Namenszeile weg.
   **Marken:** Getränkestellen mit Nummer, km der Höhenkurve und Inhalt aus Karte und Kurve: 1 (2,6 / 39,6) und 2 (5,1 / 37,1) Wasser,
   Elektrolyt; 3 (5,5 / 36,7) Wasser, Erste Hilfe, WC; 4 (6,1 / 36,1) Wasser; 5 (6,4 / 35,8) Wasser, Erste Hilfe; 6 (8,1) Wasser,
   Elektrolyt, Banane, (34,9) dazu Gel; 7 (11,5 / 31,5) Wasser, Elektrolyt, WC; 8, 9, 10 (14,2 / 16,6 / 19,5, an 10 WC), 11 (22,7) Wasser,
   Elektrolyt; 12 (25,3) dazu Gel; 13 (26,9) Wasser; 14 (28,9) Wasser, Elektrolyt, Banane. Guide: auf der Mauer nur Wasser, Gel für
   Marathonläufer ab km 25 und 34,5, Bananen an zwei Stellen, Toiletten an 3, 7, 10 und am Platz. Mit Banane oder Gel als
   „Verpflegung“ (`food`), sonst „Getränke“ (`water`). Erste Hilfe ohne Getränke (rote Kreuze der Karte) bei km 12,8, 21,0 und 30,1 als
   `water`-Marke „Erste Hilfe“ (wie die Schwämme in Rom). Halbmarathon-Marke bei 21 098 m (die Strecke des Halbmarathons selbst biegt
   in Duanzhuang ab).
   **`D.mauer`** = `[[5136, 7229, "Mauer, 1. Mal"], [35078, 37083, "Mauer, 2. Mal"]]`: vom Fuß der Treppe am Wall point 1 (OSM-Treppe
   222071702, Getränke 2 „5,1“ steht davor am Parkplatz, das Schild „5 KM“ im Ausschnitt gut 100 m davor) über die ganze Mauer, den Goat
   Track und die Mauerbrücke bis Tower 6, bzw. umgekehrt. Beide Durchgänge gleich gebaut, 2,1 bzw. 2,0 km (Unterschied aus der Eichung),
   je 120 m auf und 309 m ab bzw. umgekehrt. Nicht dazu gehört die Runde auf der Festungsmauer (km 7,2–8,0, 0,8 km, flach, laut Ausschnitt
   auf der Mauerkrone, nur im ersten Durchgang): Sie läuft mit dem Steigungsmodell. Wer sie mitzählen will: erster Durchgang bis 8020
   (Ende der Nordmauer am Tor). Der Halbmarathon kreuzt die Mauer einmal wie der erste Durchgang.
9. `splits.py`, `mauer.py`: **`D.mauerMin` = 65** (seit dem gemeinsamen Code 1.68 die Zeit für beide Durchgänge zusammen, in
   `app.py` nach den Medianen 22,6 : 42,5 auf die Durchgänge verteilt, vierter Wert in `D.mauer`, Herkunft in `D.mauerQ`; der Agent
   hatte zuerst 33 je Durchgang vorgeschlagen). Grundlage sind die Zwischenzeiten 2026 aller Marathonläufer beim Zeitnehmer
   (Ultimate Sports Service, live.ultimate.dk, Veranstaltung 7227, ohne Anmeldung; Messpunkte 7,5 km nach der ersten Mauer, 22, 29,
   35 km am Tor, Ziel; gespeichert nur Startnummer und Zeiten in `../dl/splits2026.json`, 394 Läufer mit allen Messpunkten). Je Läufer
   die Pace im Flachen aus 7,5 → 35 km (nur Straße) mit dem Pace-Modell der App (Minetti, 1,0 s je Höhenmeter bei 4:00 /km, bergab
   halb, 100-m-Fenster), dann Mauerzeit = Abschnittszeit minus die Straßenstücke nach Modell. Bei 4:45–5:15 Zielzeit (n = 38): **erster
   Durchgang 22,6 min** (Hälfte der Läufer 20,0–25,1), **zweiter 42,5 min** (39,3–46,2); linear über alle bei 5:00 22,2 und 41,7 min,
   je Stunde Zielzeit +3,1 bzw. +12,2 min. Das Steigungsmodell allein gäbe 14,5 und 22,5 min. Der zweite Durchgang ist langsamer, weil
   er die 300 m des Goat Track und des Abstiegs vom Wall point 2 hinaufführt und in ihm die Müdigkeit der letzten 7 km steckt (die
   Straße hinab ins Ziel rechnet das Modell mit Gewinn). Die Summe (65 min) trifft die Zielzeit,
   die Aufteilung 22,6 : 42,5 auch die Ankunft am Tor bei km 35. Unsicherheit: Lage der Matte „7,5 km“ ist nicht veröffentlicht (hier
   offiziell km 7,5 auf der Festungsmauer; stünde sie an der Ausfahrt bei km 8,1, wären es für den ersten Durchgang gut 3 min mehr).
   Weitere Quellen: Laufbericht katieaune.com (Ziel 6:51, „off the wall in just 45 minutes“, zweiter Durchgang 15 min länger, ältere
   Strecke und andere Grenzen; die Messung ergibt bei 6,5–7 h 26 und 62 min), travellingfit.com („Goat Track“ 700 m steil bergab bei
   km 7, „3 km stretch on the wall … includes a loop around the fortress walls“). Strava nicht abgefragt: Die Zwischenzeiten des Zeitnehmers für fast 400 Läufer sind belastbarer als einzelne Segmente. Der
   Guide nennt für den Inspection Day nur den Gang auf der Mauer „von Ost nach West“, keine Zeiten.
10. `route.py` (lat0/lon0 40,15/117,40), `tiles.py relief`: **Kartenhintergrund.** Proben (`../dl/proben/`, je z13 ganze Strecke, z15
    Mauer und Festung, z15 Dörfer am Anfang; nebeneinander in `vergleich_z13_strecke.jpg`, `vergleich_z15_mauer.jpg`,
    `vergleich_z15_doerfer.jpg`): (a) dunkle OSM-Karte wie sonst: fast leer, chinesisch beschriftet, keine Dorfwege; (b) Sentinel-2
    cloudless 2016 von EOX (`s2cloudless_3857`, CC BY 4.0, entsättigt und abgedunkelt): Täler und Dörfer erkennbar, aber 10 m je Pixel,
    ab z14 verschwommen, die Mauer unsichtbar, unruhiger Grund unter der farbigen Strecke; (c) **dunkles Relief** aus Copernicus GLO-30
    (Schummerung von Nordwest, kubisch interpoliert, Kacheln N40E117 und N39E117) mit Flüssen, Straßen, Wegen, Mauer (ocker) und Türmen
    aus OSM und den Dorfnamen der Karte des Veranstalters (Pinyin; weitere Orte aus OSM ohne „cun“), Namen so gesetzt, dass sie die
    Strecke möglichst nicht verdecken. **Gewählt (c):** Man sieht, dass die Strecke im Tal beginnt, über den Grat mit der Mauer führt
    und durch welche Täler und Dörfer sie läuft; ruhiger, dunkler Grund wie in den anderen Strecken; Lizenzen klar (Copernicus DEM frei
    mit Nennung, OSM ODbL; beides unter „Karte“ genannt). Dateien und `D.tiles` wie sonst (`karte-dunkel-z11…z15-*.jpg`, 17 Stücke,
    1,1 MB); Flächen wie `tiles.py`/`tiles_z11.py`/`tiles_rand.py <strecke> 2` der anderen Strecken. OSM-Linien reichen so weit wie
    die Stufen 12/13; in den Randkacheln von z11 (bis 39,9–40,6° N) nur Relief.
11. `app.py` (Texte in `sub.html`, `quellen.html`, `karte.html`, `strassennamen.html`, `imgnote.html`, `rohdaten.txt`).

## Ergebnis

↑ 1003 m / ↓ 1000 m mit 200-m-Fenster (so in der App), ↑ 1313 m mit 50 m, ↑ 1171 m mit 100 m, ↑ 789 m mit 1 km, Rohdaten ↑ 1500 m.
Start 242 m auf dem Yin-&-Yang-Platz, hinauf über Xiaoping'an und Huayuan zum Wall point 1 (434 m, km 5,1), höchster Punkt 511 m am
Beacon Tower (km 5,7 und 36,5), Wall point 2 423 m, Goat Track hinab zur Festung (241 m, km 7,1). Im Tal hinab bis 194 m an der
Qingnian-Brücke in Xiaying (km 15,5), drei Hügel 297 m (km 18,2), 356 m (km 23,3) und 354 m (km 27,4), zurück durchs Tal zum Platz
(244 m, km 35), Mauer in Gegenrichtung (270 m hinauf), 5 km Straße hinab ins Ziel (245 m). Steilste Straßenstücke über 200 m +18,9 %
(km 4,9, vor dem Wall point 1) und −19,6 % (km 37,3); auf Goat Track und Treppen über 200 m bis ±50 %.

Geprüft mit Playwright (393 × 852, Faktor 2, Server auf Port 8777): keine Konsolenfehler, `APP_VERSION` 1.0, Service Worker installiert
(Cache `gwm-marathon-profil`), Tipp auf die Version meldet „Version 1.0 ist aktuell“, alle 17 Kartenstücke laden und passen zu
`D.tiles` und `sw.js` (prüft `app.py` selbst). Laufansicht am Start, km 2,6, auf der Mauer (Tower 1), Goat Track, Festung, Tor (km 35),
zweiter Durchgang, Beacon Tower und Ziel angesehen, Zahlen- und Kartenseite; Abschnitte „Woher die Zahlen kommen“, „Für Zuschauer“,
„Zwischenzeiten“ geöffnet: Mauerzeile („zweimal über die Mauer: km 5,1–7,2 und km 35,1–37,1“), Tor („Am Tor zur Mauer (km 35,0)“,
Reserve, Zielschluss 15:50) und Wellen erscheinen. `grep -i "tokio|tokyo|tyo-|tyo\.|GSI"` in `greatwall/index.html` und `sw.js`: keine
Treffer.

## Offen

- Prüfung am iPhone; Karte auf der Startseite (Vorschlag: Eyebrow „Great Wall Marathon“, Stadt „Große Mauer“, „Kurs 2026“,
  `data-termine="2027-05-15"`, `data-monat="5"`, Termin „Sa., 15. Mai 2027“, ↑ 1003 m / ↓ 1000 m, Höhe 194–511 m, `data-such`
  „Great Wall Chinesische Mauer China Peking Beijing Tianjin Jizhou Huangyaguan Albatros interAir“), README-Tabelle und Liste der
  Speicherschlüssel/Cache-Präfixe (`gwm-`). Der Höhenbereich (317 m) wäre im gemeinsamen Maßstab der Mini-Profile 444 px hoch.
- Runners Guide 2027 (Wellen, Tor- und Zielschlusszeiten) und Streckenkarte 2027 abwarten; bei neuer Karte `plan.py` bis `build.py`
  neu laufen lassen (die Einpassung in `georef.py` gilt nur für dieses PDF).
- Linie: 12 km nur nach der gezeichneten Karte (auf etwa ±20–40 m; im Satellitenbild der Karte sind die Wege nicht sicher zu
  erkennen). Sobald OSM dort Wege bekommt oder eine GPX-Datei auftaucht, `osm.py` und `linie.py` neu laufen lassen.
- Mauerzeit: Ein Wert für beide Durchgänge passt schlecht (gemessen 23 und 42 min bei 5 h); siehe Daten 9.
- Schild „27 KM“ und Getränkestelle 13 widersprechen Linie und Höhenkurve um 0,4 km (Daten 6); vor Ort oder in einer neuen Karte prüfen.
