# OSM-Wege (highway) im Umkreis von 40 m um die Linie, Punkte alle 100 m, Overpass-Spiegel maps.mail.ru, in Stücken zu 50 Punkten
# (die ganze Abfrage lief in einen 504) -> ../dl/osm_wege.json
import json, os, time, urllib.request, urllib.parse
import numpy as np
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
ss = np.append(np.arange(0, d[-1], 100.0), d[-1]); la = np.interp(ss, d, P[:, 0]); lo = np.interp(ss, d, P[:, 1])
wege = {}
for i in range(0, len(ss), 50):
    koord = ",".join(f"{a:.6f},{b:.6f}" for a, b in zip(la[i:i + 51], lo[i:i + 51]))
    q = f'[out:json][timeout:120];way["highway"](around:40,{koord});out tags geom;'
    f = f"../dl/osm_teil_{i:03d}.json"   # Zwischenstand je Stück, der Spiegel antwortet oft mit 504
    if os.path.exists(f): E = json.load(open(f))
    else:
      for att in range(20):
        try:
            req = urllib.request.Request("https://maps.mail.ru/osm/tools/overpass/api/interpreter", data=urllib.parse.urlencode({"data": q}).encode(), headers={"User-Agent": "marathon-profile-check/1.0"})
            E = json.loads(urllib.request.urlopen(req, timeout=150).read())["elements"]; json.dump(E, open(f, "w")); break
        except Exception as e: print("  Fehler", e, flush=True); time.sleep(min(60, 5 + 5 * att))
      else: raise SystemExit("Overpass nicht erreichbar")
    for w in E: wege[w["id"]] = w
    print(i, len(E), "Wege, zusammen", len(wege), flush=True)
json.dump({"elements": list(wege.values())}, open("../dl/osm_wege.json", "w"))
print(len(wege), "Wege")
