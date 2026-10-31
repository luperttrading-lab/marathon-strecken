# Erstausgabe der App für den SwissCityMarathon – Lucerne: Felder (Texte, const D, Speicher- und Cache-Präfix lzn-, Kartenliste) für den
# gemeinsamen Kern -> felder.json, dann python3 werkzeuge/kern/kern.py --neu luzern werkzeuge/luzern/work/felder.json (nur beim ersten
# Mal; gibt es luzern/index.html schon, setzt dieses Skript die Felder dort selbst ein, über die Funktionen von kern.py).
# Muster: werkzeuge/zuerich/work/app.py.
# Reihenfolge: parse.py, kmmarken.py, osm.py, strassen.py, bedeckt.py, dgm.py (mit swissalti.py), deck.py, clean.py, orte.py, build.py,
# route.py, tiles.py, dann aus werkzeuge/: tiles_z11.py luzern, luzern/work/app.py, tiles_rand.py luzern 2. Nur Abgleich: vergleich.py.
# Später allein laufen lassen geht: Gibt es luzern/index.html schon, bleiben Kartenbilder und D.tiles (von tiles_rand.py) stehen.
import json, os, shutil, subprocess, sys
R = "../../../"; OUT = R + "luzern/"
sys.path.insert(0, R + "werkzeuge/kern"); import kern
# Termin: 19. SwissCityMarathon – Lucerne am Sonntag, 25. Oktober 2026 (gelaufen; Medienmitteilung des Veranstalters vom 25./28.10.2026,
# Rangliste TrackMaxx scm26); 20. Austragung am Sonntag, 31. Oktober 2027 (Startseite, „Zahlen und Fakten“, Medienmitteilung).
# Start auf der Haldenstrasse am See (Startadresse laut Veranstalter Haldenstrasse 28; „Start & Ziel befinden sich beim Verkehrshaus“),
# gut 0,8 km Luftlinie westlich vom Ziel im Verkehrshaus der Schweiz.
# Startslots nach Wahl bei der Anmeldung (höchstens 500 je Slot, nicht nach Leistung), Performance-Slot nur mit Nachweis; Zeiten laut
# Seite „Start und Startzeiten“ und „Marathon“ (Stand Oktober 2026, für 2027). Zielschluss 15:00 Uhr, maximale Laufzeit 6:15 h
# (Seite „Zielschluss“).
WELLEN = {"q": "Startslots laut Veranstalter (Stand Oktober 2026, für 2027): Den Slot wählt man bei der Anmeldung nach Wunsch und "
               "Verfügbarkeit, nicht nach Leistung, höchstens 500 Läufer je Slot; Buchstabe und Startzeit stehen auf der Startnummer, "
               "später starten geht immer. Der Performance-Slot braucht einen Leistungsnachweis (Frauen unter 3:30, Männer unter 3:00). "
               "Start auf der Haldenstrasse am See, gut 0,8 km westlich vom Ziel im Verkehrshaus. Maximale Laufzeit 6:15 h, Zielschluss 15:00 Uhr; das Schlussfahrzeug "
               "fährt hinter dem letzten Slot, wer überholt wird, ist nicht mehr im Wettkampf.",
          "w": [["Performance", 505, "Frauen unter 3:30, Männer unter 3:00"], ["Startslot", 506, "Pacemaker 3:00, 3:15, 3:30"],
                ["Startslot", 509, "Pacemaker 3:40, 3:50"], ["Startslot", 512, "Pacemaker 4:00"], ["Startslot", 514, "Pacemaker 4:15"],
                ["Startslot", 516, "Pacemaker 4:30, 4:45"], ["Startslot", 518, "Pacemaker 5:00"]]}
D = {"wellen": WELLEN, "tz": "Europe/Zurich", "ort": "Luzern", "ortKurz": " Luzern", "termine": ["2026-10-25", "2027-10-31"], "start": 505}
D.update(json.load(open("data.json"))); D["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); D["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
D["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
NEU = not os.path.exists(OUT + "index.html")
if NEU:
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir("../assets"):
        if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
else:   # Kartenbilder und D.tiles so lassen, wie tiles_rand.py sie gesetzt hat
    D["tiles"] = json.loads(kern.lies_app("luzern")["teile"]["D"])["tiles"]
karte = ["./" + f for f in sorted(os.listdir(OUT)) if f.startswith("karte-")]
quellen = [z.strip()[4:-5] for z in open("quellen.html", encoding="utf-8").read().strip().split("\n")]
quellen.append("<b>Straßennamen:</b> " + open("strassennamen.html", encoding="utf-8").read().strip())
F = {"praefix": "lzn", "cachepraefix": "lzn-", "cachezeile": 'const CACHE = "lzn-marathon-profil";',
     "beschreibung": "Steigungsprofil des SwissCityMarathon Luzern: Höhe, Steigung, Pace-Modell und Karte.",
     "titel": "Steigungsprofil SwissCityMarathon Luzern", "eyebrow": "SwissCityMarathon – Lucerne · Kurs 2026", "h1": "Luzern",
     "sub": open("sub.html", encoding="utf-8").read().strip(), "kartenquelle": "© OpenStreetMap-Mitwirkende",
     "quellen": quellen, "rohdaten": int(open("rohdaten.txt").read().strip()), "SHORT": {}, "karte": karte, "D": D}
json.dump(F, open("felder.json", "w"), ensure_ascii=False, indent=1)
if NEU:
    sys.exit(subprocess.call([sys.executable, R + "werkzeuge/kern/kern.py", "--neu", "luzern", os.path.abspath("felder.json")]))
# Seite gibt es schon: Felder ersetzen (Version und Kern bleiben)
d = kern.lies_app("luzern")
teile = dict(d["teile"], beschreibung=F["beschreibung"], titel=F["titel"], eyebrow=F["eyebrow"], h1=F["h1"], sub=F["sub"],
             kartenquelle=F["kartenquelle"], quellen="".join(f"      <li>{q}</li>\n" for q in quellen), rohdaten=str(F["rohdaten"]),
             D=json.dumps(D, ensure_ascii=False, separators=(",", ":")), SHORT="{}")
kern.schreibe("luzern/index.html", kern.setze(d["kern"], teile))
kern.schreibe("luzern/sw.js", kern.setze(d["swkern"], dict(d["swteile"], karte=json.dumps(karte, ensure_ascii=False))))
print("luzern/ Felder ersetzt:", len(karte), "Kartenstücke")
