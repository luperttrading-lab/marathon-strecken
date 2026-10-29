# Erstausgabe der Osaka-App aus der Tokio-App (Stand 1.22): gleicher Code, eigene Daten, Texte und Speicherschlüssel (osa-…).
# Ohne eigenes Manifest und Symbol: die Seite verweist auf ../manifest.webmanifest (eine App für alle Strecken).
# Danach wird direkt in osaka/index.html gearbeitet; dieses Skript ist nur die Herkunft.
import json, os, re, shutil
R = "../../../"; OUT = R + "osaka/"; VERSION = "1.0"
os.makedirs(OUT, exist_ok=True)
t = open(R + "tokio/index.html", encoding="utf-8").read()
def rep(old, new, n=1):
    global t
    assert t.count(old) == n, ("Anzahl", old[:70], t.count(old))
    t = t.replace(old, new)
# 15. Osaka Marathon am Sonntag, 28. Februar 2027 (Osaka Marathon Foundation). Erste Welle 9:15 Uhr laut Ausschreibung 2027,
# danach Welle 2 und 3 nacheinander; Uhrzeiten der Wellen aus der Teilnehmerinfo 2026 (9:15 / 9:30 / 9:45), für 2027 nennt die
# Ausschreibung wieder 9:15 und für den 720-Lauf, der mit der dritten Welle startet, 9:45. Asia/Tokyo ergäbe „Tokyo“: Ort aus den Daten.
data = {"wellen": {"q": "Wellen 2026 laut Teilnehmerinfo des Veranstalters (Block G: 720-Lauf). Für 2027 nennt die Ausschreibung wieder 9:15 für die erste Welle und 9:45 für die dritte; deinen Block findest du auf der Startnummer.",
                   "w": [["Welle 1", 555, "Blöcke A–C"], ["Welle 2", 570, "Blöcke D–F"], ["Welle 3", 585, "Blöcke H und J"]]},
        "tz": "Asia/Tokyo", "ort": "Osaka", "ortKurz": " Osaka", "termine": ["2027-02-28"], "start": 555}
data.update(json.load(open("data.json"))); data["route"] = json.load(open("route50.json"))
tm = json.load(open("tilemeta.json")); tm["11"] = json.load(open("tilemeta_z11.json")); data["tiles"] = {z: tm[z] for z in sorted(tm, key=int)}
data["imgNote"] = open("imgnote.html", encoding="utf-8").read().strip()
m = re.search(r'^const D = \{.*\};$', t, re.M); t = t[:m.start()] + "const D = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";" + t[m.end():]
rep('<meta name="description" content="Steigungsprofil des Tokio-Marathons: Höhe, Steigung, Pace-Modell und Karte.">',
    '<meta name="description" content="Steigungsprofil des Osaka-Marathons: Höhe, Steigung, Pace-Modell und Karte.">')
rep('<title>Steigungsprofil Tokio-Marathon</title>', '<title>Steigungsprofil Osaka-Marathon</title>')
rep('<span class="eyebrow">Tokyo Marathon · Kurs 2026 · ', '<span class="eyebrow">Osaka Marathon · Kurs 2026 · ')
rep("/* Hell/Dunkel: eigene Wahl (tyo-theme)", "/* Hell/Dunkel: eigene Wahl (osa-theme)")
t = t.replace('"tyo-', '"osa-').replace('"tyo.', '"osa.')
assert "tyo-" not in t and "tyo." not in t, "tyo übrig"
v = re.search(r"const APP_VERSION = '([\d.]+)';", t).group(1)
rep(f"const APP_VERSION = '{v}';", f"const APP_VERSION = '{VERSION}';")
# Versionsknöpfe: der feste Text wird beim Start aus APP_VERSION überschrieben; in tokio/index.html steht dort noch v1.0
alt = re.search(r'aria-label="Nach Update suchen">v([\d.]+)</button>', t).group(1)
if alt != VERSION: rep(f'aria-label="Nach Update suchen">v{alt}</button>', f'aria-label="Nach Update suchen">v{VERSION}</button>', 2)
li = lambda b, s: f"      <li><b>{b}:</b> {s}</li>\n"
a = lambda href, txt: f'<a href="{href}" target="_blank" rel="noopener">{txt}</a>'
neu = (li("Strecke", f'Linie, Kilometermarken und Getränkestellen aus der Streckenkarte des Veranstalters ({a("https://www.osaka-marathon.com/2026/info/course/", "Osaka Marathon")}, Kurs 2026; die Seite für 2027 zeigt dieselbe Strecke). Vom Präfekturamt (Ōsaka-fuchō) über den Ōkawa nach Tenma und den Tenjinbashi-suji hinunter nach Nakanoshima, über den Midō-suji nach Namba, auf der Minato-dōri hinaus bis Ichioka-motomachi (Wendepunkt), auf der Naniwa-suji nach Süden bis zur Yanagi-dōri (Wendepunkt), auf dem Matsuyamachi-suji bis Kōen-kitaguchi am Tennōji-Park (Wendepunkt), hinauf nach Uehonmachi, über Katsuyama-dōri und Imazato-suji nach Norden und auf der Shiromi-dōri in den Burgpark (Ōsaka-jō-kōen) zum Ziel. Kilometer stückweise über die Marken des Veranstalters alle 5 km und den Halbmarathon geeicht (Linie 42,69 km, entlang der Straßenmitte gezeichnet). Getränkestellen an den Kilometerangaben derselben Karte.')
     + li("Höhe", f'Digitales Höhenmodell der GSI ({a("https://maps.gsi.go.jp/development/ichiran.html", "国土地理院, 地理院タイル")}): 5-m-Raster aus Laserscans (DEM5A), alle 10 m abgelesen; Höhen über T.P., dem Bezugsniveau für ganz Japan (etwa Meeresspiegel). Quelle: 国土地理院.')
     + li("Brücken", 'Ein Geländemodell kennt keine Brücken und misst darunter Fluss oder Kanal. Wo OpenStreetMap eine Brücke kennt und das Modell darunter abfällt, ist die Fahrbahn zwischen den Rampen gerade gezogen und im Läuferblick gestrichelt, ebenso an der Naniwa-suji über der tiefer gelegten Nationalstraße 43: <span id="bridges"></span>. Die Hochstraßen des Hanshin Expressway über vielen Straßen der Strecke zählen nicht, gelaufen wird darunter. Die Unterführung des Shiromi-dōri unter der Ringbahn (km 41,2) misst das Modell im offenen Einschnitt selbst.')
     + li("Glättung", 'Gleitender Median über 30 m gegen Ausreißer am Straßenrand. Die Steigung ist der Höhenunterschied über das gewählte Messfenster.'))
m = re.search(r'      <li><b>Strecke:</b>.*?\n      <li><b>Glättung:</b>.*?</li>\n', t, re.S); t = t[:m.start()] + neu + t[m.end():]
# Straßennamen: gleiche Herkunft wie in Tokio (OSM-Netz unter der Linie, Umschrift, Bezirke über die GSI), Text bleibt
assert '      <li><b>Straßennamen:</b> © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>-Mitwirkende; Straßen aus dem Netz unter der Linie, japanische Namen in Umschrift, Bezirke über den Adressdienst der GSI.</li>\n' in t
m = re.search(r"ergeben die Rohdaten \d+ m\.", t); t = t[:m.start()] + f"ergeben die Rohdaten {open('rohdaten.txt').read().strip()} m." + t[m.end():]
open(OUT + "index.html", "w", encoding="utf-8").write(t)
open(OUT + "version.json", "w").write(json.dumps({"version": VERSION}))
for f in os.listdir("../assets"):
    if f.startswith("karte-"): shutil.copy("../assets/" + f, OUT + f)
maps = sorted(f for f in os.listdir(OUT) if f.startswith("karte-"))
sw = open(R + "tokio/sw.js", encoding="utf-8").read()
assert 'const CACHE = "tyo-marathon-profil";' in sw and 'k.startsWith("tyo-")' in sw
sw = sw.replace('const CACHE = "tyo-marathon-profil";', 'const CACHE = "osa-marathon-profil";').replace('k.startsWith("tyo-")', 'k.startsWith("osa-")')
sw = re.sub(r"const KARTE = \[.*?\];", "const KARTE = " + json.dumps(["./" + f for f in maps]).replace('","', '", "') + ";", sw, flags=re.S)
assert "tyo" not in sw
open(OUT + "sw.js", "w", encoding="utf-8").write(sw)
print("osaka/ geschrieben:", len(maps), "Kartenstücke, index.html", len(t) // 1024, "KB")
