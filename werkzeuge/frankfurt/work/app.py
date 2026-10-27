# Erstausgabe der Frankfurt-App aus der Hamburg-App: gleicher Code, eigene Daten, Texte, Schlüssel und Symbole.
# Danach wird wie in Hamburg direkt in frankfurt/index.html gearbeitet; dieses Skript ist nur die Herkunft.
import json, os, re, shutil
import numpy as np
from PIL import Image, ImageDraw
R = "../../../"; OUT = R + "frankfurt/"; VERSION = "1.0"
os.makedirs(OUT, exist_ok=True)
t = open(R + "hamburg/index.html", encoding="utf-8").read()
def rep(old, new, n=1):
    global t
    assert t.count(old) == n, ("Anzahl", old[:70], t.count(old))
    t = t.replace(old, new)
data = json.load(open("data.json")); data["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); data["tiles"] = {z: tm[z] for z in sorted(tm)}
data["imgNote"] = ("<b>Abgleich mit dem Veranstalter:</b> Er nennt einen Gesamthöhenunterschied von 27,8 m und 83 Höhenmeter. "
                   "Im Laserscan liegen zwischen dem tiefsten Punkt (90,0 m, Unterführung Oeserstraße, km 28,7) und dem höchsten "
                   "(118,1 m, Eschersheimer Landstraße, km 10,2) 28,1 m, mit 200-m-Messfenster ergeben sich 82 Höhenmeter. Beides passt.")
m = re.search(r'^const D = \{.*\};$', t, re.M); t = t[:m.start()] + "const D = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";" + t[m.end():]
rep('<meta name="description" content="Steigungsprofil des Hamburg-Marathons: Höhe, Steigung, Pace-Modell und Karte.">',
    '<meta name="description" content="Steigungsprofil des Frankfurt-Marathons: Höhe, Steigung, Pace-Modell und Karte.">')
rep('<title>Steigungsprofil Hamburg-Marathon</title>', '<title>Steigungsprofil Frankfurt-Marathon</title>')
rep('<meta name="apple-mobile-web-app-title" content="HH-Marathon">', '<meta name="apple-mobile-web-app-title" content="FFM-Marathon">')
rep('<span class="eyebrow">Haspa Marathon Hamburg · Kurs 2025/2026 · ', '<span class="eyebrow">Mainova Frankfurt Marathon · Kurs 2026 · ')
rep('const SHORT = { "St. Pauli Fischmarkt": "Fischmarkt", "St. Pauli Hafenstraße": "Hafenstraße", "Bei den St. Pauli-Landungsbrücken": "Landungsbrücken" };', 'const SHORT = {};')
# eigene Speicherschlüssel, damit Position und Einstellungen getrennt bleiben
t = t.replace('"hhm-', '"ffm-').replace('"hhm.', '"ffm.').replace("hhm-theme", "ffm-theme")
assert "hhm" not in t, "hhm übrig"
v = re.search(r"const APP_VERSION = '([\d.]+)';", t).group(1)
rep(f"const APP_VERSION = '{v}';", f"const APP_VERSION = '{VERSION}';")
rep(f'aria-label="Nach Update suchen">v{v}</button>', f'aria-label="Nach Update suchen">v{VERSION}</button>', 2)
# Datengrundlage
li = lambda b, s: f"      <li><b>{b}:</b> {s}</li>\n"
neu = (li("Strecke", 'offizielle GPX-Datei und die 41 offiziellen Kilometerpunkte des Veranstalters (<a href="https://www.frankfurt-marathon.com/dein-lauf/marathon/strecke/" target="_blank" rel="noopener">frankfurt-marathon.com</a>). Die gezeichnete Linie ist 0,4 % länger als die vermessene Strecke. Deshalb ist jeder Kilometer auf die offiziellen Kilometerpunkte geeicht.')
     + li("Höhe", 'Digitales Geländemodell DGM1 Hessen, Laserscan im 1-m-Raster (© HVBG, <a href="https://www.govdata.de/dl-de/zero-2-0" target="_blank" rel="noopener">dl-de/zero-2-0</a>), über den Geodienst des Landes abgelesen alle 10 m.')
     + li("Brücken und Unterführungen", 'Ein Geländemodell kennt keine Brücken. Auf einer Brücke misst es das Wasser darunter, und wo die Strecke unter einer Bahn- oder Autobahnbrücke durchführt, an manchen Stellen den Damm darüber. Diese Stellen sind erkannt und durch eine Gerade ersetzt, im Läuferblick sind sie gestrichelt: <span id="bridges"></span>. Ebenso geglättet ist ein Buckel des Modells am Zieleinlauf in die Festhalle.')
     + li("Glättung", 'Gleitender Median über 30 m gegen Ausreißer am Straßenrand. Die Steigung ist der Höhenunterschied über das gewählte Messfenster.'))
m = re.search(r'      <li><b>Strecke:</b>.*?\n      <li><b>Glättung:</b>.*?</li>\n', t, re.S); t = t[:m.start()] + neu + t[m.end():]
rep("Ohne jede Glättung, Punkt für Punkt alle 10 m, ergeben die Rohdaten 174 m.", "Ohne jede Glättung, Punkt für Punkt alle 10 m, ergeben die Rohdaten 178 m.")
open(OUT + "index.html", "w", encoding="utf-8").write(t)
open(OUT + "version.json", "w").write(json.dumps({"version": VERSION}))
# Kartenstücke
maps = sorted(f for f in os.listdir("../assets") if f.startswith("karte-"))
for f in maps: shutil.copy("../assets/" + f, OUT + f)
# Service Worker: wie Hamburg, eigener Cache-Name und eigene Kartenliste
sw = open(R + "hamburg/sw.js", encoding="utf-8").read()
sw = sw.replace('const CACHE = "hh-marathon-profil";', 'const CACHE = "ffm-marathon-profil";')
sw = sw.replace('k.startsWith("hh-")', 'k.startsWith("ffm-")')
sw = re.sub(r"const KARTE = \[.*?\];", "const KARTE = " + json.dumps(["./" + f for f in maps]).replace('","', '", "') + ";", sw, flags=re.S)
open(OUT + "sw.js", "w", encoding="utf-8").write(sw)
man = json.load(open(R + "hamburg/manifest.webmanifest", encoding="utf-8"))
man.update({"name": "Steigungsprofil Frankfurt-Marathon", "short_name": "FFM-Marathon", "description": "Höhe, Steigung, Pace-Modell und Karte für den Frankfurt-Marathon.", "background_color": "#140b10", "theme_color": "#0b141c"})
open(OUT + "manifest.webmanifest", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1) + "\n")
# Symbol: Höhenprofil nach Steigung gefärbt, auf Weinrot statt Nachtblau (zur Unterscheidung von Hamburg)
H = [x / 100 for x in data["h"]][:4220]; lo_, hi_ = min(H) - 2, max(H) + 2
def icon(size):
    S4 = size * 4
    im = Image.new("RGB", (S4, S4)); dr = ImageDraw.Draw(im)
    for y in range(S4):
        q = y / S4; dr.line([(0, y), (S4, y)], fill=(int(28 + 50 * q), int(11 + 14 * q), int(20 + 22 * q)))
    mrg = int(S4 * 0.14); x0, x1 = mrg, S4 - mrg; base = int(S4 * 0.74); top = int(S4 * 0.30)
    n = len(H); step = max(1, n // 300); pts = []
    for i in range(0, n, step): pts.append((x0 + (x1 - x0) * i / (n - 1), base - (H[i] - lo_) / (hi_ - lo_) * (base - top)))
    cols = [(13, 102, 128), (58, 148, 173), (149, 201, 214), (155, 167, 178), (240, 192, 96), (229, 131, 58), (195, 53, 42)]
    edges = [-3, -1.5, -0.5, 0.5, 1.5, 3]
    for j in range(len(pts) - 1):
        i = j * step; i2 = min(n - 1, i + 100); i1 = max(0, i - 100)
        g = (H[i2] - H[i1]) / ((i2 - i1) * 10) * 100 * 3; c = 0          # Frankfurt ist flach: Steigung für die Farbe dreifach
        while c < len(edges) and g >= edges[c]: c += 1
        (xa, ya), (xb, yb) = pts[j], pts[j + 1]
        dr.polygon([(xa, ya), (xb + 1, yb), (xb + 1, base), (xa, base)], fill=cols[c])
    dr.line(pts, fill=(229, 236, 241), width=max(2, S4 // 90), joint="curve")
    dr.rectangle([x0, base, x1, base + max(2, S4 // 120)], fill=(106, 156, 255))
    return im.resize((size, size), Image.LANCZOS)
for s, name in ((512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png")):
    icon(s).save(OUT + name, optimize=True)
print("frankfurt/ geschrieben:", len(maps), "Kartenstücke, index.html", len(t) // 1024, "KB")
