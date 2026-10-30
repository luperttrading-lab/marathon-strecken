# Erstausgabe der App für den TCS Amsterdam Marathon aus der Tokio-App (Stand 1.24, aktueller gemeinsamer Code): gleicher Code,
# eigene Daten, Texte und Speicherschlüssel (ams-…). Ohne eigenes Manifest und Symbol: die Seite verweist auf ../manifest.webmanifest
# (eine App für alle Strecken). Danach wird direkt in amsterdam/index.html gearbeitet; dieses Skript ist nur die Herkunft.
# Reihenfolge: pdflinie.py, osm.py grob, wasser.py, einpassen.py, linie.py, strassen.py, dgm.py, clean.py, orte.py, build.py,
# marken.py (nur Abgleich), route.py, tiles.py, dann aus werkzeuge/: tiles_z11.py amsterdam, work/app.py, tiles_rand.py amsterdam 2
import json, os, re, shutil
R = "../../../"; OUT = R + "amsterdam/"; VERSION = "1.0"
os.makedirs(OUT, exist_ok=True)
t = open(R + "tokio/index.html", encoding="utf-8").read()
def rep(old, new, n=1):
    global t
    assert t.count(old) == n, ("Anzahl", old[:70], t.count(old))
    t = t.replace(old, new)
# TCS Amsterdam Marathon 2026 am Sonntag, 18. Oktober 2026 (gelaufen); 2027 laut Veranstalter am Wochenende 30./31. Oktober, der
# Marathon wie immer am Sonntag (31.10.2027). Start 9:00 in sechs Wellen bis 9:43, gleichzeitig in Startbereich A (Olympiastadion)
# und B (Stadionweg), laut Seiten „Start times“ und „TCS Marathon“ des Veranstalters (2026).
WELLEN = {"q": "Sechs Wellen 2026 laut Veranstalter, eingeteilt nach erwarteter Zielzeit; die Farbe steht auf der Startnummer. "
               "Startbereich A im Olympiastadion und B auf dem Stadionweg starten gleichzeitig. Für 2027 noch nicht veröffentlicht.",
          "w": [["Welle 1", 540, "Weiß · Eingeladene und bis 2:40"], ["Welle 2", 542, "Gelb · 2:40–3:15"], ["Welle 3", 551, "Rosa · 3:15–3:45"],
                ["Welle 4", 564, "Orange · 3:45–4:00"], ["Welle 5", 574, "Grün · 4:00–4:30"], ["Welle 6", 583, "Blau · 4:30–6:00"]]}
data = {"wellen": WELLEN, "tz": "Europe/Amsterdam", "ort": "Amsterdam", "ortKurz": " Amsterdam",
        "termine": ["2026-10-18", "2027-10-31"], "start": 540}
data.update(json.load(open("data.json"))); data["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); data["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
data["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
m = re.search(r'^const D = \{.*\};$', t, re.M); t = t[:m.start()] + "const D = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";" + t[m.end():]
rep('<meta name="description" content="Steigungsprofil des Tokio-Marathons: Höhe, Steigung, Pace-Modell und Karte.">',
    '<meta name="description" content="Steigungsprofil des Amsterdam-Marathons: Höhe, Steigung, Pace-Modell und Karte.">')
rep('<title>Steigungsprofil Tokio-Marathon</title>', '<title>Steigungsprofil Amsterdam-Marathon</title>')
rep('<span class="eyebrow">Tokyo Marathon · Kurs 2026 · ', '<span class="eyebrow">TCS Amsterdam Marathon · Kurs 2026 · ')
rep('<h1>Tokio</h1>', '<h1>Amsterdam</h1>')   # Ort als Überschrift (seit Hamburg 1.73)
rep('<p class="sub">Amtliches Laser-Höhenmodell der GSI (5-m-Raster) entlang der offiziellen Strecke, alle 10 m ausgewertet.</p>',
    '<p class="sub">' + open("sub.html", encoding="utf-8").read().strip() + '</p>')
rep("/* Hell/Dunkel: eigene Wahl (tyo-theme)", "/* Hell/Dunkel: eigene Wahl (ams-theme)")
t = t.replace('"tyo-', '"ams-').replace('"tyo.', '"ams.')
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
sw = sw.replace('const CACHE = "tyo-marathon-profil";', 'const CACHE = "ams-marathon-profil";').replace('k.startsWith("tyo-")', 'k.startsWith("ams-")')
sw = re.sub(r"const KARTE = \[.*?\];", "const KARTE = " + json.dumps(["./" + f for f in maps]).replace('","', '", "') + ";", sw, flags=re.S)
assert "tyo" not in sw
open(OUT + "sw.js", "w", encoding="utf-8").write(sw)
assert "lage" not in data
print("amsterdam/ geschrieben:", len(maps), "Kartenstücke, index.html", len(t) // 1024, "KB")
