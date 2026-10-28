# Kurs 2025: Linie von goandrace.com (../dl/paris2025_goandrace.gpx, in Garmin Connect gezeichnet, 1044 Punkte, 42,85 km, Lücken
# bis 1 km) auf das OSM-Straßennetz gelegt: kürzester Weg, jede Kante kostet Länge × (1 + (Abstand zur Linie / 20 m)²),
# Fußwege, Radwege und Pfade das Dreifache (in Paris liegen Gehwege als eigene Wege neben der Fahrbahn), Autobahnen
# (Périphérique) gar nicht. Etappen von Anker zu Anker (alle ~500 m ein Knoten höchstens 15 m neben der Linie).
# -> gpx2026.json (Punkte und laufende Länge wie bei den anderen Strecken)
import json, math, re, numpy as np, networkx as nx
from pyproj import Transformer
from scipy.spatial import cKDTree
T = Transformer.from_crs(4326, 32631, always_xy=True)
t = open("../dl/paris2025_goandrace.gpx").read()
P = np.array([(float(a), float(b)) for a, b in re.findall(r'lat="([-\d.]+)"\s+lon="([-\d.]+)"', t)])
le, ln = T.transform(P[:, 1], P[:, 0]); M = np.c_[le, ln]
dl = np.r_[0, np.cumsum(np.hypot(*np.diff(M, axis=0).T))]
s = np.arange(0, dl[-1], 5.0); line = np.c_[np.interp(s, dl, M[:, 0]), np.interp(s, dl, M[:, 1])]
lt = cKDTree(line)
G = nx.Graph(); xy = {}
LANGSAM = ("footway", "cycleway", "path", "pedestrian", "track", "steps")
# Der Kurs läuft unten an der Seine (2024 wegen Hochwasser ausnahmsweise oben „zwischen Henri-IV- und Tuileries-Tunnel“);
# die GPX-Linie trennt die Ebenen nicht, sie liegen in der Karte fast übereinander.
# Pflichtpunkte: Ost- und Westende des Tunnels des Tuileries (OSM-Weg 4294224); Anker dazwischen entfallen.
ZWANG = [25670638, 25670554]
for w in json.load(open("../dl/osm_wege.json"))["elements"]:
    tg = w.get("tags", {})
    if tg.get("highway") in ("motorway", "motorway_link") or tg.get("access") == "no": continue
    g = w.get("geometry") or []
    if len(g) < 2: continue
    xe, yn = T.transform([q["lon"] for q in g], [q["lat"] for q in g])
    for n, x, y in zip(w["nodes"], xe, yn): xy[n] = (x, y)
    f = 3.0 if tg.get("highway") in LANGSAM else 1.0
    for a, b in zip(w["nodes"][:-1], w["nodes"][1:]):
        pa, pb = np.array(xy[a]), np.array(xy[b]); ln_ = float(np.hypot(*(pb - pa)))
        k = max(2, int(ln_ / 5) + 1); q = pa + (pb - pa) * np.linspace(0, 1, k)[:, None]
        dist = lt.query(q)[0].mean()
        if dist > 300: continue
        G.add_edge(a, b, length=ln_, cost=ln_ * f * (1 + (dist / 20.0) ** 2), name=tg.get("name", ""), tunnel=tg.get("tunnel", ""), bridge=tg.get("bridge", ""))
ids = np.array([n for n in xy if n in G]); nt = cKDTree(np.array([xy[i] for i in ids]))
anchors = []
for sa in list(np.arange(0, dl[-1], 500.0)) + [dl[-1]]:
    p = np.array([np.interp(sa, dl, M[:, 0]), np.interp(sa, dl, M[:, 1])])
    cand = nt.query_ball_point(p, 15.0 if 0 < sa < dl[-1] else 60.0)
    if not cand: continue
    best = min(cand, key=lambda j: np.hypot(*(np.array(xy[ids[j]]) - p)))
    if not anchors or anchors[-1][1] != ids[best]: anchors.append((sa, ids[best]))
zs = [float(s[lt.query(xy[z])[1]]) for z in ZWANG]   # Lage der Pflichtpunkte auf der Linie
anchors = [a for a in anchors if not (zs[0] - 300 < a[0] < zs[1] + 300)] + list(zip(zs, ZWANG))
anchors = [n for _, n in sorted(anchors, key=lambda a: a[0])]
path = [anchors[0]]
for a, b in zip(anchors[:-1], anchors[1:]):
    seg = nx.shortest_path(G, a, b, weight="cost"); path += seg[1:]
changed = True
while changed:
    changed = False
    for i in range(1, len(path) - 1):
        if path[i - 1] == path[i + 1]: del path[i:i + 2]; changed = True; break
# kurze Schleifen zurück zum selben Knoten (unter 400 m, Anker auf einer Rampe neben der Strecke) herausschneiden
lauf = lambda p: sum(math.dist(xy[a], xy[b]) for a, b in zip(p, p[1:]))
changed = True
while changed:
    changed = False; pos = {}
    for i, q in enumerate(path):
        if q in pos and lauf(path[pos[q]:i + 1]) < 400:
            print(f"  Schleife entfernt: {lauf(path[pos[q]:i + 1]):.0f} m"); del path[pos[q] + 1:i + 1]; changed = True; break
        pos[q] = i
xyp = np.array([xy[n] for n in path]); dp = np.r_[0, np.cumsum(np.hypot(*np.diff(xyp, axis=0).T))]
off = lt.query(xyp)[0]
print(f"Anker {len(anchors)}, Knoten {len(path)}, Länge {dp[-1]:.0f} m (Linie {dl[-1]:.0f} m); Abstand zur Linie Median {np.median(off):.1f} m, 95 % {np.percentile(off, 95):.1f} m, max {off.max():.0f} m bei {dp[np.argmax(off)]:.0f} m")
TI = Transformer.from_crs(32631, 4326, always_xy=True)
lo, la = TI.transform(xyp[:, 0], xyp[:, 1])
pts = [(float(a), float(b), 0.0) for a, b in zip(la, lo)]
def hav(p, q):
    R = 6371008.8; la1, lo1, la2, lo2 = map(math.radians, (p[0], p[1], q[0], q[1]))
    return 2 * R * math.asin(math.sqrt(math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))
d = [0.0]
for i in range(1, len(pts)): d.append(d[-1] + hav(pts[i - 1], pts[i]))
print("Punkte", len(pts), "Länge km", round(d[-1] / 1000, 3), "Start", pts[0][:2], "Ende", pts[-1][:2])
json.dump({"pts": pts, "d": d}, open("gpx2026.json", "w"))
json.dump({"names": [G[a][b]["name"] for a, b in zip(path, path[1:])], "tunnel": [G[a][b]["tunnel"] for a, b in zip(path, path[1:])], "bridge": [G[a][b]["bridge"] for a, b in zip(path, path[1:])]}, open("../dl/kanten.json", "w"))
