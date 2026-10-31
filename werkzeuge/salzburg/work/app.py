# Erstausgabe der App für den PUMA Salzburg Marathon: Felder (Texte, const D, Speicher- und Cache-Präfix szg, Kartenliste) für den
# gemeinsamen Kern -> felder.json, dann python3 werkzeuge/kern/kern.py --neu salzburg werkzeuge/salzburg/work/felder.json (nur beim
# ersten Mal; gibt es salzburg/index.html schon, setzt dieses Skript die Felder dort selbst ein, über die Funktionen von kern.py).
# Muster: werkzeuge/freiburg/work/app.py.
# Reihenfolge: parse.py, osm.py, strassen.py, schnur_szg.py 3 (Ideallinie, mit ideal.py), strecke.py, bev_meta.py (nur Ausgabe), dtm.py
# (mit bev.py, httpfile.py), clean.py, orte.py, build.py, route.py, tiles.py, dann aus werkzeuge/: tiles_z11.py salzburg,
# salzburg/work/app.py, tiles_rand.py salzburg 2. Später allein laufen lassen geht: Gibt es salzburg/index.html schon, bleiben
# Kartenbilder und D.tiles stehen.
import json, os, shutil, subprocess, sys
R = "../../../"; OUT = R + "salzburg/"
sys.path.insert(0, R + "werkzeuge/kern"); import kern
# Termin: 24. PUMA Salzburg Marathon am Sonntag, 23. Mai 2027, Start 8:30 Uhr auf der Staatsbrücke (Veranstalter, Seite
# „PUMA Salzburg Marathon – 42,195km“ auf salzburg-marathon.at, abgerufen 31.10.2026). Der 23. war am Sonntag, 17. Mai 2026 (Seite
# „Ergebnisse, Fotos und Video-Highlights 2026“, Pressemitteilung vom 17.05.2026). Start 2026 laut Seite „Wichtige Informationen
# PUMA Salzburg Marathon“: vier Startblöcke, drei Wellen: Grün und Orange 8:30, Rot 8:35, Blau 8:40 Uhr.
WELLEN = {"q": "Startwellen 2026 laut Veranstalter: vier Startblöcke in drei Wellen, Marathon und Halbmarathon gemeinsam auf der "
               "Staatsbrücke (Aufstellung in der Schwarzstraße); den Block wählt man bei der Anmeldung, die Farbe steht auf der Startnummer. "
               "Die Staffel startet um 8:40 Uhr aus dem letzten Block. Zielschluss nach 5:45 Stunden (2026: 14:15 Uhr); wer nach der ersten "
               "Runde ins Ziel läuft, wird im Halbmarathon gewertet. Für den 23. Mai 2027 nennt der Veranstalter den Start um 8:30 Uhr "
               "„in mehreren Wellen“, die Blöcke noch nicht.",
          "w": [["Grün und Orange", 510, "1. Welle"], ["Rot", 515, "2. Welle"], ["Blau", 520, "3. Welle · mit der Staffel"]]}
D = {"wellen": WELLEN, "tz": "Europe/Vienna", "ort": "Salzburg", "ortKurz": " Salzburg", "termine": ["2026-05-17", "2027-05-23"], "start": 510}
D.update(json.load(open("data.json"))); D["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); D["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
D["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
NEU = not os.path.exists(OUT + "index.html")
if NEU:
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir("../assets"):
        if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
else:   # Kartenbilder und D.tiles so lassen, wie tiles_rand.py sie gesetzt hat
    D["tiles"] = json.loads(kern.lies_app("salzburg")["teile"]["D"])["tiles"]
karte = ["./" + f for f in sorted(os.listdir(OUT)) if f.startswith("karte-")]
quellen = [z.strip()[4:-5] for z in open("quellen.html", encoding="utf-8").read().strip().split("\n")]
quellen.append("<b>Straßennamen:</b> " + open("strassennamen.html", encoding="utf-8").read().strip())
F = {"praefix": "szg", "cachepraefix": "szg-", "cachezeile": 'const CACHE = "szg-marathon-profil";',
     "beschreibung": "Steigungsprofil des PUMA Salzburg Marathon: Höhe, Steigung, Pace-Modell und Karte.",
     "titel": "Steigungsprofil Marathon Salzburg", "eyebrow": "PUMA Salzburg Marathon · Kurs 2026", "h1": "Salzburg",
     "sub": open("sub.html", encoding="utf-8").read().strip(), "kartenquelle": "© OpenStreetMap-Mitwirkende",
     "quellen": quellen, "rohdaten": int(open("rohdaten.txt").read().strip()), "SHORT": {}, "karte": karte, "D": D}
json.dump(F, open("felder.json", "w"), ensure_ascii=False, indent=1)
if NEU:
    sys.exit(subprocess.call([sys.executable, R + "werkzeuge/kern/kern.py", "--neu", "salzburg", os.path.abspath("felder.json")]))
# Seite gibt es schon: Felder ersetzen (Version und Kern bleiben)
d = kern.lies_app("salzburg")
teile = dict(d["teile"], beschreibung=F["beschreibung"], titel=F["titel"], eyebrow=F["eyebrow"], h1=F["h1"], sub=F["sub"],
             kartenquelle=F["kartenquelle"], quellen="".join(f"      <li>{q}</li>\n" for q in quellen), rohdaten=str(F["rohdaten"]),
             D=json.dumps(D, ensure_ascii=False, separators=(",", ":")), SHORT="{}")
kern.schreibe("salzburg/index.html", kern.setze(d["kern"], teile))
kern.schreibe("salzburg/sw.js", kern.setze(d["swkern"], dict(d["swteile"], karte=json.dumps(karte, ensure_ascii=False))))
print("salzburg/ Felder ersetzt:", len(karte), "Kartenstücke")
