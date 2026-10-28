# Bodenhöhen alle 10 m (Linienmeter) aus dem LIDAR Composite DTM 1 m der Environment Agency (England, Höhen über ODN,
# Open Government Licence) über den WCS-Dienst: je 300 m Strecke ein Ausschnitt in British National Grid (EPSG:27700),
# bilinear abgelesen. Mit Argument „dsm“ dasselbe aus dem Oberflächenmodell (last return) -> dsm2026_10m.json
import json, sys, time, io, urllib.request, numpy as np
from PIL import Image
from pyproj import Transformer
DSM = len(sys.argv) > 1 and sys.argv[1] == "dsm"
SVC = ("lidar-composite-digital-surface-model-last-return-dsm-1m", "9ba4d5ac-d596-445a-9056-dae3ddec0178__Lidar_Composite_Elevation_LZ_DSM_1m") if DSM else \
      ("lidar-composite-digital-terrain-model-dtm-1m", "13787b9a-26a4-4775-8523-806d13af58fc__Lidar_Composite_Elevation_DTM_1m")
T = Transformer.from_crs(4326, 27700, always_xy=True)
g = json.load(open("gpx2026.json")); pts, d = g["pts"], g["d"]
dd = np.array(d); la_ = np.array([p[0] for p in pts]); lo_ = np.array([p[1] for p in pts])
ss = np.append(np.arange(0, d[-1], 10.0), d[-1]); la = np.interp(ss, dd, la_); lo = np.interp(ss, dd, lo_)
E, N = T.transform(lo, la); H = np.full(len(ss), np.nan)
def hole(e0, n0, e1, n1):
    url = (f"https://environment.data.gov.uk/spatialdata/{SVC[0]}/wcs?service=WCS&version=2.0.1&request=GetCoverage&CoverageId={SVC[1]}"
           f"&format=image/tiff&subset=E({e0},{e1})&subset=N({n0},{n1})")
    for att in range(5):
        try: return np.array(Image.open(io.BytesIO(urllib.request.urlopen(url, timeout=120).read())), dtype=float)
        except Exception: time.sleep(3 + 5 * att)
    return None
t0 = time.time(); B = 30
for a in range(0, len(ss), 30):
    ii = np.arange(a, min(a + 31, len(ss)))
    e0, e1 = int(E[ii].min()) - B, int(E[ii].max()) + B; n0, n1 = int(N[ii].min()) - B, int(N[ii].max()) + B
    A = hole(e0, n0, e1, n1)
    if A is None: print("fehlt", a); continue
    A[A < -100] = np.nan
    # Pixel (Zeile 0 = Nordrand n1, Spalte 0 = Westrand e0), Mittelpunkte bei +0,5 m
    c = E[ii] - e0 - 0.5; r = n1 - N[ii] - 0.5
    c0 = np.clip(np.floor(c).astype(int), 0, A.shape[1] - 2); r0 = np.clip(np.floor(r).astype(int), 0, A.shape[0] - 2); fc = c - c0; fr = r - r0
    H[ii] = (A[r0, c0] * (1 - fc) * (1 - fr) + A[r0, c0 + 1] * fc * (1 - fr) + A[r0 + 1, c0] * (1 - fc) * fr + A[r0 + 1, c0 + 1] * fc * fr)
res = [[float(s), float(x), float(y), None if np.isnan(h) else float(h)] for s, x, y, h in zip(ss, la, lo, H)]
print(len(res), "Punkte in", round(time.time() - t0), "s; fehlend:", int(np.isnan(H).sum()), "min/max", round(np.nanmin(H), 1), round(np.nanmax(H), 1))
json.dump(res, open("dsm2026_10m.json" if DSM else "dgm2026_10m.json", "w"))
