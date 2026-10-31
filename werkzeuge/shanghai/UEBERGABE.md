# Übergabe: Steigungsprofil Shanghai Marathon

Stand 31.10.2026, App-Version **2.2** (erste Fassung, angelegt mit `werkzeuge/kern/kern.py --neu` auf dem gemeinsamen Kern; die
Hauptsitzung zählt die Nummer beim Veröffentlichen hoch).
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/shanghai/.

Die App hat den gemeinsamen Kern aus `hamburg/` und eigene Felder (Texte, `const D`, Speicherschlüssel `sha-…`, Service-Worker-Cache
`sha-marathon-profil`, löscht nur Caches mit Präfix `sha-`; der Präfix war frei, `kern.py --neu` prüft das), ohne eigenes Manifest und
Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md). Startseite,
README und `version.json` sind noch nicht angepasst (Hauptsitzung).

**Wichtigste Unterschiede zu den anderen Strecken:**
1. **Keine GPS-Datei und noch kein Plan 2026.** Die Linie folgt dem Streckenplan 2025 des Veranstalters (gleich 2024) auf den Straßen
   von OpenStreetMap; die Wendepunkte zeigt der Plan nur ungefähr (Daten 4). Kilometer auf etwa ±0,3 km.
2. **Kein Laser- oder amtliches Höhenmodell.** FABDEM (30 m), kräftig geglättet, weil die Stadt flach ist und das Modell sonst Hausreste
   als Hügel zeigt. Die einzigen spürbaren Steigungen sind sechs Brücken über Bäche; ihre Fahrbahn kennt kein freies Modell, sie ist
   nach dem Höhenbild des Veranstalters geschätzt (Daten 7).

## Termin und Start

**2026上海马拉松 (Shanghai Marathon) am Sonntag, 6. Dezember 2026**, Start 7:00 Uhr (Rennrollstühle 6:45), Wettkampfordnung 2026
(„2026上海马拉松竞赛规程“, Stand April 2026) auf https://www.shang-ma.com/ (Vue-App unter `static.shang-ma.com/web/`; die Texte liefert die
Schnittstelle `https://apih5.shang-ma.com/app/web/newsPosts/eventsNews/232`, `../dl/api/`, Text `../dl/api/news_3280.txt`). Der
Countdown der Startseite zeigte am 31.10.2026 „距 2026上海马拉松 35天13时24分“, also 6.12. 7:00 Pekinger Zeit; `eventDate` der Schnittstelle
6.12.2026 6:45. Die interAir-Reise (03.–08.12.2026) passt. 30. Ausgabe („三十而砺“), 30 000 Plätze im Marathon (2025: 23 000), dazu 20
Rennrollstühle; der 5-km-Lauf („健身跑“) ist 2026 ein eigener Lauf am 5. Dezember. Veranstalter: Shanghai Donghao Lansheng Sports
(上海东浩兰生体育有限公司), technisch zugelassen vom chinesischen Leichtathletikverband; World Athletics Label, seit 2025 Kandidat für die
Abbott World Marathon Majors (zweite Bewertung am 6.12.2026, Aufnahme 2027 möglich; Mitteilung des Veranstalters 11.03.2026).
2025 war es Sonntag, der 30. November (gelaufen). 2027 ist nicht veröffentlicht; eine Reiseseite nennt den 5.12.2027 ohne Beleg, nicht
übernommen.
`D.termine` `["2025-11-30", "2026-12-06"]`, `D.tz` Asia/Shanghai (die Zeitzone heißt wie die Stadt, kein `D.ort`), `D.ortKurz`
„ Shanghai“, `D.start` = 420 (7:00). Kein `D.lage`, `D.mauer`, `D.tor`.

**Starts** (`D.wellen`): Die Ordnung sagt nur „分枪发令“ (Start in Wellen). Uhrzeiten gibt es für 2025 aus der Mitteilung vom 22.11.2025
(„关于2025上海马拉松参赛相关事宜的公告“, `…/web/newsPosts/detail/3182`, `../dl/api/news_3182.txt`): 6:45 Rennrollstühle, 7:00 Eingeladene,
Läufer mit Qualifikationszeit (预达级) und Startbereiche A und B, 7:10 C, 7:20 D und E. Für 2026 noch nicht veröffentlicht (2025 kam die
Mitteilung acht Tage vor dem Lauf, also etwa am 28.11.2026 nachsehen). Startbereiche 2025 laut Startplan („起点示意图“): A an der Hankou
Lu, B Jiujiang Lu, C Nanjing Dong Lu, D Dianchi Lu/Beijing Dong Lu, E bis zur Suzhou-Bach-Brücke.
**Schlusszeiten 2026** (Uhrzeit, für alle gleich): km 10 8:50, 15 9:35, 20 10:20, 25 11:00, 30 11:45, 35 12:30, 40 13:15, Ziel 13:30 (die
Ordnung 2025 hatte noch 30 min weniger; die Mitteilung vom 22.11.2025 hob sie auf diese Werte an und nannte dazu km 5 8:05). Medaille
für alle, die in 6 Stunden im Ziel sind. Nur im Text der Wellen (`D.tor` zeigt der Kern nur mit `D.mauer`).

**Halbmarathon-Marke** bei 21 098 m (Zeitnahme „中点 21.0975km“; Matten an Start, alle 5 km, Halbmarathon, Wendepunkten und Ziel). Kein
Halbmarathon und keine Staffel im selben Rennen.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Reihenfolge: `plan.py`, `osm.py`, `georef.py` (nur Kontrolle), `linie.py`, `strassen.py`, `orte.py`, `fabdem.py`, `dgm.py`, `planprofil.py`,
`vergleich.py` (nur Abgleich), `clean.py`, `build.py`, `marken.py` (nur Abgleich), `route.py`, `tiles.py`, dann aus `werkzeuge/`:
`tiles_z11.py shanghai`, `shanghai/work/app.py` (beim ersten Mal über `kern.py --neu shanghai work/felder.json`, danach ersetzt es nur die
Felder und lässt Kartenbilder und `D.tiles` stehen), `tiles_rand.py shanghai 2`. Nur Kontrolle: `karte_pruefen.py <lat> <lon> <Breite m>
<Bild>` (OSM-Straßen mit chinesischen Namen und die Linie als Bild). Seiten des Veranstalters im Browser: `web_holen.js`. Prüfen:
`pruefen.js` … `pruefen4.js` (Server auf Port 8792, `NODE_PATH=/opt/node-tools/node_modules node pruefen.js`).

1. **Quellen des Veranstalters** (`../dl/`): Die Seite shang-ma.com ist eine Vue-App; GET-Abfragen an `apih5.shang-ma.com/app` gehen
   direkt (`web/newsPosts/eventsNews/<Lauf>`: 232 = 2026, 224 = 2025, 219 = 2024; `web/newsPosts/detail/<Nr>`), die Nachrichtenliste
   (POST, von der Seite selbst verschlüsselt) über Chromium (`web_holen.js`). Kein Login nötig, nichts umgangen. Die Seite „赛事路线图“
   2026 (Nr. 3289), „起点平面图“ und „终点平面图“ zeigen am 31.10.2026 nur „敬请期待！“ (folgt). Die Ordnung 2026 nennt als Strecke „外滩、南京路
   步行街、静安寺、淮海路、新天地、中共一大会址、黄浦滨江、龙腾大道、龙华寺、龙华烈士陵园“, Start „中山东一路（外滩金牛广场）“, Ziel „中山南二路（徐家汇体育公园）“:
   dieselben Orte wie 2025 („外滩、南京路步行街、静安寺、淮海路、新天地、龙腾大道、龙华路“, Ziel ebenso), nur ausführlicher (Gründungsort der KP an der
   Xingye Lu, Ufer in Huangpu, Longhua-Tempel und Märtyrerfriedhof an der Longhua Lu liegen alle an der Strecke 2025). Pläne 2025 (Nr. 3087–
   3089): Streckenplan `https://media.shang-ma.com/bms/bkeq2u5mfMbpVKf5.JPG` (4739 × 6571 px, mit Kilometerkreisen, Getränkestellen,
   Schlusszeiten und kleinem Höhenbild), Startplan `…/TX2qqJKZV4BAV6yn.jpg`, Zielplan `…/5zxjL0DyRkeBhSmr.jpg`; Plan 2024
   `https://awsmedia.shang-ma.com/image/202411/1732545369350562.jpg` (dieselbe Strecke, dazu „半程点“ am Uferweg).
2. `plan.py`: blaue Linie des Plans 2025 als Pixel (`../dl/plan_blau.npy`, nur die zusammenhängende Fläche mit den Kilometerkreisen),
   Mitten der Kreise 1–42 (`plan2025.json`, von Hand grob gesucht und auf den Kreis gesetzt), Wendepunkte grob.
3. `osm.py`: OSM über die API (`api.openstreetmap.org/api/0.6/map`) in 307 Rechtecken zu 0,005° entlang einer groben Linie durch bekannte
   Punkte der Strecke (1,2 km Puffer), eine Abfrage je Sekunde (`../dl/osmapi/`) → `../dl/osm_netz.json` (11 589 Wege). Overpass war nicht
   nutzbar (overpass-api.de Verbindung abgebrochen, maps.mail.ru 504, kumi.systems und private.coffee Zeitüberschreitung). OSM ist WGS 84;
   chinesische Kartendienste (GCJ-02) wurden nicht benutzt.
4. **Linie** (`georef.py`, `linie.py`): Der Plan ist eine stark vereinfachte Zeichnung: Affin eingepasst (vier Ecken, dann ICP der
   blauen Pixel gegen OSM-Straßen) liegt die Linie im Median 24 m, an der Longteng Dadao bis 450 m neben den Straßen; zum Nachzeichnen
   taugt das nicht. `linie.py` baut die Linie deshalb aus der **Reihenfolge der Straßen**, die der Plan beschriftet: Wegpunkte sind die
   Kreuzungen, an denen die Strecke abbiegt (OSM-Knoten, an dem sich Wege beider Namen treffen), dazwischen der kürzeste Weg im
   OSM-Netz, wobei die Straße des Stücks einfach zählt, Wege ohne Namen 1,3-fach, Fuß- und Radwege 2-fach (am Ufer einfach), andere
   benannte Straßen 4-fach; Hochstraßen (高架), große Brücken (大桥), Tunnel und Rampen sind gesperrt. Folge: Zhongshan Dong Yi Lu
   (Start ein Drittel von der Fuzhou Lu zur Hankou Lu, Startplan), Zhongshan Dong Er Lu, Xinkaihe Lu, Renmin Lu, Henan Nan Lu/Henan
   Zhong Lu, Nanjing Dong Lu (OSM: 南京路步行街, Fußgängerzone) bis Hubei Lu, Hubei Lu, Jiujiang Lu, Nanjing Xi Lu bis Huashan Lu
   (Jing'an-Tempel), Huashan Lu, Changshu Lu, Huaihai Zhong Lu nach Osten, Madang Lu, Xingye Lu, Huangpi Nan Lu (kurz), Hubin Lu, Jinan
   Lu, Zizhong Lu, Huangpi Nan Lu nach Norden, Huaihai Zhong Lu, Xizang Nan Lu nach Süden, Gaoxiong Lu, Zhizaoju Lu, Longhua Dong Lu,
   Bansongyuan Lu nach Nordosten bis zur **Wende an der Nanchezhan Lu** (geschätzt) und zurück, Wangda Lu, Miaojiang Lu, Waima Lu,
   Bansongyuan Lu unter der Nanpu-Brücke, Lujiabang Lu, Waima Lu, **Uferweg am Huangpu** (OSM ohne Namen, im Plan „黄浦滨江步道 Huangpu
   Riverside“) zurück nach Südwesten, Miaojiang Lu, Longhua Dong Lu nach Westen, Furun Lu, Jiangbin Lu, Ruining Lu, Longteng Dadao nach
   Süden (über die Brücke am Longhua Gang) bis zur **Wende**, zurück nach Norden, **Stichstraße bei km 37** (im Plan „Fenggu Rd. 丰谷路“; in
   OSM heißt die Straße an dieser Stelle 瑞江路 Ruijiang Lu, das OSM-丰谷路 liegt 600–800 m weiter westlich; Lage aus dem Plan: 35 % des Wegs
   vom Westbund-Kunstzentrum zur Longheng Dong Lu, das passt nur auf die Ruijiang Lu) bis zur Yunjin Lu (Wende geschätzt, 464 m) und
   zurück, Longteng Dadao, Longheng Dong Lu, Wanping Nan Lu nach Norden, in spitzem Winkel auf die Longhua Lu nach Süden (Longhua-Tempel),
   Longhua Xi Lu, Zhongshan Nan Er Lu bis Tor 12 des Xujiahui-Sportparks, im Park nach dem Zielplan (eingepasst an Stadion, Hallenstadion
   und Schwimmhalle, Restfehler 3–4 m) zur Ziellinie südlich der Sponsorenfläche zwischen Hallenstadion und Stadion (379 m im Park).
   Die **Wende auf der Longteng Dadao** liegt so, dass die Linie 42 195 m lang ist: 5973 m südlich der Ruining Lu (31,1378° N, 570 m
   südlich der Mittleren Ringstraße), bei km 31,96. Der Plan zeigt sie kurz hinter km 32. → `linie2025.json`.
5. `common.py`, `marken.py`: **Kilometer** gleichmäßig über die Linie (Faktor 1, die Linie hat genau die Länge). Abgleich mit 14
   Kilometerkreisen des Plans an erkennbaren Stellen: Median 0,00 km, |Abweichung| im Median 0,15 km, höchstens 0,64 km (km 16 auf der
   Gaoxiong Lu: Die Linie erreicht sie erst bei km 16,4–16,9; km 8, 11, 13 liegen 0,2–0,35 km später als im Plan, km 1, 37, 40 0,15 km
   früher). km 20, 26, 27, 32, 37, 38 und die Halbmarathon-Matte am Uferweg (Plan 2024) passen auf 0,2 km. Die Spitzen im Höhenbild des
   Veranstalters an den Brücken liegen 0,2–0,7 km neben den OSM-Brücken (seine km-Achse ist ungenau). **Genauigkeit: Kilometer auf etwa
   ±0,3 km**, einzelne Stellen bis 0,6 km. Unsicher sind vor allem die drei Wenden (Bansongyuan Lu, Stichstraße, Longteng Dadao): Liegt
   eine von ihnen anders, verschiebt sich die Wende auf der Longteng Dadao um die Hälfte des Unterschieds.
6. `strassen.py`, `namen.py`, `orte.py`: Straße je 10 m aus dem OSM-Weg, auf dem die Linie liegt (nicht aus dem nächsten Weg: sonst
   tritt der Innere Ring, eine Hochstraße über der Zhongshan Nan Er Lu, an die Stelle der Straße darunter). **Namen:** Pinyin ohne Töne
   in der Schreibweise der Reiseführer (Nanjing Dong Lu, Huaihai Zhong Lu, Zhongshan Nan Er Lu, Longteng Dadao); Tabelle in `namen.py`,
   gegengelesen mit `name:en` in OSM und dem Plan. Begründung: Auf den Schildern in Shanghai stehen die Zeichen groß und darunter die
   Umschrift (meist „Nanjing Rd. (E)“), der Plan schreibt englisch („East Nanjing Rd.“); Zeichen sind für die meisten Nutzer nicht lesbar
   und machten die Zeile unter dem Profil doppelt so lang, Pinyin ist die amtliche Umschrift und liest sich wie in jedem Reiseführer.
   Die Zeichen stehen in `strassen.json`. Ohne Namen: „Huangpu-Uferweg“ (km 20,4–21,1), „Xujiahui-Sportpark“ (ab km 41,9).
   **Viertel** (`orte.py`): Straßenviertel (Jiedao, OSM admin_level 8) in Pinyin (Waitan = Bund, Yuyuan, Jing'ansi, Laoximen, Wuliqiao,
   Longhua, Changqiao, Caohejing, Xujiahui); wo das Viertel nach einer Straße heißt (Nanjing Dong Lu, Bansongyuan Lu, Huaihai Zhong Lu
   …), der Bezirk (Huangpu, Jing'an, Xuhui), weil „Xizang Nan Lu · Bansongyuan Lu“ sich wie zwei Straßen läse. Je 40 m links und rechts
   nachgesehen, bei zwei Seiten „links / rechts“. Bezirke: Huangpu km 0–4,8 und 9,4–24,9, Jing'an 4,8–8,0, Xuhui 8,0–9,4 und ab 24,9.
7. `fabdem.py`, `hoehen.py`, `dgm.py`, `planprofil.py`, `vergleich.py`, `clean.py`: **Höhe.**
   **Kein freies Laser- oder amtliches Geländemodell:** Amtliche Höhendaten gibt China nicht frei heraus (genaue Geodaten unterliegen den
   Vermessungs- und Geheimhaltungsvorschriften; nach meinem Kenntnisstand, nicht im Einzelnen geprüft). Das Datenportal der Stadt
   (`data.sh.gov.cn`) antwortet nur mit einer Browser-Prüfung (412 mit Skript), nicht umgangen; eine Suche nach einem Höhenmodell für
   Shanghai fand nichts Freies. Bleiben die globalen Modelle (alle ohne Anmeldung): FABDEM V1-2 (data.bris.ac.uk, Zip
   `N30E120-N40E130_FABDEM_V1-2.zip` per Teilabruf, nur Kachel N31E121), Copernicus GLO-30 (AWS `copernicus-dem-30m`), SRTM 1″ (AWS
   „skadi“). FathomDEM, ALOS, NASADEM nur mit Anmeldung (wie bei Athen geprüft).
   Vergleich alle 10 m (`vergleich.py`; Unruhe = mittlere |2. Differenz| je 10 m; „Plan“ = Höhenbild des Veranstalters auf seiner km-Achse):

   | Quelle | Start | Ziel | min | max (km) | ↑/↓ 200 m | ↑ 1 km | gegen FABDEM (Median) | Unruhe |
   |---|---|---|---|---|---|---|---|---|
   | FABDEM V1-2 (30 m) | 1,8 | 1,8 | 0,0 | 10,4 (3,29) | 67/67 | 21 | – | 0,047 |
   | Copernicus GLO-30 | 2,3 | 6,2 | 0,0 | 25,8 (3,29) | 235/232 | 56 | +1,8 | 0,258 |
   | SRTM 1″ (2000) | 12,7 | 4,8 | −2,3 | 62,4 (3,68) | 511/517 | 120 | +6,2 | 0,377 |
   | Höhenbild Veranstalter | 9,8 | 7,4 | 5,1 | 18,3 (27,43) | 57/59 | 21 | +7,8 | 0,008 |
   | App (Gelände + Brücken) | 2,7 | 1,8 | 0,4 | 11,5 (26,73) | 29/30 | 14 | −0,1 | 0,004 |
   | davon Gelände | 2,7 | 1,8 | 0,4 | 4,2 (32,26) | 16/17 | 11 | −0,1 | 0,001 |

   Mittel je 5 km (FABDEM / Höhenbild): 2,1/12,9 – 2,1/12,4 – 1,9/11,4 – 1,3/10,9 – 1,4/8,9 – 2,5/7,9 – 3,5/7,1 – 2,4/7,0 – 1,9/6,5.
   **Gewählt: FABDEM.** Es ist das einzige Geländemodell (ohne Häuser und Bäume) und das ruhigste. Die Stadt liegt auf 1–4 m (FABDEM: Bund
   und Innenstadt 2 m, Ufer bei der Nanpu-Brücke 1 m, West Bund an der Longteng Dadao 3–4 m, aufgeschüttetes Neubaugebiet). Copernicus
   und SRTM sind Oberflächenmodelle mit Häusern (Innenstadt bis 26 bzw. 62 m). Das **Höhenbild des Veranstalters** (`planprofil.py`, aus
   dem Plan 2025 abgelesen, Herkunft nicht angegeben) liegt 6–10 m höher und fällt von der Innenstadt (13 m) zum West Bund (7 m) wie SRTM
   aus dem Jahr 2000, als die Hochhäuser der Innenstadt schon standen und der West Bund noch Industrie war; vermutlich ein Oberflächenmodell
   oder eine GPS-Aufzeichnung. Für das Gelände nicht genommen. Es zeigt aber an genau den sechs Brücken der Strecke schmale Spitzen, auf
   Hin- und Rückweg gleich hoch (marken.py): Das sind die Fahrbahnen.
   **Gelände** (`clean.py`): FABDEM zeigt über dem Gelände fast nur Reste großer Häuser (10,4 m an der Nanjing Dong Lu/Hubei Lu, 4–6 m an der
   Nanjing Xi Lu am Volksplatz, 3–5 m an Huaihai Zhong Lu, Xizang Nan Lu, Miaojiang Lu) und an den Bächen das Wasser (0–0,6 m). Deshalb
   robust geglättet: lokal gewichtete Ausgleichsgerade über ±500 m (LOWESS, Tricube, vier Runden Bisquare), Werte über der Kurve zählen ab
   2·MAD nicht mehr, Werte darunter erst ab 6·MAD (Hausreste ragen nur nach oben). Abweichung vom Modell im Median 0,14 m, 90 % bis 1,2 m,
   höchstens 7,1 m (km 3,29). Mit ±300 m und gleichen Gewichten (`python3 clean.py 300 6`) blieben Buckel von 2,5 m an der Nanjing Xi Lu
   und der Xizang Nan Lu, ↑ Gelände 29 statt 16 m. **Wellen unter etwa einem Meter zeigt das Profil nicht**; ob es sie gibt (Rampen an
   Kreuzungen, der leicht erhöhte Uferweg), kann ein 30-m-Modell nicht sagen.
   **Brücken** (OSM bridge=yes auf der Linie; Hochstraßen und Tunnel benutzt die Strecke nicht, auch nicht unter der Erde: geprüft in
   `strassen.json`): Longteng Dadao über den Longhua Gang (km 26,51–26,96, 450 m, in OSM layer 2: Sie überspannt auch die Einmündung der Longheng Dong Lu), über den
   Zhangjiatang Gang (km 30,35 und 33,44, 140–150 m) und den Chunshen Gang (km 30,96 und 32,85, 120 m), Wanping Nan Lu über den Longhua
   Gang (km 38,52, 70 m). FABDEM rechnet die Fahrbahnen heraus und misst darunter Wasser; an der Longteng Dadao zeigt es vor dem Zhangjiatang
   Gang die Rampe (6 m). **Geschätzt** (schraffiert): Deck als halbe Kosinuswelle über die OSM-Brücke samt 20 m an jedem Ende auf das
   geglättete Gelände, Höhe aus dem Höhenbild (Spitze minus Mittel 0,2–0,5 km daneben): Longhua Gang +9,2 m (→ 11,5 m, Rampen bis 6 %),
   Zhangjiatang Gang +3,6 m (Mittel aus 3,6 und 3,7), Chunshen Gang +2,4 m (2,3/2,6), Wanping Nan Lu +2,4 m. Die Höhe der Brücke über den
   Longhua Gang ist die größte Unsicherheit im Profil; sie macht allein 9 der 29 Höhenmeter aus.
8. `build.py`: Höhen in cm im 10-m-Raster, Median über 30 m; Straßenstücke unter 80 m und Viertel unter 300 m dem Vorgänger zugeschlagen.
   **Marken** laut Wettkampfordnung 2026 („补给站“, an der km-Angabe): Getränke und Wasser (饮料/饮水) an km 5, 10, …, 40, Wasser und
   Schwämme (饮水/用水) an km 7,5, 12,5, …, 37,5. Energie (Riegel o. Ä.) nennt die Ordnung nicht; der Plan 2025 zeigt sie an 12,5, 15, 17,5, 25,
   27,5, 30, 32,5, 35, 37,5 und 40: dort „Verpflegung“ (food, mit „Energie laut Plan 2025“), sonst „Getränke“ bzw. „Wasser“. 16 Marken mit
   Halbmarathon. Nicht übernommen: die „补给点“ (kleine Kreise im Plan), die eigenen Getränke der Eingeladenen.
   `route.py` (lat0/lon0 31,2/121,45), `tiles.py` (z12–z15), `tiles_z11.py shanghai`, `app.py`, `tiles_rand.py shanghai 2`: 20 Kartenstücke,
   2,9 MB. Die OSM-Kartenbilder sind chinesisch beschriftet (wie die Schilder).

## Ergebnis

↑ 29 m / ↓ 30 m mit 200-m-Fenster, ↑ 39 / ↓ 40 m mit 50 m, ↑ 36 / ↓ 37 m mit 100 m, ↑ 14 / ↓ 14 m mit 1 km; wie GPS-Uhren 32 (ab 0,5 m),
22 (ab 1 m), 10 (ab 3 m); Rohdaten ↑ 149 m. Davon Gelände 16/17 m, Brücken 13 m. Start 2,7 m am Bund, Ziel 1,8 m im Xujiahui-Sportpark,
tiefster Punkt 0,4 m am Huangpu-Ufer bei der Nanpu-Brücke (km 20,4), höchster 11,5 m auf der Brücke der Longteng Dadao über den Longhua
Gang (km 26,73), im Gelände 4,2 m am West Bund (km 32,3). Flach durch die Innenstadt (1,5–3,4 m), am Ufer 0,5–1,5 m, am West Bund 2,5–4 m;
spürbar sind nur die Brücke über den Longhua Gang (+9 m, bis 4,3 % über 200 m, 5,7 % über 50 m) und die vier kleinen Brücken auf der
Longteng Dadao (2,4–3,6 m).
**Modellzeit:** Mit 4:00/km im Flachen ergibt das Modell **2:49:00** (das Profil kostet 13 s); **bei 2:50:00 kostet es 13 s, bei 4:00:00
19 s** (Flach-Pace 4:01,4 bzw. 5:40,8 /km; gemessen mit `pruefen.js` in der App 2.2). Zum Vergleich bei 2:50:00: Wien 61 s, Stockholm
113 s (Übergaben).

Geprüft mit Playwright (Chromium, 393 × 852, Faktor 2, Server auf Port 8792, `pruefen.js` … `pruefen4.js`): keine Konsolenfehler,
`APP_VERSION` 2.2 und Knopf v2.2, Service Worker installiert (Cache `sha-marathon-profil`), Tipp auf die Version meldet „Version 2.2 ist
aktuell“; alle 20 Kartenstücke passen zu `D.tiles` und `sw.js` (Größen geprüft); Tabellen bei 320/375/393/430 px ohne Überbreite, Seite
nicht breiter als das Fenster. Laufansicht am Start, km 11,5 (Xintiandi), 20,3 (Nanpu-Brücke), 26,7 (Brücke Longhua Gang, Karte und
Zahlen), 32 (Wende) und im Ziel, Kartenübersicht mit Verpflegung, Zuschauer-Tabelle mit drei Starts (2025) und nächstem Termin
6. Dezember 2026, „Woher die Zahlen kommen“ angesehen. Bilder in `work/shots/`. `kern.py` meldet „Alle gleich“.

## Offen

- Prüfung am iPhone.
- **Plan 2026**: erscheint auf shang-ma.com unter „赛事路线图“ (Nr. 3289), dazu Start- und Zielplan (3290, 3291), wohl Ende November.
  Dann vergleichen; weicht er ab, `linie.py` (Wegpunkte) anpassen und die Kette ab `strassen.py` neu laufen lassen. Ebenso die Startzeiten
  je Bereich (Mitteilung etwa eine Woche vorher) in `app.py` (`WELLEN`), die Getränkestellen und Energie.
- **Wendepunkte** (Daten 4/5): Bansongyuan Lu (an der Nanchezhan Lu angenommen), Stichstraße bei km 37 (Ruijiang Lu bis Yunjin Lu
  angenommen; der Plan schreibt „Fenggu Rd.“) und Longteng Dadao (aus der Länge). Ein GPS-Track eines Läufers von 2024/2025 würde das
  klären (Strava/Garmin nur mit Anmeldung, nicht benutzt).
- **Brücken**: Höhe der Fahrbahnen nur aus dem Höhenbild des Veranstalters (Daten 7). Eine Gegenprobe (Bauplan, Foto mit Maßstab, Lidar)
  gibt es nicht.
- Startseite: Karte fehlt (Eyebrow „Shanghai Marathon“, Stadt „Shanghai“, „Kurs 2025“, `data-termine="2025-11-30 2026-12-06"`,
  `data-monat="12"` (2023: 26.11., 2024: 1.12., 2025: 30.11., 2026: 6.12.; Wettkampfordnungen), ↑ 29 m / ↓ 30 m, Höhe 0–12 m, `data-such` z. B. „Shanghai China
  上海 上马 Bund Waitan Huangpu Xujiahui Abbott“; Mini-Profil mit 11 m Höhenbereich passt in die Grundhöhe 64 px), README-Tabelle und Liste
  der Präfixe (`sha-`). **Teilnehmer:** Die Zahl der Finisher 2025 hat der Veranstalter nicht veröffentlicht (gesucht: Seite des
  Veranstalters, Bericht „2025上海马拉松圆满收官“ vom 1.12.2025, Xinhua, 163.com, Tencent, Jing Daily). Belegt sind 23 000 Plätze
  (Wettkampfordnung 2025) und „两万三千名跑者从外滩金牛广场出发“ (Bericht des Veranstalters; ebenso 163.com, Tencent News 30.11.2025); 2024
  meldete der Veranstalter bei ebenfalls 23 000 Plätzen eine Finisherquote von 98,24 % (Tencent News 2.12.2024). Schätzung für 2025 also
  **gut 22 000 Finisher** (nicht belegt). 2026: 30 000 Plätze.
- Gegenprobe mit dem privaten Eichdatensatz (`course_segments`) nicht gemacht: Die Datei lag in dieser Sitzung nicht vor.
