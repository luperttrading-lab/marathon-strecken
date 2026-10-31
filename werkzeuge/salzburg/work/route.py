# Koordinaten alle 50 offizielle Meter für Karte und Läuferpunkt -> route50.json (Muster: werkzeuge/freiburg/work/route.py).
# Lage aus der Straßenmitte (dtm.py: Fußpunkt auf dem OSM-Weg), geglättet über ±20 m, damit der Läuferpunkt nicht mit der Spur wackelt.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official
r = json.load(open("dtm_10m.json"))
s = np.array([x[0] for x in r]); la = np.array([x[7] for x in r]); lo = np.array([x[8] for x in r])
def glatt(v, n=2): return np.array([v[max(0, i - n):i + n + 1].mean() for i in range(len(v))])
la, lo = glatt(la), glatt(lo)
k = official(s)
grid = np.append(np.arange(0, 42195, 50.0), 42195.0)
glat = np.interp(grid, k, la); glon = np.interp(grid, k, lo)
lat0, lon0 = 47.8, 13.0
route = [[int(round((a - lat0) * 1e5)), int(round((b - lon0) * 1e5))] for a, b in zip(glat, glon)]
json.dump({"step": 50, "lat0": lat0, "lon0": lon0, "pts": route}, open("route50.json", "w"), separators=(",", ":"))
print(len(route), "Punkte", "lat", glat.min(), glat.max(), "lon", glon.min(), glon.max())
