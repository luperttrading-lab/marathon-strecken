# Erstausgabe der Valencia-App aus der Tokio-App (Stand 1.22, aktueller gemeinsamer Code): gleicher Code, eigene Daten, Texte
# und Speicherschlüssel (vlc-…). Ohne eigenes Manifest und Symbol: die Seite verweist auf ../manifest.webmanifest (eine App für
# alle Strecken). Danach wird direkt in valencia/index.html gearbeitet; dieses Skript ist nur die Herkunft.
# Reihenfolge: build.py, route.py, tiles.py, dann aus werkzeuge/: tiles_z11.py valencia, work/app.py, tiles_rand.py valencia 2
import json, os, re, shutil
R = "../../../"; OUT = R + "valencia/"; VERSION = "1.0"
os.makedirs(OUT, exist_ok=True)
t = open(R + "tokio/index.html", encoding="utf-8").read()
def rep(old, new, n=1):
    global t
    assert t.count(old) == n, ("Anzahl", old[:70], t.count(old))
    t = t.replace(old, new)
# 46. Maratón Valencia Trinidad Alfonso Zurich am Sonntag, 6. Dezember 2026 (Reglement 2026, Art. 1 und 3); 2027 üblicherweise
# am ersten Sonntag im Dezember, noch nicht bestätigt. Start 8:15 in neun Wellen bis 9:35 (Art. 3), Boxen und Farben laut
# Streckenplan 2026 und Google-Karte. Ortsname für die Uhrzeiten aus den Daten: Europe/Madrid ergäbe „Madrid“.
WELLEN = {"q": "Neun Wellen 2026 laut Reglement des Veranstalters, eingeteilt nach angegebener Zielzeit (unter 3:32 mit Nachweis "
               "einer Bestzeit); Box und Welle stehen auf der Startnummer. Rollstühle starten vorab mit der dritten Welle.",
          "w": [["Box 1–3", 495, "Gelb, Grün, Blau · unter 2:50"], ["Box 4", 505, "Rosa · 2:50–3:00"], ["Box 5", 515, "Orange · 3:00–3:12"],
                ["Box 6", 525, "Lila · 3:12–3:20"], ["Box 7", 535, "Braun · 3:20–3:32"], ["Box 8", 545, "Grau · 3:32–3:43"],
                ["Box 9", 555, "Rot · 3:43–3:56"], ["Box 10", 565, "Blaue Punkte · 3:56–4:10"], ["Box 11", 575, "Weiß · ab 4:10"]]}
data = {"wellen": WELLEN, "tz": "Europe/Madrid", "ort": "Valencia", "ortKurz": " Valencia", "termine": ["2026-12-06", "2027-12-05?"], "start": 495}
data.update(json.load(open("data.json"))); data["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); data["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
data["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
m = re.search(r'^const D = \{.*\};$', t, re.M); t = t[:m.start()] + "const D = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";" + t[m.end():]
rep('<meta name="description" content="Steigungsprofil des Tokio-Marathons: Höhe, Steigung, Pace-Modell und Karte.">',
    '<meta name="description" content="Steigungsprofil des Valencia-Marathons: Höhe, Steigung, Pace-Modell und Karte.">')
rep('<title>Steigungsprofil Tokio-Marathon</title>', '<title>Steigungsprofil Valencia-Marathon</title>')
rep('<span class="eyebrow">Tokyo Marathon · Kurs 2026 · ', '<span class="eyebrow">Maratón Valencia Trinidad Alfonso Zurich · Kurs 2026 · ')
rep('<p class="sub">Amtliches Laser-Höhenmodell der GSI (5-m-Raster) entlang der offiziellen Strecke, alle 10 m ausgewertet.</p>',
    '<p class="sub">' + open("sub.html", encoding="utf-8").read().strip() + '</p>')
rep("/* Hell/Dunkel: eigene Wahl (tyo-theme)", "/* Hell/Dunkel: eigene Wahl (vlc-theme)")
t = t.replace('"tyo-', '"vlc-').replace('"tyo.', '"vlc.')
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
rep(alt, '      <li><b>Straßennamen:</b> © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>-Mitwirkende; Straßen aus dem Netz unter der Linie, valencianische Namen wie in OpenStreetMap. Distrikte: Ajuntament de València (<a href="https://geoportal.valencia.es/" target="_blank" rel="noopener">Geoportal, Open Data</a>).</li>\n')
m = re.search(r"ergeben die Rohdaten \d+ m\.", t); t = t[:m.start()] + f"ergeben die Rohdaten {open('rohdaten.txt').read().strip()} m." + t[m.end():]
open(OUT + "index.html", "w", encoding="utf-8").write(t)
open(OUT + "version.json", "w").write(json.dumps({"version": VERSION}))
for f in os.listdir("../assets"):
    if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
maps = sorted(f for f in os.listdir(OUT) if f.startswith("karte-"))
sw = open(R + "tokio/sw.js", encoding="utf-8").read()
assert 'const CACHE = "tyo-marathon-profil";' in sw and 'k.startsWith("tyo-")' in sw
sw = sw.replace('const CACHE = "tyo-marathon-profil";', 'const CACHE = "vlc-marathon-profil";').replace('k.startsWith("tyo-")', 'k.startsWith("vlc-")')
sw = re.sub(r"const KARTE = \[.*?\];", "const KARTE = " + json.dumps(["./" + f for f in maps]).replace('","', '", "') + ";", sw, flags=re.S)
assert "tyo" not in sw
open(OUT + "sw.js", "w", encoding="utf-8").write(sw)
print("valencia/ geschrieben:", len(maps), "Kartenstücke, index.html", len(t) // 1024, "KB")
