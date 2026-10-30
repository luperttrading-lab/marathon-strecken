# Streckenplan des Veranstalters (Vektor-PDF, Seitenkoordinaten in pt) auf die Karte einpassen, damit Linie und Kilometerkreise
# auf die OSM-Straßen gelegt werden können. Der Plan ist eine gezeichnete Stadtkarte, aber verzerrt (affin über acht
# Bahnhofssymbole bis 360 m daneben). Deshalb ICP (iterative closest point) in zwei Klassen: weiße Straßenlinien des Plans
# (Breite 2,5–8 pt) auf OSM-Straßen (auch service und track, ohne Rad- und Fußwege) und Uferlinien der Wasserflächen des Plans
# auf die Uferlinien der OSM-Wasserflächen (wasser.py; im Polder an der Amstel gibt es kaum Straßen). Alle 3 m bzw. 1,5 pt ein
# Punkt, jeder Punkt sucht seinen Partner nur in der eigenen Klasse. Erst global affin, dann lokal affin in Fenstern um
# Stützpunkte alle 60 pt der roten Linie (Radius 200 pt, dann 110 pt), die Fenster gaußförmig gewichtet überblendet.
# -> ../dl/einpassung.json (Stützpunkte mit ihren lokalen Abbildungen nach RD New, EPSG:28992)
import json, sys
import numpy as np, pymupdf
from pyproj import Transformer
from scipy.spatial import cKDTree
T = Transformer.from_crs(4326, 28992, always_xy=True)
doc = pymupdf.open("../dl/parcours-2026-v2.pdf"); p = doc[0]
def bez(p0, p1, p2, p3, n):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3
S = []
for d in p.get_drawings():
    if d["type"] != "s" or tuple(round(x, 2) for x in (d.get("color") or ())) != (1.0, 1.0, 1.0) or not 2.5 <= (d.get("width") or 0) <= 8: continue
    for it in d["items"]:
        if it[0] == "l": a, b = np.array([it[1].x, it[1].y]), np.array([it[2].x, it[2].y]); n = max(2, int(np.hypot(*(b - a)) / 1.5) + 1); S.append(a + np.linspace(0, 1, n)[:, None] * (b - a))
        elif it[0] == "c":
            q = [np.array([v.x, v.y]) for v in it[1:5]]; n = max(4, int(sum(np.hypot(*(q[i + 1] - q[i])) for i in range(3)) / 1.5) + 1); S.append(bez(*q, n))
S = np.unique(np.round(np.vstack(S), 1), axis=0)
W = []
for d in p.get_drawings():
    if d["type"] != "fs" or tuple(round(x, 2) for x in (d.get("fill") or ())) != (0.76, 0.91, 0.94): continue
    for it in d["items"]:
        if it[0] == "l": a, b = np.array([it[1].x, it[1].y]), np.array([it[2].x, it[2].y]); n = max(2, int(np.hypot(*(b - a)) / 1.5) + 1); W.append(a + np.linspace(0, 1, n)[:, None] * (b - a))
        elif it[0] == "c":
            q = [np.array([v.x, v.y]) for v in it[1:5]]; n = max(4, int(sum(np.hypot(*(q[i + 1] - q[i])) for i in range(3)) / 1.5) + 1); W.append(bez(*q, n))
W = np.unique(np.round(np.vstack(W), 1), axis=0)
# OSM-Straßen
net = json.load(open("../dl/osm_netz.json")); K = net["knoten"]
KLASSEN = {"trunk", "primary", "secondary", "tertiary", "unclassified", "residential", "living_street", "pedestrian",
           "primary_link", "secondary_link", "tertiary_link", "trunk_link", "service", "track"}
O = []
for w in net["wege"].values():
    if w["tags"].get("highway") not in KLASSEN or w["tags"].get("tunnel") in ("yes",): continue
    ll = np.array([K[str(k)] for k in w["nd"] if str(k) in K])
    if len(ll) < 2: continue
    xy = np.c_[T.transform(ll[:, 1], ll[:, 0])]
    for a, b in zip(xy[:-1], xy[1:]):
        n = max(2, int(np.hypot(*(b - a)) / 3) + 1); O.append(a + np.linspace(0, 1, n)[:, None] * (b - a))
O = np.vstack(O)
OW = []
for ll in json.load(open("../dl/osm_wasser.json")):
    ll = np.array(ll); xy = np.c_[T.transform(ll[:, 1], ll[:, 0])]
    for a, b in zip(xy[:-1], xy[1:]):
        n = max(2, int(np.hypot(*(b - a)) / 3) + 1); OW.append(a + np.linspace(0, 1, n)[:, None] * (b - a))
OW = np.vstack(OW)
# Klasse in einer dritten Koordinate: Wasser 100 km entfernt, so findet jeder Punkt nur Partner seiner Klasse
O3 = np.vstack([np.c_[O, np.zeros(len(O))], np.c_[OW, np.full(len(OW), 1e5)]]); bO = cKDTree(O3)
print(len(S), "Straßenpunkte und", len(W), "Uferpunkte im Plan,", len(O), "und", len(OW), "in OSM")
# Startwert: affin über die Bahnhofssymbole
P0 = {(1128.2, 50.9): (52.37890, 4.90058), (411.0, 1158.9): (52.33881, 4.87319), (752.2, 1118.9): (52.33703, 4.89023),
      (1637.2, 1834.0): (52.31224, 4.94709), (1067.9, 529.5): (52.3613, 4.9078), (989.0, 372.0): (52.3672, 4.9024),
      (955.9, 235.2): (52.3721, 4.9007), (1140.5, 728.9): (52.3552, 4.9116)}
M = np.linalg.lstsq(np.array([[x, y, 1] for x, y in P0]), np.array([T.transform(lo, la) for la, lo in P0.values()]), rcond=None)[0]
rot = [np.array(z) for z in json.load(open("../dl/pdf_linie.json"))["rot"] if len(z) > 30]
R = np.vstack(rot); bR = cKDTree(R)
# nur Planstraßen in der Nähe der Strecke (dort gibt es OSM-Daten)
S = S[bR.query(S)[0] < 160]; W = W[bR.query(W)[0] < 160]
KL = np.r_[np.zeros(len(S)), np.full(len(W), 1e5)]; S = np.vstack([S, W])
def icp(Sx, M, schwellen, mind=60, kl=None):
    A = np.c_[Sx, np.ones(len(Sx))]
    for thr in schwellen:
        for _ in range(4):
            Y = A @ M; dd, ii = bO.query(np.c_[Y, kl])
            sel = dd < thr
            if sel.sum() < mind: return M, None
            M = np.linalg.lstsq(A[sel], O3[ii[sel], :2], rcond=None)[0]
    dd = bO.query(np.c_[A @ M, kl])[0]
    return M, float(np.median(dd))
M, med = icp(S, M, [400, 300, 200, 150, 100, 80, 60, 50, 40, 30, 25, 20], kl=KL)
print("global affin: Median", round(med, 1), "m")
# Stützpunkte alle 60 pt entlang der roten Linie
stuetz = []
for z in rot:
    dl = np.r_[0, np.cumsum(np.hypot(*np.diff(z, axis=0).T))]
    for s in np.arange(0, dl[-1] + 1, 60.0): stuetz.append([np.interp(s, dl, z[:, 0]), np.interp(s, dl, z[:, 1])])
stuetz = np.array(stuetz); stuetz = stuetz[np.r_[True, np.hypot(*np.diff(stuetz, axis=0).T) > 20]]
bS = cKDTree(S)
lokal, guete = [], []
for c in stuetz:
    Mk = M; mk_med = 99.0
    for rad, schw in ((200, [80, 60, 45, 35, 25]), (110, [30, 22, 16, 12, 10])):
        idx = bS.query_ball_point(c, rad)
        if len(idx) < 150: continue
        Mn, med = icp(S[idx], Mk, schw, kl=KL[idx])
        if med is not None: Mk = Mn; mk_med = med
    lokal.append(Mk); guete.append(mk_med)
    print(f"Stützpunkt {c[0]:6.0f} {c[1]:6.0f}: Median {mk_med:5.1f} m, Verschiebung gegen global {np.hypot(*(np.r_[c, 1] @ (Mk - M))):5.0f} m", flush=True)
json.dump({"global": M.tolist(), "stuetz": stuetz.tolist(), "lokal": [m.tolist() for m in lokal], "median": guete, "sigma": 70.0},
          open("../dl/einpassung.json", "w"))
print("Median über alle Fenster", round(float(np.median(guete)), 1), "m, schlechtestes", round(max(guete), 1))
