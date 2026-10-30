# Erstausgabe der App für den Vienna City Marathon aus der Tokio-App (aktueller gemeinsamer Code): gleicher Code, eigene Daten,
# Texte und Speicherschlüssel (vie-…). Ohne eigenes Manifest und Symbol: die Seite verweist auf ../manifest.webmanifest (eine App
# für alle Strecken). Danach wird direkt in wien/index.html gearbeitet; dieses Skript ist nur die Herkunft.
# Reihenfolge: parse.py, vergleich.py (nur Abgleich), osm.py, strassen.py, dgm.py, als.py (nur Abgleich), dsm.py, clean.py,
# orte.py, build.py, gegenprobe.py und planprofil.py (nur Abgleich), route.py, tiles.py, dann aus werkzeuge/: tiles_z11.py wien,
# work/app.py, tiles_rand.py wien 2
import json, os, re, shutil
R = "../../../"; OUT = R + "wien/"; VERSION = "1.6"
os.makedirs(OUT, exist_ok=True)
t = open(R + "tokio/index.html", encoding="utf-8").read()
def rep(old, new, n=1):
    global t
    assert t.count(old) == n, ("Anzahl", old[:70], t.count(old))
    t = t.replace(old, new)
# 43. Vienna City Marathon am Sonntag, 19. April 2026 (gelaufen); 44. am Sonntag, 18. April 2027 laut Veranstalter (Seite
# „Marathon“: Start ab 9:00 in mehreren Wellen, Wagramer Straße/Reichsbrücke, Zielschluss 15:30, Ziel Ringstraße/Burgtheater).
# Startblöcke 2026 laut Seite „Dein Start am VCM-Sonntag“ und Startblockplan 2026; für 2027 noch nicht veröffentlicht.
WELLEN = {"q": "Sechs Startblöcke 2026 laut Veranstalter: Marathon, Halbmarathon und Staffel starten gemeinsam, eingeteilt nach der "
               "angegebenen Zielzeit (Marathon unter 3:40 nur mit Nachweis); Block und Farbe stehen auf der Startnummer. Elite und "
               "Superfast Runners starten mit Block A, der Startvorgang endet um 9:40. Für 2027 noch nicht veröffentlicht "
               "(„ab 9:00 Uhr in mehreren Wellen“).",
          "w": [["Block A", 540, "Orange · mit Elite und Superfast Runners"], ["Block B", 546, "Blau"], ["Block C", 553, "Schwarz"],
                ["Block D", 559, "Rot"], ["Block E", 566, "Lila"], ["Block F", 573, "Gelb"]]}
data = {"wellen": WELLEN, "tz": "Europe/Vienna", "ort": "Wien", "ortKurz": " Wien", "termine": ["2026-04-19", "2027-04-18"], "start": 540}
data.update(json.load(open("data.json"))); data["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); data["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
data["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
m = re.search(r'^const D = \{.*\};$', t, re.M); t = t[:m.start()] + "const D = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";" + t[m.end():]
rep('<meta name="description" content="Steigungsprofil des Tokio-Marathons: Höhe, Steigung, Pace-Modell und Karte.">',
    '<meta name="description" content="Steigungsprofil des Vienna City Marathons: Höhe, Steigung, Pace-Modell und Karte.">')
rep('<title>Steigungsprofil Tokio-Marathon</title>', '<title>Steigungsprofil Vienna City Marathon</title>')
rep('<span class="eyebrow">Tokyo Marathon · Kurs 2026 · ', '<span class="eyebrow">Vienna City Marathon · Kurs 2026 · ')
rep('<h1>Tokio</h1>', '<h1>Wien</h1>')   # Ort als Überschrift (seit Hamburg 1.73)
rep('<p class="sub">Amtliches Laser-Höhenmodell der GSI (5-m-Raster) entlang der offiziellen Strecke, alle 10 m ausgewertet.</p>',
    '<p class="sub">' + open("sub.html", encoding="utf-8").read().strip() + '</p>')
rep("/* Hell/Dunkel: eigene Wahl (tyo-theme)", "/* Hell/Dunkel: eigene Wahl (vie-theme)")
t = t.replace('"tyo-', '"vie-').replace('"tyo.', '"vie.')
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
sw = sw.replace('const CACHE = "tyo-marathon-profil";', 'const CACHE = "vie-marathon-profil";').replace('k.startsWith("tyo-")', 'k.startsWith("vie-")')
sw = re.sub(r"const KARTE = \[.*?\];", "const KARTE = " + json.dumps(["./" + f for f in maps]).replace('","', '", "') + ";", sw, flags=re.S)
assert "tyo" not in sw
open(OUT + "sw.js", "w", encoding="utf-8").write(sw)
assert "lage" not in data and "mauer" not in data
print("wien/ geschrieben:", len(maps), "Kartenstücke, index.html", len(t) // 1024, "KB")
