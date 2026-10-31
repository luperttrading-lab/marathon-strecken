# Erstausgabe der App für den Uniper Düsseldorf Marathon: Felder (Texte, const D, Speicher- und Cache-Präfix dus-, Kartenliste) für den
# gemeinsamen Kern -> felder.json, dann python3 werkzeuge/kern/kern.py --neu duesseldorf werkzeuge/duesseldorf/work/felder.json (nur
# beim ersten Mal; gibt es duesseldorf/index.html schon, setzt dieses Skript die Felder dort selbst ein, über die Funktionen von
# kern.py). Muster: werkzeuge/honolulu/work/app.py.
# Reihenfolge: parse.py, osm.py, georef.py, strecke.py, dgm.py, strassen.py, dom.py, clean.py, orte.py, stationen.py, build.py, route.py,
# tiles.py, dann aus werkzeuge/: tiles_z11.py duesseldorf, duesseldorf/work/app.py, tiles_rand.py duesseldorf 2. Nur Abgleich: marken.py.
# Später allein laufen lassen geht: Gibt es duesseldorf/index.html schon, bleiben Kartenbilder und D.tiles (von tiles_rand.py) stehen.
import json, os, shutil, subprocess, sys
R = "../../../"; OUT = R + "duesseldorf/"
sys.path.insert(0, R + "werkzeuge/kern"); import kern
# Termin: Uniper Düsseldorf Marathon am Sonntag, 18. April 2027, Start Marathon 9:45 Uhr (Veranstalter, Seite „Wettbewerbe Marathon“:
# „Datum: Sonntag, 18. April 2027 · Startzeit: 9:45 Uhr“, Startzeiten: Halbmarathon 8:00/8:20/8:40, Marathon 9:45, Staffel 10:15;
# „Zielschluss für den Marathon ist 15:45 Uhr … Für die Marathon-Staffel schließt das Ziel um 16:15 Uhr“). Der letzte war am
# Sonntag, 26. April 2026 (Marathon ebenfalls 9:45, Zielschluss 15:45, Staffel 16:00 laut Vorbericht von D.SPORTS vom 24.04.2026).
# Startblöcke für den Marathon nennt der Veranstalter nicht (ein Start); die Halbmarathon-Wellen laufen auf eigener Strecke.
WELLEN = {"q": "Ein Start um 9:45 Uhr am Joseph-Beuys-Ufer (2026 und 2027 laut Veranstalter; Startblöcke nennt er nicht). Die "
               "Marathon-Staffel startet um 10:15 Uhr, der Halbmarathon ab 8:00 Uhr in drei Wellen auf eigener Strecke. Zielschluss "
               "15:45 Uhr, also 6 Stunden nach dem Start; hinter dem Feld fährt ein Besenwagen. Staffel: Ziel bis 16:15 Uhr (2027).",
          "w": []}
D = {"wellen": WELLEN, "tz": "Europe/Berlin", "termine": ["2026-04-26", "2027-04-18"], "start": 585}
D.update(json.load(open("data.json"))); D["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); D["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
D["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
NEU = not os.path.exists(OUT + "index.html")
if NEU:
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir("../assets"):
        if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
else:   # Kartenbilder und D.tiles so lassen, wie tiles_rand.py sie gesetzt hat
    D["tiles"] = json.loads(kern.lies_app("duesseldorf")["teile"]["D"])["tiles"]
karte = ["./" + f for f in sorted(os.listdir(OUT)) if f.startswith("karte-")]
quellen = [z.strip()[4:-5] for z in open("quellen.html", encoding="utf-8").read().strip().split("\n")]
quellen.append("<b>Straßennamen:</b> " + open("strassennamen.html", encoding="utf-8").read().strip())
F = {"praefix": "dus", "cachepraefix": "dus-", "cachezeile": 'const CACHE = "dus-marathon-profil";',
     "beschreibung": "Steigungsprofil des Düsseldorf Marathons: Höhe, Steigung, Pace-Modell und Karte.",
     "titel": "Steigungsprofil Düsseldorf Marathon", "eyebrow": "Uniper Düsseldorf Marathon · Kurs 2026", "h1": "Düsseldorf",
     "sub": open("sub.html", encoding="utf-8").read().strip(), "kartenquelle": "© OpenStreetMap-Mitwirkende",
     "quellen": quellen, "rohdaten": int(open("rohdaten.txt").read().strip()), "SHORT": {}, "karte": karte, "D": D}
json.dump(F, open("felder.json", "w"), ensure_ascii=False, indent=1)
if NEU:
    sys.exit(subprocess.call([sys.executable, R + "werkzeuge/kern/kern.py", "--neu", "duesseldorf", os.path.abspath("felder.json")]))
# Seite gibt es schon: Felder ersetzen (Version und Kern bleiben)
d = kern.lies_app("duesseldorf")
teile = dict(d["teile"], beschreibung=F["beschreibung"], titel=F["titel"], eyebrow=F["eyebrow"], h1=F["h1"], sub=F["sub"],
             kartenquelle=F["kartenquelle"], quellen="".join(f"      <li>{q}</li>\n" for q in quellen), rohdaten=str(F["rohdaten"]),
             D=json.dumps(D, ensure_ascii=False, separators=(",", ":")), SHORT="{}")
kern.schreibe("duesseldorf/index.html", kern.setze(d["kern"], teile))
kern.schreibe("duesseldorf/sw.js", kern.setze(d["swkern"], dict(d["swteile"], karte=json.dumps(karte, ensure_ascii=False))))
print("duesseldorf/ Felder ersetzt:", len(karte), "Kartenstücke")
