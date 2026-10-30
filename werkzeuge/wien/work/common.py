# Linienmeter <-> offizielle Meter: stückweise linear über die 42 Kilometermarken der Google-Karte des Veranstalters
# (marken.json, höchstens 12 m neben der Linie, Marke zu Marke 965–1049 Linienmeter, Median 1009). Start am Anfang der um 70 m
# verlängerten Linie (parse.py), Ziel an ihrem Ende (km 42 bis Ziel 196 m). Die Linie ist 42 593 m lang.
import json, numpy as np
GL = json.load(open("gpx2026.json"))["d"][-1]
_m = json.load(open("marken.json"))["km"]
_s = np.array([0.0] + [m[1] for m in _m] + [GL]); _k = np.array([0.0] + [m[0] * 1000 for m in _m] + [42195.0])
assert np.all(np.diff(_s) > 0) and np.all(np.diff(_k) > 0), "Marken nicht in Reihenfolge"
def official(s): return np.interp(np.asarray(s, float), _s, _k)
def gpx_of(k): return np.interp(np.asarray(k, float), _k, _s)
