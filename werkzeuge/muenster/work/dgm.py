# Höhen alle 10 m (Linienmeter) aus dem DGM1 NRW (1-m-Laserscan) über den WCS von Geobasis NRW (Achsen x/y). Kopie von werkzeuge/duesseldorf/work/dgm.py.
# Statt einer Abfrage je Punkt: je ~250 m Strecke ein GeoTIFF-Ausschnitt (EPSG:25832), dann bilinear abgelesen.
# Anders als in Düsseldorf wird nicht auf der gezeichneten Linie gemessen, sondern auf dem OSM-Weg darunter (strassen.py, Lotfußpunkt):
# Die Linie liegt bis 18 m neben der Fahrbahn (in der Aegidiistraße drei Linien nebeneinander), auf dem Land sonst auf Gräben und Böschungen.
# Ohne Weg (Unterführungen) gilt der Punkt der Linie. Spalten 1–2 bleiben die Lage auf der Linie (für Karte und Route).
import io, json, sys, time, urllib.request, concurrent.futures as cf
import numpy as np
from PIL import Image
from pyproj import Transformer
src, out, step = "strecke2026.json", "dgm2026_10m.json", 10.0
g = json.load(open(src)); pts, d = g["pts"], g["d"]
dd = np.array(d); la_ = np.array([p[0] for p in pts]); lo_ = np.array([p[1] for p in pts])
ss = np.append(np.arange(0, d[-1], step), d[-1])
la = np.interp(ss, dd, la_); lo = np.interp(ss, dd, lo_)
T = Transformer.from_crs(4326, 25832, always_xy=True)
E, N = T.transform(lo, la)
E, N = np.asarray(E, float).copy(), np.asarray(N, float).copy()
st = json.load(open("strassen.json")); o = json.load(open("../dl/osm_netz.json")); NO = o["nodes"]; WEG = {}
def weg(wid):
    if wid not in WEG:
        pts = [NO[str(q)] for q in o["ways"][wid][1] if str(q) in NO]
        x, y = T.transform([p[1] for p in pts], [p[0] for p in pts]); WEG[wid] = np.c_[x, y]
    return WEG[wid]
versatz = []
for i in range(len(ss)):
    wid = st[min(len(st) - 1, i)][7]
    if not wid: continue
    A = weg(wid); p = np.array([E[i], N[i]]); a = A[:-1]; b = A[1:]; v = b - a
    t = np.clip(((p - a) * v).sum(1) / np.maximum((v * v).sum(1), 1e-9), 0, 1); q = a + t[:, None] * v; dq = np.hypot(*(q - p).T); j = dq.argmin()
    E[i], N[i] = q[j]; versatz.append(dq[j])
print(f"auf den OSM-Weg gelegt: {len(versatz)} von {len(ss)} Punkten, Versatz Median {np.median(versatz):.1f} m, 90 % {np.percentile(versatz, 90):.1f} m")
# Gruppen aufeinanderfolgender Punkte mit höchstens 250 m Ausdehnung
groups, a = [], 0
for i in range(1, len(ss) + 1):
    if i == len(ss) or max(E[a:i+1].max() - E[a:i+1].min(), N[a:i+1].max() - N[a:i+1].min()) > 250:
        groups.append((a, i)); a = i
URL = "https://www.wcs.nrw.de/geobasis/wcs_nw_dgm?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&COVERAGEID=nw_dgm&FORMAT=image/tiff"
def fetch(gr):
    a, b = gr
    e0, e1 = int(np.floor(E[a:b].min())) - 3, int(np.ceil(E[a:b].max())) + 4
    n0, n1 = int(np.floor(N[a:b].min())) - 3, int(np.ceil(N[a:b].max())) + 4
    url = URL + f"&SUBSET=x({e0},{e1})&SUBSET=y({n0},{n1})"
    for att in range(5):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "marathon-profile-check/1.0 (private use)"}), timeout=60).read()
            A = np.array(Image.open(io.BytesIO(raw)), dtype=float)
            # Zeile r deckt N in [n1-1-r, n1-r), Spalte c deckt E in [e0+c, e0+c+1); Mittelpunkte bei +0,5
            c = E[a:b] - e0 - 0.5; r = (n1 - 0.5) - N[a:b]
            c0 = np.clip(np.floor(c).astype(int), 0, A.shape[1] - 2); r0 = np.clip(np.floor(r).astype(int), 0, A.shape[0] - 2)
            fc, fr = c - c0, r - r0
            v = (A[r0, c0] * (1 - fc) * (1 - fr) + A[r0, c0 + 1] * fc * (1 - fr) + A[r0 + 1, c0] * (1 - fc) * fr + A[r0 + 1, c0 + 1] * fc * fr)
            return a, v.tolist()
        except Exception as ex:
            time.sleep(2 + 3 * att)
    return a, [None] * (b - a)
t0 = time.time(); H = [None] * len(ss)
with cf.ThreadPoolExecutor(4) as ex:
    for a, v in ex.map(fetch, groups): H[a:a + len(v)] = v
res = [[float(s), float(x), float(y), h] for s, x, y, h in zip(ss, la, lo, H)]
print(len(res), "Punkte in", len(groups), "Ausschnitten,", round(time.time() - t0), "s; fehlend:", sum(r[3] is None for r in res))
hv = [r[3] for r in res if r[3] is not None]; print("Höhe min/max", round(min(hv), 1), round(max(hv), 1))
json.dump(res, open(out, "w"))
