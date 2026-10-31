# Koordinaten alle 50 offizielle Meter für Karte und Läuferpunkt -> route50.json (Muster: werkzeuge/freiburg/work/route.py; hier direkt aus
# der gelegten Linie gelegt.json)
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official
g = json.load(open("gelegt.json")); s = np.array(g["d"]); P = np.array(g["pts"])
k = official(s)
grid = np.append(np.arange(0, 42195, 50.0), 42195.0)
glat = np.interp(grid, k, P[:, 0]); glon = np.interp(grid, k, P[:, 1])
lat0, lon0 = 51.8, 10.7
route = [[int(round((a - lat0) * 1e5)), int(round((b - lon0) * 1e5))] for a, b in zip(glat, glon)]
json.dump({"step": 50, "lat0": lat0, "lon0": lon0, "pts": route}, open("route50.json", "w"), separators=(",", ":"))
print(len(route), "Punkte", "lat", glat.min(), glat.max(), "lon", glon.min(), glon.max())
