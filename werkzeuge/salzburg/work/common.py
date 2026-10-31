# Linienmeter der Linie der Google-Karte (linie.json) <-> offizielle Meter (Tabelle aus strecke.py: Ideallinie, Runde und Schleife je
# auf 21 097,5 m gestreckt).
import json, os
import numpy as np
_D = os.path.dirname(os.path.abspath(__file__))
_S = json.load(open(os.path.join(_D, "strecke.json")))
_LM = np.array(_S["lm"]); _OFF = np.array(_S["off"])
def official(s): return np.interp(np.asarray(s, float), _LM, _OFF)
def gpx_of(k):
    # Umkehrung; vor dem Start und nach dem Ziel ist off konstant: dort den ersten bzw. letzten passenden Linienmeter
    k = np.asarray(k, float); i0 = np.searchsorted(_OFF, 0, side="right") - 1; i1 = np.searchsorted(_OFF, _OFF[-1], side="left")
    return np.interp(k, _OFF[i0:i1 + 1], _LM[i0:i1 + 1])
