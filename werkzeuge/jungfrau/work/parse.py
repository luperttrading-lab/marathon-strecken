# Strecke aus den Daten des Veranstalters: Seite „Strecke“ (jungfrau-marathon.ch/de/strecke.html, Downloads „GPX Daten Jungfrau-Marathon“
# und „KMZ Daten Jungfrau-Marathon“, beide „Originalstrecke_2024“, Track „ORIGINAL_STRECKE_2024_3D_DRAPED“, erstellt mit Global Mapper;
# dazu die „Vermessene Strecke“ als Karte 1:40 000 von Flotron AG, 27.05.2024). Die KMZ hat dieselben 67 296 Punkte wie die GPX, aber
# mit 10 statt 6 Nachkommastellen: genommen wird die KMZ (../dl/kmz/doc.kml aus ../dl/gpx/Originalstrecke_2024.KMZ).
# Die Linie ist in der Ebene (LV95) 42 194,5 m lang, geodätisch 42 193,5 m: Sie ist die vermessene Strecke selbst, die Kilometer
# laufen gleichmäßig über sie (common.py). Die Punkte liegen im Mittel 0,5 m auseinander und zittern seitlich um Zentimeter bis
# Dezimeter (Ausdünnen auf 1 m kürzt die Länge um 21 m): Für die Kilometer zählt die Länge der vollen Linie. Gespeichert wird eine
# nach Douglas-Peucker (0,25 m) ausgedünnte Linie, je Punkt mit der Länge entlang der vollen Linie.
# -> gpx2026.json {"pts": [[lat, lon, ele], …], "d": [Länge entlang der vollen Linie bis zum Punkt, geodätisch GRS80]}
import json, re
import numpy as np
from pyproj import Geod, Transformer
T = Transformer.from_crs(4326, 2056, always_xy=True)       # LV95
t = open("../dl/kmz/doc.kml", encoding="iso-8859-1").read()
P = np.array([[float(v) for v in x.split(",")] for x in re.search(r"<coordinates>(.*?)</coordinates>", t, re.S).group(1).split()])
lon, lat, ele = P[:, 0], P[:, 1], P[:, 2]
G = Geod(ellps="GRS80")
_, _, dd = G.inv(lon[:-1], lat[:-1], lon[1:], lat[1:])
d = np.r_[0, np.cumsum(dd)]
x, y = T.transform(lon, lat); X = np.c_[x, y]
dl = np.r_[0, np.cumsum(np.hypot(*np.diff(X, axis=0).T))]
def dp(X, tol):
    keep = np.zeros(len(X), bool); keep[0] = keep[-1] = True; st = [(0, len(X) - 1)]
    while st:
        a, b = st.pop()
        if b <= a + 1: continue
        v = X[b] - X[a]; L = np.hypot(*v); w = X[a + 1:b] - X[a]
        dist = np.abs(v[0] * w[:, 1] - v[1] * w[:, 0]) / L if L > 0 else np.hypot(*w.T)
        i = int(np.argmax(dist))
        if dist[i] > tol: keep[a + 1 + i] = True; st += [(a, a + 1 + i), (a + 1 + i, b)]
    return np.where(keep)[0]
k = dp(X, 0.25)
print(f"KMZ: {len(P)} Punkte, Länge geodätisch {d[-1]:.1f} m, in LV95 {dl[-1]:.1f} m, Abstand Median {np.median(dd):.2f} m, bis {dd.max():.1f} m; "
      f"Höhe {ele.min():.1f}–{ele.max():.1f} m; ausgedünnt (Douglas-Peucker 0,25 m) {len(k)} Punkte")
print("Anfang", lat[0], lon[0], "Ende", lat[-1], lon[-1])
json.dump({"pts": [[round(float(lat[i]), 8), round(float(lon[i]), 8), round(float(ele[i]), 3)] for i in k], "d": [round(float(d[i]), 2) for i in k]},
          open("gpx2026.json", "w"), separators=(",", ":"))
