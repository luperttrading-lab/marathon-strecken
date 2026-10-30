# Koordinaten alle 50 offizielle Meter für Karte und Läuferpunkt -> route50.json
import json, numpy as np
from common import official
L = json.load(open("linie.json"))
s = np.array(L["d"]); la = np.array(L["lat"]); lo = np.array(L["lon"])
k = official(s)
grid = np.append(np.arange(0, 42195, 50.0), 42195.0)
glat = np.interp(grid, k, la); glon = np.interp(grid, k, lo)
lat0, lon0 = 40.15, 117.40
route = [[int(round((a - lat0) * 1e5)), int(round((b - lon0) * 1e5))] for a, b in zip(glat, glon)]
json.dump({"step": 50, "lat0": lat0, "lon0": lon0, "pts": route}, open("route50.json", "w"), separators=(",", ":"))
print(len(route), "Punkte", "lat", glat.min(), glat.max(), "lon", glon.min(), glon.max())
