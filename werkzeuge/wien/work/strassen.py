# Straße je 10 Linienmeter: nächster OSM-Weg (../dl/osm_wege.json) höchstens 35 m neben der Linie, Hauptstraßen bevorzugt
# (Abstand + Aufschlag je Klasse + Aufschlag für Wege quer zur Laufrichtung + 25 für Wege ohne Namen: Im Prater liegt die Linie
# auf dem Rückweg bis 30 m neben der Mitte der Hauptallee, auf den Reit- und Radwegen daneben), ohne Unterführungen und Tunnel unter der Strecke (layer < 0, tunnel=yes), außer die Linie
# liegt selbst darin (dann ist der Tunnelweg der einzige nahe Weg in Laufrichtung). Brücken (bridge=yes) zählen; ihr Name
# steht in bridge:name oder name.
# -> strassen.json: [Linienmeter, Name (wie in OSM), bridge:name, Brücke, Tunnel, highway, layer]
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
from namen import name
T = Transformer.from_crs(4326, 31256, always_xy=True)
AUF = {"trunk": 0, "primary": 0, "secondary": 0, "tertiary": 2, "trunk_link": 8, "primary_link": 8, "secondary_link": 8, "tertiary_link": 8,
       "unclassified": 4, "residential": 4, "living_street": 6, "pedestrian": 5, "road": 8, "service": 10, "track": 8, "footway": 9,
       "path": 9, "cycleway": 12, "bridleway": 9}
wege, pk, pw = [], [], []
for w in json.load(open("../dl/osm_wege.json"))["elements"]:
    t = w.get("tags", {}); hw = t.get("highway")
    if hw not in AUF or len(w.get("geometry") or []) < 2: continue
    lay = t.get("layer", "0")
    if t.get("tunnel") in ("yes", "building_passage", "culvert") or (lay.lstrip("-").isdigit() and int(lay) < 0): continue
    x, y = T.transform([q["lon"] for q in w["geometry"]], [q["lat"] for q in w["geometry"]]); P = np.c_[x, y]
    k = len(wege); wege.append(t)
    for a, b in zip(P[:-1], P[1:]):
        n = max(2, int(np.hypot(*(b - a)) / 3) + 1)
        for f in np.linspace(0, 1, n): pk.append(a + f * (b - a)); pw.append(k)
pk = np.array(pk); baum = cKDTree(pk); pw = np.array(pw)
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); Q = np.array([p[:2] for p in g["pts"]])
ss = np.arange(0, d[-1], 10.0); x, y = T.transform(np.interp(ss, d, Q[:, 1]), np.interp(ss, d, Q[:, 0]))
# Laufrichtung je Punkt, damit Querstraßen an Kreuzungen weniger zählen
dx = np.gradient(np.array(x)); dy = np.gradient(np.array(y)); nrm = np.hypot(dx, dy); dx, dy = dx / nrm, dy / nrm
out = []
for s, px, py, rx, ry in zip(ss, x, y, dx, dy):
    best = None
    for j in baum.query_ball_point([px, py], 35.0):
        t = wege[pw[j]]; dist = float(np.hypot(*(pk[j] - [px, py])))
        # Richtung des Wegs an dieser Stelle
        nb = [i for i in baum.query_ball_point(pk[j], 6.0) if pw[i] == pw[j]]
        v = pk[nb].max(0) - pk[nb].min(0) if len(nb) > 1 else np.array([rx, ry])
        quer = 1 - abs((v[0] * rx + v[1] * ry) / (np.hypot(*v) or 1))
        sc = dist + AUF[t["highway"]] + 12 * quer + (0 if name(t) else 25)
        if best is None or sc < best[0]: best = (sc, t)
    t = best[1] if best else {}
    out.append([float(s), name(t), t.get("bridge:name", ""), t.get("bridge", ""), t.get("tunnel", ""), t.get("highway", ""), t.get("layer", "")])
json.dump(out, open("strassen.json", "w"), ensure_ascii=False)
from itertools import groupby
for (n, br), grp in groupby(out, key=lambda o: (o[1], o[3])):
    grp = list(grp); print(f"{grp[0][0]:7.0f} {len(grp) * 10:5d} m  {n} {'| BRÜCKE ' + grp[0][2] if br else ''} {grp[0][5]}")
