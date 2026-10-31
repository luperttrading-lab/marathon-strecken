# Streckenplan (PDF-Punkte) -> Lage (ETRS89 / UTM 32N, EPSG:25832), affin (6 Werte). Ausgang: grob.json (zehn Ortsbeschriftungen gegen
# Nominatim, auf etwa 70 m genau). Dann an den Straßen in OSM (../dl/osm_netz.json, alle Wege mit highway außer Treppen): jeder
# Planpunkt zum nächsten Straßenpunkt, Ausreißer weg, wiederholt (ICP), mit enger werdendem Fangradius 150 → 60 → 30 → 20 m. Muster:
# werkzeuge/duesseldorf/work/georef.py (dort zuerst an einer Tour von Visit Düsseldorf; eine solche Gegenlinie gibt es hier nicht).
# -> georef.json {"M": 3×2-Matrix [x, y, 1] @ M = [E, N], "plan": [[E, N] je PDF-Punkt], "abstand": [Abstand je Punkt zur OSM-Straße]}
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
o = json.load(open("../dl/osm_netz.json")); NO = o["nodes"]
Z = []
for wid, (tg, refs) in o["ways"].items():
    if tg.get("highway") in (None, "steps", "proposed", "construction", "platform", "elevator", "bus_stop"): continue
    pts = [NO[str(r)] for r in refs if str(r) in NO]
    if len(pts) < 2: continue
    x, y = T.transform([q[1] for q in pts], [q[0] for q in pts]); A = np.c_[x, y]
    Z.append(dicht(A, 2.0) if np.hypot(*np.diff(A, axis=0).T).sum() > 2 else A)
Z = np.vstack(Z)
M = np.array(json.load(open("grob.json"))["M"])
for g in (150, 60, 30, 20):
    M, dist = icp(Z, M, g)
    print(f"Fangradius {g:3d} m: Abstand Median {np.median(dist):.1f} m, 90 % {np.percentile(dist, 90):.1f} m, 99 % {np.percentile(dist, 99):.1f} m")
M0 = np.array(json.load(open("grob.json"))["M"])
print("Maßstab x/y m/pt", np.hypot(*M[0]).round(4), np.hypot(*M[1]).round(4), "Winkel zwischen den Achsen",
      round(float(np.degrees(np.arccos(np.dot(M[0], M[1]) / np.hypot(*M[0]) / np.hypot(*M[1])))), 2), "°; Verschiebung gegen grob: Mittel",
      np.round((PH @ M - PH @ M0).mean(0), 1), "max", np.round(np.hypot(*(PH @ M - PH @ M0).T).max(), 1), "m")
plan = np.c_[P, np.ones(len(P))] @ M
d, _ = cKDTree(Z).query(plan)
print(f"Planlinie {np.hypot(*np.diff(plan, axis=0).T).sum():.0f} m (UTM); Planpunkte neben OSM: Median {np.median(dist):.1f} m")
json.dump({"M": M.tolist(), "plan": plan.tolist(), "abstand": d.tolist()}, open("georef.json", "w"))
