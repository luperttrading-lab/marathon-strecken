# Straße je 10 Linienmeter: nächster OSM-Weg (../dl/osm_wege.json) höchstens 20 m neben der Linie, Hauptstraßen bevorzugt
# (Abstand + Aufschlag je Klasse), ohne Unterführungen und Tunnel (die Strecke bleibt oben).
# -> strassen.json: [Linienmeter, Name (valencianisch, wie in OSM), name:es, Brücke, Tunnel, highway]
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
from namen import name
T = Transformer.from_crs(4326, 25830, always_xy=True)
AUF = {"trunk": 0, "primary": 0, "secondary": 0, "tertiary": 3, "trunk_link": 8, "primary_link": 8, "secondary_link": 8, "tertiary_link": 8,
       "unclassified": 6, "residential": 6, "living_street": 8, "pedestrian": 8, "road": 8, "service": 12}
wege, pk, pw = [], [], []
for w in json.load(open("../dl/osm_wege.json"))["elements"]:
    t = w.get("tags", {}); hw = t.get("highway")
    if hw not in AUF or len(w.get("geometry") or []) < 2: continue
    if t.get("tunnel") in ("yes", "building_passage") or t.get("layer", "0").lstrip("-").isdigit() and int(t.get("layer", "0")) < 0: continue
    x, y = T.transform([q["lon"] for q in w["geometry"]], [q["lat"] for q in w["geometry"]]); P = np.c_[x, y]
    k = len(wege); wege.append(t)
    for a, b in zip(P[:-1], P[1:]):
        n = max(2, int(np.hypot(*(b - a)) / 3) + 1)
        for f in np.linspace(0, 1, n): pk.append(a + f * (b - a)); pw.append(k)
baum = cKDTree(np.array(pk)); pw = np.array(pw)
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); Q = np.array([p[:2] for p in g["pts"]])
ss = np.arange(0, d[-1], 10.0); x, y = T.transform(np.interp(ss, d, Q[:, 1]), np.interp(ss, d, Q[:, 0]))
out = []
for s, px, py in zip(ss, x, y):
    best = None
    for j in baum.query_ball_point([px, py], 20.0):
        t = wege[pw[j]]; dist = float(np.hypot(*(np.array(pk[j]) - [px, py]))); sc = dist + AUF[t["highway"]]
        if best is None or sc < best[0]: best = (sc, t)
    t = best[1] if best else {}
    out.append([float(s), name(t), t.get("name:es", ""), t.get("bridge", ""), t.get("tunnel", ""), t.get("highway", "")])
json.dump(out, open("strassen.json", "w"), ensure_ascii=False)
from itertools import groupby
for (n, e), grp in groupby(out, key=lambda o: (o[1], o[2])):
    grp = list(grp); print(f"{grp[0][0]:7.0f} {len(grp) * 10:5d} m  {n} | {e} {'BR' if any(o[3] for o in grp) else ''}")
