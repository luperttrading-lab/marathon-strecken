# Übergabe: Steigungsprofil Hamburg-Marathon

Stand 27.10.2026, App-Version **1.57** (1.57: flacher Halbmarathon in der Tabelle ohne Höhenmeter, Erklärung im Info-Fenster (i); 1.56: Kosten je Höhenmeter bei 4:00 /km mit wählbarer Bezugs-Pace, Bahnzeiten als Tabelle, größere Überschriften in den Einstellungen; 1.55: unter der Zielzeit flacher Marathon und Bahnzeiten 10 000 m / 5000 m; 1.54: Zeiten immer mit 100 m, „Pace hier“ über das Messfenster gemittelt; 1.53: Messfenster 50 / 100 / 200 m / 1 km statt 10 m, neuer Erklärtext; 1.52: Zwischenzeiten mit Halbmarathon-Zeile und „je 10 km“; 1.51: Knopfrahmen so hell wie die Räder, „Vollbild“ blau, im Vollbild führt ‹ zurück in die normale Ansicht; 1.50: Kopf eines offenen Abschnitts bleibt oben stehen, Zuklappen von überall; 1.49: beim Aufklappen bleibt der Kopf des Abschnitts an seiner Stelle; 1.48: Hinweis, wenn die eingestellte Startzeit zu keiner Welle passt; 1.47: Standard 5 km Ausschnitt und Tempo ×200, Menü-Knopf blau mit Beschriftung, Abschnitte unter dem Läuferblick aufklappbar; 1.46: Startwellen mit Uhrzeiten unter „Deine Startzeit“; 1.45: Pfeile in Bisher/Noch/Ganze Strecke und Rampe als Grafik, dreistellige Werte ohne „…“, zu breite Werte werden kleiner; 1.44: Bergab U-Kurve statt Grenze bei −4 %: am schnellsten bei −8 %, ab −16 % langsamer als flach, ohne Knick bei 0 %; 1.43: Tempo-Rad mit ×1 (Echtzeit), ×50 und ×100–×180 in 20er-Schritten; 1.42: Brücken-Beschriftungen überlappen nicht mehr; 1.41: Kästchen bunt/grau neben der Gesamtstrecke, Diagramm „So rechnet das Pace-Modell“; 1.40: Ortsname bei Uhrzeiten aus `D.ort`, für Boston, sonst unverändert; 1.39: Seite springt beim Drehen an Zielzeit und Startzeit nicht mehr; 1.38: Höhenangaben mit dunklem Schein statt Kasten; 1.37: Höhenangaben auf Schildern lesbar, Straßennamen in eigener Zeile unter der km-Skala; 1.36: Gesamtstrecke unten mit feiner weißer Linie und Schalter farbig/einfarbig, die drei hellsten Bergab-Blau weniger türkis; 1.35: Farben fest (bergauf Rot bis Aubergine, bergab Blau), Dreieck unter der Skala, nur noch dunkel; 1.34: geschätzte Brücken schraffiert statt abgedunkelt; 1.33: Steigungszahl ohne Farbe; 1.32: Steigungszahl immer lesbar; 1.31: Schalter Blautöne bergab auto/tief/leicht; 1.30: Blauverlauf bergab dunkler beginnend, Ende Marineblau; 1.29: nur flach grün, bergab sieben Blautöne; 1.28: Zeiger als Dreieck über der Skala, Varianten 1–4 mit Grün und Blauverlauf bergab; 1.27: Farbvarianten A, 1–4 und Schalter für flach; 1.26: Farbwahl auch im Vollbild, Hilfslinien mindestens 18 px auseinander; 1.25: Farbvarianten A–E zum Testen unter der Legende; 1.24: Text über den Zwischenzeiten nennt auch die Kosten steiler Anstiege; 1.23: Höhenachse in gröberen Schritten bei großem Höhenbereich, hier ohne Wirkung), live unter https://luperttrading-lab.github.io/marathon-strecken/hamburg/.
Auf dem iPhone wird nur noch die gemeinsame App „Marathon“ installiert (siehe „Mehrere Strecken“).

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
  gilt eine feste Höhe für beide Seiten). Laufende Zahlen im Canvas (Uhrzeit, Pace im Profil) zeichnet `tabText` Ziffer für
  Ziffer in gleich breite Zellen, weil es im Canvas kein `tabular-nums` gibt (seit 1.21).
  Beim Drehen an Zielzeit, Kosten je Höhenmeter und Startzeit hält `mitAnker` das Rad an seiner Stelle (seit 1.39):
  Text darüber nennt die Zeit und kann umbrechen (bei 375 px Breite z. B. „Bei Zielzeit 2:00:00 …“ zwischen zwei und
  drei Zeilen), und Safari hat keine Scroll-Verankerung, also sprang die Seite unter dem Finger.
- **Start im Vollbild** (Klasse `body.run`): Anzeige, Läuferblick, Übersicht und Steuerung auf einem Bildschirm.
  ☰ führt zu Zwischenzeiten, Einstellungen, Rampen und Quellen.
- **Anzeige oben hat zwei wischbare Seiten: Zahlen und Karte.** Fotoseiten (Wikimedia, Sehenswertes, Straßenfotos
  „Blick voraus“ von Panoramax) wurden gebaut und **ausdrücklich wieder entfernt**.
- **Drehräder senkrecht** (wie die Zielzeit), Variante „drei Zeilen, knapp angeschnitten“, 52 px hoch,
  Ausschnitt 0,5–10 km in 0,5er-Schritten, Tempo ×1 (Echtzeit), ×50, ×100–×200 in 20er-Schritten, dann bis ×1000 in 100er-Schritten (`SPEEDS`; seit 1.43). Ränder und Nachbarzahlen kontrastreich. Voreinstellung seit 1.47: 5 km und ×200 (vorher 2 km
  und ×300); gespeicherte Werte bleiben.
- **Menü-Knopf** (seit 1.47, rechts neben den Rädern im Vollbild, `#run-close`): blau gefüllt mit ☰ und „Menü“; das
  schmale ☰-Zeichen davor übersah der Nutzer. Führt zu den Abschnitten unter dem Läuferblick.
- **Vollbild ein und aus** (seit 1.51): „Vollbild“ in der normalen Ansicht ist blau wie „Menü“. Im Vollbild führt der Pfeil
  oben links (`.corner.back`) zurück in die normale Ansicht (nach oben), in der normalen Ansicht zu allen Strecken.
  Knopfrahmen allgemein `--edge` statt `--rule`, so hell wie die Räder.
- **Aufklappbare Abschnitte** (seit 1.47): Zwischenzeiten, Für Zuschauer, Einstellungen, Rampen, Woher die Zahlen kommen
  (`section.klapp`, `data-t` Titel, `data-h` Inhaltsangabe). Beim ersten Besuch alle zu, danach wie zuletzt (store
  `klapp-<k>`). Der Inhalt wandert in `.klapp-inhalt`; beim Öffnen setzt `syncGoalWheels` die Räder und `renderSplits`
  die Spark-Linien neu, weil beide im zugeklappten Zustand keine Größe haben. Seit 1.49 bleibt der Kopf beim
  Auf- und Zuklappen an seiner Stelle (`mitAnker`, `overflow-anchor: none`): Safari hielt vorher die Abschnitte darunter
  fest, der geöffnete Abschnitt rutschte nach oben weg und man sah nur sein Ende. Seit 1.50 bleibt der Kopf eines offenen Abschnitts beim
  Scrollen oben stehen (sticky); Zuklappen geht von überall, danach steht der zugeklappte Kopf an derselben Stelle und darunter
  die übrigen Abschnitte wie vorher. Seite zugeklappt 1,6 statt 5,8 Bildschirme.
- **Voreinstellung der Zielzeit (seit 1.13): genau 4:00 /km im Flachen**, damit „Pace hier“ und die Kilometerzeiten die
  Abweichung durch das Höhenprofil gegenüber 4:00 zeigen. Die Zielzeit enthält dann die Kosten des Profils und ist je
  Strecke verschieden: Hamburg 2:50:01, Berlin 2:49:24, Frankfurt 2:49:31 (nicht 2:48:46,8 – das wäre 4:00 im Schnitt).
  Speicherschlüssel `goal-v2`; frühere Einstellungen (`goal-s`) werden bewusst nicht mehr gelesen.
- **Zielzeit sekundengenau per Drehrad.** Ein Rad übernimmt erst nach Berührung und nach dem Einrasten den sichtbaren
  Wert (iOS rollt nach dem Loslassen weiter; das hatte einmal zu falschen Zeiten geführt).
- **Pace-Modell:** Minetti et al. (2002), skaliert auf die Erfahrung des Nutzers: **1,0 s je Höhenmeter bei 4:00 /km** (= 15 km/h; seit 1.56 so beschriftet, weil Läufer im Schnitt denken)
  (= 4,2 m flache Strecke je Höhenmeter; Minetti ergibt 5,4 m bzw. 1,3 s). Einstellbar 0,5–2,0 s.
  Bergab seit 1.44 eine U-Kurve (`BERGAB`, abgestimmt mit dem Nutzer im „Pace-Kurven-Simulator“, einem privaten Artifact,
  an Felddaten aus 20 belgischen Trailrennen, Jidovtseff und De Cock 2026, und Stravas Herzfrequenzmodell): bei **halb**
  (Standard) anfangs die halbe Bergauf-Steigung, am schnellsten bei −8 % (12 % schneller als flach, 3:31 bei 4:00), bei
  −16 % wieder so schnell wie flach, steiler immer langsamer (Parabel und Kubik je zur Hälfte, −20 %: 4:52). „voll“
  verdoppelt die Abweichung vom Flachen, „gar nicht“ rechnet bergab wie flach. Auf ±1 % rundet ein Hermite-Übergang den
  Knick bei 0 ab (Steigung dort: Mittel beider Seiten); das macht jede Strecke rund 10 s schneller, weil die häufigen
  Steigungen um 0 % etwas weniger kosten. Bis 1.43: halber Minetti-Gewinn, ab −4 % kein weiterer.
  Die 1,0 s gelten für sanfte Anstiege; Minetti ist konvex, bei 5 % kostet ein Höhenmeter 1,1 s, bei 8 % 1,2 s. Seit 1.24
  nennt der Text über den Zwischenzeiten den Wert bei 8 % (`kostHm`), weil „+43 m, +48 s“ sonst wie ein Rechenfehler aussah.
- **Messfenster der Steigung** 50 m / 100 m / 200 m (Standard) / 1 km. Höhenmeter hängen stark davon ab:
  159 / 150 / 136 / 80 m; eine Tabelle dazu steht in der App unter „Woher die Zahlen kommen“. Bis 1.52 gab es 10 m
  statt 100 m; 10 m lag auf allen Strecken nur 5–13 Hm über 50 m (Daten schon geglättet), flackerte aber doppelt so oft.
  200 m bleibt Standard (Nutzer, 29.10.2026): ruhigere Anzeige (Farbwechsel je km z. B. Hamburg 9,2 bei 50 m, 4,1 bei
  200 m), Nahtstellen geschätzter Tunnel und Brücken werden nicht zu Rampen. Durchgehende Anstiege zählen bei jedem
  Fenster fast gleich; der Unterschied kommt von Senken und Buckeln unter etwa 200 m Länge.
  **Seit 1.54 getrennt** (Nutzer, 29.10.2026): Pace, Zeiten, Zielzeit-Kosten und Rampenkosten rechnen immer mit
  `RECHEN = 100` m, damit kurze Wellen mitkosten (bergab „halb“: eine Welle kostet netto, das 200-m-Fenster zählte sie
  als flach, Jensen-Lücke der konvexen, schiefen Pace-Kurve). Das Messfenster steuert nur die Anzeige: Steigung, Farben,
  Höhenmeter, Rampen und `P.glatt` = „Pace hier“, gemittelt über das Fenster aus `P.t` (Zeit für das Stück um die Stelle
  geteilt durch seine Länge; das Mittel lässt die Summe gleich). Auch das Abspielen läuft mit `P.glatt`.
  Unruhe von „Pace hier“ (Summe der Änderungen je km): Hamburg vorher 36 s/km bei 200 m, 57 bei 100 m, jetzt 30.
  Steigungskosten bei 2:50 jetzt z. B. Hamburg 72 s (vorher 64), Boston 88 s (61), London 53 s (35).
- **Flacher Marathon und Bahnzeiten** (seit 1.55, Nutzer 29.10.2026): Unter der Zielzeit steht, welchem flachen Marathon
  die Zielzeit entspricht (`P.p0 × 42,195`), darunter 10 000 m und 5000 m auf der Bahn. Faustregel des Nutzers
  Marathon = 10 km × 4,667; das ist Riegel T₂ = T₁ · (D₂/D₁)^k mit k = 1,070, 5000 m daher 10 km · 0,5^k. Nur Ausgabe:
  Ein Referenzrennen als Eingabe hat der Nutzer verworfen, weil man dessen eigenes Höhenprofil bewerten müsste;
  Halbmarathon fehlt bewusst (nicht auf der Bahn). Flach-Pace bleibt auf ganze Sekunden gerundet (Nutzer).
  Für Freizeitläufer ist Riegel beim Marathon oft zu optimistisch (Vickers & Vertosick 2016: bei etwa der Hälfte
  10 min oder mehr zu schnell), deshalb der Hinweis im Text.
  Seit 1.56 als Tabelle mit großen Zahlen (`#bahn`: Flacher Marathon, 10 000 m, 5000 m auf der Bahn), weil der Nutzer
  die Zeiten im Fließtext nicht gefunden hat. Seit 1.57 mit „Flacher Halbmarathon“ (Marathon / 2^k, Wunsch des
  Nutzers, ohne „Bahn“) und die Erklärung nicht mehr als Text, sondern im Info-Fenster: Knopf (i) neben „Ohne
  Höhenmeter entspricht das“ öffnet `#bahn-info` als HTML-Popover (Safari ab 17), sonst per Klasse `offen`.
  Höhenmeter nie als „HM“ abkürzen: unter Läufern heißt HM Halbmarathon.
- **Kosten je Höhenmeter mit Bezugs-Pace** (seit 1.56, Nutzer 29.10.2026): zwei Räder „Sekunden“ und „Pace /km“
  (3:00–7:00 in 5-s-Schritten, Standard 4:00). Eingabe `S.secRef` bei `S.ref` (Speicher `sechm`, `sechm-pace`),
  gerechnet wird mit `S.secHm = S.secRef · 240 / S.ref` (Sekunden bei 4:00 /km), weil der Höhenmeter einer festen
  flachen Strecke entspricht (4,2 m bei 1,0 s) und seine Zeit mit der Pace wächst. Die Pace ändert also das Modell:
  1,0 s bei 5:00 /km ist weniger als 1,0 s bei 4:00 /km.
- **Überschriften in den Einstellungen** (seit 1.56): `.setting .head .lbl` 15 px in `--ink` statt 12 px grau, weil
  „Zielzeit“ zu klein wirkte; lange Überschriften brechen um, die Knöpfe daneben rutschen dann in die nächste Zeile.
- **Höhenachse** (seit 1.23): Hilfslinien alle 5 m, ab 30 m Höhenbereich alle 10 m, ab 100 m alle 25 m, ab 200 m alle
  50 m (höchstens ~8 Linien); seit 1.26 außerdem mindestens 18 px Abstand, sonst die nächste Stufe (kleine iPhones im Vollbild). Der Bereich gilt für die ganze Strecke, nicht je Ausschnitt. Über 100 m reicht bisher nur
  der Rennsteig (180 m, Linien alle 25 m). Höhenangaben seit 1.38 hell mit dunklem Schein nach
  unten und feiner Kontur (`textSchein`), sonst waren sie auf den Steigungsfarben kaum lesbar (1.37 mit Schild in
  der Grundfarbe: dem Nutzer zu kastig); ein Wert, der oben in eine
  Markenbeschriftung wie „Halbmarathon“ liefe, entfällt. „Brücke“ bei geschätzten Stücken steht über der Kurve.
- **Farbklassen der Steigung** (seit 1.35 fest, `CLASS_EDGES` / `CLASS_FARBE` im Skript; Wahl des Nutzers nach
  Testvarianten 1.25–1.34): gespiegelte Grenzen ±0,5 / 1,5 / 3 / 4,5 / 6 / 8 / 10, 15 Klassen. Flach (±0,5) grün;
  bergab sieben Blautöne von Himmelblau bis Marineblau, die dunkler werden (Helligkeit L 0,74 → 0,31, die Mitte
  zwischen den Testsätzen „tief“ und „leicht“; seit 1.36 die drei hellsten weniger türkis, OKLCH-Farbton
  245 / 251 / 255 statt 230 / 240 / 248 bei gleicher Helligkeit); bergauf gelb (0,5–1,5), orange (1,5–3), dann Rot über Bordeaux bis
  Aubergine (3–4,5 / 4,5–6 / 6–8 / 8–10 / ≥ 10). Benachbarte Stufen liegen in ΔE (OKLab ×100) bei 6,7–9,2 bergab
  und 6,8–10 in den dunklen Bergauf-Stufen: mit Legende gut, aus dem Augenwinkel nur grob unterscheidbar.
  Die CSS-Tokens `--g-u1…u3` bleiben für Zieltitel, Konfetti und den roten Live-Punkt.
- **Steigungsskala**: ein Feld je Klasse, darunter ein schmales **Dreieck**, dessen Spitze nach oben auf die aktive
  Farbe zeigt (`gaugePos`, anteilig im Feld). Darüber stieß es ans Komma der Zahl (bis 1.34). Die große
  Steigungszahl ist ohne Farbe (seit 1.33): in Klassenfarbe verschwand Marineblau im Dunkeln.
- **Gesamtstrecke unten** (seit 1.36): feine weiße Linie auf der Höhe (0,75 px, `--ink`), damit die Form auch über
  Marineblau und Aubergine klar bleibt. Umschaltbar farbig (Standard) / einfarbig (`OV_EIN`, Speicherschlüssel
  `ov-einfarbig`): seit 1.41 mit dem Kästchen rechts neben der Übersicht (Wunsch des Nutzers). Es zeigt den Zustand nach
  dem Antippen: grau, solange sie bunt ist, in Regenbogenfarben, solange sie grau ist. Der Schalter in den Einstellungen
  ist damit entfallen.
- **Diagramm „So rechnet das Pace-Modell“** (seit 1.41, Einstellungen nach „Bergab-Gewinn“): Pace je Steigung, seit 1.44
  von −20 bis +10 % bei der eigenen Pace im Flachen, App (`paceFaktor`) gegen Labormodell (Minetti unverändert, unten
  abgeschnitten), graue Zone steiler als `UNSICHER` (−8 %), wo Strava und Felddaten auseinanderliegen, Punkt an der
  Steigung der aktuellen Stelle. Der Text nennt die Pace bei +5, +10 und −4 %, das Minimum und wie viele km steiler als
  −8 % sind (nur Rennsteig: 2,0 km, Messfenster 200 m). Profilkosten bei 2:50:00 gegenüber 1.43: Boston −21 s, Sydney
  −19 s, New York −15 s, Kapstadt −14 s, flache Strecken −7 bis −12 s (Rundung bei 0 %), Rennsteig −57 s. Die Einstellung
  „Bergab-Gewinn“ wiegt weiter viel mehr als die Form der Kurve.
- Wasser/Verpflegung und Staffelwechsel standardmäßig **aus**, einschaltbar. Halbmarathon-Marke immer sichtbar.
- Straßennamen seit 1.37 in eigener Zeile unter der km-Skala (vorher am Fuß der Fläche, wo Kurve und Farben sie auf
  flachen Stücken überdeckten, z. B. New York km 22–23), aktuelle Straße blau. Welche Namen gezeigt werden, entscheidet `roadLabels` einmal je
  Maßstab über die ganze Strecke, nie je Position: sonst springen sie beim Abspielen (so bis 1.8). Ein Name bleibt am
  linken Rand stehen, bis das Ende seiner Straße ihn hinausschiebt. Ist das Profil unter 180 px hoch (Kartengröße-Stufen 2 und 3,
  kleine iPhones schon ab Stufe 1), entfällt die Zeile, damit die Kurve den Platz behält (seit 1.3, Wunsch des Nutzers).
- **Startzeit Hamburg** (`D.start` = 510, 8:30 Uhr): Seit der 40. Ausgabe 2026 startet der Marathon eine Stunde früher als bis
  2025 (9:30), in zwei Wellen an Karolinenstraße und Bei den Kirchhöfen; der Halbmarathon läuft nachmittags um 14:00 (Mitteilung
  des Veranstalters vom 30.04.2025, haspa-marathon-hamburg.de, „Save the date“). Uhrzeit der zweiten Welle nicht veröffentlicht;
  für 2027 (25.04., `D.termine`) beim Veranstalter prüfen, sobald der Zeitplan steht.
- **Für Zuschauer** (seit 1.19, Abschnitt unter den Zwischenzeiten): Startzeit mit zwei Rädern (`start`, Minuten ab
  Mitternacht, Voreinstellung `D.start`), Uhrzeit an Start, jeder 5-km-Marke, 21,1 und Ziel mit Straße. „Plan teilen“
  schickt `…/<strecke>/?ziel=3:45:00&start=9:35`; der Link übernimmt beides nur für den Besuch (nichts gespeichert) und
  startet am Renntag (`D.termine`) gleich „Live nach Plan“: Der Punkt steht jede Sekunde dort, wo der Läufer laut
  Pace-Modell gerade ist, der Abspielknopf zeigt „Start 9:35“ bzw. „● Live“; Antippen oder Wischen beendet es.
  Uhrzeiten in der Zeitzone der Strecke (`D.tz`), mit Hinweis auf den Unterschied zur Uhr des Betrachters am Renntag.
- **Startwellen** (seit 1.46, alle Strecken): `D.wellen = { q, w: [[Name, Minuten ab Mitternacht, Blöcke oder „ca.“], …] }`.
  Unter „Deine Startzeit“ setzt je Welle ein Knopf die Startzeit (Räder, Plan, Live, geteilter Link); gedrückt ist die
  Welle, deren Zeit eingestellt ist. Darunter `q`: Jahr und Quelle der Zeiten. Ohne Wellenzeiten (London nur per E-Mail,
  Paris 2027 offen, Tokio/Oberelbe/Rennsteig ein Start) nur der Hinweis. Zeiten recherchiert am 29.10.2026 (Seiten der
  Veranstalter, Teilnehmer-PDFs); für jedes neue Jahr prüfen. `D.start` ist die erste Welle der Läufer.
- **Pace-Band** (seit 1.19, Knopf unter den Zwischenzeiten): Bild 1170 × 2532 (Sperrbildschirm, oben Platz für die Uhr),
  km 1–42,2 in zwei Spalten: Gesamtzeit, Zeit für den km, Sekunden gegenüber flach (orange langsamer, blau schneller).
  Wird synchron erzeugt und über das Teilen-Menü übergeben (iPhone: „Bild sichern“).
- **Jeder Start bei km 0** (seit 1.18): Die Stelle wird nicht mehr gespeichert. Nur der Neustart nach einem Update
  behält sie, einmalig über `sessionStorage` (`hhm-pos`). Einstellungen (Zoom, Zielzeit, Karte …) bleiben gespeichert.
- **Knopf zum Start** (seit 1.18): kleiner Knopf ganz links in der Knopfleiste (Strich mit Dreieck), bei km 0
  abgeblendet, nie ausgeblendet. Die sechs Knöpfe teilen sich auch außerhalb des Vollbilds eine Zeile.
- **Uhrzeit im Läuferblick** (seit 1.20): vor der Pace im selben Feld oben rechts die Uhrzeit an dieser Stelle
  (Startzeit + Plan); bei „Live nach Plan“ mit rotem Punkt die aktuelle Uhr an der Strecke. Das Feld ist deckend
  (seit 1.22), sonst scheinen Beschriftungen wie „Ziel“ durch. Zusatz „NY“ bzw.
  „Ortszeit“, wenn der Betrachter am Renntag in einer anderen Zeitzone ist.
- **Pace im Läuferblick** (seit 1.17): klein oben rechts im Profil die Pace an der aktuellen Stelle und dahinter die
  Abweichung zur Pace im Flachen (wie „Pace hier“, z. B. „4:38 +38 s“), auf halbdurchsichtiger Fläche, feste Spalten.
- **Übersicht auf der Karte** (seit 1.14): „−“ eine Stufe unter z12 zeigt die ganze Strecke, passend zur Kartengröße und
  mittig (rechts Platz für die Knöpfe); die Karte folgt dann nicht dem Läufer, der Punkt wandert. Kartenstücke z11 aus
  `werkzeuge/tiles_z11.py <strecke>`. `mapz` 11 = Übersicht.
- **Zwischenstufen zwischen Übersicht und z12** (seit Hamburg 1.15, Berlin 1.3, Frankfurt 1.4, New York 1.1): `mapStufen(w, h)`
  setzt so viele Stufen ein, dass kein Schritt größer als Faktor 2 ist (`k = ceil(12 − Übersicht) − 1`, gleichmäßig verteilt).
  Hängt von Streckenausdehnung und Kartengröße ab: New York 1–2, Hamburg und Berlin bei kleiner Karte 1, Frankfurt keine.
  Zwischenstufen folgen dem Läufer und zeichnen mit den z11-Stücken. Gespeichert in `mapz-v2` (`"ov"` = Übersicht, sonst Zoom);
  die alte Einstellung `mapz` wird beim ersten Start übernommen.
- **Kein Grau am Kartenrand** (gleiche Versionen): Ab z12 steht der Läufer in der Mitte; das feste Rechteck um die Strecke
  (±0,012° / ±0,02°, in z13 nur ~115 px) reichte an Start, Ziel und Außenkurven nicht (New York z12 am Start bis 42 % grau,
  Frankfurt bis 29 %, Hamburg bis 13 %). `werkzeuge/tiles_rand.py <strecke> [Rand z11]` baut z11–z13 neu: bisherige Fläche
  plus ein Kachelrand entlang der ganzen Strecke (z11 bei New York zwei Kacheln für die tiefen Zwischenstufen), schreibt
  `D.tiles` und die Kartenliste in `sw.js`. Geprüft für jede Stufe alle 250 m bei 390 und 430 px Breite und beiden Kartengrößen: 0 % grau.
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
- **Nur dunkel** (seit 1.35, Wunsch des Nutzers: der helle Grund war zu hell, und jede Farbe brauchte einen zweiten
  Satz). Der Kopf setzt `applyTheme("dark")`, Sonne/Mond und die hellen Kartenbilder sind entfernt, die
  Kartenwerkzeuge erzeugen nur noch `karte-dunkel-…`; Service Worker mit neuem Cache-Namen `…-marathon-profil-2`,
  damit der alte Cache samt hellen Bildern gelöscht wird. Die hellen CSS-Werte stehen noch im Stil, wirken aber nicht.
- Bis 1.34: **Hell/Dunkel-Umschalter** (Sonne/Mond) links oben in der Anzeige, **Versionsnummer** rechts oben (nur Vollbild).
  Beide liegen absolut im Leerraum über „Kilometer“ und „Höhe“ und schieben nichts. Der Umschalter wechselt zum
  Gegenteil des Sichtbaren; landet er dabei auf der Systemeinstellung, folgt die App wieder dem System
  (`localStorage` `hhm-theme`, gesetzt im Kopf vor dem ersten Zeichnen). Versionstext kommt aus `APP_VERSION`.
- **Farben** (seit 1.6, in 1.7 nachgedunkelt): Hell gedämpft, kein reines Weiß (`--surface` #e2e7eb, `--bg` #cdd5dc,
  `--muted` #4f5f6c), weil es blendete. Die Strecke auf der Karte hat einen Rand im Gegenton (`--ink`: hell dunkel,
  dunkel hell, seit 1.8), sonst verschwinden die flachen grauen Abschnitte im Kartengrund. Dunkel bleibt bewusst dunkler: die Strecke hebt
  sich dort besser ab.
  Kartenuntergrund wird nach dem Zeichnen der Kacheln getönt: dunkel per `screen` aufgehellt, hell per `multiply`
  abgedunkelt (Farbwert `--map-tint` in CSS, seit 1.9). Die Kachel-JPGs selbst sind unverändert. Ob hell oder dunkel
  gezeichnet wird (`isDark`), richtet sich nach `--surface`, nicht nach `--bg`. Farbe für „flach“ im Hellen #9ba7b2
  (seit 1.10, vorher zu hell). **Offen:** Der Nutzer mag den hellen Hintergrund nicht; sechs Varianten (Papier, Grau,
  Salbei, Nebelblau, dunkler Rahmen) liegen ihm zur Auswahl vor.
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
   Danach `../../tiles_rand.py <strecke>` (z11–z13 mit Streckenrand, siehe oben).
7. `digit.py` hat das ursprüngliche Profilbild des Nutzers ausgelesen (Kalibrierung ±1,4 m). Es zeigt einen
   **älteren Kurs** (Staffelwechsel 16,3/27,7/32,7 statt 15,4/27,2/32,4), die Form stimmt mit dem DGM überein.
8. `pwa_build.py` hat aus der damaligen Artifact-Fassung die App gebaut. **Nur noch historisch** – die Artifact-Fassung
   ist gelöscht, gearbeitet wird direkt in `hamburg/index.html`.

## Mehrere Strecken (seit 1.11)

- Startseite mit Auswahl im Hauptordner (`index.html`, eigene Version), Frankfurt unter `frankfurt/` mit demselben Code.
  Regeln für beide Apps stehen im README im Hauptordner.
- Blauer Pfeil ‹ ganz links oben in der Anzeige (vor Sonne/Mond, seit 1.12, auch im Vollbild) und Link
  „‹ Alle Strecken“ im Kopf der Normalansicht führen zur Startseite.
- **Nur eine App** (Entscheidung des Nutzers, 27.10.2026, Hamburg 1.16): Die Strecken haben kein eigenes Manifest und
  kein eigenes Symbol mehr, sondern verweisen auf `../manifest.webmanifest` und `../apple-touch-icon.png`
  (Titel „Marathon“). *Zum Home-Bildschirm* installiert damit auch aus einer Strecke heraus immer die ganze App
  (Start auf der Startseite, Scope Hauptordner). Ein früher nur aus `hamburg/` installiertes Symbol bleibt die alte
  Einzel-App: löschen und neu hinzufügen.
- Hell/Dunkel gemeinsam über `marathon-theme` (Rückfall auf das alte `hhm-theme`).
- Service Worker löscht nur Caches mit Präfix `hh-`: vorher hätte jede Aktivierung die Offline-Speicher der anderen
  Apps derselben Adresse gelöscht (gilt auch für andere Repos unter luperttrading-lab.github.io, die noch so arbeiten).
- Brückenbeschriftung allgemein nach `kind` (Brücke, Tunnel, Unterführung).
- Geschätzte Abschnitte (Brücken, Tunnel, Rampen): gestrichelte Oberkante, darunter seit 1.34 **schraffiert** statt
  abgedunkelt; mit den dunklen Farben für steil bergab sah ein abgedunkeltes Stück wie ein steiles Gefälle aus (NYC km 2,7).

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
