# Bodenhöhen alle 10 m (Linienmeter) aus dem AHN4 (Actueel Hoogtebestand Nederland, Laserbefliegung 2020–2022), Geländemodell
# DTM 0,5 m („maaiveld“: nur als Boden klassifizierte Punkte, quadratisch-IDW auf 0,5 m), über den WCS von PDOK
# (https://service.pdok.nl/rws/ahn/wcs/v1_0, Coverage dtm_05m, GeoTIFF float32 in RD New, Höhen in m über NAP). Kacheln von
# 250 × 250 m, die die Linie (±15 m) berühren, Zwischenstand ../dl/ahn/. Je Punkt der Median der gültigen Zellen im Umkreis von
# 1,0 m (13 Zellen); weniger als 4 gültige Zellen: Lücke. Lücken hat das DTM unter Gebäuden, auf Wasser und auf Brücken (Brücken
# sind dort keine Bodenpunkte); sie behandelt clean.py. Zum Vergleich auf Brücken dieselben Kacheln aus dem Oberflächenmodell
# (dsm_05m, alle Punkte außer Wasser), nur wo das DTM eine Lücke hat.
# -> dgm2026_10m.json [Linienmeter, Breite, Länge, Höhe DTM oder None, Höhe DSM oder None]
import json, os, sys, time, urllib.request, concurrent.futures as cf
import numpy as np
from PIL import Image
from pyproj import Transformer
T = Transformer.from_crs(4326, 28992, always_xy=True)
CACHE = "../dl/ahn"; os.makedirs(CACHE, exist_ok=True)
g = json.load(open("gpx2026.json")); pts, d = g["pts"], np.array(g["d"])
la_ = np.array([p[0] for p in pts]); lo_ = np.array([p[1] for p in pts])
ss = np.append(np.arange(0, d[-1], 10.0), d[-1]); la = np.interp(ss, d, la_); lo = np.interp(ss, d, lo_)
x, y = T.transform(lo, la)
K = 250.0
def kacheln(xs, ys, r=15):
    s = set()
    for a, b in zip(xs, ys):
        for dx in (-r, 0, r):
            for dy in (-r, 0, r): s.add((int((a + dx) // K), int((b + dy) // K)))
    return sorted(s)
# auch zwischen den 10-m-Punkten (Linie dicht)
xd, yd = T.transform(np.interp(np.arange(0, d[-1], 2.0), d, lo_), np.interp(np.arange(0, d[-1], 2.0), d, la_))
KL = kacheln(xd, yd)
URL = ("https://service.pdok.nl/rws/ahn/wcs/v1_0?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&COVERAGEID={c}"
       "&SUBSET=x({x0:.0f},{x1:.0f})&SUBSET=y({y0:.0f},{y1:.0f})&FORMAT=image/tiff")
def hole(args):
    c, i, j = args
    f = f"{CACHE}/{c}_{i}_{j}.tif"
    if os.path.exists(f) and os.path.getsize(f) > 1000: return f
    for att in range(8):
        try:
            req = urllib.request.Request(URL.format(c=c, x0=i * K, x1=(i + 1) * K, y0=j * K, y1=(j + 1) * K), headers={"User-Agent": "marathon-profile-check/1.0"})
            data = urllib.request.urlopen(req, timeout=120).read()
            if data[:2] not in (b"II", b"MM"): raise ValueError(data[:200])
            open(f + ".tmp", "wb").write(data); os.replace(f + ".tmp", f); return f
        except Exception as e:
            print("  Fehler", c, i, j, str(e)[:120], flush=True); time.sleep(2 + 3 * att)
    return None
def lade(c, kl):
    t0 = time.time()
    with cf.ThreadPoolExecutor(4) as ex: res = list(ex.map(hole, [(c, i, j) for i, j in kl]))
    print(c, len(kl), "Kacheln,", sum(r is None for r in res), "fehlen,", round(time.time() - t0), "s", flush=True)
    if any(r is None for r in res): sys.exit("Kacheln fehlen: dgm.py noch einmal starten")
lade("dtm_05m", KL)
_cache = {}
def raster(c, i, j):
    k = (c, i, j)
    if k not in _cache:
        im = Image.open(f"{CACHE}/{c}_{i}_{j}.tif"); a = np.array(im, dtype=np.float32)
        tp = im.tag_v2.get(33922); assert abs(tp[3] - i * K) < 0.01 and abs(tp[4] - (j + 1) * K) < 0.01, tp
        a[(a > 1e30) | (a < -50)] = np.nan; _cache[k] = a
    return _cache[k]
OFF = [(dx, dy) for dx in range(-2, 3) for dy in range(-2, 3) if dx * dx + dy * dy <= 4]   # 13 Zellen, Umkreis 1,0 m
def wert(c, px, py):
    v = []
    for dx, dy in OFF:
        X = px + dx * 0.5; Y = py + dy * 0.5
        i, j = int(X // K), int(Y // K); a = raster(c, i, j)
        col = int((X - i * K) / 0.5); row = int(((j + 1) * K - Y) / 0.5)
        if 0 <= row < a.shape[0] and 0 <= col < a.shape[1] and not np.isnan(a[row, col]): v.append(float(a[row, col]))
    return (float(np.median(v)) if len(v) >= 4 else None), len(v)
dtm = [wert("dtm_05m", a, b)[0] for a, b in zip(x, y)]
luecke = [n for n, v in enumerate(dtm) if v is None]
print(len(ss), "Punkte,", len(luecke), "ohne Bodenhöhe im DTM")
# DSM nur für die Kacheln mit Lücken
KD = kacheln([x[n] for n in luecke], [y[n] for n in luecke], r=3)
lade("dsm_05m", KD)
dsm = {n: wert("dsm_05m", x[n], y[n])[0] for n in luecke}
res = [[float(s), float(a), float(b), h, dsm.get(n)] for n, (s, a, b, h) in enumerate(zip(ss, la, lo, dtm))]
json.dump(res, open("dgm2026_10m.json", "w"))
hv = [h for h in dtm if h is not None]
print("DTM min/max", round(min(hv), 2), round(max(hv), 2))
from itertools import groupby
for k, grp in groupby(enumerate(dtm), key=lambda t: t[1] is None):
    grp = list(grp)
    if k: print(f"  Lücke {ss[grp[0][0]]:7.0f}–{ss[grp[-1][0]]:7.0f} m ({len(grp)} Punkte), DSM {[dsm[n] and round(dsm[n], 1) for n, _ in grp][:8]}")
