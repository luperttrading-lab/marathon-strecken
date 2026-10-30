# Strecke aus der GPX-Datei des Veranstalters (SEGAS, athensauthenticmarathon.gr, Seite „Marathon Race“, „Download the route
# file“: athens_marathon_the_authentic.gpx). Die Datei ist eine Strava-Route des Veranstalters (strava.com/routes/
# 3343870889182584480, Konto „Athens Marathon The Authentic“), gezeichnet auf OpenStreetMap: 644 Punkte von der Startlinie im
# Stadion von Marathon bis zur Ziellinie im Panathinaiko-Stadion. Die KML-Datei derselben Seite (plotaroute.com) ist dieselbe Linie
# mit 390 Punkten und Kilometerzeichen, die plotaroute selbst alle 1000 Linienmeter setzt (keine Schilder des Veranstalters).
# -> gpx_veranstalter.json {"pts": [[lat, lon, ele_strava], …], "d": [Linienmeter geodätisch, GRS80]}
import json, re
import numpy as np
from pyproj import Geod
t = open("../dl/athens_marathon_the_authentic.gpx", encoding="utf-8").read()
pts = [(float(a), float(b), float(e)) for a, b, e in re.findall(r'<trkpt lat="([-\d.]+)" lon="([-\d.]+)">\s*<ele>([-\d.]+)</ele>', t)]
# doppelte Punkte (Abstand 0) entfernen
neu = [pts[0]]
for p in pts[1:]:
    if abs(p[0] - neu[-1][0]) > 1e-9 or abs(p[1] - neu[-1][1]) > 1e-9: neu.append(p)
pts = neu
G = Geod(ellps="GRS80")
_, _, dd = G.inv([p[1] for p in pts[:-1]], [p[0] for p in pts[:-1]], [p[1] for p in pts[1:]], [p[0] for p in pts[1:]])
d = [0.0] + np.cumsum(dd).tolist()
json.dump({"pts": [[round(a, 7), round(b, 7), e] for a, b, e in pts], "d": d}, open("gpx_veranstalter.json", "w"))
print(len(pts), "Punkte, Linie", round(d[-1], 1), "m geodätisch (GRS80), Start", pts[0][:2], "Ziel", pts[-1][:2])
print("Strava-Höhen: Start", pts[0][2], "max", max(p[2] for p in pts), "Ziel", pts[-1][2])
# Gegenprobe KML (plotaroute): gleiche Linie?
k = open("../dl/athens_marathon_the_authentic-1.kml", encoding="utf-8").read()
ls = re.search(r'<LineString id="Route">.*?<coordinates>([^<]+)</coordinates>', k, re.S).group(1).split()
kp = [(float(c.split(",")[1]), float(c.split(",")[0])) for c in ls]
_, _, kd = G.inv([p[1] for p in kp[:-1]], [p[0] for p in kp[:-1]], [p[1] for p in kp[1:]], [p[0] for p in kp[1:]])
from pyproj import Transformer
T = Transformer.from_crs(4326, 2100, always_xy=True)   # GGRS87 / Greek Grid
xy = np.array([T.transform(b, a) for a, b, _ in pts]); kxy = np.array([T.transform(b, a) for a, b in kp])
def abst(p):
    a = xy[:-1]; v = xy[1:] - a; t_ = np.clip(((p - a) * v).sum(1) / np.maximum((v * v).sum(1), 1e-9), 0, 1)
    return np.hypot(*(a + v * t_[:, None] - p).T).min()
ab = np.array([abst(p) for p in kxy])
print("KML-Linie", len(kp), "Punkte,", round(float(np.sum(kd)), 1), "m; Abstand zur GPX-Linie: Median", round(float(np.median(ab)), 1), "m, max", round(float(ab.max()), 1), "m")
