# Linienmeter <-> offizielle Meter. Die GPX-Linie des Veranstalters (parse.py, MySchweizMobil) ist ohne die Doppelpunkte 42 735 m lang,
# 540 m (1,28 %) länger als die vermessene Strecke: Sie folgt den Straßenmitten (im Median 1 m neben OSM) und biegt an jeder Ecke ab,
# statt Kurven und Plätze zu schneiden; die Linie im Streckenplan 2026 ist ebenso lang (plan.py). Sie wird gleichmäßig gestaucht
# (Faktor 0,98737), Start am Linienanfang (Quaibrücke; der Startstrich im Plan liegt 7 m daneben), Ziel am Linienende
# (Sechseläutenplatz; Zielstrich im Plan rund 20 m weiter). Die Kilometertafeln des Plans liegen bis 0,2 km daneben (marken_plan.json).
import json, os
import numpy as np
_D = os.path.dirname(os.path.abspath(__file__))
GL = json.load(open(os.path.join(_D, "gpx2026.json")))["d"][-1]
def official(s): return np.asarray(s, float) * (42195.0 / GL)
def gpx_of(k): return np.asarray(k, float) * (GL / 42195.0)
