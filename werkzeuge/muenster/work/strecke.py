# Linie des Kurses 2026 = eingepasste Planlinie (georef.json, ETRS89/UTM 32N) -> strecke2026.json {"pts": [[lat, lon]], "d": [laufende
# Länge, m, geodätisch GRS80]}. Muster: werkzeuge/duesseldorf/work/strecke.py.
import json
import numpy as np
from pyproj import Transformer, Geod
Ti = Transformer.from_crs(25832, 4326, always_xy=True)
X = np.array(json.load(open("georef.json"))["plan"])
X = X[np.r_[True, np.hypot(*np.diff(X, axis=0).T) > 0.01]]
lo, la = Ti.transform(X[:, 0], X[:, 1])
_, _, dd = Geod(ellps="GRS80").inv(lo[:-1], la[:-1], lo[1:], la[1:]); d = np.r_[0, np.cumsum(dd)]
print(f"{len(X)} Punkte, {d[-1]:.1f} m geodätisch; Start {la[0]:.6f} {lo[0]:.6f}, Ziel {la[-1]:.6f} {lo[-1]:.6f}")
json.dump({"pts": [[float(a), float(b)] for a, b in zip(la, lo)], "d": d.tolist()}, open("strecke2026.json", "w"))
