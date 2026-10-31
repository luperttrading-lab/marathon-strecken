# Linie des Veranstalters (linie.json, Strava-Route aus der GPX-Datei, 1163 Punkte, Abstand im Median 30 m, gerade Stücke bis 100 m) auf die
# Wege aus OpenStreetMap legen (../dl/osm_netz.json, osm.py): Die Strava-Route liegt schon auf OSM-Wegen (im Median 0,8 m daneben), ist
# aber vereinfacht; in Kehren und Kurven der Waldwege schneidet sie ab. Kürzester Weg im OSM-Netz, jede Kante kostet ihre Länge ×
# (1 + (Abstand zur Linie / 8 m)²), Etappen von Anker zu Anker (alle 200 m der Knoten, der höchstens 8 m neben der Linie liegt), damit der
# Weg der Linie folgt und nicht abkürzt. Wo der gelegte Weg mehr als 25 m neben der Linie liegt (Weg fehlt in OSM oder ist anders
# verbunden), gilt die Linie selbst. Muster: werkzeuge/rennsteig/work/match.py.
# -> gelegt.json {"pts": [[lat, lon]…], "d": Linienmeter (geodätisch)}
import json, numpy as np, networkx as nx
from pyproj import Transformer, Geod
from scipy.spatial import cKDTree
T = Transformer.from_crs(4326, 25832, always_xy=True); TI = Transformer.from_crs(25832, 4326, always_xy=True); G_ = Geod(ellps="WGS84")
L = json.load(open("linie.json")); P = np.array(L["pts"])
le, ln = T.transform(P[:, 1], P[:, 0]); M = np.c_[le, ln]
dl = np.r_[0, np.cumsum(np.hypot(*np.diff(M, axis=0).T))]
s = np.arange(0, dl[-1], 2.0); line = np.c_[np.interp(s, dl, M[:, 0]), np.interp(s, dl, M[:, 1])]
lt = cKDTree(line)
o = json.load(open("../dl/osm_netz.json")); NO = o["nodes"]
G = nx.Graph(); xy = {}
for wid, (tg, refs) in o["ways"].items():
    if "highway" not in tg or tg["highway"] in ("motorway", "motorway_link", "trunk", "trunk_link", "construction", "proposed", "razed"): continue
    refs = [r for r in refs if str(r) in NO]
    if len(refs) < 2: continue
    xe, yn = T.transform([NO[str(r)][1] for r in refs], [NO[str(r)][0] for r in refs])
    for n, x, y in zip(refs, xe, yn): xy[n] = (x, y)
    for a, b in zip(refs[:-1], refs[1:]):
        pa, pb = np.array(xy[a]), np.array(xy[b]); ln_ = float(np.hypot(*(pb - pa)))
        k = max(2, int(ln_ / 3) + 1); q = pa + (pb - pa) * np.linspace(0, 1, k)[:, None]
        dist = lt.query(q)[0].mean()
        G.add_edge(a, b, length=ln_, cost=ln_ * (1 + (dist / 8.0) ** 2), weg=wid)
ids = np.array(list(xy)); nt = cKDTree(np.array([xy[i] for i in ids]))
anchors = []
for sa in list(np.arange(0, dl[-1], 200.0)) + [dl[-1]]:
    p = np.array([np.interp(sa, dl, M[:, 0]), np.interp(sa, dl, M[:, 1])])
    cand = nt.query_ball_point(p, 8.0 if 0 < sa < dl[-1] else 40.0)
    if not cand: continue
    best = min(cand, key=lambda j: np.hypot(*(np.array(xy[ids[j]]) - p)))
    if ids[best] in G and (not anchors or anchors[-1] != ids[best]): anchors.append(ids[best])
path = [anchors[0]]
for a, b in zip(anchors[:-1], anchors[1:]):
    seg = nx.shortest_path(G, a, b, weight="cost"); path += seg[1:]
changed = True
while changed:     # hin und zurück auf demselben Stück (Anker auf einem Seitenweg) herausschneiden
    changed = False
    for i in range(1, len(path) - 1):
        if path[i - 1] == path[i + 1]: del path[i:i + 2]; changed = True; break
xyp = np.array([xy[n] for n in path]); dp = np.r_[0, np.cumsum(np.hypot(*np.diff(xyp, axis=0).T))]
qd = np.arange(0, dp[-1], 2.0); dicht = np.c_[np.interp(qd, dp, xyp[:, 0]), np.interp(qd, dp, xyp[:, 1])]
off = lt.query(dicht)[0]
print(f"Anker {len(anchors)}, Knoten {len(path)}, Länge {dp[-1]:.0f} m (Linie {dl[-1]:.0f} m); Abstand zur Linie Median {np.median(off):.1f} m, "
      f"95 % {np.percentile(off, 95):.1f} m, max {off.max():.0f} m bei Wegmeter {qd[np.argmax(off)]:.0f}")
# Linie > 25 m neben dem gelegten Weg: dort die Linie übernehmen
dist = cKDTree(dicht).query(line)[0]; pt = cKDTree(xyp)
over = dist > 25; i = 0; teile = []
while i < len(s):
    if not over[i]: i += 1; continue
    j = i
    while j + 1 < len(s) and over[j + 1]: j += 1
    while i > 0 and dist[i - 1] > 3: i -= 1
    while j + 1 < len(s) and dist[j + 1] > 3: j += 1
    teile.append((i, j)); i = j + 1
neu, k0 = [], 0
for i, j in teile:
    a_ = pt.query(line[i])[1]; b_ = pt.query(line[j])[1] if j + 1 < len(s) else len(xyp) - 1
    neu += list(xyp[k0:a_ + 1]) + list(line[i:j + 1]); k0 = b_ + 1 if j + 1 < len(s) else len(xyp)
    print(f"  Linie übernommen: Linienmeter {s[i]:.0f}–{s[j]:.0f}, bis {dist[i:j + 1].max():.0f} m neben dem gelegten Weg")
neu += list(xyp[k0:])
xyp = np.array(neu)
# Anfang und Ende genau auf Start und Ziel der GPX
xyp = np.r_[[M[0]], xyp, [M[-1]]]
lo, la = TI.transform(xyp[:, 0], xyp[:, 1])
pts = [[float(a), float(b)] for a, b in zip(la, lo)]
pts = [pts[0]] + [q for p, q in zip(pts[:-1], pts[1:]) if q != p]
d = [0.0]
for a, b in zip(pts[:-1], pts[1:]): d.append(d[-1] + G_.inv(a[1], a[0], b[1], b[0])[2])
xs, ys = T.transform([p[1] for p in pts], [p[0] for p in pts]); dd = np.r_[0, np.cumsum(np.hypot(*np.diff(np.c_[xs, ys], axis=0).T))]
q2 = np.arange(0, dd[-1], 2.0); off2 = lt.query(np.c_[np.interp(q2, dd, xs), np.interp(q2, dd, ys)])[0]
print(f"Ergebnis: {len(pts)} Punkte, {d[-1]:.1f} m (GPX {L['d'][-1]:.1f} m, {100 * (d[-1] / L['d'][-1] - 1):+.2f} %); neben der GPX-Linie Median "
      f"{np.median(off2):.1f} m, 95 % {np.percentile(off2, 95):.1f} m, max {off2.max():.1f} m")
json.dump({"pts": pts, "d": d}, open("gelegt.json", "w"))
