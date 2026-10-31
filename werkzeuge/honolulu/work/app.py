# Erstausgabe der App für den JAL Honolulu Marathon: Felder (Texte, const D, Speicher- und Cache-Präfix hnl-, Kartenliste) für den
# gemeinsamen Kern -> felder.json, dann python3 werkzeuge/kern/kern.py --neu honolulu werkzeuge/honolulu/work/felder.json (nur
# beim ersten Mal; gibt es honolulu/index.html schon, setzt dieses Skript die Felder dort selbst ein, über die Funktionen von
# kern.py). Muster: werkzeuge/stockholm/work/app.py.
# Reihenfolge: parse.py, osm.py, strassen.py, dgm.py, deck.py, clean.py, orte.py, stationen.py, build.py, route.py, tiles.py, dann aus
# werkzeuge/: tiles_z11.py honolulu, honolulu/work/app.py, tiles_rand.py honolulu 2. Nur Abgleich: vergleich.py, planprofil.py, marken.py.
# Später allein laufen lassen geht: Gibt es honolulu/index.html schon, bleiben Kartenbilder und D.tiles (von tiles_rand.py) stehen.
import json, os, shutil, subprocess, sys
R = "../../../"; OUT = R + "honolulu/"
sys.path.insert(0, R + "werkzeuge/kern"); import kern
# Termin: 54. JAL Honolulu Marathon am Sonntag, 13. Dezember 2026, Start 5:00 Uhr (Veranstalter, Seite „JAL Honolulu Marathon“ und
# FAQ); 2027 am Sonntag, 12. Dezember („December 11 & 12, 2027“, immer der zweite Sonntag im Dezember). Der 53. war am 14.12.2025.
# Ein gemeinsamer Start, Startgruppen nach erwarteter Zielzeit (Seite „Getting to the Start“). Kein Zeitlimit (FAQ, „Finish Area“).
# Startlinie an der Piʻikoi Street, Startgruppen dahinter nach Osten bis Atkinson Drive (Startlinien-Karte 2026 R6 vom 13.08.2026).
WELLEN = {"q": "Ein gemeinsamer Start um 5:00 Uhr mit Feuerwerk auf dem Ala Moana Boulevard an der Piʻikoi Street (Veranstalter, 2026). "
               "Die Startgruppe nach erwarteter Zielzeit steht als Farbe auf der Startnummer: Weiß Elite, Grün unter 4 h, Blau 4–5 h, "
               "Orange 5–6 h, Lila ab 6 h. Die Startlinie schließt um 5:30. Kein Zeitlimit: Das Ziel bleibt offen, bis die letzte Person "
               "angekommen ist; man muss nur in Bewegung bleiben.", "w": []}
D = {"wellen": WELLEN, "tz": "Pacific/Honolulu", "termine": ["2025-12-14", "2026-12-13", "2027-12-12"], "start": 300}
D.update(json.load(open("data.json"))); D["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); D["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
D["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
NEU = not os.path.exists(OUT + "index.html")
if NEU:
    for f in os.listdir("../assets"):
        if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
else:   # Kartenbilder und D.tiles so lassen, wie tiles_rand.py sie gesetzt hat
    D["tiles"] = json.loads(kern.lies_app("honolulu")["teile"]["D"])["tiles"]
karte = ["./" + f for f in sorted(os.listdir(OUT)) if f.startswith("karte-")]
quellen = [z.strip()[4:-5] for z in open("quellen.html", encoding="utf-8").read().strip().split("\n")]
quellen.append("<b>Straßennamen:</b> " + open("strassennamen.html", encoding="utf-8").read().strip())
F = {"praefix": "hnl", "cachepraefix": "hnl-", "cachezeile": 'const CACHE = "hnl-marathon-profil";',
     "beschreibung": "Steigungsprofil des Honolulu Marathons: Höhe, Steigung, Pace-Modell und Karte.",
     "titel": "Steigungsprofil Honolulu Marathon", "eyebrow": "JAL Honolulu Marathon · Kurs 2026", "h1": "Honolulu",
     "sub": open("sub.html", encoding="utf-8").read().strip(), "kartenquelle": "© OpenStreetMap-Mitwirkende",
     "quellen": quellen, "rohdaten": int(open("rohdaten.txt").read().strip()), "SHORT": {}, "karte": karte, "D": D}
json.dump(F, open("felder.json", "w"), ensure_ascii=False, indent=1)
if NEU:
    sys.exit(subprocess.call([sys.executable, R + "werkzeuge/kern/kern.py", "--neu", "honolulu", os.path.abspath("felder.json")]))
# Seite gibt es schon: Felder ersetzen (Version und Kern bleiben)
d = kern.lies_app("honolulu")
teile = dict(d["teile"], beschreibung=F["beschreibung"], titel=F["titel"], eyebrow=F["eyebrow"], h1=F["h1"], sub=F["sub"],
             kartenquelle=F["kartenquelle"], quellen="".join(f"      <li>{q}</li>\n" for q in quellen), rohdaten=str(F["rohdaten"]),
             D=json.dumps(D, ensure_ascii=False, separators=(",", ":")), SHORT="{}")
kern.schreibe("honolulu/index.html", kern.setze(d["kern"], teile))
kern.schreibe("honolulu/sw.js", kern.setze(d["swkern"], dict(d["swteile"], karte=json.dumps(karte, ensure_ascii=False))))
print("honolulu/ Felder ersetzt:", len(karte), "Kartenstücke")
