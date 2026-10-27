# Erstausgabe der Rennsteiglauf-App aus der Hamburg-App: gleicher Code, eigene Daten, Texte und Speicherschlüssel (rsl-…).
# Ohne eigenes Manifest und Symbol: die Seite verweist auf ../manifest.webmanifest (eine App für alle Strecken).
# Danach wird wie in Hamburg direkt in rennsteig/index.html gearbeitet; dieses Skript ist nur die Herkunft.
import json, os, re, shutil
R = "../../../"; OUT = R + "rennsteig/"; VERSION = "1.0"
os.makedirs(OUT, exist_ok=True)
t = open(R + "hamburg/index.html", encoding="utf-8").read()
def rep(old, new, n=1):
    global t
    assert t.count(old) == n, ("Anzahl", old[:70], t.count(old))
    t = t.replace(old, new)
data = {"tz": "Europe/Berlin", "termine": ["2027-05-22"], "start": 540}   # Start 9:00 am Sportplatz in Neuhaus am Rennweg
data.update(json.load(open("data.json"))); data["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); data["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
data["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
m = re.search(r'^const D = \{.*\};$', t, re.M); t = t[:m.start()] + "const D = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";" + t[m.end():]
rep('<meta name="description" content="Steigungsprofil des Hamburg-Marathons: Höhe, Steigung, Pace-Modell und Karte.">',
    '<meta name="description" content="Steigungsprofil des Marathons beim GutsMuths-Rennsteiglauf: Höhe, Steigung, Pace-Modell und Karte.">')
rep('<title>Steigungsprofil Hamburg-Marathon</title>', '<title>Steigungsprofil Rennsteiglauf-Marathon</title>')
rep('<p class="sub">Amtliches Laser-Höhenmodell (1-m-Raster) entlang der offiziellen Strecke, alle 10 m ausgewertet.</p>',
    '<p class="sub">Laser-Geländemodell Thüringen (20-m-Raster) entlang der Strecke des Veranstalters, alle 10 m ausgewertet.</p>')
rep('<span class="eyebrow">Haspa Marathon Hamburg · Kurs 2025/2026 · ', '<span class="eyebrow">GutsMuths-Rennsteiglauf · Marathon · Kurs 2026 · ')
rep(re.search(r'const SHORT = \{.*?\};', t).group(0), 'const SHORT = {};')
# eigene Speicherschlüssel, damit Einstellungen getrennt bleiben
t = t.replace('"hhm-', '"rsl-').replace('"hhm.', '"rsl.').replace("hhm-theme", "rsl-theme")
assert "hhm" not in t, "hhm übrig"
v = re.search(r"const APP_VERSION = '([\d.]+)';", t).group(1)
rep(f"const APP_VERSION = '{v}';", f"const APP_VERSION = '{VERSION}';")
rep(f'aria-label="Nach Update suchen">v{v}</button>', f'aria-label="Nach Update suchen">v{VERSION}</button>', 2)
# Datengrundlage
g = json.load(open("gpx2026.json")); lk = f"{g['d'][-1] / 1000:.2f}".replace(".", ",")
li = lambda b, s: f"      <li><b>{b}:</b> {s}</li>\n"
a = lambda href, txt: f'<a href="{href}" target="_blank" rel="noopener">{txt}</a>'
neu = (li("Strecke", f'Linie der Outdooractive-Tour des Veranstalters ({a("https://www.rennsteiglauf.de/wettkampf/strecken/marathon/", "rennsteiglauf.de")}), auf die Wege aus OpenStreetMap gelegt: vom Sportplatz in Neuhaus am Rennweg über Steinheid, Friedrichshöhe, Masserberg, Neustadt am Rennsteig und Frauenwald nach Schmiedefeld am Rennsteig, fast ganz auf Forstwegen am Rennsteig. Kilometer nennt der Veranstalter nur für die Verpflegungsstellen; die Linie ist {lk} km lang und gleichmäßig auf 42,195 km gebracht.')
     + li("Höhe", f'Laser-Geländemodell des Freistaats Thüringen (DGM1 2014–2019, © GDI-Th, {a("https://creativecommons.org/licenses/by/4.0/deed.de", "CC BY 4.0")}), von Sonny zu einem 20-m-Raster zusammengestellt ({a("https://sonny.4lima.de", "sonny.4lima.de")}, CC BY 4.0), alle 10 m abgelesen. Das 1-m-Original des Landes war beim Bau nicht abrufbar. Das 20-m-Raster glättet Kuppen und Mulden, die kürzer als etwa 40 m sind; Anstiege über 200 m und mehr zeigt es richtig.<span id="bridges" hidden></span>')
     + li("Glättung", 'Gleitender Median über 30 m gegen Ausreißer. Die Steigung ist der Höhenunterschied über das gewählte Messfenster.'))
m = re.search(r'      <li><b>Strecke:</b>.*?\n      <li><b>Glättung:</b>.*?</li>\n', t, re.S); t = t[:m.start()] + neu + t[m.end():]
rep("Ohne jede Glättung, Punkt für Punkt alle 10 m, ergeben die Rohdaten 174 m.", f"Ohne jede Glättung, Punkt für Punkt alle 10 m, ergeben die Rohdaten {open('rohdaten.txt').read().strip()} m.")
# Staffel: beim Rennsteiglauf-Marathon keine -> Einstellung ausblenden
m = re.search(r'    <div class="setting">\n      <div class="head"><span class="lbl">Staffelwechsel im Profil</span>', t); t = t[:m.start()] + '    <div class="setting" hidden>' + t[m.start() + len('    <div class="setting">'):]
open(OUT + "index.html", "w", encoding="utf-8").write(t)
open(OUT + "version.json", "w").write(json.dumps({"version": VERSION}))
# Kartenstücke
for f in os.listdir("../assets"):
    if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
maps = sorted(f for f in os.listdir(OUT) if f.startswith("karte-"))   # samt Übersicht z11 (werkzeuge/tiles_z11.py schreibt direkt nach rennsteig/)
# Service Worker: wie Hamburg, eigener Cache-Name und eigene Kartenliste
sw = open(R + "hamburg/sw.js", encoding="utf-8").read()
assert 'const CACHE = "hh-marathon-profil";' in sw and 'k.startsWith("hh-")' in sw
sw = sw.replace('const CACHE = "hh-marathon-profil";', 'const CACHE = "rsl-marathon-profil";').replace('k.startsWith("hh-")', 'k.startsWith("rsl-")')
sw = re.sub(r"const KARTE = \[.*?\];", "const KARTE = " + json.dumps(["./" + f for f in maps]).replace('","', '", "') + ";", sw, flags=re.S)
open(OUT + "sw.js", "w", encoding="utf-8").write(sw)
print("rennsteig/ geschrieben:", len(maps), "Kartenstücke, index.html", len(t) // 1024, "KB")
