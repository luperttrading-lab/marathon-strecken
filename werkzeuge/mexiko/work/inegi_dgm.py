# Lesen der INEGI-Höhenmodelle (../dl/inegi/<Blatt>_<Ausgabe>/, geladen mit inegi.py) und bilineares Ablesen in UTM 14 N.
#   BIL (5m2017/5m2018, 15m2020): Float32 little-endian, Zeilen von oben, ULXMAP/ULYMAP = Mitte der Zelle oben links, NODATA −3,4e38.
#   XYZ (5m2011): Textzeilen „Ost Nord Höhe“ auf einem 5-m-Raster (Zellmitten), Lücken ohne Zeile.
# Die .prj der BIL-Dateien nennt MEXICO_ITRF_2008_UTM_Zone_14N (GRS80), die XYZ-Datei ITRF92 Epoche 1988.0; beides weicht von
# WGS84 (OSM) um weniger als einen Meter ab und wird nicht umgerechnet.
import glob, os, numpy as np
from pyproj import Transformer
T = Transformer.from_crs(4326, 32614, always_xy=True)   # UTM 14 N
class Raster:
    def __init__(self, x0, y0, dx, a, name): self.x0, self.y0, self.dx, self.a, self.name = x0, y0, dx, a, name   # a[0] = oberste Zeile, y0 = Mitte oben
    def wert(self, x, y):
        c = (x - self.x0) / self.dx; r = (self.y0 - y) / self.dx; c0, r0 = int(np.floor(c)), int(np.floor(r))
        if c0 < 0 or r0 < 0 or c0 + 1 >= self.a.shape[1] or r0 + 1 >= self.a.shape[0]: return None
        q = self.a[r0:r0 + 2, c0:c0 + 2]
        if not np.all(np.isfinite(q)): return None
        fc, fr = c - c0, r - r0
        return float(q[0, 0] * (1 - fc) * (1 - fr) + q[0, 1] * fc * (1 - fr) + q[1, 0] * (1 - fc) * fr + q[1, 1] * fc * fr)
def lies_bil(d):
    hdr = glob.glob(d + "/*.hdr")[0]; h = {l.split()[0]: l.split()[1] for l in open(hdr) if l.strip()}
    nr, nc = int(h["NROWS"]), int(h["NCOLS"]); a = np.fromfile(hdr[:-4] + ".bil", dtype="<f4").reshape(nr, nc).astype(float)
    a[a < -1e30] = np.nan
    assert "Zone_14N" in open(hdr[:-4] + ".prj").read()
    return Raster(float(h["ULXMAP"]), float(h["ULYMAP"]), float(h["XDIM"]), a, os.path.basename(d))
def lies_xyz(d):
    cache = d + "/raster.npz"
    if os.path.exists(cache):
        z = np.load(cache); return Raster(float(z["x0"]), float(z["y0"]), 5.0, z["a"], os.path.basename(d))
    v = np.loadtxt(glob.glob(d + "/*.xyz")[0]); x, y, hh = v[:, 0], v[:, 1], v[:, 2]
    x0, y1 = x.min(), y.max(); c = np.round((x - x0) / 5).astype(int); r = np.round((y1 - y) / 5).astype(int)
    a = np.full((r.max() + 1, c.max() + 1), np.nan); a[r, c] = hh
    np.savez_compressed(cache, x0=x0, y0=y1, a=a)
    return Raster(x0, y1, 5.0, a, os.path.basename(d))
def lade(ausgabe):
    """ausgabe: '5m2011', '5m201x' (2017/2018) oder '15m2020'"""
    out = []
    for d in sorted(glob.glob("../dl/inegi/*_" + ausgabe.replace("201x", "201[78]"))):
        out.append(lies_xyz(d) if ausgabe == "5m2011" else lies_bil(d))
    return out
def hoehe(raster, la, lo):
    x, y = T.transform(lo, la)
    for r in raster:
        v = r.wert(x, y)
        if v is not None: return v, r.name
    return None, None
