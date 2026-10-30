# Gemeinsame Helfer: UTM 50N (EPSG:32650) für metrische Rechnungen, Linien verdichten, OSM laden.
import json, math
import numpy as np
from pyproj import Transformer
_fw = Transformer.from_crs("EPSG:4326", "EPSG:32650", always_xy=True)
_bw = Transformer.from_crs("EPSG:32650", "EPSG:4326", always_xy=True)
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
def osm():
    d = json.load(open("../dl/osm_all.json"))
    N = {int(k): v for k, v in d["nodes"].items()}
    W = {int(k): (tg, refs) for k, (tg, refs) in d["ways"].items()}
    return N, W, {int(k): v for k, v in d["ntags"].items()}
