# OSM-Wege (highway) im Umkreis von 40 m um die Linie, Punkte alle 100 m, Overpass-Spiegel maps.mail.ru -> ../dl/osm_wege.json
import json, urllib.request, urllib.parse
import numpy as np
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
ss = np.arange(0, d[-1], 100.0); la = np.interp(ss, d, P[:, 0]); lo = np.interp(ss, d, P[:, 1])
koord = ",".join(f"{a:.6f},{b:.6f}" for a, b in zip(la, lo))
q = f'[out:json][timeout:170];way["highway"](around:40,{koord});out tags geom;'
req = urllib.request.Request("https://maps.mail.ru/osm/tools/overpass/api/interpreter", data=urllib.parse.urlencode({"data": q}).encode(), headers={"User-Agent": "marathon-profile-check/1.0"})
r = urllib.request.urlopen(req, timeout=200).read()
open("../dl/osm_wege.json", "wb").write(r)
E = json.loads(r)["elements"]; print(len(E), "Wege,", len(r) // 1024, "KB")
