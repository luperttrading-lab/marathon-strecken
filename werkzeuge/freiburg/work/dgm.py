# Höhen alle 10 Linienmeter der Marathonlinie aus dem DGM1 Baden-Württemberg (Laserscan, Bodenpunkte, 1-m-Raster; LGL, Open GeoData) und
# zum Vergleich aus dem DOM1 (Oberflächenmodell derselben Befliegung: Dächer, Bäume, Brücken). lgl.py lädt die 2-km-Kacheln und liest
# bilinear. Befliegung laut Metadaten der Kacheln (../dl/dgm1/meta.json) 2017 bzw. 2018, Genauigkeit 0,15 m, Höhen NHN (DHHN2016).
# -> dgm2026_10m.json [[Linienmeter, lat, lon, DGM1, DOM1], …]
import json, time
import numpy as np
from pyproj import Transformer
import lgl as lgln
T = Transformer.from_crs(4326, 25832, always_xy=True)
g = json.load(open("strecke2026.json")); d = np.array(g["d"]); P = np.array(g["pts"])
ss = np.append(np.arange(0, d[-1], 10.0), d[-1])
la = np.interp(ss, d, P[:, 0]); lo = np.interp(ss, d, P[:, 1])
E, N = T.transform(lo, la)
t0 = time.time()
h1 = lgln.hoehe("dgm1", E, N); h2 = lgln.hoehe("dom1", E, N)
res = [[float(s), float(a), float(b), (None if np.isnan(x) else round(float(x), 3)), (None if np.isnan(y) else round(float(y), 3))]
       for s, a, b, x, y in zip(ss, la, lo, h1, h2)]
print(len(res), "Punkte,", round(time.time() - t0), "s; ohne DGM-Wert:", int(np.isnan(h1).sum()), " ohne DOM-Wert:", int(np.isnan(h2).sum()))
print("DGM1 min/max", np.nanmin(h1).round(2), np.nanmax(h1).round(2), " Start", h1[0].round(2), "Ziel", h1[-1].round(2))
json.dump(res, open("dgm2026_10m.json", "w"))
