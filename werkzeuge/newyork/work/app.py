# Erstausgabe der New-York-App aus der Hamburg-App: gleicher Code, eigene Daten, Texte, Schlüssel und Symbole.
# Danach wird wie in Hamburg direkt in newyork/index.html gearbeitet; dieses Skript ist nur die Herkunft.
import json, os, re, shutil
import numpy as np
from PIL import Image, ImageDraw
R = "../../../"; OUT = R + "newyork/"; VERSION = "1.0"
os.makedirs(OUT, exist_ok=True)
t = open(R + "hamburg/index.html", encoding="utf-8").read()
def rep(old, new, n=1):
    global t
    assert t.count(old) == n, ("Anzahl", old[:70], t.count(old))
    t = t.replace(old, new)
data = json.load(open("data.json")); data["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); data["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
data["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
m = re.search(r'^const D = \{.*\};$', t, re.M); t = t[:m.start()] + "const D = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";" + t[m.end():]
rep('<meta name="description" content="Steigungsprofil des Hamburg-Marathons: Höhe, Steigung, Pace-Modell und Karte.">',
    '<meta name="description" content="Steigungsprofil des New-York-City-Marathons: Höhe, Steigung, Pace-Modell und Karte.">')
rep('<title>Steigungsprofil Hamburg-Marathon</title>', '<title>Steigungsprofil New-York-City-Marathon</title>')
rep('<meta name="apple-mobile-web-app-title" content="HH-Marathon">', '<meta name="apple-mobile-web-app-title" content="NYC-Marathon">')
rep('<span class="eyebrow">Haspa Marathon Hamburg · Kurs 2025/2026 · ', '<span class="eyebrow">TCS New York City Marathon · Kurs 2026 · ')
rep('const SHORT = { "St. Pauli Fischmarkt": "Fischmarkt", "St. Pauli Hafenstraße": "Hafenstraße", "Bei den St. Pauli-Landungsbrücken": "Landungsbrücken" };', 'const SHORT = {};')
# New York hat geschätzte Auf- und Abfahrten (Queensboro Bridge): im Text zur Datengrundlage mit aufzählen
rep('// Tunnel einzeln mit Länge, Unterführungen und Brücken gesammelt', '// Tunnel einzeln mit Länge, Unterführungen, Brücken und Rampen gesammelt')
rep('["Brücke", "Brücken"]].map', '["Brücke", "Brücken"], ["Rampe", "Rampen"]].map')
# eigene Speicherschlüssel, damit Position und Einstellungen getrennt bleiben
t = t.replace('"hhm-', '"nyc-').replace('"hhm.', '"nyc.').replace("hhm-theme", "nyc-theme")
assert "hhm" not in t, "hhm übrig"
v = re.search(r"const APP_VERSION = '([\d.]+)';", t).group(1)
rep(f"const APP_VERSION = '{v}';", f"const APP_VERSION = '{VERSION}';")
rep(f'aria-label="Nach Update suchen">v{v}</button>', f'aria-label="Nach Update suchen">v{VERSION}</button>', 2)
# Datengrundlage
li = lambda b, s: f"      <li><b>{b}:</b> {s}</li>\n"
neu = (li("Strecke", 'offizielle Karte des Veranstalters New York Road Runners (<a href="https://www.nyrr.org" target="_blank" rel="noopener">nyrr.org</a>), Kurs 2026 mit der geänderten Führung durch die Bronx, Linie der blauen Startwelle über die obere Ebene der Verrazzano-Narrows Bridge, dazu 26 Meilen-, 8 Fünf-Kilometer-Marken, Halbmarathon und Ziel. Die gezeichnete Linie ist 0,4 % länger als die vermessene Strecke. Deshalb ist jeder Abschnitt auf die offiziellen Marken geeicht. Angezeigt wird in Kilometern.')
     + li("Höhe", 'USGS 3DEP, Laser-Geländemodell im 1-m-Raster (Höhen über NAVD88, etwa Meeresspiegel), über den Dienst der USGS abgefragt alle 10 m. Brücken: USGS-Laserpunktwolke „NY_NewYorkCity“. Beides gemeinfrei (U.S. Geological Survey).')
     + li("Brücken", 'Ein Geländemodell kennt keine Brücken, in New York sind sie aber die großen Anstiege. Die Fahrbahnen der Verrazzano-Narrows, Pulaski, Queensboro, Willis Avenue und Madison Avenue Bridge sind deshalb aus der Laser-Punktwolke gemessen: das untere Zehntel der Punkte im Umkreis von 4 m, die über dem Boden liegen (Seile, Fachwerk und Fahrzeuge liegen darüber). Auf der Queensboro Bridge wird unten gelaufen, gemessen ist die obere Ebene; Auf- und Abfahrt sind Geraden. Geschätzte und kurze übrige Stellen sind im Läuferblick gestrichelt: <span id="bridges"></span>.')
     + li("Glättung", 'Gleitender Median über 30 m gegen Ausreißer am Straßenrand. Die Steigung ist der Höhenunterschied über das gewählte Messfenster.'))
m = re.search(r'      <li><b>Strecke:</b>.*?\n      <li><b>Glättung:</b>.*?</li>\n', t, re.S); t = t[:m.start()] + neu + t[m.end():]
rep("Ohne jede Glättung, Punkt für Punkt alle 10 m, ergeben die Rohdaten 174 m.", f"Ohne jede Glättung, Punkt für Punkt alle 10 m, ergeben die Rohdaten {open('rohdaten.txt').read().strip()} m.")
# Kein Staffelmarathon: Einstellung ausblenden (die Knöpfe bleiben im Code, damit nichts bricht)
m = re.search(r'    <div class="setting">\n      <div class="head"><span class="lbl">Staffelwechsel im Profil</span>', t); t = t[:m.start()] + '    <div class="setting" hidden>' + t[m.start() + len('    <div class="setting">'):]
open(OUT + "index.html", "w", encoding="utf-8").write(t)
open(OUT + "version.json", "w").write(json.dumps({"version": VERSION}))
# Kartenstücke
for f in os.listdir("../assets"):
    if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
maps = sorted(f for f in os.listdir(OUT) if f.startswith("karte-"))   # samt Übersicht z11 (werkzeuge/tiles_z11.py schreibt direkt nach newyork/)
# Service Worker: wie Hamburg, eigener Cache-Name und eigene Kartenliste
sw = open(R + "hamburg/sw.js", encoding="utf-8").read()
sw = sw.replace('const CACHE = "hh-marathon-profil";', 'const CACHE = "nyc-marathon-profil";')
sw = sw.replace('k.startsWith("hh-")', 'k.startsWith("nyc-")')
sw = re.sub(r"const KARTE = \[.*?\];", "const KARTE = " + json.dumps(["./" + f for f in maps]).replace('","', '", "') + ";", sw, flags=re.S)
open(OUT + "sw.js", "w", encoding="utf-8").write(sw)
man = json.load(open(R + "hamburg/manifest.webmanifest", encoding="utf-8"))
man.update({"name": "Steigungsprofil New-York-City-Marathon", "short_name": "NYC-Marathon", "description": "Höhe, Steigung, Pace-Modell und Karte für den New-York-City-Marathon.", "background_color": "#140a1a", "theme_color": "#0b141c"})
open(OUT + "manifest.webmanifest", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1) + "\n")
# Symbol: Höhenprofil nach Steigung gefärbt, auf Pflaume (Hamburg Nachtblau, Frankfurt Weinrot, Berlin Tannengrün)
H = [x / 100 for x in data["h"]][:4220]; lo_, hi_ = min(H) - 2, max(H) + 2
def icon(size):
    S4 = size * 4
    im = Image.new("RGB", (S4, S4)); dr = ImageDraw.Draw(im)
    for y in range(S4):
        q = y / S4; dr.line([(0, y), (S4, y)], fill=(int(28 + 40 * q), int(12 + 18 * q), int(36 + 50 * q)))
    mrg = int(S4 * 0.14); x0, x1 = mrg, S4 - mrg; base = int(S4 * 0.74); top = int(S4 * 0.30)
    n = len(H); step = max(1, n // 300); pts = []
    for i in range(0, n, step): pts.append((x0 + (x1 - x0) * i / (n - 1), base - (H[i] - lo_) / (hi_ - lo_) * (base - top)))
    cols = [(13, 102, 128), (58, 148, 173), (149, 201, 214), (155, 167, 178), (240, 192, 96), (229, 131, 58), (195, 53, 42)]
    edges = [-3, -1.5, -0.5, 0.5, 1.5, 3]
    for j in range(len(pts) - 1):
        i = j * step; i2 = min(n - 1, i + 100); i1 = max(0, i - 100)
        g = (H[i2] - H[i1]) / ((i2 - i1) * 10) * 100; c = 0
        while c < len(edges) and g >= edges[c]: c += 1
        (xa, ya), (xb, yb) = pts[j], pts[j + 1]
        dr.polygon([(xa, ya), (xb + 1, yb), (xb + 1, base), (xa, base)], fill=cols[c])
    dr.line(pts, fill=(229, 236, 241), width=max(2, S4 // 90), joint="curve")
    dr.rectangle([x0, base, x1, base + max(2, S4 // 120)], fill=(106, 156, 255))
    return im.resize((size, size), Image.LANCZOS)
for s, name in ((512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png")):
    icon(s).save(OUT + name, optimize=True)
print("newyork/ geschrieben:", len(maps), "Kartenstücke, index.html", len(t) // 1024, "KB")
