# Streckenplan 2025 des Veranstalters (Seite „上马赛事路线图“, Rasterbild 4739 × 6571 px, ../dl/bilder/bkeq2u5mfMbpVKf5.JPG; für 2026
# zeigt die Seite „赛事路线图“ am 31.10.2026 nur „敬请期待！“, also noch keinen Plan) -> plan2025.json:
#   ../dl/plan_blau.npy: alle Pixel in der Farbe der Streckenlinie (RGB etwa 32/117/184), ausgedünnt auf jedes 3. Pixel (groß, bleibt lokal);
#   „km“: Mitten der Kilometerkreise 1–42 (Kreis mit Zahl, an 5/10/…/40 größer), von Hand grob abgelesen (Vorschaubild 1400 px breit)
#   und auf den nächsten gefundenen Kreis gesetzt (größter Abstand zum Rand der blauen Fläche);
#   „start“, „ziel“: Sterne „起点“ und „终点“; „wende“: Spitzen der Wendepunkte, die die Linie zeigt (grob, von Hand).
# Die Kreise sind von Hand gezeichnet und stehen neben der Linie; sie taugen zum Einpassen und zur Gegenprobe, nicht als Schilder.
import json
import numpy as np
from PIL import Image
from scipy import ndimage as nd
im = Image.open("../dl/bilder/bkeq2u5mfMbpVKf5.JPG").convert("RGB"); A = np.asarray(im).astype(int)
H, W = A.shape[:2]; S = W / 1400.0
R, G, B = A[..., 0], A[..., 1], A[..., 2]
blau = (R < 90) & (G > 85) & (G < 150) & (B > 150) & (B - R > 100)
voll = nd.binary_fill_holes(nd.binary_closing(blau, iterations=4)); dt = nd.distance_transform_edt(voll)
# grobe Lage der Kreise im Vorschaubild (x, y)
GROB = {1: (903, 393), 2: (823, 347), 3: (753, 299), 4: (658, 336), 5: (544, 366), 6: (447, 416), 7: (352, 489), 8: (397, 592),
        9: (506, 557), 10: (609, 505), 11: (690, 516), 12: (692, 488), 13: (766, 486), 14: (813, 596), 15: (845, 713), 16: (853, 812),
        17: (914, 785), 18: (911, 812), 19: (963, 778), 20: (993, 688), 21: (982, 767), 22: (889, 860), 23: (813, 836), 24: (705, 873),
        25: (637, 913), 26: (569, 980), 27: (547, 1107), 28: (559, 1220), 29: (572, 1329), 30: (494, 1435), 31: (460, 1553),
        32: (495, 1660), 33: (457, 1574), 34: (464, 1461), 35: (527, 1372), 36: (546, 1246), 37: (516, 1178), 38: (528, 1093),
        39: (456, 1038), 40: (437, 1090), 41: (364, 1128), 42: (281, 1059)}
km = {}
for k, (x, y) in GROB.items():
    X, Y = int(x * S), int(y * S); r = 45
    sub = dt[Y - r:Y + r, X - r:X + r]; j = np.unravel_index(np.argmax(sub), sub.shape)
    km[k] = [int(X - r + j[1]), int(Y - r + j[0]), round(float(sub[j]), 1)]
    if sub[j] < 28: print("  km", k, "kein Kreis gefunden, Radius", sub[j])
start = [int(874 * S), int(307 * S)]; ziel = [int(289 * S), int(1047 * S)]
# Wendepunkte, wie die Linie sie zeigt (Vorschaubild): Longteng Dadao Süd hinter km 32, Fenggu Lu (km 37), Bansongyuan Lu (km 17),
# Lujiabang Lu (km 20)
WENDE = {"longteng": (497, 1679), "fenggu": (508, 1178), "bansongyuan": (920, 762), "lujiabang": (1003, 676)}
# nur die zusammenhängenden blauen Flächen, die einen Kilometerkreis enthalten (Linie samt Kreisen); Schrift, Rahmen, Logo und die
# Symbole der Getränkestellen (eigene Flächen neben der Linie) fallen weg
lab, n = nd.label(nd.binary_dilation(blau, iterations=2))
behalten = {lab[v[1], v[0]] for v in km.values()} - {0}
ys, xs = np.where(blau & np.isin(lab, list(behalten)))
print(len(behalten), "Flächen mit Kilometerkreisen")
sel = (np.arange(len(xs)) % 3) == 0
json.dump({"breite": W, "hoehe": H, "km": km, "start": start, "ziel": ziel,
           "wende": {k: [int(x * S), int(y * S)] for k, (x, y) in WENDE.items()}}, open("plan2025.json", "w"))
np.save("../dl/plan_blau.npy", np.c_[xs[sel], ys[sel]].astype(np.int32))
print(len(km), "Kreise,", sel.sum(), "blaue Pixel (jedes 3.)")
for k, v in km.items(): print(f"  km {k:2d}: {v}")
