# Straße je 10 Linienmeter. Die Linie besteht aus OSM-Wegen (route_osm.py, „wege“ je Punkt): Name und Art kommen vom Weg, auf dem die
# Linie an dieser Stelle liegt. Hat er keinen Namen (Gehweg, Radweg neben einer Straße), gilt der Name einer Straße höchstens 20 m daneben,
# die in dieselbe Richtung läuft (höchstens 35° Abweichung; Muster für die Suche: werkzeuge/zermatt/work/strassen.py). Namen wie in OSM.
# -> strassen.json: [Linienmeter, name, name (namen.py), bridge, tunnel, layer, highway, OSM-Weg]
import json
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
from namen import name
T = Transformer.from_crs(4326, 2056, always_xy=True)
o = json.load(open("../dl/osm_netz.json")); N = o["nodes"]; WG = o["ways"]
STR = {"primary", "secondary", "tertiary", "unclassified", "residential", "living_street", "pedestrian"}
pk, pr, pw = [], [], []
for wid, (tg, refs) in WG.items():
    if tg.get("highway") not in STR or not tg.get("name"): continue
    pts = [N[str(r)] for r in refs if str(r) in N]
    if len(pts) < 2: continue
    x, y = T.transform([p[1] for p in pts], [p[0] for p in pts]); P = np.c_[x, y]
    for a, b in zip(P[:-1], P[1:]):
        L = np.hypot(*(b - a))
        if L < 0.01: continue
        for f in np.linspace(0, 1, max(2, int(L / 3) + 1)): pk.append(a + f * (b - a)); pr.append((b - a) / L); pw.append(wid)
pk = np.array(pk); pr = np.array(pr); baum = cKDTree(pk)
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); W = g["wege"]; Q = np.array([p[:2] for p in g["pts"]])
ss = np.arange(0, d[-1], 10.0)
x, y = T.transform(np.interp(ss, d, Q[:, 1]), np.interp(ss, d, Q[:, 0])); X = np.c_[x, y]
rl = np.array([X[min(len(X) - 1, i + 2)] - X[max(0, i - 2)] for i in range(len(X))]); rl /= np.maximum(np.hypot(*rl.T), 1e-9)[:, None]
idx = np.clip(np.searchsorted(d, ss, side="right") - 1, 0, len(W) - 1)
out = []
for i, (s, k) in enumerate(zip(ss, idx)):
    wid = str(W[k]); tg = WG[wid][0]; nm = tg.get("name", "")
    if not nm and tg.get("highway") in ("footway", "cycleway", "path", "service", "steps", "track"):
        best = None
        for j in baum.query_ball_point(X[i], 20.0):
            if abs(float(np.dot(pr[j], rl[i]))) < np.cos(np.radians(35)): continue
            dist = float(np.hypot(*(pk[j] - X[i])))
            if best is None or dist < best[0]: best = (dist, pw[j])
        if best: nm = WG[best[1]][0]["name"]
    out.append([float(s), nm, name(nm), tg.get("bridge", ""), tg.get("tunnel", "") or ("yes" if tg.get("covered") == "yes" else ""),
                tg.get("layer", ""), tg.get("highway", ""), wid])
json.dump(out, open("strassen.json", "w"), ensure_ascii=False)
if __name__ == "__main__":
    from itertools import groupby
    from common import official
    for key, grp in groupby(out, key=lambda o: (o[1], o[3], o[4], o[6])):
        grp = list(grp)
        print(f"{grp[0][0]:7.0f} km {float(official(grp[0][0])) / 1000:6.2f} {len(grp) * 10:5d} m  {key[0]:28s} {key[3]:12s} "
              f"{'Brücke' if key[1] not in ('', 'no') else ''} {'Tunnel ' + key[2] if key[2] not in ('', 'no') else ''} {grp[0][7]}")
