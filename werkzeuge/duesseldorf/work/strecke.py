# Linie des Kurses 2026 = eingepasste Planlinie (georef.json, ETRS89/UTM 32N) -> strecke2026.json {"pts": [[lat, lon]], "d": [laufende
# Länge, m, geodätisch GRS80]}. Die Planlinie liegt im Median 2 m neben einer OSM-Straße (95 % bis 6 m; ein paar gerundete Ecken bis
# 16 m), die Tour von Visit Düsseldorf im Median 1 m daneben. Gegen eine Linie auf den Straßenmitten (Kartenabgleich über das
# OSM-Netz, ausprobiert und verworfen: 43,3 km, Zickzack über Rad- und Gehwege und rechtwinklige Ecken) ist die gezeichnete Linie
# näher an der vermessenen Ideallinie: Ecken gerundet, 42,39 km statt 42,195 (0,5 % zu lang).
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
