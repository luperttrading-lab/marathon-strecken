# Erstausgabe der App für den Athens Marathon. The Authentic aus der Tokio-App (aktueller gemeinsamer Code): gleicher Code, eigene
# Daten, Texte und Speicherschlüssel (ath-…). Ohne eigenes Manifest und Symbol: die Seite verweist auf ../manifest.webmanifest (eine App
# für alle Strecken). Danach wird direkt in athen/index.html gearbeitet; dieses Skript ist nur die Herkunft.
# Reihenfolge: parse.py, osm.py, linie.py, marken.py, fabdem.py, dgm.py, planprofil.py, strassen.py, orte.py, clean.py, build.py,
# route.py, tiles.py, dann aus werkzeuge/: tiles_z11.py athen, athen/work/app.py, tiles_rand.py athen 2
import json, os, re, shutil
R = "../../../"; OUT = R + "athen/"
VERSION = json.load(open(R + "version.json"))["version"]   # eine Nummer für die ganze App (seit 2.0), setzt werkzeuge/kern/kern.py
os.makedirs(OUT, exist_ok=True)
t = open(R + "tokio/index.html", encoding="utf-8").read()
def rep(old, new, n=1):
    global t
    assert t.count(old) == n, ("Anzahl", old[:70], t.count(old))
    t = t.replace(old, new)
# 43. Athens Marathon. The Authentic am Sonntag, 8. November 2026 (Seite „Marathon Race“ und Wochenprogramm des Veranstalters SEGAS,
# athensauthenticmarathon.gr). Start 8:30 in Marathonas in 15 Blöcken plus einem Block für Läufer mit Behinderung, Zeitlimit 8 h, alle
# im Ziel bis 18:15. Blockzeiten laut Seite „Marathon Race“ (Tabelle „Starting blocks“, „indicative“, zwei Wochen vor dem Lauf
# festgelegt) und gleichlautend in der Mitteilung „What’s New at the 2026 Athens Authentic Marathon: Race Schedule and Start Times“
# vom 16.10.2026. 2027 ist nicht veröffentlicht; der Lauf ist seit Jahren am zweiten Sonntag im November, daher 2027-11-14?.
# Europe/Athens ergäbe „Athens“: Ort aus den Daten.
WELLEN = {"q": "Startzeiten 2026 laut Veranstalter (Seite „Marathon Race“ und Mitteilung vom 16.10.2026): 15 Blöcke nach der Bestzeit "
               "der letzten drei Jahre, der Block steht auf der Startnummer; dazu ein Block für Läufer mit Behinderung. Die Blöcke 11–15 "
               "fahren als zweite Welle später zum Start. Zeitlimit 8 Stunden, alle im Ziel bis 18:15.",
          "w": [["Block 1", 510, "Elite, Meisterschaft, schnellste 600"], ["Block 2", 512, "nächste 1500"], ["Block 3", 515, "nächste 1500"],
                ["Block 4", 519, "nächste 1500"], ["Block 5", 524, "nächste 1500"], ["Block 6", 529, "nächste 1500"],
                ["Sonderblock", 534, "Läufer mit Behinderung"], ["Block 7", 540, "nächste 1700"], ["Block 8", 546, "nächste 1800"],
                ["Block 9", 552, "nächste 1800"], ["Block 10", 558, "nächste 1800"], ["Block 11", 585, "2. Welle · nächste 1800"],
                ["Block 12", 591, "2. Welle · nächste 1800"], ["Block 13", 597, "2. Welle · über 6 h oder ohne Zeit"],
                ["Block 14", 603, "2. Welle · über 6 h oder ohne Zeit"], ["Block 15", 609, "2. Welle · ohne Zeit"]]}
data = {"wellen": WELLEN, "tz": "Europe/Athens", "ort": "Athen", "ortKurz": " Athen", "termine": ["2026-11-08", "2027-11-14?"], "start": 510}
data.update(json.load(open("data.json"))); data["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); data["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
data["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
m = re.search(r'^const D = \{.*\};$', t, re.M); t = t[:m.start()] + "const D = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";" + t[m.end():]
rep('<meta name="description" content="Steigungsprofil des Tokio-Marathons: Höhe, Steigung, Pace-Modell und Karte.">',
    '<meta name="description" content="Steigungsprofil des Athen-Marathons: Höhe, Steigung, Pace-Modell und Karte.">')
rep('<title>Steigungsprofil Tokio-Marathon</title>', '<title>Steigungsprofil Athen-Marathon</title>')
rep('<span class="eyebrow">Tokyo Marathon · Kurs 2026 · ', '<span class="eyebrow">Athens Marathon. The Authentic · Kurs 2026 · ')
rep('<h1>Tokio</h1>', '<h1>Athen</h1>')   # Ort als Überschrift (seit Hamburg 1.73)
rep('<p class="sub">Amtliches Laser-Höhenmodell der GSI (5-m-Raster) entlang der offiziellen Strecke, alle 10 m ausgewertet.</p>',
    '<p class="sub">' + open("sub.html", encoding="utf-8").read().strip() + '</p>')
rep("/* Hell/Dunkel: eigene Wahl (tyo-theme)", "/* Hell/Dunkel: eigene Wahl (ath-theme)")
t = t.replace('"tyo-', '"ath-').replace('"tyo.', '"ath.')
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
sw = sw.replace('const CACHE = "tyo-marathon-profil";', 'const CACHE = "ath-marathon-profil";').replace('k.startsWith("tyo-")', 'k.startsWith("ath-")')
sw = re.sub(r"const KARTE = \[.*?\];", "const KARTE = " + json.dumps(["./" + f for f in maps]).replace('","', '", "') + ";", sw, flags=re.S)
assert "tyo" not in sw
open(OUT + "sw.js", "w", encoding="utf-8").write(sw)
print("athen/ geschrieben:", len(maps), "Kartenstücke, index.html", len(t) // 1024, "KB")
