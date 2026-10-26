# Steigungsprofil Hamburg-Marathon

Wischbares Höhen- und Steigungsprofil der Strecke des Haspa Marathon Hamburg (Kurs 2025/2026), als Web-App für den Home-Bildschirm.
Inoffiziell, kein Angebot des Veranstalters.

**App:** https://luperttrading-lab.github.io/marathon-strecken/hamburg/ – in Safari öffnen, *Teilen → Zum Home-Bildschirm*.

## Datenquellen

- Strecke und Kilometerpunkte: veröffentlichte GPX- und KMZ-Dateien des Veranstalters (haspa-marathon-hamburg.de, mhv-maps.de).
- Höhe: Digitales Geländemodell DGM1 Hamburg, © Freie und Hansestadt Hamburg, LGV, Datenlizenz Deutschland – Namensnennung 2.0 (dl-de/by-2-0).
  Brücken und der Wallringtunnel sind durch Geraden ersetzt, eine Geländekante in der Breiten Straße ist ausgeglichen.
- Karte: © OpenStreetMap-Mitwirkende (ODbL), Kartenbilder von tile.openstreetmap.org, für hellen und dunklen Modus umgefärbt.
- Straßennamen: © OpenStreetMap-Mitwirkende, über Nominatim.
- Pace-Modell: Energiekosten des Laufens nach Minetti u. a. (2002), auf einstellbare Kosten je Höhenmeter skaliert.

## Updates

`APP_VERSION` in `index.html` und `version.json` bei jeder Änderung gemeinsam hochzählen. Die App prüft beim Öffnen und beim Zurückholen aus dem Hintergrund,
ein Tipp auf die Versionsnummer im Kopf prüft von Hand.
