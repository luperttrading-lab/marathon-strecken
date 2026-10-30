# Erstausgabe der App für Run Rome The Marathon aus der Tokio-App (Stand 1.24, aktueller gemeinsamer Code): gleicher Code, eigene Daten,
# Texte und Speicherschlüssel (rom-…). Ohne eigenes Manifest und Symbol: die Seite verweist auf ../manifest.webmanifest (eine App für
# alle Strecken). Danach wird direkt in rom/index.html gearbeitet; dieses Skript ist nur die Herkunft.
# Reihenfolge: build.py, route.py, tiles.py, dann aus werkzeuge/: tiles_z11.py rom, work/app.py, tiles_rand.py rom 2
import json, os, re, shutil
R = "../../../"; OUT = R + "rom/"; VERSION = "1.0"
os.makedirs(OUT, exist_ok=True)
t = open(R + "tokio/index.html", encoding="utf-8").read()
def rep(old, new, n=1):
    global t
    assert t.count(old) == n, ("Anzahl", old[:70], t.count(old))
    t = t.replace(old, new)
# 32. Run Rome The Marathon am Sonntag, 14. März 2027 (Reglement 2027 des Veranstalters, „partenza alle ore 8:30 circa“; dieselbe
# Formel stand im Reglement 2026, gestartet wurde dann ab 8:00). Wellen 2026 laut Event Guide und Seite des Veranstalters: Rollstühle
# 8:00, Welle 1 Griglie TOP und A 8:10, B 8:20, C 8:30, D 8:45, E 9:00, Staffel 9:15 (die englische Fassung des Guides nennt für die
# erste Welle 8:15, die italienische und die Zeitlimits 8:10). Der Wellenplan 2027 ist noch nicht veröffentlicht.
WELLEN = {"q": "Wellen 2026 laut Event Guide des Veranstalters, eingeteilt nach der angegebenen Bestzeit; die Griglia steht auf der "
               "Startnummer (Rollstühle 8:00, Staffel 9:15). Für 2027 nennt das Reglement „8:30 circa“ wie schon für 2026; den "
               "Wellenplan 2027 gibt der Veranstalter später bekannt.",
          "w": [["Welle 1", 490, "Griglie TOP und A · orange"], ["Welle 2", 500, "Griglia B · grün"], ["Welle 3", 510, "Griglia C · blau"],
                ["Welle 4", 525, "Griglia D · weiß"], ["Welle 5", 540, "Griglia E · rot"]]}
data = {"wellen": WELLEN, "tz": "Europe/Rome", "ort": "Rom", "ortKurz": " Rom", "termine": ["2027-03-14"], "start": 490}
data.update(json.load(open("data.json"))); data["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); data["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
data["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
m = re.search(r'^const D = \{.*\};$', t, re.M); t = t[:m.start()] + "const D = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";" + t[m.end():]
rep('<meta name="description" content="Steigungsprofil des Tokio-Marathons: Höhe, Steigung, Pace-Modell und Karte.">',
    '<meta name="description" content="Steigungsprofil des Rom-Marathons: Höhe, Steigung, Pace-Modell und Karte.">')
rep('<title>Steigungsprofil Tokio-Marathon</title>', '<title>Steigungsprofil Rom-Marathon</title>')
rep('<span class="eyebrow">Tokyo Marathon · Kurs 2026 · ', '<span class="eyebrow">Run Rome The Marathon · Kurs 2026 · ')
rep('<p class="sub">Amtliches Laser-Höhenmodell der GSI (5-m-Raster) entlang der offiziellen Strecke, alle 10 m ausgewertet.</p>',
    '<p class="sub">' + open("sub.html", encoding="utf-8").read().strip() + '</p>')
rep("/* Hell/Dunkel: eigene Wahl (tyo-theme)", "/* Hell/Dunkel: eigene Wahl (rom-theme)")
t = t.replace('"tyo-', '"rom-').replace('"tyo.', '"rom.')
assert "tyo-" not in t and "tyo." not in t, "tyo übrig"
v = re.search(r"const APP_VERSION = '([\d.]+)';", t).group(1)
rep(f"const APP_VERSION = '{v}';", f"const APP_VERSION = '{VERSION}';")
# Beschriftung der beiden Versionsknöpfe vor dem Skript (das Skript setzt sie aus APP_VERSION)
assert len(re.findall(r'aria-label="Nach Update suchen">v[\d.]+</button>', t)) == 2
t = re.sub(r'aria-label="Nach Update suchen">v[\d.]+</button>', f'aria-label="Nach Update suchen">v{VERSION}</button>', t)
# Quellen: Strecke, Höhe, Brücken, Glättung (Texte in quellen.html, eine <li>-Zeile je Punkt)
neu = open("quellen.html", encoding="utf-8").read().rstrip("\n") + "\n"
m = re.search(r'      <li><b>Strecke:</b>.*?\n      <li><b>Glättung:</b>.*?</li>\n', t, re.S); t = t[:m.start()] + neu + t[m.end():]
alt = '      <li><b>Straßennamen:</b> © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>-Mitwirkende; Straßen aus dem Netz unter der Linie, japanische Namen in Umschrift, Bezirke über den Adressdienst der GSI.</li>\n'
rep(alt, '      <li><b>Straßennamen:</b> ' + open("strassennamen.html", encoding="utf-8").read().strip() + '</li>\n')
m = re.search(r"ergeben die Rohdaten \d+ m\.", t); t = t[:m.start()] + f"ergeben die Rohdaten {open('rohdaten.txt').read().strip()} m." + t[m.end():]
open(OUT + "index.html", "w", encoding="utf-8").write(t)
open(OUT + "version.json", "w").write(json.dumps({"version": VERSION}))
for f in os.listdir("../assets"):
    if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
maps = sorted(f for f in os.listdir(OUT) if f.startswith("karte-"))
sw = open(R + "tokio/sw.js", encoding="utf-8").read()
assert 'const CACHE = "tyo-marathon-profil";' in sw and 'k.startsWith("tyo-")' in sw
sw = sw.replace('const CACHE = "tyo-marathon-profil";', 'const CACHE = "rom-marathon-profil";').replace('k.startsWith("tyo-")', 'k.startsWith("rom-")')
sw = re.sub(r"const KARTE = \[.*?\];", "const KARTE = " + json.dumps(["./" + f for f in maps]).replace('","', '", "') + ";", sw, flags=re.S)
assert "tyo" not in sw
open(OUT + "sw.js", "w", encoding="utf-8").write(sw)
print("rom/ geschrieben:", len(maps), "Kartenstücke, index.html", len(t) // 1024, "KB")
