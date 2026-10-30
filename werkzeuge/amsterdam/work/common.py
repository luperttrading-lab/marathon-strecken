# Linienmeter <-> offizielle Meter: gleichmäßig über die ganze Linie (Start und Ziel auf der Bahn im Stadion). Die Linie folgt der
# Straßenmitte und ist 43,10 km lang (2,1 % mehr als 42,195 km; das Höhenbild des Veranstalters ist über 42,9 km gezeichnet und
# stimmt Kilometer für Kilometer mit der Linie überein). Die Kilometerkreise des Streckenplans (marken.py) liegen nach der
# Zuordnung bis 0,4 km neben dieser Eichung; der Plan ist gezeichnet und taugt für einzelne Marken nicht.
import json, numpy as np
GL = json.load(open("gpx2026.json"))["d"][-1]
def official(s): return np.asarray(s, float) * 42195.0 / GL
def gpx_of(k): return np.asarray(k, float) * GL / 42195.0
