# Erstausgabe der App für den Mein Freiburg Marathon: Felder (Texte, const D, Speicher- und Cache-Präfix fbg, Kartenliste) für den
# gemeinsamen Kern -> felder.json, dann python3 werkzeuge/kern/kern.py --neu freiburg werkzeuge/freiburg/work/felder.json (nur beim
# ersten Mal; gibt es freiburg/index.html schon, setzt dieses Skript die Felder dort selbst ein, über die Funktionen von kern.py).
# Muster: werkzeuge/hannover/work/app.py.
# Reihenfolge: parse.py, osm.py, georef.py (nur Abgleich), ideal_w.py 2 (Ideallinie), strecke.py, strassen.py, dgm.py (mit lgl.py),
# deck.py, clean.py, orte.py, stationen.py, build.py, auswertung.py (nur Ausgabe), route.py, tiles.py, dann aus werkzeuge/:
# tiles_z11.py freiburg, freiburg/work/app.py, tiles_rand.py freiburg 2. Später allein laufen lassen geht: Gibt es freiburg/index.html
# schon, bleiben Kartenbilder und D.tiles stehen.
import json, os, shutil, subprocess, sys
R = "../../../"; OUT = R + "freiburg/"
sys.path.insert(0, R + "werkzeuge/kern"); import kern
# Termin: 22. Mein Freiburg Marathon am Sonntag, 4. April 2027 (Veranstalter, Startseite mein-freiburgmarathon.de: „Save the Date
# 4. April 2027“; Seite „Marathon“: „4. April 2027 · Start 9:00 Uhr, 9:10 Uhr · Cut-off-Zeit 5:45 h“). Der 21. war am Sonntag,
# 12. April 2026 (Starterinformation 2026, Pressemitteilung der FWTM vom 12.04.2026). Start 2026 laut Starterinformation: „Marathon
# 09:00 Uhr / 09:10 Uhr … Aufteilung in zwei Startblöcke mit einem Abstand von 10 Minuten“.
WELLEN = {"q": "Startzeiten laut Veranstalter (2026 und für den 4. April 2027): zwei Startblöcke mit 10 Minuten Abstand auf dem Freigelände "
               "der Messe, eingeteilt nach der bei der Anmeldung angegebenen Zielzeit. Zeitlimit 5:45 Stunden. Wer die erste Runde nicht "
               "innerhalb von 2:45 Stunden beendet (bis etwa 12:00 Uhr), wird ins Ziel umgeleitet und darf nicht in die zweite Runde. "
               "Der Halbmarathon startet um 10:30 Uhr in vier Blöcken, der badenova Schülermarathon um 11:00 und 11:15 Uhr; beide laufen "
               "die Runde, wenn die Marathonläufer in der zweiten sind.",
          "w": [["1. Block", 540, "nach Zielzeit"], ["2. Block", 550, "nach Zielzeit"]]}
D = {"wellen": WELLEN, "tz": "Europe/Berlin", "termine": ["2026-04-12", "2027-04-04"], "start": 540}
D.update(json.load(open("data.json"))); D["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); D["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
D["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
NEU = not os.path.exists(OUT + "index.html")
if NEU:
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir("../assets"):
        if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
else:   # Kartenbilder und D.tiles so lassen, wie tiles_rand.py sie gesetzt hat
    D["tiles"] = json.loads(kern.lies_app("freiburg")["teile"]["D"])["tiles"]
karte = ["./" + f for f in sorted(os.listdir(OUT)) if f.startswith("karte-")]
quellen = [z.strip()[4:-5] for z in open("quellen.html", encoding="utf-8").read().strip().split("\n")]
quellen.append("<b>Straßennamen:</b> " + open("strassennamen.html", encoding="utf-8").read().strip())
F = {"praefix": "fbg", "cachepraefix": "fbg-", "cachezeile": 'const CACHE = "fbg-marathon-profil";',
     "beschreibung": "Steigungsprofil des Mein Freiburg Marathon: Höhe, Steigung, Pace-Modell und Karte.",
     "titel": "Steigungsprofil Marathon Freiburg", "eyebrow": "Mein Freiburg Marathon · Kurs 2026", "h1": "Freiburg",
     "sub": open("sub.html", encoding="utf-8").read().strip(), "kartenquelle": "© OpenStreetMap-Mitwirkende",
     "quellen": quellen, "rohdaten": int(open("rohdaten.txt").read().strip()), "SHORT": {}, "karte": karte, "D": D}
json.dump(F, open("felder.json", "w"), ensure_ascii=False, indent=1)
if NEU:
    sys.exit(subprocess.call([sys.executable, R + "werkzeuge/kern/kern.py", "--neu", "freiburg", os.path.abspath("felder.json")]))
# Seite gibt es schon: Felder ersetzen (Version und Kern bleiben)
d = kern.lies_app("freiburg")
teile = dict(d["teile"], beschreibung=F["beschreibung"], titel=F["titel"], eyebrow=F["eyebrow"], h1=F["h1"], sub=F["sub"],
             kartenquelle=F["kartenquelle"], quellen="".join(f"      <li>{q}</li>\n" for q in quellen), rohdaten=str(F["rohdaten"]),
             D=json.dumps(D, ensure_ascii=False, separators=(",", ":")), SHORT="{}")
kern.schreibe("freiburg/index.html", kern.setze(d["kern"], teile))
kern.schreibe("freiburg/sw.js", kern.setze(d["swkern"], dict(d["swteile"], karte=json.dumps(karte, ensure_ascii=False))))
print("freiburg/ Felder ersetzt:", len(karte), "Kartenstücke")
