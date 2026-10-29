# Übergabe: Steigungsprofil Tokio-Marathon

Stand 28.10.2026, App-Version **1.16** (1.16: Bergab fest „halb“ ohne Schalter, steiler als −8 % kein weiterer Gewinn statt U-Kurve; 1.15: flacher Halbmarathon in der Tabelle ohne Höhenmeter, Erklärung im Info-Fenster (i); 1.14: Kosten je Höhenmeter bei 4:00 /km mit wählbarer Bezugs-Pace, Bahnzeiten als Tabelle, größere Überschriften in den Einstellungen; 1.13: unter der Zielzeit flacher Marathon und Bahnzeiten 10 000 m / 5000 m; 1.12: Zeiten immer mit 100 m, „Pace hier“ über das Messfenster gemittelt; 1.11: Messfenster 50 / 100 / 200 m / 1 km statt 10 m, neuer Erklärtext; 1.10: Zwischenzeiten mit Halbmarathon-Zeile und „je 10 km“; 1.9: Knopfrahmen so hell wie die Räder, „Vollbild“ blau, im Vollbild führt ‹ zurück in die normale Ansicht; 1.8: Kopf eines offenen Abschnitts bleibt oben stehen, Zuklappen von überall; 1.7: beim Aufklappen bleibt der Kopf des Abschnitts an seiner Stelle; 1.6: Hinweis, wenn die eingestellte Startzeit zu keiner Welle passt; 1.5: Standard 5 km Ausschnitt und Tempo ×200, Menü-Knopf blau mit Beschriftung, Abschnitte unter dem Läuferblick aufklappbar; 1.4: Hinweis: ein gemeinsamer Start unter „Deine Startzeit“; 1.3: Pfeile in Bisher/Noch/Ganze Strecke und Rampe als Grafik, dreistellige Werte ohne „…“, zu breite Werte werden kleiner; 1.2: Bergab U-Kurve statt Grenze bei −4 %: am schnellsten bei −8 %, ab −16 % langsamer als flach, ohne Knick bei 0 %; 1.1: Tempo-Rad mit ×1 (Echtzeit), ×50 und ×100–×180 in 20er-Schritten; 1.0: Erstausgabe), live unter https://luperttrading-lab.github.io/marathon-strecken/tokio/.

Die App ist eine Kopie der Boston-App (Stand 1.1) mit eigenen Daten, Texten und Speicherschlüsseln (`tyo-…`), ohne eigenes
Manifest und Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in
[`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Änderungen am gemeinsamen Code in allen Apps nachziehen (README).

20. Tokyo Marathon am Sonntag, 7. März 2027 (Tokyo Marathon Foundation). Start der Läufer 9:10 Uhr laut Zeitplan des
Veranstalters (Rollstühle 9:05), `D.start` = 550, `D.tz` Asia/Tokyo, `D.ort` „Tokio“ (sonst hieße es nach der Zeitzone
„Tokyo“), `D.ortKurz` „ Tokio“. Vom Rathaus (Tokyo Metropolitan Government) in Shinjuku zur Gyōkō-dōri vor dem Bahnhof Tokio.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

1. **Strecke** aus der Google-Karte des Veranstalters, eingebettet auf https://www.marathon.tokyo/en/about/course/ (Seite für
   2027, Karte „Tokyo Marathon 2026“), als KML: `https://www.google.com/maps/d/kml?mid=1jGYjkrF_m5K3rWgYJu1XqyMbjHPq2pQ&forcekml=1`
   (`../dl/karte_….kml`). Linie in zwei Stücken rückwärts (Ziel → Wendepunkt Ueno-hirokoji → Start), dazu Start, Ziel,
   42 Kilometermarken, Halbmarathon, 15 Getränkestellen (給水所), Kontrollpunkte, Sanität, Toiletten. `parse.py` dreht und setzt
   zusammen, schneidet an Start und Ziel (Linie 42,255 km Haversine), projiziert die Marken auf die Linie. Die Strecke läuft an
   den Wendepunkten auf derselben Straße zurück: Liegen mehrere Stellen höchstens 15 m neben einer Marke, gilt die, die der
   erwarteten am nächsten ist (km 24 lag sonst auf der Hinwegseite am Tomioka Hachimangū). → `gpx2026.json`, `marken.json`.
2. `common.py`: Kilometer stückweise linear über die 42 Marken (Marke zu Marke 989–1013 Linienmeter).
3. `dgm.py`: **GSI-Höhenmodell** (国土地理院, 地理院タイル) als PNG-Kacheln z15: DEM5A (Laser, 5 m), wo es fehlt DEM5B, sonst
   DEM10B (85 von 4227 Punkten, auf Brücken); Höhe = (R·65536 + G·256 + B)·0,01 m, bilinear, alle 10 m. Höhen über T.P.
4. `osm.py`: OSM-Wege im Umkreis von 40 m um die Linie (Overpass maps.mail.ru). `streets.py`: je 10 m der nächste Weg
   höchstens 20 m daneben, Hauptstraßen bevorzugt, ohne Autobahnen (Shuto-Expressway über vielen Strecken-Straßen) und ohne
   Unterführungen (Hibiya). `namen.py`: japanische Namen in Umschrift (Hepburn mit Längenstrich, „-dōri“); die englischen Namen
   in OSM sind uneinheitlich. Unbekannte Namen (kurze Querstraßen) übernehmen den Namen davor.
5. `orte.py`: Bezirk (区) alle 100 m über den Adressdienst der GSI (`mreversegeocoder.gsi.go.jp`, Gemeindeschlüssel → Shinjuku,
   Chiyoda, Bunkyō, Taitō, Chūō, Sumida, Kōtō, Minato).
6. `clean.py`: zuerst die Brücken aus OSM (bridge=yes auf der Linie, je Durchgang ein Stück, Enden oben auf den Rampen; nur wo
   das Modell innen mehr als 0,5 m unter der Geraden liegt). Die Kanalbrücken in Kōtō (Takahashi, Umibe-bashi) sind gewölbt: ihre
   Rampen misst das Modell richtig, nur die Fahrbahn fehlt; die reine Stufensuche hatte dort die Rampe statt der Senke
   geglättet. Geschätzt: Mansei-bashi, Nihonbashi, Kayaba-bashi, Asakusa-bashi, Kuramae-bashi (Sumida, 190 m), Takahashi,
   Umibe-bashi, Shibazono-bashi, jeweils auf Hin- und Rückweg, und zwei Stücke der oberen Straßenebene in Nishi-Shinjuku
   (Gijidō-dōri über Querstraßen, das Modell misst dort 7 m tiefer).
7. `build.py` (Bezirke unter 300 m dem Vorgänger zugeschlagen), `route.py` (lat0/lon0 35,6/139,6), `tiles.py`, dann aus
   `werkzeuge/`: `tiles_z11.py tokio`, `work/app.py` (aus `boston/index.html`), `tiles_rand.py tokio 2`.

## Ergebnis

↑ 60 m / ↓ 97 m mit 200-m-Fenster, ↑ 91 / ↓ 129 m mit 50 m, Rohdaten ↑ 177 m. Start 40,6 m, höchster Punkt 41,1 m (km 0,25),
tiefster 0,2 m (Monzen-nakachō, km 23,9), Ziel 2,9 m. Bis km 7 geht es 37 m hinunter, danach Flachland; Buckel sind nur die
Brückenrampen. Steilste Stelle −4,2 % über 200 m auf der Yasukuni-dōri (km 3,1). Mit 4:00/km im Flachen ergibt das Modell
2:49:00 (das Profil bringt 13 s).

## Offen

- Prüfung am iPhone.
- Getränkestellen: nur die 15 der Karte (給水所); was es dort gibt (Wasser, Sportgetränk, Essen), ist nicht eingetragen.
- Für 2027 die Karte erneut abrufen, sobald der Veranstalter sie aktualisiert (gleiche Adresse).
