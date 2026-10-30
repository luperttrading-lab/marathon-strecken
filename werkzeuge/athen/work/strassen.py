# Straße je 10 Linienmeter: nächster OSM-Weg (../dl/osm_netz.json) höchstens 20 m neben der Linie, dessen Richtung zur Linie passt
# (höchstens 35° abweichend; sonst nimmt eine Brücke quer über die Strecke, z. B. die Katechaki über der Mesogeion, den Platz der
# Straße darunter ein), Hauptstraßen bevorzugt (Abstand + Aufschlag je Klasse). Tunnel und Brücken zählen mit: Die Strecke läuft durch
# die Unterführungen am Stavros und an der Katechaki.
# -> strassen.json: [Linienmeter, name (griechisch), Umschrift (namen.py), bridge, tunnel, layer, highway, OSM-Weg]
import json
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
from namen import name
T = Transformer.from_crs(4326, 2100, always_xy=True)
AUF = {"motorway": 6, "trunk": 0, "primary": 0, "secondary": 0, "tertiary": 3, "trunk_link": 8, "primary_link": 8, "secondary_link": 8,
       "tertiary_link": 8, "unclassified": 6, "residential": 6, "living_street": 8, "pedestrian": 8, "road": 8, "service": 12,
       "footway": 14, "path": 14, "track": 14, "cycleway": 14}
o = json.load(open("../dl/osm_netz.json")); N = o["nodes"]
pk, pr, pw, W = [], [], [], []
for wid, (tg, refs) in o["ways"].items():
    if tg.get("highway") not in AUF: continue
    pts = [N[str(r)] for r in refs if str(r) in N]
    if len(pts) < 2: continue
    x, y = T.transform([p[1] for p in pts], [p[0] for p in pts]); P = np.c_[x, y]; k = len(W); W.append((wid, tg))
    for a, b in zip(P[:-1], P[1:]):
        L = np.hypot(*(b - a))
        if L < 0.01: continue
        r = (b - a) / L
        for f in np.linspace(0, 1, max(2, int(L / 3) + 1)): pk.append(a + f * (b - a)); pr.append(r); pw.append(k)
pk = np.array(pk); pr = np.array(pr); pw = np.array(pw); baum = cKDTree(pk)
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); Q = np.array([p[:2] for p in g["pts"]])
ss = np.arange(0, d[-1], 10.0); x, y = T.transform(np.interp(ss, d, Q[:, 1]), np.interp(ss, d, Q[:, 0]))
X = np.c_[x, y]
# Laufrichtung über ±20 m
rl = np.array([X[min(len(X) - 1, i + 2)] - X[max(0, i - 2)] for i in range(len(X))]); rl /= np.maximum(np.hypot(*rl.T), 1e-9)[:, None]
out = []
for i, (s, p) in enumerate(zip(ss, X)):
    best = None
    for j in baum.query_ball_point(p, 20.0):
        if abs(float(np.dot(pr[j], rl[i]))) < np.cos(np.radians(35)): continue
        wid, tg = W[pw[j]]; dist = float(np.hypot(*(pk[j] - p))); sc = dist + AUF[tg["highway"]]
        if best is None or sc < best[0]: best = (sc, wid, tg)
    if best is None: out.append([float(s), "", "", "", "", "", "", ""]); continue
    _, wid, tg = best
    out.append([float(s), tg.get("name", ""), name(tg.get("name", ""), tg.get("name:prefix", "")), tg.get("bridge", ""), tg.get("tunnel", ""),
                tg.get("layer", ""), tg.get("highway", ""), wid])
json.dump(out, open("strassen.json", "w"), ensure_ascii=False)
from itertools import groupby
from common import official
for key, grp in groupby(out, key=lambda o: (o[1], o[2], o[3], o[4], o[5], o[6])):
    grp = list(grp)
    print(f"{grp[0][0]:7.0f} km {float(official(grp[0][0])) / 1000:6.2f} {len(grp) * 10:5d} m  {key[1]:30s} {key[0]:22s} {key[5]:12s} {'Brücke' if key[2] not in ('', 'no') else ''} {'Tunnel ' + key[3] if key[3] not in ('', 'no') else ''} {key[4]}")
