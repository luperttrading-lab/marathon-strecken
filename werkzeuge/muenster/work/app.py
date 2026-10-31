# Erstausgabe der App für den Volksbank-Münster-Marathon: Felder (Texte, const D, Speicher- und Cache-Präfix mst, Kartenliste) für den
# gemeinsamen Kern -> felder.json, dann python3 werkzeuge/kern/kern.py --neu muenster werkzeuge/muenster/work/felder.json (nur beim ersten
# Mal; gibt es muenster/index.html schon, setzt dieses Skript die Felder dort selbst ein, über die Funktionen von kern.py). Muster:
# werkzeuge/duesseldorf/work/app.py.
# Reihenfolge: parse.py, grob.py, osm.py, georef.py, strecke.py, eichung.py, strassen.py, dgm.py, dom.py, clean.py, orte.py, build.py,
# route.py, tiles.py, dann aus werkzeuge/: tiles_z11.py muenster, muenster/work/app.py, tiles_rand.py muenster 2. Nur Abgleich: marken.py.
# Später allein laufen lassen geht: Gibt es muenster/index.html schon, bleiben Kartenbilder und D.tiles (von tiles_rand.py) stehen.
import json, os, shutil, subprocess, sys
R = "../../../"; OUT = R + "muenster/"
sys.path.insert(0, R + "werkzeuge/kern"); import kern
# Termin: 25. Volksbank-Münster-Marathon am Sonntag, 12. September 2027 (Startseite des Veranstalters: Countdown „12.09.2027“ bis
# „2027-09-12T09:00:00“, Anmeldestart 2. November 2026 „zu unserem Jubiläumslauf, dem 25. Volksbank-Münster-Marathon“; Marathonguide 2026:
# „12.09.2027 SAVE THE DATE“). Der 24. war am Sonntag, 13. September 2026 (Ergebnisse bei RaceTime, Marathonguide 2026).
# Start: „9.00 Uhr Volksbank-Münster-Marathon (Schlossplatz)“, „9.15 Uhr Atruvia Staffelmarathon“, „10.10 Uhr Wecker-28“ (FAQ zum
# Volksbank-Münster-Marathon, Stand 23.10.2026, schon für 2027; ebenso Marathonguide 2026). Startblöcke nach Bestzeit (FAQ
# „Startaufstellung“: Gruppe 1 bis 3:00 h, 2 bis 3:30 h, 3 bis 4:00 h, 4 ab 4:00 h und Erststarter), keine Wellen. Zielschluss nach
# 6 Stunden bzw. 15:00 Uhr (FAQ „Zielschluss“, Marathonguide „Zielschluss: 15 Uhr“); „Teilnehmer:innen, die über den jeweiligen Sollzeiten
# liegen, werden aus dem Rennen genommen“, am Ende des Feldes ein Bus (Besenwagen).
WELLEN = {"q": "Ein Start um 9:00 Uhr am Schlossplatz (2026 und laut FAQ des Veranstalters auch 2027), aufgestellt in vier Blöcken nach "
               "Bestzeit: bis 3:00, bis 3:30, bis 4:00 Stunden, dahinter alle anderen und Erststarter. Der Atruvia Staffelmarathon startet "
               "um 9:15 Uhr aus dem letzten Block, der Wecker-28 um 10:10 Uhr am Kardinal-von-Galen-Ring. Zielschluss 6 Stunden nach dem "
               "Start, 15:00 Uhr; wer über den Sollzeiten liegt, wird aus dem Rennen genommen, am Ende des Feldes fährt ein Bus.",
          "w": []}
D = {"wellen": WELLEN, "tz": "Europe/Berlin", "termine": ["2026-09-13", "2027-09-12"], "start": 540}
D.update(json.load(open("data.json"))); D["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); D["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
D["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
NEU = not os.path.exists(OUT + "index.html")
if NEU:
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir("../assets"):
        if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
else:   # Kartenbilder und D.tiles so lassen, wie tiles_rand.py sie gesetzt hat
    D["tiles"] = json.loads(kern.lies_app("muenster")["teile"]["D"])["tiles"]
karte = ["./" + f for f in sorted(os.listdir(OUT)) if f.startswith("karte-")]
quellen = [z.strip()[4:-5] for z in open("quellen.html", encoding="utf-8").read().strip().split("\n")]
quellen.append("<b>Straßennamen:</b> " + open("strassennamen.html", encoding="utf-8").read().strip())
F = {"praefix": "mst", "cachepraefix": "mst-", "cachezeile": 'const CACHE = "mst-marathon-profil";',
     "beschreibung": "Steigungsprofil des Münster-Marathons: Höhe, Steigung, Pace-Modell und Karte.",
     "titel": "Steigungsprofil Münster Marathon", "eyebrow": "Volksbank-Münster-Marathon · Kurs 2026", "h1": "Münster",
     "sub": open("sub.html", encoding="utf-8").read().strip(), "kartenquelle": "© OpenStreetMap-Mitwirkende",
     "quellen": quellen, "rohdaten": int(open("rohdaten.txt").read().strip()), "SHORT": {}, "karte": karte, "D": D}
json.dump(F, open("felder.json", "w"), ensure_ascii=False, indent=1)
if NEU:
    sys.exit(subprocess.call([sys.executable, R + "werkzeuge/kern/kern.py", "--neu", "muenster", os.path.abspath("felder.json")]))
# Seite gibt es schon: Felder ersetzen (Version und Kern bleiben)
d = kern.lies_app("muenster")
teile = dict(d["teile"], beschreibung=F["beschreibung"], titel=F["titel"], eyebrow=F["eyebrow"], h1=F["h1"], sub=F["sub"],
             kartenquelle=F["kartenquelle"], quellen="".join(f"      <li>{q}</li>\n" for q in quellen), rohdaten=str(F["rohdaten"]),
             D=json.dumps(D, ensure_ascii=False, separators=(",", ":")), SHORT="{}")
kern.schreibe("muenster/index.html", kern.setze(d["kern"], teile))
kern.schreibe("muenster/sw.js", kern.setze(d["swkern"], dict(d["swteile"], karte=json.dumps(karte, ensure_ascii=False))))
print("muenster/ Felder ersetzt:", len(karte), "Kartenstücke")
