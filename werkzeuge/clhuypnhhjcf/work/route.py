# Koordinaten alle 50 Streckenmeter für Karte und Läuferpunkt -> route50.json (Kopie von werkzeuge/hannover/work/route.py)
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official, L
r = json.load(open("dgm_10m.json"))
s = np.array([x[0] for x in r]); la = np.array([x[1] for x in r]); lo = np.array([x[2] for x in r])
k = official(s)
grid = np.append(np.arange(0, L, 50.0), L)
glat = np.interp(grid, k, la); glon = np.interp(grid, k, lo)
lat0, lon0 = 50.5, 8.7
route = [[int(round((a - lat0) * 1e5)), int(round((b - lon0) * 1e5))] for a, b in zip(glat, glon)]
json.dump({"step": 50, "lat0": lat0, "lon0": lon0, "pts": route}, open("route50.json", "w"), separators=(",", ":"))
print(len(route), "Punkte", "lat", glat.min(), glat.max(), "lon", glon.min(), glon.max())
