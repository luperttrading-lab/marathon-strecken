# Linienmeter <-> offizielle Meter. Die Linie ist aus OSM-Wegen nachgezeichnet (route_osm.py, geführt vom Streckenplan des Veranstalters)
# und rund 43,4 km lang, 2,8 % mehr als 42,195 km. Eine vermessene Linie oder Kilometermarken veröffentlicht der Veranstalter nicht; seine
# Kilometer der Posten (5, 10, 12,5, 15 …) sind runde Werte. Deshalb gleichmäßig auf 42,195 km gestaucht (wie Zermatt und Rennsteig, dort
# gedehnt): Start am Linienanfang (Schaanerstrasse in Bendern), Ziel am Linienende (Malbun, Schlucher-Treff).
import json, os
import numpy as np
_D = os.path.dirname(os.path.abspath(__file__))
GL = json.load(open(os.path.join(_D, "gpx2026.json")))["d"][-1]
F = 42195.0 / GL
def official(s): return np.asarray(s, float) * F
def gpx_of(k): return np.asarray(k, float) / F
