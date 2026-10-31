# Linienmeter <-> offizielle Meter. Die Linie aus der My-Maps-Karte des Veranstalters (parse.py) ist 42 279 m lang, 84 m (0,2 %)
# länger als die vermessene Strecke: Sie folgt den Straßen (im Median 1,8 m neben einem OSM-Weg, höchstens 10 m), läuft aber auf der
# Mitte und biegt rechtwinklig ab, statt die Kurven zu schneiden. Sie wird gleichmäßig gestaucht (Faktor 0,99801), Start am
# Linienanfang (Friedrichswall vor dem Neuen Rathaus), Ziel am Linienende (27 m östlich davon). Die Kilometerpunkte der Karte sind
# von Hand gesetzt (Abstand 736–1211 m), die der Stadt (Digitaler Zwilling) gleichmäßig über dieselbe Linie verteilt; beide taugen
# nicht zum Eichen (marken.py).
import json, os
import numpy as np
_D = os.path.dirname(os.path.abspath(__file__))
GL = json.load(open(os.path.join(_D, "gpx2026.json")))["d"][-1]
def official(s): return np.asarray(s, float) * (42195.0 / GL)
def gpx_of(k): return np.asarray(k, float) * (GL / 42195.0)
