# Erstausgabe der App für den Brocken-Marathon (Harz-Gebirgslauf): Felder (Texte, const D, Speicher- und Cache-Präfix brk, Kartenliste) für den
# gemeinsamen Kern -> felder.json, dann python3 werkzeuge/kern/kern.py --neu brocken werkzeuge/brocken/work/felder.json (nur beim ersten Mal;
# gibt es brocken/index.html schon, setzt dieses Skript die Felder dort selbst ein, über die Funktionen von kern.py).
# Muster: werkzeuge/freiburg/work/app.py.
# Reihenfolge: parse.py, osm.py, match.py, georef.py (nur Abgleich), strassen.py, vorladen.py (mit lvermgeo.py), dgm.py, clean.py, orte.py,
# stationen.py, build.py, auswertung.py (nur Ausgabe), route.py, tiles.py, dann aus werkzeuge/: tiles_z11.py brocken, brocken/work/app.py,
# tiles_rand.py brocken 2. Später allein laufen lassen geht: Gibt es brocken/index.html schon, bleiben Kartenbilder und D.tiles stehen.
import json, os, shutil, subprocess, sys
R = "../../../"; OUT = R + "brocken/"
sys.path.insert(0, R + "werkzeuge/kern"); import kern
# Termin: 48. Harz-Gebirgslauf am Samstag, 10. Oktober 2026 (Veranstalter, harz-gebirgslauf.de: „Alle Infos zum 48. Harz-Gebirgslauf am
# 10.10.2026“, Zeitplan „Samstag, 10. Oktober 2026 … 09:00 Uhr Brocken-Marathon“). 2027 ist noch nicht veröffentlicht; der Verein betreut
# die Verpflegung „jährlich am zweiten Samstag im Oktober“ (Seite „Verein“, „Seit 1978 … am zweiten Wochenende im Oktober“), das wäre der
# 9. Oktober 2027: mit „?“ (unbestätigt). 2025 war es der 11. Oktober (zweiter Samstag).
WELLEN = {"q": "Ein gemeinsamer Start um 9:00 Uhr an der Himmelpforte in Wernigerode-Hasserode (Zeitplan 2026; der Termin 2027 ist noch nicht "
               "veröffentlicht, gelaufen wird am zweiten Samstag im Oktober). Zeitlimits laut Veranstalter: Wer den Brocken nicht bis 12:00 Uhr "
               "passiert hat, also binnen 3 Stunden (Gipfel hier bei km 19,2), wird aus der Wertung genommen; Zielschluss für alle Strecken "
               "15:00 Uhr, 6 Stunden nach dem Start. Die Verpflegungsstellen sind nur zu festen Zeiten besetzt (bei den Marken). Höchstens 1000 "
               "Teilnehmer (Nationalpark Harz). Der Halb-Marathon (22,5 km) startet um 10:15 Uhr auf derselben Strecke, biegt im Ilsetal (km 9,3) "
               "zur Plessenburg ab und kommt an der Mönchsbuche (km 36,5) wieder dazu.",
          "w": []}
D = {"wellen": WELLEN, "tz": "Europe/Berlin", "termine": ["2026-10-10", "2027-10-09?"], "start": 540}
D.update(json.load(open("data.json"))); D["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); D["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
D["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
NEU = not os.path.exists(OUT + "index.html")
if NEU:
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir("../assets"):
        if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
else:   # Kartenbilder und D.tiles so lassen, wie tiles_rand.py sie gesetzt hat
    D["tiles"] = json.loads(kern.lies_app("brocken")["teile"]["D"])["tiles"]
karte = ["./" + f for f in sorted(os.listdir(OUT)) if f.startswith("karte-")]
quellen = [z.strip()[4:-5] for z in open("quellen.html", encoding="utf-8").read().strip().split("\n")]
quellen.append("<b>Wegenamen:</b> " + open("strassennamen.html", encoding="utf-8").read().strip())
F = {"praefix": "brk", "cachepraefix": "brk-", "cachezeile": 'const CACHE = "brk-marathon-profil";',
     "beschreibung": "Steigungsprofil des Brocken-Marathons beim Harz-Gebirgslauf: Höhe, Steigung, Pace-Modell und Karte.",
     "titel": "Steigungsprofil Brocken-Marathon", "eyebrow": "Harz-Gebirgslauf · Brocken-Marathon · Kurs 2026", "h1": "Brocken",
     "sub": open("sub.html", encoding="utf-8").read().strip(), "kartenquelle": "© OpenStreetMap-Mitwirkende",
     "quellen": quellen, "rohdaten": int(open("rohdaten.txt").read().strip()), "SHORT": {}, "karte": karte, "D": D}
json.dump(F, open("felder.json", "w"), ensure_ascii=False, indent=1)
if NEU:
    sys.exit(subprocess.call([sys.executable, R + "werkzeuge/kern/kern.py", "--neu", "brocken", os.path.abspath("felder.json")]))
# Seite gibt es schon: Felder ersetzen (Version und Kern bleiben)
d = kern.lies_app("brocken")
teile = dict(d["teile"], beschreibung=F["beschreibung"], titel=F["titel"], eyebrow=F["eyebrow"], h1=F["h1"], sub=F["sub"],
             kartenquelle=F["kartenquelle"], quellen="".join(f"      <li>{q}</li>\n" for q in quellen), rohdaten=str(F["rohdaten"]),
             D=json.dumps(D, ensure_ascii=False, separators=(",", ":")), SHORT="{}")
kern.schreibe("brocken/index.html", kern.setze(d["kern"], teile))
kern.schreibe("brocken/sw.js", kern.setze(d["swkern"], dict(d["swteile"], karte=json.dumps(karte, ensure_ascii=False))))
print("brocken/ Felder ersetzt:", len(karte), "Kartenstücke")
