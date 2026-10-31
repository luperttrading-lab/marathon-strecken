# Geografische Namen entlang der Linie aus swissNAMES3D (swisstopo, geo.admin.ch „identify“, Ebene ch.swisstopo.swissnames3d), je Kachel
# 1 × 1 km in LV95, die die Linie bis 150 m berührt -> ../dl/orte/names3d_<E>_<N>.json (einmal abgerufen, höchstens 200 je Abfrage;
# volle Kacheln in vier Teile geteilt). Ausgewertet in orte.py.
import json, os, time, urllib.parse, urllib.request
import numpy as np
from pyproj import Transformer
T = Transformer.from_crs(4326, 2056, always_xy=True)
g = json.load(open("gpx2026.json")); P = np.array(g["pts"]); d = np.array(g["d"])
ss = np.arange(0, d[-1], 25.0); x, y = T.transform(np.interp(ss, d, P[:, 1]), np.interp(ss, d, P[:, 0]))
K = set()
for a, b in zip(x, y):
    for da in (-150, 0, 150):
        for db in (-150, 0, 150): K.add((int((a + da) // 1000), int((b + db) // 1000)))
U = "https://api3.geo.admin.ch/rest/services/api/MapServer/identify?"
def hole(e0, n0, e1, n1):
    q = {"geometryType": "esriGeometryEnvelope", "geometry": f"{e0},{n0},{e1},{n1}", "imageDisplay": "1000,1000,96",
         "mapExtent": f"{e0},{n0},{e1},{n1}", "tolerance": "0", "layers": "all:ch.swisstopo.swissnames3d", "returnGeometry": "true",
         "geometryFormat": "geojson", "sr": "2056", "limit": "200"}
    r = urllib.request.Request(U + urllib.parse.urlencode(q), headers={"User-Agent": "MarathonProfil/1.0 (private)"})
    return json.loads(urllib.request.urlopen(r, timeout=60).read())["results"]
os.makedirs("../dl/orte", exist_ok=True)
for e, n in sorted(K):
    f = f"../dl/orte/names3d_{e}_{n}.json"
    if os.path.exists(f): continue
    res = hole(e * 1000, n * 1000, e * 1000 + 1000, n * 1000 + 1000); time.sleep(0.3)
    if len(res) >= 200:
        res = []
        for de in (0, 500):
            for dn in (0, 500):
                part = hole(e * 1000 + de, n * 1000 + dn, e * 1000 + de + 500, n * 1000 + dn + 500); time.sleep(0.3)
                if len(part) >= 200: print("  voll:", e, n, de, dn)
                res += part
    json.dump(res, open(f, "w"), ensure_ascii=False)
print(len(K), "Kacheln")
