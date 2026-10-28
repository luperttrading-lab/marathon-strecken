# Erstausgabe der Tokio-App aus der Boston-App: gleicher Code, eigene Daten, Texte und Speicherschlüssel (tyo-…).
# Ohne eigenes Manifest und Symbol: die Seite verweist auf ../manifest.webmanifest (eine App für alle Strecken).
# Danach wird direkt in tokio/index.html gearbeitet; dieses Skript ist nur die Herkunft.
import json, os, re, shutil
R = "../../../"; OUT = R + "tokio/"; VERSION = "1.0"
os.makedirs(OUT, exist_ok=True)
t = open(R + "boston/index.html", encoding="utf-8").read()
def rep(old, new, n=1):
    global t
    assert t.count(old) == n, ("Anzahl", old[:70], t.count(old))
    t = t.replace(old, new)
# 20. Tokyo Marathon am Sonntag, 7. März 2027 (Tokyo Marathon Foundation); Start der Läufer 9:10 Uhr laut Zeitplan des
# Veranstalters (Rollstühle 9:05). Ortsname für die Uhrzeiten aus den Daten: Asia/Tokyo ergäbe „Tokyo“.
data = {"tz": "Asia/Tokyo", "ort": "Tokio", "ortKurz": " Tokio", "termine": ["2027-03-07"], "start": 550}
data.update(json.load(open("data.json"))); data["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); data["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
data["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
m = re.search(r'^const D = \{.*\};$', t, re.M); t = t[:m.start()] + "const D = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";" + t[m.end():]
rep('<meta name="description" content="Steigungsprofil des Boston-Marathons: Höhe, Steigung, Pace-Modell und Karte.">',
    '<meta name="description" content="Steigungsprofil des Tokio-Marathons: Höhe, Steigung, Pace-Modell und Karte.">')
rep('<title>Steigungsprofil Boston-Marathon</title>', '<title>Steigungsprofil Tokio-Marathon</title>')
rep('<span class="eyebrow">Boston Marathon · Kurs 2026 · ', '<span class="eyebrow">Tokyo Marathon · Kurs 2026 · ')
rep('<p class="sub">Amtliches Laser-Höhenmodell (1-m-Raster) entlang der offiziellen Strecke, alle 10 m ausgewertet.</p>',
    '<p class="sub">Amtliches Laser-Höhenmodell der GSI (5-m-Raster) entlang der offiziellen Strecke, alle 10 m ausgewertet.</p>')
rep("/* Hell/Dunkel: eigene Wahl (bos-theme)", "/* Hell/Dunkel: eigene Wahl (tyo-theme)")
t = t.replace('"bos-', '"tyo-').replace('"bos.', '"tyo.')
assert "bos-" not in t and "bos." not in t, "bos übrig"
v = re.search(r"const APP_VERSION = '([\d.]+)';", t).group(1)
rep(f"const APP_VERSION = '{v}';", f"const APP_VERSION = '{VERSION}';")
rep(f'aria-label="Nach Update suchen">v{v}</button>', f'aria-label="Nach Update suchen">v{VERSION}</button>', 2)
li = lambda b, s: f"      <li><b>{b}:</b> {s}</li>\n"
a = lambda href, txt: f'<a href="{href}" target="_blank" rel="noopener">{txt}</a>'
neu = (li("Strecke", f'Linie, Kilometermarken und Getränkestellen aus der Streckenkarte des Veranstalters ({a("https://www.marathon.tokyo/en/about/course/", "Tokyo Marathon Foundation")}, Kurs 2026; die Seite für 2027 zeigt dieselbe Karte). Vom Rathaus in Shinjuku über Iidabashi, Kanda und Akihabara zum Wendepunkt Ueno-hirokoji, über Nihonbashi nach Asakusa (Kaminarimon), über die Sumida zum Wendepunkt am Tomioka Hachimangū in Monzen-nakachō, zurück über Nihonbashi und Ginza nach Shiba (Wendepunkt auf der Daiichi-Keihin) und zum Ziel auf der Gyōkō-dōri vor dem Bahnhof Tokio. Kilometer stückweise über die 42 Kilometermarken des Veranstalters geeicht (Linie 42,25 km). Getränkestellen laut derselben Karte.')
     + li("Höhe", f'Digitales Höhenmodell der GSI ({a("https://maps.gsi.go.jp/development/ichiran.html", "国土地理院, 地理院タイル")}): 5-m-Raster aus Laserscans (DEM5A), alle 10 m abgelesen; Höhen über Tokyo Peil (T.P., etwa Meeresspiegel). Quelle: 国土地理院.')
     + li("Brücken", 'Ein Geländemodell kennt keine Brücken und misst darunter Fluss oder Kanal. Wo OpenStreetMap eine Brücke kennt und das Modell darunter abfällt, ist die Fahrbahn zwischen den Rampen gerade gezogen und im Läuferblick gestrichelt; ebenso in Nishi-Shinjuku, wo die Strecke auf der oberen Straßenebene über Querstraßen läuft: <span id="bridges"></span>.')
     + li("Glättung", 'Gleitender Median über 30 m gegen Ausreißer am Straßenrand. Die Steigung ist der Höhenunterschied über das gewählte Messfenster.'))
m = re.search(r'      <li><b>Strecke:</b>.*?\n      <li><b>Glättung:</b>.*?</li>\n', t, re.S); t = t[:m.start()] + neu + t[m.end():]
alt = '      <li><b>Straßennamen:</b> © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>-Mitwirkende, über Nominatim.</li>\n'
rep(alt, '      <li><b>Straßennamen:</b> © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>-Mitwirkende; Straßen aus dem Netz unter der Linie, japanische Namen in Umschrift, Bezirke über den Adressdienst der GSI.</li>\n')
m = re.search(r"ergeben die Rohdaten \d+ m\.", t); t = t[:m.start()] + f"ergeben die Rohdaten {open('rohdaten.txt').read().strip()} m." + t[m.end():]
open(OUT + "index.html", "w", encoding="utf-8").write(t)
open(OUT + "version.json", "w").write(json.dumps({"version": VERSION}))
for f in os.listdir("../assets"):
    if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
maps = sorted(f for f in os.listdir(OUT) if f.startswith("karte-"))
sw = open(R + "boston/sw.js", encoding="utf-8").read()
assert 'const CACHE = "bos-marathon-profil";' in sw and 'k.startsWith("bos-")' in sw
sw = sw.replace('const CACHE = "bos-marathon-profil";', 'const CACHE = "tyo-marathon-profil";').replace('k.startsWith("bos-")', 'k.startsWith("tyo-")')
sw = re.sub(r"const KARTE = \[.*?\];", "const KARTE = " + json.dumps(["./" + f for f in maps]).replace('","', '", "') + ";", sw, flags=re.S)
assert "bos" not in sw
open(OUT + "sw.js", "w", encoding="utf-8").write(sw)
print("tokio/ geschrieben:", len(maps), "Kartenstücke, index.html", len(t) // 1024, "KB")
