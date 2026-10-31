# Vorgemerkt

Ideen und offene Punkte, die besprochen, aber noch nicht gebaut sind. Stand 30.10.2026.

## Ideen (mit dem Nutzer besprochen, Reihenfolge offen)

- ~~Alle Strecken offline ohne Karten~~ – erledigt 31.10.2026 als Marathon 2.3 (Karten aller Strecken per Knopf mit
  Rückfrage und Datenmenge, Hinweis im Kartenfeld; [`kern/AENDERUNGEN.md`](kern/AENDERUNGEN.md)).
- **Halbmarathons** (interAir bietet 8 an: Lissabon, Paris, New York, Prag, Berlin, Brooklyn, Kopenhagen, Cardiff):
  **vorerst nicht** (Nutzer 31.10.2026: „ein ganz anderes Projekt“). Der Kern hat 42,2 km an mehreren Stellen fest
  (Zielkarte, Achse, Schieber, 5-km-Tabelle); vorher müsste er alles aus der Streckenlänge rechnen.
- **Startseite „Deine Form auf allen Strecken“:** eine Zeit auf flacher Strecke eingeben, für jede Strecke die gleichwertige
  Zeit sehen (hilft bei der Wahl einer Reise). Das Modell dafür ist seit 30.10.2026 an echten Zwischenzeiten geprüft
  (`werkzeuge/eichung/`).
- ~~**Gemeinsamer Kern statt 24 Kopien**~~ – erledigt 30.10.2026 als Marathon 2.0: Erzeuger `werkzeuge/kern/kern.py` mit
  Hamburg als Vorlage, eine Versionsnummer für die ganze App, „ist geladen“ einmal statt je Strecke
  ([`kern/AENDERUNGEN.md`](kern/AENDERUNGEN.md)). Im Browser blieb alles wie vorher, der Service Worker ist unverändert. Der
  Staffel-Schalter kommt seitdem aus den Daten und ist auch in Rom und Wien sichtbar. Offen: Prüfung am iPhone.
  - **Option für später, Variante A:** Kern zur Laufzeit als eine gemeinsame Datei (`kern.js` mit CSS, Markup und Code im
    Wurzelordner, je Strecke nur eine dünne Seite mit den Feldern). Nur bei konkretem Bedarf, etwa wenn die Startseite den
    Pace-Code selbst braucht. Bedingungen aus der Analyse: Kern in SHELL des Service Workers, die Startseite frischt ihn mit
    auf, Hinweis in der dünnen Seite, wenn der Kern fehlt, Cache-Namen unverändert, Übergang am iPhone prüfen. `kern.py` kennt
    die Grenze zwischen Kern und Feldern schon und könnte dann dünne Seiten schreiben.
- **Weitere Strecken aus dem Angebot von interAir** (Abgleich 31.10.2026 mit 32 Laufreisen): Honolulu und Shanghai gebaut
  31.10.2026 (Marathon 2.3). Beaujolais nachrangig (dort läuft kaum jemand auf Zeit; IGN 1 m frei, Weg wie Médoc). Nicht
  sinnvoll oder nicht machbar: Frozen Lake (auf dem Eis, flach), Lost City Mexiko (keine offizielle Strecke), Bhutan (Pfade,
  nur 30-m-Modell), Antarktis (Kurs wechselt, kleines Feld).

## Kleinigkeiten aus den Übergaben

- Shanghai: Kurs 2025 in der App, weil der Plan 2026 fehlt (Seite „赛事路线图“, Nr. 3289): **Ende November 2026 nachsehen**
  (Rennen 6.12.2026), dann Wegpunkte in `linie.py`, Startzeiten in `app.py`. Linie aus OSM-Straßen, Wenden geschätzt (±0,3 km);
  Brücke Longhua Gang (+9,2 m) ist die größte Unsicherheit. Finisher nicht veröffentlicht (23 000 Starter 2025).
- Honolulu: 17 Verpflegungsstellen von Hand aus dem schematischen Plan (±0,3 km, Veranstalter sagt 16); Grenzen der
  Startgruppen widersprüchlich.

- Stockholm: Höhen aus der GPX-Datei des Veranstalters (Herkunft unbekannt, sehr glatt; Brückendecks drin). Laser-Modell
  von Lantmäteriet (Markhöjdmodell 1 m, CC BY 4.0) nur mit kostenlosem Geotorget-Konto: Nutzer entscheidet, ob er sich
  anmeldet; dann wie Wien rechnen. Kurs, Starts und Marken 2027 nachtragen.
- Médoc: Kilometer nur über die Länge geeicht (±50 m); „Parcours 2027“ (OpenRunner, kommt etwa im Juli) neu einlesen;
  Château-Namen an den Weinproben; Uhrzeit der Sperre zur Halbzeit.

- Wien: drei Wasserstellen nur auf der Karte des Veranstalters (Schüttelstraße bei km 6,5/36,5, Alserbachstraße bei km 23,7),
  fehlen in der App; Startlinie 70 m vor der Karte nur abgeleitet; Startblöcke 2027 eintragen.
- Athen: Laufbahn im Stadion steigt im 30-m-Modell um gut 2 m (in Wirklichkeit eben); Kataster-Modell (5 m), falls es frei
  wird; GPX 2027 prüfen (Umweg über Michalakopoulou/Feidippidou). Höhen unter CC BY-NC-SA (FABDEM): vor einer Weitergabe
  an interAir klären.

## Eichung

- New York: Lage der 20- und 25-km-Matten zur Queensboro Bridge klären, dann die Brückenabschnitte wieder aufnehmen.

## Wartet auf andere

- Rom: Laser-Geländemodell des Umweltministeriums (MASE) nach dessen Wartung, Erinnerung am 07.11.2026.
- Great Wall: Kurs 2027 und Runners Guide (Schild 27 und Getränkestelle 13 widersprechen sich; 12 km der Linie nur aus der Karte).
- Amsterdam: Strecke 2027 über Rokin und Dam.
- Startwellen mit Uhrzeiten 2027 für mehrere Strecken.
- Prüfungen am iPhone.
