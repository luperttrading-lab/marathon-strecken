# Erstausgabe der App für den LGT Alpin Marathon: Felder (Texte, const D, Speicher- und Cache-Präfix lgt-, Kartenliste) für den gemeinsamen
# Kern -> felder.json, dann python3 werkzeuge/kern/kern.py --neu liechtenstein werkzeuge/liechtenstein/work/felder.json (nur beim ersten Mal;
# gibt es liechtenstein/index.html schon, setzt dieses Skript die Felder dort selbst ein, über die Funktionen von kern.py).
# Muster: werkzeuge/zermatt/work/app.py.
# Reihenfolge: plan.py, osm.py, route_osm.py (mit via.json), strassen.py, bedeckt.py, dgm.py (mit swissalti.py), deck.py, clean.py,
# namen3d.py, orte.py, build.py, route.py, tiles.py, dann aus werkzeuge/: tiles_z11.py liechtenstein (Ordner ../liechtenstein/ muss es
# geben), liechtenstein/work/app.py, tiles_rand.py liechtenstein 2. Nur Abgleich: vergleich.py, kmcheck.py.
# Später allein laufen lassen geht: Gibt es liechtenstein/index.html schon, bleiben Kartenbilder und D.tiles (von tiles_rand.py) stehen.
import json, os, shutil, subprocess, sys
R = "../../../"; OUT = R + "liechtenstein/"
sys.path.insert(0, R + "werkzeuge/kern"); import kern
# Termin: 25. LGT Alpin Marathon am Samstag, 13. Juni 2026 (gelaufen; Rangliste Datasport „lgt-alpin-marathon-2026“, 13.06.2026). Nächste
# Austragung, der 26., am Samstag, 12. Juni 2027 um 9:00 Uhr (Seite „LGT Alpin Marathon“: „Herzlich willkommen zum 26. LGT Alpin Marathon im
# Fürstentum Liechtenstein am 12. Juni 2027 … Start: 9.00 Uhr, 12. Juni 2027“; Programm 2027 „Samstag, 12. Juni 2027, 9.00 Uhr in Bendern“;
# Countdown der Startseite auf 2027-06-12T09:00; Datasport „26. LGT Alpin Marathon 2027“, Startliste 12.06.2027).
# Zeitlimits laut Programm 2027 und Seite „Durchgangszeiten“ (Vaduz 10:15, Steg 13:00, Ziel 16:00); das Reglement nennt Vaduz 10:10 Uhr.
WELLEN = {"q": "Start um 9:00 Uhr bei der LGT Bank an der Schaanerstrasse in Bendern, für Marathon, LGT Halbmarathon PLUS (Ziel in Steg) und "
               "LGT Staffel 25 + 17 gemeinsam (Programm 2027). Zeitlimits laut Programm 2027: Vaduz (km 10) 10:15 Uhr, Steg (km 25) 13:00 Uhr, "
               "Zielschluss in Malbun 16:00 Uhr; das Reglement nennt für Vaduz 10:10 Uhr. Wer später durchkommt, wird aus dem Rennen genommen "
               "oder läuft mit markierter Startnummer auf eigene Verantwortung und ohne Anspruch auf weitere Leistungen weiter. Pacemaker mit "
               "Fahnen für 4:30, 5:00 und 6:00 Stunden. Stöcke sind verboten. Bergmarathon mit Gehpassagen.",
          "w": []}
D = {"wellen": WELLEN, "tz": "Europe/Vaduz", "termine": ["2026-06-13", "2027-06-12"], "start": 540}
D.update(json.load(open("data.json"))); D["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); D["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
D["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
NEU = not os.path.exists(OUT + "index.html")
if NEU:
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir("../assets"):
        if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
else:   # Kartenbilder und D.tiles so lassen, wie tiles_rand.py sie gesetzt hat
    D["tiles"] = json.loads(kern.lies_app("liechtenstein")["teile"]["D"])["tiles"]
karte = ["./" + f for f in sorted(os.listdir(OUT)) if f.startswith("karte-")]
quellen = [z.strip()[4:-5] for z in open("quellen.html", encoding="utf-8").read().strip().split("\n")]
quellen.append("<b>Straßennamen:</b> " + open("strassennamen.html", encoding="utf-8").read().strip())
F = {"praefix": "lgt", "cachepraefix": "lgt-", "cachezeile": 'const CACHE = "lgt-marathon-profil";',
     "beschreibung": "Steigungsprofil des LGT Alpin Marathons von Bendern nach Malbun: Höhe, Steigung, Pace-Modell und Karte.",
     "titel": "Steigungsprofil LGT Alpin Marathon", "eyebrow": "LGT Alpin Marathon · Kurs 2026", "h1": "Liechtenstein",
     "sub": open("sub.html", encoding="utf-8").read().strip(), "kartenquelle": "© OpenStreetMap-Mitwirkende",
     "quellen": quellen, "rohdaten": int(open("rohdaten.txt").read().strip()), "SHORT": {}, "karte": karte, "D": D}
json.dump(F, open("felder.json", "w"), ensure_ascii=False, indent=1)
if NEU:
    sys.exit(subprocess.call([sys.executable, R + "werkzeuge/kern/kern.py", "--neu", "liechtenstein", os.path.abspath("felder.json")]))
# Seite gibt es schon: Felder ersetzen (Version und Kern bleiben)
d = kern.lies_app("liechtenstein")
teile = dict(d["teile"], beschreibung=F["beschreibung"], titel=F["titel"], eyebrow=F["eyebrow"], h1=F["h1"], sub=F["sub"],
             kartenquelle=F["kartenquelle"], quellen="".join(f"      <li>{q}</li>\n" for q in quellen), rohdaten=str(F["rohdaten"]),
             D=json.dumps(D, ensure_ascii=False, separators=(",", ":")), SHORT="{}")
kern.schreibe("liechtenstein/index.html", kern.setze(d["kern"], teile))
kern.schreibe("liechtenstein/sw.js", kern.setze(d["swkern"], dict(d["swteile"], karte=json.dumps(karte, ensure_ascii=False))))
print("liechtenstein/ Felder ersetzt:", len(karte), "Kartenstücke")
