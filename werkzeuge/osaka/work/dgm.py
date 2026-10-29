# Bodenhöhen alle 10 m (Linienmeter) aus dem Höhenmodell der GSI (国土地理院, 地理院タイル): DEM5A (Laser, 5 m), wo es fehlt
# DEM5B (Bildkorrelation), sonst DEM10B. PNG-Kacheln, Höhe = (R·65536 + G·256 + B) · 0,01 m (über 2^23: minus 2^24, genau 2^23:
# keine Daten), bilinear. Höhen über T.P. (Tokyo Peil, Bezugsniveau für ganz Japan). Quelle: 国土地理院, Nutzung mit Quellenangabe. -> dgm2026_10m.json
import json, math, os, time, urllib.request
import numpy as np
from PIL import Image
CACHE = "../dl/dem"; os.makedirs(CACHE, exist_ok=True)
g = json.load(open("gpx2026.json")); pts, d = g["pts"], np.array(g["d"])
la_ = np.array([p[0] for p in pts]); lo_ = np.array([p[1] for p in pts])
ss = np.append(np.arange(0, d[-1], 10.0), d[-1]); la = np.interp(ss, d, la_); lo = np.interp(ss, d, lo_)
QUELLEN = [("dem5a_png", 15), ("dem5b_png", 15), ("dem_png", 14)]
_kacheln = {}
def kachel(name, z, x, y):
    k = (name, z, x, y)
    if k in _kacheln: return _kacheln[k]
    f = f"{CACHE}/{name}_{z}_{x}_{y}.png"
    if not os.path.exists(f):
        for att in range(4):
            try:
                req = urllib.request.Request(f"https://cyberjapandata.gsi.go.jp/xyz/{name}/{z}/{x}/{y}.png", headers={"User-Agent": "marathon-profile-check/1.0"})
                data = urllib.request.urlopen(req, timeout=30).read(); open(f, "wb").write(data); break
            except urllib.error.HTTPError as e:
                if e.code == 404: open(f, "wb").write(b""); break
                time.sleep(2 + 3 * att)
            except Exception: time.sleep(2 + 3 * att)
    if not os.path.exists(f) or os.path.getsize(f) == 0: _kacheln[k] = None; return None
    a = np.asarray(Image.open(f).convert("RGB")).astype(np.int64); v = a[..., 0] * 65536 + a[..., 1] * 256 + a[..., 2]
    h = np.where(v < 2 ** 23, v * 0.01, (v - 2 ** 24) * 0.01).astype(float); h[v == 2 ** 23] = np.nan
    _kacheln[k] = h; return h
def wert(name, z, px, py):
    x, y = int(px // 256), int(py // 256); t = kachel(name, z, x, y)
    if t is None: return np.nan
    return t[int(py) % 256, int(px) % 256]
def hoehe(la1, lo1):
    for name, z in QUELLEN:
        n = 256 * 2 ** z; px = (lo1 + 180) / 360 * n - 0.5; py = (1 - math.log(math.tan(math.radians(la1)) + 1 / math.cos(math.radians(la1))) / math.pi) / 2 * n - 0.5
        x0, y0 = math.floor(px), math.floor(py); fx, fy = px - x0, py - y0
        v = [wert(name, z, x0 + dx, y0 + dy) for dy in (0, 1) for dx in (0, 1)]
        if not any(np.isnan(v)):
            return v[0] * (1 - fx) * (1 - fy) + v[1] * fx * (1 - fy) + v[2] * (1 - fx) * fy + v[3] * fx * fy, name
    return None, None
t0 = time.time(); res, quelle = [], {}
for s, a, b in zip(ss, la, lo):
    h, q = hoehe(a, b); quelle[q] = quelle.get(q, 0) + 1; res.append([float(s), float(a), float(b), h])
print(len(res), "Punkte in", round(time.time() - t0), "s; Quellen:", quelle)
hv = [r[3] for r in res if r[3] is not None]; print("Höhe min/max", round(min(hv), 1), round(max(hv), 1))
json.dump(res, open("dgm2026_10m.json", "w"))
