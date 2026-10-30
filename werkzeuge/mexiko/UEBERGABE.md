# Übergabe: Steigungsprofil Maratón de la Ciudad de México

Stand 29.10.2026, App-Version **1.7** (1.7: zu breite Tabellen werden stufenweise enger statt rechts abgeschnitten; 1.6: Mauer-Beschriftung in einer freien Zeile über dem Profil, mittig über der Mauer, nur bei `D.mauer`; 1.5: Mauer-Beschriftung im Profil neben dem Gipfel statt darauf, nur bei `D.mauer`; 1.4: Mauer je Durchgang ein Rad mit Empfehlung nach Zielzeit, nur bei `D.mauer`; 1.3: Mauer-Zeit und Tor-Rechner für Strecken mit `D.mauer`, sonst unverändert; 1.2: Steigungskosten als große Zeile unter der Zielzeit; 1.1: Umschalter Höhe/Meereshöhe für die Tabelle „Ohne Höhenmeter“, nur bei `D.lage`; 1.0: erste Fassung). Adresse nach dem Hochladen:
https://luperttrading-lab.github.io/marathon-strecken/mexiko/.

Die App ist eine Kopie der Tokio-App (Stand 1.22, aktueller gemeinsamer Code) mit eigenen Daten, Texten und Speicherschlüsseln
(`mex-…`, Service-Worker-Cache `mex-marathon-profil`, löscht nur Caches mit Präfix `mex-`), ohne eigenes Manifest und Symbol. Alle
Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Änderungen am
gemeinsamen Code in allen Apps nachziehen (README). Neu in `D`: `lage` = mittlere Höhe der Strecke über dem Meer, auf 10 m
gerundet (hier 2240); der gemeinsame Code zeigt sie noch nicht an.

## Termin und Start

XLIII. Maratón de la Ciudad de México Telcel am Sonntag, 30. August 2026 (gelaufen, rund 30 000 Teilnehmer; Ausschreibung des
Veranstalters auf Race Roster, „XLIII TELCEL MEXICO CITY MARATHON 2026“, und Presse). Der Lauf ist seit Jahren am letzten Sonntag im
August (2024: 25.08., 2025: 31.08., 2026: 30.08.); 2027 ist noch nicht veröffentlicht, daher `2027-08-29?` (unbestätigt).
`D.termine` `["2026-08-30", "2027-08-29?"]`, `D.tz` America/Mexico_City, `D.ort` „Mexiko-Stadt“ (nach der Zeitzone hieße es sonst
„Mexico City“), `D.ortKurz` „ Mexiko-Stadt“, `D.start` = 360 (6:00, erster Block der Läufer). Start auf der Avenida Insurgentes Sur
zwischen Biblioteca Central und Estadio Olímpico Universitario (Ciudad Universitaria, UNAM), Ziel erstmals direkt auf der Plancha des
Zócalo (Plaza de la Constitución) vor dem Fahnenmast. Zielschluss 6 Stunden (8:30 /km).

Startblöcke (`D.wellen`) laut Ausschreibung 2026, gleichlautend in der Presse (Claro Sports, Dónde Ir, American Health & Fitness,
López-Dóriga, El Universal): Rollstühle und Sehbehinderte 5:45, Elite Frauen 5:50, Elite Männer und Block A 6:00, Block B 6:15,
Block C 6:30. Eingetragen sind die Blöcke A–C; die Sonderstarts stehen im Hinweis. Den Block weist die Anmeldung zu. Eine Grafik
von UnoTV nennt für Block C 6:15, alle anderen Quellen 6:30.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Der Veranstalter (Gobierno de la Ciudad de México / Indeporte, https://maraton.cdmx.gob.mx/) war aus dieser Umgebung nicht
erreichbar (Zeitüberschreitung, auch datos.cdmx.gob.mx), web.archive.org antwortete mit 429. Die offizielle Strecke liegt als Kurs in
Garmin Connect (https://connect.garmin.com/app/course/505037497, verlinkt im Garmin-Blog zum Lauf), aber nur angemeldet; nicht
umgangen. Die Linie ist deshalb nachgezeichnet:

1. **Streckenplan 2026** des Veranstalters als Bild aus der Presse (`../dl/ruta-maraton-cdmx-2026.jpg`, 1200 × 795 px, von
   https://media.dondeir.com/2026/08/ruta-maraton-cdmx-2026.jpg; Karte um 90° gedreht, Norden rechts, am Rand abgeschnitten): Linie,
   Kilometerkreise 5–40 und 42, Getränkestellen, Sanität, Toiletten, Höhenbild „Altimetría“. Höher aufgelöste Fassungen gab es nicht
   (Claro Sports und American Health & Fitness zeigen andere Bilder). Straßenfolge laut Presse, am genauesten bei grupoanimal.mx und
   El Financiero (29./30.08.2026): Insurgentes Sur → Glorieta de Insurgentes → Oaxaca → Fuente de Cibeles → Nuevo León (Wende an
   Citlaltépetl/Mexicali) → Parque España → Sonora → Chapultepec → Florencia → Reforma → Bosque de Chapultepec → Chivatito → Reforma
   (Wende an Monte Elbruz) → Julio Verne → Luis G. Urbina, Edgar Allan Poe, Emilio Castelar (um den Parque Lincoln) → Anatole France →
   Masaryk (bis Sudermann und zurück) → Moliere → Ejército Nacional → Ferrocarril de Cuernavaca → Miguel de Cervantes Saavedra →
   Moliere → Ejército Nacional → Thiers → Darwin → Mariano Escobedo → Campos Elíseos → Rubén Darío → Schiller → Mahatma Gandhi →
   Reforma → Ignacio Ramírez → Runde um das Monumento a la Revolución → Avenida de la República → Reforma (Wende an der Glorieta Simón
   Bolívar) → Avenida Juárez → Madero → Bolívar → República de El Salvador → 20 de Noviembre → Zócalo. Wo der Plan genauer ist, gilt er:
   die Schleife im Bosque im Uhrzeigersinn über die Gran Avenida (Andador Gandhi nach Süden, Ostende, Süd- und Westseite, Avenida
   Heroico Colegio Militar zur Chivatito), die ganze Runde um das Monumento (Süd-, West-, Nord-, Ostseite), der Rückweg bei km 32 über
   den Westbogen der Calzada Mahatma Gandhi (der Ostbogen im Plan ist nur die Beschriftung). Im Centro ist der Plan schematisch
   (Zócalo und República de El Salvador zu klein gezeichnet; die Wende nach Süden sähe nach Isabel la Católica aus); dort gilt die
   Beschreibung, die Länge ist bei diesem Rechteck dieselbe.
2. `osm.py`: OSM-Straßennetz über die OSM-API (`https://api.openstreetmap.org/api/0.6/map?bbox=…`) in 255 Rechtecken von 0,004°
   (Insurgentes Sur ±450 m, dazu Roma/Condesa, Bosque/Polanco und Reforma bis Zócalo als Flächen), eine Abfrage je Sekunde
   (Rohantworten `../dl/osmapi/`, 94 MB) → `../dl/osm_netz.json` (13 329 Wege). Overpass war wie bei Osaka nicht nutzbar.
3. `netz.py`, `linie.py`: eigenes Routing (Dijkstra) auf diesem Netz zwischen 53 Wegmarken, meist Kreuzungen benannter Straßen;
   Kosten Länge × Straßenklasse, gegen Einbahnstraßen × 2,5 (auf zweibahnigen Straßen die Fahrbahn in Laufrichtung), ohne
   Autobahnen; wo das Routing eine gesperrte Einbahnstraße umgehen würde, bleibt der Abschnitt auf der genannten Straße (Nuevo León,
   Parque Lincoln, Anatole France, Plaza de la República). Glorieta de Insurgentes: OSM hat zwei Halbringe, deren Nordenden direkt
   verbunden sind (17 m). Ziel: vom Nordende der 20 de Noviembre gerade über den Platz zum Fahnenmast (19,43260 / −99,13320).
   → `gpx2026.json` (1373 Punkte, **43,93 km** auf dem Ellipsoid), `wegmarken.json`, `strassen.json` (Weg und Name je 10 m aus den
   Kanten der Linie). Erste Fassungen hatten Zwischenmarken auf der Gegenfahrbahn der Insurgentes (Wendeschleifen, +0,5 km) und
   Umwege um Einbahnstraßen; geprüft über den Umwegfaktor je km und Karten mit Linie.
4. `marken.py`: Plan affin auf die Linie eingepasst (ICP über die Pixel der dunkelblauen Streckenlinie, Startwerte aus fünf
   Passpunkten; Abstand Median 2,3 px = 25 m, 90 % 12,8 px, Maßstab 10,7 m/px), Kreise per Farbe erkannt (dunkeltürkis = km 5–40,
   hellgrün = Getränkestellen 2,5–37,5) und auf die Linie projiziert; Masaryk (dreimal an derselben Stelle) nach der erwarteten Lage.
   Die Marke 25 gilt für den Rückweg von Sudermann, sonst passten 22,5 → 25 → 27,5 nicht. → `marken.json`.
5. `common.py`: Kilometer stückweise linear über die km-Kreise 5–40, Start = Linienanfang, Ziel = Linienende. Marke zu Marke 4,97–5,50
   km Linie je 5 km (Linie im Mittel 4,1 % zu lang: Straßenmitte, Glorietas, fünf Wenden, viele Ecken; am meisten km 10–15 und
   20–25 mit 9–10 %). **Gegenprobe** mit den acht Getränkestellen, die nicht geeicht sind: +5, +15, −18, +94, −27, −73, −10, 0 m neben
   ihrer Angabe; gleichmäßige Eichung (Linie / 42,195) liegt dort bis 190 m daneben. Die Wende Monte Elbruz, an der im Plan „21“ steht,
   fällt auf km 21,16. Die Kilometer sind daher auf etwa ±100 m genau (Plan unscharf, Kreise mit 15 px ≈ 160 m Durchmesser).
6. `inegi.py`, `inegi_dgm.py`, `dgm.py`: **Höhenmodell des INEGI** (Continuo de Elevaciones Mexicano,
   https://www.inegi.org.mx/app/geo2/elevacionesmex/, Download über `getF10KDescarga.do`), Blätter 1:10 000 E14A39E1 (Start),
   B3, B4, B1, B2 decken die Linie ganz ab. Je Blatt drei Ausgaben „Terreno“: **5m2011** „Alta Resolución LiDAR“ (Laserbefliegung
   2007, Leica ALS50 II, 0,21 Bodenpunkte/m², XYZ-Text, ITRF92, NAVD88), 5m2017/2018 (BIL) und 15m2020 (1,5 m, BIL). Laut Metadaten
   stammen 2017/18 und 2020 aus **Satelliten-Stereobildern** (Dezember 2017) und einer fotogrammetrischen Punktwolke (2019), trotz
   „lidar“ im Pfad. Entlang der Linie sind 2018 und 2020 gleich (σ 0,05 m), die 1,5-m-Ausgabe bringt also nichts. Gegen den Laserscan:
   im Mittel 0,74 m höher (σ 1,5 m), auf Straßen glatter, aber unter den Bäumen des Bosque de Chapultepec (km 17,7–19) bis 15 m
   daneben und an den Reforma-Viadukten über dem Circuito Interior 8 m tief; 44 statt 7 Sprünge über 1,5 m je 10 m. **Genommen: 5m2011**,
   bilinear alle 10 m, Höhen über dem Meer (NAVD88). Nachteil: Stand 2007; Senkungen im Seebecken (Centro) bis 2017 zeigen sich im
   Vergleich nur als 0,1–0,4 m Neigung. → `dgm2026_10m.json`, `dgm_vergleich.json` (alle drei), `dgm_vorstart.json`.
7. `orte.py`: **Colonia** alle 100 m über Nominatim (zoom 17, eine Abfrage je 1,1 s, 429 mit Wiederholung, Rohantworten
   `../dl/nominatim.json`), nur das Feld „neighbourhood“ (Flächen in OSM); „quarter“/„suburb“ ordnet Nominatim nach dem nächsten
   Ortspunkt zu und lag daneben. Bereinigung in `namen.py`: ohne „Colonia“, Polanco 1ª–5ª Sección als „Polanco“ (die Strecke läuft auf
   ihren Grenzstraßen), Stücke ohne Fläche am Park als „Bosque de Chapultepec“, Start „Ciudad Universitaria“. Gewählt statt der
   Alcaldías, weil diese zu grob sind (Miguel Hidalgo allein 18,4 km von Chapultepec bis Anzures, insgesamt fünf); die Colonias (Roma
   Norte, Condesa, Polanco, Centro …) sind die Namen, mit denen man sich in der Stadt verabredet. Auf der Insurgentes wechseln sie,
   weil die Straße Grenze vieler Colonias ist, aber nicht unter 300 m (build.py).
8. `clean.py`: Brücken aus OSM (bridge=yes/viaduct auf den Kanten der Linie), gerade gezogen, wo das Modell innen mehr als 1,0 m unter
   oder über der Geraden zwischen den Enden liegt (wie Valencia). **Geschätzt** (schraffiert): Brücke der Insurgentes am Estadio
   Olímpico (km 0–0,21, der Start liegt auf ihrem Südende; Südende = Rampe 25 m vor dem Start, Modell darunter bis 4,5 m tiefer),
   Überführung über die Avenida San Jerónimo (km 0,46–0,77; OSM-Brücke nur 30 m, nördlich misst das Laser-Modell unter der Rampe,
   5 m tiefer als das Modell 2017; gerade von 480 bis 800 Linienmeter, wo beide Modelle übereinstimmen) und Glorieta de los
   Insurgentes (km 10,38–10,76, Ring über dem versenkten Platz, Modell ±1,9 m). **Gemessen:** Reforma über dem Circuito Interior
   (km 16,9 und 34,2, Abweichung 0,4/0,5 m), Brücke der Ejército Nacional (km 29,3–29,6, Rauschen ±0,7 m), Insurgentes über dem
   Viaducto Miguel Alemán (km 7,7, OSM layer=1, beide Modelle zeigen dieselbe Rampe von +4 m). Unterführungen oder Tunnel nimmt die
   Strecke keine. Weitere Stufen über 1,5 m gab es nicht.
9. `build.py` (Straßen unter 80 m und Colonias unter 300 m dem Vorgänger zugeschlagen; Namen wie in OSM, `namen.py` vereinheitlicht
   „Avenida Paseo de la Reforma“ und „… Norte“ zu „Paseo de la Reforma“ und „Calle 20 de Noviembre“ zu „Avenida 20 de Noviembre“;
   Getränke laut Plan an ihrer Kilometerangabe: Wasser „Agua Skarch“ bei 2,5, 7,5 … 37,5 km, Electrolit an den km-Kreisen 5 … 40,
   dort laut Kästen auch Sanität und Toiletten; `D.lage` = Mittel der Höhe über das 10-m-Raster, 2243,2 → 2240), `route.py` (lat0/lon0
   19,3/−99,2), `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py mexiko`, `work/app.py` (aus `tokio/index.html` und `tokio/sw.js`;
   Texte in `sub.html`, `quellen.html`, `strassennamen.html`, `imgnote.html`), `tiles_rand.py mexiko 2`.
10. `planprofil.py`, `vergleich.py`: Höhenbild des Plans ausgelesen (Achsen nach den Beschriftungen) und gegen die App verglichen.

## Ergebnis

↑ 88 m / ↓ 145 m mit 200-m-Fenster, ↑ 115 / ↓ 172 m mit 50 m (Tabelle in der App: 50 m 115, 100 m 103, 1 km 50), Rohdaten ↑ 227 m.
Start 2284,8 m auf der Brücke am Stadion, höchster Punkt 2288,0 m an der Überführung über die Avenida San Jerónimo (km 0,45), tiefster
2226,3 m in der Calle Simón Bolívar (km 41,05), Ziel 2227,9 m auf dem Zócalo; mittlere Höhe 2243 m (`D.lage` 2240). Auf der Insurgentes
55 m gleichmäßig hinab bis zur Glorieta (2231 m, km 10,5), einzige Welle die Rampe über den Viaducto (km 7,7); Roma und Condesa flach;
vom Ángel sanft hinauf über Reforma und Bosque bis 2261 m an der Wende Monte Elbruz (km 21,1), in Polanco Senke an der Wende Sudermann
(2244 m, km 23,9), Hoch an der Ferrocarril de Cuernavaca am Museo Soumaya (2262 m, km 26,9), über Ejército Nacional und Thiers hinab
auf 2240 m (km 30,7), über Rubén Darío und Gandhi auf 2249 m (km 32,9), dann auf der Reforma 21 m hinab ins Centro. Steilste Stelle
+2,0 % über 200 m an der Rampe über den Viaducto (km 7,6), bergab −3,2 % dahinter (km 7,8). Mit 4:00/km im Flachen ergibt das Modell
2:49:04 (das Profil kostet 17 s, bei 2:50:00 ebenfalls 17 s); die Höhenlage selbst rechnet das Modell nicht.

**Abgleich mit dem Höhenbild des Veranstalters** (Plan, `vergleich.py`): km 0–10 im Mittel 1,9 m höher als die App, km 10–17 3,4 m,
km 34–42 2,7 m (Start 2291 statt 2285, Ziel 2231 statt 2228); km 17–34 dagegen 12–16 m höher (bis +29 m) mit Buckeln, wo die Strecke
unter Bäumen und zwischen Häusern läuft (Bosque, Polanco) – vermutlich ein Oberflächenmodell. Die Wellen liegen an denselben Stellen
(Hoch Monte Elbruz 20,2 im Plan / 21,2 App, Soumaya 26,2 / 26,9, Gandhi 32,1 / 32,9, Tief Sudermann 24,2 / 23,9, Thiers 30,3 / 30,8),
im Plan meist 0,3–0,8 km früher; das Höhenbild ist grob gezeichnet, die Kilometerkreise der Karte und die Getränkestellen sprechen für
die Eichung hier.

Geprüft mit Playwright (393 × 852, Server auf Port 8773): keine Konsolenfehler, `APP_VERSION` 1.0, Service Worker installiert (26
Dateien im Cache `mex-marathon-profil`), Tipp auf die Version meldet „Version 1.0 ist aktuell“, alle 20 Kartenstücke passen zu
`D.tiles`, Laufansicht, Glorieta, Bosque, Monumento und Ziel auf der Karte angesehen.

## Offen

- Prüfung am iPhone.
- Startseite: Karte für Mexiko-Stadt fehlt noch (Eyebrow „Maratón de la Ciudad de México Telcel“, Stadt „Mexiko-Stadt“, „Kurs 2026“,
  `data-termine="2026-08-30 2027-08-29?"`, `data-monat="8"`, ↑ 88 m / ↓ 145 m, Höhe 2226–2288 m, `data-such` z. B. „Mexico City CDMX
  Ciudad de México Mexiko México Telcel“), README-Tabelle und Liste der Speicherschlüssel/Cache-Präfixe (`mex-`). Der Höhenbereich
  (62 m) braucht auf der Startseite wohl eine höhere Mini-Grafik; Zahlen wie 2288 m sind breiter als bei den anderen Strecken.
- `D.lage` anzeigen (gemeinsamer Code, alle Apps).
- **GPX der offiziellen Strecke** (Garmin Connect, Kurs 505037497, angemeldet) oder eine Karte mit allen Kilometern: Linie und Eichung
  damit ersetzen; dann klärt sich auch, ob die Wenden genau an Citlaltépetl, Monte Elbruz, Sudermann und der Glorieta Simón Bolívar
  liegen und ob auf der Ejército Nacional die Brücke oder die Seitenfahrbahn gelaufen wird.
- Termin 2027 (`2027-08-29?`) und die Blöcke 2027 prüfen, sobald die Ausschreibung erscheint (2026 auf Race Roster und
  maraton.cdmx.gob.mx).
- Kurs 2027: Die Zielführung auf die Plancha war 2026 neu; bei einer Änderung `linie.py` (Wegmarken) und die Kette ab `marken.py`
  erneut laufen lassen.
