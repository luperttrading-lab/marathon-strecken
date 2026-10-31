# Bandbreite w der Ideallinie, bei der die Runde der RaceDayMap 21 097,5 m misst (Halbmarathon = eine Runde). Nur Abgleich und
# Grundlage für common.py: schreibt ideal_w.json {w: Länge} und für das gewählte w die Zuordnung Linienmeter -> Meter auf der Ideallinie.
import json, sys, time
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
from ideal import ideal, laenge, dicht
T = Transformer.from_crs(4326, 25832, always_xy=True)
g = json.load(open("runde.json")); Q = np.array(g["pts"]); d = np.array(g["d"])
E, N = T.transform(Q[:, 1], Q[:, 0]); X = np.c_[E, N]
erg = {}
for w in [float(x) for x in sys.argv[1:]]:
    t = time.time(); P, s0 = ideal(X, w, schritt=2.0, iter=2500)
    erg[w] = laenge(P); print(f"w = {w} m: Runde {erg[w]:.1f} m ({time.time() - t:.0f} s)", flush=True)
    # Zuordnung: jeder Punkt der Ideallinie -> nächster Punkt der Ausgangslinie (im Fenster), monoton
    F, sf = dicht(X, 0.5); b = cKDTree(F); dd, j = b.query(P, k=40)
    ok = np.abs(sf[j] - s0[:, None]) < 80; dd = np.where(ok, dd, np.inf); m = np.argmin(dd, axis=1)
    lm = np.maximum.accumulate(sf[j[np.arange(len(P)), m]]); lm[0] = 0; lm[-1] = sf[-1]
    ia = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
    # Linienmeter (UTM) -> geodätische Linienmeter der runde.json
    du = np.r_[0, np.cumsum(np.hypot(*np.diff(X, axis=0).T))]
    json.dump({"w": w, "lm": np.interp(lm, du, d).round(2).tolist(), "ideal": ia.round(2).tolist()}, open(f"ideal_{w:g}.json", "w"))
json.dump(erg, open("ideal_w.json", "w"))
