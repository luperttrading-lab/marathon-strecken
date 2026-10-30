# Linienmeter <-> offizielle Meter: stückweise linear über die Stützpunkte aus marken.py (km 5 Ecke Via Cristoforo Colombo /
# Circonvallazione Ostiense, Plätze mit Kilometermarke laut Straßenliste des Veranstalters: km 10, 11, 15, 25, 26, 37, 41),
# Start = Linienanfang, Ziel = Linienende (42 195 m). Die Linie läuft auf der Straßenmitte (OSM) und ist 3,3 % länger als die
# vermessene Strecke (43,60 km).
import json, numpy as np
GL = json.load(open("gpx2026.json"))["d"][-1]
_m = json.load(open("marken.json"))["km"]
_s = np.array([0.0] + [m[1] for m in _m] + [GL]); _k = np.array([0.0] + [m[0] * 1000 for m in _m] + [42195.0])
assert np.all(np.diff(_s) > 0) and np.all(np.diff(_k) > 0), "Marken nicht in Reihenfolge"
def official(s): return np.interp(np.asarray(s, float), _s, _k)
def gpx_of(k): return np.interp(np.asarray(k, float), _k, _s)
