# Linienmeter <-> offizielle Meter. Die GPX-Linie des Veranstalters (parse.py, MySchweizMobil, „SCML_42KM_DEFINITIV“) ist ohne die
# Doppelpunkte 42 808 m lang, 613 m (1,45 %) länger als die vermessene Strecke: Sie folgt den Straßenmitten und biegt an jeder Ecke ab.
# Geeicht wird stückweise linear über die 42 Kilometermarken der Karte des Veranstalters (kmmarken.py; 1008–1020 Linienmeter je km),
# Start am Linienanfang (Haldenstrasse; der Startpunkt der Karte liegt 13 m daneben), Ziel am Linienende (Verkehrshaus).
import json, os
import numpy as np
_D = os.path.dirname(os.path.abspath(__file__))
GL = json.load(open(os.path.join(_D, "gpx2026.json")))["d"][-1]
_K = json.load(open(os.path.join(_D, "kmmarken.json")))
_S = np.array([0.0] + [s for _, s in _K] + [GL]); _O = np.array([0.0] + [k * 1000.0 for k, _ in _K] + [42195.0])
def official(s): return np.interp(np.asarray(s, float), _S, _O)
def gpx_of(k): return np.interp(np.asarray(k, float), _O, _S)
