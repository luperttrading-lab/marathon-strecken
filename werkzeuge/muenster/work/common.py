# Linienmeter <-> offizielle Meter: stückweise gleichmäßig zwischen den Kilometerkreisen des Streckenplans (eichung.json, eichung.py),
# Start = Anfang der Planlinie, Ziel = ihr Ende (42 195 m).
import json, numpy as np
E = np.array(json.load(open("eichung.json"))); g = json.load(open("strecke2026.json")); GL = g["d"][-1]
def official(s): return np.interp(np.asarray(s, dtype=float), E[:, 0], E[:, 1])
def gpx_of(k): return np.interp(np.asarray(k, dtype=float), E[:, 1], E[:, 0])
