# Hilfsskript zum Nachsehen (Kopie von werkzeuge/luzern/work/wege.py): alle OSM-Wege (../dl/osm_netz.json) höchstens N m neben der Linie zwischen zwei Linienmetern, mit den
# wichtigsten Tags. Aufruf: python3 wege.py <von> <bis> [N, Standard 25]   (so wurden Brücken, Tunnel und Durchläufe geprüft)
import json, sys, numpy as np
from pyproj import Transformer
T = Transformer.from_crs(4326, 2056, always_xy=True)
o = json.load(open("../dl/osm_netz.json")); N = o["nodes"]
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); Q = np.array([p[:2] for p in g["pts"]])
def near(s0, s1, maxd=25, nur=None):
    ss = np.arange(s0, s1, 10.0); x, y = T.transform(np.interp(ss, d, Q[:, 1]), np.interp(ss, d, Q[:, 0])); L = np.c_[x, y]
    res = {}
    for wid, (tg, refs) in o["ways"].items():
        if nur and not nur(tg): continue
        pts = [N[str(r)] for r in refs if str(r) in N]
        if len(pts) < 2: continue
        px, py = T.transform([p[1] for p in pts], [p[0] for p in pts]); P = np.c_[px, py]
        if np.min(np.hypot(P[:, 0, None] - L[None, :, 0], P[:, 1, None] - L[None, :, 1])) > 600: continue
        dense = np.vstack([a + f * (b - a) for a, b in zip(P[:-1], P[1:]) for f in np.linspace(0, 1, max(2, int(np.hypot(*(b - a)) / 3)))])
        dd = np.min(np.hypot(L[:, None, 0] - dense[None, :, 0], L[:, None, 1] - dense[None, :, 1]), axis=1)
        idx = np.where(dd < maxd)[0]
        if len(idx): res[wid] = (ss[idx[0]], ss[idx[-1]], dd[idx].min(), {k: v for k, v in tg.items() if k in ("highway", "name", "ref", "tunnel", "bridge", "layer", "covered", "level", "indoor", "location", "man_made", "railway", "waterway", "building")})
    for wid, (a, b, m, tg) in sorted(res.items(), key=lambda x: x[1][0]):
        print(f"  {a:7.0f}-{b:7.0f} min {m:5.1f} m  {wid}  {tg}")
a, b = float(sys.argv[1]), float(sys.argv[2]); md = float(sys.argv[3]) if len(sys.argv) > 3 else 25
near(a, b, md)
