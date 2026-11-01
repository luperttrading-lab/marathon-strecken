# Prüfbild (nur Abgleich): Linie mit km-Marken und Flurnamen auf den OSM-Kacheln der Stufe 15 -> shots/_karte.png
import glob, json, math
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from common import official
z = 15
def px(lat, lon):
    n = 256 * 2 ** z
    return (lon + 180) / 360 * n, (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
fs = glob.glob(f"../dl/tiles/osm_{z}_*.png"); ts = [tuple(map(int, f.split("_")[-2:][0:1] + [f.split("_")[-1][:-4]])) for f in fs]
xs = [t[0] for t in ts]; ys = [t[1] for t in ts]; x0, y0 = min(xs), min(ys)
img = Image.new("RGB", ((max(xs) - x0 + 1) * 256, (max(ys) - y0 + 1) * 256), (240, 240, 240))
for f, (x, y) in zip(fs, ts): img.paste(Image.open(f).convert("RGB"), ((x - x0) * 256, (y - y0) * 256))
dr = ImageDraw.Draw(img); F = ImageFont.load_default(size=20)
r = json.load(open("dgm_10m.json")); k = official([x[0] for x in r])
P = [(px(a[1], a[2])[0] - x0 * 256, px(a[1], a[2])[1] - y0 * 256) for a in r]
dr.line(P, fill=(220, 0, 0), width=4)
for km in np.arange(0.5, 10, 0.5):
    i = int(np.argmin(np.abs(k - km * 1000))); x, y = P[i]
    dr.ellipse((x - 14, y - 14, x + 14, y + 14), fill=(255, 255, 255), outline=(0, 0, 0)); dr.text((x, y), f"{km:g}", fill=(0, 0, 0), font=ImageFont.load_default(size=13), anchor="mm")
o = json.load(open("orte.json"))
import xml.etree.ElementTree as ET
for f in glob.glob("../dl/osmapi/t_*.xml"):
    for n in ET.parse(f).getroot().iter("node"):
        tg = {t.get("k"): t.get("v") for t in n.iter("tag")}
        if tg.get("place") == "locality" or tg.get("natural") == "peak" or tg.get("historic"):
            x, y = px(float(n.get("lat")), float(n.get("lon"))); dr.text((x - x0 * 256, y - y0 * 256), tg.get("name", "?"), fill=(0, 0, 160), font=F)
img.save("shots/_karte.png"); print(img.size)
