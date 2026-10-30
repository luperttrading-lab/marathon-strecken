# Kartenstücke für die App -> ../assets/karte-dunkel-z{11..15}-*.jpg und tilemeta.json (alle Stufen, D.tiles).
# Aufruf aus work/:  python3 tiles.py [relief|sat|osm] [probe]
#   relief  dunkles Relief aus Copernicus GLO-30 (Kacheln N40E117 und N39E117, Schummerung) mit Linien aus OSM: Flüsse, Straßen, Wege, Mauer, Türme; Dörfer mit
#           den Namen der Karte des Veranstalters (Pinyin), sonst OSM (name:en ohne „cun“). Gewählt (siehe UEBERGABE.md).
#   sat     Sentinel-2 cloudless 2016 von EOX (s2cloudless_3857, CC BY 4.0), abgedunkelt und entsättigt
#   osm     die dunkle OSM-Karte wie in den anderen Strecken (tile.openstreetmap.org, umgefärbt)
#   probe   nur Probebilder nach ../dl/proben/ (z13 ganze Strecke, z15 Mauer und Festung, z15 Dörfer am Anfang), keine App-Dateien
# Kachelflächen wie in den anderen Strecken: z12/z13 Rechteck um die Strecke (±0,012° / ±0,02°) plus ein Kachelrand entlang der
# Strecke, z14/z15 nur entlang der Strecke (±1 Kachel), z11 Übersicht wie tiles_z11.py plus zwei Kacheln Rand (tiles_rand.py
# <strecke> 2). tiles_z11.py und tiles_rand.py holen OSM-Kacheln und dürfen hier nicht laufen: sie würden das Relief überschreiben.
import json, math, os, sys, time, urllib.request, concurrent.futures as cf
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from geo import osm
from dgm import lade
VAR = sys.argv[1] if len(sys.argv) > 1 else "relief"; PROBE = "probe" in sys.argv
R = json.load(open("route50.json")); pts = [(R["lat0"] + a / 1e5, R["lon0"] + b / 1e5) for a, b in R["pts"]]
lats = [p[0] for p in pts]; lons = [p[1] for p in pts]
def px(lat, lon, z):
    n = 256 * 2 ** z
    return (lon + 180) / 360 * n, (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
def ll(X, Y, z):
    n = 256 * 2 ** z; lon = X / n * 360 - 180; lat = np.degrees(np.arctan(np.sinh(np.pi * (1 - 2 * Y / n)))); return lat, lon
def rechteck(z, dlat, dlon):
    x0, y1 = px(min(lats) - dlat, min(lons) - dlon, z); x1, y0 = px(max(lats) + dlat, max(lons) + dlon, z); return x0, y0, x1, y1
def kacheln(x0, y0, x1, y1): return {(x, y) for x in range(int(x0 // 256), int(x1 // 256) + 1) for y in range(int(y0 // 256), int(y1 // 256) + 1)}
def rand(z, k):
    s = set()
    for la, lo in pts:
        x, y = px(la, lo, z); tx, ty = int(x // 256), int(y // 256); s |= {(tx + dx, ty + dy) for dx in range(-k, k + 1) for dy in range(-k, k + 1)}
    return s
def flaeche_z11():
    z = 11; x0, y0, x1, y1 = rechteck(z, 0.03, 0.06)
    P = [px(a, b, z) for a, b in pts]; rx0, rx1 = min(p[0] for p in P), max(p[0] for p in P); ry0, ry1 = min(p[1] for p in P), max(p[1] for p in P)
    for w in (300, 340, 390, 420):
        for h in (140, 230, 320):
            sc = min((w - 70) / (rx1 - rx0), (h - 28) / (ry1 - ry0)); cx, cy = (rx0 + rx1) / 2, (ry0 + ry1) / 2; mx = (w - 42) / 2
            x0 = min(x0, cx - (mx + 16) / sc); x1 = max(x1, cx + (w - mx + 16) / sc); y0 = min(y0, cy - (h / 2 + 16) / sc); y1 = max(y1, cy + (h / 2 + 16) / sc)
    return kacheln(x0, y0, x1, y1)
STUFEN = {11: flaeche_z11() | rand(11, 2), 12: kacheln(*rechteck(12, 0.012, 0.02)) | rand(12, 1), 13: kacheln(*rechteck(13, 0.012, 0.02)) | rand(13, 1),
          14: rand(14, 1), 15: rand(15, 1)}
# ---------------------------------------------------------------- Kacheln aus dem Netz (osm, sat)
CACHE = "../dl/tiles"; os.makedirs(CACHE, exist_ok=True)
QUELLE = {"osm": ("https://tile.openstreetmap.org/{z}/{x}/{y}.png", "png"),
          "sat": ("https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless_3857/default/g/{z}/{y}/{x}.jpg", "jpg")}
def fetch(var, z, x, y):
    url, ext = QUELLE[var]; f = f"{CACHE}/{var}_{z}_{x}_{y}.{ext}"
    if os.path.exists(f) and os.path.getsize(f) > 100: return f
    req = urllib.request.Request(url.format(z=z, x=x, y=y), headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial, one-time download)"})
    for att in range(4):
        try: open(f, "wb").write(urllib.request.urlopen(req, timeout=30).read()); time.sleep(0.15); return f
        except Exception: time.sleep(2 + 3 * att)
    return None
def dark_osm(im):   # wie tiles.py der anderen Strecken
    a = 255 - np.asarray(im.convert("RGB")).astype(np.uint8)
    hsv = np.asarray(Image.fromarray(a).convert("HSV")).copy()
    hsv[..., 0] = (hsv[..., 0].astype(int) + 128) % 256; hsv[..., 1] = (hsv[..., 1] * 0.55).astype(np.uint8)
    rgb = np.asarray(Image.fromarray(hsv, "HSV").convert("RGB")).astype(float)
    return Image.fromarray(np.clip(10 + rgb * 0.62, 0, 255).astype(np.uint8))
def dark_sat(im):   # Satellitenbild: entsättigt und abgedunkelt, damit die farbige Strecke vorne liegt
    rgb = np.asarray(im.convert("RGB")).astype(float); g = rgb.mean(axis=2, keepdims=True)
    rgb = g + (rgb - g) * 0.6; rgb = 8 + rgb * 0.5
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
def mosaik_netz(var, z, ts, X0, Y0, W, H):
    with cf.ThreadPoolExecutor(2) as ex: list(ex.map(lambda t: fetch(var, z, *t), sorted(ts)))
    base = Image.new("RGB", (W, H), (242, 239, 233) if var == "osm" else (0, 0, 0))
    for (x, y) in ts:
        f = fetch(var, z, x, y)
        if f: base.paste(Image.open(f).convert("RGB"), (x * 256 - X0, y * 256 - Y0))
    return dark_osm(base) if var == "osm" else dark_sat(base)
# ---------------------------------------------------------------- Relief
DEM = None; OSMD = None
def dem():
    """Copernicus GLO-30, Kacheln N40E117 und N39E117 übereinander (die Übersicht z11 reicht bis 39,9° N)."""
    global DEM
    if DEM is None:
        a = lade("../dl/dem/cop30_N40_E117.tif"); b = lade("../dl/dem/cop30_N39_E117.tif")
        assert a[0].shape == b[0].shape and a[1:] == (b[1], b[2] + 1, b[3], b[4])
        DEM = (np.vstack([a[0], b[0]]),) + a[1:]
    return DEM
SPL = None
def hoehe_bei(lat, lon):
    """Höhe kubisch (Spline 3. Ordnung) aus dem 1″-Raster: bilinear gäbe in der Schummerung bei z14/z15 sichtbare Facetten."""
    global SPL
    from scipy import ndimage
    Z, lon0, lat0, sx, sy = dem()
    i0, i1 = int((lat0 - 40.62) / sy), int((lat0 - 39.86) / sy); j0, j1 = int((117.03 - lon0) / sx), int((117.99 - lon0) / sx)   # ganze Fläche von z11
    if SPL is None: SPL = ndimage.spline_filter(Z[i0:i1, j0:j1], order=3)
    fx = (lon - lon0) / sx - 0.5 - j0; fy = (lat0 - lat) / sy - 0.5 - i0
    return ndimage.map_coordinates(SPL, [fy.ravel(), fx.ravel()], order=3, prefilter=False, mode="nearest").reshape(np.shape(lat))
FONT = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"; FONT_B = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
KARTE_DOERFER = {"黄崖关村", "小平安村", "中营村", "下营村", "下营镇", "董家坟", "白滩村", "北车道峪村", "大平安村", "段庄村", "石炮沟村"}   # stehen schon über namen.doerfer()
BELEGT = []
def schrift(d, xy, text, font, col, SS, z, X0, Y0):
    """Ortsname neben den Ort setzen, wo er die Strecke am wenigsten verdeckt (Mitte, darüber, darunter, links, rechts)."""
    x, y = xy; l, t_, r, b = d.textbbox((0, 0), text, font=font, anchor="mm"); w, h = r - l, b - t_
    route = np.array([px(a, c, z) for a, c in pts]); route = (route - [X0, Y0]) * SS
    best = None
    for dx, dy in ((0, 0), (0, -h * 1.1), (0, h * 1.1), (-w * 0.6 - 6 * SS, 0), (w * 0.6 + 6 * SS, 0), (0, -h * 2.2), (0, h * 2.2)):
        cx, cy = x + dx, y + dy
        # Abstand der Strecke zum Schriftkasten
        ax = np.maximum(np.abs(route[:, 0] - cx) - w / 2, 0); ay = np.maximum(np.abs(route[:, 1] - cy) - h / 2, 0)
        frei = float(np.min(np.hypot(ax, ay))) if len(route) else 1e9
        kosten = -min(frei, 12 * SS) + 0.02 * math.hypot(dx, dy)
        if best is None or kosten < best[0]: best = (kosten, cx, cy)
    d.text((best[1], best[2]), text, font=font, fill=col, anchor="mm", stroke_width=int(2 * SS), stroke_fill=(14, 16, 20))
def mosaik_relief(z, X0, Y0, W, H):
    global OSMD
    if OSMD is None: OSMD = osm()
    N, Wy, NT = OSMD
    SS = 2 if z >= 14 else 1                                # Linien und Schrift doppelt fein zeichnen, dann verkleinern
    # Höhen an Pixelmitten
    Xs = X0 + np.arange(W) + 0.5; Ys = Y0 + np.arange(H) + 0.5
    lat, _ = ll(np.zeros(H), Ys, z); _, lon = ll(Xs, np.zeros(W), z)
    LA, LO = np.meshgrid(lat, lon, indexing="ij"); Zh = hoehe_bei(LA, LO)
    m = 156543.034 * math.cos(math.radians(float(np.mean(lat)))) / 2 ** z     # Meter je Pixel
    gy, gx = np.gradient(Zh, m)
    slope = np.arctan(np.hypot(gx, gy) * 1.6); aspect = np.arctan2(-gx, gy)
    az, alt = math.radians(315), math.radians(42)
    hs = np.clip(math.sin(alt) * np.cos(slope) + math.cos(alt) * np.sin(slope) * np.cos(az - aspect + math.pi / 2), 0, 1)
    # Grundfarbe: dunkles Blaugrau, Täler etwas dunkler als Grate (Höhe 180–700 m), Schummerung hellt auf
    t = np.clip((Zh - 180) / 520, 0, 1)
    base = np.stack([18 + 10 * t, 22 + 10 * t, 27 + 8 * t], -1)
    rgb = base + hs[..., None] * np.array([62, 66, 70]) * (0.55 + 0.45 * t[..., None])
    img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).resize((W * SS, H * SS), Image.BILINEAR)
    d = ImageDraw.Draw(img)
    def P(la_, lo_):
        x, y = px(la_, lo_, z); return ((x - X0) * SS, (y - Y0) * SS)
    k = SS * (1.0 if z <= 12 else 1.25 if z == 13 else 1.6 if z == 14 else 2.0)
    def zeichne(filt, col, w, dash=None):
        for tg, refs in Wy.values():
            if not filt(tg): continue
            q = [P(*N[r]) for r in refs if r in N]
            if len(q) > 1: d.line(q, fill=col, width=max(1, int(round(w * k))), joint="curve")
    # Wasser
    for tg, refs in Wy.values():
        if tg.get("natural") == "water" or tg.get("landuse") == "reservoir":
            q = [P(*N[r]) for r in refs if r in N]
            if len(q) > 2: d.polygon(q, fill=(28, 52, 78))
    zeichne(lambda t: t.get("waterway") in ("river",), (44, 84, 125), 2.2 if z >= 13 else 1.5)
    zeichne(lambda t: t.get("waterway") in ("stream",), (40, 72, 105), 1.0)
    # Straßen und Wege
    if z >= 13: zeichne(lambda t: t.get("highway") in ("track", "path", "footway"), (92, 92, 84), 0.8)
    if z >= 12: zeichne(lambda t: t.get("highway") in ("residential", "service", "unclassified", "living_street", "road"), (105, 108, 112), 1.0)
    zeichne(lambda t: t.get("highway") in ("tertiary", "tertiary_link", "secondary", "secondary_link"), (128, 131, 136), 1.5)
    zeichne(lambda t: t.get("highway") in ("trunk", "trunk_link", "primary", "primary_link"), (150, 152, 156), 2.0)
    zeichne(lambda t: t.get("highway") == "steps", (176, 150, 112), 1.2)
    # Große Mauer: ockerfarben mit dunklem Rand
    mauer = lambda t: t.get("historic") == "citywalls" or t.get("barrier") == "city_wall"
    zeichne(mauer, (40, 30, 20), 3.6 if z >= 13 else 2.6)
    zeichne(mauer, (196, 160, 104), 2.0 if z >= 13 else 1.4)
    if z >= 14:
        for kk, tg in NT.items():
            if tg.get("man_made") == "tower" and kk in N:
                x, y = P(*N[kk]); r = 2.2 * k
                d.rectangle([x - r, y - r, x + r, y + r], fill=(206, 172, 116), outline=(40, 30, 20), width=max(1, int(k / 1.5)))
    # Dörfer
    if z >= 12:
        f1 = ImageFont.truetype(FONT_B, int(round((11 if z <= 12 else 12 if z == 13 else 13) * SS)))
        f2 = ImageFont.truetype(FONT, int(round((10 if z <= 13 else 11) * SS)))
        from namen import doerfer
        from geo import wgs
        for nm, (hx, hy) in doerfer().items():          # Dörfer der Karte des Veranstalters an der Stelle ihrer Beschriftung
            hla, hlo = wgs(hx, hy); schrift(d, P(float(hla), float(hlo)), nm, f1, (226, 230, 236), SS, z, X0, Y0)
        for kk, tg in NT.items():                       # weitere Orte aus OSM (ohne „cun“ = Dorf)
            if tg.get("place") not in ("village", "town", "hamlet") or kk not in N or tg.get("name") in KARTE_DOERFER: continue
            if tg.get("place") == "hamlet" and z < 13: continue
            en = tg.get("name:en") or ""; nm = en[:-3] if en.endswith("cun") else en
            if nm: schrift(d, P(*N[kk]), nm, f2, (170, 176, 184), SS, z, X0, Y0)
    if SS > 1: img = img.resize((W, H), Image.LANCZOS)
    return img
# ---------------------------------------------------------------- Mosaik je Stufe, in Stücke zu 1024 px
def baue(var, z, ts, ziel, name_fn, nur=None):
    xs = [t[0] for t in ts]; ys = [t[1] for t in ts]; tx0, ty0, tx1, ty1 = min(xs), min(ys), max(xs), max(ys)
    X0, Y0 = tx0 * 256, ty0 * 256; W, H = (tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256
    if nur: (X0, Y0, W, H) = nur
    img = mosaik_relief(z, X0, Y0, W, H) if var == "relief" else mosaik_netz(var, z, ts, X0, Y0, W, H)
    if nur: return img
    have = np.zeros((ty1 - ty0 + 1, tx1 - tx0 + 1), bool)
    for (x, y) in ts: have[y - ty0, x - tx0] = True
    chunks = []
    for cy in range(0, H, 1024):
        for cx in range(0, W, 1024):
            if not have[cy // 256:(cy + 1024) // 256, cx // 256:(cx + 1024) // 256].any(): continue
            box = (cx, cy, min(cx + 1024, W), min(cy + 1024, H))
            img.crop(box).save(f"{ziel}/karte-dunkel-z{z}-{cx // 1024}-{cy // 1024}.jpg", "JPEG", quality=78, optimize=True)
            chunks.append([cx, cy, box[2] - cx, box[3] - cy, f"z{z}-{cx // 1024}-{cy // 1024}"])
    return {"x0": X0, "y0": Y0, "chunks": chunks}
if PROBE:
    os.makedirs("../dl/proben", exist_ok=True)
    # Ausschnitte: ganze Strecke z12, Mauer und Festung z14, Platz z15 (je mit der Strecke als dünne helle Linie zur Orientierung)
    for z, (la0, lo0, la1, lo1), nm in ((13, (40.178, 117.418, 40.256, 117.486), "z13_strecke"), (15, (40.238, 117.432, 40.252, 117.462), "z15_mauer"),
                                         (15, (40.226, 117.436, 40.247, 117.462), "z15_doerfer")):
        x0, y1 = px(la0, lo0, z); x1, y0 = px(la1, lo1, z); X0, Y0 = int(x0), int(y0); W, H = int(x1 - x0), int(y1 - y0)
        ts = kacheln(x0, y0, x1, y1)
        img = baue(VAR, z, ts, None, None, nur=(X0, Y0, W, H))
        d = ImageDraw.Draw(img)
        d.line([((px(a, b, z)[0] - X0), (px(a, b, z)[1] - Y0)) for a, b in pts], fill=(240, 240, 240), width=4 if z >= 14 else 3)
        d.line([((px(a, b, z)[0] - X0), (px(a, b, z)[1] - Y0)) for a, b in pts], fill=(215, 60, 50), width=2)
        img.save(f"../dl/proben/{VAR}_{nm}.jpg", quality=85); print("Probe", VAR, nm, img.size)
    sys.exit()
ASSETS = "../assets"; os.makedirs(ASSETS, exist_ok=True)
for f in os.listdir(ASSETS):
    if f.startswith("karte-"): os.remove(f"{ASSETS}/{f}")
meta = {}
for z, ts in STUFEN.items():
    meta[str(z)] = baue(VAR, z, ts, ASSETS, None); print(VAR, "z", z, len(ts), "Kacheln, Stücke", len(meta[str(z)]["chunks"]), flush=True)
json.dump({"variante": VAR, **meta}, open("tilemeta.json", "w"))
