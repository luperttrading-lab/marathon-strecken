# Eichung des Pace-Modells an echten Zwischenzeiten

Stand 30.10.2026. Frage: Stimmen die **1,0 s je Höhenmeter bei 4:00 /km** und **„bergab die Hälfte“**, mit denen alle Apps
rechnen? Bisher waren sie nur aus Minetti (Labor) und der Erfahrung des Nutzers abgeleitet, nie an Rennen gemessen.

## Ergebnis

Faktor 1 heißt: das App-Modell stimmt. Bereiche: 95 % aus Bootstrap über ganze Jahrgänge (`ergebnis.txt`).

| Ansatz | bergauf (1 = 1,0 s) | bergab (1 = „Hälfte“) |
|---|---|---|
| Boston allein (gegen die flachen Strecken) | **1,13** [1,03–1,20] | 1,00 [0,74–1,34] |
| New York allein | 0,69 [0,65–0,73] | 0,98 [0,78–1,26] |
| New York ohne die Brücken bei km 20–30 | 0,77 [0,55–1,00] | unsicher |
| alle zusammen, New York ohne Brücken | **0,87** [0,76–0,96] | 0,78 [0,53–1,06] |
| alle zusammen, Ermüdung nur linear | 0,86 [0,72–0,97] | 1,00 [0,78–1,25] |

- **Boston ist der sauberste Fall:** unser Profil und das unabhängige des Datensatzes stimmen je Abschnitt fast überein
  (km 25–30: +51 gegen +52 m), die Newton Hills liegen mitten in den Abschnitten.
- **New York ist unzuverlässig:** Unser Profil steht bei km 25 auf dem Scheitel der Queensboro Bridge (51 m). Liegt die
  Zeitmatte 200–300 m anders, landet ein großer Teil des Anstiegs im falschen Abschnitt; Messfehler in der erklärenden Größe
  drücken den Faktor nach unten. Ohne km 20–30 trägt New York kaum noch Information.
- **Die Bereiche sind zu eng:** Sie erfassen die Streuung zwischen Jahrgängen, nicht zwischen Strecken. Ehrlich ist eher
  0,8–1,15 bergauf.
- **Bergab „die Hälfte“** wird von Boston und New York einzeln bestätigt (0,98–1,00).
- **Leistung:** Läufer unter 3 h verlieren relativ weniger (0,7–0,9), das Mittelfeld um 4 h eher 1,0–1,3; nicht über alle
  Strecken stabil.
- **Grundsätzlich:** Gemessen ist, wie Läufer tatsächlich laufen. Die meisten drücken bergauf mehr und verlieren dort weniger
  Zeit, als gleiche Anstrengung kosten würde. Für das Ziel der App (Plan bei gleichmäßiger Anstrengung) sind die Werte eher
  eine Untergrenze.

**Folgerung (Empfehlung, Nutzer hat am 30.10.2026 nicht anders entschieden):** Die App bleibt bei 1,0 s und „bergab die
Hälfte“. 0,87 statt 1,0 hieße bei 4:00 Zielzeit: Berlin 46 → 40 s, Boston 124 → 108 s, New York 229 → 199 s, Rennsteig
662 → 580 s Steigungskosten (`steigungskosten_vergleich.js`).

## Daten

**Pace Notes v3** von Andrew Kam, [Figshare](https://doi.org/10.6084/m9.figshare.33965155), Lizenz **CC BY 4.0**:
5,3 Mio. Ergebnisse aus 34 Städten mit Zwischenzeiten alle 5 km, gesammelt von öffentlichen Ergebnisseiten. Die Rechte der
Veranstalter klärt die Lizenz des Hochladers nicht; deshalb nur Auswertung und verdichtete Kennzahlen.
`zellen.csv` ist daraus abgeleitet (Mediane, keine Personendaten) und steht mit dieser Quellenangabe ebenfalls unter CC BY 4.0.
Die Rohdaten enthalten Namen: `verdichten.py` liest sie gar nicht ein, die Rohdaten kommen nie ins Repo.

Gewählt sind nur Jahrgänge auf derselben Strecke wie in unserer App und mit Nettozeit (Chip):

| Rolle | Strecke | Jahre |
|---|---|---|
| hügelig | Boston | 2013–2026 ohne 2016, 2017 (Zeitnahme unklar) |
| hügelig | New York | 2009–2025 |
| hügelig | London | 2019, 2021–2026 |
| flach | Berlin | 2005–2026 |
| flach | Chicago | 2005–2026 ohne 2007 (Hitzeabbruch) |
| flach | Amsterdam | 2012–2025 ohne 2020 |
| flach | Valencia | 2016–2025 |

Nicht genommen: Paris, Sydney, Tokio (Strecke damals anders als in unserer App), Kapstadt und Rom (nicht im Datensatz).
Ausgefiltert: Qualitätsmarken des Datensatzes (`record_flags`), unvollständige Zwischenzeiten, Abschnitts-Pace außerhalb
2:40–15:00 /km, Zielzeit außerhalb 2–7 h, Abschnitt mehr als 40 % schneller oder doppelt so langsam wie der eigene Schnitt.
Übrig: 3 057 243 Läufer, verdichtet zu 8 874 Zellen (Jahrgang × Leistungsklasse × Abschnitt, mindestens 30 Läufer).

## Methode

- Je Läufer und Abschnitt (0–5, 5–10 … 35–40, 40–Ziel): `y = log(Abschnitts-Pace / eigene Durchschnitts-Pace)`; je Zelle
  der Median. Leistungsklassen nach Zielzeit: unter 2:45, dann in Viertelstunden bis 4:00, halbe Stunden bis 6:00, 6–7 h.
- Erklärende Größe: der Steigungsaufschlag der App je Abschnitt, `E = Mittel(paceRatio) − 1`, getrennt in bergauf (`E⁺`) und
  bergab (`E⁻`), aus unseren eigenen Höhenprofilen (`modell_seg9.json`).
- Modell: `y = α(Klasse, Abschnitt) + glatte Ermüdung je Jahrgang×Klasse (linear oder quadratisch im km) + kp·E⁺ + km·E⁻`.
  Die Ermüdung wird je Gruppe herausprojiziert (Frisch-Waugh), `kp` und `km` kommen damit nur aus dem „zackigen“ Teil.
  Gewichte: Läufer je Zelle, höchstens 1000.
- Robustheit: ohne ersten und letzten Abschnitt, Mittelwert statt Median, jede Stadt einmal weggelassen, je Leistungsklasse.

## Wiederholen

1. `./laden.sh /tmp/pacenotes` (1,57 GB, Prüfsumme wird geprüft)
2. `python3 -m pip install pyarrow pandas` und `python3 verdichten.py /tmp/pacenotes/private-export-20261021-1050` → `zellen.csv`
3. Nur wenn sich Profile oder Modell geändert haben: im Repo-Wurzelordner `python3 -m http.server 8765`, dann hier
   `node modell_segmente.js` → `modell_seg9.json`
4. `python3 schaetzen.py > ergebnis.txt` (einige Minuten)

Neue Strecke (z. B. Athen): Jahrgänge in `WAHL` (`verdichten.py`), App-Ordner in der Liste von `modell_segmente.js`,
Stadtname in `NAME` (`schaetzen.py`).

## Offen

- New York: Lage der 20- und 25-km-Matten zur Queensboro Bridge klären, dann die Brückenabschnitte wieder aufnehmen.
- Athen ist der stärkste weitere Test (gut 20 km stetig bergauf, 9 Jahrgänge im Datensatz), sobald es die App gibt.
- Leistungsabhängigkeit: ob schnelle Läufer relativ weniger verlieren, an weiteren Strecken prüfen.
