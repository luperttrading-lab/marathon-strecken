# Strecke 2026: die Linie aus der Outdooractive-Tour des Veranstalters (../dl/outdooractive_linie.json, 416 Punkte,
# im Mittel alle 86 m, Lücken bis 570 m) kürzt Kurven ab. Deshalb auf die Wege aus OpenStreetMap legen: kürzester Weg im
# OSM-Netz, jede Kante kostet ihre Länge × (1 + (Abstand zur Linie / 20 m)²). Etappen von Ankerpunkt zu Ankerpunkt
# (alle ~500 m ein Knoten höchstens 15 m neben der Linie), damit der Weg der Linie folgt und nicht abkürzt.
# -> gpx2026.json (Punkte und laufende Länge wie die GPX der anderen Strecken) und ../dl/locations.json (Start, Ziel)
import json, math, numpy as np, networkx as nx
from pyproj import Transformer
from scipy.spatial import cKDTree
T = Transformer.from_crs(4326, 32632, always_xy=True); TI = Transformer.from_crs(32632, 4326, always_xy=True)
L = json.load(open("../dl/outdooractive_linie.json")); P = np.array(L if isinstance(L[0], (list, tuple)) else L["pts"])
le, ln = T.transform(P[:, 1], P[:, 0]); M = np.c_[le, ln]
dl = np.r_[0, np.cumsum(np.hypot(*np.diff(M, axis=0).T))]
s = np.arange(0, dl[-1], 5.0); line = np.c_[np.interp(s, dl, M[:, 0]), np.interp(s, dl, M[:, 1])]
lt = cKDTree(line)
G = nx.Graph(); xy = {}
for w in json.load(open("../dl/osm_wege.json"))["elements"]:
    if w.get("tags", {}).get("highway") in ("motorway", "motorway_link", "trunk", "trunk_link", "construction", "proposed"): continue
    g = w.get("geometry") or []
    if len(g) < 2: continue
    xe, yn = T.transform([q["lon"] for q in g], [q["lat"] for q in g])
    for n, x, y in zip(w["nodes"], xe, yn): xy[n] = (x, y)
    for a, b in zip(w["nodes"][:-1], w["nodes"][1:]):
        pa, pb = np.array(xy[a]), np.array(xy[b]); ln_ = float(np.hypot(*(pb - pa)))
        k = max(2, int(ln_ / 5) + 1); q = pa + (pb - pa) * np.linspace(0, 1, k)[:, None]
        dist = lt.query(q)[0].mean()
        G.add_edge(a, b, length=ln_, cost=ln_ * (1 + (dist / 20.0) ** 2), name=w.get("tags", {}).get("name", ""))
ids = np.array(list(xy)); nt = cKDTree(np.array([xy[i] for i in ids]))
# Anker: Start, alle ~500 m, Ziel; jeweils der Knoten, der der Linie am nächsten liegt (im Umkreis von 15 m der Linienstelle)
anchors = []
for sa in list(np.arange(0, dl[-1], 500.0)) + [dl[-1]]:
    p = np.array([np.interp(sa, dl, M[:, 0]), np.interp(sa, dl, M[:, 1])])
    cand = nt.query_ball_point(p, 15.0 if 0 < sa < dl[-1] else 80.0)
    if not cand: continue
    best = min(cand, key=lambda j: np.hypot(*(np.array(xy[ids[j]]) - p)))
    if ids[best] in G and (not anchors or anchors[-1] != ids[best]): anchors.append(ids[best])
path = [anchors[0]]
for a, b in zip(anchors[:-1], anchors[1:]):
    seg = nx.shortest_path(G, a, b, weight="cost"); path += seg[1:]
# Hin und zurück auf demselben Stück (Anker auf einem Seitenweg) herausschneiden: ... A B A ... -> ... A ...
changed = True
while changed:
    changed = False
    for i in range(1, len(path) - 1):
        if path[i - 1] == path[i + 1]: del path[i:i + 2]; changed = True; break
xyp = np.array([xy[n] for n in path]); dp = np.r_[0, np.cumsum(np.hypot(*np.diff(xyp, axis=0).T))]
off = lt.query(xyp)[0]
print(f"Anker {len(anchors)}, Knoten {len(path)}, Länge {dp[-1]:.0f} m (Linie {dl[-1]:.0f} m); Abstand zur Linie Median {np.median(off):.1f} m, 95 % {np.percentile(off, 95):.1f} m, max {off.max():.0f} m bei {dp[np.argmax(off)]:.0f} m")
seen = {}
for i, n in enumerate(path):
    if n in seen and i - seen[n] > 2: print("  Knoten doppelt befahren:", n, round(dp[seen[n]]), round(dp[i]))
    seen[n] = i
lo, la = TI.transform(xyp[:, 0], xyp[:, 1])
pts = [(float(a), float(b), 0.0) for a, b in zip(la, lo)]
def hav(p, q):
    R = 6371008.8
    la1, lo1, la2, lo2 = map(math.radians, (p[0], p[1], q[0], q[1]))
    a = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))
d = [0.0]
for i in range(1, len(pts)): d.append(d[-1] + hav(pts[i - 1], pts[i]))
print("Punkte", len(pts), "Länge km", round(d[-1] / 1000, 3), "Start", pts[0][:2], "Ende", pts[-1][:2])
json.dump({"pts": pts, "d": d}, open("gpx2026.json", "w"))
json.dump([{"cat": "km", "name": "Start", "lat": pts[0][0], "lon": pts[0][1]}, {"cat": "km", "name": "Ziel", "lat": pts[-1][0], "lon": pts[-1][1]}], open("../dl/locations.json", "w"))
