# Marathon-Steigungsprofile

Steigungsprofile von 31 Marathonstrecken als Web-Apps für das iPhone, ausgeliefert über GitHub Pages aus `main`:
https://luperttrading-lab.github.io/marathon-strecken/ . Aufbau, Strecken und Konventionen stehen in `README.md`,
Bedien- und Designentscheidungen in `werkzeuge/hamburg/UEBERGABE.md`, je Strecke in `werkzeuge/<strecke>/UEBERGABE.md`.
Offene Ideen und Punkte: `werkzeuge/VORGEMERKT.md`. Eichung des Pace-Modells: `werkzeuge/eichung/README.md`.

## Arbeitsweise mit dem Nutzer

- Der Nutzer gibt Richtung und prüft die Logik; Claude liefert Breite und Umsetzung. Er liest auf dem Handy.
- **Zwischendurch kurz sagen, was gerade läuft und wer es macht** (z. B. „zwei Agenten bauen Athen und Wien, ich prüfe
  derweil …“). Wenig Text, aber laufend.
- Am Ende einer Arbeit eine Push-Nachricht aufs Handy, dass es weitergehen kann.
- Wurde etwas veröffentlicht, als letzte Zeile vor der Kostenzeile:
  `**Link:** [Marathon-Steigungsprofile](https://luperttrading-lab.github.io/marathon-strecken/)`
- Kostenzeile: `tools/kosten.py` liegt im Repo `fragen-allgemein`; ist es in der Sitzung, von dort frisch ausführen.
- Bilder und Prüfergebnisse (Screenshots) dem Nutzer schicken, bevor eine größere Änderung auf alle Apps geht.
- „Höhenmeter“ nie als „HM“ abkürzen.

## Konventionen beim Ändern

- **Gemeinsamer Kern** (seit Marathon 2.0): Alle Strecken-Apps haben denselben Kern; Unterschiede nur in ihren Feldern
  (Daten `const D`, `SHORT`, Texte zur Strecke, Präfixe, Kartenliste). **Den Kern nur in `hamburg/index.html` bzw.
  `hamburg/sw.js` ändern**, dann `python3 werkzeuge/kern/kern.py --version 2.N --schreiben` (setzt ihn in alle Strecken ein).
  Ohne Schalter prüft `kern.py` nur und muss „Alle gleich“ melden; vor jedem Commit laufen lassen. Patch-Skripte über 24
  Dateien entfallen; für die Startseite (`index.html`, kein Erzeugnis) weiter mit `assert s.count(alt) == 1`.
- **Eine Versionsnummer für die ganze App** (Quelle `version.json` im Wurzelordner): `kern.py --version 2.N --schreiben` setzt
  sie in allen Strecken und auf der Startseite, auch wenn sich nur Daten einer Strecke geändert haben. **Nummern nur nach
  oben** (Zahlvergleich, 2.10 > 2.9), auch beim Zurücknehmen, sonst erkennen die Handys den Stand nicht. Änderungen am Kern in
  `werkzeuge/kern/AENDERUNGEN.md` eintragen, Änderungen an Daten oder Texten einer Strecke im Kopf ihrer
  `werkzeuge/<strecke>/UEBERGABE.md`. Commits heißen „… (Marathon 2.N)“.
- Great Wall: Daten und Texte entstehen über `werkzeuge/greatwall/work/app.py` aus `tokio/index.html` und `tokio/sw.js`; die
  Nummer liest es aus `version.json`. Kette: `app.py` laufen lassen, danach `kern.py` (prüfen) muss „Alle gleich“ melden. Athen
  und Wien lesen die Nummer ebenso, ihr `app.py` aber **nicht** allein laufen lassen (danach müsste `tiles_rand.py` folgen,
  sonst sind Kartenbilder und Kachelangaben falsch).
- Neue Strecken baut ein Agent nach dem Muster in `werkzeuge/athen/` bzw. `werkzeuge/wien/` (nicht committen) und liefert die
  Felder; die Seite entsteht mit `kern.py --neu <ordner> <felder.json>` (Format: `kern.py --felder tokio`). Startseite (Karte,
  Reihenfolge nach Teilnehmerzahl, Mini-Profil), README und Push macht die Hauptsitzung.
- Commits auf Deutsch, direkt auf `main`.

## Prüfen

- Lokaler Server aus dem Repo-Wurzelordner: `python3 -m http.server 8765` (im Hintergrund; endet nach 2 Stunden).
- Playwright mit Chromium (vorinstalliert, nicht neu installieren), 393×852 bei Faktor 2: alle Apps auf Konsolenfehler und
  Version, Tabellen bei 320/375/393/430 px ohne Überbreite, Bilder der geänderten Stelle ansehen.
- Nach dem Push jede `version.json` unter GitHub Pages abfragen, bis alle den neuen Stand haben; erst dann „live“ melden.

## Offline (Stand Marathon 2.3)

- Service Worker je Strecke: eigene Dateien Netz zuerst, offline **nur aus dem eigenen Speicher**; die Seite wird bei jedem
  Besuch mit Netz auch als `index.html` erneuert. Bei der Installation **keine Kartenbilder**; die holt die Seite beim Öffnen
  mit Netz (Auftrag `karten` an den eigenen Service Worker).
- Die Startseite richtet beim Öffnen mit Netz alle Strecken ein (ohne Karten, ≈ 1,8 MB) und frischt gespeicherte auf
  (`version.json` vergleichen). Knopf „Alle Karten offline speichern (≈ N MB)“ mit Rückfrage; Grundlage `karten.json`, das
  `kern.py --schreiben` schreibt (Prüfen meldet eine veraltete Liste, also nach neuen Strecken oder Kartenbildern immer
  `--schreiben`).
- Offline erscheint oben ein oranger Hinweis „gespeicherte Fassung vX, vielleicht nicht die neueste“, bis man ihn antippt; im
  Kartenfeld ohne Bilder „Offline: Karte nicht gespeichert“ (gegenüber dem Maßstab).

## Regeln

- Logins, Captchas und Sperren nie umgehen. Keine Daten erfinden; Unsicheres kennzeichnen.
- Personendaten (Läufernamen aus Ergebnislisten) nie ins Repo; nur verdichtete Kennzahlen.

## Nächste Schritte (Stand 30.10.2026)

1. ~~**Gemeinsamer Kern** statt 24 Kopien~~ – erledigt 30.10.2026 als Marathon 2.0 (`werkzeuge/kern/`). Offen: Prüfung am
   iPhone (Banner aus dem Hintergrund, „2.0 ist geladen“ einmal, Tipp „ist aktuell“, Flugmodus).
2. Startseite „Deine Form auf allen Strecken“.
3. ~~Stockholm~~ – gebaut 30.10.2026 (Marathon 2.1), dazu Médoc. Offen: Höhen Stockholm nur aus der GPX-Datei des
   Veranstalters (Lantmäteriet-Laserdaten nur mit Geotorget-Konto, Entscheidung des Nutzers).
4. Kleinkram: drei Wasserstellen in Wien, Stadion-Laufbahn in Athen. (Entschieden 30.10.2026: im Ziel „42,2“ – „42,195“ war
   kurz drin und wurde zurückgenommen –, Halbmarathon „21,1“.)
5. Rom: Laser-Geländemodell des Umweltministeriums prüfen, geplante Erinnerung am 07.11.2026.
