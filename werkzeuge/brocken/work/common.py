# Linienmeter der gelegten Linie (gelegt.json, match.py) <-> offizielle Meter. Die Linie ist 42 284 m lang (GPX des Veranstalters 42 253 m);
# die Kilometer sind gleichmäßig auf 42 195 m gestreckt (Faktor 0,9979). Abgleich mit den Kilometerdreiecken der Streckenkarte
# (georef.py): km 5, 10, 15, 20, 30, 35, 40 liegen hier 0,1–0,3 km daneben; das Dreieck „25 km“ steht 1,4 km früher (km 23,6).
import json, os
import numpy as np
_D = os.path.dirname(os.path.abspath(__file__))
_S = json.load(open(os.path.join(_D, "gelegt.json")))
GL = _S["d"][-1]; L = 42195.0
def official(s): return np.asarray(s, float) * (L / GL)
def gpx_of(k): return np.asarray(k, float) * (GL / L)
