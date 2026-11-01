# Linie der Hausrunde aus der GPX-Datei des Nutzers (MapPlanner, ../dl/runde.gpx; bleibt lokal, dl/ ist gitignored). Rundkurs, Start
# und Ziel am Westende (50,5745 / 8,6960). MapPlanner schreibt jeden Punkt doppelt; die Höhen der Datei (Höhenmodell von MapPlanner,
# im Wald 15–25 m zu hoch) werden nicht benutzt.
# -> linie.json (Punkte [lat, lon] und laufende Länge, geodätisch WGS 84)
import json, re
import numpy as np
from pyproj import Geod
s = open("../dl/runde.gpx", encoding="utf-8").read()
pts = [(float(a), float(b)) for a, b in re.findall(r'<trkpt lat="([-\d.]+)" lon="([-\d.]+)"', s)]
n0 = len(pts)
pts = [p for i, p in enumerate(pts) if i == 0 or (round(p[0], 7), round(p[1], 7)) != (round(pts[i - 1][0], 7), round(pts[i - 1][1], 7))]
G = Geod(ellps="WGS84")
_, _, dd = G.inv([p[1] for p in pts[:-1]], [p[0] for p in pts[:-1]], [p[1] for p in pts[1:]], [p[0] for p in pts[1:]])
dd = np.array(dd); d = np.r_[0, np.cumsum(dd)]
_, _, schluss = G.inv(pts[-1][1], pts[-1][0], pts[0][1], pts[0][0])
print(f"{n0} Punkte, {len(pts)} ohne doppelte, {d[-1]:.1f} m geodätisch, Abstand bis {dd.max():.0f} m, Median {np.median(dd):.1f} m")
print("Start", pts[0], "Ende", pts[-1], f"Lücke Ende–Start {schluss:.1f} m")
json.dump({"pts": pts, "d": d.tolist()}, open("linie.json", "w"))
