# Streckenplan (PDF-Punkte) -> Lage (ETRS89 / UTM 32N, EPSG:25832), affin (6 Werte), in zwei Schritten:
# 1. grob an der Tour von Visit Düsseldorf (tour2026.json): Plan und Tour sind dieselbe Linie (nach der Einpassung im Median 1–2 m
#    auseinander; die Tour ist offenbar nach dem Plan gezeichnet),
# 2. fein an den Straßen in OSM (../dl/osm_netz.json): jeder Planpunkt zum nächsten Straßenpunkt bis 20 m, Ausreißer weg, wiederholt
#    (ICP). Die Karte im PDF ist nicht winkeltreu gestreckt (x 4,07 m/pt, y 4,25 m/pt), daher affin statt Ähnlichkeit.
# -> georef.json {"M": 3×2-Matrix [x, y, 1] @ M = [E, N], "plan": [[E, N] je PDF-Punkt], Kennzahlen}
import json
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
T = Transformer.from_crs(4326, 25832, always_xy=True)
P = np.array(json.load(open("plan_pdf.json"))["pts"])
def dicht(A, step):
    s = np.r_[0, np.cumsum(np.hypot(*np.diff(A, axis=0).T))]; g = np.arange(0, s[-1], step)
    return np.c_[np.interp(g, s, A[:, 0]), np.interp(g, s, A[:, 1])]
PD = dicht(P, 1.0); PH = np.c_[PD, np.ones(len(PD))]
def icp(Z, M, grenze, runden=30, quant=90):
    baum = cKDTree(Z)
    for _ in range(runden):
        dist, idx = baum.query(PH @ M)
        ok = (dist < grenze) & (dist <= np.percentile(dist, quant))
        M = np.linalg.lstsq(PH[ok], Z[idx[ok]], rcond=None)[0]
    dist, _ = baum.query(PH @ M)
    return M, dist
# 1. Tour
tu = json.load(open("tour2026.json")); Q = np.array(tu["pts"]); d = np.array(tu["d"])
ss = np.arange(0, d[-1], 2.0); E, N = T.transform(np.interp(ss, d, Q[:, 1]), np.interp(ss, d, Q[:, 0])); TU = np.c_[E, N]
i1 = np.linspace(0, len(PD) - 1, 400).astype(int); i2 = np.linspace(0, len(TU) - 1, 400).astype(int)
M0 = np.linalg.lstsq(PH[i1], TU[i2], rcond=None)[0]
M1, d1 = icp(TU, M0, 1e9)
print(f"an der Tour: Abstand Median {np.median(d1):.1f} m, 90 % {np.percentile(d1, 90):.1f} m, 99 % {np.percentile(d1, 99):.1f} m")
# 2. OSM-Straßen (Fahrbahnen und Wege, ohne Treppen), alle 2 m ein Punkt
o = json.load(open("../dl/osm_netz.json")); NO = o["nodes"]
Z = []
for wid, (tg, refs) in o["ways"].items():
    if tg.get("highway") in (None, "steps", "proposed", "construction", "platform", "elevator", "bus_stop"): continue
    pts = [NO[str(r)] for r in refs if str(r) in NO]
    if len(pts) < 2: continue
    x, y = T.transform([q[1] for q in pts], [q[0] for q in pts]); A = np.c_[x, y]
    Z.append(dicht(A, 2.0) if np.hypot(*np.diff(A, axis=0).T).sum() > 2 else A)
Z = np.vstack(Z)
M2, d2 = icp(Z, M1, 20.0)
print(f"an OSM: Abstand Median {np.median(d2):.1f} m, 90 % {np.percentile(d2, 90):.1f} m, 99 % {np.percentile(d2, 99):.1f} m")
print("Maßstab x/y m/pt", np.hypot(*M2[0]).round(4), np.hypot(*M2[1]).round(4), "Verschiebung gegen Tour-Einpassung (m):",
      np.round((PH @ M2 - PH @ M1).mean(0), 1), "max", np.round(np.hypot(*(PH @ M2 - PH @ M1).T).max(), 1))
d_t, _ = cKDTree(TU).query(PH @ M2)
print(f"Tour gegen OSM-eingepassten Plan: Median {np.median(d_t):.1f} m, 90 % {np.percentile(d_t, 90):.1f} m, max {d_t.max():.0f} m")
plan = (np.c_[P, np.ones(len(P))] @ M2)
print(f"Planlinie {np.hypot(*np.diff(plan, axis=0).T).sum():.0f} m (UTM)")
json.dump({"M": M2.tolist(), "M_tour": M1.tolist(), "plan": plan.tolist()}, open("georef.json", "w"))
