# Erstausgabe der Barcelona-App aus der Tokio-App (aktueller gemeinsamer Code): gleicher Code, eigene Daten, Texte und
# Speicherschlüssel (bcn-…). Ohne eigenes Manifest und Symbol: die Seite verweist auf ../manifest.webmanifest (eine App für alle
# Strecken). Danach wird direkt in barcelona/index.html gearbeitet; dieses Skript ist nur die Herkunft.
# Reihenfolge: build.py, route.py, tiles.py, dann aus werkzeuge/: tiles_z11.py barcelona, barcelona/work/app.py, tiles_rand.py barcelona 2
import json, os, re, shutil
R = "../../../"; OUT = R + "barcelona/"; VERSION = "1.0"
os.makedirs(OUT, exist_ok=True)
t = open(R + "tokio/index.html", encoding="utf-8").read()
def rep(old, new, n=1):
    global t
    assert t.count(old) == n, ("Anzahl", old[:70], t.count(old))
    t = t.replace(old, new)
# Zurich Marató Barcelona 2027 am Sonntag, 14. März 2027, Start 8:30 (Reglament 2027 des Veranstalters, Art. 1 und 3; Rollstühle
# 8:25, Zielschluss 6 h nach dem Start des letzten Läufers, etwa 16:15). Gestaffelte Starts nach erwartetem Tempo; die Zeiten 2027
# sind noch nicht veröffentlicht. Eingetragen sind die Wellen 2026 laut Startplan des Veranstalters („Mapa de sortida“, 15/03/2026,
# Anhang II der Information Técnica der RFEA zur spanischen Meisterschaft): Farbe der Startnummer, Einlass in den Block, Start,
# Zugläufer im Block. Schwarz (Elite) und Weiß (spanische Meisterschaft) starten mit Gelb. Europe/Madrid ergäbe „Madrid“: Ort aus den Daten.
WELLEN = {"q": "Wellen 2026 laut Startplan des Veranstalters, nach Farbe der Startnummer; den Block wählt man bei der Anmeldung nach "
               "erwarteter Zielzeit (Wechsel bis 1. Februar). Rollstühle 8:25. 2027 wieder Start 8:30 in Wellen, die Zeiten sind noch "
               "nicht veröffentlicht.",
          "w": [["Gelb", 510, "mit Elite · Einlass bis 8:25 · Zugläufer 2:45"], ["Rot", 520, "Einlass bis 8:35 · Zugläufer 3:00"],
                ["Blau", 530, "Einlass bis 8:45 · Zugläufer 3:15"], ["Rosa", 540, "Einlass bis 8:55 · Zugläufer 3:30"],
                ["Hellblau", 560, "Einlass bis 9:15 · Zugläufer 3:45"], ["Grün", 580, "Einlass bis 9:35 · Zugläufer 4:00"],
                ["Grau, Lila", 590, "Einlass bis 9:45 · Zugläufer 4:30"]]}
data = {"wellen": WELLEN, "tz": "Europe/Madrid", "ort": "Barcelona", "ortKurz": " Barcelona", "termine": ["2027-03-14"], "start": 510}
data.update(json.load(open("data.json"))); data["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); data["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
data["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
m = re.search(r'^const D = \{.*\};$', t, re.M); t = t[:m.start()] + "const D = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";" + t[m.end():]
rep('<meta name="description" content="Steigungsprofil des Tokio-Marathons: Höhe, Steigung, Pace-Modell und Karte.">',
    '<meta name="description" content="Steigungsprofil des Barcelona-Marathons: Höhe, Steigung, Pace-Modell und Karte.">')
rep('<title>Steigungsprofil Tokio-Marathon</title>', '<title>Steigungsprofil Barcelona-Marathon</title>')
rep('<span class="eyebrow">Tokyo Marathon · Kurs 2026 · ', '<span class="eyebrow">Zurich Marató Barcelona · Kurs 2026 · ')
rep('<h1>Tokio</h1>', '<h1>Barcelona</h1>')   # Ort als Überschrift (seit Hamburg 1.73)
rep('<p class="sub">Amtliches Laser-Höhenmodell der GSI (5-m-Raster) entlang der offiziellen Strecke, alle 10 m ausgewertet.</p>',
    '<p class="sub">' + open("sub.html", encoding="utf-8").read().strip() + '</p>')
rep("/* Hell/Dunkel: eigene Wahl (tyo-theme)", "/* Hell/Dunkel: eigene Wahl (bcn-theme)")
t = t.replace('"tyo-', '"bcn-').replace('"tyo.', '"bcn.')
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
sw = sw.replace('const CACHE = "tyo-marathon-profil";', 'const CACHE = "bcn-marathon-profil";').replace('k.startsWith("tyo-")', 'k.startsWith("bcn-")')
sw = re.sub(r"const KARTE = \[.*?\];", "const KARTE = " + json.dumps(["./" + f for f in maps]).replace('","', '", "') + ";", sw, flags=re.S)
assert "tyo" not in sw
open(OUT + "sw.js", "w", encoding="utf-8").write(sw)
print("barcelona/ geschrieben:", len(maps), "Kartenstücke, index.html", len(t) // 1024, "KB")
