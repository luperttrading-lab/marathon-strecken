# Erstausgabe der App für den Marathon des Châteaux du Médoc über den gemeinsamen Kern (seit Marathon 2.0): Felder (Texte, const D,
# Präfix med-, Kartenliste) -> felder.json -> python3 werkzeuge/kern/kern.py --neu medoc felder.json. Ohne eigenes Manifest und
# Symbol (verweist auf ../manifest.webmanifest). Danach wird direkt in medoc/index.html gearbeitet; dieses Skript ist nur die Herkunft.
# Reihenfolge: parse.py, osm.py, linie.py, dgm.py, vergleich.py (nur Abgleich), strassen.py, orte.py, clean.py, marken.py, build.py,
# route.py, tiles.py, dann aus werkzeuge/: tiles_z11.py medoc, medoc/work/app.py, tiles_rand.py medoc 2
# Achtung: legt medoc/index.html neu an (löscht eine vorhandene; danach muss tiles_rand.py folgen).
import json, os, re, shutil, subprocess
R = "../../../"; OUT = R + "medoc/"
os.makedirs(OUT, exist_ok=True)
# 40. Marathon des Châteaux du Médoc am Samstag, 5. September 2026 (gelaufen, Motto „Années 80“); 41. am Samstag, 4. September 2027
# laut Veranstalter (Startseite, FAQ, Règlement 2027: Motto „Expédition Médoc : à la conquête du monde !“), Start 9:30 auf den
# Quais von Pauillac, ein gemeinsamer Start ohne Blöcke, Zeitlimit 6:30 h (Besenläufer; zur Halbzeit wird hinter ihnen gesperrt).
WELLEN = {"q": "Ein gemeinsamer Start um 9:30 auf den Quais von Pauillac, ohne Startblöcke (Läuferheft 2026, Règlement 2027). "
               "Zeitlimit 6:30 h: Besenläufer laufen im Tempo von 6:30 h, wer hinter ihnen ist, wird nicht gewertet; zur Halbzeit "
               "wird die Strecke hinter ihnen gesperrt.", "w": []}
data = {"wellen": WELLEN, "tz": "Europe/Paris", "ort": "Pauillac", "ortKurz": " Pauillac", "termine": ["2026-09-05", "2027-09-04"], "start": 570}
data.update(json.load(open("data.json"))); data["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); data["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
data["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
for f in os.listdir("../assets"):
    if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
maps = sorted(f for f in os.listdir(OUT) if f.startswith("karte-"))
quellen = [re.fullmatch(r"\s*<li>(.*)</li>", z).group(1) for z in open("quellen.html", encoding="utf-8").read().strip().split("\n")]
quellen.append("<b>Straßennamen:</b> " + open("strassennamen.html", encoding="utf-8").read().strip())
F = {"praefix": "med", "cachepraefix": "med-", "cachezeile": 'const CACHE = "med-marathon-profil";',
     "beschreibung": "Steigungsprofil des Marathon des Châteaux du Médoc: Höhe, Steigung, Pace-Modell und Karte.",
     "titel": "Steigungsprofil Marathon du Médoc", "eyebrow": "Marathon des Châteaux du Médoc · Kurs 2026", "h1": "Médoc",
     "sub": open("sub.html", encoding="utf-8").read().strip(), "kartenquelle": "© OpenStreetMap-Mitwirkende",
     "quellen": quellen, "rohdaten": int(open("rohdaten.txt").read()), "SHORT": {}, "karte": ["./" + f for f in maps], "D": data}
json.dump(F, open("felder.json", "w"), ensure_ascii=False, indent=0)
if os.path.exists(OUT + "index.html"): os.remove(OUT + "index.html")
subprocess.run(["python3", R + "werkzeuge/kern/kern.py", "--neu", "medoc", os.path.abspath("felder.json")], check=True)
print("medoc/ geschrieben:", len(maps), "Kartenstücke")
