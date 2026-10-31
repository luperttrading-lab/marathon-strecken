# Höhen alle 10 Linienmeter der gelegten Linie (gelegt.json) aus dem DGM1 Sachsen-Anhalt (LVermGeo, Laserscan, Bodenpunkte, 1-m-Raster,
# Open Data). lvermgeo.py lädt die 2-km-Kacheln und liest bilinear. Befliegung laut Metadaten der Kacheln (../dl/dgm1/meta.json),
# Genauigkeit 0,15 m, Höhen NHN (DHHN2016). Zum Vergleich die Höhen der GPX-Datei (Strava) an derselben Stelle.
# -> dgm2026_10m.json [[Linienmeter, lat, lon, DGM1], …]
import json, time
import numpy as np
from pyproj import Transformer
import lvermgeo
T = Transformer.from_crs(4326, 25832, always_xy=True)
g = json.load(open("gelegt.json")); d = np.array(g["d"]); P = np.array(g["pts"])
ss = np.append(np.arange(0, d[-1], 10.0), d[-1])
la = np.interp(ss, d, P[:, 0]); lo = np.interp(ss, d, P[:, 1])
E, N = T.transform(lo, la)
t0 = time.time()
h1 = lvermgeo.hoehe("dgm1", E, N)
res = [[float(s), float(a), float(b), (None if np.isnan(x) else round(float(x), 3))] for s, a, b, x in zip(ss, la, lo, h1)]
print(len(res), "Punkte,", round(time.time() - t0), "s; ohne DGM-Wert:", int(np.isnan(h1).sum()))
print("DGM1 min/max", np.nanmin(h1).round(2), np.nanmax(h1).round(2), " Start", h1[0].round(2), "Ziel", h1[-1].round(2))
# Vergleich mit den Höhen der GPX-Datei (Strava, auf die nächste Stelle der GPX-Linie)
G = json.load(open("linie.json")); ge = np.array(G["ele"]); gx, gy = T.transform([p[1] for p in G["pts"]], [p[0] for p in G["pts"]])
from scipy.spatial import cKDTree
_, j = cKDTree(np.c_[gx, gy]).query(np.c_[E, N]); diff = ge[j] - h1
print(f"GPX-Höhe minus DGM1: Median {np.nanmedian(diff):+.1f} m, 90 % des Betrags {np.nanpercentile(np.abs(diff), 90):.1f} m")
json.dump(res, open("dgm2026_10m.json", "w"))
m = json.load(open("../dl/dgm1/meta.json"))
from collections import Counter
print("Befliegung (Aktualität) der Kacheln:", Counter(v.get("Aktualitaet") for v in m.values()), " Fortführung:", Counter(v.get("Fortfuehrung") for v in m.values()))
