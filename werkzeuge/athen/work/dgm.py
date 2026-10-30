# Höhen entlang der Linie alle 10 Linienmeter aus FABDEM, Copernicus GLO-30 und SRTM 1″ (hoehen.py) -> dgm_vergleich.json
# {"s": [Linienmeter], "lat", "lon", "fabdem", "cop30", "srtm", "strava"}; die gewählte Quelle (FABDEM, siehe vergleich.py) zusätzlich
# als dgm2026_10m.json [[Linienmeter, lat, lon, h], …] wie bei den anderen Strecken.
import json
import numpy as np
from pyproj import Geod
from hoehen import modell
g = json.load(open("gpx2026.json")); P = np.array(g["pts"]); d = np.array(g["d"])
# Zwischenpunkte entlang der Geodäte jedes Linienstücks (die Stücke sind bis 900 m lang, gerade Straße)
G = Geod(ellps="GRS80")
s = np.append(np.arange(0, d[-1], 10.0), d[-1])
lat = np.empty_like(s); lon = np.empty_like(s)
for n, x in enumerate(s):
    i = min(max(1, int(np.searchsorted(d, x, side="right"))), len(d) - 1)
    f = (x - d[i - 1]) / ((d[i] - d[i - 1]) or 1)
    lo1, la1, lo2, la2 = P[i - 1, 1], P[i - 1, 0], P[i, 1], P[i, 0]
    az, _, dist = G.inv(lo1, la1, lo2, la2)
    lo_, la_, _ = G.fwd(lo1, la1, az, f * dist)
    lat[n], lon[n] = la_, lo_
strava = np.interp(s, d, P[:, 2])
out = {"s": s.round(1).tolist(), "lat": lat.round(7).tolist(), "lon": lon.round(7).tolist(), "strava": strava.round(2).tolist()}
for m in ("fabdem", "cop30", "srtm"):
    h = modell(m)(lat, lon); out[m] = np.round(h, 2).tolist()
    print(f"{m:7s} Start {h[0]:6.1f}  min {np.nanmin(h):6.1f}  max {np.nanmax(h):6.1f} bei Linienmeter {s[np.nanargmax(h)]:7.0f}  Ziel {h[-1]:6.1f}  fehlend {np.isnan(h).sum()}")
json.dump(out, open("dgm_vergleich.json", "w"))
json.dump([[float(a), float(b), float(c), float(e)] for a, b, c, e in zip(out["s"], out["lat"], out["lon"], out["fabdem"])],
          open("dgm2026_10m.json", "w"))
print(len(s), "Punkte")
