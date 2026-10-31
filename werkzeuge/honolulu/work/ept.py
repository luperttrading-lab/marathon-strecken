# Punkte der USGS-Punktwolke HI_NOAAMauiOahu_2_B20 (NOAA-Laserscan Maui/Oʻahu, QL1, 2023; EPT auf AWS usgs-lidar-public, EPSG:3857) in
# einem Rechteck holen, alle Ebenen bis zur vollen Dichte. Kopie von werkzeuge/boston/work/ept.py; Kacheln werden in ../dl/ept/ zwischengespeichert.
import io, json, math, urllib.request, functools
import numpy as np, laspy
BASE = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/HI_NOAAMauiOahu_2_B20/"
def get(url):
    import time, os, hashlib
    os.makedirs("../dl/ept", exist_ok=True); f = "../dl/ept/" + hashlib.md5(url.encode()).hexdigest()
    if os.path.exists(f): return open(f, "rb").read()
    for att in range(6):
        try:
            d = urllib.request.urlopen(url, timeout=60).read(); open(f, "wb").write(d); return d
        except Exception:
            if att == 5: raise
            time.sleep(1 + 2 * att)
E = json.loads(get(BASE + "ept.json"))
B = E["bounds"]
@functools.lru_cache(4000)
def node(key):
    las = laspy.read(io.BytesIO(get(BASE + f"ept-data/{key}.laz")))
    return np.c_[np.asarray(las.x), np.asarray(las.y), np.asarray(las.z), np.asarray(las.classification)].astype(np.float64)
@functools.lru_cache(None)
def hier(key): return json.loads(get(BASE + f"ept-hierarchy/{key}.json"))
def node_bounds(d, x, y, z):
    s = (B[3] - B[0]) / 2 ** d
    return B[0] + x * s, B[1] + y * s, B[0] + (x + 1) * s, B[1] + (y + 1) * s
def query(x0, y0, x1, y1, maxdepth=30):
    out = []; H = hier("0-0-0-0")
    def walk(d, x, y, z, H):
        key = f"{d}-{x}-{y}-{z}"
        if key not in H: return
        n = H[key]
        if n == -1: H = hier(key); n = H[key]
        bx0, by0, bx1, by1 = node_bounds(d, x, y, z)
        if bx1 < x0 or bx0 > x1 or by1 < y0 or by0 > y1: return
        if n > 0:
            A = node(key); m = (A[:, 0] >= x0) & (A[:, 0] <= x1) & (A[:, 1] >= y0) & (A[:, 1] <= y1)
            if m.any(): out.append(A[m])
        if d < maxdepth:
            for dx in (0, 1):
                for dy in (0, 1):
                    for dz in (0, 1): walk(d + 1, 2 * x + dx, 2 * y + dy, 2 * z + dz, H)
    walk(0, 0, 0, 0, H)
    return np.vstack(out) if out else np.zeros((0, 4))
def merc(lat, lon):
    return math.radians(lon) * 6378137.0, math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)) * 6378137.0
