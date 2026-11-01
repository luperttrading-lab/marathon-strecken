# Linienmeter <-> Streckenmeter. Die in MapPlanner gezeichnete Linie ist 9 911 m lang; gelaufen sind laut Nutzer 9,85 km (Ecken
# abgekürzt). Sie wird gleichmäßig gestaucht (Faktor 0,99381), wie die Marathons auf 42 195 m; Start am Linienanfang, Ziel am Linienende
# (33 m neben dem Start).
import json, os
import numpy as np
L = 9850.0
_D = os.path.dirname(os.path.abspath(__file__))
GL = json.load(open(os.path.join(_D, "linie.json")))["d"][-1]
def official(s): return np.asarray(s, float) * (L / GL)
def gpx_of(k): return np.asarray(k, float) * (GL / L)
