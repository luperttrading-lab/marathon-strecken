# Übergabe: Steigungsprofil München-Marathon

Stand 27.10.2026, App-Version **1.10** (1.10: Steigungszahl immer lesbar; 1.9: Schalter Blautöne bergab auto/tief/leicht; 1.8: Blauverlauf bergab dunkler beginnend, Ende Marineblau; 1.7: nur flach grün, bergab sieben Blautöne; 1.6: Zeiger als Dreieck über der Skala, Varianten 1–4 mit Grün und Blauverlauf bergab; 1.5: Farbvarianten A, 1–4 und Schalter für flach; 1.4: Farbwahl auch im Vollbild; 1.3: Farbvarianten A–E zum Testen unter der Legende; 1.2: Text über den Zwischenzeiten nennt auch die Kosten steiler Anstiege; 1.1: Höhenachse in gröberen Schritten bei großem Höhenbereich, hier ohne Wirkung), live unter https://luperttrading-lab.github.io/marathon-strecken/muenchen/.

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
