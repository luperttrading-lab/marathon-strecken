# Linienmeter <-> offizielle Meter. Die GPX-Linie des Veranstalters (parse.py, MySchweizMobil, „GZM Marathon 2026“) ist ohne die
# Doppelpunkte und die 41 Stichwege hin und zurück 41 621 m lang, 574 m (1,36 %) kürzer als 42,195 km. Kilometermarken gibt es nicht; die
# Kilometerangaben des Veranstalters widersprechen sich (Sunnegga km 31,7, 32,0, 32,4 und 32,5) und folgen an mehreren Stellen der Länge
# der Rohdatei mit den Stichwegen (Zermatt Bahnhofplatz 21,1, Sunnegga 32,4, Patrullarve 28,6; Rohdatei 42,62 km). Deshalb gleichmäßig
# gedehnt (wie Rennsteig): Start am Linienanfang (Umfahrungsstrasse St. Niklaus), Ziel am Linienende (Riffelberg).
import json, os
import numpy as np
_D = os.path.dirname(os.path.abspath(__file__))
GL = json.load(open(os.path.join(_D, "gpx2026.json")))["d"][-1]
F = 42195.0 / GL
def official(s): return np.asarray(s, float) * F
def gpx_of(k): return np.asarray(k, float) / F
