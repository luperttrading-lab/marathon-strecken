# Linienmeter <-> offizielle Meter. Die Linie des Veranstalters („ORIGINAL_STRECKE_2024_3D_DRAPED“, parse.py) ist die vermessene
# Strecke: in der Ebene (LV95) 42 194,5 m, geodätisch 42 193,5 m lang. Die Kilometer laufen gleichmäßig über sie (Faktor 1,00004);
# Start am Linienanfang (Höheweg Interlaken), Ziel am Linienende (Eigergletscher). Abgleich mit den Kilometerangaben des Veranstalters
# (Durchlaufzeiten, Verpflegung, Kontrollschlüsse): kmcheck.py.
import json, os
import numpy as np
_D = os.path.dirname(os.path.abspath(__file__))
GL = json.load(open(os.path.join(_D, "gpx2026.json")))["d"][-1]
F = 42195.0 / GL
def official(s): return np.asarray(s, float) * F
def gpx_of(k): return np.asarray(k, float) / F
