# Übergabe: Steigungsprofil Marathon des Châteaux du Médoc

Stand 30.10.2026, App-Version **2.1** (erste Fassung, veröffentlicht als Marathon 2.1, angelegt über den gemeinsamen Kern: `werkzeuge/kern/kern.py --neu medoc
work/felder.json`; Kern nur in `hamburg/` ändern, Änderungen am Kern in [`../kern/AENDERUNGEN.md`](../kern/AENDERUNGEN.md)).
Adresse nach dem Hochladen: https://luperttrading-lab.github.io/marathon-strecken/medoc/.

Speicherschlüssel `med-…`, Service-Worker-Cache `med-marathon-profil` (löscht nur Caches mit Präfix `med-`), ohne eigenes Manifest
und Symbol. Alle Entscheidungen zur Bedienung und zum Aussehen stehen in [`../hamburg/UEBERGABE.md`](../hamburg/UEBERGABE.md).
Startseite und README sind noch nicht angepasst (siehe Offen).

## Termin und Start

40. Marathon des Châteaux du Médoc am **Samstag, 5. September 2026** (gelaufen, Motto „Années 80“, Läuferheft
`guide-du-coureur-2026-40emepdf.pdf` und Plaquette Prestige 2026 des Veranstalters, AMCM). **41. Ausgabe am Samstag,
4. September 2027** laut Startseite, Nachricht „41ème édition du Marathon“, FAQ und Règlement 2027 auf https://www.marathondumedoc.com/
(daher ohne „?“); Motto 2027 „Expédition Médoc : à la conquête du monde !“ (FAQ, Nachricht). Achtung: 2027 ist der erste Samstag im
September, nicht wie oft der zweite. Anmeldung ab Anfang März 2027, höchstens 8500 Teilnehmer, ab 20 Jahren, 110 €.

**Start 9:30** auf den Quais von Pauillac, Ziel am selben Ort, eine Runde (Läuferheft 2026: „9h30 : Départ du marathon sur les quais
de Pauillac“; Règlement 2027 Art. 5: „Départ à 9h30 sur les Quais de Pauillac et arrivée au même endroit“). Keine Startblöcke oder
Wellen: `D.wellen` nur mit Hinweis (`w` leer, wie Paris). `D.termine` `["2026-09-05", "2027-09-04"]`, `D.tz` Europe/Paris,
`D.ort` „Pauillac“ (nach der Zeitzone hieße es „Paris“), `D.ortKurz` „ Pauillac“, `D.start` = 570.

**Zeitlimit 6:30 h** (Règlement Art. 5–7, FAQ, Läuferheft): Ziel also gegen 16:00. Eine Gruppe „coureurs balais“ (Besenläufer, im
Läuferheft „char balai“) läuft im Tempo von 6:30 h; wer hinter ihr ins Ziel kommt, wird nicht gewertet, und **zur Halbzeit wird die
Strecke hinter ihnen gesperrt** (Art. 6). Eine feste Uhrzeit nennt der Veranstalter dafür nicht (bei gleichmäßigem Tempo etwa
12:45 bei km 21,1). Nur im Text (Hinweis unter „Für Zuschauer“), kein `D.tor`: Der Tor-Rechner des Kerns erscheint nur bei
`D.mauer`. Sechs Zeitmatten („6 points de contrôle“, Lage nicht veröffentlicht). Straßensperren laut Läuferheft: D 206 bis 11:30, D 2
Richtung Bordeaux bis 13:30, D 205 bis 14:10, D 2 Richtung Saint-Estèphe bis 14:45, D 2E4 am Ufer bis 17:20.

Teilnehmer: 8051 Ergebnisse in der Gesamtwertung 2026 (Zeitnahme Chrono-Compétition, https://www.sport-info.com/i_resultats.php?id=331,
„Marathon du Médoc 2026“ → „Classement général“: „8051 résultats trouvés“; nur die Zahl gelesen). Höchstens 8500 Anmeldungen.

## Daten (`work/`, aus `work/` heraus starten; `../dl` und `../assets` bleiben lokal)

Reihenfolge: `parse.py`, `osm.py`, `linie.py`, `dgm.py`, `vergleich.py` (nur Abgleich), `strassen.py`, `orte.py`, `clean.py`,
`marken.py`, `build.py`, `route.py`, `tiles.py`, dann aus `werkzeuge/`: `tiles_z11.py medoc`, `medoc/work/app.py` (schreibt
`felder.json` und ruft `kern.py --neu medoc`; löscht vorher `medoc/index.html`), `tiles_rand.py medoc 2`, danach
`python3 werkzeuge/kern/kern.py` (muss „Alle gleich“ melden). `pruefen.js` prüft im Browser (siehe unten).

1. **Strecke** (`parse.py`): Die Seite „Plans“ des Veranstalters (https://www.marathondumedoc.com/plans/, „Parcours 2026“) bettet eine
   OpenRunner-Karte ein (Strecke 23032885). Deren Daten gibt die öffentliche Schnittstelle des Einbettens ohne Anmeldung heraus
   (`https://api.openrunner.com/api/v2/embedded-routes/<code aus dem iframe>`, `../dl/embedded.json`): Linie als Polyline, 580 Punkte,
   **42 277 m** auf dem Ellipsoid (OpenRunner selbst: 42 245 m), Start 45,20258 N / 0,74689 W auf dem Quai, Ende 20 m daneben; Höhen
   alle 100 m in ganzen Metern (Quelle unbekannt, „D+ 178“); 46 Punkte mit Linienmeter: 16 Wasser-Punkte („Bouteille d'eau“), 19
   Weinproben („Dégustation“), Frühstück, Cannelés, Austern, Entrecôte, Käse, Eis und 6 Sanitätszelte. Die Karte mit km-Schildern im
   Läuferheft 2026 (S. 18, „Temps de passage“) ist dieselbe OpenRunner-Linie. → `openrunner.json`.
2. `osm.py`: OSM-Wege (highway, railway) im Rechteck 45,135–45,275 N, 0,805–0,725 W über Overpass (overpass-api.de brach die Verbindung
   ab, maps.mail.ru 504, **overpass.kumi.systems** lieferte, 2840 Wege) → `../dl/osm_wege.json`. Dazu Châteaux (`name` „Château …“,
   „Cave …“, „Domaine …“, `../dl/osm_chateaux.json`, kumi) und Weiler (`place`, `../dl/osm_orte.json`, maps.mail.ru).
3. `linie.py`: **Prüfung gegen OSM, keine Berichtigung.** Die Linie liegt im Median 1,7 m neben dem nächsten OSM-Weg, 95 % bis 4,7 m;
   nur an sieben kurzen Stellen 15–46 m daneben, und zwar dort, wo sie durch Château-Höfe und Rebzeilen ohne OSM-Weg läuft (größte bei
   km 33,0 am Château Tronquoy-Lalande, genau an einer „Dégustation“ der Karte; ebenso km 34,2 Phélan-Ségur, km 29,3). Deshalb nicht
   auf OSM gelegt (anders als Athen). → `gpx2026.json`. Wegarten unter der Linie laut OSM: secondary 13,2 km, tertiary 12,0,
   service 6,6, unclassified 5,4, track 3,9, sonst 1,2 km; ausdrücklich unbefestigt (surface gravel/unpaved oder track ohne Belag)
   4,5 km = 11 %. Der Veranstalter nennt 24 % „chemins de grave“ (Règlement Art. 7); in OSM fehlt bei vielen Hof- und Feldwegen die
   Angabe zum Belag.
4. `common.py`: **Kilometer gleichmäßig gestaucht** (Linie 42 277 m auf 42 195 m, Faktor 0,99806). Die Lage der Kilometerschilder und
   der sechs Zeitmatten ist nicht veröffentlicht; die km-Schilder der Karte im Läuferheft setzt OpenRunner selbst. Gegenproben: Die
   km-Angaben der 16 Stände in der Plaquette (ganze km) passen zu den Wasser-Punkten der Karte (km 3,06 / 6,71 / 10,17 / 12,43 / 14,27 /
   16,26 / 17,86 / … / 39,16 gegen „3 / 7 / 10 / 12 / 13 / 16 / 18 / … / 39“; nur Ducru-Beaucaillou „13e km“ liegt bei 14,27, das Château
   selbst laut OSM bei 13,98). **Genauigkeit etwa ±50 m** (Linie entlang der Wegmitte; wie viel der Überlänge auf Kurven entfällt, ist
   unbekannt). Die Plaquette nennt das Ziel scherzhaft bei „42,3e km“.
5. `dgm.py`: **RGE ALTI 1 m der IGN** (Höhen über NGF-IGN69, Licence Ouverte Etalab 2.0) über den Höhendienst der Géoplateforme
   (`https://data.geopf.fr/altimetrie/1.0/calcul/alti/rest/elevation.json?lon=…|…&lat=…|…&resource=ign_rge_alti_wld&zonly=true`,
   **frei ohne Anmeldung**, nur GET, je 100 Punkte wie Paris), alle 10 Linienmeter, 4229 Punkte, keine Lücke → `dgm2026_10m.json`.
   Im selben Lauf **LiDAR HD MNT** (Ressource `ign_lidar_hd_mnt_multi_wld`, Geländemodell aus dem neuen Laserscan der IGN, 50-cm-Raster,
   „Pas de 50 cm“; deckt das Médoc schon ab) → `dgm_vergleich.json`. Copernicus GLO-30 (Kachel N45 W001 von
   `copernicus-dem-30m.s3.amazonaws.com`, ohne Anmeldung) liest `vergleich.py` selbst. BD ALTI 25 m nicht geholt (RGE ALTI und LiDAR HD
   sind feiner und stimmen überein).
6. `vergleich.py`: **Vergleich der Quellen** (offizielle km, 10-m-Raster, Median über 30 m; ohne Brückenbereinigung; Unruhe = mittlere
   |2. Differenz| je 10 m; OpenRunner = Höhen der Veranstalter-Karte alle 100 m):

   | Quelle | Start | Ziel | min | max | ↑/↓ 200 m | ↑/↓ 1 km | gegen RGE ALTI (Median / 95 % \|Δ\|) | r | Unruhe |
   |---|---|---|---|---|---|---|---|---|---|
   | RGE ALTI 1 m | 4,2 | 4,0 | 2,6 | 28,3 | 204/204 | 93/93 | – | – | 0,061 |
   | LiDAR HD MNT 50 cm | 4,4 | 4,1 | 2,4 | 28,3 | 203/204 | 93/93 | −0,05 / 0,24 m | 0,9998 | 0,044 |
   | Copernicus GLO-30 | 6,8 | 5,9 | 1,7 | 31,9 | 223/224 | 93/94 | −0,44 / 2,50 m | 0,9853 | 0,125 |
   | OpenRunner (Karte) | 6,0 | 6,0 | 1,0 | 28,0 | 167/167 | 89/89 | −0,52 / 3,06 m | 0,9744 | 0,007 |

   Je 5 km (↑/↓, 200-m-Fenster) RGE ALTI / LiDAR HD / Copernicus / OpenRunner: 0–5 28/4 · 28/4 · 31/8 · 28/6; 5–10 8/22 · 8/21 · 12/24 ·
   5/16; 10–15 21/30 · 21/30 · 18/28 · 10/19; 15–20 41/28 · 41/28 · 45/33 · 31/21; 20–25 33/35 · 33/35 · 36/38 · 28/31; 25–30 32/30 ·
   33/31 · 34/32 · 29/26; 30–35 31/38 · 31/39 · 32/39 · 19/28; 35–40 9/15 · 9/15 · 11/17 · 11/17; 40–42,2 1/2 · 1/2 · 5/4 · 6/3.
   **Gewählt RGE ALTI**, wie gewünscht und wie Paris; der Laserscan LiDAR HD bestätigt ihn fast punktgenau (90 % der Punkte innerhalb
   −0,22 bis +0,18 m, gleiche Höhenmeter). Copernicus ist ein Oberflächenmodell (Reben, Häuser, Bäume) und unruhiger; die
   OpenRunner-Höhen sind auf 100 m und ganze Meter gerundet und glätten die kurzen Kuppen weg (daher 167 statt 204 m).
7. `strassen.py`, `namen.py`: Weg je 10 m: nächster OSM-Weg höchstens 30 m neben der Linie (Straßen mit kleinem Vorzug, Wege quer zur
   Laufrichtung mit Aufschlag). Bezeichnung: `name` aus OSM (französisch, z. B. „Route des Châteaux“, „Communale n°64“, „Grand' Rue“);
   sonst die Nummer der Départementstraße („D 206“, „D 101“, „D 205“, „D 2“); Ortsstraßen ohne Namen „Weg in <Weiler>“; **Feld- und
   Hofwege ohne Namen nach dem nächsten Château bis 600 m** („Weg am Château Lafite-Rothschild“), sonst nach dem nächsten Weiler
   („Weg bei Marbuzet“, „Weinbergsweg bei Meyney“). Entscheidung: Auf den Weinbergswegen orientiert man sich an den Châteaux, die auf
   der Karte des Veranstalters stehen; der Text unter „Straßennamen“ sagt, dass das eine Ortsangabe ist, nicht der Besitzer.
   Schreibweise der Châteaux wie in der Liste der Plaquette (Bindestriche, `namen.EINHEIT`). Start (erste 20 m) und Zielgerade (letzte
   160 m, in OSM ein Hofweg neben dem Quai) heißen „Quai Jean Fleuret“ (`build.py`).
8. `orte.py`: **Gemeinde** alle 100 m aus ADMIN EXPRESS der IGN (WFS `data.geopf.fr/wfs/ows`, Layer `ADMINEXPRESS-COG.LATEST:commune`,
   `../dl/commune.geojson`), auf Grenzen beide. Ergebnis: Pauillac (km 0–6,3), Saint-Laurent-Médoc (–9,3), Saint-Julien-Beychevelle
   (–17,3), Pauillac (–26,2), Saint-Estèphe (–39,4), Pauillac (bis Ziel).
9. `clean.py`: **Brücken** aus OSM (bridge=yes auf der Linie). Einzige: D 2 (Route de Bordeaux) über die **Jalle du Breuil** an der
   Grenze Pauillac/Saint-Estèphe (km 26,21–26,24; Bach laut OSM-API 5 m neben der Brücke, `../dl/osmapi_bruecke.xml`); das Modell liegt
   dort 0,5 m unter der Geraden, gerade gezogen, im Läuferblick gestrichelt. **Stufe nur im RGE ALTI**: km 26,38–26,39 misst das
   1-m-Raster 1,6 m tiefer und dann eine Stufe von 3,3 m (Graben oder Durchlass neben der Fahrbahn am Anstieg nach Saint-Estèphe),
   LiDAR HD ist dort glatt: über 70 m durch LiDAR HD ersetzt, an den Enden angeglichen. Sonst keine Stufe über 1,5 m je 10 m, keine
   Unterführung, kein Tunnel.
10. `marken.py`, `build.py`: Höhen in cm im 10-m-Raster, Median über 30 m; Wegstücke unter 80 m und Gemeinden unter 300 m dem Vorgänger
    zugeschlagen. **Marken** (42): Lage aus der OpenRunner-Karte (Punkte auf die Linie projiziert, meist 0–28 m daneben).
    - 16 **Verpflegungsstände** mit Namen und km laut Plaquette Prestige 2026 (S. 12 „Les responsables des stands de ravitaillement“;
      **nur Stand und km übernommen, keine Personennamen**), an den Wasser-Punkten der Karte: Château Grand-Puy-Lacoste km 3,1,
      Larose-Trintaudon 6,7, Lagrange 10,2, Beychevelle 12,4, Ducru-Beaucaillou 14,3, Saint-Julien 16,3, Pichon-Longueville 17,9,
      Cave La Rose Pauillac 21,2 (in der Karte ohne Wasser-Punkt: Lage nach OSM, 16 m neben der Linie), d'Armailhac 23,7,
      Lafite-Rothschild 25,6, Lafon-Rochet 27,7, Le Crock 30,6, Tronquoy-Lalande 33,1, Phélan-Ségur 34,1, Montrose 37,2, „Gironde 1“
      39,2. Angebot laut Läuferheft: Wasser, Cola, Orangen, Bananen, süße und salzige Kekse, Zucker, Energieriegel (`n` kurz:
      „Wasser, Cola, Obst, Kekse“).
    - „Rencontres gustatives insolites“ (Plaquette S. 12, Lage aus der Karte): Frühstück km 3,4, Cannelés km 21,3, **Austern km 37,2,
      Entrecôte km 38,8, Käse km 40,8, Eis km 41,3**. Nicht übernommen: „Remise en beauté“ km 41 (kein Essen, nicht in der Karte).
    - 19 **Weinproben** („Dégustation“ der Karte, `s` „Wein“; welches Château ausschenkt, sagt die Karte nicht). Eine liegt 131 m neben
      der Linie (km 40,85, Pauillac), trotzdem übernommen.
    - Halbmarathon-Marke bei 21 098 m (es gibt keinen Halbmarathon-Lauf). Keine Staffel. Sanitätszelte nicht übernommen.
    Kategorien: Stände und Essen `food`, Weinproben `water` (beide grau, nur mit Schalter „Verpflegung“ im Profil).
    `route.py` (lat0/lon0 45,2/−0,8), `tiles.py` (z12–z15, Kopie aus Wien), dann `tiles_z11.py medoc`, `app.py`, `tiles_rand.py medoc 2`:
    28 Kartenstücke, 2,1 MB. `tiles_z11.py` und `tiles_rand.py` brauchen keinen Eintrag je Strecke (nur `medoc/` muss es geben).

## Ergebnis

↑ 204 m / ↓ 204 m mit 200-m-Fenster, ↑ 247 / ↓ 247 m mit 50 m, ↑ 232 / ↓ 232 m mit 100 m, ↑ 93 / ↓ 93 m mit 1 km, Rohdaten ↑ 301 m.
Start 4,2 m auf dem Quai von Pauillac, Ziel 4,0 m; höchster Punkt **28,3 m** an der D 206 Richtung Saint-Laurent (km 5,2), tiefster
**2,6 m** an der Jalle du Breuil (km 26,1); Höhenbereich 25,7 m (Höhen über NGF-IGN69). Gleich hinter der Stadt hinauf auf die
Kiesrücken (20 m bei km 2), danach ein ständiges Auf und Ab zwischen 3 und 25 m: jede Senke ein Bach zur Gironde (Beychevelle km 15:
4,9 m, Pauillac km 21,5: 3,4 m, Jalle du Breuil km 26: 2,6 m, Saint-Estèphe km 34,3: 3,4 m), jede Kuppe ein Weinberg (Pontet-Canet/
Mouton km 23,2: 24,7 m, Lafon-Rochet km 27,8: 25,3 m, Tronquoy km 32,5: 23 m). Ab km 36 flach am Ufer der Gironde (3–5 m) bis ins
Ziel. Steilste Stellen über 200 m: **+5,9 %** von der Jalle du Breuil hinauf nach Saint-Estèphe (km 26,44), −4,1 % bei km 34,1
(Phélan-Ségur); über 50 m +8,6 % bei km 30,6 (Marbuzet). Im 1-km-Fenster höchstens ±2 %.

Mit 4:00/km im Flachen ergibt das Modell **2:50:52** (das Profil kostet 125 s); **bei 2:50:00 kostet es 124 s, bei 4:00:00 175 s**
(Flach-Pace 3:58,8 bzw. 5:37,1 /km). Damit etwa wie Kapstadt (123 s bei 2:50), deutlich mehr als Wien (61 s), weniger als Athen (213 s):
wenig Höhe, aber sehr viele kurze Wellen.

Geprüft mit Playwright (`work/pruefen.js`, Chromium, 393 × 852, Faktor 2, Server auf Port 8782): keine Konsolenfehler und keine
fehlgeschlagenen Abrufe, `APP_VERSION` 2.0, Knopf „v2.0“, Service Worker aktiv (34 Einträge im Cache `med-marathon-profil`), Tipp auf
die Version meldet „Version 2.0 ist aktuell“; alle Abschnitte aufgeklappt bei 320 / 375 / 393 / 430 px: Seite nicht breiter als das
Fenster, keine der 4 Tabellen zu breit. Laufansicht bei km 5,2 (D 206, 28,2 m), 14,0 (Weg am Château Ducru-Beaucaillou), 26,4 (Route
de Bordeaux, Saint-Estèphe, +5,3 %), 37,2 und 38 (Route de Loudenne, Verpflegung eingeschaltet, Karte herausgezoomt) angesehen.
Bilder: `work/shots/lauf_karte_km5.png`, `lauf_karte_km14_ducru.png`, `lauf_zahlen_km26_saintestephe.png`,
`lauf_karte_km37_austern.png`, `lauf_karte_uebersicht_km38_verpflegung.png`. `kern.py`: „Alle gleich“.

## Offen

- Prüfung am iPhone.
- Startseite: Karte für Médoc fehlt (Eyebrow „Marathon des Châteaux du Médoc“, Ort „Médoc“ bzw. „Pauillac“, „Kurs 2026“,
  `data-termine="2026-09-05 2027-09-04"`, `data-monat="9"`, ↑ 204 m / ↓ 204 m, Höhe 3–28 m; Mini-Profil im gemeinsamen Maßstab nur
  36 px Höhenbereich, Grundhöhe 64 px reicht; `data-such` z. B. „Medoc Médoc Pauillac Châteaux Chateaux Wein Bordeaux Frankreich
  France Saint-Julien Saint-Estèphe“), README-Tabelle und Liste der Präfixe (`med-`).
- **Strecke 2027**: Der Veranstalter ändert die Strecke oft leicht von Jahr zu Jahr. Sobald „Parcours 2027“ auf der Seite „Plans“ steht
  (2026 im Juli), `parse.py` mit dem neuen OpenRunner-Code und die Kette neu laufen lassen; Stände nach der Plaquette 2027.
- Kilometer nur über die Länge geeicht (±50 m); Lage der sechs Zeitmatten oder der Schilder prüfen, falls veröffentlicht.
- Halbzeit-Sperre hinter den Besenläufern ohne feste Uhrzeit: Falls der Veranstalter eine Uhrzeit nennt, wäre ein Tor-Rechner
  sinnvoll; der Kern zeigt `D.tor` bisher nur zusammen mit `D.mauer` (Great Wall).
- Weinproben ohne Namen der Châteaux; falls eine Liste „Dégustations 2027“ erscheint, in `build.py` nachtragen.
