# Übergabe: Steigungsprofil Berlin-Marathon

Stand 27.10.2026, App-Version **1.6** (seit 1.4 ohne eigenes Manifest und Symbol, siehe README; 1.5 Pace im Läuferblick; 1.6 Start bei km 0, Knopf zum Start), live unter https://luperttrading-lab.github.io/marathon-strecken/berlin/.

Die App ist eine Kopie der Hamburg-App (Stand 1.12) mit eigenen Daten, Texten und Speicherschlüsseln (`bln-…`).
Alle Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md) und gelten
hier genauso. Änderungen am gemeinsamen Code in allen Apps nachziehen (siehe README im Hauptordner).

Das Rennen heißt ab 2027 **GENERALI BERLIN-MARATHON** (vorher BMW BERLIN-MARATHON). Die offizielle Karte zeigt laut
Veranstalter noch den Kurs 2026; die App trägt deshalb „BMW Berlin-Marathon · Kurs 2026“.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

1. `../dl/karte.json`: GeoJSON der offiziellen Karte (Seite generali-berlin-marathon.com/das-rennen/strecken bettet
   `maps.scc-events.com/maps/0190fe72-54d1-7103-88d9-219da00683be` ein, Daten unter `/api/maps/<id>`). Ebene 130
   „Strecke Läufer:innen“: Linie „Ideallinie“ (506 Punkte, 42,29 km, also 0,2 % zu lang), 42 KM-Punkte, Ziellinie,
   6 Verpflegungspunkte (km 9, 15, 20, 25, 30, 36), 9 Erfrischungen (km 5, 12, 17,5, 22,5, 27,5, 32,5, 34,5, 38, 40).
   Eine Startmarke gibt es nicht; die Linie beginnt an der Startlinie. Eine Staffel gibt es in Berlin nicht, die
   Einstellung „Staffelwechsel im Profil“ ist ausgeblendet.
2. `parse.py` → `gpx2026.json` und `../dl/locations.json`; `proj.py` → `kmproj.json`; `common.py` eicht stückweise linear.
3. `dgm.py`: **DGM1 Berlin** über WMS-GetFeatureInfo (`gdi.berlin.de/services/wms/dgm1`, Ebene `c_dgm1`, JSON-Feld
   `Höhe_in_Meter_über_NHN`), alle 10 m, 8 parallel, ~7 min. GetMap liefert nur ein eingefärbtes Bild, keine Höhen.
4. `streets.py` (Nominatim alle 150 m), `clean.py` (wie Frankfurt, ohne Festhallen-Regel), `build.py` (Brückennamen:
   Kronprinzenbrücke, Michaelbrücke, Kottbusser Brücke statt der Straßen, die Nominatim nennt), `route.py`, `tiles.py`.
5. `app.py`: hat aus `hamburg/index.html` die Erstausgabe von `berlin/` gebaut (Symbol auf Tannengrün, seit 1.4 nicht mehr verwendet). **Nur historisch.**

## Ergebnis und Abgleich

7 Brücken (Franklinstraße, Gotzkowskybrücke, Moltkebrücke, Kronprinzenbrücke, Michaelbrücke, Kottbusser Brücke,
Hohenzollerndamm) und 1 Unterführung (Hauptstraße, Schöneberg). Tiefster Punkt 32,0 m (Franklinstraße, km 3,3), höchster
53,6 m (Lentzeallee, Schmargendorf, km 27,8): 21,6 m Unterschied. ↑ 70 m mit 200-m-Fenster, Rohdaten ↑ 156 m. Steilste Stelle
über 200 m: 2,5 % an der Kronprinzenbrücke (km 7,0). Der Veranstalter nennt keine Zahl („flachste der World Marathon Majors“).

## Offen

- Prüfung am iPhone (Flugmodus, Tipp auf „v1.0“).
- Kurs 2027 (GENERALI BERLIN-MARATHON) noch nicht veröffentlicht.
