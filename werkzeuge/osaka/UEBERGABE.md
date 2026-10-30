# Übergabe: Steigungsprofil Osaka-Marathon

Stand 29.10.2026, App-Version **1.16** (1.16: Offline-Hinweis orange und stehend, bis man ihn antippt; 1.15: Offline-Laden aller Strecken aus 1.78 zurückgenommen (Nutzer: erstmal nur die Meldung), dafür Meldung „Offline: gespeicherte Fassung, vielleicht nicht die neueste“; 1.14: alle Strecken offline: Seiten beim Öffnen der Startseite, Kartenbilder beim Öffnen der Strecke oder per Knopf; 1.13: offline nur noch aus dem eigenen Speicher, Rückfallseite bei jedem Besuch erneuert (Service Worker); 1.12: im Ziel 42,195 statt 42,2 in Anzeige, Gesamtstrecke, Zwischenzeiten und Pace-Band; 1.11: Maßstab auf der Karte ohne Kasten, kleiner, in der freieren linken Ecke; 1.10: im Vollbild der Ort groß oben rechts statt am Pfeil, Maßstab auf der Karte; 1.9: Kopf mit Ort groß und „Streckenplan und Steigungsprofil“, Umschalter Karte | Zahlen statt Pünktchen, Karte zuerst, Name der Strecke im Vollbild; 1.8: zu breite Tabellen werden stufenweise enger statt rechts abgeschnitten; 1.7: Mauer-Beschriftung in einer freien Zeile über dem Profil, mittig über der Mauer, nur bei `D.mauer`; 1.6: Mauer-Beschriftung im Profil neben dem Gipfel statt darauf, nur bei `D.mauer`; 1.5: Mauer je Durchgang ein Rad mit Empfehlung nach Zielzeit, nur bei `D.mauer`; 1.4: Mauer-Zeit und Tor-Rechner für Strecken mit `D.mauer`, sonst unverändert; 1.3: Steigungskosten als große Zeile unter der Zielzeit; 1.2: Umschalter Höhe/Meereshöhe für die Tabelle „Ohne Höhenmeter“, nur bei `D.lage`; 1.1: Feld `D.lage` für hoch gelegene Strecken: Tabelle „Ohne Höhenmeter“ nennt dann die Höhe; 1.0: erste Fassung). Adresse nach dem Hochladen:
https://luperttrading-lab.github.io/marathon-strecken/osaka/.

Die App ist eine Kopie der Tokio-App (Stand 1.22) mit eigenen Daten, Texten und Speicherschlüsseln (`osa-…`, Service-Worker-Cache
`osa-marathon-profil`, löscht nur Caches mit Präfix `osa-`), ohne eigenes Manifest und Symbol. Alle Entscheidungen zur Bedienung
und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Änderungen am gemeinsamen Code in allen Apps
nachziehen (README).

## Termin und Start

Osaka Marathon 2027 (15. Ausgabe, Osaka Marathon Foundation) am Sonntag, 28. Februar 2027 laut Ausschreibung
(https://www.osaka-marathon.com/2027/info/gist/). Start der ersten Welle 9:15 Uhr, danach Welle 2 und 3 nacheinander; Zielschluss
16:15 (7 Stunden ab der ersten Welle). `D.start` = 555, `D.tz` Asia/Tokyo, `D.ort` „Osaka“ (nach der Zeitzone hieße es sonst
„Tokyo“), `D.ortKurz` „ Osaka“, `D.termine` `["2027-02-28"]`. Start vor dem Präfekturamt (大阪府庁前) am Uemachi-suji, Ziel im
Burgpark (大阪城公園).

Wellen (`D.wellen`): Uhrzeiten aus den Unterlagen 2026, Tabelle auf der Karte „集合会場およびコースMAP“
(https://www.osaka-marathon.com/2026/map.pdf) und Teilnehmerinfo
(https://www.osaka-marathon.com/2026/runner/guidance/pdf/Info_on_participation_jp.pdf): Welle 1 9:15 Blöcke A–C, Welle 2 9:30
Blöcke D–F, Welle 3 9:45 Blöcke H und J (Block G ist der 720〈なにわ〉-Lauf über 7,2 km, der mit der dritten Welle startet; einen
Block I gibt es nicht). Die Ausschreibung 2027 nennt 9:15 für die erste Welle und 9:45 als Start des 720-Laufs, also der dritten
Welle; die Uhrzeit der zweiten Welle 2027 steht noch nicht fest.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

1. **Strecke** aus der Google-Karte des Veranstalters, eingebettet auf https://www.osaka-marathon.com/2026/info/course/ (Karte
   „大阪マラソン2026 Osaka Marathon 2026“), als KML:
   `https://www.google.com/maps/d/kml?mid=1pWXP58aD4dUxOsWy6nTnC8iqO31PGfc&forcekml=1` (`../dl/karte_….kml`). Die Kursseite 2027
   (https://www.osaka-marathon.com/2027/info/course/) hat keine Google-Karte mehr und nur ein PDF aus Bildern
   (`/2027/info/course/pdf/course_en.pdf`); ihr Streckenbild ist im Pixelvergleich bis auf Bildrauschen dasselbe wie 2026, die
   Ausschreibung 2027 beschreibt denselben Kurs (Start Präfekturamt, Ziel Burgpark). Linie „走路 Route“ in einem Stück in
   Laufrichtung (382 Punkte, 42,69 km auf dem Ellipsoid), dazu Start, Ziel, Kilometermarken nur alle 5 km und der Halbmarathon
   (中間点), 16 Getränkestellen (給水, Kilometer im Namen), 10 Kontrollpunkte (収容関門), Sanität, Toiletten, Startblöcke.
   `parse.py` schneidet an Start und Ziel (beide höchstens 5 m daneben) und projiziert die Marken auf die Linie; auf den drei
   Stichen (Minato-dōri, Naniwa-suji, Matsuyamachi-suji) gilt die Stelle nahe der erwarteten. → `gpx2026.json`, `marken.json`.
   Die Linie liegt überall höchstens 9 m neben einer OSM-Straße (Median 1,6 m), ist also entlang der Straßenmitte gezeichnet.
2. `common.py`: Kilometer stückweise linear über die 8 Marken und den Halbmarathon (höchstens 17 m neben der Linie). Marke zu
   Marke 4967–5221 Linienmeter je 5 km; km 5–10 hat 5221 (4,4 % mehr), alle anderen Abschnitte 0,3–1,3 % mehr (Straßenmitte statt
   Ideallinie), das Stück km 40–Ziel 2,9 %. Gegenprobe mit den übrigen Nadeln derselben Karte: Die Kontrollpunkte liegen nach dieser
   Eichung −21 bis +97 m neben ihrer Kilometerangabe, die Getränkestellen +24 bis +212 m (im Mittel +100 m: eine Stelle ist
   100–200 m lang, die Angabe meint wohl den Anfang). Eine gleichmäßige Eichung (Linie / 42,195) passt zu beiden Nadelsätzen
   schlechter; nur das Ziel des 720-Laufs (7,2 km, zweigt bei Linienmeter 7085 ab) spräche für sie (Unterschied dort 70 m). Die
   Kilometer sind daher auf etwa ±100 m genau, am unsichersten zwischen km 5 und 10.
3. `dgm.py`: **GSI-Höhenmodell** (国土地理院, 地理院タイル, https://maps.gsi.go.jp/development/ichiran.html) als PNG-Kacheln z15 von
   `https://cyberjapandata.gsi.go.jp/xyz/dem5a_png/…`: DEM5A (Laser, 5 m), wo es fehlt DEM5B, sonst DEM10B (93 von 4270 Punkten,
   auf Brücken). Höhe = (R·65536 + G·256 + B)·0,01 m, bilinear, alle 10 m. Höhen über T.P. (Tokyo Peil, Bezug für ganz Japan; das
   in Osaka übliche O.P. liegt 1,3 m tiefer und wird nicht verwendet). → `dgm2026_10m.json`.
4. `osm.py`: OSM-Wege im Umkreis von 40 m um die Linie. Overpass war am 29.10.2026 aus dieser Umgebung nicht nutzbar (maps.mail.ru
   504, overpass-api.de Verbindung abgebrochen, overpass.kumi.systems Zeitüberschreitung); deshalb über die OSM-API
   (`https://api.openstreetmap.org/api/0.6/map?bbox=…`) in 107 kleinen Rechtecken entlang der Linie, eine Abfrage je Sekunde
   (Rohantworten `../dl/osmapi/`, 75 MB), danach auf 40 m gefiltert, Aufbau wie eine Overpass-Antwort. `streets.py`: je 10 m der
   nächste Weg höchstens 20 m daneben, Hauptstraßen bevorzugt, ohne Autobahnen (Hanshin Expressway, aufgeständert über
   Tenjinbashi-suji, Tosabori-dōri, Midō-suji, Sennichimae-dōri, Minato-dōri und Naniwa-suji). Anders als in Tokio zählen Wege mit
   layer < 0, weil die Strecke durch die Unterführung des Shiromi-dōri läuft (km 41,1); nur Tunnel bleiben aus (sonst stand dort
   160 m „Tamatsukuri-suji“, die Straße oben drüber). `namen.py`: japanische Namen in Umschrift (Hepburn mit Längenstrich,
   „-dōri“, „-suji“). Zwei Stücke tragen in OSM nur Verwaltungsnamen und stehen so in Umschrift: 大阪市道赤川天王寺線
   (Katamachi–Higashinoda, 400 m) „Akagawa-Tennōji-sen“ und 府道173号大阪八尾線 (Taishō-bashi–Honden, hin 1,3 km, zurück 1,0 km)
   „Ōsaka-Yao-sen“. Ab der Shin-Shigino-bashi Parkwege ohne Namen: „Ōsaka-jō-kōen“.
5. `orte.py`: Bezirk (区) alle 100 m über den Adressdienst der GSI (`mreversegeocoder.gsi.go.jp`, Gemeindeschlüssel 271xx → Chūō,
   Miyakojima, Kita, Nishi, Naniwa, Taishō, Minato, Nishinari, Tennōji, Ikuno, Higashinari, Jōtō).
6. `clean.py`: zuerst die Brücken aus OSM (bridge=yes auf der Linie, Enden oben auf den Rampen, nur wo das Modell innen mehr als
   0,5 m unter der Geraden liegt). Zwei OSM-Teile derselben Brücke mit einer Lücke bis 80 m werden ein Stück (Tenjin-bashi:
   dazwischen misst das Modell den Park auf der Spitze von Nakanoshima 3 m unter der Fahrbahn). Danach Stufen > 1,5 m paarweise
   (es blieben keine weiteren). Geschätzt (13 Stücke): Neyagawa-bashi, Sakuranomiya-bashi (Ginbashi, über den Ōkawa), Tenjin-bashi,
   Tosabori-dōri über den Higashi-Yokobori-gawa, Yodoya-bashi, Midō-suji über den Dōtonbori, Taishō-bashi und Iwamatsu-bashi auf
   Hin- und Rückweg, zweimal die Naniwa-suji über der tiefer gelegten Nationalstraße 43 (Modell dort −5 m) und die Shin-Shigino-bashi
   in den Burgpark. Higo-bashi, Ōike-bashi und die Brücke des Imazato-suji über den Daini-Neya-gawa (km 39,6, Buckel 2,4 m) misst
   das Modell selbst mit Fahrbahn; sie bleiben, wie gemessen. Ebenso die Unterführung des Shiromi-dōri unter der Ringbahn
   (km 41,0–41,3, bis −2,0 m): Das Modell misst den offenen Einschnitt, die Stufen dort liegen unter 1,5 m je 10 m.
7. `build.py` (Straßen unter 80 m und Bezirke unter 300 m dem Vorgänger zugeschlagen; Getränkestellen an ihrer Kilometerangabe,
   „給水・給食“ und „まいどエイド“ als Verpflegung, „6.0km“ gibt es zweimal, vor und hinter der Tenjin-bashi: die zweite um den
   Abstand der beiden Nadeln weiter, bei 6,38 km), `route.py` (lat0/lon0 34,6/135,4), `tiles.py`, dann aus `werkzeuge/`:
   `tiles_z11.py osaka`, `work/app.py` (aus `tokio/index.html` und `tokio/sw.js`), `tiles_rand.py osaka 2`.

## Ergebnis

↑ 72 m / ↓ 83 m mit 200-m-Fenster, ↑ 104 / ↓ 114 m mit 50 m (Tabelle in der App: 50 m 103, 100 m 90, 1 km 36), Rohdaten ↑ 186 m.
Start 15,5 m am Nordrand der Uemachi-Hochfläche, Ziel 4,7 m im Burgpark, höchster Punkt 21,4 m (km 32,4, Uehonmachi), tiefster
−2,0 m in der Unterführung des Shiromi-dōri (km 41,15); auf offener Straße am tiefsten die Minato-dōri mit −1,0 m (km 15,5).
Bis km 0,5 geht es 10 m hinunter an den Ōkawa, danach Flachland mit Brückenbuckeln; einziger Anstieg ist die Sennichimae-dōri vom
Matsuyamachi-suji hinauf nach Tanimachi 9 und Uehonmachi (km 31,8–32,4, 18 m). Steilste Stelle +4,7 % über 200 m auf der
Sennichimae-dōri (km 32,0), bergab −3,2 % auf dem Uemachi-suji (km 0,3). Mit 4:00/km im Flachen ergibt das Modell 2:49:22 (das
Profil kostet 35 s, bei 2:50:00 ebenfalls 35 s).

Abgleich mit dem Höhenbild des Veranstalters (Kursseite, `img_map_02.jpg`): Start etwa 15 m, Flachland 0–5 m, Buckel um km 13,5
und 19,5 (Taishō-bashi), Hochfläche km 31–34 bis 20 m, Buckel bei 39,5, Ziel etwa 5 m – passt. Den Anstieg zeigt das Bild etwa
0,7 km früher; es ist grob gezeichnet, und Lage und Wendepunkt (Kontrollpunkt „30.5km“ am Kōen-kitaguchi) sprechen für die
Eichung hier.

## Offen

- Prüfung am iPhone.
- Startseite: Karte für Osaka fehlt noch (Eyebrow „Osaka Marathon“, Stadt „Osaka“, „Kurs 2026“, `data-termine="2027-02-28"`,
  `data-monat="2"`, ↑ 72 m / ↓ 83 m, Höhe −2–21 m, `data-such` z. B. „Japan Ōsaka Kansai“), README-Tabelle und Liste der
  Speicherschlüssel/Cache-Präfixe (`osa-`).
- Wellen 2027: Uhrzeit der zweiten Welle und die Blöcke prüfen, sobald die Teilnehmerinfo 2027 erscheint (2026: Anfang Februar).
- Kilometer zwischen km 5 und 10 (siehe Daten 2): Die Karte hat nur Marken alle 5 km. Erscheint eine Karte mit allen
  Kilometermarken (z. B. in der Teilnehmerinfo 2027) oder eine GPX-Datei, neu eichen.
- Getränkestellen: Lage nach der Kilometerangabe 2026; was es dort gibt, steht in der Karte (Wasser, Aquarius, Cola, Essen), ist aber
  nicht eingetragen. Für 2027 die Karte erneut abrufen, falls der Veranstalter wieder eine Google-Karte einbettet.
