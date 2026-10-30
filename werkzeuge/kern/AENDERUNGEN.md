# Änderungen am gemeinsamen Kern

Eine Nummer für die ganze App (Startseite und alle Strecken). Neueste oben. Den Kern nur in `hamburg/index.html` bzw.
`hamburg/sw.js` ändern, dann `python3 werkzeuge/kern/kern.py --version 2.N --schreiben` und hier eintragen. Was der Kern ist
und welche Felder jede Strecke hat, steht im Kopf von [`kern.py`](kern.py) und in
[`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md) („Gemeinsamer Kern“). Ältere Stände (bis Hamburg 1.82, Startseite 1.40)
stehen in den Köpfen der `UEBERGABE.md` je Strecke.

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
