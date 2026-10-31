# Erstausgabe der App für den Gornergrat Zermatt Marathon: Felder (Texte, const D, Speicher- und Cache-Präfix zgm-, Kartenliste) für den
# gemeinsamen Kern -> felder.json, dann python3 werkzeuge/kern/kern.py --neu zermatt werkzeuge/zermatt/work/felder.json (nur beim ersten
# Mal; gibt es zermatt/index.html schon, setzt dieses Skript die Felder dort selbst ein, über die Funktionen von kern.py).
# Muster: werkzeuge/luzern/work/app.py.
# Reihenfolge: parse.py, osm.py, strassen.py, bedeckt.py, dgm.py (mit swissalti.py), deck.py, clean.py, namen3d.py, orte.py, build.py,
# route.py, tiles.py, dann aus werkzeuge/: tiles_z11.py zermatt (Ordner ../zermatt/ muss es geben), zermatt/work/app.py,
# tiles_rand.py zermatt 2. Nur Abgleich: vergleich.py.
# Später allein laufen lassen geht: Gibt es zermatt/index.html schon, bleiben Kartenbilder und D.tiles (von tiles_rand.py) stehen.
import json, os, shutil, subprocess, sys
R = "../../../"; OUT = R + "zermatt/"
sys.path.insert(0, R + "werkzeuge/kern"); import kern
# Termin: Gornergrat Zermatt Marathon am Samstag, 4. Juli 2026 (gelaufen; Seite „Marathon“: „Am 4. Juli 2026 führt die Strecke …“,
# Rangliste Datasport „gornergrat-zermatt-marathon-2026“, 03.–04.07.2026, Marathon am Samstag). Nächste Austragung Samstag, 3. Juli 2027
# (Seiten „Startzeiten“ und „Marathon“: „Startzeiten in St. Niklaus 1120 m ü. M · Samstag, 3. Juli 2027 · 8:30 Uhr Elite Runner sowie
# Block 1 für Marathon + ULTRA · ab 8:33 Uhr Blockstarts Marathon + ULTRA“; Anmeldung bei Datasport „gornergrat-zermatt-marathon-2027“).
# Startblöcke laut Race Magazin 2026 (S. 27): Start 8:30 ELITE, MARATHON Block 1, ULTRA Block 1; Start 8:33 MARATHON Block 2, ULTRA Block 2.
# Kontrollschluss laut Seite „Streckenverpflegung & Kontrollzeiten“, Reglement Ziffer 8 und Race Magazin 2026.
WELLEN = {"q": "Startzeiten laut Veranstalter für den 3. Juli 2027 (wie 2026): 8:30 Uhr Elite und Block 1, ab 8:33 Uhr Block 2, Marathon und "
               "Ultra gemeinsam in St. Niklaus; ausser bei Elite und Block 1 zählt die Zeit ab der Startlinie. Kontrollschluss: Zermatt "
               "Bahnhofplatz 11:50 Uhr (hier km 20,6, Veranstalter km 21,1), Sunnegga 13:45 Uhr (hier km 32,0), Hotel Riffelalp Resort "
               "14:55 Uhr (km 39,1), Zielschluss auf dem Riffelberg 15:45 Uhr. Wer einen Posten später erreicht, wird nicht mehr klassiert "
               "und hat keinen Anspruch mehr auf Verpflegung und Sanität; wer weiterläuft, bekommt eine Markierung auf die Startnummer. "
               "Stöcke sind verboten.",
          "w": [["Elite und Block 1", 510, "Marathon und Ultra"], ["Block 2", 513, "Marathon und Ultra"]]}
D = {"wellen": WELLEN, "tz": "Europe/Zurich", "ort": "Zermatt", "ortKurz": " Zermatt", "termine": ["2026-07-04", "2027-07-03"], "start": 510}
D.update(json.load(open("data.json"))); D["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); D["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
D["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
NEU = not os.path.exists(OUT + "index.html")
if NEU:
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir("../assets"):
        if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
else:   # Kartenbilder und D.tiles so lassen, wie tiles_rand.py sie gesetzt hat
    D["tiles"] = json.loads(kern.lies_app("zermatt")["teile"]["D"])["tiles"]
karte = ["./" + f for f in sorted(os.listdir(OUT)) if f.startswith("karte-")]
quellen = [z.strip()[4:-5] for z in open("quellen.html", encoding="utf-8").read().strip().split("\n")]
quellen.append("<b>Straßennamen:</b> " + open("strassennamen.html", encoding="utf-8").read().strip())
F = {"praefix": "zgm", "cachepraefix": "zgm-", "cachezeile": 'const CACHE = "zgm-marathon-profil";',
     "beschreibung": "Steigungsprofil des Gornergrat Zermatt Marathons von St. Niklaus auf den Riffelberg: Höhe, Steigung, Pace-Modell und Karte.",
     "titel": "Steigungsprofil Gornergrat Zermatt Marathon", "eyebrow": "Gornergrat Zermatt Marathon · Kurs 2026", "h1": "Zermatt",
     "sub": open("sub.html", encoding="utf-8").read().strip(), "kartenquelle": "© OpenStreetMap-Mitwirkende",
     "quellen": quellen, "rohdaten": int(open("rohdaten.txt").read().strip()), "SHORT": {}, "karte": karte, "D": D}
json.dump(F, open("felder.json", "w"), ensure_ascii=False, indent=1)
if NEU:
    sys.exit(subprocess.call([sys.executable, R + "werkzeuge/kern/kern.py", "--neu", "zermatt", os.path.abspath("felder.json")]))
# Seite gibt es schon: Felder ersetzen (Version und Kern bleiben)
d = kern.lies_app("zermatt")
teile = dict(d["teile"], beschreibung=F["beschreibung"], titel=F["titel"], eyebrow=F["eyebrow"], h1=F["h1"], sub=F["sub"],
             kartenquelle=F["kartenquelle"], quellen="".join(f"      <li>{q}</li>\n" for q in quellen), rohdaten=str(F["rohdaten"]),
             D=json.dumps(D, ensure_ascii=False, separators=(",", ":")), SHORT="{}")
kern.schreibe("zermatt/index.html", kern.setze(d["kern"], teile))
kern.schreibe("zermatt/sw.js", kern.setze(d["swkern"], dict(d["swteile"], karte=json.dumps(karte, ensure_ascii=False))))
print("zermatt/ Felder ersetzt:", len(karte), "Kartenstücke")
