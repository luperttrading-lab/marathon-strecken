# Nur Abgleich: die nachgezeichnete Linie (gpx2026.json, orange) über dem Streckenplan des Veranstalters (Programm 2027, violett), mit der
# angepassten affinen Abbildung aus route_osm.py (plan_geordnet.json) zurück ins Bild gerechnet -> shots/plan_vergleich.png (ganze Karte)
# und shots/plan_vergleich_malbun.png, shots/plan_vergleich_vaduz.png (Ausschnitte, doppelt vergrößert). Kilometer der Linie in Rot.
import json
import numpy as np
from PIL import Image, ImageDraw
from pyproj import Transformer
from common import official
T = Transformer.from_crs(4326, 2056, always_xy=True)
cx, cy = map(np.array, json.load(open("plan_geordnet.json"))["affin"])
M = np.array([[cx[0], cx[1]], [cy[0], cy[1]]]); t = np.array([cx[2], cy[2]]); Mi = np.linalg.inv(M)
g = json.load(open("gpx2026.json")); P = np.array(g["pts"]); d = np.array(g["d"])
x, y = T.transform(P[:, 1], P[:, 0]); px = (np.c_[x, y] - t) @ Mi.T
im = Image.open("../dl/dateien/plan500-1.png").convert("RGB"); dr = ImageDraw.Draw(im)
dr.line([tuple(p) for p in px], fill=(255, 140, 0), width=3)
k = np.asarray(official(d))
for km in range(0, 43, 2):
    i = int(np.searchsorted(k, km * 1000)); i = min(i, len(px) - 1)
    dr.ellipse([px[i][0] - 5, px[i][1] - 5, px[i][0] + 5, px[i][1] + 5], fill=(230, 0, 0)); dr.text((px[i][0] + 7, px[i][1] - 7), str(km), fill=(200, 0, 0))
im.crop((450, 180, 2500, 2650)).resize((1025, 1235)).save("shots/plan_vergleich.png")
im.crop((1950, 2150, 2450, 2650)).resize((1000, 1000)).save("shots/plan_vergleich_malbun.png")
im.crop((900, 1350, 1300, 1800)).resize((800, 900)).save("shots/plan_vergleich_vaduz.png")
print("shots/plan_vergleich*.png")
