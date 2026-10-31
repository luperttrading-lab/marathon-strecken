# Strecke aus der Strava-Route „JAL Honolulu Marathon 2026“, die der Veranstalter auf seiner Seite „Course Description“
# einbettet (honolulumarathon.org/key-information/course-description, Strava-Route 3517891324308402546; die Einbettung
# strava-embeds.com/route/<id> liefert die Linie als JSON „__ROUTE_DATA__“, ohne Anmeldung, ../dl/strava/route_embed.html,
# ../dl/strava/route_data.json). Die Linie hat Höhen aus Stravas eigenem Geländemodell (Herkunft nicht angegeben; nur zum
# Vergleich, dgm.py). Strava nennt 42 596,9 m (26,4 mi) und 407 ft bergauf.
# -> gpx2026.json (Punkte [lat, lon, Strava-Höhe] und laufende Länge, geodätisch WGS 84)
import json
import numpy as np
from pyproj import Transformer, Geod
T = Transformer.from_crs(4326, 32604, always_xy=True)   # UTM 4N
r = json.load(open("../dl/strava/route_data.json"))
co = r["coordinates"]
pts = [(float(c[1]), float(c[0]), float(c[2])) for c in co]
n0 = len(pts)
pts = [p for i, p in enumerate(pts) if i == 0 or (round(p[0], 7), round(p[1], 7)) != (round(pts[i - 1][0], 7), round(pts[i - 1][1], 7))]
# Zacken entfernen: Die Linie besteht aus 64 Stücken zwischen den Klickpunkten des Strava-Routenplaners; an vielen Klickpunkten
# läuft sie ein paar Meter weiter und wieder zurück (Richtungsumkehr um mehr als ~107°, eines der beiden Stücke unter 30 m), zusammen
# rund 200 m. Ohne sie ist die Linie so lang wie Strava sie angibt (42,60 km).
xy0 = np.array([T.transform(p[1], p[0]) for p in pts]); idx = list(range(len(pts))); weg = 0
k = 1
while k < len(idx) - 1:
    a_, b_, c_ = xy0[idx[k - 1]], xy0[idx[k]], xy0[idx[k + 1]]
    u_, v_ = b_ - a_, c_ - b_; lu, lv = np.hypot(*u_), np.hypot(*v_)
    if lu < 0.01 or lv < 0.01 or (np.dot(u_, v_) / (lu * lv) < -0.3 and min(lu, lv) < 30):
        del idx[k]; weg += 1; k = max(1, k - 1)
    else: k += 1
pts = [pts[i] for i in idx]
print(f"{weg} Zackenpunkte entfernt")
G = Geod(ellps="WGS84")
_, _, dd = G.inv([p[1] for p in pts[:-1]], [p[0] for p in pts[:-1]], [p[1] for p in pts[1:]], [p[0] for p in pts[1:]])
dd = np.array(dd); d = np.r_[0, np.cumsum(dd)]
xy = np.array([T.transform(p[1], p[0]) for p in pts]); dl = np.r_[0, np.cumsum(np.hypot(*np.diff(xy, axis=0).T))]
print(f"Strava: {n0} Punkte, {len(pts)} ohne doppelte, {d[-1]:.1f} m geodätisch ({dl[-1]:.1f} m in UTM 4N), Abstand bis {dd.max():.0f} m, "
      f"Median {np.median(dd):.1f} m")
print("Wegpunkte:", [(w["title"], w["point"], w["distance"]) for w in r["waypoints"]])
print("Start", pts[0], "Ende", pts[-1])
# Verbliebene Spitzkehren (sollte keine geben)
v = np.diff(xy, axis=0); L = np.hypot(*v.T); ok = L > 0.5
u = v[ok] / L[ok][:, None]; dok = d[1:][ok]
for i in range(1, len(u)):
    if np.dot(u[i], u[i - 1]) < -0.8: print(f"  Umkehr bei Linienmeter {dok[i]:.0f}")
json.dump({"pts": pts, "d": d.tolist()}, open("gpx2026.json", "w"))
