# Erstausgabe der App für den Maratón de la Ciudad de México aus der Tokio-App (Stand 1.22, aktueller gemeinsamer Code): gleicher
# Code, eigene Daten, Texte und Speicherschlüssel (mex-…). Ohne eigenes Manifest und Symbol: die Seite verweist auf
# ../manifest.webmanifest (eine App für alle Strecken). Danach wird direkt in mexiko/index.html gearbeitet; dieses Skript ist nur die
# Herkunft. Reihenfolge: build.py, route.py, tiles.py, dann aus werkzeuge/: tiles_z11.py mexiko, work/app.py, tiles_rand.py mexiko 2
import json, os, re, shutil
R = "../../../"; OUT = R + "mexiko/"; VERSION = "1.0"
os.makedirs(OUT, exist_ok=True)
t = open(R + "tokio/index.html", encoding="utf-8").read()
def rep(old, new, n=1):
    global t
    assert t.count(old) == n, ("Anzahl", old[:70], t.count(old))
    t = t.replace(old, new)
# XLIII. Maratón de la Ciudad de México Telcel am Sonntag, 30. August 2026 (Ausschreibung des Veranstalters auf Race Roster und
# Presse); seit Jahren am letzten Sonntag im August, 2027 noch nicht veröffentlicht: 29.08.2027 unbestätigt. Startzeiten laut
# Ausschreibung 2026: Rollstühle und Sehbehinderte 5:45, Elite Frauen 5:50, Elite Männer und Block A 6:00, Block B 6:15, Block C 6:30.
# America/Mexico_City ergäbe „Mexico City“: Ort aus den Daten.
WELLEN = {"q": "Startzeiten 2026 laut Ausschreibung des Veranstalters (Rollstühle und Sehbehinderte 5:45, Elite Frauen 5:50, "
               "Elite Männer mit Block A). Den Block weist die Anmeldung zu; für 2027 noch nicht veröffentlicht.",
          "w": [["Block A", 360, "mit Elite Männer"], ["Block B", 375, ""], ["Block C", 390, ""]]}
data = {"wellen": WELLEN, "tz": "America/Mexico_City", "ort": "Mexiko-Stadt", "ortKurz": " Mexiko-Stadt",
        "termine": ["2026-08-30", "2027-08-29?"], "start": 360}
data.update(json.load(open("data.json"))); data["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); data["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
data["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
m = re.search(r'^const D = \{.*\};$', t, re.M); t = t[:m.start()] + "const D = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";" + t[m.end():]
rep('<meta name="description" content="Steigungsprofil des Tokio-Marathons: Höhe, Steigung, Pace-Modell und Karte.">',
    '<meta name="description" content="Steigungsprofil des Mexiko-Stadt-Marathons: Höhe, Steigung, Pace-Modell und Karte.">')
rep('<title>Steigungsprofil Tokio-Marathon</title>', '<title>Steigungsprofil Mexiko-Stadt-Marathon</title>')
rep('<span class="eyebrow">Tokyo Marathon · Kurs 2026 · ', '<span class="eyebrow">Maratón de la Ciudad de México Telcel · Kurs 2026 · ')
rep('<h1>Tokio</h1>', '<h1>Mexiko-Stadt</h1>')   # Ort als Überschrift (seit Hamburg 1.73)
rep('<p class="sub">Amtliches Laser-Höhenmodell der GSI (5-m-Raster) entlang der offiziellen Strecke, alle 10 m ausgewertet.</p>',
    '<p class="sub">' + open("sub.html", encoding="utf-8").read().strip() + '</p>')
rep("/* Hell/Dunkel: eigene Wahl (tyo-theme)", "/* Hell/Dunkel: eigene Wahl (mex-theme)")
t = t.replace('"tyo-', '"mex-').replace('"tyo.', '"mex.')
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
sw = sw.replace('const CACHE = "tyo-marathon-profil";', 'const CACHE = "mex-marathon-profil";').replace('k.startsWith("tyo-")', 'k.startsWith("mex-")')
sw = re.sub(r"const KARTE = \[.*?\];", "const KARTE = " + json.dumps(["./" + f for f in maps]).replace('","', '", "') + ";", sw, flags=re.S)
assert "tyo" not in sw
open(OUT + "sw.js", "w", encoding="utf-8").write(sw)
print("mexiko/ geschrieben:", len(maps), "Kartenstücke, index.html", len(t) // 1024, "KB, D.lage", data["lage"])
