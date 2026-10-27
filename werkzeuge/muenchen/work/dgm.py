# Höhen alle 10 m (GPX-Meter) aus dem DGM1 Bayern (1-m-Laserscan, Open Data der Bayerischen Vermessungsverwaltung, CC BY 4.0):
# 1-km-Kacheln als GeoTIFF von download1.bayernwolke.de/a/dgm/dgm1/<E km>_<N km>.tif (ETRS89/UTM32), bilinear abgelesen.
import io, json, os, time, urllib.request, concurrent.futures as cf
import numpy as np
from PIL import Image
from pyproj import Transformer
src, out, step, CACHE = "gpx2026.json", "dgm2026_10m.json", 10.0, "../dl/dgm"
os.makedirs(CACHE, exist_ok=True)
g = json.load(open(src)); pts, d = g["pts"], g["d"]
dd = np.array(d); ss = np.append(np.arange(0, d[-1], step), d[-1])
la = np.interp(ss, dd, [p[0] for p in pts]); lo = np.interp(ss, dd, [p[1] for p in pts])
E, N = map(np.asarray, Transformer.from_crs(4326, 25832, always_xy=True).transform(lo, la))
# Die Linie liegt örtlich bis ~20 m neben dem Weg (gezeichnete Linie, Gegenverkehr nebeneinander). Am Olympiaberg misst
# das Modell dann den Hang (+20 m). Deshalb jeden Messpunkt auf den nächsten Weg aus OpenStreetMap legen (höchstens 40 m).
from scipy.spatial import cKDTree
T = Transformer.from_crs(4326, 25832, always_xy=True); road = []
for w in json.load(open("../dl/osm_wege.json"))["elements"]:
    g_ = w.get("geometry")
    if not g_ or len(g_) < 2 or w.get("tags", {}).get("highway") in ("motorway", "motorway_link", "trunk", "trunk_link"): continue
    xe, yn = map(np.asarray, T.transform([q["lon"] for q in g_], [q["lat"] for q in g_])); m = np.c_[xe, yn]
    for a_, b_ in zip(m[:-1], m[1:]):
        n_ = max(1, int(np.hypot(*(b_ - a_)) / 2)); road.append(a_ + (b_ - a_) * np.linspace(0, 1, n_ + 1)[:-1, None])
road = np.vstack(road); dist, idx = cKDTree(road).query(np.c_[E, N]); ok = dist < 40
E = np.where(ok, road[idx, 0], E); N = np.where(ok, road[idx, 1], N)
print(f"auf Wege gelegt: {ok.mean() * 100:.0f} %, Verschiebung Median {np.median(dist[ok]):.1f} m, 90 % {np.percentile(dist[ok], 90):.1f} m")
need = sorted({(int(e // 1000), int(n // 1000)) for e, n in zip(E, N)} | {(int((e + dx) // 1000), int((n + dy) // 1000)) for e, n in zip(E, N) for dx in (-2, 2) for dy in (-2, 2)})
def lade(t):
    f = f"{CACHE}/{t[0]}_{t[1]}.tif"
    if not (os.path.exists(f) and os.path.getsize(f) > 1000):
        for att in range(5):
            try:
                raw = urllib.request.urlopen(urllib.request.Request(f"https://download1.bayernwolke.de/a/dgm/dgm1/{t[0]}_{t[1]}.tif", headers={"User-Agent": "marathon-profile/1.0 (private use)"}), timeout=120).read()
                open(f, "wb").write(raw); break
            except Exception:
                time.sleep(2 + 3 * att)
    return t
t0 = time.time()
with cf.ThreadPoolExecutor(4) as ex: list(ex.map(lade, need))
print(len(need), "Kacheln geladen in", round(time.time() - t0), "s")
K = {}
def kachel(t):
    if t not in K: K[t] = np.array(Image.open(f"{CACHE}/{t[0]}_{t[1]}.tif"), dtype=float)
    return K[t]
def h(e, n):   # Pixel (r, c) deckt E in [E0+c, E0+c+1), N in [N1-r-1, N1-r); Mittelpunkte bei +0,5
    vals = []
    for de, dn in ((0, 0), (1, 0), (0, 1), (1, 1)):
        ee, nn = np.floor(e - 0.5) + de + 0.5, np.floor(n - 0.5) + dn + 0.5
        t = (int(ee // 1000), int(nn // 1000)); A = kachel(t)
        c, r = int(ee - t[0] * 1000), int((t[1] + 1) * 1000 - nn)
        vals.append(A[r, c])
    fe, fn = (e - 0.5) - np.floor(e - 0.5), (n - 0.5) - np.floor(n - 0.5)
    return vals[0] * (1 - fe) * (1 - fn) + vals[1] * fe * (1 - fn) + vals[2] * (1 - fe) * fn + vals[3] * fe * fn
H = [float(h(e, n)) for e, n in zip(E, N)]
res = [[float(s), float(x), float(y), v] for s, x, y, v in zip(ss, la, lo, H)]
print(len(res), "Punkte; Höhe min/max", round(min(H), 1), round(max(H), 1), "; ungültig:", sum(v < 0 for v in H))
json.dump(res, open(out, "w"))
