# Linienmeter <-> offizielle Meter. Die GPX-Linie des Veranstalters (parse.py) ist 42 166,6 m lang, 28,4 m kürzer als die vermessene
# Strecke; sie wird gleichmäßig gestreckt (Faktor 1,00067), Start am Linienanfang (Lidingövägen), Ziel am Linienende (Ziellinie im
# Stadion). Die Kilometermarken der dynamischen Karte des Veranstalters liegen von Hand gesetzt bis 225 m daneben und taugen nicht
# zum Eichen (marken.py zeigt den Abgleich).
import json, os
import numpy as np
_D = os.path.dirname(os.path.abspath(__file__))
GL = json.load(open(os.path.join(_D, "gpx2026.json")))["d"][-1]
def official(s): return np.asarray(s, float) * (42195.0 / GL)
def gpx_of(k): return np.asarray(k, float) * (GL / 42195.0)
