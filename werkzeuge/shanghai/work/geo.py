# Gemeinsame Helfer: UTM 51N (EPSG:32651) für metrische Rechnungen, Linien verdichten, OSM laden. Muster: werkzeuge/greatwall/work/geo.py.
# OSM liegt in WGS 84; chinesische Kartendienste verschieben ihre Koordinaten (GCJ-02), OSM und die Höhenmodelle nicht.
import json, math
import numpy as np
from pyproj import Transformer
_fw = Transformer.from_crs("EPSG:4326", "EPSG:32651", always_xy=True)
_bw = Transformer.from_crs("EPSG:32651", "EPSG:4326", always_xy=True)
def utm(lat, lon):
    x, y = _fw.transform(np.asarray(lon, float), np.asarray(lat, float)); return np.asarray(x), np.asarray(y)
def wgs(x, y):
    lon, lat = _bw.transform(np.asarray(x, float), np.asarray(y, float)); return np.asarray(lat), np.asarray(lon)
def dicht(P, d=5.0):
    """Polylinie (n×2) auf Abstände ≤ d verdichten."""
    P = np.asarray(P, float); out = [P[0]]
    for a, b in zip(P[:-1], P[1:]):
        n = max(1, int(math.ceil(np.hypot(*(b - a)) / d)))
        for k in range(1, n + 1): out.append(a + (b - a) * k / n)
    return np.array(out)
def laenge(P):
    P = np.asarray(P, float); return np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
def gleich(P, step):
    """Polylinie in gleichen Abständen neu abtasten."""
    P = np.asarray(P, float); s = laenge(P); t = np.arange(0, s[-1], step)
    if s[-1] - t[-1] > 1e-6: t = np.r_[t, s[-1]]
    return np.c_[np.interp(t, s, P[:, 0]), np.interp(t, s, P[:, 1])], t
_O = None
def osm():
    global _O
    if _O is None:
        d = json.load(open("../dl/osm_netz.json"))
        N = {int(k): v for k, v in d["nodes"].items()}
        W = {int(k): (tg, refs) for k, (tg, refs) in d["ways"].items()}
        _O = (N, W, {int(k): v for k, v in d["punkte"].items()})
    return _O
def kreuzung(n1, n2, nahe=None):
    """Knoten, an dem sich Wege der Namen n1 und n2 treffen (gemeinsamer Knoten; sonst die nächste Annäherung), UTM. Bei mehreren
    Treffern der nächste an nahe (UTM)."""
    N, W, _ = osm()
    k1 = {r for tg, refs in W.values() if tg.get("name") == n1 and "highway" in tg for r in refs}
    k2 = {r for tg, refs in W.values() if tg.get("name") == n2 and "highway" in tg for r in refs}
    gem = [r for r in k1 & k2 if r in N]
    if gem:
        P = np.array([np.r_[utm(*N[r])] for r in gem])
    else:
        from scipy.spatial import cKDTree
        A = np.array([np.r_[utm(*N[r])] for r in k1 if r in N]); B = np.array([np.r_[utm(*N[r])] for r in k2 if r in N])
        d, i = cKDTree(B).query(A); j = np.argsort(d)[:5]; P = (A[j] + B[i[j]]) / 2
    if nahe is None: return P.mean(0)
    return P[np.argmin(np.hypot(*(P - np.asarray(nahe)).T))]
