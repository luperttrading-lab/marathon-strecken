# Lesen von TINITALY/1.1 (INGV, 10-m-Raster, GeoTIFF Float32, WGS 84 / UTM 32 N, Blätter w46075_s10 und w46575_s10 aus
# https://tinitaly.pi.ingv.it/Download_Area1_1.html, entpackt unter ../dl/tinitaly/). Ecke oben links laut GeoTIFF-Tag
# (Ecke der Zelle, PixelIsArea), Zellmitten also 5 m weiter; NODATA −9999. Bilinear zwischen den Zellmitten.
import glob, numpy as np
from PIL import Image
from pyproj import Transformer
Image.MAX_IMAGE_PIXELS = None
T32 = Transformer.from_crs(4326, 32632, always_xy=True)
class Blatt:
    def __init__(self, f):
        im = Image.open(f); tg = im.tag_v2
        self.x0, self.y0 = tg[33922][3], tg[33922][4]; self.dx = tg[33550][0]
        self.a = np.array(im, dtype=np.float64); self.a[self.a < -9000] = np.nan; self.name = f.split("/")[-1][:-4]
    def wert(self, x, y):
        c = (x - self.x0) / self.dx - 0.5; r = (self.y0 - y) / self.dx - 0.5; c0, r0 = int(np.floor(c)), int(np.floor(r))
        if c0 < 0 or r0 < 0 or c0 + 1 >= self.a.shape[1] or r0 + 1 >= self.a.shape[0]: return None
        q = self.a[r0:r0 + 2, c0:c0 + 2]
        if not np.all(np.isfinite(q)): return None
        fc, fr = c - c0, r - r0
        return float(q[0, 0] * (1 - fc) * (1 - fr) + q[0, 1] * fc * (1 - fr) + q[1, 0] * (1 - fc) * fr + q[1, 1] * fc * fr)
BLAETTER = None
def hoehe(la, lo):
    global BLAETTER
    if BLAETTER is None: BLAETTER = [Blatt(f) for f in sorted(glob.glob("../dl/tinitaly/*/*/*.tif"))]
    x, y = T32.transform(lo, la)
    for b in BLAETTER:
        v = b.wert(x, y)
        if v is not None: return v, b.name
    return None, None
