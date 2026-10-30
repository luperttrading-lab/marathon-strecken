# Linienmeter <-> offizielle Meter: stückweise linear über die Stützpunkte aus marken.py (Steine der Klassischen Marathonstrecke:
# Mittel von 33 und 34, 37, 39), Start = Linienanfang, Ziel = Linienende (42 195 m). Bis km 33,5 ist die Linie gleichmäßig um 0,45 %
# gestaucht (153 m), danach liegt sie fast genau 160 m über dem Kilometer.
import json, os
import numpy as np
_D = os.path.dirname(os.path.abspath(__file__))
GL = json.load(open(os.path.join(_D, "gpx2026.json")))["d"][-1]
_m = json.load(open(os.path.join(_D, "marken.json")))["km"]
_s = np.array([0.0] + [m[1] for m in _m] + [GL]); _k = np.array([0.0] + [m[0] * 1000 for m in _m] + [42195.0])
assert np.all(np.diff(_s) > 0) and np.all(np.diff(_k) > 0), "Marken nicht in Reihenfolge"
def official(s): return np.interp(np.asarray(s, float), _s, _k)
def gpx_of(k): return np.interp(np.asarray(k, float), _k, _s)
