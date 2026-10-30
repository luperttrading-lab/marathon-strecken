# Erstausgabe der App für den Stockholm Marathon: Felder (Texte, const D, Speicher- und Cache-Präfix sth-, Kartenliste) für den
# gemeinsamen Kern -> felder.json, dann python3 werkzeuge/kern/kern.py --neu stockholm werkzeuge/stockholm/work/felder.json (nur
# beim ersten Mal; gibt es stockholm/index.html schon, setzt dieses Skript die Felder dort selbst ein, über die Funktionen von
# kern.py). Muster: werkzeuge/wien/work/app.py (noch aus tokio kopiert) und kern.py --felder wien.
# Reihenfolge: parse.py, osm.py, strassen.py, fabdem.py, dgm.py, vergleich.py (nur Abgleich), clean.py, orte.py, build.py, route.py,
# tiles.py, dann aus werkzeuge/: tiles_z11.py stockholm, stockholm/work/app.py, tiles_rand.py stockholm 2.
# Später allein laufen lassen geht: Gibt es stockholm/index.html schon, bleiben Kartenbilder und D.tiles (von tiles_rand.py) stehen.
import json, os, shutil, subprocess, sys
R = "../../../"; OUT = R + "stockholm/"
sys.path.insert(0, R + "werkzeuge/kern"); import kern
# Termin: 48. adidas Stockholm Marathon am Samstag, 29. Mai 2027 (Veranstalter, Seite „About the race 2027“: „DATE May 29 2027 |
# Prel. Start at 12:00“, Startseite „29 Maj 2027 – slutsålt“); der 47. war am Samstag, 30. Mai 2026 (gelaufen).
# Starts 2026 laut „Participant Information 2026“ (drei Starts, Startgruppen A–J nach früheren Ergebnissen).
WELLEN = {"q": "Drei Starts 2026 laut Veranstalter, die Startgruppe (A–J, nach früheren Ergebnissen) steht auf der Startnummer. Die Uhren "
               "an der Strecke laufen ab 12:00 (Start 2: 8 min abziehen, Start 3: 16 min). Zeitlimit 6:30 h; die Kontrollen schließen "
               "unabhängig vom eigenen Start: km 21,1 Slussen 15:35, km 27 Heleneborgsgatan 16:25, km 32 Fleminggatan 17:15, km 35,5 "
               "Vasagatan/Tegelbacken 17:45 Uhr. 2027: Start voraussichtlich 12:00, Starts noch nicht veröffentlicht.",
          "w": [["Start 1", 720, "Gruppen A–C · A: Elite"], ["Start 2", 728, "Gruppen D–F"], ["Start 3", 736, "Gruppen G, H, J"]]}
D = {"wellen": WELLEN, "tz": "Europe/Stockholm", "termine": ["2026-05-30", "2027-05-29"], "start": 720}
D.update(json.load(open("data.json"))); D["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); D["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
D["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
NEU = not os.path.exists(OUT + "index.html")
if NEU:
    for f in os.listdir("../assets"):
        if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
else:   # Kartenbilder und D.tiles so lassen, wie tiles_rand.py sie gesetzt hat
    D["tiles"] = json.loads(kern.lies_app("stockholm")["teile"]["D"])["tiles"]
karte = ["./" + f for f in sorted(os.listdir(OUT)) if f.startswith("karte-")]
quellen = [z.strip()[4:-5] for z in open("quellen.html", encoding="utf-8").read().strip().split("\n")]
quellen.append("<b>Straßennamen:</b> " + open("strassennamen.html", encoding="utf-8").read().strip())
F = {"praefix": "sth", "cachepraefix": "sth-", "cachezeile": 'const CACHE = "sth-marathon-profil";',
     "beschreibung": "Steigungsprofil des Stockholm Marathons: Höhe, Steigung, Pace-Modell und Karte.",
     "titel": "Steigungsprofil Stockholm Marathon", "eyebrow": "adidas Stockholm Marathon · Kurs 2026", "h1": "Stockholm",
     "sub": open("sub.html", encoding="utf-8").read().strip(), "kartenquelle": "© OpenStreetMap-Mitwirkende",
     "quellen": quellen, "rohdaten": int(open("rohdaten.txt").read().strip()), "SHORT": {}, "karte": karte, "D": D}
json.dump(F, open("felder.json", "w"), ensure_ascii=False, indent=1)
if NEU:
    sys.exit(subprocess.call([sys.executable, R + "werkzeuge/kern/kern.py", "--neu", "stockholm", os.path.abspath("felder.json")]))
# Seite gibt es schon: Felder ersetzen (Version und Kern bleiben)
d = kern.lies_app("stockholm")
teile = dict(d["teile"], beschreibung=F["beschreibung"], titel=F["titel"], eyebrow=F["eyebrow"], h1=F["h1"], sub=F["sub"],
             kartenquelle=F["kartenquelle"], quellen="".join(f"      <li>{q}</li>\n" for q in quellen), rohdaten=str(F["rohdaten"]),
             D=json.dumps(D, ensure_ascii=False, separators=(",", ":")), SHORT="{}")
kern.schreibe("stockholm/index.html", kern.setze(d["kern"], teile))
kern.schreibe("stockholm/sw.js", kern.setze(d["swkern"], dict(d["swteile"], karte=json.dumps(karte, ensure_ascii=False))))
print("stockholm/ Felder ersetzt:", len(karte), "Kartenstücke")
