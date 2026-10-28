# Fahrbahnhöhe aus der USGS-Punktwolke an den Bauwerken: je Punkt Laserpunkte im Umkreis von 4 m, die mehr als 1 m über dem
# Geländemodell liegen; davon das 10-%-Quantil (Fahrbahn; Geländer, Schilder, Fahrzeuge liegen darüber) -> deck.json
import json, math, time, numpy as np
from common import official
from ept import query, merc
r = json.load(open("dgm2026_10m.json")); s = np.array([x[0] for x in r]); la = np.array([x[1] for x in r]); lo = np.array([x[2] for x in r])
dem = np.array([x[3] for x in r]); k = official(s)
FENSTER = [(6.20, 6.40), (6.52, 6.72), (12.12, 12.28), (14.57, 14.73), (23.70, 23.92), (25.45, 25.66), (26.06, 26.34), (26.96, 27.14), (40.02, 40.32), (40.86, 41.04)]
X, Y = np.array([merc(a, b) for a, b in zip(la, lo)]).T
rad = 4.0 / math.cos(math.radians(42.3))
deck = np.full(len(s), np.nan); n = np.zeros(len(s), int); t0 = time.time()
for a_km, b_km in FENSTER:
    idx = np.where((k >= a_km * 1000) & (k <= b_km * 1000))[0]
    for c0 in range(0, len(idx), 6):
        ii = idx[c0:c0 + 6]
        P = query(X[ii].min() - rad, Y[ii].min() - rad, X[ii].max() + rad, Y[ii].max() + rad)
        for i in ii:
            m = ((P[:, 0] - X[i]) ** 2 + (P[:, 1] - Y[i]) ** 2 <= rad * rad) & (P[:, 2] > dem[i] + 1)
            n[i] = m.sum()
            if m.sum() >= 5: deck[i] = np.percentile(P[m, 2], 10)
    print(f"km {a_km:5.2f}-{b_km:5.2f}: {round(time.time() - t0)} s")
    for i in idx: print(f"   {k[i]/1000:7.3f}  Boden {dem[i]:6.1f}  Fahrbahn {deck[i]:6.1f}  n {n[i]:5d}")
json.dump({"deck": [None if not np.isfinite(v) else float(v) for v in deck], "n": n.tolist()}, open("deck.json", "w"))
