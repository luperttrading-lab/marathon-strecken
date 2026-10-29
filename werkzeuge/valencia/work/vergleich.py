# Gegenprobe Kurs 2026: Die Google-Karte des Veranstalters trägt noch „Edición 2025“. Der Plan 2026
# (../dl/recorrido-42k-valencia-2026.pdf, „Plano Recorrido 42k 2026 v3 - Provisional“, 20.07.2026, Vektorgrafik) enthält die
# Streckenlinie als Pfad (Farbe 0,05/0,71/0,85, 2,74 pt). Affin auf die Linie der Google-Karte eingepasst (ICP); dann der Abstand
# in beide Richtungen. Der Plan ist leicht verzerrt (Maßstab waagerecht 5,59, senkrecht 6,13 m/pt) und schematisch an Start und Ziel.
import json, numpy as np, pymupdf
from scipy.spatial import cKDTree
from pyproj import Transformer
T = Transformer.from_crs(4326, 25830, always_xy=True)
g = json.load(open("gpx2026.json")); K = np.array([T.transform(p[1], p[0]) for p in g["pts"]])
def dicht(P, step):
    out = [P[0]]
    for a, b in zip(P[:-1], P[1:]):
        n = max(1, int(np.hypot(*(b - a)) / step)); out += [a + f * (b - a) for f in np.linspace(0, 1, n + 1)[1:]]
    return np.array(out)
segs = []
for dr in pymupdf.open("../dl/recorrido-42k-valencia-2026.pdf")[0].get_drawings():
    c = tuple(round(x, 2) for x in dr["color"]) if dr.get("color") else None
    if dr["type"] != "s" or c != (0.05, 0.71, 0.85) or abs(dr["width"] - 2.74) > 0.05: continue
    p = []
    for it in dr["items"]:
        if it[0] == "l": p += [(it[1].x, -it[1].y), (it[2].x, -it[2].y)]
        elif it[0] == "c":
            a, b, c_, e = it[1:5]
            for t in np.linspace(0, 1, 8): p.append(((1-t)**3*a.x+3*(1-t)**2*t*b.x+3*(1-t)*t**2*c_.x+t**3*e.x, -((1-t)**3*a.y+3*(1-t)**2*t*b.y+3*(1-t)*t**2*c_.y+t**3*e.y)))
    segs.append(dicht(np.array(p), 0.5))
P = np.vstack(segs); Kd = dicht(K, 5); baum = cKDTree(Kd)
s = (K.max(0) - K.min(0)) / (P.max(0) - P.min(0)); A = np.diag(s); t = K.min(0) - P.min(0) * s
for _ in range(40):
    d, i = baum.query(P @ A.T + t); m = d < np.percentile(d, 90)
    sol, *_ = np.linalg.lstsq(np.c_[P[m], np.ones(m.sum())], Kd[i[m]], rcond=None); A, t = sol[:2].T, sol[2]
Q = P @ A.T + t; d, _ = baum.query(Q); d2, _ = cKDTree(Q).query(Kd)
print("Maßstab m/pt", np.round(np.diag(A), 2))
print(f"Plan 2026 -> Linie: Median {np.median(d):.1f} m, 95 % {np.percentile(d, 95):.1f} m, max {d.max():.0f} m")
print(f"Linie -> Plan 2026: Median {np.median(d2):.1f} m, 95 % {np.percentile(d2, 95):.1f} m, max {d2.max():.0f} m")
cum = np.r_[0, np.cumsum(np.hypot(*np.diff(Kd, axis=0).T))]
print("Linie mehr als 60 m neben dem Plan:", [round(float(c)) for c in cum[d2 > 60]] or "nirgends")
