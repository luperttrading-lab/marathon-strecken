# Erstausgabe der App für den Jungfrau-Marathon: Felder (Texte, const D, Speicher- und Cache-Präfix jfm, Kartenliste) für den gemeinsamen
# Kern -> felder.json, dann python3 werkzeuge/kern/kern.py --neu jungfrau werkzeuge/jungfrau/work/felder.json (nur beim ersten Mal; gibt es
# jungfrau/index.html schon, setzt dieses Skript die Felder dort selbst ein, über die Funktionen von kern.py).
# Muster: werkzeuge/luzern/work/app.py.
# Reihenfolge: parse.py, osm.py, strassen.py, strassenverz.py, bedeckt.py, dgm.py (mit swissalti.py), deck.py, clean.py, orte.py, build.py,
# route.py, tiles.py, dann aus werkzeuge/: tiles_z11.py jungfrau, jungfrau/work/app.py, tiles_rand.py jungfrau 2. Nur Abgleich: vergleich.py.
# Später allein laufen lassen geht: Gibt es jungfrau/index.html schon, bleiben Kartenbilder und D.tiles (von tiles_rand.py) stehen.
import json, os, shutil, subprocess, sys
R = "../../../"; OUT = R + "jungfrau/"
sys.path.insert(0, R + "werkzeuge/kern"); import kern
# Termin: 33. Jungfrau-Marathon am Samstag, 5. September 2026 (gelaufen; Rangliste Datasport „jungfrau-marathon-2026“, Bericht des
# Veranstalters vom 06.09.2026). 34. Austragung „10. / 11. September 2027“ (Startseite jungfrau-marathon.ch, „Nächste Austragungen“): Freitag
# die Freitagsrennen, Samstag, 11. September 2027 der Marathon, wie 2026 (4. und 5. September). Danach 8./9. September 2028, 7./8. September 2029.
# Start: Massenstart um 8.30 Uhr auf dem Höheweg in Interlaken, Richtung Osten (Race-Info 2026, Seite „Lauf-Infos“). Startblöcke nach
# erwarteter Laufzeit, alle im selben Start: deshalb keine Wellenknöpfe, nur der Text. Kontrollschlüsse laut Reglement 2026 und Seite „Strecke“.
WELLEN = {"q": "Massenstart um 8:30 Uhr auf dem Höheweg in Interlaken, Richtung Osten. Startblöcke nach erwarteter Laufzeit (Race-Info "
               "2026): Elite (Nummern 1–200), Block 1 bis 4:40, Block 2 4:40–5:10, Block 3 5:10–5:30, Block 4 5:30–5:50, Block 5 5:50–6:10, "
               "Block 6 6:10–6:30; Pacemaker mit Fahne für 5:00, 5:30, 6:00 und 6:30. Kontrollschluss in Wengen beim Bahnhof (km 30,7) "
               "nach 4:25 h Laufzeit, die Strecke schließt dort um 13:00 Uhr; an der Abzweigung Wixi auf der Wengernalp (km 38,5) nach 5:50 h, "
               "um 14:25 Uhr. Wer später kommt, darf nicht weiterlaufen und wird nicht klassiert. Ein Pace-Bike fährt im Tempo der "
               "Kontrollschlüsse, dahinter das Besen-Bike. Bergmarathon: ab Lauterbrunnen meist Wander- und Bergwege, Stöcke sind verboten.",
          "w": []}
D = {"wellen": WELLEN, "tz": "Europe/Zurich", "ort": "Interlaken", "ortKurz": " Interlaken", "termine": ["2026-09-05", "2027-09-11"], "start": 510}
D.update(json.load(open("data.json"))); D["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); D["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
D["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
# Kürzere Namen nur für die Zeile unter dem Profil (sonst passen dort die langen beschreibenden Namen oft nicht hin)
SHORT = {"Strasse über Gsteigwiler": "Gsteigwiler", "Wanderweg an der Lütschine": "Lütschine", "Bahnhof Zweilütschinen": "Zweilütschinen",
         "Wanderweg an der Weissen Lütschine": "Weisse Lütschine", "Wanderweg zum Trümmelbach": "Trümmelbach",
         "Strasse Wengen–Allmend": "Wengen–Allmend", "Bergweg Wixi–Haaregg": "Wixi–Haaregg", "Bergweg über die Moräne": "Moräne"}
NEU = not os.path.exists(OUT + "index.html")
if NEU:
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir("../assets"):
        if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
else:   # Kartenbilder und D.tiles so lassen, wie tiles_rand.py sie gesetzt hat
    D["tiles"] = json.loads(kern.lies_app("jungfrau")["teile"]["D"])["tiles"]
karte = ["./" + f for f in sorted(os.listdir(OUT)) if f.startswith("karte-")]
quellen = [z.strip()[4:-5] for z in open("quellen.html", encoding="utf-8").read().strip().split("\n")]
quellen.append("<b>Straßennamen:</b> " + open("strassennamen.html", encoding="utf-8").read().strip())
F = {"praefix": "jfm", "cachepraefix": "jfm-", "cachezeile": 'const CACHE = "jfm-marathon-profil";',
     "beschreibung": "Steigungsprofil des Jungfrau-Marathons von Interlaken zum Eigergletscher: Höhe, Steigung, Pace-Modell und Karte.",
     "titel": "Steigungsprofil Jungfrau-Marathon", "eyebrow": "Jungfrau-Marathon · Kurs 2026", "h1": "Jungfrau",
     "sub": open("sub.html", encoding="utf-8").read().strip(), "kartenquelle": "© OpenStreetMap-Mitwirkende",
     "quellen": quellen, "rohdaten": int(open("rohdaten.txt").read().strip()), "SHORT": SHORT, "karte": karte, "D": D}
json.dump(F, open("felder.json", "w"), ensure_ascii=False, indent=1)
if NEU:
    sys.exit(subprocess.call([sys.executable, R + "werkzeuge/kern/kern.py", "--neu", "jungfrau", os.path.abspath("felder.json")]))
# Seite gibt es schon: Felder ersetzen (Version und Kern bleiben)
d = kern.lies_app("jungfrau")
teile = dict(d["teile"], beschreibung=F["beschreibung"], titel=F["titel"], eyebrow=F["eyebrow"], h1=F["h1"], sub=F["sub"],
             kartenquelle=F["kartenquelle"], quellen="".join(f"      <li>{q}</li>\n" for q in quellen), rohdaten=str(F["rohdaten"]),
             D=json.dumps(D, ensure_ascii=False, separators=(",", ":")),
             SHORT="{ " + ", ".join(json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False) for k, v in SHORT.items()) + " }")   # Schreibweise wie kern.py --neu
kern.schreibe("jungfrau/index.html", kern.setze(d["kern"], teile))
kern.schreibe("jungfrau/sw.js", kern.setze(d["swkern"], dict(d["swteile"], karte=json.dumps(karte, ensure_ascii=False))))
print("jungfrau/ Felder ersetzt:", len(karte), "Kartenstücke")
