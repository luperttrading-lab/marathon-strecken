# Bodenhöhen alle 10 m (Linienmeter) aus TINITALY/1.1 (INGV, 10-m-Raster, tinitaly.py), bilinear. Höhen über dem Meer
# (orthometrisch, Bezug der italienischen Landesvermessung, Pegel Genua). Warum dieses Modell und nicht ein Laser-Modell: siehe
# UEBERGABE.md, „Höhe“. -> dgm_tinitaly.json [Linienmeter, Breite, Länge, Höhe] (angleich.py gleicht sie an die Höhen der Regione Lazio an)
import json, numpy as np
from tinitaly import hoehe
g = json.load(open("gpx2026.json")); pts, d = g["pts"], np.array(g["d"])
la_ = np.array([p[0] for p in pts]); lo_ = np.array([p[1] for p in pts])
ss = np.append(np.arange(0, d[-1], 10.0), d[-1]); la = np.interp(ss, d, la_); lo = np.interp(ss, d, lo_)
h, q = zip(*[hoehe(a, b) for a, b in zip(la, lo)])
from collections import Counter
print("Blätter:", dict(Counter(q)), "fehlend", sum(v is None for v in h))
assert all(v is not None for v in h), "Lücken im Modell"
json.dump([[float(s), float(a), float(b), round(v, 3)] for s, a, b, v in zip(ss, la, lo, h)], open("dgm_tinitaly.json", "w"))
print(len(h), "Punkte, Höhe min/max", round(min(h), 2), round(max(h), 2))
