# Distrikt alle 100 m (Linienmeter) aus den Distriktsflächen der Stadt (Ajuntament de València, Geoportal, Open Data
# „districtes-distritos“, ../dl/districtes.geojson) -> orte2026.json
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from matplotlib.path import Path
from namen import DISTRIKT
def flaechen(geom):
    cs = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    return [[Path(np.array(r)) for r in poly] for poly in cs]
def innen(ff, x, y):
    return any(p[0].contains_point((x, y)) and not any(h.contains_point((x, y)) for h in p[1:]) for p in ff)
D = [(f["properties"]["nombre"], flaechen(f["geometry"])) for f in json.load(open("../dl/districtes.geojson"))["features"]]
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
out = []
for s in np.arange(0, d[-1], 100.0):
    la, lo = np.interp(s, d, P[:, 0]), np.interp(s, d, P[:, 1])
    n = next((n for n, ff in D if innen(ff, lo, la)), "")
    out.append([float(s), DISTRIKT[n] if n else ""])
json.dump(out, open("orte2026.json", "w"), ensure_ascii=False)
from itertools import groupby
print([(k, len(list(v)) * 100) for k, v in groupby(o[1] for o in out)])
