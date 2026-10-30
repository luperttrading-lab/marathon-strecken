# Übergabe: Steigungsprofil München-Marathon

Stand 30.10.2026, App-Version **1.57** (1.57: Offline-Laden aller Strecken aus 1.78 zurückgenommen (Nutzer: erstmal nur die Meldung), dafür Meldung „Offline: gespeicherte Fassung, vielleicht nicht die neueste“; 1.56: alle Strecken offline: Seiten beim Öffnen der Startseite, Kartenbilder beim Öffnen der Strecke oder per Knopf; 1.55: offline nur noch aus dem eigenen Speicher, Rückfallseite bei jedem Besuch erneuert (Service Worker); 1.54: im Ziel 42,195 statt 42,2 in Anzeige, Gesamtstrecke, Zwischenzeiten und Pace-Band; 1.53: Maßstab auf der Karte ohne Kasten, kleiner, in der freieren linken Ecke; 1.52: im Vollbild der Ort groß oben rechts statt am Pfeil, Maßstab auf der Karte; 1.51: Kopf mit Ort groß und „Streckenplan und Steigungsprofil“, Umschalter Karte | Zahlen statt Pünktchen, Karte zuerst, Name der Strecke im Vollbild; 1.50: zu breite Tabellen werden stufenweise enger statt rechts abgeschnitten; 1.49: Mauer-Beschriftung in einer freien Zeile über dem Profil, mittig über der Mauer, nur bei `D.mauer`; 1.48: Mauer-Beschriftung im Profil neben dem Gipfel statt darauf, nur bei `D.mauer`; 1.47: Mauer je Durchgang ein Rad mit Empfehlung nach Zielzeit, nur bei `D.mauer`; 1.46: Mauer-Zeit und Tor-Rechner für Strecken mit `D.mauer`, sonst unverändert; 1.45: Steigungskosten als große Zeile unter der Zielzeit; 1.44: Umschalter Höhe/Meereshöhe für die Tabelle „Ohne Höhenmeter“, nur bei `D.lage`; 1.43: Feld `D.lage` für hoch gelegene Strecken: Tabelle „Ohne Höhenmeter“ nennt dann die Höhe; 1.42: unter der Zielzeit Pace auf flachen Stücken und im Schnitt; 1.41: Pace im Flachen mit zwei Nachkommastellen; 1.40: weißer Punkt im Pace-Diagramm ist der Flachpunkt 0 % mit Flach-Pace statt der aktuellen Stelle; 1.39: Markierung im Pace-Diagramm stufenlos und ohne Wackeln, Tippen daneben nimmt sie weg, Punkt „hier“ mit km; 1.38: Markierung im Pace-Diagramm auch waagerecht zur Pace-Achse; 1.37: Pace-Diagramm ohne Laborlinie und graue Zone, −15 bis +10 %, Achse bei 0 %, Markierung zum Antippen; 1.36: Bergab fest „halb“ ohne Schalter, steiler als −8 % kein weiterer Gewinn statt U-Kurve; 1.35: flacher Halbmarathon in der Tabelle ohne Höhenmeter, Erklärung im Info-Fenster (i); 1.34: Kosten je Höhenmeter bei 4:00 /km mit wählbarer Bezugs-Pace, Bahnzeiten als Tabelle, größere Überschriften in den Einstellungen; 1.33: unter der Zielzeit flacher Marathon und Bahnzeiten 10 000 m / 5000 m; 1.32: Zeiten immer mit 100 m, „Pace hier“ über das Messfenster gemittelt; 1.31: Messfenster 50 / 100 / 200 m / 1 km statt 10 m, neuer Erklärtext; 1.30: Zwischenzeiten mit Halbmarathon-Zeile und „je 10 km“; 1.29: Knopfrahmen so hell wie die Räder, „Vollbild“ blau, im Vollbild führt ‹ zurück in die normale Ansicht; 1.28: Kopf eines offenen Abschnitts bleibt oben stehen, Zuklappen von überall; 1.27: beim Aufklappen bleibt der Kopf des Abschnitts an seiner Stelle; 1.26: Hinweis, wenn die eingestellte Startzeit zu keiner Welle passt; 1.25: Standard 5 km Ausschnitt und Tempo ×200, Menü-Knopf blau mit Beschriftung, Abschnitte unter dem Läuferblick aufklappbar; 1.24: Startwellen mit Uhrzeiten unter „Deine Startzeit“; 1.23: Pfeile in Bisher/Noch/Ganze Strecke und Rampe als Grafik, dreistellige Werte ohne „…“, zu breite Werte werden kleiner; 1.22: Bergab U-Kurve statt Grenze bei −4 %: am schnellsten bei −8 %, ab −16 % langsamer als flach, ohne Knick bei 0 %; 1.21: Tempo-Rad mit ×1 (Echtzeit), ×50 und ×100–×180 in 20er-Schritten; 1.20: Brücken-Beschriftungen überlappen nicht mehr; 1.19: Kästchen bunt/grau neben der Gesamtstrecke, Diagramm „So rechnet das Pace-Modell“; 1.18: Ortsname bei Uhrzeiten aus `D.ort`, für Boston, sonst unverändert; 1.17: Seite springt beim Drehen an Zielzeit und Startzeit nicht mehr; 1.16: Höhenangaben mit dunklem Schein statt Kasten; 1.15: Höhenangaben auf Schildern lesbar, Straßennamen in eigener Zeile unter der km-Skala; 1.14: Gesamtstrecke unten mit feiner weißer Linie und Schalter farbig/einfarbig, die drei hellsten Bergab-Blau weniger türkis; 1.13: Farben fest (bergauf Rot bis Aubergine, bergab Blau), Dreieck unter der Skala, nur noch dunkel; 1.12: geschätzte Brücken schraffiert statt abgedunkelt; 1.11: Steigungszahl ohne Farbe; 1.10: Steigungszahl immer lesbar; 1.9: Schalter Blautöne bergab auto/tief/leicht; 1.8: Blauverlauf bergab dunkler beginnend, Ende Marineblau; 1.7: nur flach grün, bergab sieben Blautöne; 1.6: Zeiger als Dreieck über der Skala, Varianten 1–4 mit Grün und Blauverlauf bergab; 1.5: Farbvarianten A, 1–4 und Schalter für flach; 1.4: Farbwahl auch im Vollbild; 1.3: Farbvarianten A–E zum Testen unter der Legende; 1.2: Text über den Zwischenzeiten nennt auch die Kosten steiler Anstiege; 1.1: Höhenachse in gröberen Schritten bei großem Höhenbereich, hier ohne Wirkung), live unter https://luperttrading-lab.github.io/marathon-strecken/muenchen/.

Die App ist eine Kopie der Hamburg-App (Stand 1.22) mit eigenen Daten, Texten und Speicherschlüsseln (`muc-…`), ohne eigenes
Manifest und Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in
[`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Änderungen am gemeinsamen Code in allen Apps nachziehen (README).

Das Rennen heißt 2026 „MARATHON MÜNCHEN by Brooks“ (neuer Ausrichter seit 2025), neuer Einrunden-Kurs 2026: Start
9:00 Uhr am Spiridon-Louis-Ring im Olympiapark, Ziel Willi-Daume-Platz am Olympiasee. Den Termin 2027 vergibt die Stadt
neu (höchstens ein Marathon im Jahr, ein Oktobersonntag nach der Wiesn); `D.termine` hat nur 2026, die Startseite zeigt
„Voraussichtlich im Oktober 2027“.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

1. `../dl/Marathon-Muenchen.gpx`: offizielle GPX von marathonmuenchen.org/gpx-downloads (1757 Punkte, 42,419 km, also
   0,5 % zu lang). Die Seite verlinkt sie hinter „Die Strecke als GPX“; die Suche fand sie erst nicht.
   **Gegenprobe aus dem Streckenplan-PDF** (`../dl/strecke2026.pdf`, Karte von mapz.com, alles Vektoren): `georef.py`
   (Linie an OSM-Straßen, ICP) blieb in einem Nebenminimum (0,7 % Maßstab, 0,5° Drehung, am Olympiasee 70 m daneben);
   `wasser_versatz.py` misst an 12 Gewässern per Kreuzkorrelation mit der Wasserfarbe der OSM-Kacheln und rechnet daraus
   eine neue Ähnlichkeit (Restfehler 2–9 m), `georef_wasser.py` legt die PDF-Linie damit auf Koordinaten. Ergebnis: im
   Mittel 7 m, höchstens 28 m neben der offiziellen GPX. Lehre: bei Karten ohne GPX Gewässer als Passpunkte nehmen.
   Die Kilometerkreise im PDF liegen 110–160 m neben der Linie und taugen nicht zum Eichen: `proj.py` nur Start/Ziel,
   `common.py` staucht gleichmäßig.
2. `dgm.py`: **DGM1 Bayern** als 1-km-Kacheln (`download1.bayernwolke.de/a/dgm/dgm1/<E km>_<N km>.tif`, ETRS89/UTM32,
   29 Kacheln, CC BY 4.0, „Datenquelle: Bayerische Vermessungsverwaltung – www.geodaten.bayern.de“). Jeder Messpunkt
   wird vorher auf den nächsten OSM-Weg gelegt (`../dl/osm_wege.json`, über den Overpass-Spiegel maps.mail.ru; die
   übrigen Spiegel sind aus der Umgebung gesperrt). Ohne das misst das Modell am Olympiaberg den Hang (+30 m).
3. `streets.py` (Nominatim alle 150 m, wiederholt bei HTTP 429), `clean.py` (wie Berlin; **Start von Hand**: Unterführung
   Toni-Merkens-Weg km 0,35–0,40 und Brücke über den Nymphenburg-Biedersteiner Kanal km 0,60–0,77, sonst baut die
   Automatik eine falsche Senke), `build.py`, `route.py` (lat0/lon0 48,0/11,4), `tiles.py`, dann aus `werkzeuge/`:
   `tiles_z11.py muenchen`, `work/app.py`, `tiles_rand.py muenchen`.
4. `app.py`: hat aus `hamburg/index.html` die Erstausgabe von `muenchen/` gebaut. **Nur historisch.**

## Ergebnis

↑ 90 m / ↓ 92 m mit 200-m-Fenster, Rohdaten ↑ 246 m. Start 512,5 m, Ziel 510,7 m; tiefster Punkt 496,7 m (Schwabing,
km 16,5), höchster 534,1 m (Berg am Laim, km 32,3). Steilste 200 m: +4,6 % Montgelasstraße aufs Isarhochufer (km 22,1),
−4,6 % Rosenheimer Straße hinunter zur Ludwigsbrücke (km 34,0). 5 Unterführungen, 10 Brücken (Isar: Tivolibrücke,
Ludwigsbrücke). Bei 4:00 /km im Flachen: 2:49:34, das Profil kostet 48 s. Das Höhenprofil des Veranstalters liegt im
Mittel gut 10 m höher (Marienplatz 527 statt amtlich 519 m) und hat nur einen Wert je km.

## Offen

- Termin 2027 (Vergabe durch die Stadt).
- Verpflegungsstellen und Staffelwechsel (nur als Symbole im PDF).
- Prüfung am iPhone.
