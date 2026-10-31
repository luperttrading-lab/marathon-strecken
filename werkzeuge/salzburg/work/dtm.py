# Höhen alle 10 Linienmeter der Linie der Google-Karte (linie.json, beide Runden) aus dem Laser-Geländemodell des BEV (ALS DTM, 1 m,
# bev.py), bilinear; dazu das 25-%-Quantil des Oberflächenmodells (ALS DSM) im Umkreis von 2 m (Fahrbahn ohne Geländer, Laternen,
# Fahrzeuge) für Brücken und den Abgleich. Die Linie ist eine aufgezeichnete Spur und liegt im Median 3 m, bis 9 m neben der
# Straßenmitte (strassen.py); am Salzachkai (Rudolfskai, Elisabethkai, Griesgasse) läge sie sonst auf der Böschung zum Fluss. Deshalb
# zusätzlich an der Straßenmitte (Fußpunkt auf dem OSM-Weg aus strassen.json, wo er höchstens 15 m entfernt ist). clean.py nimmt die
# Werte an der Straßenmitte. -> dtm_10m.json [[Linienmeter, lat, lon, DTM Spur, DSM Spur, DTM Mitte, DSM Mitte, lat Mitte, lon Mitte], …]
import json, time
import numpy as np
from pyproj import Transformer
import bev
T = Transformer.from_crs(4326, 3035, always_xy=True)
g = json.load(open("linie.json")); d = np.array(g["d"]); P = np.array(g["pts"])
st = json.load(open("strassen.json"))
ss = np.append(np.arange(0, d[-1], 10.0), d[-1]); assert len(ss) == len(st)
la = np.interp(ss, d, P[:, 0]); lo = np.interp(ss, d, P[:, 1]); X, Y = T.transform(lo, la)
def werte(x, y):
    h = bev.hoehe("DTM", x, y); v = bev.umkreis("DSM", x, y, 2.0)
    return (None if np.isnan(h) else round(h, 3)), (round(float(np.percentile(v, 25)), 3) if v else None)
t0 = time.time(); res = []
for i, (s, a, b, x, y) in enumerate(zip(ss, la, lo, X, Y)):
    h, ds = werte(x, y)
    q = st[i]
    if q[8] is not None and q[8] <= 15: ma, mo = q[9], q[10]
    else: ma, mo = float(a), float(b)
    xm, ym = T.transform(mo, ma); hm, dm = werte(xm, ym)
    res.append([float(s), float(a), float(b), h, ds, hm, dm, ma, mo])
    if i % 1000 == 0: print(i, len(ss), round(time.time() - t0), "s", flush=True)
json.dump(res, open("dtm_10m.json", "w"))
h = np.array([r[3] if r[3] is not None else np.nan for r in res]); hm = np.array([r[5] if r[5] is not None else np.nan for r in res])
print(len(res), "Punkte; ohne DTM:", int(np.isnan(h).sum()), int(np.isnan(hm).sum()), "; Spur min/max", np.nanmin(h).round(2), np.nanmax(h).round(2),
      "; Mitte min/max", np.nanmin(hm).round(2), np.nanmax(hm).round(2), "; Mitte minus Spur: Median", np.nanmedian(hm - h).round(2),
      "90 % der Beträge bis", np.nanpercentile(np.abs(hm - h), 90).round(2))
