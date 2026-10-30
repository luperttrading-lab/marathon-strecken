# Höhen entlang der Linie alle 10 m (Linienmeter) aus Copernicus GLO-30 -> dgm_cop30_10m.json [[Linienmeter, lat, lon, h], …].
# Copernicus DEM GLO-30 (Kachel N40 E117, öffentlich auf AWS: copernicus-dem-30m.s3.amazonaws.com, ohne Anmeldung), Raster 1″
# (≈ 24 × 31 m hier), Höhen über dem Geoid EGM2008. Es ist ein Oberflächenmodell (TanDEM-X 2011–2015): Bäume, Häuser und die Mauer
# selbst stecken mit drin; auf schmalen Graten glättet das 30-m-Raster die Spitzen. Bilinear zwischen den Rasterpunkten.
# Lesen mit tifffile (rasterio gibt es nicht); Lage aus ModelTiepoint/ModelPixelScale (Ecke des ersten Pixels bei 117,0° O / 41,0° N).
import json
import numpy as np, tifffile
from geo import gleich
def lade(f):
    t = tifffile.TiffFile(f); p = t.pages[0]
    sx, sy, _ = p.tags["ModelPixelScaleTag"].value; tp = p.tags["ModelTiepointTag"].value
    return p.asarray().astype(float), tp[3], tp[4], sx, sy
def abtasten(Z, lon0, lat0, sx, sy, lat, lon, mitte=True):
    # Pixelmitte bei (lon0 + (j + 0,5)·sx, lat0 − (i + 0,5)·sy)
    fx = (np.asarray(lon) - lon0) / sx - (0.5 if mitte else 0); fy = (lat0 - np.asarray(lat)) / sy - (0.5 if mitte else 0)
    j0 = np.floor(fx).astype(int); i0 = np.floor(fy).astype(int); ax = fx - j0; ay = fy - i0
    return (Z[i0, j0] * (1 - ax) * (1 - ay) + Z[i0, j0 + 1] * ax * (1 - ay) + Z[i0 + 1, j0] * (1 - ax) * ay + Z[i0 + 1, j0 + 1] * ax * ay)
if __name__ == "__main__":
    from geo import wgs
    L = json.load(open("linie.json")); X = np.c_[L["x"], L["y"]]
    G, d = gleich(X, 10.0); lat, lon = wgs(G[:, 0], G[:, 1])
    Z, lon0, lat0, sx, sy = lade("../dl/dem/cop30_N40_E117.tif")
    h = abtasten(Z, lon0, lat0, sx, sy, lat, lon)
    json.dump([[round(float(a), 1), round(float(b), 7), round(float(c), 7), round(float(e), 2)] for a, b, c, e in zip(d, lat, lon, h)],
              open("dgm_cop30_10m.json", "w"))
    print(len(d), "Punkte, Höhe", round(h.min(), 1), "–", round(h.max(), 1), "m, Start", round(h[0], 1), "Ziel", round(h[-1], 1))
