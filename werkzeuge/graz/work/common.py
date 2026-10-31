# Linienmeter der Marathonlinie (strecke2026.json, zwei Runden der Garmin-Strecke) <-> offizielle Meter. Die Zuordnung rechnet strecke.py
# über die Ideallinie (ideal.py): Der Überschuss der gezeichneten Linie (0,7 % je Runde) fällt an Ecken und Zacken weg, nicht gleichmäßig.
import json, os
import numpy as np
_D = os.path.dirname(os.path.abspath(__file__))
_S = json.load(open(os.path.join(_D, "strecke2026.json")))
_LM = np.array(_S["lm"]); _OFF = np.array(_S["off"])
GL = _S["d"][-1]
def official(s): return np.interp(np.asarray(s, float), _LM, _OFF)
def gpx_of(k): return np.interp(np.asarray(k, float), _OFF, _LM)
