# Lesen der Höhenmodelle (Kacheln unter ../dl/dem/, 1″-Raster, WGS 84). rasterio gibt es nicht: tifffile und numpy.
# - FABDEM V1-2 (fabdem.py): Copernicus GLO-30 ohne Gebäude und Wald, Höhen über dem Geoid EGM2008, NODATA −9999.
# - Copernicus DEM GLO-30 (AWS copernicus-dem-30m, ohne Anmeldung): Oberflächenmodell aus TanDEM-X 2011–2015, EGM2008.
#   Beide GeoTIFF sagen RasterPixelIsPoint (GeoKey 1025 = 2): die Mitte des ersten Pixels liegt genau auf der Ecke der Kachel.
# - SRTM 1″ (AWS Terrain Tiles skadi, .hgt): Oberflächenmodell aus dem Radarflug im Februar 2000, EGM96; 3601 × 3601 Werte,
#   Big Endian int16, erste Zeile = Nordrand, Werte auf ganzen Graden.
# Je Modell die Kacheln N38E023 (oben) und N37E023 zu einem Gitter zusammengesetzt; bilinear zwischen den Rasterpunkten.
import gzip, os
import numpy as np, tifffile
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../dl/dem/")
S = 1 / 3600
class Gitter:
    def __init__(self, Z, lat0, lon0):
        self.Z, self.lat0, self.lon0 = Z, lat0, lon0           # Z[0, 0] liegt auf (lat0, lon0)
    def __call__(self, lat, lon):
        fy = (self.lat0 - np.asarray(lat, float)) / S; fx = (np.asarray(lon, float) - self.lon0) / S
        i0 = np.floor(fy).astype(int); j0 = np.floor(fx).astype(int); ay = fy - i0; ax = fx - j0
        Z = self.Z
        return (Z[i0, j0] * (1 - ax) * (1 - ay) + Z[i0, j0 + 1] * ax * (1 - ay) + Z[i0 + 1, j0] * (1 - ax) * ay
                + Z[i0 + 1, j0 + 1] * ax * ay)
def _tif(f):
    p = tifffile.TiffFile(D + f).pages[0]
    gk = p.tags["GeoKeyDirectoryTag"].value; gk = {gk[i]: gk[i + 3] for i in range(4, len(gk), 4)}
    assert gk.get(1025) == 2, "erwartet RasterPixelIsPoint"
    tp = p.tags["ModelTiepointTag"].value
    Z = p.asarray().astype(float); Z[Z < -1000] = np.nan
    return Z, tp[4], tp[3]
def _tifgitter(muster):
    Zo, lato, lono = _tif(muster.format(n="N38")); Zu, latu, lonu = _tif(muster.format(n="N37"))
    assert abs(lato - 39) < 1e-9 and abs(latu - 38) < 1e-9 and lono == lonu == 23.0
    # oben 39,0 … 38,000278 (3600 Zeilen), darunter 38,0 … 37,000278: nahtlos
    return Gitter(np.vstack([Zo, Zu]), 39.0, 23.0)
def _hgt(n):
    with open(D + f"srtm_{n}E023.hgt", "rb") as fh: Z = np.frombuffer(fh.read(), ">i2").reshape(3601, 3601).astype(float)
    Z[Z < -1000] = np.nan; return Z
_cache = {}
def modell(name):
    if name not in _cache:
        if name == "fabdem": _cache[name] = _tifgitter("fabdem_{n}E023.tif")
        elif name == "cop30": _cache[name] = _tifgitter("cop30_{n}_E023.tif")
        elif name == "srtm": _cache[name] = Gitter(np.vstack([_hgt("N38")[:-1], _hgt("N37")]), 39.0, 23.0)
        else: raise KeyError(name)
    return _cache[name]
