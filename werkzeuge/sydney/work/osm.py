# OSM-Wege (highway) aus dem Auszug von BBBike (Kapstadt, ../dl/Sydney.osm.pbf, Stand 24.10.2026), weil die Overpass-Spiegel
# nicht antworteten; nur Wege im Umkreis von 150 m um die offizielle Linie, im Format von Overpass „out body geom“ -> ../dl/osm_wege.json
import json, re, math, os, urllib.request
import numpy as np, osmium
from scipy.spatial import cKDTree
PBF = "../dl/Sydney.osm.pbf"
if not os.path.exists(PBF):
    urllib.request.urlretrieve("https://download.bbbike.org/osm/bbbike/CapeTown/Sydney.osm.pbf", PBF)
t = open("../dl/sydney2026_offiziell.gpx").read()
P = np.array([(float(a), float(b)) for a, b in re.findall(r'lat="([-\d.]+)"\s+lon="([-\d.]+)"', t)])
k = math.cos(math.radians(-33.87)) * 111320
x = P[:, 1] * k; y = P[:, 0] * 110540; d = np.r_[0, np.cumsum(np.hypot(np.diff(x), np.diff(y)))]
ss = np.arange(0, d[-1], 20.0); baum = cKDTree(np.c_[np.interp(ss, d, x), np.interp(ss, d, y)])
out = []
class H(osmium.SimpleHandler):
    def way(self, w):
        if "highway" not in w.tags: return
        try: g = [(n.lat, n.lon) for n in w.nodes]
        except osmium.InvalidLocationError: return
        a = np.array(g); dd, _ = baum.query(np.c_[a[:, 1] * k, a[:, 0] * 110540])
        if dd.min() > 150: return
        out.append({"type": "way", "id": w.id, "nodes": [n.ref for n in w.nodes], "tags": {t.k: t.v for t in w.tags},
                    "geometry": [{"lat": la, "lon": lo} for la, lo in g]})
H().apply_file(PBF, locations=True)
json.dump({"elements": out}, open("../dl/osm_wege.json", "w"))
print(len(out), "Wege")
