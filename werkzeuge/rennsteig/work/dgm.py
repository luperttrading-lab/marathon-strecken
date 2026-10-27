# Höhen alle 10 m (GPX-Meter) -> dgm2026_10m.json. Quelle: Sonnys LiDAR-Geländemodell im 20-m-Raster (siehe dtm20.py).
# Das amtliche DGM1 Thüringen ist von hier aus nicht abrufbar: geoportal-th.de zeigt eine Wartungsseite, das neue
# geoportal.thueringen.de verlangt ein Captcha, und api.hoehendaten.de (Port 14444) lässt der Netzfilter nicht durch.
# Die Punkte liegen schon auf den OSM-Wegen (match.py), ein Nachrücken wie in München und an der Elbe entfällt.
import json, numpy as np
from pyproj import Transformer
from dtm20 import lade, hoehe
src, out, step = "gpx2026.json", "dgm2026_10m.json", 10.0
g = json.load(open(src)); pts, d = g["pts"], g["d"]
dd = np.array(d); ss = np.append(np.arange(0, d[-1], step), d[-1])
la = np.interp(ss, dd, [p[0] for p in pts]); lo = np.interp(ss, dd, [p[1] for p in pts])
E, N = Transformer.from_crs(4326, 32632, always_xy=True).transform(lo, la)
A, m = lade(); H = hoehe(A, m, E, N)
res = [[float(s), float(x), float(y), (None if np.isnan(h) else float(h))] for s, x, y, h in zip(ss, la, lo, H)]
hv = H[~np.isnan(H)]; print(len(res), "Punkte; Höhe min/max", round(hv.min(), 1), round(hv.max(), 1), "; fehlend:", int(np.isnan(H).sum()))
json.dump(res, open(out, "w"))
