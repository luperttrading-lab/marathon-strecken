# Kartenstücke der Zoomstufe 11 für die Übersicht (ganze Strecke im Bild), gleiche Umfärbung wie tiles.py.
# Aufruf aus werkzeuge/:  python3 tiles_z11.py <strecke>   (liest <strecke>/work/route50.json, schreibt nach ../<strecke>/)
import json, math, os, sys, time, urllib.request
import numpy as np
from PIL import Image
race = sys.argv[1]; APP = f"../{race}/"; CACHE = f"{race}/dl/tiles"; os.makedirs(CACHE, exist_ok=True)
R = json.load(open(f"{race}/work/route50.json"))
pts = [(R["lat0"] + a / 1e5, R["lon0"] + b / 1e5) for a, b in R["pts"]]
lats = [p[0] for p in pts]; lons = [p[1] for p in pts]
bbox = (min(lats) - 0.03, max(lats) + 0.03, min(lons) - 0.06, max(lons) + 0.06)   # großzügig: die Übersicht zeigt mehr als die Strecke
def px(lat, lon, z):
    n = 256 * 2 ** z
    return (lon + 180) / 360 * n, (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
z = 11
x0, y1 = px(bbox[0], bbox[2], z); x1, y0 = px(bbox[1], bbox[3], z)
ts = [(x, y) for x in range(int(x0 // 256), int(x1 // 256) + 1) for y in range(int(y0 // 256), int(y1 // 256) + 1)]
def fetch(x, y):
    f = f"{CACHE}/osm_{z}_{x}_{y}.png"
    if os.path.exists(f) and os.path.getsize(f) > 100: return f
    req = urllib.request.Request(f"https://tile.openstreetmap.org/{z}/{x}/{y}.png", headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial, one-time download)"})
    for att in range(4):
        try: open(f, "wb").write(urllib.request.urlopen(req, timeout=30).read()); time.sleep(0.2); return f
        except Exception: time.sleep(2 + 3 * att)
    return None
def dark(im):
    a = 255 - np.asarray(im.convert("RGB")).astype(np.uint8)
    hsv = np.asarray(Image.fromarray(a).convert("HSV")).copy()
    hsv[..., 0] = (hsv[..., 0].astype(int) + 128) % 256
    hsv[..., 1] = (hsv[..., 1] * 0.55).astype(np.uint8)
    rgb = np.asarray(Image.fromarray(hsv, "HSV").convert("RGB")).astype(float)
    return Image.fromarray(np.clip(10 + rgb * 0.62, 0, 255).astype(np.uint8))
def light(im):
    rgb = np.asarray(im.convert("RGB")).astype(float); g = rgb.mean(axis=2, keepdims=True)
    rgb = g + (rgb - g) * 0.45; rgb = 255 - (255 - rgb) * 0.85
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
xs = [t[0] for t in ts]; ys = [t[1] for t in ts]; tx0, ty0 = min(xs), min(ys)
W, H = (max(xs) - tx0 + 1) * 256, (max(ys) - ty0 + 1) * 256
base = Image.new("RGB", (W, H), (242, 239, 233)); missing = 0
for x, y in ts:
    f = fetch(x, y)
    if f: base.paste(Image.open(f).convert("RGB"), ((x - tx0) * 256, (y - ty0) * 256))
    else: missing += 1
chunks = []
for cy in range(0, H, 1024):
    for cx in range(0, W, 1024):
        box = (cx, cy, min(cx + 1024, W), min(cy + 1024, H)); crop = base.crop(box)
        for theme, fn in (("dunkel", dark), ("hell", light)):
            fn(crop).save(f"{APP}karte-{theme}-z{z}-{cx // 1024}-{cy // 1024}.jpg", "JPEG", quality=76, optimize=True)
        chunks.append([cx, cy, box[2] - cx, box[3] - cy, f"z{z}-{cx // 1024}-{cy // 1024}"])
meta = {"x0": tx0 * 256, "y0": ty0 * 256, "chunks": chunks}
json.dump(meta, open(f"{race}/work/tilemeta_z11.json", "w"))
print(race, len(ts), "Kacheln, fehlend", missing, "Stücke", len(chunks), json.dumps(meta))
