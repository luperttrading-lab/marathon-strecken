# Teilabruf aus Cloud-Optimized GeoTIFFs (COG) über HTTP-Range-Anfragen: Nur der Dateikopf und die gebrauchten internen Kacheln
# werden geladen (die drei USGS-1-m-Kacheln für Oʻahu sind zusammen 626 MB groß). Geladene Blöcke landen in ../dl/dem/blocks/,
# ein zweiter Lauf braucht kein Netz. tifffile liest den Kopf aus einem dateiähnlichen Objekt; die Kacheln werden mit
# page.decode entpackt.
import hashlib, io, os, time, urllib.request
import numpy as np, tifffile
BLK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../dl/dem/blocks")
UA = {"User-Agent": "MarathonProfil/1.0 (private, non-commercial)"}
def hole(url, a, b):
    os.makedirs(BLK, exist_ok=True)
    f = os.path.join(BLK, hashlib.md5(f"{url} {a} {b}".encode()).hexdigest())
    if os.path.exists(f) and os.path.getsize(f) == b - a + 1: return open(f, "rb").read()
    for att in range(6):
        try:
            d = urllib.request.urlopen(urllib.request.Request(url, headers={**UA, "Range": f"bytes={a}-{b}"}), timeout=120).read()
            if len(d) == b - a + 1: open(f, "wb").write(d); return d
        except Exception as e:
            print("  Fehler", e, flush=True)
        time.sleep(2 + 3 * att)
    raise IOError(f"{url} {a}-{b}")
class Fern(io.RawIOBase):
    """Dateiähnlicher Zugriff auf eine entfernte Datei in Blöcken zu 256 KB (nur für den Kopf)."""
    B = 1 << 18
    def __init__(self, url, groesse):
        self.url, self.size, self.pos, self.cache = url, groesse, 0, {}
    def seekable(self): return True
    def readable(self): return True
    def tell(self): return self.pos
    def seek(self, o, w=0):
        self.pos = o if w == 0 else (self.pos + o if w == 1 else self.size + o); return self.pos
    def _blk(self, i):
        if i not in self.cache: self.cache[i] = hole(self.url, i * self.B, min(self.size, (i + 1) * self.B) - 1)
        return self.cache[i]
    def read(self, n=-1):
        if n < 0: n = self.size - self.pos
        out = []
        while n > 0 and self.pos < self.size:
            i = self.pos // self.B; o = self.pos - i * self.B; c = self._blk(i)[o:o + n]
            out.append(c); self.pos += len(c); n -= len(c)
        return b"".join(out)
    def readinto(self, b):
        d = self.read(len(b)); b[:len(d)] = d; return len(d)
def groesse(url):
    os.makedirs(BLK, exist_ok=True)
    f = os.path.join(BLK, hashlib.md5(("HEAD " + url).encode()).hexdigest())
    if os.path.exists(f): return int(open(f).read())
    n = int(urllib.request.urlopen(urllib.request.Request(url, method="HEAD", headers=UA), timeout=60).headers["Content-Length"])
    open(f, "w").write(str(n)); return n
class COG:
    """Erste Seite (volle Auflösung) eines COG. Werte an Kartenkoordinaten (x, y in der Projektion der Datei) bilinear."""
    def __init__(self, url):
        self.url = url; self.tf = tifffile.TiffFile(Fern(url, groesse(url))); p = self.p = self.tf.pages[0]
        tp = p.tags["ModelTiepointTag"].value; sc = p.tags["ModelPixelScaleTag"].value
        gk = p.tags["GeoKeyDirectoryTag"].value; gk = {gk[i]: gk[i + 3] for i in range(4, len(gk), 4)}
        self.punkt = gk.get(1025) == 2                 # RasterPixelIsPoint: Mitte des ersten Pixels auf der Ecke
        self.x0, self.y0, self.sx, self.sy = tp[3], tp[4], sc[0], sc[1]
        if not self.punkt: self.x0 += self.sx / 2; self.y0 -= self.sy / 2   # Mitte des ersten Pixels
        self.H, self.W = p.shape[:2]; self.tw, self.th = p.tilewidth, p.tilelength
        self.nx = -(-self.W // self.tw); self.kach = {}
        nd = p.tags.get("GDAL_NODATA"); self.nodata = float(nd.value.strip("\x00")) if nd else None
        self.epsg = gk.get(3072)
    def kachel(self, i, j):
        if (i, j) not in self.kach:
            k = i * self.nx + j; a = self.p.dataoffsets[k]; n = self.p.databytecounts[k]
            if n == 0: z = np.full((self.th, self.tw), np.nan)
            else:
                z = self.p.decode(hole(self.url, a, a + n - 1), k)[0].reshape(self.th, self.tw).astype(float)
                if self.nodata is not None: z[z <= self.nodata + 1] = np.nan
            self.kach[(i, j)] = z
        return self.kach[(i, j)]
    def wert(self, r, c):
        r = np.asarray(r); c = np.asarray(c); out = np.full(r.shape, np.nan)
        ok = (r >= 0) & (r < self.H) & (c >= 0) & (c < self.W)
        for n in np.where(ok)[0]:
            i, j = r[n] // self.th, c[n] // self.tw
            out[n] = self.kachel(i, j)[r[n] - i * self.th, c[n] - j * self.tw]
        return out
    def __call__(self, x, y):
        fx = (np.asarray(x, float) - self.x0) / self.sx; fy = (self.y0 - np.asarray(y, float)) / self.sy
        c0 = np.floor(fx).astype(int); r0 = np.floor(fy).astype(int); ax = fx - c0; ay = fy - r0
        return (self.wert(r0, c0) * (1 - ax) * (1 - ay) + self.wert(r0, c0 + 1) * ax * (1 - ay) + self.wert(r0 + 1, c0) * (1 - ax) * ay
                + self.wert(r0 + 1, c0 + 1) * ax * ay)
