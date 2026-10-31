# Straße je 10 Linienmeter der Linie der Google-Karte (linie.json, beide Runden): nächster OSM-Weg (../dl/osm_netz.json) höchstens 25 m
# neben der Linie (die Linie ist eine aufgezeichnete Spur, keine Straßenmitte), dessen Richtung zur Linie passt (höchstens 35°
# abweichend; sonst nimmt eine Brücke quer über die Strecke den Platz der Straße darunter ein), Hauptstraßen bevorzugt (Abstand +
# Aufschlag je Klasse). Fußwege unter der Erde (level < 0, indoor, Fußweg mit layer < 0, z. B. die Staatsbrückenunterführung) bekommen
# 10 m Aufschlag. Namen wie in OSM (namen.py). Dazu der Fußpunkt auf dem Weg (Straßenmitte) und der Abstand der Spur davon.
# Muster: werkzeuge/freiburg/work/strassen.py (Kopie Hannover).
# -> strassen.json: [Linienmeter, name, name (namen.py), bridge, tunnel, layer, highway, OSM-Weg, Abstand, lat, lon (Fußpunkt)]
import json
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
from namen import name
T = Transformer.from_crs(4326, 31258, always_xy=True); TI = Transformer.from_crs(31258, 4326, always_xy=True)
AUF = {"motorway": 6, "trunk": 0, "primary": 0, "secondary": 0, "tertiary": 3, "motorway_link": 8, "trunk_link": 8, "primary_link": 8, "secondary_link": 8,
       "tertiary_link": 8, "unclassified": 6, "residential": 6, "living_street": 8, "pedestrian": 8, "road": 8, "service": 12,
       "footway": 14, "path": 14, "track": 14, "cycleway": 14}
o = json.load(open("../dl/osm_netz.json")); N = o["nodes"]
def unten(tg):
    return (tg.get("level", "0").startswith("-") or tg.get("indoor") in ("yes", "corridor")
            or (tg.get("layer", "0").startswith("-") and tg["highway"] in ("footway", "pedestrian", "path", "cycleway", "steps")))
pk, pr, pw, W = [], [], [], []
for wid, (tg, refs) in o["ways"].items():
    if tg.get("highway") not in AUF: continue
    if tg.get("tunnel") in ("yes", "building_passage") and tg["highway"] in ("motorway", "trunk", "primary", "trunk_link", "motorway_link"): continue
    pts = [N[str(r)] for r in refs if str(r) in N]
    if len(pts) < 2: continue
    x, y = T.transform([p[1] for p in pts], [p[0] for p in pts]); P = np.c_[x, y]; k = len(W); W.append((wid, tg))
    for a, b in zip(P[:-1], P[1:]):
        L = np.hypot(*(b - a))
        if L < 0.01: continue
        r = (b - a) / L
        for f in np.linspace(0, 1, max(2, int(L / 1) + 1)): pk.append(a + f * (b - a)); pr.append(r); pw.append(k)
pk = np.array(pk); pr = np.array(pr); pw = np.array(pw); baum = cKDTree(pk)
g = json.load(open("linie.json")); d = np.array(g["d"]); Q = np.array([p[:2] for p in g["pts"]])
ss = np.append(np.arange(0, d[-1], 10.0), d[-1]); x, y = T.transform(np.interp(ss, d, Q[:, 1]), np.interp(ss, d, Q[:, 0]))
X = np.c_[x, y]
rl = np.array([X[min(len(X) - 1, i + 2)] - X[max(0, i - 2)] for i in range(len(X))]); rl /= np.maximum(np.hypot(*rl.T), 1e-9)[:, None]
out = []
for i, (s, p) in enumerate(zip(ss, X)):
    best = None
    for j in baum.query_ball_point(p, 25.0):
        if abs(float(np.dot(pr[j], rl[i]))) < np.cos(np.radians(35)): continue
        wid, tg = W[pw[j]]; dist = float(np.hypot(*(pk[j] - p))); sc = dist + AUF[tg["highway"]] + (10 if unten(tg) else 0)
        if best is None or sc < best[0]: best = (sc, wid, tg, dist, j)
    if best is None: out.append([float(s), "", "", "", "", "", "", "", None, None, None]); continue
    _, wid, tg, dist, j = best
    lo_, la_ = TI.transform(*pk[j])
    nm = tg.get("name", "")
    out.append([float(s), nm, name(nm, tg.get("name:prefix", "")), tg.get("bridge", ""), tg.get("tunnel", ""),
                tg.get("layer", ""), tg.get("highway", ""), wid, round(dist, 1), round(la_, 7), round(lo_, 7)])
json.dump(out, open("strassen.json", "w"), ensure_ascii=False)
ab = np.array([q[8] for q in out if q[8] is not None])
print(f"{len(out)} Punkte, ohne Weg {sum(q[8] is None for q in out)}; Abstand Spur–Weg Median {np.median(ab):.1f} m, 90 % bis {np.percentile(ab, 90):.1f}, 99 % bis {np.percentile(ab, 99):.1f}, max {ab.max():.1f}")
from itertools import groupby
for key, grp in groupby(out, key=lambda o: (o[1], o[2], o[3], o[4], o[5], o[6])):
    grp = list(grp)
    print(f"{grp[0][0]:7.0f} {len(grp) * 10:5d} m  {key[1]:30s} {key[5]:12s} {'Brücke' if key[2] not in ('', 'no') else ''} {'Tunnel ' + key[3] if key[3] not in ('', 'no') else ''} {key[4]}  Abstand max {max((q[8] or 0) for q in grp):.0f}")
