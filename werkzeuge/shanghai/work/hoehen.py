# Lesen der frei abrufbaren Höhenmodelle (Kacheln unter ../dl/dem/, WGS 84, Kachel N31E121 = 31–32° N, 121–122° O; die ganze Strecke
# liegt darin). rasterio gibt es nicht: tifffile und numpy. Muster: werkzeuge/stockholm/work/hoehen.py.
# - FABDEM V1-2 (fabdem.py): Copernicus GLO-30 ohne Gebäude und Wald, 1″ × 1″, Höhen über dem Geoid EGM2008, NODATA −9999.
# - Copernicus DEM GLO-30 (AWS copernicus-dem-30m): Oberflächenmodell aus TanDEM-X 2011–2015 (mit Häusern, Bäumen, Hochstraßen),
#   EGM2008; südlich von 50° 1″ × 1″.
#   Beide GeoTIFF sagen RasterPixelIsPoint (GeoKey 1025 = 2): Die Mitte des ersten Pixels liegt genau auf der Ecke der Kachel.
# - SRTM 1″ (AWS Terrain Tiles skadi, .hgt.gz): Oberflächenmodell aus dem Radarflug im Februar 2000, EGM96; 3601 × 3601 Werte,
#   Big Endian int16, erste Zeile = Nordrand.
# Bilinear zwischen den Rasterpunkten.
import gzip, os
import numpy as np, tifffile
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../dl/dem/")
class Gitter:
    def __init__(self, Z, lat0, lon0, sy, sx):
        self.Z, self.lat0, self.lon0, self.sy, self.sx = Z, lat0, lon0, sy, sx   # Z[0, 0] liegt auf (lat0, lon0)
    def __call__(self, lat, lon):
        fy = (self.lat0 - np.asarray(lat, float)) / self.sy; fx = (np.asarray(lon, float) - self.lon0) / self.sx
        i0 = np.floor(fy).astype(int); j0 = np.floor(fx).astype(int); ay = fy - i0; ax = fx - j0
        Z = self.Z
        return (Z[i0, j0] * (1 - ax) * (1 - ay) + Z[i0, j0 + 1] * ax * (1 - ay) + Z[i0 + 1, j0] * (1 - ax) * ay
                + Z[i0 + 1, j0 + 1] * ax * ay)
def _tif(f):
    p = tifffile.TiffFile(D + f).pages[0]
    gk = p.tags["GeoKeyDirectoryTag"].value; gk = {gk[i]: gk[i + 3] for i in range(4, len(gk), 4)}
    assert gk.get(1025) == 2, "erwartet RasterPixelIsPoint"
    tp = p.tags["ModelTiepointTag"].value; sc = p.tags["ModelPixelScaleTag"].value
    Z = p.asarray().astype(float); Z[Z < -1000] = np.nan
    return Gitter(Z, tp[4], tp[3], sc[1], sc[0])
def _hgt(f):
    with gzip.open(D + f, "rb") as fh: Z = np.frombuffer(fh.read(), ">i2").reshape(3601, 3601).astype(float)
    Z[Z < -1000] = np.nan
    return Gitter(Z, 32.0, 121.0, 1 / 3600, 1 / 3600)
_cache = {}
def modell(name):
    if name not in _cache:
        if name == "fabdem": _cache[name] = _tif("fabdem_N31E121.tif")
        elif name == "cop30": _cache[name] = _tif("cop30_N31_E121.tif")
        elif name == "srtm": _cache[name] = _hgt("srtm_N31E121.hgt.gz")
        else: raise KeyError(name)
    return _cache[name]
