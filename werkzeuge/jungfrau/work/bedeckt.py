# Überdeckte Stücke der Strecke aus OSM (../dl/osm_netz.json): je 10 Linienmeter, ob ein Weg mit tunnel=* oder covered=yes höchstens 4 m
# neben der Linie liegt und in dieselbe Richtung läuft (höchstens 35° Abweichung). Dort misst das Geländemodell die Decke (Erdreich bzw.
# Galerie darüber) statt der Fahrbahn; clean.py schätzt diese Stücke als Gerade zwischen den Portalen, wenn das Modell dort über der
# Fahrbahn liegt (GPX-Höhe des Veranstalters als Hinweis). Unterführungen unter Brücken (Fahrbahn sichtbar) bleiben gemessen.
# Kopie von werkzeuge/luzern/work/bedeckt.py.
# -> bedeckt.json [[Linienmeter, Weg-ID, Tags], …] nur für Treffer
import json
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
T = Transformer.from_crs(4326, 2056, always_xy=True)
o = json.load(open("../dl/osm_netz.json")); N = o["nodes"]
pk, pr, pw, W = [], [], [], []
for wid, (tg, refs) in o["ways"].items():
    if "highway" not in tg: continue
    if not (tg.get("tunnel", "no") not in ("no",) or tg.get("covered") == "yes"): continue
    pts = [N[str(r)] for r in refs if str(r) in N]
    if len(pts) < 2: continue
    x, y = T.transform([p[1] for p in pts], [p[0] for p in pts]); P = np.c_[x, y]; k = len(W); W.append((wid, tg))
    for a, b in zip(P[:-1], P[1:]):
        L = np.hypot(*(b - a))
        if L < 0.01: continue
        r = (b - a) / L
        for f in np.linspace(0, 1, max(2, int(L / 2) + 1)): pk.append(a + f * (b - a)); pr.append(r); pw.append(k)
pk = np.array(pk); pr = np.array(pr); pw = np.array(pw); baum = cKDTree(pk)
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); Q = np.array([p[:2] for p in g["pts"]])
ss = np.arange(0, d[-1], 10.0); x, y = T.transform(np.interp(ss, d, Q[:, 1]), np.interp(ss, d, Q[:, 0])); X = np.c_[x, y]
rl = np.array([X[min(len(X) - 1, i + 2)] - X[max(0, i - 2)] for i in range(len(X))]); rl /= np.maximum(np.hypot(*rl.T), 1e-9)[:, None]
out = []
for i, (s, p) in enumerate(zip(ss, X)):
    best = None
    for j in baum.query_ball_point(p, 4.0):
        if abs(float(np.dot(pr[j], rl[i]))) < np.cos(np.radians(35)): continue
        dist = float(np.hypot(*(pk[j] - p)))
        if best is None or dist < best[0]: best = (dist, W[pw[j]])
    if best: out.append([float(s), best[1][0], {k: v for k, v in best[1][1].items() if k in ("highway", "name", "tunnel", "covered", "layer", "ref")}])
json.dump(out, open("bedeckt.json", "w"), ensure_ascii=False)
from itertools import groupby
from common import official
for key, grp in groupby(out, key=lambda o: o[1]):
    grp = list(grp); print(f"Linie {grp[0][0]:6.0f}–{grp[-1][0]:6.0f} km {official(grp[0][0]) / 1000:6.2f}  {len(grp) * 10:4d} m  {key} {grp[0][2]}")
