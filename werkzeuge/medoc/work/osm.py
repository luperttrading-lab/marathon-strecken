# OSM-Wege (highway, railway) im Rechteck um die Strecke (45,135–45,275 N, 0,805–0,725 W) über Overpass. overpass-api.de brach am
# 30.10.2026 die Verbindung ab, maps.mail.ru antwortete 504, overpass.kumi.systems lieferte. -> ../dl/osm_wege.json
import json, os, subprocess
Q = '[out:json][timeout:180];(way["highway"](45.135,-0.805,45.275,-0.725);way["railway"](45.135,-0.805,45.275,-0.725););out tags geom;'
f = "../dl/osm_bbox.json"
if not os.path.exists(f):
    for u in ("https://overpass-api.de/api/interpreter", "https://maps.mail.ru/osm/tools/overpass/api/interpreter", "https://overpass.kumi.systems/api/interpreter"):
        r = subprocess.run(["curl", "-sS", "-A", "marathon-profile-check/1.0", "--data-urlencode", "data=" + Q, "-o", f, u])
        try: json.load(open(f)); break
        except Exception: continue
E = json.load(open(f))["elements"]
json.dump({"elements": E}, open("../dl/osm_wege.json", "w"))
print(len(E), "Wege")
