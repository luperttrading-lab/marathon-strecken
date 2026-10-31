# Nur zum Ansehen: Linien (GPX, abgeleitete Linie) über OSM-Kacheln zeichnen -> shots/ansicht_<name>.png
# Aufruf: python3 ansicht.py <name> <lat_min> <lat_max> <lon_min> <lon_max> <zoom> [linie.json …]
#   linie.json: {"pts": [[lat, lon, …], …]} (gpx2026.json, linie2026.json) oder dgm2026_10m.json ([[s, lat, lon, h], …])
import json, math, os, sys, time, urllib.request
from PIL import Image, ImageDraw
OUT = "../dl/tiles"; os.makedirs(OUT, exist_ok=True)
def px(lat, lon, z):
    n = 256 * 2 ** z
    return (lon + 180) / 360 * n, (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
def kachel(z, x, y):
    f = f"{OUT}/osm_{z}_{x}_{y}.png"
    if not (os.path.exists(f) and os.path.getsize(f) > 100):
        req = urllib.request.Request(f"https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                                     headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial, one-time download)"})
        open(f, "wb").write(urllib.request.urlopen(req, timeout=30).read()); time.sleep(0.2)
    return Image.open(f).convert("RGB")
name, la0, la1, lo0, lo1, z = sys.argv[1], *map(float, sys.argv[2:6]), int(sys.argv[6])
x0, y1 = px(la0, lo0, z); x1, y0 = px(la1, lo1, z)
tx0, ty0, tx1, ty1 = int(x0 // 256), int(y0 // 256), int(x1 // 256), int(y1 // 256)
im = Image.new("RGB", ((tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256))
for tx in range(tx0, tx1 + 1):
    for ty in range(ty0, ty1 + 1): im.paste(kachel(z, tx, ty), ((tx - tx0) * 256, (ty - ty0) * 256))
dr = ImageDraw.Draw(im)
FARBEN = [(220, 0, 0), (0, 90, 255), (0, 160, 0), (200, 0, 200)]
for n, f in enumerate(sys.argv[7:]):
    j = json.load(open(f)); pts = j["pts"] if isinstance(j, dict) else [p[1:3] for p in j]
    xy = [(px(p[0], p[1], z)[0] - tx0 * 256, px(p[0], p[1], z)[1] - ty0 * 256) for p in pts]
    dr.line(xy, fill=FARBEN[n % 4], width=2)
    if isinstance(j, dict) and j.get("punkte", True):
        for x, y in xy: dr.ellipse((x - 2, y - 2, x + 2, y + 2), outline=FARBEN[n % 4])
os.makedirs("shots", exist_ok=True); im.save(f"shots/ansicht_{name}.png"); print(f"shots/ansicht_{name}.png", im.size)
