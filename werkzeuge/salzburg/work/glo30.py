# Nur Abgleich: Copernicus DEM GLO-30 (Oberflächenmodell, 1 Bogensekunde, © DLR/Airbus, ESA; offen über AWS Open Data) an einigen
# Stellen der Strecke, um den Höhenbereich des BEV-Lasermodells (417–438 m) gegen den „9 m“ des Veranstalters zu prüfen.
# Liest über HTTP-Range nur die nötigen Teilkacheln (httpfile.py). Ausgabe nur auf dem Bildschirm.
import json, urllib.request, numpy as np, tifffile
from httpfile import HttpFile
URL = "https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_N47_00_E013_00_DEM/Copernicus_DSM_COG_10_N47_00_E013_00_DEM.tif"
n = int(urllib.request.urlopen(urllib.request.Request(URL, method="HEAD"), timeout=60).headers["Content-Length"])
tf = tifffile.TiffFile(HttpFile(URL, n)); p = tf.pages[0]
x0, y0 = p.tags["ModelTiepointTag"].value[3:5]; sx, sy = p.tags["ModelPixelScaleTag"].value[:2]
tw, tl = p.tilewidth, p.tilelength; ntx = -(-p.shape[1] // tw); kach = {}
def wert(lat, lon):
    c = int((lon - x0) / sx); r = int((y0 - lat) / sy); i, j = c // tw, r // tl
    if (i, j) not in kach:
        idx = j * ntx + i; tf.filehandle.seek(p.dataoffsets[idx]); kach[(i, j)] = p.decode(tf.filehandle.read(p.databytecounts[idx]), idx)[0].reshape(tl, tw)
    return float(kach[(i, j)][r % tl, c % tw])
d = json.load(open("data.json")); R = json.load(open("route50.json")); h = np.array(d["h"]) / 100
for km in (0.5, 3, 5, 7.7, 9, 12, 14, 16, 18.5, 19.5, 21, 23):
    la, lo = R["lat0"] + R["pts"][int(km * 20)][0] / 1e5, R["lon0"] + R["pts"][int(km * 20)][1] / 1e5
    print(f"km {km:5.1f}: BEV {h[int(km * 100)]:6.1f}  GLO-30 {wert(la, lo):6.1f}")
