# Höhen alle 10 Linienmeter aus dem DGM1 Hessen (Laserscan, Bodenpunkte, 1-m-Raster, © HVBG) über den WCS des HVBG, wie
# werkzeuge/frankfurt/work/dgm.py, und zum Vergleich aus dem DOM1 Hessen (Oberflächenmodell derselben Befliegung: Bäume, Dächer,
# Brücken; WCS wie frankfurt/work/dom.py). Je ~250 m Linie ein GeoTIFF-Ausschnitt (EPSG:25832), bilinear abgelesen; dazu je Punkt
# das 25-%-Quantil der 5 × 5 DOM-Werte (darüber Fahrzeuge, Geländer, Laub). Die Ausschnitte bleiben in ../dl/wcs/.
# -> dgm_10m.json [[Linienmeter, lat, lon, DGM1, DOM1 bilinear, DOM1 Q25 5 × 5], …]
import io, json, os, time, urllib.request, concurrent.futures as cf
import numpy as np
from PIL import Image
from pyproj import Transformer
CACHE = "../dl/wcs"; os.makedirs(CACHE, exist_ok=True)
g = json.load(open("linie.json")); pts, d = g["pts"], g["d"]
dd = np.array(d); la_ = np.array([p[0] for p in pts]); lo_ = np.array([p[1] for p in pts])
ss = np.append(np.arange(0, d[-1], 10.0), d[-1])
la = np.interp(ss, dd, la_); lo = np.interp(ss, dd, lo_)
E, N = Transformer.from_crs(4326, 25832, always_xy=True).transform(lo, la)
E, N = np.asarray(E), np.asarray(N)
groups, a = [], 0
for i in range(1, len(ss) + 1):
    if i == len(ss) or max(E[a:i+1].max() - E[a:i+1].min(), N[a:i+1].max() - N[a:i+1].min()) > 250:
        groups.append((a, i)); a = i
URL = {"dgm1": "https://inspire-hessen.de/raster/dgm1/ows?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&COVERAGEID=he_dgm1&FORMAT=image/tiff",
       "dom1": "https://inspire-hessen.de/raster/dom1/ows?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&COVERAGEID=dom1&FORMAT=image/tiff"}
def raster(modell, e0, e1, n0, n1):
    f = f"{CACHE}/{modell}_{e0}_{n0}_{e1}_{n1}.tif"
    if not os.path.exists(f) or os.path.getsize(f) < 200:
        url = URL[modell] + f"&SUBSET=E({e0},{e1})&SUBSET=N({n0},{n1})"
        for att in range(5):
            try:
                raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "marathon-profile-check/1.0 (private use)"}), timeout=90).read()
                Image.open(io.BytesIO(raw)); open(f, "wb").write(raw); break
            except Exception:
                time.sleep(2 + 3 * att)
    return np.array(Image.open(f), dtype=float)
def fetch(gr):
    a, b = gr
    e0, e1 = int(np.floor(E[a:b].min())) - 5, int(np.ceil(E[a:b].max())) + 6
    n0, n1 = int(np.floor(N[a:b].min())) - 5, int(np.ceil(N[a:b].max())) + 6
    aus = []
    # Zeile r deckt N in [n1-1-r, n1-r), Spalte c deckt E in [e0+c, e0+c+1); Mittelpunkte bei +0,5
    c = E[a:b] - e0 - 0.5; r = (n1 - 0.5) - N[a:b]
    for modell in ("dgm1", "dom1"):
        A = raster(modell, e0, e1, n0, n1)
        c0 = np.clip(np.floor(c).astype(int), 0, A.shape[1] - 2); r0 = np.clip(np.floor(r).astype(int), 0, A.shape[0] - 2)
        fc, fr = c - c0, r - r0
        aus.append(A[r0, c0] * (1 - fc) * (1 - fr) + A[r0, c0 + 1] * fc * (1 - fr) + A[r0 + 1, c0] * (1 - fc) * fr + A[r0 + 1, c0 + 1] * fc * fr)
        if modell == "dom1":
            q = []
            for x, y in zip(E[a:b], N[a:b]):
                rr, cc = int(n1 - y), int(x - e0); q.append(float(np.percentile(A[rr - 2:rr + 3, cc - 2:cc + 3], 25)))
            aus.append(np.array(q))
    return a, [v.tolist() for v in aus]
t0 = time.time(); H = [[None] * len(ss) for _ in range(3)]
with cf.ThreadPoolExecutor(3) as ex:
    for a, vs in ex.map(fetch, groups):
        for j, v in enumerate(vs): H[j][a:a + len(v)] = v
res = [[float(s), float(x), float(y), round(h1, 3), round(h2, 3), round(h3, 3)] for s, x, y, h1, h2, h3 in zip(ss, la, lo, *H)]
print(len(res), "Punkte in", len(groups), "Ausschnitten,", round(time.time() - t0), "s")
h1 = np.array(H[0]); print("DGM1 min/max", h1.min().round(1), h1.max().round(1), "Start", h1[0].round(1), "Ende", h1[-1].round(1),
                          "; ungültig (< 0):", int((h1 < 0).sum()))
json.dump(res, open("dgm_10m.json", "w"))
