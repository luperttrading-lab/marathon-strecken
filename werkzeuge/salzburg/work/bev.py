# Höhen aus den Laser-Höhenmodellen des BEV (ALS DTM bzw. DSM, Höhenraster 1 m, Serie Stichtag 15.09.2025; in Salzburg Befliegung
# 2022 laut Metadatenübersicht des BEV, bev_meta.py), CC BY 4.0, https://data.bev.gv.at/download/ALS/<DTM|DSM>/20250915/.
# Die Kacheln sind Cloud-Optimized GeoTIFFs zu 50 × 50 km (EPSG 3035, ETRS89/LAEA, Name nach der linken unteren Ecke), je 4–9 GB.
# Gelesen werden über HTTP-Range nur die inneren Kacheln (256 × 256 m o. ä.) an der Strecke (httpfile.py), abgelegt als .npy in
# ../dl/bev/<typ>_<E>_<N>/. Die Strecke liegt auf zwei Kacheln (Grenze E = 4 550 000, Salzach-Ostufer bis Hellbrunn).
# Höhen laut Metadaten EVRF2000 (EPSG 9274), wie in Wien. Muster: werkzeuge/wien/work/als.py und dsm.py.
import os, sys, urllib.request
import numpy as np, tifffile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from httpfile import HttpFile
DL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../dl/bev")
URL = "https://data.bev.gv.at/download/ALS/{t}/20250915/ALS_{t}_CRS3035RES50000mN{n}E{e}.tif"
class Kachel:
    def __init__(self, typ, e, n):
        self.url = URL.format(t=typ, n=n, e=e); self.ordner = f"{DL}/{typ}_{e}_{n}"; os.makedirs(self.ordner, exist_ok=True)
        groesse = int(urllib.request.urlopen(urllib.request.Request(self.url, method="HEAD"), timeout=60).headers["Content-Length"])
        self.tf = tifffile.TiffFile(HttpFile(self.url, groesse)); p = self.p = self.tf.pages[0]
        self.x0, self.y0 = p.tags["ModelTiepointTag"].value[3:5]; sc = p.tags["ModelPixelScaleTag"].value
        assert abs(sc[0] - 1) < 1e-9 and abs(sc[1] - 1) < 1e-9, sc
        self.tw, self.tl = p.tilewidth, p.tilelength; self.ntx = -(-p.shape[1] // self.tw)
        self.nod = float(p.tags["GDAL_NODATA"].value); self.fh = self.tf.filehandle; self.kach = {}
        self.shape = p.shape
    def kachel(self, i, j):
        if (i, j) not in self.kach:
            f = f"{self.ordner}/{i}_{j}.npy"
            if os.path.exists(f): self.kach[(i, j)] = np.load(f)
            else:
                idx = j * self.ntx + i; a_, n_ = self.p.dataoffsets[idx], self.p.databytecounts[idx]
                daten = holen(self.url, a_, n_)   # eine Range-Abfrage je Kachel statt 64-KB-Blöcken
                a = self.p.decode(daten, idx)[0].reshape(self.tl, self.tw).astype(np.float64); a[a == self.nod] = np.nan
                np.save(f, a); self.kach[(i, j)] = a
        return self.kach[(i, j)]
    def zelle(self, c, r):
        if c < 0 or r < 0 or c >= self.shape[1] or r >= self.shape[0]: return np.nan
        return self.kachel(c // self.tw, r // self.tl)[r % self.tl, c % self.tw]
    def bilinear(self, x, y):
        # Pixelmitten: Spalte c hat die Mitte bei x0 + c + 0,5 (PixelIsArea)
        c = x - (self.x0 + 0.5); r = (self.y0 - 0.5) - y; c0, r0 = int(np.floor(c)), int(np.floor(r)); fc, fr = c - c0, r - r0
        q = np.array([[self.zelle(c0, r0), self.zelle(c0 + 1, r0)], [self.zelle(c0, r0 + 1), self.zelle(c0 + 1, r0 + 1)]])
        if not np.all(np.isfinite(q)): return np.nan
        return float(q[0, 0] * (1 - fc) * (1 - fr) + q[0, 1] * fc * (1 - fr) + q[1, 0] * (1 - fc) * fr + q[1, 1] * fc * fr)
    def umkreis(self, x, y, rad):
        """alle Zellwerte, deren Mitte höchstens rad m von (x, y) entfernt ist"""
        v = []
        for dx in range(-int(rad) - 1, int(rad) + 2):
            for dy in range(-int(rad) - 1, int(rad) + 2):
                cx = int(np.floor(x - self.x0)) + dx; cy = int(np.floor(self.y0 - y)) + dy
                mx = self.x0 + cx + 0.5; my = self.y0 - cy - 0.5
                if (mx - x) ** 2 + (my - y) ** 2 <= rad * rad:
                    a = self.zelle(cx, cy)
                    if np.isfinite(a): v.append(a)
        return v
def holen(url, a, n):
    for att in range(5):
        try:
            req = urllib.request.Request(url, headers={"Range": f"bytes={a}-{a + n - 1}", "User-Agent": "marathon-profile-check/1.0"})
            b = urllib.request.urlopen(req, timeout=180).read()
            if len(b) == n: return b
        except Exception as e: print("  Fehler", e, flush=True)
        import time; time.sleep(3 + 5 * att)
    raise RuntimeError("Kachel nicht geladen")
_K = {}
def kachel_fuer(typ, x, y):
    e, n = int(x // 50000 * 50000), int(y // 50000 * 50000)
    if (typ, e, n) not in _K: _K[(typ, e, n)] = Kachel(typ, e, n)
    return _K[(typ, e, n)]
def hoehe(typ, x, y): return kachel_fuer(typ, x, y).bilinear(x, y)
def umkreis(typ, x, y, rad): return kachel_fuer(typ, x, y).umkreis(x, y, rad)
