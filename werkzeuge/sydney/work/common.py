# Linienmeter <-> offizielle Meter: Kilometermarken mit Lage gibt es nicht. Die offizielle Linie (42 242 m) wird gleichmäßig von
# Start bis Ziel auf 42 195 m gestaucht.
import json, numpy as np
GL = json.load(open("gpx2026.json"))["d"][-1]
def official(s): return np.asarray(s, float) * 42195.0 / GL
def gpx_of(k): return np.asarray(k, float) * GL / 42195.0
