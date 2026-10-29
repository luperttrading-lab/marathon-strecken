# Übergabe: Steigungsprofil Paris-Marathon (Kurs 2025)

Stand 28.10.2026, App-Version **1.24** (1.24: Pace im Flachen mit zwei Nachkommastellen; 1.23: weißer Punkt im Pace-Diagramm ist der Flachpunkt 0 % mit Flach-Pace statt der aktuellen Stelle; 1.22: Markierung im Pace-Diagramm stufenlos und ohne Wackeln, Tippen daneben nimmt sie weg, Punkt „hier“ mit km; 1.21: Markierung im Pace-Diagramm auch waagerecht zur Pace-Achse; 1.20: Pace-Diagramm ohne Laborlinie und graue Zone, −15 bis +10 %, Achse bei 0 %, Markierung zum Antippen; 1.19: Bergab fest „halb“ ohne Schalter, steiler als −8 % kein weiterer Gewinn statt U-Kurve; 1.18: flacher Halbmarathon in der Tabelle ohne Höhenmeter, Erklärung im Info-Fenster (i); 1.17: Kosten je Höhenmeter bei 4:00 /km mit wählbarer Bezugs-Pace, Bahnzeiten als Tabelle, größere Überschriften in den Einstellungen; 1.16: unter der Zielzeit flacher Marathon und Bahnzeiten 10 000 m / 5000 m; 1.15: Zeiten immer mit 100 m, „Pace hier“ über das Messfenster gemittelt; 1.14: Messfenster 50 / 100 / 200 m / 1 km statt 10 m, neuer Erklärtext; 1.13: Zwischenzeiten mit Halbmarathon-Zeile und „je 10 km“; 1.12: Knopfrahmen so hell wie die Räder, „Vollbild“ blau, im Vollbild führt ‹ zurück in die normale Ansicht; 1.11: Kopf eines offenen Abschnitts bleibt oben stehen, Zuklappen von überall; 1.10: beim Aufklappen bleibt der Kopf des Abschnitts an seiner Stelle; 1.9: Hinweis, wenn die eingestellte Startzeit zu keiner Welle passt; 1.8: Standard 5 km Ausschnitt und Tempo ×200, Menü-Knopf blau mit Beschriftung, Abschnitte unter dem Läuferblick aufklappbar; 1.7: Hinweis: Startzeiten 2027 noch offen unter „Deine Startzeit“; 1.6: Pfeile in Bisher/Noch/Ganze Strecke und Rampe als Grafik, dreistellige Werte ohne „…“, zu breite Werte werden kleiner; 1.5: Bergab U-Kurve statt Grenze bei −4 %: am schnellsten bei −8 %, ab −16 % langsamer als flach, ohne Knick bei 0 %; 1.4: Tempo-Rad mit ×1 (Echtzeit), ×50 und ×100–×180 in 20er-Schritten; 1.3: Brücken-Beschriftungen überlappen nicht mehr; 1.2: Linie repariert, die Schleife um die Opéra Garnier fehlte; Kurs 2026 verglichen; 1.1: Kästchen bunt/grau neben der Gesamtstrecke, Diagramm „So rechnet das Pace-Modell“; 1.0: Erstausgabe), live unter https://luperttrading-lab.github.io/marathon-strecken/paris/.

Die App ist eine Kopie der Boston-App (Stand 1.0) mit eigenen Daten, Texten und Speicherschlüsseln (`par-…`), ohne eigenes
Manifest und Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in
[`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Änderungen am gemeinsamen Code in allen Apps nachziehen (README).

**Warum Kurs 2025:** Ab 2027 richtet Cadence Running United den Lauf aus (bis 2026 ASO), als „ASICS Marathon de Paris“,
50. Ausgabe am Sonntag, 4. April 2027 (`D.termine`). Die neue Strecke wird erst Anfang 2027 vorgestellt und soll sich künftig
jedes Jahr ändern. Die Website der ASO ist abgeschaltet. Gezeigt wird deshalb der Kurs 2025 (13. April 2025) zum Vergleich und
Nachschauen; der Kurs 2024 war zu 92 % gleich (Abweichungen km 8,4–10,2, 11,8–12,2 und 24,7–25,9; 2024 wegen Hochwasser oben
auf den Quais statt durch den Tunnel des Tuileries). Start 2025 um 8:00 Uhr (Elite und vordere Startblöcke, runpack.fr),
`D.start` = 480. `D.tz` Europe/Paris, `D.ortKurz` „ Paris“. Hinweis-Kasten auf der Startseite (seit 1.18).

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

1. **Strecke:** GPX von goandrace.com (`../dl/paris2025_goandrace.gpx`, in Garmin Connect gezeichnet, 1044 Punkte, 42,92 km,
   Lücken bis 1 km; daneben `paris2024_goandrace.gpx` und `paris2026_goandrace.gpx`). `match.py [GPX]` legt sie auf das
   OSM-Straßennetz (`../dl/osm_wege.json` plus `osm_wege_sued.json` für den Süden des Bois de Vincennes, Overpass maps.mail.ru):
   kürzester Weg von Anker zu Anker (alle 500 m ein Knoten höchstens 15 m neben der Linie, lieber auf der Fahrbahn), Kante kostet
   Länge × (1 + (Abstand / 20 m)²), Fuß- und Radwege das Dreifache, Périphérique gesperrt. Pflichtpunkte an beiden Enden der
   fünf Tunnel unten an der Seine (`ZWANG`; Linie und Straße darüber liegen in der Karte übereinander). Danach Hin-und-zurück-Stücke
   und kurze Schleifen entfernt und **Gegenprobe** Linie gegen Weg: wo die Linie mehr als 40 m abliegt, kommt dort ein Anker dazu
   (seit 1.2: in 1.0/1.1 fehlte die Schleife um die Opéra Garnier, 600 m, weil ein Anker auf einem Fußweg-Stummel lag und das
   Entfernen der Hin-und-zurück-Stücke die ganze Schleife herausschnitt). Linie 43,087 km (2,1 % länger als vermessen),
   `common.py` staucht gleichmäßig auf 42 195 m. Kanten mit Name, Tunnel, Brücke → `../dl/kanten.json`.
   **Kurs 2026** (`match.py ../dl/paris2026_goandrace.gpx`, 42,528 km): gleich bis auf km 24,8–25,8, 2026 von der Bastille über
   Boulevard Henri IV, Rue Jacques Cœur, Rue de l'Arsenal, Rue Mornay und Rue de Sully zum Quai des Célestins statt über Boulevard
   Bourdon und Quai Henri IV. Der Nutzer wollte 2026 nur bei gleicher Strecke, deshalb bleibt die App beim Kurs 2025.
2. `dgm.py`: **RGE ALTI 1 m der IGN** (NGF-IGN69, Licence Ouverte) über den Höhendienst der Géoplateforme, nur per GET
   (`elevation.json?lon=a|b&lat=…&resource=ign_rge_alti_wld&zonly=true`, je 100 Punkte; POST meldet „unexpected error“).
3. `clean.py`: Tunnel nach OSM (wo das Modell innen mehr als 1,2 m von der Geraden abweicht), übrige Stufen paarweise wie bei
   den anderen Strecken, Rampe vom Quai Henri IV ans Ufer (Linienmeter 25 860) über 120 m geglättet. Geschätzt (gestrichelt): Tunnel des
   Tuileries, Tunnel unter der Place de la Concorde, der Place du Canada (Pont Alexandre III), der Place de l'Alma, Unterführung
   Place de Varsovie (Pont d'Iéna); Brücken Rue de Picpus über die Coulée verte, Avenue de Gravelle über den Périphérique,
   Rue de Charenton und Boulevard Exelmans über Einschnitte. Die kurzen Durchfahrten unter den Brücken im Parc Rives de Seine misst das Modell
   richtig. Nach dem Tunnel des Tuileries steigt die Strecke laut Modell auf Quai-Höhe (33–34 m, Querschnitte geprüft).
4. `orte.py`: Arrondissement bzw. Gemeinde aus ADMIN EXPRESS der IGN (WFS `data.geopf.fr/wfs`, Layer
   `arrondissement_municipal` und `commune`, `../dl/*.geojson`). Nominatim drosselte die 280 Abfragen (HTTP 429).
5. `build.py`: Straßennamen aus den OSM-Kanten unter der Linie (Nominatim griff oft Gehweg oder Quai daneben), Stücke unter
   80 m dem Vorgänger zugeschlagen, Orte unter 600 m ebenso und auf den nächsten Straßenwechsel gelegt; Namen der Tunnel und
   Brücken nach dem, was darüber bzw. darunter liegt (`NAMEN`). Verpflegung alle 5 km (Wasser, Iso, Bananen, Trockenobst laut
   runpack.fr), Lage nach Kilometer, nicht nach Plan des Veranstalters.
6. `route.py` (lat0/lon0 48,8/2,2), `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py paris`, `work/app.py` (aus
   `boston/index.html`), `tiles_rand.py paris 2`.

## Ergebnis

↑ 157 m / ↓ 147 m mit 200-m-Fenster, ↑ 184 / ↓ 174 m mit 50 m, Rohdaten ↑ 271 m. Start 34,4 m (Champs-Élysées), höchster
Punkt 67,5 m (Bois de Vincennes, Plateau de Gravelle, km 16,7), tiefster 27,8 m (an der Seine, km 29,6), Ziel 45,1 m
(Avenue Foch). Steilste Stellen über 200 m: +3,5 % im Bois de Boulogne (km 36,3), −3,7 % auf der Rue de Charenton (km 21,4).
Mit 4:00/km im Flachen ergibt das Modell 2:50:19 (Profil kostet 1:32 min).

## Offen

- Prüfung am iPhone.
- Strecke 2027 einbauen, sobald Cadence Running United sie vorstellt (Anfang 2027); dann Hinweis-Kasten der Startseite anpassen.
  Den Kurs 2025 als eigene Ansicht behalten, falls gewünscht.
- Verpflegungsstellen nach Plan des Veranstalters statt nach Kilometer; Startzeit 2027.
