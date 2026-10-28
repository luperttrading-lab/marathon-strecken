# Stadtteil alle 50 m (Linienmeter) aus OSM (BBBike-Auszug): Fläche boundary=administrative admin_level 10 (Vororte/„suburbs“), sonst place=suburb
# höchstens 2 km entfernt  -> orte2026.json
import json, math, numpy as np, osmium
from matplotlib.path import Path
from scipy.spatial import cKDTree
flaechen, punkte = [], []
class H(osmium.SimpleHandler):
    def node(self, n):
        if n.tags.get("place") == "suburb" and n.tags.get("name"): punkte.append((n.tags["name"], n.location.lat, n.location.lon))
    def area(self, a):
        if a.tags.get("name") and (a.tags.get("place") == "suburb" or (a.tags.get("boundary") == "administrative" and a.tags.get("admin_level") == "10")):
            for ring in a.outer_rings(): flaechen.append((a.tags["name"], Path(np.array([(nd.lon, nd.lat) for nd in ring]))))
H().apply_file("../dl/Sydney.osm.pbf", locations=True)
k = math.cos(math.radians(-33.87)) * 111320
nb = cKDTree(np.array([(lo * k, la * 110540) for _, la, lo in punkte]))
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
out = []
for s in np.arange(0, d[-1], 50.0):
    la, lo = np.interp(s, d, P[:, 0]), np.interp(s, d, P[:, 1])
    hit = [n for n, pa in flaechen if pa.contains_point((lo, la))]
    if hit: name = hit[0]
    else:
        dd, j = nb.query((lo * k, la * 110540)); name = punkte[j][0] if dd < 2000 else ""
    out.append([float(s), name])
json.dump(out, open("orte2026.json", "w"), ensure_ascii=False)
from itertools import groupby
print([(n, len(list(v)) * 50) for n, v in groupby(o[1] for o in out)])
