# Linienmeter <-> offizielle Meter: stückweise linear über die 42 Kilometermarken und den Halbmarathon der Google-Karte des
# Veranstalters (marken.json, höchstens 12 m neben der Linie, Marke zu Marke 986–1014 Linienmeter). Die Linie ist 42 193 m lang.
import json, numpy as np
GL = json.load(open("gpx2026.json"))["d"][-1]
_m = json.load(open("marken.json"))["km"]
_s = np.array([0.0] + [s for km, s, _ in _m] + [GL]); _k = np.array([0.0] + [km * 1000 for km, s, _ in _m] + [42195.0])
_o = np.argsort(_s); _s, _k = _s[_o], _k[_o]
assert np.all(np.diff(_s) > 0) and np.all(np.diff(_k) > 0), "Marken nicht in Reihenfolge"
def official(s): return np.interp(np.asarray(s, float), _s, _k)
def gpx_of(k): return np.interp(np.asarray(k, float), _k, _s)
