# Erstausgabe der Paris-App (Kurs 2025) aus der Boston-App: gleicher Code, eigene Daten, Texte und Speicherschlüssel (par-…).
# Ohne eigenes Manifest und Symbol: die Seite verweist auf ../manifest.webmanifest (eine App für alle Strecken).
# Danach wird direkt in london/index.html gearbeitet; dieses Skript ist nur die Herkunft.
import json, os, re, shutil
R = "../../../"; OUT = R + "paris/"; VERSION = "1.0"
os.makedirs(OUT, exist_ok=True)
t = open(R + "boston/index.html", encoding="utf-8").read()
def rep(old, new, n=1):
    global t
    assert t.count(old) == n, ("Anzahl", old[:70], t.count(old))
    t = t.replace(old, new)
# 50. Ausgabe am Sonntag, 4. April 2027 („ASICS Marathon de Paris“, neuer Veranstalter Cadence Running United); die Strecke 2027
# wird erst Anfang 2027 vorgestellt, die App zeigt den Kurs 2025. Start 2025 um 8:00 Uhr (Elite und vordere Startblöcke).
data = {"tz": "Europe/Paris", "ortKurz": " Paris", "termine": ["2027-04-04"], "start": 480}
data.update(json.load(open("data.json"))); data["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); data["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
data["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
m = re.search(r'^const D = \{.*\};$', t, re.M); t = t[:m.start()] + "const D = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";" + t[m.end():]
rep('<meta name="description" content="Steigungsprofil des Boston-Marathons: Höhe, Steigung, Pace-Modell und Karte.">',
    '<meta name="description" content="Steigungsprofil des Paris-Marathons (Kurs 2025): Höhe, Steigung, Pace-Modell und Karte.">')
rep('<title>Steigungsprofil Boston-Marathon</title>', '<title>Steigungsprofil Paris-Marathon</title>')
rep('<span class="eyebrow">Boston Marathon · Kurs 2026 · ', '<span class="eyebrow">Marathon de Paris · Kurs 2025 · ')
rep('<p class="sub">Amtliches Laser-Höhenmodell (1-m-Raster) entlang der offiziellen Strecke, alle 10 m ausgewertet.</p>',
    '<p class="sub">Amtliches Höhenmodell der IGN (1-m-Raster) entlang der Strecke von 2025, alle 10 m ausgewertet. Die Strecke 2027 stellt der neue Veranstalter erst Anfang 2027 vor.</p>')
rep("/* Hell/Dunkel: eigene Wahl (bos-theme)", "/* Hell/Dunkel: eigene Wahl (par-theme)")
t = t.replace('"bos-', '"par-').replace('"bos.', '"par.')
assert "bos-" not in t and "bos." not in t, "bos übrig"
v = re.search(r"const APP_VERSION = '([\d.]+)';", t).group(1)
rep(f"const APP_VERSION = '{v}';", f"const APP_VERSION = '{VERSION}';")
rep(f'aria-label="Nach Update suchen">v{v}</button>', f'aria-label="Nach Update suchen">v{VERSION}</button>', 2)
li = lambda b, s: f"      <li><b>{b}:</b> {s}</li>\n"
a = lambda href, txt: f'<a href="{href}" target="_blank" rel="noopener">{txt}</a>'
neu = (li("Strecke", f'Kurs 2025 (Schneider Electric Marathon de Paris, 13. April 2025): Linie von {a("https://www.goandrace.com/en/running-events/schneider-electric-marathon-de-paris-2025.php", "goandrace.com")}, auf das Straßennetz von OpenStreetMap gelegt. Von den Champs-Élysées über die Rue de Rivoli und die Bastille in den Bois de Vincennes, zurück über die Bastille, unten an der Seine entlang (Tunnel des Tuileries, Voie Georges-Pompidou), am Eiffelturm vorbei durch den Bois de Boulogne zur Avenue Foch. Der Kurs 2024 war zu gut 90 % gleich. Die Linie entlang der Straßenmitte ist 0,5 % länger als die vermessene Ideallinie und gleichmäßig auf 42,195 km gebracht. Verpflegung alle 5 km (Wasser, Iso, Bananen, Trockenobst), Lage nach Kilometer, nicht nach Plan des Veranstalters.')
     + li("Höhe", f'RGE ALTI 1 m der IGN (Laser und Bildkorrelation, Höhen über NGF-IGN69, etwa Meeresspiegel), über den Höhendienst der {a("https://geoservices.ign.fr/", "Géoplateforme")} alle 10 m abgelesen. Licence Ouverte (Etalab).')
     + li("Tunnel und Brücken", 'Ein Geländemodell misst im Tunnel den Quai oder Platz darüber und auf Brücken den Graben darunter. Dort ist die Höhe zwischen den Enden gerade gezogen und im Läuferblick gestrichelt: <span id="bridges"></span>.')
     + li("Glättung", 'Gleitender Median über 30 m gegen Ausreißer am Straßenrand. Die Steigung ist der Höhenunterschied über das gewählte Messfenster.'))
m = re.search(r'      <li><b>Strecke:</b>.*?\n      <li><b>Glättung:</b>.*?</li>\n', t, re.S); t = t[:m.start()] + neu + t[m.end():]
alt = '      <li><b>Straßennamen:</b> © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>-Mitwirkende, über Nominatim.</li>\n'
rep(alt, '      <li><b>Straßennamen:</b> © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>-Mitwirkende; Straßen aus dem Netz unter der Linie, Arrondissements über Nominatim.</li>\n')
m = re.search(r"ergeben die Rohdaten \d+ m\.", t); t = t[:m.start()] + f"ergeben die Rohdaten {open('rohdaten.txt').read().strip()} m." + t[m.end():]
open(OUT + "index.html", "w", encoding="utf-8").write(t)
open(OUT + "version.json", "w").write(json.dumps({"version": VERSION}))
for f in os.listdir("../assets"):
    if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
maps = sorted(f for f in os.listdir(OUT) if f.startswith("karte-"))
sw = open(R + "boston/sw.js", encoding="utf-8").read()
assert 'const CACHE = "bos-marathon-profil";' in sw and 'k.startsWith("bos-")' in sw
sw = sw.replace('const CACHE = "bos-marathon-profil";', 'const CACHE = "par-marathon-profil";').replace('k.startsWith("bos-")', 'k.startsWith("par-")')
sw = re.sub(r"const KARTE = \[.*?\];", "const KARTE = " + json.dumps(["./" + f for f in maps]).replace('","', '", "') + ";", sw, flags=re.S)
assert "bos" not in sw
open(OUT + "sw.js", "w", encoding="utf-8").write(sw)
print("paris/ geschrieben:", len(maps), "Kartenstücke, index.html", len(t) // 1024, "KB")
