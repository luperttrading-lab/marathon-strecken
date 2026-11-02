# Linienmeter <-> Streckenmeter. Bis 01.11.2026 wurde die MapPlanner-Linie (9 911 m) gleichmäßig auf die 9,85 km der Uhr des Nutzers
# gestaucht. Seit 02.11.2026 korrigiert korrektur.py die Linie nach den Markierungen des Nutzers (Start +20 m, vier Kurven, zwei Haken):
# 9 845,5 m, praktisch seine 9,85 km. Daher keine Stauchung mehr, L ist die gemessene Länge auf ganze Meter.
import json, os
import numpy as np
_D = os.path.dirname(os.path.abspath(__file__))
GL = json.load(open(os.path.join(_D, "linie.json")))["d"][-1]
L = float(round(GL))
def official(s): return np.asarray(s, float) * (L / GL)
def gpx_of(k): return np.asarray(k, float) * (GL / L)
