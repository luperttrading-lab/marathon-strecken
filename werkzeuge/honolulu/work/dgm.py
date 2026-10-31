# Höhen entlang der Linie alle 10 Linienmeter aus dem USGS-3DEP-Geländemodell 1 m (Projekt HI_NOAAMauiOahu_2020_B20, Arbeitseinheit
# HI_NOAAMauiOahu_2_B20: NOAA-Laserscan QL1, 8 Punkte/m², Flüge Januar–Juli 2023, Klasse 10 cm RMSEz; Bodenmodell ohne Gebäude,
# Bäume und Brücken, Gewässer flach; NAD83(PA11) / UTM 4N, Höhen „NAVD88 (GEOID12B)“, auf Hawaii also über dem Geoid GEOID12B,
# rund Meereshöhe). Drei Kacheln zu 10 × 10 km (x61y236, x62y236, x63y236), als COG nur in Teilen geladen (cog.py).
# Dazu die Höhen der Strava-Linie (Stravas eigenes Modell, nur Vergleich).
# -> dgm2026_10m.json [[Linienmeter, lat, lon, h], …] und dgm_vergleich.json {"s", "lat", "lon", "lidar", "strava"}
import json
import numpy as np
from pyproj import Geod, Transformer
from cog import COG
URL = "https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1m/Projects/HI_NOAAMauiOahu_2020_B20/TIFF/USGS_1M_4_x{}y236_HI_NOAAMauiOahu_2020_B20.tif"
K = {x: COG(URL.format(x)) for x in (61, 62, 63)}
T = Transformer.from_crs(4326, 6634, always_xy=True)   # NAD83(PA11) / UTM 4N wie die Kacheln (Unterschied zu WGS 84 rund 1 m)
g = json.load(open("gpx2026.json")); P = np.array(g["pts"]); d = np.array(g["d"])
G = Geod(ellps="WGS84")
s = np.append(np.arange(0, d[-1], 10.0), d[-1])
lat = np.empty_like(s); lon = np.empty_like(s)
for n, x in enumerate(s):
    i = min(max(1, int(np.searchsorted(d, x, side="right"))), len(d) - 1)
    f = (x - d[i - 1]) / ((d[i] - d[i - 1]) or 1)
    az, _, dist = G.inv(P[i - 1, 1], P[i - 1, 0], P[i, 1], P[i, 0])
    lo_, la_, _ = G.fwd(P[i - 1, 1], P[i - 1, 0], az, f * dist)
    lat[n], lon[n] = la_, lo_
X, Y = T.transform(lon, lat)
h = np.full(len(s), np.nan)
for kx, c in K.items():
    sel = (X >= kx * 10000 - 5) & (X < (kx + 1) * 10000 + 5) & np.isnan(h)
    if sel.any(): h[sel] = c(X[sel], Y[sel])
    print(f"Kachel x{kx}y236: {sel.sum()} Punkte, {len(c.kach)} interne Kacheln geladen", flush=True)
print(f"Lidar: Start {h[0]:.2f}  min {np.nanmin(h):.2f}  max {np.nanmax(h):.2f} bei Linienmeter {s[np.nanargmax(h)]:.0f}  Ziel {h[-1]:.2f}  fehlend {np.isnan(h).sum()}")
strava = np.interp(s, d, P[:, 2])
json.dump({"s": s.round(1).tolist(), "lat": lat.round(7).tolist(), "lon": lon.round(7).tolist(), "lidar": np.round(h, 3).tolist(),
           "strava": strava.round(2).tolist()}, open("dgm_vergleich.json", "w"))
json.dump([[float(a), float(b), float(c), float(e)] for a, b, c, e in zip(s, lat.round(7), lon.round(7), np.round(h, 3))], open("dgm2026_10m.json", "w"))
print(len(s), "Punkte")
