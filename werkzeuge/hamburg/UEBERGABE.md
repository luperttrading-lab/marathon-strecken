# Übergabe: Steigungsprofil Hamburg-Marathon

Stand 26.10.2026, App-Version **1.8**, live unter https://luperttrading-lab.github.io/marathon-strecken/hamburg/
und auf dem iPhone des Nutzers als Home-Bildschirm-App installiert.

Diese Notiz ist für die nächste Sitzung. Sie fasst zusammen, was in der Entstehungssitzung entschieden,
gemessen und verworfen wurde.

## Wo was liegt

| Pfad | Inhalt |
|---|---|
| `hamburg/index.html` | **Die App, und zugleich ihr Quelltext.** Eine Datei mit CSS, JS und allen Daten (`const D = {…}`). Änderungen werden direkt hier gemacht. |
| `hamburg/version.json` | Versionsmarke für die Update-Prüfung. **Immer zusammen mit `APP_VERSION` in `index.html` hochzählen.** |
| `hamburg/sw.js` | Service Worker: eigene Dateien Netz zuerst, Google-Schriften Cache zuerst, Kartenbilder werden bei der Installation vorgeladen. Cache-Name `hh-marathon-profil`. |
| `hamburg/karte-{hell,dunkel}-z{12..15}-*.jpg` | Kartenstücke (1024 px), OpenStreetMap umgefärbt. Lage pro Stück in `D.tiles`. |
| `werkzeuge/hamburg/work/` | Skripte und Zwischendaten der Aufbereitung (siehe unten). Werden von der App nicht geladen. |

Der Update-Mechanismus folgt der Skill **„app-update-iphone“** (Banner oben, Tipp auf die gepunktete
Versionsnummer im Kopf prüft von Hand, `localStorage`-Schlüssel `hhm.gesehen`).

## Entscheidungen des Nutzers (nicht wieder aufmachen, ohne zu fragen)

- **Nichts darf springen.** Anzeige oben mit fester Höhe: Texte einzeilig mit Auslassungspunkten, die Kartenseite
  bestimmt nie die Höhe (`contain: size`-Prinzip; in Kartengröße-Stufe 0 gibt die Zahlenseite sie vor, ab Stufe 1
  gilt eine feste Höhe für beide Seiten).
- **Start im Vollbild** (Klasse `body.run`): Anzeige, Läuferblick, Übersicht und Steuerung auf einem Bildschirm.
  ☰ führt zu Zwischenzeiten, Einstellungen, Rampen und Quellen.
- **Anzeige oben hat zwei wischbare Seiten: Zahlen und Karte.** Fotoseiten (Wikimedia, Sehenswertes, Straßenfotos
  „Blick voraus“ von Panoramax) wurden gebaut und **ausdrücklich wieder entfernt**.
- **Drehräder senkrecht** (wie die Zielzeit), Variante „drei Zeilen, knapp angeschnitten“, 52 px hoch,
  Ausschnitt 0,5–10 km in 0,5er-Schritten, Tempo ×100–×1000 in 100er-Schritten. Ränder und Nachbarzahlen kontrastreich.
- **Zielzeit sekundengenau per Drehrad.** Ein Rad übernimmt erst nach Berührung und nach dem Einrasten den sichtbaren
  Wert (iOS rollt nach dem Loslassen weiter; das hatte einmal zu falschen Zeiten geführt).
- **Pace-Modell:** Minetti et al. (2002), skaliert auf die Erfahrung des Nutzers: **1,0 s je Höhenmeter bei 15 km/h**
  (= 4,2 m flache Strecke je Höhenmeter; Minetti ergibt 5,4 m bzw. 1,3 s). Einstellbar 0,5–2,0 s.
  Bergab-Gewinn standardmäßig **halb**, und nur bis −4 % Gefälle, steiler bringt nichts zusätzlich.
- **Messfenster der Steigung** 10 m / 50 m / 200 m (Standard) / 1 km. Höhenmeter hängen stark davon ab:
  164 / 159 / 136 / 80 m; eine Tabelle dazu steht in der App unter „Woher die Zahlen kommen“.
- Wasser/Verpflegung und Staffelwechsel standardmäßig **aus**, einschaltbar. Halbmarathon-Marke immer sichtbar.
- Straßennamen am Fuß des Profils, aktuelle Straße blau. Ist das Profil unter 180 px hoch (Kartengröße-Stufen 2 und 3,
  kleine iPhones schon ab Stufe 1), entfallen sie, damit die Kurve frei bleibt (seit 1.3, Wunsch des Nutzers).
- **Kartengröße umschaltbar** (seit 1.2): Knopf ↕︎ unter +/− auf der Kartenseite, nur im Vollbild, schaltet reihum
  durch die Höhe der Anzeige-Seiten: Stufe 0 = wie bisher (150 px, für genaueres Hinsehen auf die Steigung),
  1 = 230 px (**Start**), 2 = 300 px. Die Zahlenseite verteilt dann ihre Zeilen und bekommt größere Zahlen. Das Profil
  behält mindestens 120 px; auf kleinen Bildschirmen werden Stufen mit gleicher Höhe übersprungen. `localStorage`
  `hhm-gr`. Eine vierte Stufe (350 px) hat der Nutzer nach dem Test verworfen: Profil zu klein, Karte kaum größer.
- **Start und Ziel** im Profil (seit 1.4): Start im Stil der Halbmarathon-Marke, Ziel als karierte Zielflagge; auf der
  Karte ein kariertes Feld am Streckenende (seit 1.5).
- **Zieleinlauf** (seit 1.5): Überquert der Läufer die Ziellinie (Abspielen, Wischen oder Knöpfe), erscheint eine
  Zielkarte mit Zielband, „ZIEL“ im Farbverlauf der Steigungsklassen, Ø-Pace, Zielzeit, Bergauf/Bergab und dem Satz
  „Das Höhenprofil kostet 1:32 min.“ (Wortlaut vom Nutzer gewünscht, ab 60 s in min), dazu etwa 3 s Konfetti (entfällt bei „Bewegung reduzieren“). Antippen schließt. Liegt fest über der
  Seite, schiebt nichts.
- **Hell/Dunkel-Umschalter** (Sonne/Mond) links oben in der Anzeige, **Versionsnummer** rechts oben (nur Vollbild).
  Beide liegen absolut im Leerraum über „Kilometer“ und „Höhe“ und schieben nichts. Der Umschalter wechselt zum
  Gegenteil des Sichtbaren; landet er dabei auf der Systemeinstellung, folgt die App wieder dem System
  (`localStorage` `hhm-theme`, gesetzt im Kopf vor dem ersten Zeichnen). Versionstext kommt aus `APP_VERSION`.
- **Farben** (seit 1.6, in 1.7 nachgedunkelt): Hell gedämpft, kein reines Weiß (`--surface` #e2e7eb, `--bg` #cdd5dc,
  `--muted` #4f5f6c), weil es blendete. Die Strecke auf der Karte hat einen Rand im Gegenton (`--ink`: hell dunkel,
  dunkel hell, seit 1.8), sonst verschwinden die flachen grauen Abschnitte im Kartengrund. Dunkel bleibt bewusst dunkler: die Strecke hebt
  sich dort besser ab.
  Kartenuntergrund wird nach dem Zeichnen der Kacheln getönt: dunkel per `screen` aufgehellt, hell per `multiply`
  abgedunkelt (`drawMap`, zwei Werte). Die Kachel-JPGs selbst sind unverändert.
- Keine Textmarkierung (`user-select: none`), keine Emoji-Darstellung von Pfeilen (`︎`).

## Datenaufbereitung (`werkzeuge/hamburg/work/`)

Die Skripte erwarten, aus `work/` heraus gestartet zu werden, mit Geschwisterordnern `../dl`, `../assets`, `../pwa`.
Die Originaldateien des Veranstalters liegen nicht im Repo; sie kommen von
`https://haspa-marathon-hamburg.de/download/strecke/HMH26_Marathon.gpx` und
`http://mhv-maps.de/marathon/strecke/maps2026/HMH26_*.kmz` (Strecke, KM-Punkte, Staffel, Verpflegung, Hotspots, Bands).

1. `parse.py` liest die GPX (42,64 km gezeichnet, also 1 % zu lang), `kml.py` die KMZ, `proj.py` projiziert die
   42 offiziellen KM-Punkte auf die Linie → `kmproj.json`; `common.py` eicht jede GPX-Strecke stückweise linear auf
   offizielle Kilometer.
2. `dgm.py` fragt das **DGM1 Hamburg** (1-m-Laserscan) über WMS-GetFeatureInfo alle 10 m ab
   (`geodienste.hamburg.de/HH_WMS_DGM1`, Ebene `WMS_DGM1_HAMBURG`, ~5 Abfragen/s mit 8 Threads) → `dgm2026_10m.json`.
3. `clean.py`: Wasser hat den Wert −20 → Brücke; Sprünge > 1,5 m auf 10 m paarweise → Brücke oder Tunnel;
   Ränder bis 3 Punkte erweitert; dazwischen linear. Ergebnis 17 Brücken und der **Wallringtunnel km 14,12–14,66**
   (Nominatim nennt dort zweimal „Wallringtunnel“; das Modell misst die Oberfläche darüber) → `clean.json`.
   Nachträglich von Hand: Geländekante Breite Straße km 9,97 über 90 m geglättet (Index 994–1003 im 10-m-Raster).
4. `streets.py`: Nominatim-Rückwärtssuche alle 150 m (1 Abfrage/s) → `streets2026.json`. Straßengrenzen daher ±75 m.
5. `build.py` baut `data.json` (Höhen in cm im 10-m-Raster, Median über 30 m, Straßen, Marken, Brücken).
6. `route.py` → Koordinaten alle 50 m (`route50.json`), `tiles.py` → Kartenstücke z12–z15 (z15 nur entlang der
   Strecke), hell entsättigt, dunkel invertiert und farbgedreht.
7. `digit.py` hat das ursprüngliche Profilbild des Nutzers ausgelesen (Kalibrierung ±1,4 m). Es zeigt einen
   **älteren Kurs** (Staffelwechsel 16,3/27,7/32,7 statt 15,4/27,2/32,4), die Form stimmt mit dem DGM überein.
8. `pwa_build.py` hat aus der damaligen Artifact-Fassung die App gebaut. **Nur noch historisch** – die Artifact-Fassung
   ist gelöscht, gearbeitet wird direkt in `hamburg/index.html`.

## Fallstricke

- **CARTO-Kartenkacheln** liefern ohne API-Schlüssel nur „API KEY REQUIRED“. OSM-Kacheln gehen, sparsam und mit
  eigenem User-Agent abrufen.
- **Wikimedia** antwortet aus dem Rechenzentrum schnell mit 429; Abfragen bündeln, langsam takten.
- **Overpass** war nicht erreichbar; Brücken/Tunnel deshalb aus dem Höhenmodell erkannt, nicht aus OSM.
- **Panoramax** (`api.panoramax.xyz/api/search?bbox=…`) hat gute Straßenfotos in Laufrichtung
  (meist „veloroute_hamburg“, Etalab 2.0) – vom Nutzer aber nicht gewünscht.
- **iOS-Drehräder:** `scrollTop` greift bei verdeckten Rädern nicht zuverlässig → beim Sichtbarwerden neu stellen
  (IntersectionObserver). Waagerechte Flex-Elemente brauchen `min-width: 0`, sonst laufen sie über.
- **GitHub:** Diese Umgebung durfte kein Repo anlegen (403); `marathon-strecken` hat der Nutzer selbst angelegt.
  Pages: Branch `main`, Ordner `/`.

## Offen

- **Kurs 2027** ist noch nicht veröffentlicht. Wenn er kommt: neue GPX/KMZ, Schritte 1–6 wiederholen, `D` ersetzen,
  Version hochzählen. Bei einer neuen Strecke eigener Ordner neben `hamburg/`, damit Home-Bildschirm-Adressen stabil bleiben.
- **Prüfung am iPhone** noch nicht gemacht: Flugmodus-Test (App und Karte offline) und Tipp auf „v1.0“
  (erwartet „Version 1.0 ist aktuell“).
- Im Repo **`fragen-allgemein`** fehlt noch diese Regel in der `CLAUDE.md` (Hochladen war dort blockiert):

  ```
  ## Link am Ende der Antwort

  Wurde in der Antwort ein Artifact, eine Seite oder eine Datei veröffentlicht oder aktualisiert: den Link dazu als
  letzte Zeile vor der Kostenzeile wiederholen (`**Link:** [Name](URL)`), auch wenn er weiter oben schon steht.
  Der Nutzer liest auf dem Handy und soll den Link nicht in langen Antworten suchen müssen.
  ```
- Die Vorschlagsseite „Drehrad-Varianten“ (Artifact `37JXJ4NiJYDdswFVPTsNQD`) existiert noch; der Nutzer hat nicht
  entschieden, ob sie weg soll.
