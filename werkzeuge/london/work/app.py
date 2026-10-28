# Erstausgabe der London-App aus der Boston-App: gleicher Code, eigene Daten, Texte und Speicherschlüssel (ldn-…).
# Ohne eigenes Manifest und Symbol: die Seite verweist auf ../manifest.webmanifest (eine App für alle Strecken).
# Danach wird direkt in london/index.html gearbeitet; dieses Skript ist nur die Herkunft.
import json, os, re, shutil
R = "../../../"; OUT = R + "london/"; VERSION = "1.0"
os.makedirs(OUT, exist_ok=True)
t = open(R + "boston/index.html", encoding="utf-8").read()
def rep(old, new, n=1):
    global t
    assert t.count(old) == n, ("Anzahl", old[:70], t.count(old))
    t = t.replace(old, new)
# 2027 einmalig „The Double“: Samstag 24. und Sonntag 25. April; Start der Masse 2026 um 9:35 Uhr (London Marathon Events)
data = {"tz": "Europe/London", "ortKurz": " London", "termine": ["2027-04-24", "2027-04-25"], "start": 575}
data.update(json.load(open("data.json"))); data["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); data["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
data["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
m = re.search(r'^const D = \{.*\};$', t, re.M); t = t[:m.start()] + "const D = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";" + t[m.end():]
rep('<meta name="description" content="Steigungsprofil des Boston-Marathons: Höhe, Steigung, Pace-Modell und Karte.">',
    '<meta name="description" content="Steigungsprofil des London-Marathons: Höhe, Steigung, Pace-Modell und Karte.">')
rep('<title>Steigungsprofil Boston-Marathon</title>', '<title>Steigungsprofil London-Marathon</title>')
rep('<span class="eyebrow">Boston Marathon · Kurs 2026 · ', '<span class="eyebrow">TCS London Marathon · Kurs 2026 · ')
rep('<p class="sub">Amtliches Laser-Höhenmodell (1-m-Raster) entlang der offiziellen Strecke, alle 10 m ausgewertet.</p>',
    '<p class="sub">Amtliches Laser-Höhenmodell (1-m-Raster) entlang der Strecke vom Blue Start, alle 10 m ausgewertet.</p>')
rep("/* Hell/Dunkel: eigene Wahl (bos-theme)", "/* Hell/Dunkel: eigene Wahl (ldn-theme)")
t = t.replace('"bos-', '"ldn-').replace('"bos.', '"ldn.')
assert "bos-" not in t and "bos." not in t, "bos übrig"
v = re.search(r"const APP_VERSION = '([\d.]+)';", t).group(1)
rep(f"const APP_VERSION = '{v}';", f"const APP_VERSION = '{VERSION}';")
rep(f'aria-label="Nach Update suchen">v{v}</button>', f'aria-label="Nach Update suchen">v{VERSION}</button>', 2)
li = lambda b, s: f"      <li><b>{b}:</b> {s}</li>\n"
a = lambda href, txt: f'<a href="{href}" target="_blank" rel="noopener">{txt}</a>'
neu = (li("Strecke", f'Linie „London Marathon (Blue Start)“ in OpenStreetMap ({a("https://www.openstreetmap.org/relation/13319641", "Relation 13319641")}), von der Shooters Hill Road in Blackheath über Woolwich, Greenwich, Rotherhithe, die Tower Bridge, die Isle of Dogs und Canary Wharf zurück über The Highway und das Embankment zur Mall. In Limehouse standen die Wege der Relation durcheinander, auf der Rückfahrt über The Highway fehlten welche; beides ist über das Straßennetz ergänzt. Die Linie entlang der Straßenmitte ist 1,8 % länger als die vermessene Ideallinie und gleichmäßig auf 42,195 km gebracht. Verpflegung laut Veranstalter (London Marathon Events, 2026): Lucozade Sport an Meile 7, 15, 21 und 23, Gels an Meile 14 und 19; Wasser laut Läuferguide 2026 an Meile 3, 6, 9, 12 und dann alle zwei Meilen bis 24.')
     + li("Höhe", 'LIDAR Composite DTM 1 m der Environment Agency (Höhen über Ordnance Datum Newlyn), über deren Dienst alle 10 m abgelesen. Brücken aus dem Oberflächenmodell derselben Befliegung (LIDAR Composite DSM, last return). Contains public sector information licensed under the Open Government Licence v3.0.')
     + li("Brücken", 'Ein Geländemodell kennt keine Brücken und misst darunter Wasser, Docks oder Einschnitte. Auf der Tower Bridge, den Brücken über Deptford Creek, die Docks von Rotherhithe und Canary Wharf, die Limehouse Basin und an der Commercial Road gilt deshalb die gemessene Fahrbahn aus dem Oberflächenmodell (ohne Türme, Stege und Fahrzeuge). Geschätzt und im Läuferblick gestrichelt: <span id="bridges"></span>.')
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
sw = sw.replace('const CACHE = "bos-marathon-profil";', 'const CACHE = "ldn-marathon-profil";').replace('k.startsWith("bos-")', 'k.startsWith("ldn-")')
sw = re.sub(r"const KARTE = \[.*?\];", "const KARTE = " + json.dumps(["./" + f for f in maps]).replace('","', '", "') + ";", sw, flags=re.S)
assert "bos" not in sw
open(OUT + "sw.js", "w", encoding="utf-8").write(sw)
print("london/ geschrieben:", len(maps), "Kartenstücke, index.html", len(t) // 1024, "KB")
