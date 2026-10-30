# Linienmeter <-> offizielle Meter. Der Veranstalter veröffentlicht keine Lage seiner Kilometerschilder; seine OpenRunner-Linie
# misst 42 277 m (GRS80; OpenRunner selbst 42 245 m), 0,2 % mehr als 42 195 m. Gleichmäßig gestaucht (Start = Linienanfang,
# Ziel = Linienende); die Kilometerangaben der Stände (Plaquette 2026) und die km-Schilder der Karte im Läuferheft passen dazu.
import json, numpy as np
GL = json.load(open("gpx2026.json"))["d"][-1]
def official(s): return np.asarray(s, float) * 42195.0 / GL
def gpx_of(k): return np.asarray(k, float) * GL / 42195.0
