# Linienmeter <-> offizielle Meter: stückweise linear über die Kilometermarken des Veranstalters (alle 5 km und Halbmarathon,
# marken.json, auf der Linie höchstens 17 m daneben). Marke zu Marke 4967–5221 Linienmeter je 5 km; die Linie ist 42 686 m lang
# (Mittellinie der Straßen, gut 1 % länger als die vermessene Ideallinie).
import json, numpy as np
GL = json.load(open("gpx2026.json"))["d"][-1]
_m = json.load(open("marken.json"))["km"]
_s = np.array([0.0] + [m[1] for m in _m] + [GL]); _k = np.array([0.0] + [m[0] * 1000 for m in _m] + [42195.0])
_o = np.argsort(_s); _s, _k = _s[_o], _k[_o]
assert np.all(np.diff(_s) > 0) and np.all(np.diff(_k) > 0), "Marken nicht in Reihenfolge"
def official(s): return np.interp(np.asarray(s, float), _s, _k)
def gpx_of(k): return np.interp(np.asarray(k, float), _k, _s)
