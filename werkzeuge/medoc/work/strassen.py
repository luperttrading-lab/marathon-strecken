# Weg je 10 Linienmeter: nächster OSM-Weg (../dl/osm_wege.json) höchstens 30 m neben der Linie, Straßen bevorzugt (Abstand +
# Aufschlag je Klasse + Aufschlag für Wege quer zur Laufrichtung), ohne Tunnel. Bezeichnung (namen.py): Name aus OSM, sonst die
# Nummer der Départementstraße („D 2“), sonst für Feld- und Hofwege das nächste Château (OSM, ../dl/osm_chateaux.json) bis 600 m:
# „Weg am Château Latour“; ohne Château in der Nähe „Weinbergsweg“ bzw. „Weg“.
# -> strassen.json: [Linienmeter, Bezeichnung, highway, surface, tracktype, Brücke, Abstand]
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
from namen import bezeichnung, CHATEAUX
T = Transformer.from_crs(4326, 2154, always_xy=True)
AUF = {"trunk": 0, "primary": 0, "secondary": 0, "tertiary": 1, "secondary_link": 6, "tertiary_link": 6, "unclassified": 2,
       "residential": 2, "living_street": 4, "pedestrian": 4, "road": 6, "service": 4, "track": 3, "footway": 8, "path": 6,
       "cycleway": 8, "bridleway": 8}
wege, pk, pw = [], [], []
for w in json.load(open("../dl/osm_wege.json"))["elements"]:
    t = w.get("tags", {}); hw = t.get("highway")
    if hw not in AUF or len(w.get("geometry") or []) < 2 or t.get("tunnel") in ("yes", "culvert"): continue
    x, y = T.transform([q["lon"] for q in w["geometry"]], [q["lat"] for q in w["geometry"]]); P = np.c_[x, y]
    k = len(wege); wege.append(t)
    for a, b in zip(P[:-1], P[1:]):
        for f in np.linspace(0, 1, max(2, int(np.hypot(*(b - a)) / 3) + 1)): pk.append(a + f * (b - a)); pw.append(k)
pk = np.array(pk); baum = cKDTree(pk); pw = np.array(pw)
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); Q = np.array([p[:2] for p in g["pts"]])
ss = np.arange(0, d[-1], 10.0); x, y = T.transform(np.interp(ss, d, Q[:, 1]), np.interp(ss, d, Q[:, 0]))
dx = np.gradient(np.array(x)); dy = np.gradient(np.array(y)); nrm = np.hypot(dx, dy); dx, dy = dx / nrm, dy / nrm
out = []
for s, px, py, rx, ry in zip(ss, x, y, dx, dy):
    best = None
    for j in baum.query_ball_point([px, py], 30.0):
        t = wege[pw[j]]; dist = float(np.hypot(*(pk[j] - [px, py])))
        nb = [i for i in baum.query_ball_point(pk[j], 6.0) if pw[i] == pw[j]]
        v = pk[nb].max(0) - pk[nb].min(0) if len(nb) > 1 else np.array([rx, ry])
        quer = 1 - abs((v[0] * rx + v[1] * ry) / (np.hypot(*v) or 1))
        sc = dist + AUF[t["highway"]] + 12 * quer
        if best is None or sc < best[0]: best = (sc, t, dist)
    t, dist = (best[1], best[2]) if best else ({}, 99.0)
    out.append([float(s), bezeichnung(t, px, py), t.get("highway", ""), t.get("surface", ""), t.get("tracktype", ""), t.get("bridge", ""), round(dist, 1)])
json.dump(out, open("strassen.json", "w"), ensure_ascii=False)
from itertools import groupby
for n, grp in groupby(out, key=lambda o: o[1]):
    grp = list(grp); print(f"{grp[0][0]:7.0f} {len(grp) * 10:5d} m  {n}  ({grp[0][2]} {grp[0][3]} {grp[0][4]})")
# Belag: Anteil der Feldwege (track) und unbefestigten Wege laut OSM
from collections import Counter
c = Counter(o[2] for o in out); print({k: f"{v * 10 / 1000:.1f} km" for k, v in c.most_common()})
unbef = sum(1 for o in out if o[3] in ("gravel", "unpaved", "compacted", "fine_gravel", "dirt", "ground", "grass") or (o[2] == "track" and o[3] in ("", None) and o[4] not in ("grade1",)))
print(f"unbefestigt (surface gravel/unpaved/… oder track ohne Belag außer grade1): {unbef * 10 / 1000:.1f} km = {unbef / len(out) * 100:.0f} %")
