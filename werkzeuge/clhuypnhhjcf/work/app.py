# Versteckte App für die Hausrunde des Nutzers am Schiffenberg (Gießen): Felder (Texte, const D, Speicher- und Cache-Präfix hrs-,
# Kartenliste) für den gemeinsamen Kern -> felder.json, dann python3 werkzeuge/kern/kern.py --neu clhuypnhhjcf
# werkzeuge/clhuypnhhjcf/work/felder.json (nur beim ersten Mal; gibt es clhuypnhhjcf/index.html schon, setzt dieses Skript die Felder
# dort selbst ein, über die Funktionen von kern.py). Muster: werkzeuge/hannover/work/app.py.
# Der Ordnername ist absichtlich nicht erratbar: Die Runde steht nicht auf der Startseite, nicht im README und nicht in karten.json.
# Reihenfolge: parse.py, osm.py, strassen.py, dgm.py, clean.py, orte.py (nur Ausgabe), build.py, route.py, tiles.py, dann aus
# werkzeuge/: tiles_z11.py clhuypnhhjcf, clhuypnhhjcf/work/app.py, tiles_rand.py clhuypnhhjcf 2. Später allein laufen lassen geht:
# Gibt es clhuypnhhjcf/index.html schon, bleiben Kartenbilder und D.tiles stehen.
import json, os, shutil, subprocess, sys
ORDNER = "clhuypnhhjcf"
R = "../../../"; OUT = R + ORDNER + "/"
sys.path.insert(0, R + "werkzeuge/kern"); import kern
# Kein Rennen: keine Termine, keine Wellen, keine Staffel, keine Halbmarathon-Marke. Startzeit 18:00 (Feierabendrunde).
D = {"tz": "Europe/Berlin", "start": 1080}
D.update(json.load(open("data.json"))); D["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); D["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
D["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
NEU = not os.path.exists(OUT + "index.html")
if NEU:
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir("../assets"):
        if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
else:   # Kartenbilder und D.tiles so lassen, wie tiles_rand.py sie gesetzt hat
    D["tiles"] = json.loads(kern.lies_app(ORDNER)["teile"]["D"])["tiles"]
karte = ["./" + f for f in sorted(os.listdir(OUT)) if f.startswith("karte-")]
quellen = [z.strip()[4:-5] for z in open("quellen.html", encoding="utf-8").read().strip().split("\n")]
quellen.append("<b>Wegnamen:</b> " + open("strassennamen.html", encoding="utf-8").read().strip())
F = {"praefix": "hrs", "cachepraefix": "hrs-", "cachezeile": 'const CACHE = "hrs-marathon-profil";',
     "beschreibung": "Steigungsprofil der Hausrunde am Schiffenberg bei Gießen: Höhe, Steigung, Pace-Modell und Karte.",
     "titel": "Steigungsprofil Hausrunde Schiffenberg", "eyebrow": "Hausrunde Schiffenberg", "h1": "Schiffenberg",
     "sub": open("sub.html", encoding="utf-8").read().strip(), "kartenquelle": "© OpenStreetMap-Mitwirkende",
     "quellen": quellen, "rohdaten": int(open("rohdaten.txt").read().strip()), "SHORT": {}, "karte": karte, "D": D}
json.dump(F, open("felder.json", "w"), ensure_ascii=False, indent=1)
if NEU:
    sys.exit(subprocess.call([sys.executable, R + "werkzeuge/kern/kern.py", "--neu", ORDNER, os.path.abspath("felder.json")]))
# Seite gibt es schon: Felder ersetzen (Version und Kern bleiben)
d = kern.lies_app(ORDNER)
teile = dict(d["teile"], beschreibung=F["beschreibung"], titel=F["titel"], eyebrow=F["eyebrow"], h1=F["h1"], sub=F["sub"],
             kartenquelle=F["kartenquelle"], quellen="".join(f"      <li>{q}</li>\n" for q in quellen), rohdaten=str(F["rohdaten"]),
             D=json.dumps(D, ensure_ascii=False, separators=(",", ":")), SHORT="{}")
kern.schreibe(ORDNER + "/index.html", kern.setze(d["kern"], teile))
kern.schreibe(ORDNER + "/sw.js", kern.setze(d["swkern"], dict(d["swteile"], karte=json.dumps(karte, ensure_ascii=False))))
print(ORDNER + "/ Felder ersetzt:", len(karte), "Kartenstücke")
