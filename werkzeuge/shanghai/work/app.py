# Erstausgabe der App für den Shanghai Marathon: Felder (Texte, const D, Speicher- und Cache-Präfix sha-, Kartenliste) für den gemeinsamen
# Kern -> felder.json, dann python3 werkzeuge/kern/kern.py --neu shanghai werkzeuge/shanghai/work/felder.json (nur beim ersten Mal; gibt
# es shanghai/index.html schon, setzt dieses Skript die Felder dort selbst ein, über die Funktionen von kern.py). Muster:
# werkzeuge/stockholm/work/app.py.
# Reihenfolge: plan.py, osm.py, georef.py (nur Kontrolle), linie.py, strassen.py, orte.py,
# fabdem.py, dgm.py, planprofil.py, vergleich.py (nur Abgleich), clean.py, build.py, marken.py (nur Abgleich), route.py, tiles.py, dann
# aus werkzeuge/: tiles_z11.py shanghai, shanghai/work/app.py, tiles_rand.py shanghai 2.
# Später allein laufen lassen geht: Gibt es shanghai/index.html schon, bleiben Kartenbilder und D.tiles (von tiles_rand.py) stehen.
import json, os, shutil, subprocess, sys
R = "../../../"; OUT = R + "shanghai/"
sys.path.insert(0, R + "werkzeuge/kern"); import kern
# Termin: 2026上海马拉松 am Sonntag, 6. Dezember 2026, 7:00 (Rollstühle 6:45), laut Wettkampfordnung 2026 („竞赛规程“, shang-ma.com) und
# Countdown der Startseite; 2025 war es Sonntag, der 30. November. 2027 ist nicht veröffentlicht.
# Starts: 2025 laut Mitteilung des Veranstalters vom 22.11.2025 („关于2025上海马拉松参赛相关事宜的公告“): 7:00 Eingeladene, Läufer mit
# Qualifikationszeit (预达级) und Startbereiche A und B, 7:10 C, 7:20 D und E. Für 2026 noch nicht veröffentlicht (2025 kam die
# Mitteilung acht Tage vor dem Lauf). Schlusszeiten 2026 laut Wettkampfordnung (Uhrzeit, für alle gleich).
WELLEN = {"q": "Startzeiten 2025 laut Veranstalter (Mitteilung vom 22.11.2025): 7:00 Eingeladene, Läufer mit Qualifikationszeit und "
               "Bereiche A und B, 7:10 Bereich C, 7:20 Bereiche D und E; der Bereich steht auf der Startnummer. 2026 beginnt der Marathon "
               "laut Wettkampfordnung wieder um 7:00 (Rollstühle 6:45), die Zeiten je Bereich sind noch nicht veröffentlicht. "
               "Schlusszeiten 2026 nach der Uhr, für alle gleich: km 10 8:50, km 15 9:35, km 20 10:20, km 25 11:00, km 30 11:45, "
               "km 35 12:30, km 40 13:15, Ziel 13:30 Uhr (2025 außerdem km 5 8:05). Medaille für alle, die in 6 Stunden im Ziel sind.",
          "w": [["Start 1", 420, "Elite, A und B"], ["Start 2", 430, "Bereich C"], ["Start 3", 440, "Bereiche D und E"]]}
D = {"wellen": WELLEN, "tz": "Asia/Shanghai", "ortKurz": " Shanghai", "termine": ["2025-11-30", "2026-12-06"], "start": 420}
D.update(json.load(open("data.json"))); D["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); D["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
D["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
NEU = not os.path.exists(OUT + "index.html")
if NEU:
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir("../assets"):
        if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
else:   # Kartenbilder und D.tiles so lassen, wie tiles_rand.py sie gesetzt hat
    D["tiles"] = json.loads(kern.lies_app("shanghai")["teile"]["D"])["tiles"]
karte = ["./" + f for f in sorted(os.listdir(OUT)) if f.startswith("karte-")]
quellen = [z.strip()[4:-5] for z in open("quellen.html", encoding="utf-8").read().strip().split("\n")]
quellen.append("<b>Straßennamen:</b> " + open("strassennamen.html", encoding="utf-8").read().strip())
F = {"praefix": "sha", "cachepraefix": "sha-", "cachezeile": 'const CACHE = "sha-marathon-profil";',
     "beschreibung": "Steigungsprofil des Shanghai Marathons: Höhe, Steigung, Pace-Modell und Karte.",
     "titel": "Steigungsprofil Shanghai Marathon", "eyebrow": "Shanghai Marathon · Kurs 2025", "h1": "Shanghai",
     "sub": open("sub.html", encoding="utf-8").read().strip(), "kartenquelle": "© OpenStreetMap-Mitwirkende",
     "quellen": quellen, "rohdaten": int(open("rohdaten.txt").read().strip()), "SHORT": {}, "karte": karte, "D": D}
json.dump(F, open("felder.json", "w"), ensure_ascii=False, indent=1)
if NEU:
    sys.exit(subprocess.call([sys.executable, R + "werkzeuge/kern/kern.py", "--neu", "shanghai", os.path.abspath("felder.json")]))
# Seite gibt es schon: Felder ersetzen (Version und Kern bleiben)
d = kern.lies_app("shanghai")
teile = dict(d["teile"], beschreibung=F["beschreibung"], titel=F["titel"], eyebrow=F["eyebrow"], h1=F["h1"], sub=F["sub"],
             kartenquelle=F["kartenquelle"], quellen="".join(f"      <li>{q}</li>\n" for q in quellen), rohdaten=str(F["rohdaten"]),
             D=json.dumps(D, ensure_ascii=False, separators=(",", ":")), SHORT="{}")
kern.schreibe("shanghai/index.html", kern.setze(d["kern"], teile))
kern.schreibe("shanghai/sw.js", kern.setze(d["swkern"], dict(d["swteile"], karte=json.dumps(karte, ensure_ascii=False))))
print("shanghai/ Felder ersetzt:", len(karte), "Kartenstücke")
