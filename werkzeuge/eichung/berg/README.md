# Eichung des Pace-Modells am Berg (Jungfrau, Zermatt, LGT Alpin)

Stand 31.10.2026. Frage: Was kostet ein Höhenmeter am Berg wirklich, und verlieren langsamere Läufer dort überproportional?
Ergänzt die Straßen-Eichung in [`../README.md`](../README.md) (dort: 1,0 s je Höhenmeter bei 4:00 /km passt für Stadtmarathons).
Kennzeichnung: **[Sicher]** gemessen und robust, **[Wahrscheinlich]** gut gestützt, **[Vermutung]** nicht belegt.

## Ergebnis in Kürze

1. **Das App-Modell rechnet nicht konstant 4,2 m.** Es nimmt die Minetti-Kurve mal 0,77 (4,17 / 5,42): 4,2 Flach-Meter je
   Höhenmeter an sanften Anstiegen, 4,6 bei 5 %, 5,1 bei 10 %, 5,4 bei 15 %, 5,8 bei 20 %, 6,4 bei 30 % (Minetti selbst:
   6,0 / 6,6 / 7,1 / 7,5 / 8,3). **[Sicher]** (Nachbau `modell.py` trifft die Modellzeiten der App auf die Sekunde.)
2. **Am Berg kostet ein Höhenmeter 6,7 bis 13 Flach-Meter**, also 1,3- bis 2,5-mal so viel wie in der App und meist mehr als
   bei Minetti. Die App schätzt deshalb Jungfrau, Zermatt und LGT um 12–13 % zu schnell: Wer flach 3:30 läuft, braucht am
   Jungfrau im Median 4:59 (App 4:20), in Zermatt 4:51 (App 4:14), beim LGT 4:50 (App 4:15). **[Sicher]** (Dabei ist „flach 3:30“
   aus der Pace im flachen Anfang geschätzt, siehe 5.)
3. **Der Preis hängt vor allem davon ab, wie viel man schon gestiegen ist, kaum von der Steigung.** Der frühe LGT-Anstieg
   (12,6 %, frisch) kostet 6,7 m, der Anstieg nach Wengen (16 %, nach 660 Höhenmetern) 8,1 m, das Stück Wengen–Wixi (nur 10 %, aber
   nach 1150 Höhenmetern) 9,5 m, die letzten Abschnitte in Zermatt und am Jungfrau 12–12,5 m. Ein Modell, in dem der
   Bergauf-Aufschlag der App mit den schon gestiegenen Höhenmetern wächst, passt mit 3,9 % mittlerem Fehler je Zelle; ein bloßer
   Faktor auf die App-Kurve nur mit 8,6 %. Ob dahinter Ermüdung, Höhe, Gehen oder schwierige Wege stecken, trennen drei Strecken
   nicht. **[Wahrscheinlich]**
4. **Langsamere verlieren am Berg nur wenig überproportional.** In Flach-Metern (die schon mit dem eigenen Tempo skalieren)
   zahlt die Klasse 3:45–4:45 etwa 3–4 % mehr je Höhenmeter als 3:15–3:45 und knapp 8 % mehr als unter 3:15; die langsamste
   Klasse (über 4:45) liegt wieder im Mittel. Im Ziel macht das 1–2 % aus. Nimmt man für Langsamere die stärkere Ermüdung flacher Marathons an, dreht sich das um.
   Die Laborformel (6–8 m statt 4,2 m für alle) erklärt die Daten nicht: Der Unterschied zur App ist für alle Klassen gleich
   groß. **[Wahrscheinlich]** für „kaum Unterschied“, die Richtung des kleinen Rests ist unsicher.
5. **Gegenprobe Spitze (Teil B):** Bergzeit / flache Marathon-Bestzeit im Median **1,435** (Spanne 1,33–1,48, **7 eindeutige
   Treffer**, 5 Jungfrau, 2 Zermatt). Die App rechnet 1,24 (Jungfrau) bzw. 1,21 (Zermatt). Dieselben Läufer liefen den flachen
   Anfang im Median 6,6 % langsamer, als ihre Bestzeit erwarten ließe (Spanne 0–8,5 %): Am Berg teilt man sich ein. **[Sicher]**
   für die 7, **[Vermutung]**, dass es bei Hobbyläufern ähnlich ist.
6. **Vorschlag:** Bergauf-Aufschlag × (1 + 0,68 × schon gestiegene Höhenmeter / 1000). Stadtmarathons ändern sich um höchstens
   0,4 % (Boston +28 s, New York +33 s bei 4:00 /km), Rennsteig +1,9 %, Brocken +5 %, Zermatt +12 %, LGT +13 %, Jungfrau +14 %.
   Für 3:30 flach: Jungfrau 4:20 → 4:56 (beobachtet 4:59), Zermatt 4:14 → 4:45 (4:51), LGT 4:15 → 4:50 (4:50).

## Daten

Zwischenzeiten aus den öffentlichen Ranglisten von **Datasport** (ohne Anmeldung; Seiten
`results.datasport.com/de/anlass/<anlass>/ranking/list/<liste>`, die Tabelle steht als JSON in der Seite, 200 Zeilen je Abruf,
4 s Pause). `laden.py` übernimmt nur Geschlecht (aus der Liste), Zielzeit und Abschnittszeiten; Namen, Startnummern, Jahrgang
und Verein werden nicht gelesen. Rohdaten lagen nur unter `/tmp` und sind gelöscht. Ins Repo kommen nur Mediane je Zelle
(mindestens 20 Läufer).

| Rennen | Jahre | Zeilen | im Ziel mit allen Zeiten | Messpunkte (km der App) |
|---|---|---|---|---|
| Jungfrau-Marathon | 2024, 2025, 2026 | 11 062 | 10 307 | 3,3 / 5 / 10,4 / 15,1 / 21,1 / 25,9 / 30,7 / 38,5 / Ziel |
| Gornergrat Zermatt Marathon | 2025, 2026 | 877 | 817 | Zermatt 20,6 / Sunnegga 32,0 / Riffelalp 39,1 / Ziel |
| Zermatt Halbmarathon (Gegenprobe) | 2025, 2026 | 1 687 | 1 624 | ab Zermatt auf derselben Linie |
| LGT Alpin Marathon | 2026 | 292 | 286 | Vaduz 10,07 / Steg 25,48 / Ziel |

- Jungfrau 2024–2026 und Zermatt 2025–2026 haben dieselben Messpunkte und Etappennamen; gleiche Strecke angenommen (Jungfrau:
  „Originalstrecke 2024“ des Veranstalters). **[Wahrscheinlich]**
- Jungfrau: die sanften Abschnitte Wilderswil–Zweilütschinen (101 Höhenmeter) und Zweilütschinen–Lauterbrunnen (161) sind
  zusammengefasst; einzeln ergaben sie 2,6 bzw. 7,7 m je Höhenmeter, was eher nach der Lage der Matte bei km 15,1 als nach
  Physik aussieht.
- Zermatt: Bei etwa 100 Läufern ist die Summe der Etappen bis zu 21 s kürzer als die Zielzeit (wohl Startverzug); behalten.
- Nicht verfügbar: LGT vor 2026 und Zermatt 2024 bei Datasport (Seiten nicht gefunden), Jungfrau 2023 ohne Listen.
- Höhen und Kilometer aus unseren App-Daten (`const D`, 10-m-Raster, Höhen aus swissALTI3D), Ermüdung flacher Marathons aus
  [`../zellen.csv`](../zellen.csv) (Berlin, Chicago, Amsterdam, Valencia; Pace Notes, CC BY 4.0).

## Methode

1. **Abschnitte** (`abschnitte.csv`): Länge, Höhenmeter (200-m-Fenster wie in den Übergaben), Höhenmeter je Steigungsklasse und
   Höhenmeter-gewichtete Steigung (100-m-Fenster, wie das Modell rechnet), schon gestiegene Höhenmeter, Faktor der App.
2. **Anker:** flacher Anfang (Jungfrau km 3,3–10,4, ohne die Startrunde; LGT km 0–10,07; Zermatt Start–Zermatt, nicht flach,
   dort mit dem jeweiligen Modell gerechnet). Aus der Anker-Zeit und dem Modell die flache Pace p0 jedes Läufers, daraus die
   **flache Marathon-Äquivalenzzeit** (p0 × 42,195 km, mit der Ermüdung eines 3:15-Läufers: × 1,025). Klassen danach: unter 3:15,
   3:15–3:45, 3:45–4:15, 4:15–4:45, über 4:45. Klassen nach Zielzeit wären verzerrt (wer am Berg schlecht ist, landet hinten).
3. **Je Läufer und Abschnitt** `y = log(Abschnittszeit / Anker-Zeit)`, je Zelle Rennen × Jahr × Klasse × Abschnitt der Median
   (`zellen_berg.csv`).
4. **Ermüdung**, vier Varianten: einheitlich wie ein 3:15-Läufer im flachen Marathon (Hauptvariante), keine, je Klasse nach km
   (wie in der Aufgabe vorgeschlagen), je Klasse nach Anteil an der Zielzeit. **Kontrolle** am flachen Abschnitt Jungfrau
   km 21,1–25,9: beobachtet 0–3,5 % langsamer als im Anker, in allen Klassen ähnlich; die einheitliche Ermüdung sagt 1,3 %, die
   klassenabhängige 1–10 % (für Langsame viel zu viel). Deshalb einheitlich als Hauptvariante, klassenabhängig als Grenzfall.
5. **Wirksame Flach-Meter je Höhenmeter je Abschnitt** (`k_abschnitte.csv`): beobachtete gewichtete Strecke minus Länge minus
   Bergab-Gewinn der App, geteilt durch die Höhenmeter bergauf.
6. **Modelle** (gewichtete kleinste Quadrate über die Zellen, Gewicht √min(n, 200)), verglichen mit mittlerem Fehler je Zelle und
   „Weglassen je Rennen“ (aus zwei Rennen schätzen, am dritten prüfen). Bereiche: 200 Bootstrap-Ziehungen über Läufer innerhalb
   Rennen × Jahr (`ergebnis.txt`, `ergebnis_steigung.csv`).
7. **Teil B:** Für die Top 5 Männer und Frauen von Jungfrau und Zermatt 2026 die flache Marathon-Bestzeit aus öffentlichen
   Profilen (World Athletics, Swiss-Running-Allzeitbestenliste, Siegerliste des Lausanne Marathon, Wikipedia, the-sports.org).
   Nur eindeutige Treffer (Name, Jahrgang und Land passen). Namen nur während der Suche, nirgends gespeichert.

## Ergebnisse

### Flach-Meter je Höhenmeter je Abschnitt und Leistungsklasse

Ermüdung einheitlich (Hauptvariante); Klasse = flache Marathon-Äquivalenzzeit. Leer: weniger als 20 Läufer je Jahr.

| Abschnitt | Steigung | Höhenmeter vorher | App | alle | < 3:15 | 3:15–3:45 | 3:45–4:15 | 4:15–4:45 | > 4:45 |
|---|---|---|---|---|---|---|---|---|---|
| Jungfrau Wilderswil–Lauterbrunnen | 4,8 % | 179 | 4,6 | 5,9 | 5,6 | 5,7 | 5,8 | 6,4 | 6,7 |
| Zermatt Zermatt–Sunnegga | 9,8 % | 896 | 5,0 | 8,2 | 7,1 | 8,1 | 8,1 | 8,5 | 8,3 |
| Jungfrau Wengen–Wixi | 10,2 % | 1152 | 5,1 | 9,5 | 9,0 | 9,7 | 9,7 | 9,3 | 7,8 |
| LGT Steg–Ziel (448 m bergab) | 12,0 % | 1608 | 5,2 | 10,6 | 9,6 | 11,1 | 10,7 | 10,3 | |
| Zermatt Sunnegga–Riffelalp (223 m bergab) | 12,2 % | 1456 | 5,2 | 14,3 | 11,6 | 13,9 | 14,0 | 15,2 | 14,8 |
| LGT Vaduz–Steg | 12,6 % | 721 | 5,3 | 6,7 | 6,3 | 6,9 | 6,7 | 6,7 | |
| Zermatt Riffelalp–Ziel | 15,9 % | 1719 | 5,5 | 12,5 | 12,9 | 12,7 | 12,4 | 12,3 | 12,4 |
| Jungfrau Stocki–Wengen | 16,3 % | 663 | 5,5 | 8,1 | 7,4 | 7,9 | 8,3 | 8,4 | 7,4 |
| Jungfrau Wixi–Ziel | 20,9 % | 1670 | 5,8 | 12,0 | 12,0 | 11,8 | 12,0 | 12,0 | 11,5 |

„Höhenmeter vorher“: Mittel über den Abschnitt. Ohne Ermüdung liegen die Werte 0,1–1,4 m höher (Zermatt Sunnegga–Riffelalp
2,9 m), mit klassenabhängiger Ermüdung für die langsamen Klassen meist 1–3 m tiefer (Sunnegga–Riffelalp bis 5,6 m; `ergebnis.txt`). Sunnegga–Riffelalp und
Steg–Ziel haben viel Gefälle auf Bergwegen; dort steckt im Wert auch, dass bergab weniger zu gewinnen ist als in der App.

**Nach Steigungsklassen allein lässt es sich nicht sauber zerlegen:** Frei geschätzt (monoton, 0–5 % fest wie in der App) fällt
alles auf eine Stufe (4,4 / 4,4 / 11,6 / 11,6 / 11,6, mittlerer Fehler 7,1 %), mit wachsendem Aufschlag bleibt kaum Steigungseffekt
über der App-Kurve (4,4 / 4,6 / 5,6 / 5,6 / 5,6 vor Ermüdung). Was die Daten tragen, ist diese Tafel (Vorschlag, Faktor 0,68):

| schon gestiegen | 5 % | 10 % | 15 % | 20 % | 30 % |
|---|---|---|---|---|---|
| 0 Höhenmeter (= App heute) | 4,6 | 5,1 | 5,4 | 5,8 | 6,4 |
| 500 | 6,2 | 6,8 | 7,3 | 7,8 | 8,6 |
| 1000 | 7,8 | 8,5 | 9,2 | 9,7 | 10,8 |
| 1500 | 9,4 | 10,3 | 11,0 | 11,7 | 13,0 |
| 2000 | 11,0 | 12,0 | 12,9 | 13,7 | 15,2 |
| Minetti (Labor) | 6,0 | 6,6 | 7,1 | 7,5 | 8,3 |

### Modelle im Vergleich

Ermüdung einheitlich, bergab wie die App. Fehler: mittlerer quadratischer Fehler je Zelle (log, in %); „weggelassen“: aus den
beiden anderen Rennen geschätzt, Median des Fehlers am dritten (negativ = Modell zu schnell).

| Modell | Parameter | Fehler je Zelle | weggelassen: Jungfrau / Zermatt / LGT |
|---|---|---|---|
| App-Kurve × a | a = 1,90 [1,89–1,91] | 8,6 % | +8,4 / −18,9 / +6,4 % |
| App × a, ab 10 % zusätzlich steiler („Knick“) | a = 1,60, +2,2 m je 10 % | 8,1 % | +0,8 / −17,9 / +3,6 % |
| App × a, dazu Höhe | a = 1,21, Pace +25,6 % je 1000 m | 5,4 % | +7,2 / −6,5 / +10,5 % |
| App × a, Pace überall langsamer je gestiegene 1000 Höhenmeter | a = 1,19, +19 % | 5,0 % | +4,4 / −4,9 / +11,1 % |
| **App, Bergauf-Aufschlag wächst je 1000 gestiegene Höhenmeter (Vorschlag)** | **+68 % [68–69]** | **3,9 %** | **+1,7 / −6,5 / +3,1 %** |
| dito, dazu Höhe wie Mexiko (2,8 % je 1000 m) | +60 % | 3,8 % | +2,1 / −6,7 / +3,5 % |
| App × a, Aufschlag wächst | a = 1,01, +68 % | 3,9 % | −0,3 / −8,8 / +3,4 % |
| Steigungsklassen frei (monoton), Aufschlag wächst | 4,4 / 4,6 / 5,6 / 5,6 / 5,6 m, +73 % | 3,6 % | +1,4 / −8,3 / +4,5 % |

Lässt man den Faktor auf die App-Kurve frei, landet er bei 1,01: Die Grundkosten der App passen, es fehlt nur der wachsende
Aufschlag. Die freien Steigungsklassen verbessern den Fehler kaum (3,6 statt 3,9 %) bei vier Größen mehr.

Abweichung je Abschnitt (Median über Jahre und Klassen, negativ = Modell zu schnell):

| Abschnitt | App | Vorschlag |
|---|---|---|
| Jungfrau Wilderswil–Lauterbrunnen | −2,8 % | −1,5 % |
| Jungfrau Lauterbrunnen–Stocki (flach) | +0,6 % | +1,1 % |
| Jungfrau Stocki–Wengen | −15,2 % | −1,3 % |
| Jungfrau Wengen–Wixi | −21,1 % | −1,0 % |
| Jungfrau Wixi–Ziel | −39,8 % | +3,0 % |
| LGT Vaduz–Steg | −7,6 % | +3,7 % |
| LGT Steg–Ziel | −18,7 % | +1,0 % |
| Zermatt Zermatt–Sunnegga | −13,9 % | −1,8 % |
| Zermatt Sunnegga–Riffelalp | −20,5 % | −10,5 % |
| Zermatt Riffelalp–Ziel | −40,5 % | −5,4 % |

Zermatt oben (über 2200 m, Bergwege mit Gefälle) bleibt auch mit dem Vorschlag 5–10 % zu schnell.

### Langsamere gegen Schnellere

Faktor auf die App-Kurve bzw. Wachstum des Aufschlags je Leistungsklasse, Differenz zur Klasse 3:15–3:45 mit 95 % aus dem
gepaarten Bootstrap.

| Klasse (flach) | App × a, Ermüdung einheitlich | Aufschlag wächst, Ermüdung einheitlich | App × a, Ermüdung je Klasse (km) |
|---|---|---|---|
| < 3:15 | 1,81 (−0,06 [−0,10; −0,04]) | 0,64 (−0,04 [−0,06; −0,02]) | 1,84 (−0,01 [−0,04; +0,01]) |
| 3:15–3:45 | 1,88 | 0,68 | 1,85 |
| 3:45–4:15 | 1,94 (+0,06 [+0,04; +0,09]) | 0,71 (+0,03 [+0,02; +0,05]) | 1,82 (−0,03 [−0,06; −0,01]) |
| 4:15–4:45 | 1,95 (+0,07 [+0,05; +0,10]) | 0,71 (+0,03 [+0,02; +0,05]) | 1,68 (−0,17 [−0,20; −0,15]) |
| > 4:45 | 1,90 (+0,02 [−0,04; +0,09]) | 0,67 (−0,01 [−0,05; +0,03]) | 1,50 (−0,37 [−0,42; −0,30]) |

Ohne Ermüdung sind die Unterschiede dieselben wie mit einheitlicher (nur das Niveau liegt höher). Die Einteilung nach dem flachen
Anfang verzerrt eher gegen die Vermutung (wer zu schnell anfängt, landet in einer schnelleren Klasse und sieht dort am Berg
schlecht aus); nach Zielzeit eingeteilt sähe der Effekt viel größer aus, wäre aber ein Kunstprodukt.

### Gegenprobe Zermatt-Halbmarathon

Halbmarathonläufer starten in Zermatt frisch auf derselben Linie. Bei gleicher Zeit Zermatt–Sunnegga brauchen sie für
Riffelalp–Ziel relativ **mehr** (0,48–0,53 der Zeit Zermatt–Sunnegga) als Marathonläufer (0,44–0,46), und der Abstand wächst zu
den Langsamen hin. Das Modell mit wachsendem Aufschlag sagt das Gegenteil (Marathon 0,43, Halbmarathon 0,42). Mögliche Gründe:
Halbmarathonläufer gehen frisch zu schnell an, das Feld ist ein anderes (mehr Wanderer). Der Mechanismus „Ermüdung durch
Höhenmeter“ ist damit **nicht bestätigt**; der Faktor ist eine Beschreibung, keine Erklärung. **[Sicher]** für die Zahlen,
**[Vermutung]** für die Gründe.

### Gegenprobe Spitze (Teil B)

| | Treffer | Bergzeit / flache Bestzeit, Median | Spanne |
|---|---|---|---|
| eindeutig, flache Strecke, Ergebnis ab 2021 | 7 (Jungfrau 5, Zermatt 2) | 1,435 | 1,326–1,483 |
| dazu 3 mit älterer (2007, 2018) oder welliger Bestzeit (Lausanne 2019) | 10 | 1,461 | 1,326–1,543 |
| App heute | | Jungfrau 1,238, Zermatt 1,212 | |
| Vorschlag | | Jungfrau 1,41, Zermatt 1,36 | |

Von 20 Plätzen (19 Personen, einer stand in beiden Top 5): 7 eindeutig, 3 nur mit älterer oder welliger Zeit, 2 weggelassen
(Name im Profil anders, Person nicht eindeutig), 8 ohne auffindbare flache Marathonzeit (reine Berg- und Trailläufer). Für die 7
lag die Äquivalenzzeit aus dem Anker im Median 6,6 % (0–8,5 %) über der echten Bestzeit: Sie laufen den flachen Anfang
zurückhaltend, oder die Bestzeit ist älter als die aktuelle Form. Eine Zeit stammt aus einem Rennen nach dem Bergmarathon.

### Prognosen

„flach“ = Marathonzeit aus der Pace im flachen Anfang (±10 min); beobachtet = Median der Zielzeit (Viertel); App und Vorschlag bei
gleichmäßiger Anstrengung. Ganze Tabelle mit allen Modellen: `prognosen.csv`.

| flach | Rennen | Läufer | beobachtet | App | Vorschlag |
|---|---|---|---|---|---|
| 2:30 | Jungfrau | 79 | 3:27 (3:20–3:36) | 3:05 | 3:31 |
| 3:00 | Jungfrau | 607 | 4:17 (4:06–4:28) | 3:42 | 4:13 |
| 3:00 | Zermatt | 38 | 4:07 (3:56–4:16) | 3:38 | 4:04 |
| 3:30 | Jungfrau | 2022 | 4:59 (4:48–5:15) | 4:20 | 4:56 |
| 3:30 | Zermatt | 77 | 4:51 (4:41–4:58) | 4:14 | 4:45 |
| 3:30 | LGT | 48 | 4:50 (4:35–5:08) | 4:15 | 4:50 |
| 4:00 | Jungfrau | 2506 | 5:44 (5:29–6:01) | 4:57 | 5:38 |
| 4:00 | Zermatt | 161 | 5:31 (5:18–5:42) | 4:50 | 5:26 |
| 4:00 | LGT | 68 | 5:26 (5:16–5:40) | 4:52 | 5:31 |
| 4:30 | Jungfrau | 1470 | 6:25 (6:09–6:42) | 5:34 | 6:20 |
| 4:30 | Zermatt | 140 | 6:13 (6:00–6:27) | 5:27 | 6:07 |
| 5:00 | Jungfrau | 83 | 6:49 (6:35–7:02) | 6:11 | 7:03 |
| 5:00 | Zermatt | 85 | 6:52 (6:40–7:06) | 6:03 | 6:48 |

Spitze (Median der 5 Schnellsten je Rennen, Jahr und Geschlecht): Zielzeit / flache Zeit aus dem Anker 1,29–1,36, LGT-Männer
1,23; der Vorschlag rechnet bei 2:30 flach 1,41 (Jungfrau). Die Besten klettern besser als ihre Klasse. Gemessen an der echten
Bestzeit (Teil B: 1,435) liegt der Vorschlag für die Spitze nahe, die App deutlich daneben.

## Grenzen

- **Drei Strecken, 15 Abschnitte.** Steigung, Lage im Rennen, Höhe über dem Meer und Wegbeschaffenheit laufen fast parallel. Die
  „schon gestiegenen Höhenmeter“ stehen für alles zusammen. Weglassen je Rennen: Fehler am weggelassenen Rennen −6,5 % (Zermatt)
  bis +3,1 % (LGT); ehrlich ist ein Faktor zwischen etwa 0,5 und 0,8 statt 0,68 (Varianten der Ermüdung 0,59–0,82).
- **Höhe:** Allein müsste sie 25 % Pace je 1000 m erklären, rund neunmal so viel wie die Regel der App (2,8 % je 1000 m,
  Mexiko-Stadt) und weit über physiologischen Werten. Sie kann nur ein kleiner Teil sein. **[Wahrscheinlich]**
- **Flache Pace aus dem Anker:** Wer den Anfang am Berg zurückhaltend läuft, wirkt im Flachen langsamer, als er ist. Für die Spitze
  sind das 6–7 % (Teil B); für Hobbyläufer ist es nicht gemessen. Gilt es dort ebenso, braucht ein echter 3:30-Läufer am Jungfrau
  eher 5:20 als 4:59. **[Vermutung]**
- **Ermüdung:** Grundlage sind flache Marathons. Die klassenabhängige Variante passt nicht zur Kontrolle bei km 21–26.
- **Bergab** ist kaum bestimmt (Fehler ändert sich zwischen Faktor 0 und 2 nur von 8,4 auf 8,9 %); die App bleibt bei „halb“.
- **Nur Finisher**, Kontrollzeiten schneiden den langsamen Rand ab (Jungfrau: Wengen nach 4:25, Wixi nach 5:50).
- Stau auf schmalen Wegen (Moräne am Jungfrau), Wetter je Jahrgang und die genaue Lage der Matten (Zermatt: Veranstalter-km 21,1
  bzw. 32,4 gegen App 20,6 bzw. 32,0) sind nicht herausgerechnet. Bootstrap-Bereiche erfassen nur die Stichprobe.

## Empfehlung für den Kern

Im Kern (`hamburg/index.html`, `paceRatio`) für Steigungen > 0 den Aufschlag mit den schon gestiegenen Höhenmetern des
Rechenfensters vervielfachen, die es dort schon gibt (`WIN[100].up`):

    ratio[i] = 1 + (paceFaktor(g) − 1) × (1 + 0,68 × WIN[100].up[i] / 1000)   (nur wo g > 0)

- Stadtmarathons bleiben praktisch gleich (`wirkung.txt`: höchstens +0,4 %), die Straßen-Eichung gilt weiter.
- Zu entscheiden: Great Wall (Mauer-Minuten fest, aber ihre Stufen zählen in den Höhenmetern mit), der Berg-Hinweis des Kerns
  („Zeiten zu optimistisch“) und ob die Spitze den Faktor eher bei 0,6 sieht (Klasse < 3:15: 0,64).
- Die Zielzeit plant gleichmäßige Anstrengung; die Läufer am Berg teilen sich ein und sind im Flachen schneller, am Ende
  langsamer als die App. Das ändert der Vorschlag nicht.

## Wiederholen

1. `python3 laden.py /tmp/berg/roh` (etwa 70 Abrufe, 5 Minuten)
2. `python3 auswerten.py /tmp/berg/roh 200 > ergebnis.txt` (etwa 5 Minuten; schreibt `abschnitte.csv`, `zellen_berg.csv`,
   `k_abschnitte.csv`, `ergebnis_steigung.csv`, `prognosen.csv`, `zermatt_halbmarathon.csv`, `parameter.json`)
3. `python3 wirkung.py > wirkung.txt` (alle Strecken bisher und neu)
4. `rm -r /tmp/berg`

`modell.py` liest die Höhen direkt aus den App-Seiten; der Nachbau des Kerns (Stand 2.7) trifft die Modellzeiten der App bei
4:00 /km auf die Sekunde (Jungfrau 3:29:01, Zermatt 3:24:31, LGT 3:25:32).
