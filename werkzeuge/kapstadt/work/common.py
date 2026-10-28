# Linienmeter <-> offizielle Meter: Kilometermarken mit Lage gibt es nicht (die Karte 2026 ist ein Bild ohne Koordinaten). Die auf
# OSM gelegte Linie (Straßenmitte) wird gleichmäßig von Start bis Ziel auf 42 195 m gestaucht.
import json, numpy as np
GL = json.load(open("gpx2026.json"))["d"][-1]
def official(s): return np.asarray(s, float) * 42195.0 / GL
def gpx_of(k): return np.asarray(k, float) * GL / 42195.0
