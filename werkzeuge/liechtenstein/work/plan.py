# Strecke aus dem Streckenplan des Veranstalters (Programm 2027, „Programm_26_LGT_Alpine_Marathon_2027_GzD.pdf“, Karte von
# reygrafik.ch, ../dl/dateien/): Die violette Linie (RGB 114/34/131) bei 500 dpi ausgelesen, Beschriftungskästen weg, mit einer
# affinen Abbildung auf LV95 gelegt. Passpunkte: fünf Bahnhofssymbole (Haag-Gams, Nendeln, Schaan-Vaduz, Buchs SG, Sevelen) und
# das Schlosssymbol Vaduz, Koordinaten aus geo.admin.ch (Haltestellen, swissNAMES3D). Die Symbole stehen neben den Bahnhöfen: Reste
# bis 140 m. Die Linie dient nur als Führung für route_osm.py (Wege aus OSM); sie selbst ist eine Grafik, keine Vermessung.
# Aufruf: python3 plan.py  -> ../dl/plan_lv95.json (2 MB, bleibt lokal) {"px": [[x, y], …] Pixel, "lv95": [[E, N], …], "affin": …}
import json, os, subprocess
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
DL = "../dl/dateien"
PDF = f"{DL}/f_12659.pdf"
PNG = f"{DL}/plan500-1.png"
if not os.path.exists(PNG):
    subprocess.check_call(["pdftoppm", "-r", "500", "-png", "-f", "1", "-l", "1", "-x", "0", "-y", "290", "-W", "2850", "-H", "2700", PDF, f"{DL}/plan500"])
im = np.asarray(Image.open(PNG).convert("RGB")).astype(int)
r, g, b = im[..., 0], im[..., 1], im[..., 2]
m = (np.abs(r - 114) < 22) & (np.abs(g - 34) < 28) & (np.abs(b - 131) < 22)
m[:1500, 1800:] = False                                            # Legende
dick = ndi.binary_dilation(ndi.binary_opening(m, structure=np.ones((13, 13))), iterations=14)   # Kästen „10 km“, „ZIEL“ …
lin = m & ~dick
lab, n = ndi.label(lin, structure=np.ones((3, 3)))
sz = ndi.sum(lin, lab, range(1, n + 1))
lin = np.isin(lab, 1 + np.where(sz > 150)[0])
ys, xs = np.where(lin)
# Passpunkte: Mitte der Bahnhofssymbole (53 × 53 px) und des Schlosses; LV95 aus geo.admin.ch SearchServer
PP = [((370.5, 336.5), (2754556, 1230499), "Haag-Gams"), ((1225.5, 440.5), (2759353, 1229868), "Nendeln"),
      ((796.5, 1063.5), (2756906, 1226260), "Schaan-Vaduz"), ((401.5, 1075.5), (2754612, 1226162), "Buchs SG"),
      ((631.5, 1901.5), (2755917, 1221402), "Sevelen"), ((1048, 1665), (2758204, 1223031), "Schloss Vaduz")]
P = np.array([p for p, _, _ in PP], float); G = np.array([q for _, q, _ in PP], float)
A = np.c_[P, np.ones(len(P))]
cx = np.linalg.lstsq(A, G[:, 0], rcond=None)[0]; cy = np.linalg.lstsq(A, G[:, 1], rcond=None)[0]
res = np.c_[A @ cx, A @ cy] - G
for (_, _, nm), (dx, dy) in zip(PP, res): print(f"  Passpunkt {nm:14s} Rest {dx:+5.0f} / {dy:+5.0f} m")
E = cx[0] * xs + cx[1] * ys + cx[2]; N = cy[0] * xs + cy[1] * ys + cy[2]
print(len(xs), "Linienpixel,", f"{np.hypot(cx[0], cy[0]):.2f} m je Pixel")
json.dump({"px": np.c_[xs, ys].tolist(), "lv95": np.c_[E, N].round(1).tolist(), "affin": [cx.tolist(), cy.tolist()]}, open("../dl/plan_lv95.json", "w"))
