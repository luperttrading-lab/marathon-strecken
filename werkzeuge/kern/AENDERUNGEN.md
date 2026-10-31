# Änderungen am gemeinsamen Kern

Eine Nummer für die ganze App (Startseite und alle Strecken). Neueste oben. Den Kern nur in `hamburg/index.html` bzw.
`hamburg/sw.js` ändern, dann `python3 werkzeuge/kern/kern.py --version 2.N --schreiben` und hier eintragen. Was der Kern ist
und welche Felder jede Strecke hat, steht im Kopf von [`kern.py`](kern.py) und in
[`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md) („Gemeinsamer Kern“). Ältere Stände (bis Hamburg 1.82, Startseite 1.40)
stehen in den Köpfen der `UEBERGABE.md` je Strecke.

## 2.3 (31.10.2026): alle Strecken offline, Karten auf Wunsch

Nutzer 31.10.2026: alle Strecken offline, aber ohne Karten (mit Karten wären es bald über 80 MB); im Kartenfeld ein Hinweis,
wenn das Handy offline ist; Karten aller Strecken per Knopf, „mit Datenmenge und ob der User sich sicher ist“.

- **Service Worker:** lädt bei der Installation nur noch Seite, `version.json`, Manifest und Symbole, keine Kartenbilder. Neu
  der Auftrag `karten` (von der eigenen Seite beim Öffnen mit Netz): fehlende Kartenbilder dieser Strecke ablegen. Wer eine
  Strecke öffnet, hat ihre Karte also weiter offline; Cache-Namen unverändert, gespeicherte Karten bleiben.
- **Kartenfeld:** Fehlt ein sichtbares Kartenbild, steht links ein Hinweis, offline „Offline: Karte nicht gespeichert /
  Strecke, Profil und Zahlen gehen“, mit Netz „Kartenbilder laden gerade nicht“; oben oder unten, gegenüber dem Maßstab, der
  OSM-Vermerk entfällt dann. Fehlgeschlagene Bilder werden mit Netz bis zu dreimal nach 2 s und nach „online“ (0,8 s später)
  neu versucht.
- **`kern.py`** schreibt `karten.json` im Wurzelordner (je App Speichername und Kartenbilder mit Bytes); Prüfen meldet eine
  veraltete Liste.
- **Startseite:** richtet beim Öffnen mit Netz die Service Worker aller Strecken ein (≈ 1,8 MB gepackt für alle, wie 1.37,
  aber ohne Karten). Knopf „Alle Karten offline speichern (≈ N MB)“ mit der Menge, die im Speicher noch fehlt (aus
  `karten.json`); Antippen öffnet die Rückfrage „Das lädt etwa N MB … wirklich?“ mit „Ja, speichern“ / „Abbrechen“. Die Seite
  holt die Bilder selbst (vier gleichzeitig, Fortschritt in MB) und legt sie in den Speicher der jeweiligen Strecke. Danach
  verschwindet der Knopf.
- **Zwei neue Strecken** über `kern.py --neu`: `honolulu/` (Präfix `hnl-`, USGS-Lasermodell 1 m) und `shanghai/` (Präfix
  `sha-`, FABDEM geglättet, Brücken geschätzt, Kurs 2025, weil der Plan 2026 noch fehlt). Karten auf der Startseite nach Boston.

## 2.2 (31.10.2026): Suche auf der Startseite

- Kern unverändert. Startseite: neue erste Suchstufe „Stadtname beginnt mit der Eingabe“. Bisher traf „St“ auch das Wort
  „Stadt“ in „Mexiko-Stadt“, und das alphabetische Rad stellte Mexiko-Stadt vor Stockholm.

## 2.1 (30.10.2026): Stockholm und Médoc

- Kern unverändert. Zwei neue Strecken über `kern.py --neu`: `stockholm/` (Präfix `sth-`) und `medoc/` (Präfix `med-`),
  Karten auf der Startseite. Nummer für alle hochgezählt, damit die Startseite das Update bringt.

## 2.0 (30.10.2026): gemeinsamer Kern, eine Versionsnummer

- **Erzeuger** `werkzeuge/kern/kern.py`: Vorlage ist Hamburg. Prüfen (Standard, schreibt nichts, Diff und Ausgang 1 bei
  Abweichung), `--schreiben`, `--version 2.N`, `--erzwingen`, `--neu <ordner> <felder.json>`, `--felder <ordner>`. Setzt auch
  `sw.js` aus `hamburg/sw.js` zusammen (alle 24 waren schon byte-gleich bis auf die Felder).
- **Eine Nummer für alles:** 2.0 in allen 24 `X/version.json`, allen `APP_VERSION`, beiden Versionsknöpfen je Strecke und auf
  der Startseite (`index.html`, `version.json`). Vorher je Strecke eigene Nummern 1.10 bis 1.82, Startseite 1.40.
- **„Version X ist geladen“ einmal für die ganze App:** gemeinsamer Schlüssel `marathon.gesehen` statt `hhm.gesehen` …
  `start.gesehen`, nur bei höherer Nummer (Zahlvergleich, 2.10 > 2.9). Rückfall beim ersten Lauf: der alte Schlüssel der Seite,
  sonst der einer anderen Strecke.
- **Kein Neuladen von selbst bei „Live nach Plan“** (`S.live`, bisher nur beim Abspielen `S.playing` gesperrt): Ein Zuschauer
  verlor sonst den Live-Modus. Dann bleibt das grüne Banner mit „Jetzt laden“.
- **Schutz vor Neuladen-Schleifen:** von selbst höchstens einmal je Zielnummer und Seite in einer Sitzung (`sessionStorage`).
- **Staffel-Schalter aus den Daten:** sichtbar, wenn `D.marks` Staffelwechsel hat (Hamburg, Frankfurt, Rom, Wien). Bisher ein
  `hidden` im Markup je Strecke; Rom und Wien hatten die Staffelwechsel in den Daten, der Schalter war aber verborgen.
- **Abdrift angeglichen:** Berlin, Frankfurt, Hamburg, Köln, München, Oberelbe und Rennsteig nennen in den Quellen jetzt auch
  „Rampen“ bei Brücken und Tunneln (wie die 17 anderen). Ohne Wirkung, keine dieser Strecken hat `"kind":"Rampe"` in `D.bridges`.
- **Werkzeuge:** `app.py` von Great Wall, Athen und Wien lesen die Nummer aus `version.json` im Wurzelordner.
- Speicherschlüssel der Einstellungen (`hhm-…` usw.) und Cache-Namen der Service Worker unverändert.
