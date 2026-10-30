# Gegenprobe der Höhen mit dem österreichweiten Laser-Geländemodell des BEV (ALS DTM, Höhenraster 1 m, Stichtag 15.09.2025,
# Kachel ALS_DTM_CRS3035RES50000mN2800000E4750000.tif, 50 × 50 km, ETRS89 / LAEA Europe, EPSG 3035, CC BY 4.0,
# https://data.bev.gv.at/download/ALS/DTM/20250915/). Die Datei ist ein gekacheltes GeoTIFF von 7,9 GB; gelesen werden über
# HTTP-Range nur die 256 × 256-m-Kacheln entlang der Linie (httpfile.py), Zwischenstand ../dl/als/. Je 10-m-Punkt bilinear.
# -> als2026_10m.json [Linienmeter, Höhe oder None]
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np, tifffile
from pyproj import Transformer
from httpfile import HttpFile
URL = "https://data.bev.gv.at/download/ALS/DTM/20250915/ALS_DTM_CRS3035RES50000mN2800000E4750000.tif"
T = Transformer.from_crs(4326, 3035, always_xy=True)
r = json.load(open("dgm2026_10m.json")); s = np.array([x[0] for x in r])
x, y = T.transform([q[2] for q in r], [q[1] for q in r])
import urllib.request
groesse = int(urllib.request.urlopen(urllib.request.Request(URL, method="HEAD"), timeout=60).headers["Content-Length"])
tf = tifffile.TiffFile(HttpFile(URL, groesse)); p = tf.pages[0]
x0, y0 = p.tags["ModelTiepointTag"].value[3:5]; tw, tl = p.tilewidth, p.tilelength; ntx = -(-p.shape[1] // tw)
nod = float(p.tags["GDAL_NODATA"].value); fh = tf.filehandle
kach = {}
def kachel(i, j):
    k = (i, j)
    if k not in kach:
        f = f"../dl/als/{i}_{j}.npy"
        if os.path.exists(f): kach[k] = np.load(f)
        else:
            idx = j * ntx + i; fh.seek(p.dataoffsets[idx]); daten = fh.read(p.databytecounts[idx])
            a = p.decode(daten, idx)[0].reshape(tl, tw).astype(np.float64); a[a == nod] = np.nan; np.save(f, a); kach[k] = a
    return kach[k]
def zelle(c, rr):
    i, j = c // tw, rr // tl; return kachel(i, j)[rr - j * tl, c - i * tw]
def wert(px, py):
    c = px - (x0 + 0.5); rr = (y0 - 0.5) - py; c0, r0 = int(np.floor(c)), int(np.floor(rr)); fc, fr = c - c0, rr - r0
    q = np.array([[zelle(c0, r0), zelle(c0 + 1, r0)], [zelle(c0, r0 + 1), zelle(c0 + 1, r0 + 1)]])
    if not np.all(np.isfinite(q)): return None
    return float(q[0, 0] * (1 - fc) * (1 - fr) + q[0, 1] * fc * (1 - fr) + q[1, 0] * (1 - fc) * fr + q[1, 1] * fc * fr)
res = [[float(a), wert(px, py)] for a, px, py in zip(s, x, y)]
print(len(kach), "Kacheln;", sum(v is None for _, v in res), "Punkte ohne Wert")
json.dump(res, open("als2026_10m.json", "w"))
h = np.array([q[3] for q in r]); a = np.array([v if v is not None else np.nan for _, v in res]); dd = a - h
print(f"ALS minus Stadt-Wien-DGM: Median {np.nanmedian(dd):+.2f} m, Hälfte zwischen {np.nanpercentile(dd, 25):+.2f} und {np.nanpercentile(dd, 75):+.2f}, "
      f"90 % zwischen {np.nanpercentile(dd, 5):+.2f} und {np.nanpercentile(dd, 95):+.2f} m")
