# Höhen alle 10 m (GPX-Meter) aus dem DGM1 Sachsen (1-m-Laserscan, GeoSN, CC BY 4.0): 2-km-Kacheln als ZIP mit GeoTIFF
# (ETRS89/UTM33) aus der GeoCloud des Landesamts, wie sie die Seite „Batch Download“ auf geodaten.sachsen.de baut:
# .../public.php/dav/files/JCcXyifaNdLDnxZ/dgm1_33<E km gerade>_<N km gerade>_2_sn_tiff.zip. Je Kachel 13 MB: laden,
# ablesen, nicht aufheben (nur die abgelesenen Werte bleiben).
import io, json, time, urllib.request, zipfile, concurrent.futures as cf
import numpy as np
from PIL import Image
from pyproj import Transformer
src, out, step = "gpx2026.json", "dgm2026_10m.json", 10.0
g = json.load(open(src)); pts, d = g["pts"], g["d"]
dd = np.array(d); ss = np.append(np.arange(0, d[-1], step), d[-1])
la = np.interp(ss, dd, [p[0] for p in pts]); lo = np.interp(ss, dd, [p[1] for p in pts])
E, N = map(np.asarray, Transformer.from_crs(4326, 25833, always_xy=True).transform(lo, la))
# Die GPX (komoot, ein Punkt je ~50 m) kürzt Kurven ab; an den Hangstraßen bei Pötzscha misst das Modell dann den Hang
# daneben (±5 m). Deshalb jeden Messpunkt auf den nächsten Weg aus OpenStreetMap legen (höchstens 40 m), wie in München.
from scipy.spatial import cKDTree
T = Transformer.from_crs(4326, 25833, always_xy=True); road = []
for w in json.load(open("../dl/osm_wege.json"))["elements"]:
    g_ = w.get("geometry")
    if not g_ or len(g_) < 2 or w.get("tags", {}).get("highway") in ("motorway", "motorway_link", "trunk", "trunk_link"): continue
    xe, yn = map(np.asarray, T.transform([q["lon"] for q in g_], [q["lat"] for q in g_])); m = np.c_[xe, yn]
    for a_, b_ in zip(m[:-1], m[1:]):
        n_ = max(1, int(np.hypot(*(b_ - a_)) / 2)); road.append(a_ + (b_ - a_) * np.linspace(0, 1, n_ + 1)[:-1, None])
road = np.vstack(road); dist, idx_ = cKDTree(road).query(np.c_[E, N]); ok = dist < 40
E = np.where(ok, road[idx_, 0], E); N = np.where(ok, road[idx_, 1], N)
print(f"auf Wege gelegt: {ok.mean() * 100:.0f} %, Verschiebung Median {np.median(dist[ok]):.1f} m, 90 % {np.percentile(dist[ok], 90):.1f} m")
ke, kn = (np.floor(E / 2000) * 2).astype(int), (np.floor(N / 2000) * 2).astype(int)
H = np.full(len(ss), np.nan)
def kachel(t):
    e2, n2 = t; idx = np.where((ke == e2) & (kn == n2))[0]
    url = f"https://geocloud.landesvermessung.sachsen.de/public.php/dav/files/JCcXyifaNdLDnxZ/dgm1_33{e2}_{n2}_2_sn_tiff.zip"
    for att in range(5):
        try:
            z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "marathon-profile/1.0 (private use)"}), timeout=180).read()))
            A = np.array(Image.open(io.BytesIO(z.read([n for n in z.namelist() if n.endswith(".tif")][0]))), dtype=float); break
        except Exception:
            time.sleep(3 + 4 * att)
    else: return t, idx, None
    # Pixel (r, c) deckt E in [E0+c, E0+c+1), N in [N1-r-1, N1-r) mit E0 = e2 km, N1 = n2 km + 2 km; Mittelpunkte bei +0,5
    e0, n1 = e2 * 1000, (n2 + 2) * 1000
    c = E[idx] - e0 - 0.5; r = (n1 - 0.5) - N[idx]
    c0 = np.clip(np.floor(c).astype(int), 0, 1998); r0 = np.clip(np.floor(r).astype(int), 0, 1998); fc, fr = c - c0, r - r0
    v = A[r0, c0] * (1 - fc) * (1 - fr) + A[r0, c0 + 1] * fc * (1 - fr) + A[r0 + 1, c0] * (1 - fc) * fr + A[r0 + 1, c0 + 1] * fc * fr
    return t, idx, v
tiles = sorted(set(zip(ke.tolist(), kn.tolist()))); t0 = time.time()
with cf.ThreadPoolExecutor(3) as ex:
    for t, idx, v in ex.map(kachel, tiles):
        if v is not None: H[idx] = v
print(len(tiles), "Kacheln in", round(time.time() - t0), "s; fehlend:", int(np.isnan(H).sum()), "Punkte")
res = [[float(s), float(x), float(y), (None if np.isnan(h) else float(h))] for s, x, y, h in zip(ss, la, lo, H)]
hv = H[~np.isnan(H)]; print(len(res), "Punkte; Höhe min/max", round(hv.min(), 1), round(hv.max(), 1), "; ungültig (<0):", int((hv < 0).sum()))
json.dump(res, open(out, "w"))
