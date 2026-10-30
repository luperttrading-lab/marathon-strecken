# Gegenproben zur Linie (parse.py):
# 1. Plan 2026 und Plan 2027 des Veranstalters (VCM-Streckenplaene_2026_SO-alleBewerbe_v4.pdf, 10.03.2026, und
#    VCM-Streckenplaene_2027_SO_v1.pdf, 13.04.2026, „Sonntag, 18. April 2027“; Vektorgrafik aus Illustrator): Die Marathonlinie
#    (Farbe 0,128/0,147/0,339, 2,75 pt) ist in beiden Plänen Punkt für Punkt gleich -> Kurs 2027 = Kurs 2026.
# 2. Plan 2026 affin auf die Linie der Google-Karte eingepasst (ICP), Abstand in beide Richtungen.
# 3. GPX des Veranstalters (ViennaCityMarathon-PoweradeRelayMarathon.gpx, mit dem Routenplaner von Strava auf OpenStreetMap
#    gezeichnet, 731 Punkte): Abstand zur Linie der Google-Karte, Länge.
import json, numpy as np, pymupdf, xml.etree.ElementTree as ET
from scipy.spatial import cKDTree
from pyproj import Transformer, Geod
T = Transformer.from_crs(4326, 31256, always_xy=True)
def dicht(P, step):
    out = [P[0]]
    for a, b in zip(P[:-1], P[1:]):
        n = max(1, int(np.hypot(*(b - a)) / step)); out += [a + f * (b - a) for f in np.linspace(0, 1, n + 1)[1:]]
    return np.array(out)
def planlinie(f):
    segs = []
    for dr in pymupdf.open(f)[0].get_drawings():
        c = tuple(round(x, 3) for x in dr["color"]) if dr.get("color") else None
        if dr["type"] not in ("s", "fs") or c != (0.128, 0.147, 0.339) or abs((dr.get("width") or 0) - 2.75) > 0.02: continue
        p = []
        for it in dr["items"]:
            if it[0] == "l": p += [(it[1].x, -it[1].y), (it[2].x, -it[2].y)]
            elif it[0] == "c":
                a, b, c_, e = it[1:5]
                for t in np.linspace(0, 1, 8): p.append(((1-t)**3*a.x+3*(1-t)**2*t*b.x+3*(1-t)*t**2*c_.x+t**3*e.x, -((1-t)**3*a.y+3*(1-t)**2*t*b.y+3*(1-t)*t**2*c_.y+t**3*e.y)))
        if len(p) > 1: segs.append(dicht(np.array(p), 0.3))
    return np.vstack(segs)
P26 = planlinie("../dl/VCM-Streckenplaene_2026_SO-alleBewerbe_v4.pdf"); P27 = planlinie("../dl/VCM-Streckenplaene_2027_SO_v1.pdf")
a, _ = cKDTree(P26).query(P27); b, _ = cKDTree(P27).query(P26)
print(f"Plan 2027 gegen Plan 2026: größter Abstand {max(a.max(), b.max()):.3f} pt (1 pt ≈ 13 m)")
g = json.load(open("gpx2026.json")); K = np.array([T.transform(p[1], p[0]) for p in g["pts"]]); Kd = dicht(K, 5); baum = cKDTree(Kd)
P = P26; s = (K.max(0) - K.min(0)) / (P.max(0) - P.min(0)); A = np.diag(s); t = K.min(0) - P.min(0) * s
for _ in range(60):
    d, i = baum.query(P @ A.T + t); m = d < np.percentile(d, 90)
    sol, *_ = np.linalg.lstsq(np.c_[P[m], np.ones(m.sum())], Kd[i[m]], rcond=None); A, t = sol[:2].T, sol[2]
Q = P @ A.T + t; d, _ = baum.query(Q); d2, _ = cKDTree(Q).query(Kd)
print("Maßstab des Plans m/pt", np.round(np.linalg.norm(A, axis=0), 2))
print(f"Plan 2026 -> Linie: Median {np.median(d):.0f} m, 95 % {np.percentile(d, 95):.0f} m, max {d.max():.0f} m")
print(f"Linie -> Plan 2026: Median {np.median(d2):.0f} m, 95 % {np.percentile(d2, 95):.0f} m, max {d2.max():.0f} m")
cum = np.r_[0, np.cumsum(np.hypot(*np.diff(Kd, axis=0).T))]
weit = cum[d2 > 80]
print("Linie mehr als 80 m neben dem Plan bei Linienmeter:", sorted({int(c // 500 * 500) for c in weit}) or "nirgends")
r = ET.parse("../dl/vcm2026.gpx").getroot(); ns = "{http://www.topografix.com/GPX/1/1}"
G = [(float(q.get("lat")), float(q.get("lon"))) for q in r.iter(ns + "trkpt")]
_, _, dd = Geod(ellps="GRS80").inv([p[1] for p in G[:-1]], [p[0] for p in G[:-1]], [p[1] for p in G[1:]], [p[0] for p in G[1:]])
Gx = dicht(np.array([T.transform(lo, la) for la, lo in G]), 2)
e1, _ = cKDTree(dicht(K[1:], 2)).query(Gx); e2, _ = cKDTree(Gx).query(dicht(K[1:], 2))   # ohne die Verlängerung am Start
print(f"GPX (Strava) {sum(dd):.0f} m, {len(G)} Punkte; GPX -> Linie Median {np.median(e1):.1f} m, max {e1.max():.0f} m; "
      f"Linie -> GPX Median {np.median(e2):.1f} m, max {e2.max():.0f} m (ohne die 70 m Verlängerung am Start)")
