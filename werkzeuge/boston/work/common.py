# Linienmeter <-> offizielle Meter: Kilometer- oder Meilenpunkte mit Lage nennt die B.A.A. nicht; die OSM-Linie ist zu lang
# (Straßenmitte statt Ideallinie) und wird gleichmäßig von Start bis Ziel auf 42 195 m gestaucht.
import json, numpy as np
GL = json.load(open("gpx2026.json"))["d"][-1]
def official(s): return np.asarray(s, float) * 42195.0 / GL
def gpx_of(k): return np.asarray(k, float) * GL / 42195.0
