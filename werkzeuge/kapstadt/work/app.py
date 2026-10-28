# Erstausgabe der Kapstadt-App aus der Boston-App: gleicher Code, eigene Daten, Texte und Speicherschlüssel (cpt-…).
# Ohne eigenes Manifest und Symbol: die Seite verweist auf ../manifest.webmanifest (eine App für alle Strecken).
# Danach wird direkt in kapstadt/index.html gearbeitet; dieses Skript ist nur die Herkunft.
import json, os, re, shutil
R = "../../../"; OUT = R + "kapstadt/"; VERSION = "1.0"
os.makedirs(OUT, exist_ok=True)
t = open(R + "boston/index.html", encoding="utf-8").read()
def rep(old, new, n=1):
    global t
    assert t.count(old) == n, ("Anzahl", old[:70], t.count(old))
    t = t.replace(old, new)
# Sanlam Cape Town Marathon am Sonntag, 23. Mai 2027, erste Ausgabe als Abbott World Marathon Major. Start 2026: Elite 8:00 Uhr
# (Rollstühle 7:50, Wellen bis 9:06). Ortsname aus den Daten: Africa/Johannesburg ergäbe „Johannesburg“.
data = {"tz": "Africa/Johannesburg", "ort": "Kapstadt", "ortKurz": " Kapstadt", "termine": ["2027-05-23"], "start": 480}
data.update(json.load(open("data.json"))); data["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); data["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
data["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
m = re.search(r'^const D = \{.*\};$', t, re.M); t = t[:m.start()] + "const D = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";" + t[m.end():]
rep('<meta name="description" content="Steigungsprofil des Boston-Marathons: Höhe, Steigung, Pace-Modell und Karte.">',
    '<meta name="description" content="Steigungsprofil des Kapstadt-Marathons: Höhe, Steigung, Pace-Modell und Karte.">')
rep('<title>Steigungsprofil Boston-Marathon</title>', '<title>Steigungsprofil Kapstadt-Marathon</title>')
rep('<span class="eyebrow">Boston Marathon · Kurs 2026 · ', '<span class="eyebrow">Sanlam Cape Town Marathon · Kurs 2026 · ')
rep('<p class="sub">Amtliches Laser-Höhenmodell (1-m-Raster) entlang der offiziellen Strecke, alle 10 m ausgewertet.</p>',
    '<p class="sub">Laser-Höhenmodell der Stadt Kapstadt (5-m-Raster) entlang der offiziellen Strecke, alle 10 m ausgewertet; Hochstraßen gemessen.</p>')
rep("/* Hell/Dunkel: eigene Wahl (bos-theme)", "/* Hell/Dunkel: eigene Wahl (cpt-theme)")
t = t.replace('"bos-', '"cpt-').replace('"bos.', '"cpt.')
assert "bos-" not in t and "bos." not in t, "bos übrig"
v = re.search(r"const APP_VERSION = '([\d.]+)';", t).group(1)
rep(f"const APP_VERSION = '{v}';", f"const APP_VERSION = '{VERSION}';")
rep(f'aria-label="Nach Update suchen">v{v}</button>', f'aria-label="Nach Update suchen">v{VERSION}</button>', 2)
li = lambda b, s: f"      <li><b>{b}:</b> {s}</li>\n"
a = lambda href, txt: f'<a href="{href}" target="_blank" rel="noopener">{txt}</a>'
neu = (li("Strecke", f'Linie von {a("https://www.goandrace.com/en/running-events/sanlam-cape-town-marathon-2025.php", "goandrace.com")} (für 2025 veröffentlicht; das Rennen fiel am Renntag wegen Sturm aus), auf das Straßennetz von OpenStreetMap gelegt und an der {a("https://capetownmarathon.com/marathon/", "Streckenkarte 2026 des Veranstalters")} geprüft: Die Karte deckt sich mit der Linie überall auf 80 m, alle zehn Kontrollpunkte liegen auf denselben Straßen. Vom DHL-Stadion in Green Point über die Hochstraßen Helen Suzman und Nelson Mandela Boulevard, Woodstock, Salt River und Observatory die Main Road hinauf nach Claremont, über Rondebosch Common und den Liesbeek Parkway zurück in die Innenstadt (Company’s Garden, Long Street) und an der Küste von Sea Point zurück nach Green Point. Die Linie entlang der Straßenmitte ist 1,8 % länger als die vermessene Ideallinie und gleichmäßig auf 42,195 km gebracht. Getränkestellen: die 15 der Karte 2026, Lage auf etwa 100 m genau.')
     + li("Höhe", f'Ground Level Map 2019 der Stadt Kapstadt, 5-m-Raster aus Laserscans (Geländemodell, ±0,3 m, Höhen über dem südafrikanischen Landeshöhennetz), alle 10 m über den {a("https://cityimg.capetown.gov.za/erdas-iws/ogc/wms/GeoSpatial%20Datasets?service=WMS&request=GetCapabilities", "Kartendienst der Stadt")} abgefragt. © City of Cape Town.')
     + li("Hochstraßen", 'Ein Geländemodell kennt keine Brücken und misst darunter den Boden. Auf den Hochstraßen (Helen Suzman Boulevard, Nelson Mandela Boulevard) und Brücken ist die Fahrbahn deshalb gemessen: Gelände plus Höhe über Grund aus den Laserscans 2025 der Stadt (Height Map 1 m), auf den Rampen das Geländemodell 2025. Übrige kurze Stücke geschätzt und im Läuferblick gestrichelt: <span id="bridges"></span>.')
     + li("Glättung", 'Gleitender Median über 30 m gegen Ausreißer am Straßenrand. Die Steigung ist der Höhenunterschied über das gewählte Messfenster.'))
m = re.search(r'      <li><b>Strecke:</b>.*?\n      <li><b>Glättung:</b>.*?</li>\n', t, re.S); t = t[:m.start()] + neu + t[m.end():]
alt = '      <li><b>Straßennamen:</b> © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>-Mitwirkende, über Nominatim.</li>\n'
rep(alt, '      <li><b>Straßennamen:</b> © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>-Mitwirkende; Straßen aus dem Netz unter der Linie, Stadtteile aus OSM (Auszug von BBBike).</li>\n')
m = re.search(r"ergeben die Rohdaten \d+ m\.", t); t = t[:m.start()] + f"ergeben die Rohdaten {open('rohdaten.txt').read().strip()} m." + t[m.end():]
open(OUT + "index.html", "w", encoding="utf-8").write(t)
open(OUT + "version.json", "w").write(json.dumps({"version": VERSION}))
for f in os.listdir("../assets"):
    if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
maps = sorted(f for f in os.listdir(OUT) if f.startswith("karte-"))
sw = open(R + "boston/sw.js", encoding="utf-8").read()
assert 'const CACHE = "bos-marathon-profil";' in sw and 'k.startsWith("bos-")' in sw
sw = sw.replace('const CACHE = "bos-marathon-profil";', 'const CACHE = "cpt-marathon-profil";').replace('k.startsWith("bos-")', 'k.startsWith("cpt-")')
sw = re.sub(r"const KARTE = \[.*?\];", "const KARTE = " + json.dumps(["./" + f for f in maps]).replace('","', '", "') + ";", sw, flags=re.S)
assert "bos" not in sw
open(OUT + "sw.js", "w", encoding="utf-8").write(sw)
print("kapstadt/ geschrieben:", len(maps), "Kartenstücke, index.html", len(t) // 1024, "KB")
