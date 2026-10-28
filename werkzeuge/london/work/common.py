# Linienmeter <-> offizielle Meter: Meilenmarken mit Lage gibt es nicht. Die OSM-Linie (Straßenmitte) ist 1,8 % länger als
# die vermessene Ideallinie und wird gleichmäßig von Start bis Ziel auf 42 195 m gestaucht.
import json, numpy as np
GL = json.load(open("gpx2026.json"))["d"][-1]
def official(s): return np.asarray(s, float) * 42195.0 / GL
def gpx_of(k): return np.asarray(k, float) * GL / 42195.0
