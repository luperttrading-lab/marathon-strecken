# Übergabe: Steigungsprofil ADAC Marathon Hannover

Stand 31.10.2026, App-Version **2.3** (erste Fassung, angelegt mit `werkzeuge/kern/kern.py --neu` auf dem gemeinsamen Kern; die
Hauptsitzung zählt die Nummer beim Veröffentlichen hoch).
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/hannover/.

Die App hat den gemeinsamen Kern aus `hamburg/` und eigene Felder (Texte, `const D`, Speicherschlüssel `han-…`, Service-Worker-Cache
`han-marathon-profil`, löscht nur Caches mit Präfix `han-`; der Präfix war frei, `kern.py --neu` prüft das), ohne eigenes Manifest und
Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Startseite,
README, `version.json` und `karten.json` sind noch nicht angepasst (Hauptsitzung).

**Besonderheiten:** Die Höhen kommen aus dem **amtlichen Laser-Geländemodell DGM1 Niedersachsen** (LGLN, 1-m-Raster, CC BY 4.0 mit
Pflicht-Quellenvermerk „© GeoBasis-DE/LGLN 2026, Daten geändert“, steht im Untertitel und unter „Woher die Zahlen kommen“), die
Brückendecks aus dem **Oberflächenmodell DOM1** derselben Befliegung (gemessen, wie die Deutzer Brücke in Köln). Die Linie stammt aus der
interaktiven Google-My-Maps-Karte des Veranstalters. Hannover ist die **flachste Strecke der App**: ↑ 43 m, das Profil kostet bei
4:00 /km 18 s. Es gibt einen **Staffel-Marathon** auf derselben Strecke (fünf Wechsel, Schalter in den Einstellungen erscheint).

## Termin und Start

35. ADAC Marathon Hannover am **Sonntag, 11. April 2027**: Startseite des Veranstalters (https://www.marathon-hannover.de/,
`../dl/seiten/start.html`: „Race Countdown 11.04.2027“, „Das war der 34. ADAC Marathon Hannover! … freuen uns auf die Neuauflage am
11. April 2027“), Seite „Allgemeine Infos“ (`teilnehmer_allgemeine-infos.html`: „Startzeiten am 11. April 2027“, Ausgabe der
Startunterlagen „Freitag (9. April) … Samstag (10. April) … Sonntag (11. April)“). Der 34. war am Sonntag, 12. April 2026 (Bildergalerie
„Sonntag, 12.04.2026“, Ergebnisse 2026). Veranstalter eichels GmbH (Hannover), Namensgeber ADAC Niedersachsen/Sachsen-Anhalt.
`D.termine` `["2026-04-12", "2027-04-11"]` (2027 vom Veranstalter bestätigt, ohne „?“), `D.tz` Europe/Berlin, `D.start` = 600 (10:00).
Kein `D.lage`, `D.mauer`, `D.tor`, `D.zielschluss`.

**Start** (`D.wellen`, Seite „Marathon“, `teilnehmer_allgemeine-infos_marathon.html`, Stand Oktober 2026, schon für 2027 überschrieben):
„Der ADAC Marathon Hannover startet um 10:00 Uhr (DM, Elite und die Blöcke B + C). Es wird in 2 Wellen gestartet. Der Block D startet
um 10:05 Uhr. Zielschluss: 16:00 Uhr.“ In der App zwei Wellenknöpfe „Welle 1 · 10:00 Elite, Blöcke B und C“ und „Welle 2 · 10:05 Block
D“, im Text dazu Deutsche Meisterschaft, Staffel ab 10:30 Uhr und Handbikes 9:45 Uhr (Tabelle „Startzeiten am 11. April 2027“ auf
„Allgemeine Infos“, dort auch „ADAC Marathon ab 10:00 Uhr, Zielschluss 16:00 Uhr, min. Pace 08:20 min/km“). **Zeitlimit:** „Für den
Marathon gilt eine Sollzeit von 6:00 Std. … dass der ‚Besenwagen‘ Sie von der Strecke holt“ (Seite „Streckenservice“). Ob die
Deutschen Meisterschaften 2027 wieder in Hannover sind (2026 ja), habe ich beim DLV nicht bestätigt gefunden; die Seite des Veranstalters
nennt „DM“ weiter.

**Halbmarathon-Marke** bei 21 098 m (nur die Marke wie in den anderen Apps): Der Halbmarathon startet um 11:30 Uhr und läuft nur auf den
ersten 4 km auf derselben Linie (danach eigene Führung; sein km 5 liegt rund 0,8 km neben dem des Marathons). Im selben Rennen
läuft der **enercity Staffel-Marathon** (fünf Läufer, Start ab 10:30 Uhr): Wechselzonen laut Seite „Streckenverlauf“ und
Staffel-Information 2026 bei km 7,4 Hildesheimer Straße, 14,5 Zoo (Waldchaussee), 20,8 Podbielskistraße, 28,0 Celler Straße, 32,6
Vahrenwalder Straße (die Etappenlängen der Tabelle, 7,4 / 7,1 / 6,5 / 7,2 / 4,6 / 9,6 km, ergeben zusammen 42,4 km, sind also gerundet).

**Start und Ziel:** beide auf dem Friedrichswall vor dem Neuen Rathaus (Plan „Veranstaltungsgelände 2026“,
`../dl/pdf/Plan_Veranstaltungsgelaende_2026_neu.jpg`), Start nach Westen, Ziel 27 m östlich der Startlinie (Linienende = Punkt „Ziel“ im
Digitalen Zwilling).

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Reihenfolge: `parse.py`, `osm.py`, `strassen.py`, `dgm.py` (mit `lgln.py`), `deck.py`, `clean.py`, `orte.py`, `stationen.py`, `build.py`,
`route.py`, `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py hannover`, `hannover/work/app.py` (beim ersten Mal über
`kern.py --neu hannover work/felder.json`, danach ersetzt es nur die Felder und lässt Kartenbilder und `D.tiles` stehen),
`tiles_rand.py hannover 2`. Nur Abgleich/Ausgabe: `marken.py`, `auswertung.py`, `text.py` (Text einer gespeicherten Seite). Prüfen:
`pruefen.js`, `pruefen2.js`, `pruefen3.js` (Server auf Port 8791, `NODE_PATH=/opt/node-tools/node_modules node pruefen.js`).

1. **Strecke** (`parse.py`): Die Seite „Streckenverlauf“ (https://www.marathon-hannover.de/strecken/streckenverlauf.html) bettet eine
   Google-My-Maps-Karte ein („Interaktive Karte der Marathon-, Halbmarathon und 10km-Strecke mit Kilometerpunkten,
   Staffel-Wechselzonen, Erfrischungs- und Verpflegungspunkten“, `mid=1uoNL65nZY9ycqJT8_tkXr18USC2-Blw`). Als KML ohne Anmeldung:
   `https://www.google.com/maps/d/kml?mid=1uoNL65nZY9ycqJT8_tkXr18USC2-Blw&forcekml=1` (`../dl/kml/mymaps.kml`). Linie „Marathon“:
   708 Punkte, Abstand im Median 38 m (gerade Stücke bis 534 m), **42 279,0 m** auf dem Ellipsoid. Sie folgt den Straßen: im Median 1,8 m
   neben einem OSM-Weg, 90 % bis 3,7 m, höchstens 9,8 m (mit Einrasten gezeichnet); daher kein eigenes Map-Matching.
   **Gegenprobe Streckenplan 2026** (`../dl/pdf/Streckenplan_ADAC-Marathon_2026_neu.pdf`/`.jpg`, Illustrator 20.02.2026, „Stand 01/2026“):
   gleicher Weg, gleiche Wechselzonen und Verpflegung. **Digitaler Zwilling der Stadt** (Link auf derselben Seite,
   `https://stadtmodell-prod4.hannover-stadt.de/DT1/`, VC Map; Konfiguration `app.config.json` → `configs/e973f6e5-….json`, Ebenen als
   GeoJSON unter `…/DT1/datasource-data/2300151-0_Marathon_Hannover/`, Namensnennung „LH Hannover - Geoinformation, CC-BY-4.0“ und
   „eichels GmbH“; `../dl/zwilling/`): `Marathon-Einzelstuecke.geojson` ist dieselbe Linie in EPSG:25832 (705 Stücke, im Median 0,2 m
   neben der KML). Eine GPX-Datei des Veranstalters gibt es nicht.
2. `common.py`: **Kilometer gleichmäßig** über die Linie (Faktor 42 195 / 42 279,0 = 0,99801), Start am Linienanfang, Ziel am Ende.
   `marken.py`: Die 42 Kilometerpunkte der My-Maps-Karte sind von Hand gesetzt (Abstand Marke zu Marke 736–1211 Linienmeter), die
   43 Punkte des Zwillings (`Marathon_Punkte.geojson`, mit „HM“) gleichmäßig über dieselbe Linie verteilt (982–1021 m, Linienmeter ≈
   km × 1002). Keiner der beiden taugt zum Eichen; der Zwilling bestätigt nur die gleichmäßige Streckung. „Alle Strecken sind offiziell
   vermessen“ (Veranstalter). **Genauigkeit: Kilometer auf etwa ±0,1 km**, einzeln nicht belegt.
3. `osm.py`: OSM über die API (`api.openstreetmap.org/api/0.6/map`) in 150 Rechtecken zu 0,005° höchstens 150 m neben der Linie, eine
   Abfrage je Sekunde (`../dl/osmapi/`, keine 509/429) → `../dl/osm_netz.json` (20 158 Wege). Overpass war nicht nutzbar
   (overpass-api.de Verbindung abgebrochen, maps.mail.ru 504, kumi.systems keine Antwort).
   `strassen.py` (wie Honolulu): je 10 m der nächste Weg bis 20 m neben der Linie mit höchstens 35° Richtungsabweichung, Hauptstraßen
   bevorzugt; Fußwege unter der Erde (`level` < 0, `indoor`) mit 10 m Aufschlag, sonst gewann am Hauptbahnhof die Ladenpassage
   „Niki-de-Saint-Phalle-Promenade“ unter der Bahnhofstraße. Namen wie in OSM (`namen.py`).
4. `orte.py`: **Stadtteil** alle 100 m: die 51 Stadtteile der Landeshauptstadt (OSM `admin_level` 10; 22 Flächen über
   `api.openstreetmap.org/api/0.6/relation/<id>/full`, `../dl/orte/`), je 40 m links und rechts, bei zwei Stadtteilen „links / rechts“.
   Die 13 Stadtbezirke (`admin_level` 9) sind Verwaltung. Das kurze Stück „Mitte“ am Ziel bleibt (`build.py`). Folge: Mitte, Calenberger
   Neustadt, Südstadt, Döhren, Waldhausen, Südstadt, Mitte, Oststadt / Mitte, Zoo, Groß-Buchholz (Groß-Buchholz / Bothfeld an der
   Podbielskistraße), Groß-Buchholz / List, Zoo / List, Zoo, Oststadt / Zoo, Oststadt, Mitte / Oststadt, List / Oststadt, List,
   List / Vahrenwald, Vahrenwald, Nordstadt, Calenberger Neustadt, Mitte / Calenberger Neustadt, Calenberger Neustadt, Mitte.
5. `dgm.py`, `lgln.py`: **Höhe aus dem DGM1 Niedersachsen** (LGLN, OpenGeoData.NI, https://ni-lgln-opengeodata.hub.arcgis.com/).
   Kachelübersichten `https://arcgis-geojson.s3.eu-de.cloud-object-storage.appdomain.cloud/{dgm1,dom1}/lgln-opengeodata-{dgm1,dom1}.geojson`
   (`../dl/lgln/idx_*.geojson`, daraus `kacheln_*.json`), Kacheln offen auf `dgm1.s3.eu-de.cloud-object-storage.appdomain.cloud/L1603/
   Vollkacheln/dgm1_32_<E>_<N>_1_ni_2016.tif` (bzw. `dom1…`), je 35 Kacheln 1 × 1 km (GeoTIFF/COG, Float32, LZW, rund 3,4 MB, NoData
   −9999), EPSG:25832, Höhen NHN (DHHN2016, Quasigeoid GCG2016). Metadaten je Kachel (`….xml`): Los L1603, Aktualität 13.02. bzw.
   18.04.2016, „GENAUIGKEIT 0.3“; Produktbeschreibung im Hub: „≤ 15 cm“ in flachem offenem Gelände, aus Laserscan mit mindestens
   4 Punkten/m², Rastermitte auf 0,5 m. Bilinear alle 10 Linienmeter, 4229 Punkte, alle mit Wert. Ein Laser-DGM1 2021 der Stadt (im
   Zwilling als Cesium-Gelände) habe ich nicht genutzt.
   **Lizenz:** AGNB des LGLN, Abschnitt 7 (https://www.lgln.niedersachsen.de/…/allgemeine-geschafts-und-nutzungsbedingungen-agnb-97401.html,
   `../dl/lgln/agnb.html`): „7.1 Die … unter https://ni-lgln-opengeodata.hub.arcgis.com aufgeführten Geodaten (offene Geodaten) können
   unter den Bedingungen der Lizenz ‚Creative Commons‘ (CC-BY 4.0) kostenfrei … genutzt werden. 7.2 … deutlich sichtbaren
   Quellenvermerk: © GeoBasis-DE/LGLN Jahr, Daten geändert“. Steht der Vermerk nicht im Zusammenhang mit der Darstellung, ist die Nutzung
   dem LGLN anzuzeigen; deshalb steht er im Untertitel direkt über Karte und Profil. (Die ältere OpenGeoData-Seite nennt noch
   dl-de/by-2-0; maßgeblich sind die AGNB.)
6. `deck.py`, `clean.py`: **Brücken und Unterführungen.**
   - **Brücken aus dem DOM1** (gleiche Befliegung, Quelle und Lizenz): Je 10-m-Punkt der OSM-Brücken das 25-%-Quantil der 5 × 5 DOM-Werte
     (`deck.json`), übernommen, wo es über dem DGM und höchstens 3 m über den Brückenenden liegt (sonst Bäume, Leuchten). An den Enden
     stimmen DOM und DGM auf 0,05 m. Arthur-Menge-Ufer km 1,65 (DGM 51,9 m im Graben, Deck 54,9 m), **Pasteurallee** km 18,74–18,81 und
     **Noltemeyerbrücke** km 19,77–19,84 über den Mittellandkanal (DGM 50,3 m = Wasserspiegel, Deck 56,8 bzw. 57,3 m), Wilhelmshavener
     Straße km 39,91 (48,4 → 52,1 m), Königsworther Straße km 40,42 (48,8 → 53,9 m), Brühlstraße km 41,17 (52,3 → 54,2 m). Gemessen,
     nicht schraffiert. Bernadotteallee km 24,62 (10 m) hat das DGM mit Fahrbahn.
   - **Unterführungen, geschätzt** (`D.bridges`, schraffiert): **Fernroder Straße** unter den Gleisen des Hauptbahnhofs (OSM `tunnel=yes`,
     km 12,11–12,26, 150 m): DGM und DOM messen das Bahngelände (bis 59,8 m); Gerade 53,75 → 54,03 m. **Kopernikusstraße** unter der Bahn in
     der Nordstadt (km 36,17–36,25, 80 m): Bahndamm bis 57,1 m; Gerade 50,56 → 49,62 m (die Rampen davor und danach sind gemessen; die
     tiefste Stelle unter der Brücke könnte etwas tiefer liegen).
   Danach keine Stufe über 0,41 m je 10 m. Keine weitere Glättung.
7. `stationen.py`: **Verpflegung und Staffelwechsel** aus der My-Maps-Karte (Ebenen „EP's & VP's“, „Wechselzonen“), je Punkt in einem
   Fenster ±2,5 km um die Sollstelle projiziert (die Fritz-Behrens-Allee kommt zweimal vor). Seite „Streckenservice“: „nach jeweils 5 km
   Verpflegungspunkte (VP), dazwischen Erfrischungspunkte (EP)“; Eigenverpflegung an allen VP; Streckenverpflegung laut Seite
   „Inhaltsstoffe“: Dextro Energy Zero Calories Orange, enerBIO Fruchtschnitte, Banane, Cola (was wo, sagt der Veranstalter nicht).
   Zwilling: VP „Getränke+Essen“, EP „Getränke“. Refill-Station (grüner Ring im Streckenplan) an VP 3, 7 und 11. Gegenprobe mit den
   Punkten des Zwillings: im Median 25 m Unterschied, höchstens 0,2 km (VP 11, VP 15, VP 1). In der App: VP „Verpflegung“ (food), EP
   „Getränke“ (water), Wechsel „Wechsel 1–5“ (relay, mit km-Angabe des Veranstalters im Text), Halbmarathon; 21 Marken. VP 1 km 4,9
   Schützenallee, EP 2 8,4 Hildesheimer Straße, VP 3 10,0, EP 4 12,4 Fernroder Straße, VP 5 15,1 Waldchaussee, EP 6 17,5 Groß-Buchholzer
   Straße, VP 7 20,0 Podbielskistraße, EP 8 22,4 Walderseestraße, VP 9 25,1 Fritz-Behrens-Allee, EP 10 27,4 Hamburger Allee, VP 11 30,1
   Lister Kirchweg, EP 12 31,9 Vahrenwalder Straße, VP 13 35,0 Henschelweg, EP 14 37,5 Appelstraße, VP 15 40,2 Wilhelmshavener Straße;
   Wechsel 7,40 / 14,50 / 20,77 / 27,89 / 32,78 (Veranstalter 7,4 / 14,5 / 20,8 / 28,0 / 32,6). Nicht übernommen: Toiletten,
   Sanitäter, Wasser in den Wechselzonen.
8. `build.py`: Höhen in cm im 10-m-Raster, Median über 30 m; Straßenstücke unter 80 m und Stadtteile unter 300 m dem Vorgänger
   zugeschlagen (außer am Ziel). `route.py` (lat0/lon0 52,4/9,7), `tiles.py` (z12–z15), `tiles_z11.py hannover`, `app.py`,
   `tiles_rand.py hannover 2`: 27 Kartenstücke, 2,9 MB.

## Ergebnis

↑ 43 m / ↓ 42 m mit 200-m-Fenster, ↑ 58 / ↓ 58 m mit 50 m, ↑ 52 / ↓ 52 m mit 100 m, ↑ 20 / ↓ 20 m mit 1 km; wie GPS-Uhren 36 (ab
0,5 m), 25 (ab 1 m), 12 (ab 3 m); Rohdaten ↑ 125 m (DGM Punkt für Punkt, mit den Senken unter den Brücken und den Buckeln über den
Unterführungen). Start 54,4 m, Ziel 54,5 m auf dem Friedrichswall, tiefster Punkt 49,7 m in der Unterführung der Kopernikusstraße
(km 36,24, geschätzt; gemessen 49,6 m an ihrem Ausgang), höchster 59,1 m an der Bothmerstraße in Döhren (km 6,42); **Höhenbereich 9,4 m**.
Der Veranstalter schreibt „Mit nur 19 m Höhenunterschied sind Bestzeiten garantiert“; woher die 19 m kommen, ist offen (das DGM ohne
Bereinigung reicht von 48,4 m im Wasser unter der Wilhelmshavener Straße bis 59,8 m auf dem Bahnhofsgelände, 11,4 m).
Verlauf: über Lavesallee und Waterlooplatz 3 m hinunter in die Leine-Aue (51,3 m), über die Brücke am Arthur-Menge-Ufer an den Maschsee,
eben am Ostufer, über Schützenallee und Wiehbergstraße 5 m hinauf nach Döhren, die Hildesheimer Straße sanft hinunter (3 m auf 4 km),
am Kröpcke 56,5 m, durch die Fernroder Straße unter dem Bahnhof, eben durch die Eilenriede (53–55 m), über den Mittellandkanal hin und
zurück (57 m), eben durch List und Vahrenwald, in der Kopernikusstraße 4,5 m hinunter und ebenso viel wieder hinauf (steilste Stellen über 200 m: −2,0 %
bei km 36,14, +2,3 % bei km 36,35; über 100 m ±2,6 %), Nordstadt, über die Brücken an Wilhelmshavener und Königsworther Straße ans
Leibnizufer und eben ins Ziel.
**Modellzeit:** Mit 4:00/km im Flachen ergibt das Modell **2:49:04** (das Profil kostet 18 s); **bei 2:50:00 kostet es 18 s, bei 4:00:00
25 s** (Flach-Pace 4:01,3 bzw. 5:40,7 /km; gemessen mit `pruefen.js` in der App 2.3). Zum Vergleich bei 4:00 /km: Köln 48 s (laut seiner Übergabe); bei
2:50:00 Wien 61 s, Honolulu 85 s, Boston 88 s, Stockholm 113 s.

Geprüft mit Playwright (Chromium, 393 × 852, Faktor 2, Server auf Port 8791, `pruefen.js`, `pruefen2.js`, `pruefen3.js`): keine
Konsolenfehler, `APP_VERSION` 2.3 und Knopf v2.3, Service Worker installiert (33 Einträge im Cache `han-marathon-profil`), Tipp auf die
Version meldet „Version 2.3 ist aktuell“; alle 27 Kartenstücke passen zu `D.tiles` und `sw.js` und laden; Tabellen bei
320/375/393/430 px ohne Überbreite, Seite nicht breiter als das Fenster; Staffel-Einstellung sichtbar. Laufansicht am Start, km 1,66
(Arthur-Menge-Ufer), 6,4 (Döhren), 12,18 (Fernroder Straße), 18,78 (Mittellandkanal), 36,2 (Kopernikusstraße), 42,05 (Ziel) und die
Kartenübersicht mit Verpflegung bei km 20 angesehen; Zuschauer-Tabelle mit zwei Wellen und „So., 11. April 2027“; „Woher die Zahlen
kommen“ angesehen. Bilder in `work/shots/`. `kern.py` meldet alle Apps „gleich“, nur `karten.json` veraltet (neue Strecke, Hauptsitzung).
Hinweis für Prüfskripte: `fetch(…, {method: 'HEAD'})` auf Kartenbilder bricht im Service Worker ab (`net::ERR_ABORTED`), daher GET.

## Offen

- Prüfung am iPhone.
- Startseite: Karte fehlt. Eyebrow „ADAC Marathon Hannover“, Stadt „Hannover“, „Kurs 2026“, `data-termine="2026-04-12 2027-04-11"`,
  `data-monat="4"`, ↑ 43 m / ↓ 42 m, Höhe 50–59 m, `data-such` z. B. „Hannover Niedersachsen Deutschland ADAC Maschsee Eilenriede
  Rathaus“; Mini-Profil mit 9,4 m Höhenbereich passt in die Grundhöhe 64 px. README-Tabelle und Liste der Präfixe (`han-`), `karten.json`
  (`kern.py --version … --schreiben`). Fuß der Startseite: „Hannover: DGM1 Niedersachsen, © GeoBasis-DE/LGLN 2026, CC BY 4.0“.
  **Teilnehmer 2026:** 4 881 Marathon-Finisher (offizielle Ergebnisliste, race result Ereignis 353464 „ADAC Marathon Hannover 2026“,
  Wettbewerb „ADAC Marathon“, Liste „Ergebnisliste MW“: 4 881 mit Platz, dazu 21 disqualifiziert, 7 aufgegeben, 1 nicht gestartet;
  verlinkt von https://www.marathon-hannover.de/ergebnisse-1/2026.html; nur gezählt, keine Namen gespeichert). Deckt sich mit der Zahl
  von runinternational.eu/HDsports.
- Kurs 2027: Die Seiten zeigen den Streckenplan 2026; ein neuer Plan kommt vermutlich Anfang 2027 („Stand 01/2026“). Dann KML neu
  laden (`parse.py` und die Kette). Wellen (Blöcke) und Deutsche Meisterschaft 2027 prüfen.
- Kilometer nur gleichmäßig gestreckt (Daten 2); Verpflegung auf etwa ±0,2 km.
- Unterführungen geschätzt (Daten 6); die Fahrbahn unter dem Bahnhof und in der Kopernikusstraße ist nicht gemessen.
- DGM1 von 2016; Bauarbeiten seitdem an der Strecke sind nicht berücksichtigt (die Stadt hat ein DGM1 2021, nur als Cesium-Gelände im
  Zwilling gesehen).
