# Linienmeter <-> offizielle Meter. Die Strava-Linie des Veranstalters (parse.py) ist nach Entfernen der Zacken 42 611 m lang,
# 416 m (1,0 %) länger als die vermessene Strecke: Sie läuft auf den Straßenmitten und biegt rechtwinklig ab, statt die Kurven zu
# schneiden. Sie wird gleichmäßig gestaucht (Faktor 0,99024), Start am Linienanfang (Ala Moana Boulevard), Ziel am Linienende
# (Kalākaua Avenue am Kapiʻolani Park). Kilometermarken mit Lage gibt es nicht (marken.py vergleicht mit dem Streckenplan).
import json, os
import numpy as np
_D = os.path.dirname(os.path.abspath(__file__))
GL = json.load(open(os.path.join(_D, "gpx2026.json")))["d"][-1]
def official(s): return np.asarray(s, float) * (42195.0 / GL)
def gpx_of(k): return np.asarray(k, float) * (GL / 42195.0)
