# (Kopie aus werkzeuge/freiburg/work/karte.py)
# Prüfbilder: Linien und Punkte auf OSM-Kacheln (tile.openstreetmap.org, Zwischenspeicher ../dl/tiles), nur zum Ansehen.
# Aufruf als Modul: bild(datei, (lat_min, lat_max, lon_min, lon_max), z, linien=[(pts [[lat, lon]…], farbe, breite)], punkte=[(lat, lon, text, farbe)])
import math, os, time, urllib.request
from PIL import Image, ImageDraw
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../dl/tiles"); os.makedirs(OUT, exist_ok=True)
def px(lat, lon, z):
    n = 256 * 2 ** z
    return (lon + 180) / 360 * n, (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
def kachel(z, x, y):
    f = f"{OUT}/osm_{z}_{x}_{y}.png"
    if not (os.path.exists(f) and os.path.getsize(f) > 100):
        req = urllib.request.Request(f"https://tile.openstreetmap.org/{z}/{x}/{y}.png", headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial, one-time download)"})
        for att in range(4):
            try: open(f, "wb").write(urllib.request.urlopen(req, timeout=30).read()); time.sleep(0.2); break
            except Exception: time.sleep(2 + 3 * att)
    return Image.open(f).convert("RGB")
def bild(datei, bb, z, linien=(), punkte=()):
    x0, y1 = px(bb[0], bb[2], z); x1, y0 = px(bb[1], bb[3], z)
    tx0, ty0, tx1, ty1 = int(x0 // 256), int(y0 // 256), int(x1 // 256), int(y1 // 256)
    im = Image.new("RGB", ((tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256))
    for x in range(tx0, tx1 + 1):
        for y in range(ty0, ty1 + 1): im.paste(kachel(z, x, y), ((x - tx0) * 256, (y - ty0) * 256))
    im = Image.blend(im, Image.new("RGB", im.size, (255, 255, 255)), 0.35)
    dr = ImageDraw.Draw(im)
    def P(la, lo): a, b = px(la, lo, z); return a - tx0 * 256, b - ty0 * 256
    for pts, farbe, breite in linien: dr.line([P(*p) for p in pts], fill=farbe, width=breite)
    for la, lo, t, farbe in punkte:
        x, y = P(la, lo); dr.ellipse([x - 4, y - 4, x + 4, y + 4], fill=farbe, outline="black"); dr.text((x + 6, y - 6), t, fill="black")
    a, b = P(bb[1], bb[2]); c, d = P(bb[0], bb[3])
    im.crop((int(a), int(b), int(c), int(d))).save(datei)
