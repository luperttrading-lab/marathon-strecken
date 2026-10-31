# Kilometermarken des Veranstalters: Die Karte von TrackMaxx auf der Seite „Streckenpläne“ (../dl/trackmaxx/getmap.json) hat für den
# Marathon 42 Punkte „KM 1“ … „KM 42“ (und Pfeile je halben km) genau auf der GPX-Linie. Ihre Abstände entlang der Linie schwanken
# zwischen 1008 und 1020 m (die Linie ist 1,45 % länger als die vermessene Strecke): Sie folgen also nicht einfach der Linie, sondern
# wohl den Marken der Vermessung (World Athletics/AIMS, 09.03.2025). Projektion auf die Linie -> kmmarken.json [[km, Linienmeter], …]
import json
import numpy as np
from pyproj import Transformer
T = Transformer.from_crs(4326, 2056, always_xy=True)
g = json.load(open("gpx2026.json")); P = np.array(g["pts"]); d = np.array(g["d"])
x, y = T.transform(P[:, 1], P[:, 0]); X = np.c_[x, y]
dl = np.r_[0, np.cumsum(np.hypot(*np.diff(X, axis=0).T))]
m = json.load(open("../dl/trackmaxx/getmap.json"))
tr = [t for t in m["tracks"] if t["caption"] == "42.2 km"][0]
pois = sorted([p for p in m["pois"] if p["trackoid"] == tr["oid"] and p["type"] == "km"], key=lambda p: p["order"])
def proj(q, lo):
    best = None
    for i in range(len(X) - 1):
        a, b = X[i], X[i + 1]; v = b - a; L = np.hypot(*v)
        if L == 0 or dl[i + 1] < lo: continue
        t = np.clip(np.dot(q - a, v) / L ** 2, 0, 1); dist = np.hypot(*(a + t * v - q)); s = dl[i] + t * L
        if best is None or dist < best[0] - 1e-6: best = (dist, s)
        if best[0] < 5 and s > best[1] + 3000: break
    return best
out, lo = [], 0.0
for p in pois:
    la, lon = map(float, p["coordinates"].split(","))
    dist, s = proj(np.array(T.transform(lon, la)), lo); lo = s
    sg = float(np.interp(s, dl, d))                   # geodätische Linienmeter wie gpx2026.json
    out.append([int(p["caption"].split()[1]), round(sg, 1)]); assert dist < 2, (p["caption"], dist)
km = np.array(out)
assert (km[:, 0] == np.arange(1, 43)).all()
ab = np.diff(np.r_[0, km[:, 1]])
print(f"42 Marken, Abstand je km {ab.min():.0f}–{ab.max():.0f} m (Mittel {ab.mean():.1f}), letzte 195 m: {d[-1] - km[-1, 1]:.1f} m Linie")
json.dump(out, open("kmmarken.json", "w"))
