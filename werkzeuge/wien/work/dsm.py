# Fahrbahn der Brücken: Oberflächenmodell des BEV (ALS DSM, Höhenraster 1 m, Stichtag 15.09.2025, Kachel
# ALS_DSM_CRS3035RES50000mN2800000E4750000.tif, EPSG 3035, Höhen EVRF2000, CC BY 4.0, https://data.bev.gv.at/download/ALS/DSM/
# 20250915/), über HTTP-Range nur die Kacheln an den Brücken (../dl/als_dsm/). Je 10-m-Punkt das 25-%-Quantil der Zellen im
# Umkreis von 2 m (Fahrbahn ohne Geländer, Laternen, Fahrzeuge). Plus 0,51 m (Unterschied Geländemodell der Stadt minus ALS-DTM
# des BEV entlang der ganzen Strecke, als2026_10m.json: Höhen über Adria statt EVRF2000). Abgefragt werden die Punkte, die
# strassen.py auf einer OSM-Brücke sieht, und 80 m davor und danach. clean.py nimmt daraus die Fahrbahn der Reichsbrücke.
# -> dsm_10m.json {Index im 10-m-Raster: Höhe}
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np, tifffile, urllib.request
from pyproj import Transformer
from httpfile import HttpFile
URL = "https://data.bev.gv.at/download/ALS/DSM/20250915/ALS_DSM_CRS3035RES50000mN2800000E4750000.tif"
T = Transformer.from_crs(4326, 3035, always_xy=True)
r = json.load(open("dgm2026_10m.json")); st = json.load(open("strassen.json"))
x, y = T.transform([q[2] for q in r], [q[1] for q in r])
br = [i for i, o in enumerate(st) if o[3] not in ("", "no")]
sel = sorted({j for i in br for j in range(max(0, i - 8), min(len(r), i + 9))})
groesse = int(urllib.request.urlopen(urllib.request.Request(URL, method="HEAD"), timeout=60).headers["Content-Length"])
tf = tifffile.TiffFile(HttpFile(URL, groesse)); p = tf.pages[0]
x0, y0 = p.tags["ModelTiepointTag"].value[3:5]; tw, tl = p.tilewidth, p.tilelength; ntx = -(-p.shape[1] // tw)
nod = float(p.tags["GDAL_NODATA"].value); fh = tf.filehandle; kach = {}
def kachel(i, j):
    if (i, j) not in kach:
        f = f"../dl/als_dsm/{i}_{j}.npy"
        if os.path.exists(f): kach[(i, j)] = np.load(f)
        else:
            idx = j * ntx + i; fh.seek(p.dataoffsets[idx]); a = p.decode(fh.read(p.databytecounts[idx]), idx)[0].reshape(tl, tw).astype(np.float64)
            a[a == nod] = np.nan; np.save(f, a); kach[(i, j)] = a
    return kach[(i, j)]
def wert(px, py):
    v = []
    for dx in (-2, -1, 0, 1, 2):
        for dy in (-2, -1, 0, 1, 2):
            if dx * dx + dy * dy > 4: continue
            cc = int(round(px + dx - (x0 + 0.5))); rr = int(round((y0 - 0.5) - (py + dy))); a = kachel(cc // tw, rr // tl)[rr % tl, cc % tw]
            if np.isfinite(a): v.append(a)
    return float(np.percentile(v, 25)) + 0.51 if v else None
out = {i: wert(x[i], y[i]) for i in sel}
print(len(out), "Punkte,", len(kach), "Kacheln")
json.dump(out, open("dsm_10m.json", "w"))
