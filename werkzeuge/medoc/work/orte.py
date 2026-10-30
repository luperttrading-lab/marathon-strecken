# Gemeinde alle 100 m (Linienmeter) aus ADMIN EXPRESS der IGN (WFS der Géoplateforme, Layer ADMINEXPRESS-COG.LATEST:commune,
# Licence Ouverte; ../dl/commune.geojson). Läuft die Linie auf einer Gemeindegrenze (im Umkreis von 25 m beide Gemeinden zu
# mindestens 4 von 13 Teilen), beide: „Pauillac / Saint-Estèphe“ (zuerst die mit dem größeren Anteil). -> orte2026.json
import json, numpy as np
from matplotlib.path import Path
from pyproj import Transformer
T = Transformer.from_crs(4326, 2154, always_xy=True)
G = []
for f in json.load(open("../dl/commune.geojson"))["features"]:
    geo = f["geometry"]; cs = geo["coordinates"] if geo["type"] == "MultiPolygon" else [geo["coordinates"]]
    polys = []
    for poly in cs:
        ringe = []
        for r in poly:
            r = np.array(r)[:, :2]; x, y = T.transform(r[:, 0], r[:, 1]); ringe.append(Path(np.c_[x, y]))
        polys.append(ringe)
    G.append((f["properties"]["nom_officiel"], polys))
def innen(polys, x, y): return any(p[0].contains_point((x, y)) and not any(hh.contains_point((x, y)) for hh in p[1:]) for p in polys)
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
RING = [(dx, dy) for dx in (-25, -12.5, 0, 12.5, 25) for dy in (-25, -12.5, 0, 12.5, 25) if dx * dx + dy * dy <= 625]
out = []
for s in np.arange(0, d[-1], 100.0):
    x, y = T.transform(np.interp(s, d, P[:, 1]), np.interp(s, d, P[:, 0]))
    z = {}
    for dx, dy in RING:
        for n, polys in G:
            if innen(polys, x + dx, y + dy): z[n] = z.get(n, 0) + 1; break
    rang = sorted(z, key=lambda q: -z[q])
    text = f"{rang[0]} / {rang[1]}" if len(rang) > 1 and z[rang[1]] >= 4 else (rang[0] if rang else "")
    out.append([float(s), text, z])
json.dump([o[:2] for o in out], open("orte2026.json", "w"), ensure_ascii=False)
from itertools import groupby
for q, v in groupby(out, key=lambda o: o[1]):
    v = list(v); print(f"{v[0][0]:7.0f} {len(v) * 100:5d} m  {q}   {v[0][2]}")
