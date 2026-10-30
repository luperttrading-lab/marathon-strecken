# OSM-Wege (highway, railway) und Gewässer im Umkreis von 40 m um die Linie, Punkte alle 100 m, Overpass-Spiegel maps.mail.ru
# in Stücken zu 50 Punkten (overpass-api.de brach am 30.10.2026 die Verbindung ab, kumi.systems und private.coffee antworteten
# nicht) -> ../dl/osm_wege.json, ../dl/osm_wasser.json
import json, os, time, urllib.request, urllib.parse
import numpy as np
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
ss = np.append(np.arange(0, d[-1], 100.0), d[-1]); la = np.interp(ss, d, P[:, 0]); lo = np.interp(ss, d, P[:, 1])
URL = "https://maps.mail.ru/osm/tools/overpass/api/interpreter"
def frage(q, f):
    if os.path.exists(f): return json.load(open(f))
    for att in range(20):
        try:
            req = urllib.request.Request(URL, data=urllib.parse.urlencode({"data": q}).encode(), headers={"User-Agent": "marathon-profile-check/1.0"})
            E = json.loads(urllib.request.urlopen(req, timeout=180).read())["elements"]; json.dump(E, open(f, "w")); return E
        except Exception as e: print("  Fehler", e, flush=True); time.sleep(min(60, 5 + 5 * att))
    raise SystemExit("Overpass nicht erreichbar")
wege, wasser = {}, {}
for i in range(0, len(ss), 50):
    koord = ",".join(f"{a:.6f},{b:.6f}" for a, b in zip(la[i:i + 51], lo[i:i + 51]))
    E = frage(f'[out:json][timeout:150];(way["highway"](around:40,{koord});way["railway"](around:40,{koord}););out tags geom;', f"../dl/osm_teil_{i:03d}.json")
    for w in E: wege[w["id"]] = w
    E = frage(f'[out:json][timeout:150];(way["natural"="water"](around:60,{koord});way["waterway"="riverbank"](around:60,{koord});'
              f'relation["natural"="water"](around:60,{koord});way["water"](around:60,{koord}););out tags geom;', f"../dl/osm_wasser_{i:03d}.json")
    for w in E: wasser[(w["type"], w["id"])] = w
    print(i, len(wege), "Wege,", len(wasser), "Gewässer", flush=True)
json.dump({"elements": list(wege.values())}, open("../dl/osm_wege.json", "w"))
json.dump({"elements": list(wasser.values())}, open("../dl/osm_wasser.json", "w"))
print(len(wege), "Wege,", len(wasser), "Gewässer")
