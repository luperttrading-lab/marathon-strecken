# Übergabe: Steigungsprofil Barcelona-Marathon

Stand 30.10.2026, App-Version **1.10** (1.10: im Ziel 42,195 statt 42,2 in Anzeige, Gesamtstrecke, Zwischenzeiten und Pace-Band; 1.9: Maßstab auf der Karte ohne Kasten, kleiner, in der freieren linken Ecke; 1.8: im Vollbild der Ort groß oben rechts statt am Pfeil, Maßstab auf der Karte; 1.7: Kopf mit Ort groß und „Streckenplan und Steigungsprofil“, Umschalter Karte | Zahlen statt Pünktchen, Karte zuerst, Name der Strecke im Vollbild; 1.6: zu breite Tabellen werden stufenweise enger statt rechts abgeschnitten; 1.5: Mauer-Beschriftung in einer freien Zeile über dem Profil, mittig über der Mauer, nur bei `D.mauer`; 1.4: Mauer-Beschriftung im Profil neben dem Gipfel statt darauf, nur bei `D.mauer`; 1.3: Mauer je Durchgang ein Rad mit Empfehlung nach Zielzeit, nur bei `D.mauer`; 1.2: Mauer-Zeit und Tor-Rechner für Strecken mit `D.mauer`, sonst unverändert; 1.1: Steigungskosten als große Zeile unter der Zielzeit; 1.0: erste Fassung).
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/barcelona/.

Die App ist eine Kopie der Tokio-App (Stand 1.24, aktueller gemeinsamer Code) mit eigenen Daten, Texten und
Speicherschlüsseln (`bcn-…`, Service-Worker-Cache `bcn-marathon-profil`, löscht nur Caches mit Präfix `bcn-`), ohne eigenes
Manifest und Symbol. Gegenüber `tokio/index.html` unterscheiden sich nur die streckenspezifischen Zeilen (wie bei Valencia).
Alle Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Änderungen
am gemeinsamen Code in allen Apps nachziehen (README). Startseite und README sind noch nicht angepasst.

## Termin und Start

Zurich Marató Barcelona am Sonntag, 14. März 2027 (Reglament 2027 des Veranstalters, Institut Barcelona Esports / RPM Sports,
Art. 1 und 3, https://zurichmaratobarcelona.es/soc-corredor-a/reglament/): Start 8:30 Uhr, Rollstühle 8:25, Zielschluss 6 h nach
dem Start des letzten Läufers, „etwa 16:15“; 37 000 Startplätze. `D.termine` `["2027-03-14"]` (bestätigt), `D.start` = 510,
`D.tz` Europe/Madrid, `D.ort` „Barcelona“ (nach der Zeitzone hieße es „Madrid“), `D.ortKurz` „ Barcelona“. Die Ausgabe 2026
lief am 15.03.2026.

**Start und Ziel sind nicht mehr an der Plaça d'Espanya:** Start im Passeig de Gràcia zwischen Casp und Gran Via (Startplan
„Mapa de sortida“ 15/03/2026; RFEA: „Paseo de Gracia junto a la Plaza de Cataluña“), Ziel im Passeig de Lluís Companys direkt
hinter dem Arc de Triomf (RFEA: „Paseo Lluis Companys, junto al Arco del Triunfo“). Der Montjuïc kommt nicht mehr vor.

**Startwellen** (`D.wellen`): die Wellen 2026 aus dem Startplan des Veranstalters („Mapa de sortida“, 15/03/2026), abgedruckt als
Anhang II der „Información Técnica“ der RFEA zur spanischen Meisterschaft
(https://www.rfeacontent.es/competi/calendario2026/IT_CtoESP_maraton_Barcelona.pdf, 10.03.2026). Farbe der Startnummer –
Einlass in den Block – Start – Zugläufer im Block: Schwarz (Elite), Weiß (Meisterschaft) und Gelb 7:45–8:25, 8:30, 2:45 / Rot
7:55–8:35, 8:40, 3:00 / Blau 8:05–8:45, 8:50, 3:15 / Rosa 8:15–8:55, 9:00, 3:30 / Hellblau 8:35–9:15, 9:20, 3:45 / Grün
8:55–9:35, 9:40, 4:00 / Grau und Lila 9:05–9:45, 9:50, 4:30 (nur Grau). Den Block wählt man bei der Anmeldung nach erwarteter Zielzeit,
Wechsel bis 1. Februar (Reglament Art. 5); Zeitgrenzen je Block sind nicht veröffentlicht. Für 2027 nennt die Seite
„Recorregut“ wieder gestaffelte Starts nach Tempo, die Zeiten noch nicht. Das Racebook 2026 mit Zeitplan
(`…/2026/03/RACEBOOK-ZMB26-5.pdf`) ist beim Veranstalter nicht mehr abrufbar (404). Eine Presseliste (archyde.com) nennt
dieselben Uhrzeiten.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Eine Linie zum Herunterladen gibt es nur angemeldet: „Descargar en .GPX“ auf der Seite Recorregut führt zu einer Strava-Route
(Anmeldung, nicht umgangen); der Google-Maps-Link dort zeigt nur einen Punkt (Treffpunkt am Start). Die Linie ist deshalb
nach dem Plan nachgezeichnet:

1. `plan.py`: **Streckenplan 2026** des Veranstalters, „6.5 Mapa Circuit (ZMB26)“, „Mapa del recorregut 15/03/2026“
   (https://zurichmaratobarcelona.es/wp-content/uploads/2026/06/6.5-Mapa-Circuit-ZMB26.pdf, Adobe Illustrator, auf der Seite
   Recorregut auch für 2027 verlinkt). Vektorgrafik auf einem maßstäblichen Stadtplan: Streckenlinie (Striche 0/0,2/0,63,
   15,93 pt, gestrichelt), 42 Kilometerkästchen (Ziffern nur als Umrisse), Start- und Zielzeichen, Schild „MITJA MARATÓ“, Tabelle
   der Getränkestellen. Linie in Laufrichtung verkettet → `plan2026.json` (Planpunkte in pt).
2. `osm.py`: OSM-Straßennetz (alle highway-Wege mit Knoten) im Rechteck 41,366–41,428° N, 2,146–2,234° O über den
   Overpass-Spiegel maps.mail.ru in 12 Stücken (overpass-api.de brach ab, kumi.systems antwortete nicht; der Spiegel brauchte
   mit 504-Wiederholungen gut 15 min) → `../dl/osm_netz.json` (43 903 Wege).
3. `netz.py`, `linie.py`: Plan affin auf die Erde (17 Kreuzungen benannter Straßen als Passpunkte, dann ICP auf die Linie:
   1,039 m/pt, um 44,8° gedreht), dann kürzeste Wege zwischen 47 Wegmarken (Ecken der Strecke). Kosten zusätzlich nach dem
   Abstand zum Planstück des jeweiligen Abschnitts (bis 35 m frei, darüber quadratisch); je Abschnitt, weil der Plan dieselbe
   Straße an anderer Stelle nutzt (Gran Via vor der Plaça de la Universitat zog sonst den Weg an). Einbahnstraßen zählen nicht
   (gesperrt; Ronda de Sant Pere und Aragó laufen gegen die Fahrtrichtung), ohne Ronda Litoral, Ronda de Dalt und ihre Rampen
   (in OSM trunk/trunk_link). → `gpx2026.json` (**43,13 km** auf dem Ellipsoid), `strassen.json`, `wegmarken.json`
   (Linienmeter und Planstelle je Wegmarke), `georef.json`. Plan gegen Linie: Median 7,5 m, 95 % 27 m; am weitesten (bis 63 m)
   an der Avinguda del Litoral bei Port Olímpic, wo der Plan ohne Straßen schematisch durch freie Fläche läuft (Linie auf der
   benannten Avinguda del Litoral am Strand; die Parkverbote des Ajuntament nennen dort „Litoral: costat mar“).
   **Wende auf der Diagonal:** Der Plan zeichnet die Linie nur bis zur Carrer de la Llacuna, beschriftet die Wende aber mit „c/ de
   la Ciutat de Granada“, zwei Blöcke weiter. Die Parkverbote des Ajuntament für den Lauf 2026 (Presse, z. B. NacióDigital
   14.03.2026) nennen „Diagonal (calçada muntanya) … fins a Ciutat de Granada“ und „Diagonal (calçada mar), des de Roc Boronat fins a
   Josep Pla“; auch die Abstände der Kilometerkästchen 31–36 passen nur so. Wende daher an der Ciutat de Granada (+540 m
   gegenüber der gezeichneten Linie). Kurze Verbindung „Carrer de Palència“ (Plan: „c/ Josep Estivill“) wie in OSM.
4. `marken.py`: die 42 Kästchen auf die Planlinie projiziert (auf der Diagonal stehen sie neben Hin- bzw. Rücklinie), die
   Planstelle über die Wegmarken in Linienmeter umgerechnet, Zuordnung zu km 1–42 per Viterbi (gleichmäßige Abstände, Abstand
   zur Planlinie). Gegenprobe `../dl/kontrolle_kaesten.png`: alle 42 Ziffern stimmen. → `marken.json`.
5. `common.py`: Die Linie ist 2,2 % zu lang (Straßenmitte statt Ideallinie an rund 45 Ecken mit abgeschrägten Eixample-Kreuzungen,
   Plätze, Wende); der maßstäbliche Plan ist ebenso lang. Die Kästchen stehen teils 150–300 m neben ihrer Stelle (Marke zu
   Marke 670–1290 Linienmeter). Daher keine Eichung Marke für Marke, sondern robust ausgleichend, stückweise linear mit Knoten
   alle 5 km Linie, Start und Ziel fest: Restabweichung der Kästchen Median 59 m, RMS 84 m, höchstens 210 m (km 35). **Kilometer
   auf etwa ±150 m.** Gegenproben: Einbiegen in die Diagonal bei km 30,6 (die Verpflegung „30,8“ steht im Plan dort), Wende
   bei km 33,2, Abzweig in die Llull bei km 35,3; die km-Beschreibung eines Läufer-Blogs (blogmaldito.com, aus eigener
   GPS-Aufzeichnung, inoffiziell) nennt 30,7 und 35,4. Halbmarathon damit in der Carrer de Floridablanca, das Schild
   „MITJA MARATÓ“ im Plan steht an der Ecke Rocafort.
6. `dgm.py`: **Geländemodell der Àrea Metropolitana de Barcelona, 25 cm, LiDAR 2022**, im „Servei WMS d'elevacions territorial“
   des ICGC (`geoserveis.icgc.cat/servei/catalunya/elevacions-territorial/wms`, Ebene
   `model-elevacions-terreny-amb-lidar-25cm-2022`, GetFeatureInfo je Punkt, ohne Anmeldung), alle 10 m, 4315 Punkte, 6 parallel,
   5 min. Höhen über dem Meer (Pegel Alicante). Lizenz CC BY 4.0 (ICGC). Den Dienst gibt es seit September 2026; der alte
   2-m-WMS „Elevacions, orientacions i ombres“ wird laut ICGC am 31.10.2026 abgeschaltet. GetMap liefert nur eingefärbte
   Bilder, keine Höhen; einen WCS bietet das ICGC nur für 5 m und 15 m.
   **Wahl** (`vergleich_dgm.py`, alle über GetFeatureInfo entlang der Linie, ohne Brücken): Das ICGC bietet ohne Anmeldung drei
   Laser-Geländemodelle, die neuer und feiner sind als das MDT02 des IGN (Valencia; PNOA-LiDAR, zweite Abdeckung, in Katalonien
   ab 2016 beflogen, 2-m-Raster): Katalonien 1 m und 50 cm (Befliegung 2021–2023) und AMB 25 cm (2022). Alle liegen auf
   Zentimeter beieinander: ICGC 50 cm gegen AMB 25 cm Median −2 cm, Streuung 5 cm (95 % unter 10 cm), ICGC 1 m ebenso, IGN
   MDT02 Median −12 cm, Streuung 7 cm (95 % unter 20 cm; nur in der Marina vor der Plaça dels Voluntaris, km 26,8–26,9, bis
   1,7 m tiefer und unruhig). Genommen AMB 25 cm: feinstes Raster und von Punkt zu Punkt am ruhigsten (mittlere |2. Differenz|
   je 10 m 4,4 cm gegen 5,1–5,9 cm bei den anderen), dazu das Oberflächenmodell derselben Befliegung für die Brückendecks. Die
   Wahl ändert das Profil kaum (Rohdaten bergauf auf denselben Stücken 141 m gegen 146–149 m).
7. `dsm.py`: Oberflächenmodell AMB 25 cm 2022 (`model-superficies-amb-lidar-25cm-2022`) auf den OSM-Brücken ±60 m →
   `../dl/dsm_bruecken.json`.
8. `orte.py`: **Barri** alle 100 m über die Rückwärtssuche von Nominatim (zoom 17, „quarter“; dazu der Districte als
   „suburb“), wegen vieler 429 langsam, Rohantworten `../dl/nominatim/`. Die Flächen der Stadt (Open Data BCN, „Unitats
   administratives“) gaben aus dieser Umgebung 403. Barris statt Districtes, weil l'Eixample allein knapp 21 km der Strecke deckt
   und Sant Martí 17 km; die 73 Barris teilen sie in Stücke von 0,5–3,5 km mit bekannten Namen (La Sagrada Família, El Fort
   Pienc, Sant Antoni, El Poblenou …). `namen.py`: Straßen wie in OSM unter `name` (katalanisch), Zusatz „(lateral mar)“ usw. der
   Seitenfahrbahnen entfällt; Barri am Zeilenanfang mit großem Artikel („La Dreta de l'Eixample“).
9. `clean.py`: Brücken aus OSM (bridge=yes auf der Linie), nur wo das Geländemodell innen (Median über 30 m) mehr als 1,0 m unter
   der Geraden zwischen den Rampen liegt. Dort gilt das Oberflächenmodell (Median über 30 m gegen Autos und Geländer), wenn es an
   beiden Enden höchstens 0,5 m neben dem Geländemodell liegt – an allen drei der Fall: **Carrer de València** über die Bahn am
   Clot (km 9,71–9,85, Geländemodell 2 Punkte im Einschnitt, 13,7 m), **Pont de Bac de Roda** (Calatrava, km 10,10–10,29,
   Geländemodell bis 9,7 m im Bahneinschnitt; das Deck ist gewölbt, 16,4 → 21,4 → 17,3 m, das IGN-MDT02 misst es ebenso) und
   **Carrer de Josep Pla** über den Trog der Ronda Litoral (km 29,77–29,83, Geländemodell 2,2 m, Deck flach 8,3 m). In der App
   gestrichelt wie geschätzte Brücken. Keine Tunnel; übrige Stufen > 1,5 m je 10 m: keine. Gemessen bleibt der Buckel am Kreisel
   am Anfang der Meridiana (km 40,4): Die Straße steigt glatt um 5 m und fällt wieder, alle vier Modelle messen das gleich.
10. `build.py`: Höhen in cm im 10-m-Raster, Median über 30 m; Straßenstücke unter 80 m und Barris unter 300 m dem Vorgänger
    zugeschlagen. Marken: Getränke und Verpflegung laut Tabelle im Plan 2026 an ihrer Kilometerangabe (alle mit WC und
    Sanität): Getränke km 5 / 7,5 / 10 / 22,5 / 32,5 (Wasser, Iso; 32,5 dazu Physio), km 12,5 / 17,5 / 27,5 / 37,5 (Wasser und
    Iso in Flaschen, Gel); Verpflegung km 15 (Bananen, Nüsse), 20 (dazu Trauben, persönliche Mehrwegflaschen), 25, 30,8, 35, 40
    (Cola, Obst, Nüsse, Fruchtgummi; ab 30,8 Kühlstation, 35 persönliche Mehrwegflaschen). Das Reglament 2027 nennt dieselben
    Kilometer „aproximadament“ (km 30 statt 30,8). Halbmarathon bei 21 098 m.
    `route.py` (lat0/lon0 41,35/2,15), `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py barcelona`, `barcelona/work/app.py`
    (aus `tokio/index.html`; Texte in `sub.html`, `quellen.html`, `strassennamen.html`, `imgnote.html`),
    `tiles_rand.py barcelona 2`.

## Ergebnis

↑ 102 m / ↓ 113 m mit 200-m-Fenster, ↑ 129 / ↓ 140 m mit 50 m, ↑ 60 / ↓ 71 m mit 1 km, Rohdaten ↑ 169 m. Start 21,1 m
(Passeig de Gràcia), höchster Punkt 35,3 m (Carrer de Mallorca am Passeig de Gràcia, km 15,5), tiefster 2,6 m (Carrer de
Llull, Poblenou, km 36,6), Ziel 11,0 m (Arc de Triomf). Die ersten 19 km laufen durch die Eixample auf und ab (Marina 8 m
hinauf, Aragó bis 30 m, Mulde an der Comte d'Urgell 23,6 m, València bis 32,8 m, hinunter zum Clot 14,3 m, Pont de Bac de Roda
21,4 m, Meridiana 29,6 m, Mallorca bis 35,3 m, Gran Via 18,3 m), dann über Sant Antoni und den Paral·lel 20 m hinunter zum
Hafen; km 23,5–40 bleibt die Strecke zwischen 2,6 und 9,4 m. Zum Schluss über den Kreisel an der Meridiana und die Ausiàs Marc
auf 16,4 m (km 41,7) und 5 m hinunter ins Ziel. Steilste Stelle +3,7 % über 200 m (Marina, km 1,8), bergab −2,2 % (km 40,5);
mit 50 m +7,2 % auf der Rampe des Pont de Bac de Roda. Mit 4:00/km im Flachen ergibt das Modell 2:49:37 (das Profil kostet 50 s,
bei 2:50:00 ebenso). Ein Höhenprofil veröffentlicht der Veranstalter nicht (weder im Plan 2026 noch auf der Seite Recorregut;
das Racebook 2026 ist weg); er nennt die Strecke „planer i ràpid“, die RFEA „un perfil favorable“.

Geprüft mit Playwright (393 × 852, Faktor 2, Server auf Port 8775): keine Konsolenfehler, `APP_VERSION` 1.0, Service Worker
installiert (26 Dateien im Cache `bcn-marathon-profil`), Tipp auf die Version meldet „Version 1.0 ist aktuell“, Kartenbilder
laden (auch Übersicht z11), alle 20 Kartenstücke passen zu `D.tiles` und `sw.js`. `grep -i "tokio|tokyo|tyo-|tyo\.|GSI|valencia"`
in `barcelona/index.html` und `sw.js`: keine Treffer; Unterschiede zu `tokio/index.html` nur in den streckenspezifischen Zeilen.

## Offen

- Prüfung am iPhone; Karte auf der Startseite, Eintrag im README.
- Kurs 2027: Die Seite Recorregut zeigt noch den Plan 2026. Wenn ein neuer Plan erscheint (oder die Strava-Route ohne
  Anmeldung erreichbar wird), `plan.py` bis `marken.py` neu laufen lassen und die Wende auf der Diagonal prüfen.
- Startwellen 2027 nachtragen, sobald veröffentlicht (`D.wellen`, gerade die Zeiten 2026).
- Kilometer nur auf etwa ±150 m (Kästchen des Plans); Linie an der Avinguda del Litoral bei Port Olímpic bis 63 m neben dem
  schematischen Plan (Höhe dort 5–9 m, ohne Einfluss auf das Profil).
