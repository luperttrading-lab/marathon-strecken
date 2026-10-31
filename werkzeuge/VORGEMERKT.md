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

- **Marathons in Deutschland, Österreich und der Schweiz** (Recherche 31.10.2026, Nutzer: „nach und nach alle“, Reichweite
  so wichtig wie das Profil, erst die flachen): Runde 1 Hannover, Düsseldorf, Zürich gebaut (Marathon 2.4), Runde 2 Münster,
  Luzern, Freiburg gebaut (Marathon 2.5). Runde 3 Berg: Jungfrau, Zermatt, Brocken gebaut mit Hinweis im Kern (Marathon 2.6), Runde 4 Graz,
  Salzburg, LGT Alpin (Liechtenstein) mit mindestens 10-facher Überhöhung im Läuferblick (Marathon 2.7). Danach Graz, Salzburg, LGT Alpin, Allgäu, Ulm und die übrigen.
  Ranking und Quellen: Bericht vom 31.10.2026 (Jungfrau 3 604, Zermatt 355, Brocken 676, Luzern 3 076, Freiburg 1 560,
  Münster 3 114 Finisher).
- **Bergmarathons, Zeitprognose:** Das Pace-Modell ist an Straßenrennen geeicht; ab etwa 10 % gehen die meisten. Später
  eichen, ohne Namen: Zwischenzeiten innerhalb des Jungfrau-Marathons (flaches Tal bis Lauterbrunnen gegen den steilen Teil),
  je Läufer relativ wie in `eichung/`. Idee: auf sehr steilen Stücken Höhenmeter je Stunde statt Pace.
  Daten dafür (31.10.2026 geprüft, nichts gespeichert): Datasport hat für Jungfrau 2026 Zwischenzeiten aller 3 604 Finisher an
  km 3,3 / 5 / 10,4 / 15,1 / 21,1 / 25,9 / 30,7 / 38,5, für Zermatt 4 Etappen (Zermatt, Sunnegga, Riffelalp); Brocken keine; LGT Alpin 3 Etappen (Vaduz km 10,3, Steg km 25,4): Median-Anteile 17,4 / 38,9 / 43,6 %, Modell 20,3 / 40,4 / 39,4 %.
  Befunde: Jungfrau-Richtzeiten des Veranstalters für 5 h: 1:59 / 3:11 / 4:16 (Halbmarathon / Wengen / Wixi), Modell 2:08 / 3:20 /
  4:22; Zermatt Median-Anteile der Etappen 39,8 / 29,5 / 17,2 / 13,3 %, Modell 45,6 / 29,1 / 15,3 / 9,9 %; Brocken Modell 3:04 bei
  4:00 /km flach, Median 2026 4:42. Das Modell unterschätzt die steilen Stücke auch bei fester Zielzeit.

## Kleinigkeiten aus den Übergaben

- Hannover: Veranstalter nennt „19 m Höhenunterschied“, gemessen 9,4 m; zwei Unterführungen (Fernroder Straße, Kopernikusstraße)
  geschätzt; DGM1 2016 (Stadt hat 2021).
- Düsseldorf: keine GPX, Linie aus dem Streckenplan-PDF 2026; Start Ehrenhof laut Plan, „Höhe Tonhalle“ laut Text.
- Münster: Kilometerangaben des Veranstalters widersprüchlich (Kanonierplatz Tabelle 4,3 / Ort 4,7; Wulfertstraße 30,0 / 29,1);
  ohne GPX nur ±0,2 km; Staffelwechsel 2 nur nach Plansymbol.
- Luzern: Stadtquartiere fehlen (map.stadtluzern.ch nicht erreichbar, opendata.swiss 403); Startslot-Zeiten ohne Jahreszahl.
- Freiburg: Kilometer ±0,3 km (Kästen im Plan bis 333 m früher); Rundenwechsel auf dem Messplatz angenommen; Kurs 2027 folgt.
- Graz: Finisherzahl (1 077) unbestätigt, Ergebnisliste bei maxfunsports hinter Cloudflare (403); Labestationen nur aus Grafik 2025.
- Salzburg: Ziel 2027 Residenzplatz oder Max-Reinhardt-Platz? Plan 2027 abwarten.
- Liechtenstein: keine GPX (nur AllTrails mit Konto), Linie nachgezeichnet, Orte auf ±0,7 km.
- Zürich: Lage der 12 Verpflegungsposten nur aus dem Plan (am See ±0,5 km); Kurs 2027 mit „punktuellen Anpassungen“.

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
