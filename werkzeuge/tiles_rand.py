# Kartenstücke der Zoomstufen 11–13 neu bauen: bisherige Fläche plus ein Kachelrand entlang der ganzen Strecke.
# Grund: Ab Stufe 12 steht der Läufer in der Kartenmitte. Am Start, am Ziel und an Außenkurven reichte der halbe
# Kartenausschnitt (bis ~200 × 150 px) über den festen Rand des Rechtecks hinaus (z13: ~115 px), dort blieb die Karte grau.
# Stufe 11 trägt außerdem die Zwischenstufen zwischen Übersicht und Stufe 12 (Karte folgt dem Läufer, bis Faktor 2 verkleinert):
# dafür zwei Kacheln Rand. Stufen 14 und 15 haben schon einen Kachelrand entlang der Strecke (tiles.py) und bleiben.
# Aufruf aus werkzeuge/:  python3 tiles_rand.py <strecke> [Rand in Stufe 11, Kacheln; Standard 1, New York 2]
# Schreibt die Stücke nach ../<strecke>/, ersetzt D.tiles["11"…"13"] in ../<strecke>/index.html und die Kartenliste in ../<strecke>/sw.js.
import glob, json, math, os, re, sys, time, urllib.request, concurrent.futures as cf
import numpy as np
from PIL import Image
race = sys.argv[1]; RAND11 = int(sys.argv[2]) if len(sys.argv) > 2 else 1; APP = f"../{race}/"; CACHE = f"{race}/dl/tiles"; os.makedirs(CACHE, exist_ok=True)
R = json.load(open(f"{race}/work/route50.json"))
pts = [(R["lat0"] + a / 1e5, R["lon0"] + b / 1e5) for a, b in R["pts"]]
lats = [p[0] for p in pts]; lons = [p[1] for p in pts]
def px(lat, lon, z):
    n = 256 * 2 ** z
    return (lon + 180) / 360 * n, (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
def rechteck(z, dlat, dlon):
    x0, y1 = px(min(lats) - dlat, min(lons) - dlon, z); x1, y0 = px(max(lats) + dlat, max(lons) + dlon, z)
    return x0, y0, x1, y1
def kacheln(x0, y0, x1, y1):
    return {(x, y) for x in range(int(x0 // 256), int(x1 // 256) + 1) for y in range(int(y0 // 256), int(y1 // 256) + 1)}
def rand(z, k):
    s = set()
    for la, lo in pts:
        x, y = px(la, lo, z); tx, ty = int(x // 256), int(y // 256)
        s |= {(tx + dx, ty + dy) for dx in range(-k, k + 1) for dy in range(-k, k + 1)}
    return s
def flaeche_z11():   # wie tiles_z11.py: Übersicht für Kartengrößen 300–420 × 140–320 px
    z = 11; x0, y0, x1, y1 = rechteck(z, 0.03, 0.06)
    P = [px(a, b, z) for a, b in pts]; rx0, rx1 = min(p[0] for p in P), max(p[0] for p in P); ry0, ry1 = min(p[1] for p in P), max(p[1] for p in P)
    for w in (300, 340, 390, 420):
        for h in (140, 230, 320):
            sc = min((w - 70) / (rx1 - rx0), (h - 28) / (ry1 - ry0)); cx, cy = (rx0 + rx1) / 2, (ry0 + ry1) / 2; mx = (w - 42) / 2
            x0 = min(x0, cx - (mx + 16) / sc); x1 = max(x1, cx + (w - mx + 16) / sc); y0 = min(y0, cy - (h / 2 + 16) / sc); y1 = max(y1, cy + (h / 2 + 16) / sc)
    return kacheln(x0, y0, x1, y1)
STUFEN = {11: flaeche_z11() | rand(11, RAND11), 12: kacheln(*rechteck(12, 0.012, 0.02)) | rand(12, 1), 13: kacheln(*rechteck(13, 0.012, 0.02)) | rand(13, 1)}
def fetch(a):
    z, x, y = a; f = f"{CACHE}/osm_{z}_{x}_{y}.png"
    if os.path.exists(f) and os.path.getsize(f) > 100: return f
    req = urllib.request.Request(f"https://tile.openstreetmap.org/{z}/{x}/{y}.png", headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial, one-time download)"})
    for att in range(4):
        try: open(f, "wb").write(urllib.request.urlopen(req, timeout=30).read()); time.sleep(0.15); return f
        except Exception: time.sleep(2 + 3 * att)
    return None
def dark(im):   # gleiche Umfärbung wie tiles.py
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
CH = 1024; meta = {}
for z, ts in STUFEN.items():
    with cf.ThreadPoolExecutor(2) as ex: res = list(ex.map(fetch, [(z, x, y) for x, y in sorted(ts)]))
    missing = sum(r is None for r in res)
    xs = [t[0] for t in ts]; ys = [t[1] for t in ts]; tx0, ty0, tx1, ty1 = min(xs), min(ys), max(xs), max(ys)
    W, H = (tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256
    base = Image.new("RGB", (W, H), (242, 239, 233)); have = np.zeros((ty1 - ty0 + 1, tx1 - tx0 + 1), bool)
    for (x, y) in ts:
        f = f"{CACHE}/osm_{z}_{x}_{y}.png"
        if os.path.exists(f): base.paste(Image.open(f).convert("RGB"), ((x - tx0) * 256, (y - ty0) * 256)); have[y - ty0, x - tx0] = True
    for alt in glob.glob(f"{APP}karte-*-z{z}-*.jpg"): os.remove(alt)
    chunks = []
    for cy in range(0, H, CH):
        for cx in range(0, W, CH):
            if not have[cy // 256:(cy + CH) // 256, cx // 256:(cx + CH) // 256].any(): continue
            box = (cx, cy, min(cx + CH, W), min(cy + CH, H)); crop = base.crop(box)
            for theme, fn in (("dunkel", dark), ("hell", light)):
                fn(crop).save(f"{APP}karte-{theme}-z{z}-{cx // CH}-{cy // CH}.jpg", "JPEG", quality=76, optimize=True)
            chunks.append([cx, cy, box[2] - cx, box[3] - cy, f"z{z}-{cx // CH}-{cy // CH}"])
    meta[str(z)] = {"x0": tx0 * 256, "y0": ty0 * 256, "chunks": chunks}
    print(race, "z", z, len(ts), "Kacheln, fehlend", missing, "Stücke", len(chunks), flush=True)
# Daten der App: nur D.tiles["11"…"13"] ersetzen, sonst bleibt D byte-gleich
s = open(f"{APP}index.html", encoding="utf-8").read()
m = re.search(r"const D = (\{.*?\});\n", s, re.S); raw = m.group(1); D = json.loads(raw)
assert json.dumps(D, ensure_ascii=False, separators=(",", ":")) == raw, "D lässt sich nicht byte-gleich neu schreiben"
D["tiles"].update(meta); neu = json.dumps(D, ensure_ascii=False, separators=(",", ":"))
open(f"{APP}index.html", "w", encoding="utf-8").write(s[:m.start(1)] + neu + s[m.end(1):])
# Kartenliste des Service Workers aus den vorhandenen Dateien
w = open(f"{APP}sw.js").read()
liste = "[" + ", ".join(f'"./{os.path.basename(p)}"' for p in sorted(glob.glob(f"{APP}karte-*.jpg"))) + "]"
open(f"{APP}sw.js", "w").write(re.sub(r"const KARTE = \[.*?\];", "const KARTE = " + liste + ";", w, count=1, flags=re.S))
print(race, "fertig:", json.dumps({k: len(v["chunks"]) for k, v in D["tiles"].items()}))
