# (Name schnur_szg.py, damit parallele Sitzungen, die „ideal_w.py“ beenden, diesen Lauf nicht treffen.) Bandbreite w der Ideallinie (kürzeste Linie im Band ±w m um die Linie der Google-Karte, ideal.py), bei der der Marathon vom Start
# bis zum Ziel 42 195 m misst. Muster: werkzeuge/freiburg/work/ideal_w.py. Schreibt ideal_w.json {w: Länge Start–Ziel} und je w
# ideal_<w>.json mit der Zuordnung Linienmeter -> Meter auf der Ideallinie. Aufruf: python3 schnur_szg.py 2 4 6 …
import json, sys, time
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
from ideal import ideal, laenge, dicht
T = Transformer.from_crs(4326, 31258, always_xy=True)   # MGI / Austria GK M31
g = json.load(open("linie.json")); Q = np.array(g["pts"]); d = np.array(g["d"])
m = json.load(open("marken.json"))["punkte"]
s0_ = next(p[1] for p in m if p[3].startswith("Start")); s1_ = next(p[1] for p in m if p[3].startswith("FINISH"))
# Linie vom Lot des Starts bis zum Lot des Ziels
sel = (d > s0_) & (d < s1_)
la = np.r_[np.interp(s0_, d, Q[:, 0]), Q[sel, 0], np.interp(s1_, d, Q[:, 0])]; lo = np.r_[np.interp(s0_, d, Q[:, 1]), Q[sel, 1], np.interp(s1_, d, Q[:, 1])]
dz = np.r_[s0_, d[sel], s1_]
E, N = T.transform(lo, la); X = np.c_[E, N]
try: erg = json.load(open("ideal_w.json"))
except FileNotFoundError: erg = {}
for w in [float(x) for x in sys.argv[1:]]:
    t = time.time(); P, s0 = ideal(X, w, schritt=2.0, iter=2500)
    erg[f"{w:g}"] = laenge(P); print(f"w = {w} m: Start–Ziel {erg[f'{w:g}']:.1f} m ({time.time() - t:.0f} s)", flush=True)
    F, sf = dicht(X, 0.5); b = cKDTree(F); dd, j = b.query(P, k=40)
    ok = np.abs(sf[j] - s0[:, None]) < 80; dd = np.where(ok, dd, np.inf); mm = np.argmin(dd, axis=1)
    lm = np.maximum.accumulate(sf[j[np.arange(len(P)), mm]]); lm[0] = 0; lm[-1] = sf[-1]
    ia = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
    du = np.r_[0, np.cumsum(np.hypot(*np.diff(X, axis=0).T))]
    lo2, la2 = Transformer.from_crs(31258, 4326, always_xy=True).transform(P[:, 0], P[:, 1])
    json.dump({"w": w, "lm": np.interp(lm, du, dz).round(2).tolist(), "ideal": ia.round(2).tolist(),
               "pts": [[round(a, 7), round(b, 7)] for a, b in zip(la2[::5], lo2[::5])]}, open(f"ideal_{w:g}.json", "w"))
    json.dump(erg, open("ideal_w.json", "w"))
