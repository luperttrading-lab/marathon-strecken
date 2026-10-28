# Offizielle Karte 2026 (../dl/pdf/26-BACM-COURSE-MAP-PRINT.pdf, Vektor-PDF): die Streckenlinie (Pfad in #00226A) ist von
# Ziel nach Start gezeichnet, ihre Enden liegen auf Start- und Ziellinie. Georeferenziert über zehn Ecken der Linie und die
# Kreuzungen derselben Straßen in OSM (affin, kleinste Quadrate) -> ../dl/kurs_karte.json [[lat, lon], …] vom Start zum Ziel
import json, numpy as np
from pyproj import Transformer
T = Transformer.from_crs(4326, 32616, always_xy=True); TI = Transformer.from_crs(32616, 4326, always_xy=True)
pts = np.array(json.load(open("../dl/pdf/kurs_pt.json")))
W = json.load(open("../dl/osm_wege.json"))["elements"]
nodes_of = {}
for w in W:
    nm = w["tags"].get("name", "")
    for g in w["geometry"]: nodes_of.setdefault(nm, {})[(round(g["lat"], 7), round(g["lon"], 7))] = (g["lat"], g["lon"])   # gemeinsame Knoten haben gleiche Koordinaten
def kreuzung(a, b):
    A = {}; [A.update(nodes_of.get(n, {})) for n in a]; B = {}; [B.update(nodes_of.get(n, {})) for n in b]
    gem = [A[n] for n in set(A) & set(B)]
    if gem: return np.mean(gem, axis=0)
    pa, pb = np.array(list(A.values())), np.array(list(B.values()))   # ohne gemeinsamen Knoten: die nächsten Punkte beider Straßen
    dd = ((pa[:, None, :] - pb[None, :, :]) ** 2).sum(-1); i, j = np.unravel_index(dd.argmin(), dd.shape)
    print('  ohne gemeinsamen Knoten:', a[0], '/', b[0], round(float(np.sqrt(dd[i, j])) * 111000), 'm Abstand')
    return (pa[i] + pb[j]) / 2
COL = ["South Columbus Drive", "North Columbus Drive", "North Upper Columbus Drive", "Upper North Columbus Drive"]
PAARE = [  # Ecke der Kartenlinie (Index), Straßen in OSM
    (2, ["East Roosevelt Road"], COL), (3, ["East Roosevelt Road"], ["South Michigan Avenue"]),
    (7, ["South Indiana Avenue"], ["East 35th Street"]), (21, ["South Loomis Street"], ["West 18th Street"]),
    (23, ["West Taylor Street"], ["South Halsted Street"]), (26, ["South Damen Avenue"], ["West Jackson Boulevard"]),
    (27, ["South Damen Avenue"], ["West Adams Street"]), (38, ["North Wells Street"], ["West North Avenue"]),
    (49, ["North Broadway"], ["North Sheridan Road"]), (76, ["East Grand Avenue"], COL)]
src = np.array([pts[i] for i, _, _ in PAARE]); ll = np.array([kreuzung(a, b) for _, a, b in PAARE])
dst = np.c_[T.transform(ll[:, 1], ll[:, 0])]
A = np.c_[src, np.ones(len(src))]; coef, *_ = np.linalg.lstsq(A, dst, rcond=None)
res = A @ coef - dst
for (i, a, b), r in zip(PAARE, res): print(f"Ecke {i:2d} {a[0][:22]:22s} / {b[0][:22]:22s} Rest {np.hypot(*r):5.1f} m")
m_pro_pt = np.sqrt(abs(np.linalg.det(coef[:2]))); print("Maßstab", round(m_pro_pt, 2), "m je pt; Rest RMS", round(float(np.sqrt((res ** 2).sum(1).mean())), 1), "m")
xy = np.c_[pts, np.ones(len(pts))] @ coef
lo, la = TI.transform(xy[:, 0], xy[:, 1])
line = [[float(a), float(b)] for a, b in zip(la, lo)][::-1]          # vom Start zum Ziel
json.dump({"line": line, "coef": coef.tolist()}, open("../dl/kurs_karte.json", "w"))
L = np.hypot(*np.diff(xy, axis=0).T).sum(); print("Kartenlinie", round(L), "m; Start", line[0], "Ziel", line[-1])
