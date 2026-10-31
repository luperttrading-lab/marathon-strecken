# Erstausgabe der App für den Kleine Zeitung Graz Marathon: Felder (Texte, const D, Speicher- und Cache-Präfix grz, Kartenliste) für den
# gemeinsamen Kern -> felder.json, dann python3 werkzeuge/kern/kern.py --neu graz werkzeuge/graz/work/felder.json (nur beim ersten Mal;
# gibt es graz/index.html schon, setzt dieses Skript die Felder dort selbst ein, über die Funktionen von kern.py). Kopie von
# werkzeuge/freiburg/work/app.py.
# Reihenfolge: parse.py, osm.py, ideal_w.py 0.5 1 1.5 2 (Ideallinie, mit ideal.py), strecke.py, strassen.py, dgm.py (mit bev.py), deck.py,
# clean.py, orte.py, stationen.py (mit nominatim.py), build.py, route.py, tiles.py, dann aus werkzeuge/: tiles_z11.py graz,
# graz/work/app.py, tiles_rand.py graz 2. Später allein laufen lassen geht: Gibt es graz/index.html schon, bleiben Kartenbilder und
# D.tiles stehen.
import json, os, shutil, subprocess, sys
R = "../../../"; OUT = R + "graz/"
sys.path.insert(0, R + "werkzeuge/kern"); import kern
# Termin: Kleine Zeitung Graz Marathon am Sonntag, 10. Oktober 2027 (Seite „Marathon“: „Datum: Sonntag, 10. Oktober 2027 Startzeit:
# 10.00 Uhr (Änderungen vorbehalten) Zielschluss: 16.00 Uhr“; Startseite „08.-10. OKTOBER 2027“). Der 33. Graz Marathon war am
# 9.–11. Oktober 2026, der Marathon am Sonntag, 11. Oktober 2026 (Straßensperren 2026, News „Graz Marathon Tag 2“ vom 11.10.2026).
# Startblöcke laut Seite „Startblöcke Aufstellung“ (gleich auf den Seiten „Marathon“ und „Staffelmarathon“ für 2027).
WELLEN = {"q": "Startzeiten laut Veranstalter (2026 und für den 10. Oktober 2027): Start vor der Oper in Blöcken, Marathon und Hyundai "
               "Staffelmarathon mit der Elite in Startblock 1 um 10:00 Uhr oder in Startblock 2 um 10:05 Uhr, jeweils gemeinsam mit dem "
               "Hervis Halbmarathon (dessen Blöcke 3 und 4 folgen um 10:10 und 10:15 Uhr); der Block steht auf der Startnummer. Der "
               "Viertelmarathon startet schon um 9:30 Uhr. Zielschluss 16:00 Uhr (Halbmarathon 14:00 Uhr).",
          "w": [["Block 1", 600, "mit Elite"], ["Block 2", 605, "Marathon, Staffel, Halbmarathon"]]}
D = {"wellen": WELLEN, "tz": "Europe/Vienna", "ort": "Graz", "ortKurz": " Graz", "termine": ["2026-10-11", "2027-10-10"], "start": 600}
D.update(json.load(open("data.json"))); D["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); D["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
D["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
NEU = not os.path.exists(OUT + "index.html")
if NEU:
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir("../assets"):
        if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
else:   # Kartenbilder und D.tiles so lassen, wie tiles_rand.py sie gesetzt hat
    D["tiles"] = json.loads(kern.lies_app("graz")["teile"]["D"])["tiles"]
karte = ["./" + f for f in sorted(os.listdir(OUT)) if f.startswith("karte-")]
quellen = [z.strip()[4:-5] for z in open("quellen.html", encoding="utf-8").read().strip().split("\n")]
quellen.append("<b>Straßennamen:</b> " + open("strassennamen.html", encoding="utf-8").read().strip())
F = {"praefix": "grz", "cachepraefix": "grz-", "cachezeile": 'const CACHE = "grz-marathon-profil";',
     "beschreibung": "Steigungsprofil des Kleine Zeitung Graz Marathons: Höhe, Steigung, Pace-Modell und Karte.",
     "titel": "Steigungsprofil Graz Marathon", "eyebrow": "Kleine Zeitung Graz Marathon · Kurs 2026", "h1": "Graz",
     "sub": open("sub.html", encoding="utf-8").read().strip(), "kartenquelle": "© OpenStreetMap-Mitwirkende",
     "quellen": quellen, "rohdaten": int(open("rohdaten.txt").read().strip()), "SHORT": {}, "karte": karte, "D": D}
json.dump(F, open("felder.json", "w"), ensure_ascii=False, indent=1)
if NEU:
    sys.exit(subprocess.call([sys.executable, R + "werkzeuge/kern/kern.py", "--neu", "graz", os.path.abspath("felder.json")]))
# Seite gibt es schon: Felder ersetzen (Version und Kern bleiben)
d = kern.lies_app("graz")
teile = dict(d["teile"], beschreibung=F["beschreibung"], titel=F["titel"], eyebrow=F["eyebrow"], h1=F["h1"], sub=F["sub"],
             kartenquelle=F["kartenquelle"], quellen="".join(f"      <li>{q}</li>\n" for q in quellen), rohdaten=str(F["rohdaten"]),
             D=json.dumps(D, ensure_ascii=False, separators=(",", ":")), SHORT="{}")
kern.schreibe("graz/index.html", kern.setze(d["kern"], teile))
kern.schreibe("graz/sw.js", kern.setze(d["swkern"], dict(d["swteile"], karte=json.dumps(karte, ensure_ascii=False))))
print("graz/ Felder ersetzt:", len(karte), "Kartenstücke")
