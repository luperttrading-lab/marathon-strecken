# Übergabe: Steigungsprofil Paris-Marathon (Kurs 2025)

Stand 28.10.2026, App-Version **1.1** (1.1: Kästchen bunt/grau neben der Gesamtstrecke, Diagramm „So rechnet das Pace-Modell“; 1.0: Erstausgabe), live unter https://luperttrading-lab.github.io/marathon-strecken/paris/.

Die App ist eine Kopie der Boston-App (Stand 1.0) mit eigenen Daten, Texten und Speicherschlüsseln (`par-…`), ohne eigenes
Manifest und Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in
[`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Änderungen am gemeinsamen Code in allen Apps nachziehen (README).

**Warum Kurs 2025:** Ab 2027 richtet Cadence Running United den Lauf aus (bis 2026 ASO), als „ASICS Marathon de Paris“,
50. Ausgabe am Sonntag, 4. April 2027 (`D.termine`). Die neue Strecke wird erst Anfang 2027 vorgestellt und soll sich künftig
jedes Jahr ändern. Die Website der ASO ist abgeschaltet. Gezeigt wird deshalb der Kurs 2025 (13. April 2025) zum Vergleich und
Nachschauen; der Kurs 2024 war zu 92 % gleich, 2026 (12. April) laut Streckenbeschreibungen derselbe (Abweichungen km 8,4–10,2, 11,8–12,2 und 24,7–25,9; 2024 wegen Hochwasser oben
auf den Quais statt durch den Tunnel des Tuileries). Start 2025 um 8:00 Uhr (Elite und vordere Startblöcke, runpack.fr),
`D.start` = 480. `D.tz` Europe/Paris, `D.ortKurz` „ Paris“. Hinweis-Kasten auf der Startseite (seit 1.18).

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

1. **Strecke:** GPX von goandrace.com (`../dl/paris2025_goandrace.gpx`, in Garmin Connect gezeichnet, 1044 Punkte, Lücken bis
   1 km; daneben `paris2024_goandrace.gpx`). `match.py` legt sie auf das OSM-Straßennetz (`../dl/osm_wege.json` plus
   `osm_wege_sued.json` für den Süden des Bois de Vincennes, Overpass maps.mail.ru): kürzester Weg von Anker zu Anker (alle 500 m
   ein Knoten höchstens 15 m neben der Linie), Kante kostet Länge × (1 + (Abstand / 20 m)²), Fuß- und Radwege das Dreifache,
   Périphérique gesperrt. Pflichtpunkte an beiden Enden des Tunnels des Tuileries (OSM-Weg 4294224, `ZWANG`), Anker dazwischen
   entfallen: Linie und Quai darüber liegen in der Karte übereinander, ohne Pflichtpunkte stieg die Linie am Louvre auf den Quai.
   Danach Hin-und-zurück-Stücke und kurze Schleifen entfernt. Linie 42,421 km (0,5 % länger als vermessen), `common.py` staucht
   gleichmäßig auf 42 195 m (Kilometermarken mit Lage gibt es nicht). Kanten mit Name, Tunnel, Brücke → `../dl/kanten.json`.
2. `dgm.py`: **RGE ALTI 1 m der IGN** (NGF-IGN69, Licence Ouverte) über den Höhendienst der Géoplateforme, nur per GET
   (`elevation.json?lon=a|b&lat=…&resource=ign_rge_alti_wld&zonly=true`, je 100 Punkte; POST meldet „unexpected error“).
3. `clean.py`: Tunnel nach OSM (wo das Modell innen mehr als 1,2 m von der Geraden abweicht), übrige Stufen paarweise wie bei
   den anderen Strecken, Rampe vom Quai Henri IV ans Ufer (km 25,1) über 120 m geglättet. Geschätzt (gestrichelt): Tunnel des
   Tuileries, Tunnel unter der Place de la Concorde, der Place du Canada (Pont Alexandre III), der Place de l'Alma, Unterführung
   Place de Varsovie (Pont d'Iéna); Brücken Rue de Picpus über die Coulée verte, Avenue de Gravelle über den Périphérique,
   Rue de Charenton über einen Einschnitt. Die kurzen Durchfahrten unter den Brücken im Parc Rives de Seine misst das Modell
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

↑ 152 m / ↓ 141 m mit 200-m-Fenster, ↑ 177 / ↓ 166 m mit 50 m, Rohdaten ↑ 262 m. Start 34,5 m (Champs-Élysées), höchster
Punkt 67,5 m (Bois de Vincennes, Plateau de Gravelle, km 16,3), tiefster 28,5 m (an der Seine, km 29,4), Ziel 45,1 m
(Avenue Foch). Steilste Stellen über 200 m: +3,5 % im Bois de Boulogne (km 36,2), −3,6 % auf der Rue de Charenton (km 21,1).
Mit 4:00/km im Flachen ergibt das Modell 2:50:16 (Profil kostet 1:29 min).

## Offen

- Prüfung am iPhone.
- Strecke 2027 einbauen, sobald Cadence Running United sie vorstellt (Anfang 2027); dann Hinweis-Kasten der Startseite anpassen.
  Den Kurs 2025 als eigene Ansicht behalten, falls gewünscht.
- Verpflegungsstellen nach Plan des Veranstalters statt nach Kilometer; Startzeit 2027.
