# Erstausgabe der Chicago-App aus der Boston-App: gleicher Code, eigene Daten, Texte und Speicherschlüssel (chi-…).
# Ohne eigenes Manifest und Symbol: die Seite verweist auf ../manifest.webmanifest (eine App für alle Strecken).
# Danach wird direkt in chicago/index.html gearbeitet; dieses Skript ist nur die Herkunft.
import json, os, re, shutil
R = "../../../"; OUT = R + "chicago/"; VERSION = "1.0"
os.makedirs(OUT, exist_ok=True)
t = open(R + "boston/index.html", encoding="utf-8").read()
def rep(old, new, n=1):
    global t
    assert t.count(old) == n, ("Anzahl", old[:70], t.count(old))
    t = t.replace(old, new)
# 49. Chicago Marathon am 10.10.2027, Start 7:30 Uhr Ortszeit (Bank of America, Pressemitteilung)
data = {"tz": "America/Chicago", "ortKurz": " Chicago", "termine": ["2027-10-10"], "start": 450}
data.update(json.load(open("data.json"))); data["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); data["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
data["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
m = re.search(r'^const D = \{.*\};$', t, re.M); t = t[:m.start()] + "const D = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";" + t[m.end():]
rep('<meta name="description" content="Steigungsprofil des Boston-Marathons: Höhe, Steigung, Pace-Modell und Karte.">',
    '<meta name="description" content="Steigungsprofil des Chicago-Marathons: Höhe, Steigung, Pace-Modell und Karte.">')
rep('<title>Steigungsprofil Boston-Marathon</title>', '<title>Steigungsprofil Chicago-Marathon</title>')
rep('<span class="eyebrow">Boston Marathon · Kurs 2026 · ', '<span class="eyebrow">Bank of America Chicago Marathon · Kurs 2026 · ')
rep("/* Hell/Dunkel: eigene Wahl (bos-theme)", "/* Hell/Dunkel: eigene Wahl (chi-theme)")
t = t.replace('"bos-', '"chi-').replace('"bos.', '"chi.')
assert "bos-" not in t and "bos." not in t, "bos übrig"
v = re.search(r"const APP_VERSION = '([\d.]+)';", t).group(1)
rep(f"const APP_VERSION = '{v}';", f"const APP_VERSION = '{VERSION}';")
rep(f'aria-label="Nach Update suchen">v{v}</button>', f'aria-label="Nach Update suchen">v{VERSION}</button>', 2)
li = lambda b, s: f"      <li><b>{b}:</b> {s}</li>\n"
a = lambda href, txt: f'<a href="{href}" target="_blank" rel="noopener">{txt}</a>'
neu = (li("Strecke", f'Abbiegeliste des Veranstalters (Straßensperrungen 2026, {a("https://www.chicagomarathon.com", "chicagomarathon.com")}) über das Straßennetz von OpenStreetMap gelegt: vom Columbus Drive im Grant Park nach Norden bis Lake View, zurück durch Lincoln Park und Old Town, nach Westen bis zur Damen Avenue, über Little Italy, Pilsen, Chinatown und Bronzeville zurück zur Michigan Avenue und über „Mount Roosevelt“ ins Ziel. Start, Ziel, 26 Meilen- und 8 Fünf-Kilometer-Marken sowie die 20 Verpflegungsstationen und 2 Gel-Depots stammen aus der offiziellen Karte (Vektor-PDF, über 24 Kreuzungen auf 15 m genau verortet). Die Linie entlang der Straßenmitte ist 1,6 % länger als die vermessene Ideallinie und deshalb auf die Marken geeicht.')
     + li("Höhe", 'USGS 3DEP, Laser-Geländemodell im 1-m-Raster (Illinois, Befliegung 2017; Höhen über NAVD88), über den Dienst der USGS abgefragt alle 10 m. Gemeinfrei (U.S. Geological Survey).')
     + li("Brücken", 'Ein Geländemodell kennt keine Brücken und misst darunter den Chicago River, Autobahnen oder Gleise; unter dem Columbus Drive misst es eine höhere Plattform. Eine Laserpunktwolke für Chicago gibt es bei der USGS nicht. Diese Stellen sind zwischen den Auflagern gerade gezogen und im Läuferblick gestrichelt: <span id="bridges"></span>.')
     + li("Glättung", 'Gleitender Median über 30 m gegen Ausreißer am Straßenrand. Die Steigung ist der Höhenunterschied über das gewählte Messfenster.'))
m = re.search(r'      <li><b>Strecke:</b>.*?\n      <li><b>Glättung:</b>.*?</li>\n', t, re.S); t = t[:m.start()] + neu + t[m.end():]
m = re.search(r"ergeben die Rohdaten \d+ m\.", t); t = t[:m.start()] + f"ergeben die Rohdaten {open('rohdaten.txt').read().strip()} m." + t[m.end():]
open(OUT + "index.html", "w", encoding="utf-8").write(t)
open(OUT + "version.json", "w").write(json.dumps({"version": VERSION}))
for f in os.listdir("../assets"):
    if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
maps = sorted(f for f in os.listdir(OUT) if f.startswith("karte-"))
sw = open(R + "boston/sw.js", encoding="utf-8").read()
assert 'const CACHE = "bos-marathon-profil";' in sw and 'k.startsWith("bos-")' in sw
sw = sw.replace('const CACHE = "bos-marathon-profil";', 'const CACHE = "chi-marathon-profil";').replace('k.startsWith("bos-")', 'k.startsWith("chi-")')
sw = re.sub(r"const KARTE = \[.*?\];", "const KARTE = " + json.dumps(["./" + f for f in maps]).replace('","', '", "') + ";", sw, flags=re.S)
assert "bos" not in sw
open(OUT + "sw.js", "w", encoding="utf-8").write(sw)
print("chicago/ geschrieben:", len(maps), "Kartenstücke, index.html", len(t) // 1024, "KB")
