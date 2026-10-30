# Bodenhöhen alle 10 m (Linienmeter) aus dem Geländemodell der Stadt Wien („Geländemodell Raster Wien“, MA 41 Stadtvermessung,
# Open Government Data, CC BY 4.0, Stand 20.11.2025): 1-m-Raster als GeoTIFF float32 je Blatt der Mehrzweckkarte 1:5000
# (2,5 × 2,5 km, MGI / Austria GK East, EPSG 31256), Download
# https://www.wien.gv.at/ma41datenviewer/downloads/geodaten/dgm_tif/<Blatt>_dgm_tif.zip (Blattschnitt aus dem WFS der Stadt,
# ogdwien:MZKBLATT5000OGD, ../dl/wfs_MZKBLATT5000OGD.json). Das Modell ist im Straßenraum aus den Höhenpunkten und Bruchkanten
# der Mehrzweckkarte gerechnet (± 10 cm), sonst aus Laserscans; Brücken enthält es nicht. Höhen über Wiener Null; + 156,68 m
# ergibt Meter über Adria (Pegel Triest), laut Stadt Wien und gleich dem Unterschied HOEHE_ADRIA − HOEHE_WIEN der
# Höhenfestpunkte im WFS. Je 10-m-Punkt bilinear zwischen den Zellmitten (ganze Meter).
# -> dgm2026_10m.json [Linienmeter, Breite, Länge, Höhe über Adria oder None]
import json, os, sys, time, zipfile, urllib.request
import numpy as np, tifffile
from pyproj import Transformer
from matplotlib.path import Path
T = Transformer.from_crs(4326, 31256, always_xy=True)
WIENER_NULL = 156.68
DL = "../dl/dgm"; os.makedirs(DL, exist_ok=True)
g = json.load(open("gpx2026.json")); pts, d = g["pts"], np.array(g["d"])
la_ = np.array([p[0] for p in pts]); lo_ = np.array([p[1] for p in pts])
ss = np.append(np.arange(0, d[-1], 10.0), d[-1]); la = np.interp(ss, d, la_); lo = np.interp(ss, d, lo_)
x, y = T.transform(lo, la)
# Blätter, die die Linie (±60 m, Punkte alle 5 m) berühren
xd, yd = T.transform(np.interp(np.arange(0, d[-1], 5.0), d, lo_), np.interp(np.arange(0, d[-1], 5.0), d, la_))
blaetter = {}
for f in json.load(open("../dl/wfs_MZKBLATT5000OGD.json"))["features"]:
    c = np.array(f["geometry"]["coordinates"][0]); blaetter[f["properties"]["BNR5000"]] = (c[:, 0].min(), c[:, 1].min(), c[:, 0].max(), c[:, 1].max())
noetig = sorted({b for b, (x0, y0, x1, y1) in blaetter.items() if np.any((xd > x0 - 60) & (xd < x1 + 60) & (yd > y0 - 60) & (yd < y1 + 60))})
print(len(noetig), "Blätter:", noetig, flush=True)
def hole(b):
    n = b.replace("/", "_"); f = f"{DL}/{n}_dgm_tif.zip"; tif = f"{DL}/{n}/{n}_dgm.tif"
    if os.path.exists(tif): return tif
    for att in range(6):
        try:
            data = urllib.request.urlopen(urllib.request.Request(f"https://www.wien.gv.at/ma41datenviewer/downloads/geodaten/dgm_tif/{n}_dgm_tif.zip",
                                          headers={"User-Agent": "marathon-profile-check/1.0"}), timeout=300).read()
            open(f, "wb").write(data); zipfile.ZipFile(f).extractall(f"{DL}/{n}"); return tif
        except Exception as e: print("  Fehler", b, e, flush=True); time.sleep(5 + 5 * att)
    sys.exit("Blatt fehlt: dgm.py noch einmal starten")
R = {}
for b in noetig:
    tif = hole(b)
    with tifffile.TiffFile(tif) as t:
        p = t.pages[0]; tp = p.tags["ModelTiepointTag"].value; sc = p.tags["ModelPixelScaleTag"].value
        a = p.asarray().astype(np.float64)
    nodata = None
    try: nodata = float(t.pages[0].tags["GDAL_NODATA"].value)
    except Exception: pass
    if nodata is not None: a[a == nodata] = np.nan
    a[a < -100] = np.nan
    assert sc[0] == 1 and sc[1] == 1
    R[b] = (tp[3] + 0.5, tp[4] - 0.5, a)   # Mitte der Zelle oben links
    print(b, a.shape, "Mitte oben links", R[b][:2], "Wiener Null", np.nanmin(a).round(2), np.nanmax(a).round(2), flush=True)
def wert(px, py):
    for b, (cx, cy, a) in R.items():
        c = px - cx; r = cy - py; c0, r0 = int(np.floor(c)), int(np.floor(r))
        if c0 < 0 or r0 < 0 or c0 + 1 >= a.shape[1] or r0 + 1 >= a.shape[0]: continue
        q = a[r0:r0 + 2, c0:c0 + 2]
        if not np.all(np.isfinite(q)): continue
        fc, fr = c - c0, r - r0
        return float(q[0, 0] * (1 - fc) * (1 - fr) + q[0, 1] * fc * (1 - fr) + q[1, 0] * (1 - fc) * fr + q[1, 1] * fc * fr) + WIENER_NULL
    return None
res = [[float(s), float(a_), float(b_), wert(px, py)] for s, a_, b_, px, py in zip(ss, la, lo, x, y)]
fehlt = [r[0] for r in res if r[3] is None]
print(len(res), "Punkte, ohne Wert:", len(fehlt), fehlt[:20])
hv = [r[3] for r in res if r[3] is not None]; print("Höhe über Adria min/max", round(min(hv), 2), round(max(hv), 2))
json.dump(res, open("dgm2026_10m.json", "w"))
