# Erstausgabe der Sydney-App aus der Boston-App: gleicher Code, eigene Daten, Texte und Speicherschlüssel (syd-…).
# Ohne eigenes Manifest und Symbol: die Seite verweist auf ../manifest.webmanifest (eine App für alle Strecken).
# Danach wird direkt in sydney/index.html gearbeitet; dieses Skript ist nur die Herkunft.
import json, os, re, shutil
R = "../../../"; OUT = R + "sydney/"; VERSION = "1.0"
os.makedirs(OUT, exist_ok=True)
t = open(R + "boston/index.html", encoding="utf-8").read()
def rep(old, new, n=1):
    global t
    assert t.count(old) == n, ("Anzahl", old[:70], t.count(old))
    t = t.replace(old, new)
# TCS Sydney Marathon am Sonntag, 29. August 2027 (Veranstalter); Start der Läufer 6:30 Uhr (Rollstühle 6:15), Zeiten der
# Startgruppen folgen laut Veranstalter kurz vor dem Rennen.
data = {"tz": "Australia/Sydney", "ortKurz": " Sydney", "termine": ["2027-08-29"], "start": 390}
data.update(json.load(open("data.json"))); data["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); data["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
data["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
m = re.search(r'^const D = \{.*\};$', t, re.M); t = t[:m.start()] + "const D = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";" + t[m.end():]
rep('<meta name="description" content="Steigungsprofil des Boston-Marathons: Höhe, Steigung, Pace-Modell und Karte.">',
    '<meta name="description" content="Steigungsprofil des Sydney-Marathons: Höhe, Steigung, Pace-Modell und Karte.">')
rep('<title>Steigungsprofil Boston-Marathon</title>', '<title>Steigungsprofil Sydney-Marathon</title>')
rep('<span class="eyebrow">Boston Marathon · Kurs 2026 · ', '<span class="eyebrow">TCS Sydney Marathon · Kurs 2026 · ')
rep('<p class="sub">Amtliches Laser-Höhenmodell (1-m-Raster) entlang der offiziellen Strecke, alle 10 m ausgewertet.</p>',
    '<p class="sub">Amtliches Höhenmodell von New South Wales (5-m-Raster) entlang der offiziellen Strecke, alle 10 m ausgewertet. Harbour Bridge und Hochstraßen geschätzt.</p>')
rep("/* Hell/Dunkel: eigene Wahl (bos-theme)", "/* Hell/Dunkel: eigene Wahl (syd-theme)")
t = t.replace('"bos-', '"syd-').replace('"bos.', '"syd.')
assert "bos-" not in t and "bos." not in t, "bos übrig"
v = re.search(r"const APP_VERSION = '([\d.]+)';", t).group(1)
rep(f"const APP_VERSION = '{v}';", f"const APP_VERSION = '{VERSION}';")
rep(f'aria-label="Nach Update suchen">v{v}</button>', f'aria-label="Nach Update suchen">v{VERSION}</button>', 2)
li = lambda b, s: f"      <li><b>{b}:</b> {s}</li>\n"
a = lambda href, txt: f'<a href="{href}" target="_blank" rel="noopener">{txt}</a>'
neu = (li("Strecke", f'Offizielle GPX-Datei des Veranstalters ({a("https://www.tcssydneymarathon.com/marathon", "TCS Sydney Marathon")}, Kurs 2026; dieselbe Linie wie bei goandrace.com). Von der Miller Street in North Sydney über die Harbour Bridge, den Western Distributor nach Pyrmont und zurück, über Barangaroo und The Rocks durch die Innenstadt, die Anzac Parade hinaus nach Kingsford und zurück, eine Runde durch den Centennial Park, über Oxford Street und College Street zu Mrs Macquarie’s Chair und ins Ziel vor dem Opernhaus. Die Linie (42,24 km) ist gleichmäßig auf 42,195 km gebracht. Getränkestellen veröffentlicht der Veranstalter ohne Lage.')
     + li("Höhe", f'NSW 5m Elevation (NSW Spatial Services, Geländemodell aus Laser- und Luftbilddaten, Höhen über AHD, etwa Meeresspiegel), über den {a("https://maps.six.nsw.gov.au/arcgis/rest/services/public/NSW_5M_Elevation/ImageServer", "Höhendienst")} alle 10 m abgefragt. © Spatial Services NSW, CC BY 4.0.')
     + li("Brücken", 'Ein Geländemodell kennt keine Brücken und misst unter der Harbour Bridge das Wasser, unter den Hochstraßen den Boden. Ein offenes Oberflächenmodell gibt es nicht; die Fahrbahn ist deshalb zwischen den Stellen, an denen sie den Boden verlässt und wieder aufsetzt, gerade gezogen und im Läuferblick gestrichelt. Auf der Harbour Bridge fehlt so der flache Scheitel der Fahrbahn über dem Hafen (einige Meter). Geschätzt: <span id="bridges"></span>.')
     + li("Glättung", 'Gleitender Median über 30 m gegen Ausreißer am Straßenrand. Die Steigung ist der Höhenunterschied über das gewählte Messfenster.'))
m = re.search(r'      <li><b>Strecke:</b>.*?\n      <li><b>Glättung:</b>.*?</li>\n', t, re.S); t = t[:m.start()] + neu + t[m.end():]
alt = '      <li><b>Straßennamen:</b> © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>-Mitwirkende, über Nominatim.</li>\n'
rep(alt, '      <li><b>Straßennamen:</b> © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>-Mitwirkende; Straßen aus dem Netz unter der Linie, Vororte aus OSM (Auszug von BBBike).</li>\n')
m = re.search(r"ergeben die Rohdaten \d+ m\.", t); t = t[:m.start()] + f"ergeben die Rohdaten {open('rohdaten.txt').read().strip()} m." + t[m.end():]
open(OUT + "index.html", "w", encoding="utf-8").write(t)
open(OUT + "version.json", "w").write(json.dumps({"version": VERSION}))
for f in os.listdir("../assets"):
    if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
maps = sorted(f for f in os.listdir(OUT) if f.startswith("karte-"))
sw = open(R + "boston/sw.js", encoding="utf-8").read()
assert 'const CACHE = "bos-marathon-profil";' in sw and 'k.startsWith("bos-")' in sw
sw = sw.replace('const CACHE = "bos-marathon-profil";', 'const CACHE = "syd-marathon-profil";').replace('k.startsWith("bos-")', 'k.startsWith("syd-")')
sw = re.sub(r"const KARTE = \[.*?\];", "const KARTE = " + json.dumps(["./" + f for f in maps]).replace('","', '", "') + ";", sw, flags=re.S)
assert "bos" not in sw
open(OUT + "sw.js", "w", encoding="utf-8").write(sw)
print("sydney/ geschrieben:", len(maps), "Kartenstücke, index.html", len(t) // 1024, "KB")
