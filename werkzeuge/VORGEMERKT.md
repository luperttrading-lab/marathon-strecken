# Vorgemerkt

Ideen und offene Punkte, die besprochen, aber noch nicht gebaut sind. Stand 30.10.2026.

## Ideen (mit dem Nutzer besprochen, Reihenfolge offen)

- **Als Nächstes (Nutzer 31.10.2026, „morgen“):** alle Strecken offline, aber **ohne Karten** (Seiten ≈ 65 KB gepackt je
  Strecke; mit Karten wären es bei 20 weiteren Strecken ≈ 140 MB). Im Kartenfeld ein Hinweis, wenn das Handy offline ist und
  die Kartenbilder fehlen. Braucht Rückfragen an den Nutzer, deshalb nicht über Nacht.
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
- **Alle Strecken offline beim Öffnen der Startseite:** gebaut als Hamburg 1.78 / Startseite 1.37 (Commit 9238f37), am
  30.10.2026 auf Wunsch des Nutzers zurückgenommen („erstmal nur die Meldung“). Kosten: ≈ 1,6 MB einmalig, Karten ≈ 72 MB
  per Knopf. Wieder einspielen: `git revert` des Rücknahme-Commits.
- **Weitere Strecken aus dem Angebot von interAir:** Beaujolais nachrangig (dort läuft kaum jemand auf Zeit). Athen und
  Wien sind seit 30.10.2026 gebaut, Stockholm und Médoc seit 30.10.2026 (Marathon 2.1).

## Kleinigkeiten aus den Übergaben

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
