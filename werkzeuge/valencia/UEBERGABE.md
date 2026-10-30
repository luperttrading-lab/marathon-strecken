# Übergabe: Steigungsprofil Valencia-Marathon

Stand 29.10.2026, App-Version **1.3** (1.3: Steigungskosten als große Zeile unter der Zielzeit; 1.2: Umschalter Höhe/Meereshöhe für die Tabelle „Ohne Höhenmeter“, nur bei `D.lage`; 1.1: Feld `D.lage` für hoch gelegene Strecken: Tabelle „Ohne Höhenmeter“ nennt dann die Höhe; 1.0: erste Fassung). Adresse nach dem Hochladen:
https://luperttrading-lab.github.io/marathon-strecken/valencia/.

Die App ist eine Kopie der Tokio-App (Stand 1.22, aktueller gemeinsamer Code) mit eigenen Daten, Texten und
Speicherschlüsseln (`vlc-…`, Service-Worker-Cache `vlc-marathon-profil`), ohne eigenes Manifest und Symbol. Alle
Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Änderungen
am gemeinsamen Code in allen Apps nachziehen (README).

## Termin und Start

46. Maratón Valencia Trinidad Alfonso Zurich am Sonntag, 6. Dezember 2026 (Reglement 2026 des Veranstalters S.D.
Correcaminos / Valencia Ciudad del Running, Art. 1 und 3, https://www.valenciaciudaddelrunning.com/maraton/reglamento-maraton-valencia/).
2027 ist noch nicht veröffentlicht; der Lauf ist seit Jahren am ersten Sonntag im Dezember, daher `2027-12-05?`
(unbestätigt). Start 8:15 Uhr, Zielschluss 15:15 Uhr (5:30 h ab Überqueren der Startlinie, km 25 bis 12:57 Uhr).
`D.start` = 495, `D.tz` Europe/Madrid, `D.ort` „Valencia“ (sonst hieße es nach der Zeitzone „Madrid“), `D.ortKurz` „ Valencia“.

**Startwellen** (`D.wellen`): neun Wellen laut Reglement 2026, Art. 3, alle 10 min von 8:15 bis 9:35, eingeteilt nach
angegebener Zielzeit (unter 3:32 mit Nachweis einer Bestzeit): unter 2:50 / 2:50–3:00 / 3:00–3:12 / 3:12–3:20 /
3:20–3:32 / 3:32–3:43 / 3:43–3:56 / 3:56–4:10 / ab 4:10. Boxen und Farben aus Streckenplan 2026 und Google-Karte:
Box 1–3 Gelb, Grün, Blau (8:15), Box 4 Rosa (8:25), 5 Orange, 6 Lila, 7 Braun, 8 Grau, 9 Rot, 10 Blaue Punkte, 11 Weiß
(9:35). Rollstühle starten vorab mit der dritten Welle.

Start auf dem Pont de Montolivet an der Plaça de la Marató (Ciutat de les Arts i les Ciències), Ziel auf dem blauen Steg
über dem Wasserbecken vor dem Hemisfèric, nach der Durchfahrt unter dem Pont de Montolivet.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

1. **Strecke** aus der Google-Karte des Veranstalters, eingebettet auf
   https://www.valenciaciudaddelrunning.com/maraton/recorrido-maraton/ (Seite „Recorrido Maratón Valencia 2026“, Karte
   „42KVALENCIA INFO CARRERA“, Beschreibung „Edición 2025“), als KML:
   `https://www.google.com/maps/d/kml?mid=1BEeuxU3kRDyxewR7Pp4Rqu_7Knajvxo&forcekml=1` (`../dl/karte_….kml`). Ordner
   „42K 2025“: Linie „RECORRIDO · RACE LINE“ (839 Punkte), km 0, 42 Kilometermarken, Halbmarathon, META; „RECORRIDO 2“
   ist nur die zweite Fahrbahn der ersten 1000 m. Ordner „AVITUALLAMIENTO“: 9 Getränkestellen, 3 Gel-Stellen („Red Point
   Enervit“). Ordner „BOX“: 11 Startboxen mit Uhrzeit. `parse.py` schneidet an km 0 und META (10 bzw. 7 m neben der Linie)
   und projiziert die Marken auf die Linie (höchstens 12 m daneben; bei Hin- und Rückweg auf derselben Straße gilt die
   Stelle nahe der erwarteten). Linienmeter geodätisch (GRS80): **42 193 m** (Haversine wäre 42 171 m, UTM 42 204 m).
   → `gpx2026.json`, `marken.json`.
   **Kurs 2026:** Der Streckenplan 2026 (`https://www.valenciaciudaddelrunning.com/wp-content/uploads/2019/04/recorrido-42k-valencia-2026.pdf`,
   „Plano Recorrido 42k 2026 v3 - Provisional“, 20.07.2026, „6 December 2026 · 8:15h“) ist eine Vektorgrafik.
   `vergleich.py` zieht die Streckenlinie aus dem PDF, passt sie affin auf die Linie der Karte ein und misst den Abstand:
   Median 5 m, nirgends mehr als 54 m (der Plan ist verzerrt und an Start und Ziel schematisch); in der Überlagerung
   liegen auch die Kilometermarken des Plans an denselben Stellen. Gleicher Weg, daher „Kurs 2026“.
2. `common.py`: Kilometer stückweise linear über die 42 Marken und den Halbmarathon (Marke zu Marke 988–1012 Linienmeter,
   km 42 bis Ziel 201 m).
3. `dgm.py`: **MDT02 des IGN** (PNOA-LiDAR, zweite Befliegung, 2-m-Raster aus Bodenpunkten) über den INSPIRE-WMS des IGN,
   GetFeatureInfo je Punkt (`servicios.idee.es/wms-inspire/mdt`, Ebene `EL.ElevationGridCoverage`, Antwort
   „MDT02_H30“, `GRAY_INDEX` in Metern mit Nachkommastellen), alle 10 m, 4221 Punkte, 8 parallel, gut 25 min (der Dienst
   bricht oft ab, Zwischenstand in `../dl/mdt02_cache.json`). Höhen über dem Meer (REDNAP, Pegel Alicante). Lizenz
   CC BY 4.0 (scne.es), Quelle Instituto Geográfico Nacional. **Nicht genommen:** der INSPIRE-WCS
   (`servicios.idee.es/wcs-inspire/mdt`, `Elevacion25830_5`): 5-m-Raster, aber auf ganze Meter gerundet (GeoTIFF Int16,
   auch die ASCII-Ausgabe ist zu 56 % ganzzahlig) – für eine Strecke mit 25 m Höhenbereich zu grob. Er dient nur als
   Gegenprobe (km 34,75: MDT02 25,9 m, WCS 26,0 m).
4. `osm.py`: OSM-Wege im Umkreis von 40 m um die Linie, Overpass-Spiegel maps.mail.ru in 9 Stücken (die ganze Abfrage lief
   in 504; overpass-api.de und andere Spiegel waren aus dieser Umgebung nicht erreichbar), Zwischenstand je Stück in
   `../dl/osm_teil_*.json`. `streets.py`: je 10 m der nächste Weg höchstens 20 m daneben, Hauptstraßen bevorzugt, ohne
   Tunnel. `namen.py`: Name so, wie er in OSM unter `name` steht (in València valencianisch, gleich `name:ca`, z. B.
   „Avinguda dels Tarongers“, „Carrer de Colón“), Klammerzusätze entfallen.
5. `orte.py`: **Distrikte** der Stadt aus dem Geoportal des Ajuntament (Open Data „districtes-distritos“,
   `geoportal.valencia.es/server/rest/services/OPENDATA/UrbanismoEInfraestructuras/MapServer/225/query?…&f=geojson`),
   alle 100 m. Die 88 Barrios (Ebene 224) wären feiner, die Strecke läuft aber oft auf ihren Grenzstraßen und wechselt
   dann im 100-m-Takt (z. B. Blasco Ibáñez, km 16–18). Schreibweise wie im Statistischen Jahrbuch der Stadt, am
   Zeilenanfang mit großem Artikel („El Pla del Real“, „La Saïdia“, „L'Olivereta“).
6. `clean.py`: Brücken aus OSM (bridge=yes auf der Linie, Enden oben auf den Rampen), nur wo das Modell innen mehr als
   **1,0 m** unter der Geraden liegt (Tokio 0,5 m; das Turia-Bett liegt hier 3–7 m tiefer). Das MDT02 misst manche
   Brücken selbst (unter der Fahrbahn fehlen Bodenpunkte, das Modell spannt dann von Widerlager zu Widerlager).
   **Geschätzt** (schraffiert): Pont de Montolivet am Start (km 0,03–0,36, Modell bis 2,9 m tiefer), Pont de les Arts
   mit Zufahrt (km 27,53–27,86; von Hand ab km 27,54: auf der Carrer de Mauro Guillén liegt die Linie auf der Kante zum
   Flussbett, das Modell fällt um gut 2 m und springt in 10 m um 2,9 m zurück) und der **Zielsteg** (km 41,96–42,195):
   Wasser laut OSM (natural=water, `../dl/osm_ziel.xml` aus der OSM-API), dort misst das Modell die Wasserfläche
   (2,7 m, östlich der Brücke 3,2–3,4 m) und unter dem Pont de Montolivet die Brücke darüber (9–12 m). Der Steg ist nicht
   vermessen: waagerecht in Höhe des Uferwegs davor (3,3 m). **Gemessen:** Pont de les Glòries Valencianes (km 32,3–32,5,
   Modell glatt auf 18 m) und Pont del Nou d'Octubre (km 34,4–34,6, Modell nur 0,3–0,6 m unter der Geraden). Tunnel:
   keiner auf der Strecke; unter der Carrer de Guillem de Castro (km 27,9–28,1) und der Carrer d'Àngel Guimerà
   (km 31,2–31,4) liegen Straßentunnel, das Modell misst die Oberfläche. Nicht bereinigt: Delle von 1,2 m auf einem
   Punkt bei km 9,3 (Kreisel an der Avinguda de Catalunya über einer Fußgängerunterführung).
7. `build.py`: Höhen in cm im 10-m-Raster, Median über 30 m; Straßenstücke unter 80 m und Distrikte unter 300 m dem
   Vorgänger zugeschlagen; ab der Rampe ins alte Flussbett (km 41,7, OSM ohne Namen, über dem Steg nur der Pont de
   Montolivet darüber) heißt die Straße „Ciutat de les Arts i les Ciències“. Marken: Getränke km 5,5 / 10 / 14,5 / 18,7
   (Wasser Aquabona, Aquarius), Verpflegung km 23 / 28,3 / 33,1 / 37,1 / 40,4 (dazu Obst), Gel km 16,2 / 25,8 / 34
   (Enervit), Angebot und km-Angaben laut Plan 2026 (die Karte nennt km 28,2 statt 28,3), Lage laut Karte.
   `route.py` (lat0/lon0 39,4/−0,5), `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py valencia`, `work/app.py` (aus
   `tokio/index.html`; Texte in `sub.html`, `quellen.html`, `imgnote.html`), `tiles_rand.py valencia 2`.

## Ergebnis

↑ 59 m / ↓ 66 m mit 200-m-Fenster, ↑ 72 / ↓ 78 m mit 50 m, Rohdaten ↑ 137 m. Start 9,4 m (Pont de Montolivet),
höchster Punkt 26,0 m (Carrer del Nou d'Octubre, km 34,8), tiefster 1,6 m am Meer (Carrer de la Reina, km 20,7; ebenso um
km 3,5–4,7), Ziel 3,3 m. Vom Start 8 m hinunter zum Hafen, sanft hinauf nach Benimaclet (13 m, km 12,8), zurück ans Meer
zum Halbmarathon, dann stetig hinauf bis in den Westen und auf den letzten 7 km 23 m hinunter, zuletzt über eine Rampe
ins alte Flussbett. Steilste Stelle −2,0 % über 200 m auf dieser Rampe (km 41,8), bergauf höchstens +1,1 % (Passeig de
l'Albereda, km 26,0). Mit 4:00/km im Flachen ergibt das Modell 2:49:06 (das Profil kostet 20 s, bei 2:50:00 ebenso).
Der Plan des Veranstalters nennt 1,8 bis 18 m; MDT02 und WCS-5-m des IGN messen im Westen übereinstimmend 26 m.

Geprüft mit Playwright (393 × 852, Server auf Port 8772): keine Konsolenfehler, `APP_VERSION` 1.0, Service Worker
installiert (23 Dateien im Cache `vlc-marathon-profil`), Tipp auf die Version meldet „Version 1.0 ist aktuell“,
Kartenbilder laden, alle 17 Kartenstücke passen zu `D.tiles`.

## Offen

- Prüfung am iPhone.
- Die Google-Karte trägt noch „Edición 2025“, der Plan 2026 heißt „Provisional“. Wenn der Veranstalter die Karte für 2026
  umstellt (gleiche Adresse), `parse.py` und `vergleich.py` erneut laufen lassen.
- Termin 2027 (`2027-12-05?`) und Wellen 2027 beim Veranstalter prüfen, sobald veröffentlicht.
- Zielsteg geschätzt (Höhe des Uferwegs); Gegenprobe nur mit Fotos möglich.
