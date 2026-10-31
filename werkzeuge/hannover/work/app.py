# Erstausgabe der App für den ADAC Marathon Hannover: Felder (Texte, const D, Speicher- und Cache-Präfix han-, Kartenliste) für den
# gemeinsamen Kern -> felder.json, dann python3 werkzeuge/kern/kern.py --neu hannover werkzeuge/hannover/work/felder.json (nur
# beim ersten Mal; gibt es hannover/index.html schon, setzt dieses Skript die Felder dort selbst ein, über die Funktionen von
# kern.py). Muster: werkzeuge/honolulu/work/app.py.
# Reihenfolge: parse.py, marken.py (nur Abgleich), osm.py, strassen.py, dgm.py (mit lgln.py), deck.py, clean.py, orte.py, stationen.py,
# build.py, auswertung.py (nur Ausgabe), route.py, tiles.py, dann aus werkzeuge/: tiles_z11.py hannover, hannover/work/app.py,
# tiles_rand.py hannover 2. Später allein laufen lassen geht: Gibt es hannover/index.html schon, bleiben Kartenbilder und D.tiles stehen.
import json, os, shutil, subprocess, sys
R = "../../../"; OUT = R + "hannover/"
sys.path.insert(0, R + "werkzeuge/kern"); import kern
# Termin: 35. ADAC Marathon Hannover am Sonntag, 11. April 2027 (Veranstalter, Startseite marathon-hannover.de: „Race Countdown
# 11.04.2027“, „Neuauflage am 11. April 2027“; Seite „Allgemeine Infos“: „Startzeiten am 11. April 2027“). Der 34. war am Sonntag,
# 12. April 2026. Start 10:00 Uhr in zwei Wellen, Zielschluss 16:00 Uhr (Seite „Marathon“, Stand Oktober 2026: „10:00 Uhr (DM, Elite
# und die Blöcke B + C) … Der Block D startet um 10:05 Uhr“; Seite „Streckenservice“: Sollzeit 6:00 h, danach Besenwagen).
WELLEN = {"q": "Startzeiten 2027 laut Veranstalter (Stand Oktober 2026): 10:00 Uhr Elite, Deutsche Meisterschaft und die Blöcke B und C, "
               "10:05 Uhr Block D. Die Staffel startet ab 10:30 Uhr, Handbikes um 9:45 Uhr. Zielschluss 16:00 Uhr; wer die Sollzeit von "
               "6 Stunden überschreitet, wird vom Besenwagen aufgenommen.",
          "w": [["Welle 1", 600, "Elite, Blöcke B und C"], ["Welle 2", 605, "Block D"]]}
D = {"wellen": WELLEN, "tz": "Europe/Berlin", "termine": ["2026-04-12", "2027-04-11"], "start": 600}
D.update(json.load(open("data.json"))); D["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); D["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
D["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
NEU = not os.path.exists(OUT + "index.html")
if NEU:
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir("../assets"):
        if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
else:   # Kartenbilder und D.tiles so lassen, wie tiles_rand.py sie gesetzt hat
    D["tiles"] = json.loads(kern.lies_app("hannover")["teile"]["D"])["tiles"]
karte = ["./" + f for f in sorted(os.listdir(OUT)) if f.startswith("karte-")]
quellen = [z.strip()[4:-5] for z in open("quellen.html", encoding="utf-8").read().strip().split("\n")]
quellen.append("<b>Straßennamen:</b> " + open("strassennamen.html", encoding="utf-8").read().strip())
F = {"praefix": "han", "cachepraefix": "han-", "cachezeile": 'const CACHE = "han-marathon-profil";',
     "beschreibung": "Steigungsprofil des ADAC Marathon Hannover: Höhe, Steigung, Pace-Modell und Karte.",
     "titel": "Steigungsprofil Marathon Hannover", "eyebrow": "ADAC Marathon Hannover · Kurs 2026", "h1": "Hannover",
     "sub": open("sub.html", encoding="utf-8").read().strip(), "kartenquelle": "© OpenStreetMap-Mitwirkende",
     "quellen": quellen, "rohdaten": int(open("rohdaten.txt").read().strip()), "SHORT": {}, "karte": karte, "D": D}
json.dump(F, open("felder.json", "w"), ensure_ascii=False, indent=1)
if NEU:
    sys.exit(subprocess.call([sys.executable, R + "werkzeuge/kern/kern.py", "--neu", "hannover", os.path.abspath("felder.json")]))
# Seite gibt es schon: Felder ersetzen (Version und Kern bleiben)
d = kern.lies_app("hannover")
teile = dict(d["teile"], beschreibung=F["beschreibung"], titel=F["titel"], eyebrow=F["eyebrow"], h1=F["h1"], sub=F["sub"],
             kartenquelle=F["kartenquelle"], quellen="".join(f"      <li>{q}</li>\n" for q in quellen), rohdaten=str(F["rohdaten"]),
             D=json.dumps(D, ensure_ascii=False, separators=(",", ":")), SHORT="{}")
kern.schreibe("hannover/index.html", kern.setze(d["kern"], teile))
kern.schreibe("hannover/sw.js", kern.setze(d["swkern"], dict(d["swteile"], karte=json.dumps(karte, ensure_ascii=False))))
print("hannover/ Felder ersetzt:", len(karte), "Kartenstücke")
