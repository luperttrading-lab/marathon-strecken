# Erstausgabe der App für den OCHSNER SPORT Zürich Marathon: Felder (Texte, const D, Speicher- und Cache-Präfix zrh-, Kartenliste) für den
# gemeinsamen Kern -> felder.json, dann python3 werkzeuge/kern/kern.py --neu zuerich werkzeuge/zuerich/work/felder.json (nur beim ersten
# Mal; gibt es zuerich/index.html schon, setzt dieses Skript die Felder dort selbst ein, über die Funktionen von kern.py).
# Muster: werkzeuge/honolulu/work/app.py.
# Reihenfolge: parse.py, osm.py, strassen.py, dgm.py (mit swissalti.py), deck.py, clean.py, orte.py, plan.py, build.py, route.py, tiles.py,
# dann aus werkzeuge/: tiles_z11.py zuerich, zuerich/work/app.py, tiles_rand.py zuerich 2. Nur Abgleich: vergleich.py, ansicht.py.
# Später allein laufen lassen geht: Gibt es zuerich/index.html schon, bleiben Kartenbilder und D.tiles (von tiles_rand.py) stehen.
import json, os, shutil, subprocess, sys
R = "../../../"; OUT = R + "zuerich/"
sys.path.insert(0, R + "werkzeuge/kern"); import kern
# Termin: 23. OCHSNER SPORT Zürich Marathon am Sonntag, 12. April 2026 (gelaufen, Rangliste bei Race Result); 24. am Sonntag, 11. April
# 2027 (Veranstalter: Startseite, „Marathon“, „von A bis Z“ und FAQ). Start 8:00 Uhr auf der Quaibrücke, Ziel Sechseläutenplatz,
# Zeitlimit 5:30 h netto, Zielschluss 13:45 Uhr, Wendepunkt Meilen bis 11:10 Uhr (Seiten „Marathon“ und „Start und Ziel“).
# Massenstart mit rollendem Ablauf der Startblöcke nach angegebener Zielzeit; Uhrzeiten je Block nicht veröffentlicht.
WELLEN = {"q": "Massenstart um 8:00 Uhr auf der Quaibrücke (Veranstalter, 2026 und 2027), die Startblöcke folgen rollend nacheinander; "
               "der Block richtet sich nach der angegebenen Zielzeit und steht als Farbe auf der Startnummer (Uhrzeiten je Block nicht "
               "veröffentlicht). Zeitlimit 5:30 h netto, Zielschluss 13:45 Uhr. Wer den Wendepunkt in Meilen (km 22) nicht bis 11:10 Uhr "
               "erreicht, muss Startnummer und Transponder abgeben.", "w": []}
D = {"wellen": WELLEN, "tz": "Europe/Zurich", "ort": "Zürich", "ortKurz": " Zürich", "termine": ["2026-04-12", "2027-04-11"], "start": 480}
D.update(json.load(open("data.json"))); D["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); D["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
D["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
NEU = not os.path.exists(OUT + "index.html")
if NEU:
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir("../assets"):
        if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
else:   # Kartenbilder und D.tiles so lassen, wie tiles_rand.py sie gesetzt hat
    D["tiles"] = json.loads(kern.lies_app("zuerich")["teile"]["D"])["tiles"]
karte = ["./" + f for f in sorted(os.listdir(OUT)) if f.startswith("karte-")]
quellen = [z.strip()[4:-5] for z in open("quellen.html", encoding="utf-8").read().strip().split("\n")]
quellen.append("<b>Straßennamen:</b> " + open("strassennamen.html", encoding="utf-8").read().strip())
F = {"praefix": "zrh", "cachepraefix": "zrh-", "cachezeile": 'const CACHE = "zrh-marathon-profil";',
     "beschreibung": "Steigungsprofil des Zürich Marathons: Höhe, Steigung, Pace-Modell und Karte.",
     "titel": "Steigungsprofil Zürich Marathon", "eyebrow": "OCHSNER SPORT Zürich Marathon · Kurs 2026", "h1": "Zürich",
     "sub": open("sub.html", encoding="utf-8").read().strip(), "kartenquelle": "© OpenStreetMap-Mitwirkende",
     "quellen": quellen, "rohdaten": int(open("rohdaten.txt").read().strip()), "SHORT": {}, "karte": karte, "D": D}
json.dump(F, open("felder.json", "w"), ensure_ascii=False, indent=1)
if NEU:
    sys.exit(subprocess.call([sys.executable, R + "werkzeuge/kern/kern.py", "--neu", "zuerich", os.path.abspath("felder.json")]))
# Seite gibt es schon: Felder ersetzen (Version und Kern bleiben)
d = kern.lies_app("zuerich")
teile = dict(d["teile"], beschreibung=F["beschreibung"], titel=F["titel"], eyebrow=F["eyebrow"], h1=F["h1"], sub=F["sub"],
             kartenquelle=F["kartenquelle"], quellen="".join(f"      <li>{q}</li>\n" for q in quellen), rohdaten=str(F["rohdaten"]),
             D=json.dumps(D, ensure_ascii=False, separators=(",", ":")), SHORT="{}")
kern.schreibe("zuerich/index.html", kern.setze(d["kern"], teile))
kern.schreibe("zuerich/sw.js", kern.setze(d["swkern"], dict(d["swteile"], karte=json.dumps(karte, ensure_ascii=False))))
print("zuerich/ Felder ersetzt:", len(karte), "Kartenstücke")
