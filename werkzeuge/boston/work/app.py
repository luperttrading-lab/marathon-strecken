# Erstausgabe der Boston-App aus der New-York-App: gleicher Code, eigene Daten, Texte und Speicherschlüssel (bos-…).
# Ohne eigenes Manifest und Symbol: die Seite verweist auf ../manifest.webmanifest (eine App für alle Strecken).
# Danach wird direkt in boston/index.html gearbeitet; dieses Skript ist nur die Herkunft.
import json, os, re, shutil
R = "../../../"; OUT = R + "boston/"; VERSION = "1.0"
os.makedirs(OUT, exist_ok=True)
t = open(R + "newyork/index.html", encoding="utf-8").read()
def rep(old, new, n=1):
    global t
    assert t.count(old) == n, ("Anzahl", old[:70], t.count(old))
    t = t.replace(old, new)
# Start der ersten Welle 10:00 Uhr Ortszeit (2026: Welle 1 um 10:00, Rollstühle ab 9:02); Patriots' Day 19.4.2027 laut B.A.A.
data = {"tz": "America/New_York", "ort": "Boston", "ortKurz": " Boston", "termine": ["2027-04-19"], "start": 600}
data.update(json.load(open("data.json"))); data["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); data["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
data["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
m = re.search(r'^const D = \{.*\};$', t, re.M); t = t[:m.start()] + "const D = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";" + t[m.end():]
rep('<meta name="description" content="Steigungsprofil des New-York-City-Marathons: Höhe, Steigung, Pace-Modell und Karte.">',
    '<meta name="description" content="Steigungsprofil des Boston-Marathons: Höhe, Steigung, Pace-Modell und Karte.">')
rep('<title>Steigungsprofil New-York-City-Marathon</title>', '<title>Steigungsprofil Boston-Marathon</title>')
rep('<span class="eyebrow">TCS New York City Marathon · Kurs 2026 · ', '<span class="eyebrow">Boston Marathon · Kurs 2026 · ')
rep("/* Hell/Dunkel: eigene Wahl (nyc-theme)", "/* Hell/Dunkel: eigene Wahl (bos-theme)")
# eigene Speicherschlüssel, damit Einstellungen getrennt bleiben
t = t.replace('"nyc-', '"bos-').replace('"nyc.', '"bos.')
assert "nyc" not in t, "nyc übrig"
v = re.search(r"const APP_VERSION = '([\d.]+)';", t).group(1)
rep(f"const APP_VERSION = '{v}';", f"const APP_VERSION = '{VERSION}';")
rep(f'aria-label="Nach Update suchen">v{v}</button>', f'aria-label="Nach Update suchen">v{VERSION}</button>', 2)
# Datengrundlage
g = json.load(open("gpx2026.json")); lk = f"{g['d'][-1] / 1000:.2f}".replace(".", ",")
li = lambda b, s: f"      <li><b>{b}:</b> {s}</li>\n"
a = lambda href, txt: f'<a href="{href}" target="_blank" rel="noopener">{txt}</a>'
neu = (li("Strecke", f'Linie „Boston Marathon“ in OpenStreetMap ({a("https://www.openstreetmap.org/relation/11680552", "Relation 11680552")}): von der Main Street in Hopkinton über Ashland, Framingham, Natick, Wellesley, Newton (Newton Hills, Heartbreak Hill) und Brookline zur Boylston Street in Boston. Eine Linie zum Herunterladen bietet der Veranstalter B.A.A. nicht an ({a("https://www.baa.org/races/boston-marathon", "baa.org")}). Die Linie folgt der Straßenmitte und ist {lk} km lang; sie ist gleichmäßig auf 42,195 km gebracht. Getränkestellen laut B.A.A. (Streckenheft 2026): Wasser und Gatorade ab Meile 2 etwa jede Meile, Gel bei Meile 12, 17 und 22.')
     + li("Höhe", 'USGS 3DEP, Laser-Geländemodell im 1-m-Raster (Höhen über NAVD88, etwa Meeresspiegel), über den Dienst der USGS abgefragt alle 10 m. Brücken: USGS-Laserpunktwolke „MA_CentralEastern_1_2021“. Beides gemeinfrei (U.S. Geological Survey).')
     + li("Brücken", 'Ein Geländemodell kennt keine Brücken und misst darunter Fluss, Gleise oder Autobahn. Die Fahrbahnen der acht Brücken auf der Strecke sind deshalb aus der Laser-Punktwolke gemessen (das untere Zehntel der Punkte im Umkreis von 4 m, die über dem Boden liegen): zweimal Union Street über den Sudbury River in Ashland, Washington Street über die Route 9 in Wellesley, über den Charles River, die I-95 / Route 128 und die Green Line in Newton, Beacon Street über Mass Pike und Bahn vor dem Kenmore Square, Commonwealth Avenue über den Muddy River. Geschätzt ist nichts.<span id="bridges" hidden></span>')
     + li("Glättung", 'Gleitender Median über 30 m gegen Ausreißer am Straßenrand. Die Steigung ist der Höhenunterschied über das gewählte Messfenster.'))
m = re.search(r'      <li><b>Strecke:</b>.*?\n      <li><b>Glättung:</b>.*?</li>\n', t, re.S); t = t[:m.start()] + neu + t[m.end():]
rep("Die Kartenbilder stammen von tile.openstreetmap.org und sind für den hellen und dunklen Modus umgefärbt.", "Die Kartenbilder stammen von tile.openstreetmap.org und sind für den dunklen Grund umgefärbt.")
rep("Ohne jede Glättung, Punkt für Punkt alle 10 m, ergeben die Rohdaten 360 m.", f"Ohne jede Glättung, Punkt für Punkt alle 10 m, ergeben die Rohdaten {open('rohdaten.txt').read().strip()} m.")
open(OUT + "index.html", "w", encoding="utf-8").write(t)
open(OUT + "version.json", "w").write(json.dumps({"version": VERSION}))
# Kartenstücke
for f in os.listdir("../assets"):
    if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
maps = sorted(f for f in os.listdir(OUT) if f.startswith("karte-"))   # samt Übersicht z11 (werkzeuge/tiles_z11.py schreibt direkt nach boston/)
# Service Worker: wie New York, eigener Cache-Name und eigene Kartenliste
sw = open(R + "newyork/sw.js", encoding="utf-8").read()
o = 'const CACHE = "nyc-marathon-profil-2";   // -2 seit 1.21: ohne helle Kartenbilder, der alte Cache wird gelöscht'
assert o in sw and 'k.startsWith("nyc-")' in sw
sw = sw.replace(o, 'const CACHE = "bos-marathon-profil";').replace('k.startsWith("nyc-")', 'k.startsWith("bos-")')
sw = re.sub(r"const KARTE = \[.*?\];", "const KARTE = " + json.dumps(["./" + f for f in maps]).replace('","', '", "') + ";", sw, flags=re.S)
assert "nyc" not in sw
open(OUT + "sw.js", "w", encoding="utf-8").write(sw)
print("boston/ geschrieben:", len(maps), "Kartenstücke, index.html", len(t) // 1024, "KB")
