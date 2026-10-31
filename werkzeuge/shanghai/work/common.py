# Linienmeter <-> offizielle Meter. Die Linie (linie.py: Streckenplan 2025 auf den OSM-Straßen) wird gleichmäßig auf 42 195 m
# gebracht, Start am Linienanfang (Zhongshan Dongyi Lu), Ziel am Linienende (Ziellinie im Xujiahui-Sportpark). Die Kilometerkreise des
# Plans sind von Hand gezeichnet und taugen nicht zum Eichen (marken.py zeigt den Abgleich).
import json, os
import numpy as np
_D = os.path.dirname(os.path.abspath(__file__))
GL = json.load(open(os.path.join(_D, "linie2025.json")))["d"][-1]
def official(s): return np.asarray(s, float) * (42195.0 / GL)
def gpx_of(k): return np.asarray(k, float) * (GL / 42195.0)
