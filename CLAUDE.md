# Marathon-Steigungsprofile

Steigungsprofile von 24 Marathonstrecken als Web-Apps für das iPhone, ausgeliefert über GitHub Pages aus `main`:
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

- Alle Strecken-Apps haben **denselben Code**; Unterschiede nur in Daten (`const D`), Texten zur Strecke und Präfixen.
  Eine Änderung am Verhalten in **allen** Apps nachziehen, am besten mit einem Python-Patch-Skript, das jeden ersetzten Text
  per `assert s.count(alt) == 1` prüft.
- Jede Änderung: `APP_VERSION` in der `index.html`, `version.json` und den Kopf der `werkzeuge/<strecke>/UEBERGABE.md`
  gemeinsam hochzählen. **Nummern nur nach oben**, auch beim Zurücknehmen, sonst erkennen die Handys den Stand nicht.
- Great Wall entsteht über `werkzeuge/greatwall/work/app.py` aus `tokio/index.html` und `tokio/sw.js`: dort `VERSION`
  hochzählen und das Skript laufen lassen. Bei Athen und Wien nur `VERSION` in `app.py` mitführen, das Skript **nicht**
  allein laufen lassen (danach müsste `tiles_rand.py` folgen, sonst sind Kartenbilder und Kachelangaben falsch).
- Neue Strecken baut ein Agent nach dem Muster in `werkzeuge/athen/` bzw. `werkzeuge/wien/` (Basis `tokio/index.html`, nicht
  committen); Startseite (Karte, Reihenfolge nach Teilnehmerzahl, Mini-Profil), README und Push macht die Hauptsitzung.
- Commits auf Deutsch, direkt auf `main`.

## Prüfen

- Lokaler Server aus dem Repo-Wurzelordner: `python3 -m http.server 8765` (im Hintergrund; endet nach 2 Stunden).
- Playwright mit Chromium (vorinstalliert, nicht neu installieren), 393×852 bei Faktor 2: alle Apps auf Konsolenfehler und
  Version, Tabellen bei 320/375/393/430 px ohne Überbreite, Bilder der geänderten Stelle ansehen.
- Nach dem Push jede `version.json` unter GitHub Pages abfragen, bis alle den neuen Stand haben; erst dann „live“ melden.

## Offline (Stand Startseite 1.40, Hamburg 1.80)

- Service Worker je Strecke: eigene Dateien Netz zuerst, offline **nur aus dem eigenen Speicher**; die Seite wird bei jedem
  Besuch mit Netz auch als `index.html` erneuert. Kartenbilder werden bei der Installation vorgeladen.
- Offline erscheint oben ein oranger Hinweis „gespeicherte Fassung vX, vielleicht nicht die neueste“, bis man ihn antippt.
- Die Startseite frischt beim Öffnen mit Netz alle schon gespeicherten Strecken auf (`version.json` vergleichen). Nie geöffnete
  Strecken sind offline nicht da; das Komplettpaket (alle Strecken beim Öffnen, Karten per Knopf) wurde gebaut und auf Wunsch
  des Nutzers zurückgenommen (Commit 9238f37).

## Regeln

- Logins, Captchas und Sperren nie umgehen. Keine Daten erfinden; Unsicheres kennzeichnen.
- Personendaten (Läufernamen aus Ergebnislisten) nie ins Repo; nur verdichtete Kennzahlen.

## Nächste Schritte (Stand 30.10.2026)

1. **Gemeinsamer Kern** statt 24 Kopien, bevor Stockholm App Nr. 25 wird (siehe `werkzeuge/VORGEMERKT.md`).
2. Startseite „Deine Form auf allen Strecken“.
3. Stockholm.
4. Kleinkram: drei Wasserstellen in Wien, Stadion-Laufbahn in Athen. (Entschieden 30.10.2026: Ziel zeigt „42,195“,
   Halbmarathon bleibt „21,1“.)
5. Rom: Laser-Geländemodell des Umweltministeriums prüfen, geplante Erinnerung am 07.11.2026.
