# App für den Great Wall Marathon aus der Tokio-App (gemeinsamer Code): gleicher Code, eigene Daten, Texte und Speicherschlüssel
# (gwm-…). Ohne eigenes Manifest und Symbol: die Seite verweist auf ../manifest.webmanifest (eine App für alle Strecken).
# Liest bei jedem Lauf tokio/index.html und tokio/sw.js frisch und ersetzt nur die streckenspezifischen Stellen; nach Änderungen am
# gemeinsamen Code einfach noch einmal laufen lassen (aus work/ heraus). Die Kartenstücke aller Stufen (z11–z15, Relief) baut
# tiles.py selbst; tiles_z11.py und tiles_rand.py dürfen hier nicht laufen (sie holen OSM-Kacheln und überschrieben das Relief).
# Reihenfolge: osm.py, plan.py, georef.py, linie.py, dgm.py, planprofil.py, marken.py, form.py, common.py (Eichung), vergleich.py,
#              build.py, splits.py, mauer.py, route.py, tiles.py relief, app.py
import json, os, re, shutil
R = "../../../"; OUT = R + "greatwall/"; VERSION = "1.0"
os.makedirs(OUT, exist_ok=True)
t = open(R + "tokio/index.html", encoding="utf-8").read()
def rep(old, new, n=1):
    global t
    assert t.count(old) == n, ("Anzahl", old[:70], t.count(old))
    t = t.replace(old, new)
# Great Wall Marathon am Samstag, 15. Mai 2027 (Seite des Veranstalters: „Future race dates are: 2027: May 15th“, Countdown
# 2027-05-15T01:30:00+0200 = 7:30 Pekinger Zeit; 2028: 20. Mai). Wellen 2026 laut Runners Guide (Marathon und Halbmarathon gemischt,
# Welle nach der bei der Anmeldung angegebenen Zeit, Farbe auf der Startnummer); Startschüsse 2026 laut Zeitnahme 7:32:09, 7:40:06,
# 7:49:38. Fun Run (Welle 4, grün) 8:00. Zeitzone Asia/Shanghai = Pekinger Zeit; die Zeitzone allein nennt „Shanghai“.
WELLEN = {"q": "Wellen 2026 laut Runners Guide des Veranstalters, Marathon und Halbmarathon gemischt: Welle 1 mit den schnelleren, Welle 3 "
               "mit den langsameren oder ohne gemeldete Zeiten; Welle und Farbe stehen auf der Startnummer, wechseln darf man nur in eine "
               "spätere Welle. 2026 fielen die Startschüsse um 7:32, 7:40 und 7:50. Fun Run 8:00. Den Zeitplan 2027 gibt der Veranstalter "
               "mit dem Runners Guide bekannt.",
          "w": [["Welle 1", 450, "rosa"], ["Welle 2", 460, "gelb"], ["Welle 3", 470, "blau"]]}
data = {"wellen": WELLEN, "tz": "Asia/Shanghai", "ort": "Huangyaguan", "ortKurz": " Peking", "termine": ["2027-05-15"], "start": 450}
data.update(json.load(open("data.json"))); data["route"] = json.load(open("route50.json"))
# Zeit auf der Mauer je Durchgang (gemeinsamer Code seit 1.69: ein Rad je Durchgang, ohne eigenes Drehen die Empfehlung für die
# Zielzeit): D.mauerEmpf = [[Minuten bei 5 h, je Stunde mehr], …] aus der Geraden durch alle Läufer 2026 (mauer.py); vierter Wert in
# D.mauer = Median bei 4:45–5:15 (nur Rückfall); D.mauerQ erklärt, warum die Durchgänge verschieden lang dauern
mz = json.load(open("mauer.json")); G = {g["ziel"]: g for g in mz["gruppen"]}
data["mauer"] = [m[:3] + [mz["median" + str(k + 1)]] for k, m in enumerate(data["mauer"])]
data["ziel"] = 5 * 3600   # Voreinstellung 5:00:00: 4:00 /km im Flachen ergäbe 3:22, schneller als der Sieger 2024 (3:43:32); die Empfehlung gilt um 5 h
data["mauerEmpf"] = [[mz["Mauer 1"]["bei5h"], mz["Mauer 1"]["jeStunde"]], [mz["Mauer 2"]["bei5h"], mz["Mauer 2"]["jeStunde"]]]
schnell, langsam = G["4–4.5 h"], G["7–7.5 h"]
mi = lambda v: str(round(v))
data["mauerQ"] = ("Warum zwei verschiedene Zeiten: Beim 1. Mal sind Marathon und Halbmarathon aller drei Wellen zugleich auf der Mauer, die Treppen "
                  "sind schmal, überholen geht kaum. Deshalb brauchten 2026 fast alle ähnlich lange: " + mi(schnell["mauer1"][1]) + " min, wer in 4 bis "
                  "4½ h ins Ziel kam, " + mi(langsam["mauer1"][1]) + " min bei 7 bis 7½ h. Das 2. Mal führt nach 35 km den Goat Track hinauf, das Feld "
                  "hat sich verteilt: Jetzt zählt die eigene Form, " + mi(schnell["mauer2"][1]) + " gegen " + mi(langsam["mauer2"][1]) + " min. Die "
                  "Empfehlung folgt den Zwischenzeiten 2026 (" + str(sum(g["n"] for g in mz["gruppen"])) + " Läufer, Mediane): je Stunde Zielzeit "
                  + mi(mz["Mauer 1"]["jeStunde"]) + " min mehr beim 1. Mal und " + mi(mz["Mauer 2"]["jeStunde"]) + " min mehr beim 2. Mal; "
                  "unter 4 h gab es keine Daten.")
tm = json.load(open("tilemeta.json")); data["tiles"] = {z: tm[z] for z in sorted((k for k in tm if k.isdigit()), key=int)}
data["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
m = re.search(r'^const D = \{.*\};$', t, re.M); t = t[:m.start()] + "const D = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";" + t[m.end():]
rep('<meta name="description" content="Steigungsprofil des Tokio-Marathons: Höhe, Steigung, Pace-Modell und Karte.">',
    '<meta name="description" content="Steigungsprofil des Great Wall Marathons: Strecke, Mauer, Höhe, Steigung, Pace-Modell und Karte.">')
rep('<title>Steigungsprofil Tokio-Marathon</title>', '<title>Steigungsprofil Great Wall Marathon</title>')
rep('<span class="eyebrow">Tokyo Marathon · Kurs 2026 · ', '<span class="eyebrow">Great Wall Marathon · Kurs 2026 · ')
rep('<p class="sub">Amtliches Laser-Höhenmodell der GSI (5-m-Raster) entlang der offiziellen Strecke, alle 10 m ausgewertet.</p>',
    '<p class="sub">' + open("sub.html", encoding="utf-8").read().strip() + '</p>')
rep("/* Hell/Dunkel: eigene Wahl (tyo-theme)", "/* Hell/Dunkel: eigene Wahl (gwm-theme)")
t = t.replace('"tyo-', '"gwm-').replace('"tyo.', '"gwm.')
assert "tyo-" not in t and "tyo." not in t, "tyo übrig"
v = re.search(r"const APP_VERSION = '([\d.]+)';", t).group(1)
rep(f"const APP_VERSION = '{v}';", f"const APP_VERSION = '{VERSION}';")
# Beschriftung der beiden Versionsknöpfe vor dem Skript (das Skript setzt sie aus APP_VERSION)
assert len(re.findall(r'aria-label="Nach Update suchen">v[\d.]+</button>', t)) == 2
t = re.sub(r'aria-label="Nach Update suchen">v[\d.]+</button>', f'aria-label="Nach Update suchen">v{VERSION}</button>', t)
# Quellen: Strecke, Höhe, Brücken, Glättung (Texte in quellen.html, eine <li>-Zeile je Punkt), Karte, Straßennamen
neu = open("quellen.html", encoding="utf-8").read().rstrip("\n") + "\n"
m = re.search(r'      <li><b>Strecke:</b>.*?\n      <li><b>Glättung:</b>.*?</li>\n', t, re.S); t = t[:m.start()] + neu + t[m.end():]
rep('      <li><b>Karte:</b> © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>-Mitwirkende (ODbL). Die Kartenbilder stammen von tile.openstreetmap.org und sind für den dunklen Grund umgefärbt.</li>\n',
    '      <li><b>Karte:</b> ' + open("karte.html", encoding="utf-8").read().strip() + '</li>\n')
alt = '      <li><b>Straßennamen:</b> © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>-Mitwirkende; Straßen aus dem Netz unter der Linie, japanische Namen in Umschrift, Bezirke über den Adressdienst der GSI.</li>\n'
rep(alt, '      <li><b>Straßennamen:</b> ' + open("strassennamen.html", encoding="utf-8").read().strip() + '</li>\n')
rep('<span class="credit map-credit">© OpenStreetMap-Mitwirkende</span>', '<span class="credit map-credit">© OpenStreetMap-Mitwirkende · Relief Copernicus DEM</span>')
m = re.search(r"ergeben die Rohdaten \d+ m\.", t); t = t[:m.start()] + f"ergeben die Rohdaten {open('rohdaten.txt').read().strip()} m." + t[m.end():]
assert not re.search(r"tokio|tokyo|GSI|国土", t, re.I), re.search(r".{40}(tokio|tokyo|GSI|国土).{40}", t, re.I).group(0)
open(OUT + "index.html", "w", encoding="utf-8").write(t)
open(OUT + "version.json", "w").write(json.dumps({"version": VERSION}))
for f in os.listdir(OUT):
    if f.startswith("karte-"): os.remove(OUT + f)
for f in os.listdir("../assets"):
    if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
maps = sorted(f for f in os.listdir(OUT) if f.startswith("karte-"))
assert sorted(f"karte-dunkel-{c[4]}.jpg" for z in data["tiles"].values() for c in z["chunks"]) == maps, "D.tiles passt nicht zu den Dateien"
sw = open(R + "tokio/sw.js", encoding="utf-8").read()
assert 'const CACHE = "tyo-marathon-profil";' in sw and 'k.startsWith("tyo-")' in sw
sw = sw.replace('const CACHE = "tyo-marathon-profil";', 'const CACHE = "gwm-marathon-profil";').replace('k.startsWith("tyo-")', 'k.startsWith("gwm-")')
sw = re.sub(r"const KARTE = \[.*?\];", "const KARTE = " + json.dumps(["./" + f for f in maps]).replace('","', '", "') + ";", sw, flags=re.S)
assert "tyo" not in sw
open(OUT + "sw.js", "w", encoding="utf-8").write(sw)
print("greatwall/ geschrieben:", len(maps), "Kartenstücke, index.html", len(t) // 1024, "KB, D.mauerEmpf", data["mauerEmpf"])
