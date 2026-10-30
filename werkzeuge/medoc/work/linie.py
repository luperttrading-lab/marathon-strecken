# Linie der OpenRunner-Karte (openrunner.json) -> gpx2026.json im Format der anderen Strecken (Punkte, laufende Länge GRS80).
# Prüfung gegen das OSM-Netz (../dl/osm_wege.json): Die Linie folgt den Wegen (Median 1,7 m daneben, 95 % bis 4,7 m); nur an
# wenigen Stellen bis 46 m daneben, wo sie durch Château-Höfe und Rebzeilen ohne OSM-Weg läuft. Deshalb nicht auf OSM gelegt.
import json, numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
o = json.load(open("openrunner.json"))
json.dump({"pts": [(a, b, 0.0) for a, b in o["pts"]], "d": o["d"]}, open("gpx2026.json", "w"))
T = Transformer.from_crs(4326, 2154, always_xy=True)   # Lambert 93
P = np.array(o["pts"]); d = np.array(o["d"])
ss = np.arange(0, d[-1], 10.0); x, y = T.transform(np.interp(ss, d, P[:, 1]), np.interp(ss, d, P[:, 0]))
pk = []
for w in json.load(open("../dl/osm_wege.json"))["elements"]:
    if "highway" not in w.get("tags", {}): continue
    wx, wy = T.transform([q["lon"] for q in w["geometry"]], [q["lat"] for q in w["geometry"]])
    for i in range(len(wx) - 1):
        a = np.array([wx[i], wy[i]]); b = np.array([wx[i + 1], wy[i + 1]])
        for f in np.linspace(0, 1, max(2, int(np.hypot(*(b - a)) / 2) + 1)): pk.append(a + f * (b - a))
dist, _ = cKDTree(np.array(pk)).query(np.c_[x, y])
print(f"Linie {d[-1]:.1f} m, {len(P)} Punkte; Abstand zum nächsten OSM-Weg: Median {np.median(dist):.1f} m, 95 % {np.percentile(dist, 95):.1f} m, max {dist.max():.1f} m")
i = 0
while i < len(dist):
    if dist[i] > 15:
        j = i
        while j + 1 < len(dist) and dist[j + 1] > 15: j += 1
        print(f"  Linienmeter {ss[i]:6.0f}–{ss[j]:6.0f}: bis {dist[i:j + 1].max():.0f} m neben dem nächsten Weg ({P[np.searchsorted(d, ss[i])][0]:.5f}, {P[np.searchsorted(d, ss[i])][1]:.5f})")
        i = j + 1
    else: i += 1
