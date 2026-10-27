# Erstausgabe der Köln-App aus der Hamburg-App: gleicher Code, eigene Daten, Texte und Speicherschlüssel (kln-…).
# Seit „nur eine App“ (Hamburg 1.16) ohne eigenes Manifest und Symbol: die Seite verweist auf ../manifest.webmanifest.
# Danach wird wie in Hamburg direkt in koeln/index.html gearbeitet; dieses Skript ist nur die Herkunft.
import json, os, re, shutil
R = "../../../"; OUT = R + "koeln/"; VERSION = "1.0"
os.makedirs(OUT, exist_ok=True)
t = open(R + "hamburg/index.html", encoding="utf-8").read()
def rep(old, new, n=1):
    global t
    assert t.count(old) == n, ("Anzahl", old[:70], t.count(old))
    t = t.replace(old, new)
data = {"tz": "Europe/Berlin", "termine": ["2027-10-03?"], "start": 630}   # Start 10:30 am Ottoplatz (Faltplan 2026)
data.update(json.load(open("data.json"))); data["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); data["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
data["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
m = re.search(r'^const D = \{.*\};$', t, re.M); t = t[:m.start()] + "const D = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";" + t[m.end():]
rep('<meta name="description" content="Steigungsprofil des Hamburg-Marathons: Höhe, Steigung, Pace-Modell und Karte.">',
    '<meta name="description" content="Steigungsprofil des Köln-Marathons: Höhe, Steigung, Pace-Modell und Karte.">')
rep('<title>Steigungsprofil Hamburg-Marathon</title>', '<title>Steigungsprofil Köln-Marathon</title>')
rep('<span class="eyebrow">Haspa Marathon Hamburg · Kurs 2025/2026 · ', '<span class="eyebrow">Generali Köln Marathon · Kurs 2026 · ')
rep(re.search(r'const SHORT = \{.*?\};', t).group(0), 'const SHORT = {};')
# eigene Speicherschlüssel, damit Einstellungen getrennt bleiben
t = t.replace('"hhm-', '"kln-').replace('"hhm.', '"kln.').replace("hhm-theme", "kln-theme")
assert "hhm" not in t, "hhm übrig"
v = re.search(r"const APP_VERSION = '([\d.]+)';", t).group(1)
rep(f"const APP_VERSION = '{v}';", f"const APP_VERSION = '{VERSION}';")
rep(f'aria-label="Nach Update suchen">v{v}</button>', f'aria-label="Nach Update suchen">v{VERSION}</button>', 2)
# Datengrundlage
li = lambda b, s: f"      <li><b>{b}:</b> {s}</li>\n"
neu = (li("Strecke", 'offizielle GPX-Datei des Veranstalters (<a href="https://generali-koeln-marathon.de/strecken/" target="_blank" rel="noopener">generali-koeln-marathon.de</a>), dieselbe Linie wie in seiner Streckenkarte, Kurs 2026 mit Start in Deutz und Ziel am Dom. Kilometerpunkte veröffentlicht der Veranstalter nicht. Die gezeichnete Linie ist 0,2 % kürzer als die vermessene Strecke und ist deshalb gleichmäßig auf 42,195 km gestreckt; einzelne Stellen können so um bis zu 80 m verschoben sein.')
     + li("Höhe", 'Digitales Geländemodell DGM1 NRW, Laserscan im 1-m-Raster (© Geobasis NRW, <a href="https://www.govdata.de/dl-de/zero-2-0" target="_blank" rel="noopener">dl-de/zero-2-0</a>), über den Geodienst des Landes abgefragt alle 10 m.')
     + li("Brücken und Unterführungen", 'Ein Geländemodell kennt keine Brücken. Auf der Deutzer Brücke misst es den Rhein, an anderen Brücken die Straße darunter, und wo die Strecke unter einem Bauwerk durchführt, an manchen Stellen das Bauwerk darüber. Diese Stellen sind erkannt und durch eine Gerade ersetzt, im Läuferblick sind sie gestrichelt: <span id="bridges"></span>.')
     + li("Glättung", 'Gleitender Median über 30 m gegen Ausreißer am Straßenrand. Die Steigung ist der Höhenunterschied über das gewählte Messfenster.'))
m = re.search(r'      <li><b>Strecke:</b>.*?\n      <li><b>Glättung:</b>.*?</li>\n', t, re.S); t = t[:m.start()] + neu + t[m.end():]
rep("Ohne jede Glättung, Punkt für Punkt alle 10 m, ergeben die Rohdaten 174 m.", f"Ohne jede Glättung, Punkt für Punkt alle 10 m, ergeben die Rohdaten {open('rohdaten.txt').read().strip()} m.")
# Staffelwechsel: Köln hat einen Staffelmarathon, die Wechselpunkte sind aber nicht veröffentlicht -> Einstellung ausblenden
m = re.search(r'    <div class="setting">\n      <div class="head"><span class="lbl">Staffelwechsel im Profil</span>', t); t = t[:m.start()] + '    <div class="setting" hidden>' + t[m.start() + len('    <div class="setting">'):]
open(OUT + "index.html", "w", encoding="utf-8").write(t)
open(OUT + "version.json", "w").write(json.dumps({"version": VERSION}))
# Kartenstücke
for f in os.listdir("../assets"):
    if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
maps = sorted(f for f in os.listdir(OUT) if f.startswith("karte-"))   # samt Übersicht z11 (werkzeuge/tiles_z11.py schreibt direkt nach koeln/)
# Service Worker: wie Hamburg, eigener Cache-Name und eigene Kartenliste
sw = open(R + "hamburg/sw.js", encoding="utf-8").read()
assert 'const CACHE = "hh-marathon-profil";' in sw and 'k.startsWith("hh-")' in sw
sw = sw.replace('const CACHE = "hh-marathon-profil";', 'const CACHE = "kln-marathon-profil";').replace('k.startsWith("hh-")', 'k.startsWith("kln-")')
sw = re.sub(r"const KARTE = \[.*?\];", "const KARTE = " + json.dumps(["./" + f for f in maps]).replace('","', '", "') + ";", sw, flags=re.S)
open(OUT + "sw.js", "w", encoding="utf-8").write(sw)
print("koeln/ geschrieben:", len(maps), "Kartenstücke, index.html", len(t) // 1024, "KB")
