import json, math, os, time, urllib.request, concurrent.futures as cf
import numpy as np
from PIL import Image
OUT = "../dl/tiles"
os.makedirs(OUT, exist_ok=True)
ASSETS = "../assets"
R = json.load(open("route50.json"))
pts = [(R["lat0"] + a / 1e5, R["lon0"] + b / 1e5) for a, b in R["pts"]]
def px(lat, lon, z):
    n = 256 * 2 ** z
    return (lon + 180) / 360 * n, (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
lats = [p[0] for p in pts]; lons = [p[1] for p in pts]
bbox = (min(lats) - 0.012, max(lats) + 0.012, min(lons) - 0.02, max(lons) + 0.02)
def tiles_for(z, corridor):
    if not corridor:
        x0, y1 = px(bbox[0], bbox[2], z); x1, y0 = px(bbox[1], bbox[3], z)
        return {(x, y) for x in range(int(x0 // 256), int(x1 // 256) + 1) for y in range(int(y0 // 256), int(y1 // 256) + 1)}
    s = set()
    for la, lo in pts:
        x, y = px(la, lo, z); tx, ty = int(x // 256), int(y // 256)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1): s.add((tx + dx, ty + dy))
    return s
def fetch(args):
    z, x, y = args
    f = f"{OUT}/osm_{z}_{x}_{y}.png"
    if os.path.exists(f) and os.path.getsize(f) > 100: return f
    url = f"https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    for att in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial, one-time download)"})
            open(f, "wb").write(urllib.request.urlopen(req, timeout=30).read()); time.sleep(0.15); return f
        except Exception:
            time.sleep(2 + 3 * att)
    return None
def dark(im):
    a = 255 - np.asarray(im.convert("RGB")).astype(np.uint8)        # Helligkeit umkehren
    hsv = np.asarray(Image.fromarray(a).convert("HSV")).copy()
    hsv[..., 0] = (hsv[..., 0].astype(int) + 128) % 256              # Farbton zurückdrehen: Wasser bleibt blau, Grün bleibt grün
    hsv[..., 1] = (hsv[..., 1] * 0.55).astype(np.uint8)              # ruhiger
    rgb = np.asarray(Image.fromarray(hsv, "HSV").convert("RGB")).astype(float)
    rgb = 10 + rgb * 0.62                                             # dunkler, weniger Kontrast
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
def light(im):
    rgb = np.asarray(im.convert("RGB")).astype(float)
    g = rgb.mean(axis=2, keepdims=True)
    rgb = g + (rgb - g) * 0.45                                        # entsättigt
    rgb = 255 - (255 - rgb) * 0.85                                    # etwas heller
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
meta = {}
CH = 1024
for z, corridor in ((12, False), (13, False), (14, True), (15, True)):   # z14 nur entlang der Strecke
    ts = tiles_for(z, corridor)
    with cf.ThreadPoolExecutor(2) as ex:
        res = list(ex.map(fetch, [(z, x, y) for x, y in sorted(ts)]))
    missing = sum(r is None for r in res)
    xs = [t[0] for t in ts]; ys = [t[1] for t in ts]; tx0, ty0, tx1, ty1 = min(xs), min(ys), max(xs), max(ys)
    W, H = (tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256
    base = Image.new("RGB", (W, H), (242, 239, 233)); have = np.zeros(((ty1 - ty0 + 1), (tx1 - tx0 + 1)), bool)
    for (x, y) in ts:
        f = f"{OUT}/osm_{z}_{x}_{y}.png"
        if os.path.exists(f):
            base.paste(Image.open(f).convert("RGB"), ((x - tx0) * 256, (y - ty0) * 256)); have[y - ty0, x - tx0] = True
    chunks = []
    for cy in range(0, H, CH):
        for cx in range(0, W, CH):
            sub = have[cy // 256:(cy + CH) // 256, cx // 256:(cx + CH) // 256]
            if not sub.any(): continue
            box = (cx, cy, min(cx + CH, W), min(cy + CH, H)); crop = base.crop(box)
            for theme, fn in (("dunkel", dark),):   # seit 1.35 nur dunkel
                fn(crop).save(f"{ASSETS}/karte-{theme}-z{z}-{cx // CH}-{cy // CH}.jpg", "JPEG", quality=76, optimize=True)
            chunks.append([cx, cy, box[2] - cx, box[3] - cy, f"z{z}-{cx // CH}-{cy // CH}"])
    meta[z] = {"x0": tx0 * 256, "y0": ty0 * 256, "chunks": chunks}
    print(z, len(ts), "Kacheln, fehlend", missing, "Stücke", len(chunks))
json.dump(meta, open("tilemeta.json", "w"))
