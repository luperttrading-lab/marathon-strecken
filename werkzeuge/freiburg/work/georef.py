# Streckenplan 2026 des Veranstalters (Anwohnerinformation, ../dl/pdf/Druck_Marathon_Anwohnerinformation_2026.pdf, Seite 2: Rasterbild
# 3570 × 3079 px, 300 dpi, ../dl/render/awkarte-000.jpg via pdfimages) auf die Linie der RaceDayMap legen: blaue Pixel der Strecke
# (Farbe um 0/128/200) affin nach ETRS89/UTM 32N eingepasst (ICP gegen die RaceDayMap-Linie), dann die 20 Kilometerkästen (weiße
# Quadrate mit blauem Rand) gesucht und ihr Mittelpunkt auf die Linie gelotet. Ergebnis: Linienmeter der RaceDayMap an jedem
# Kilometerkasten des Plans (km 1–20) -> plan_km.json. Muster: werkzeuge/duesseldorf/work/georef.py, marken.py.
import json
import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.spatial import cKDTree
from pyproj import Transformer
T = Transformer.from_crs(4326, 25832, always_xy=True)
im = np.asarray(Image.open("../dl/render/awkarte-000.jpg")).astype(int)
H, W, _ = im.shape
blau = (np.abs(im[..., 0] - 5) < 45) & (np.abs(im[..., 1] - 128) < 30) & (np.abs(im[..., 2] - 200) < 35)
lab, n = ndimage.label(blau)
groesse = ndimage.sum(blau, lab, range(1, n + 1))
haupt = np.argsort(groesse)[::-1][:5] + 1
print("blaue Flächen, größte:", [(int(k), int(groesse[k - 1])) for k in haupt])
# Strecke: die größten Flächen (Linie, dazu angehängte Symbole); Kästen: Rand eines Quadrats 55–80 px
kaesten = []
for k, sl in enumerate(ndimage.find_objects(lab), 1):
    h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
    if 50 <= h <= 85 and 50 <= w <= 85 and abs(h - w) <= 8:
        teil = lab[sl] == k; fuell = teil.mean()
        innen = teil[8:-8, 8:-8].mean() if h > 20 else 1
        if fuell < 0.55 and innen < 0.35:
            kaesten.append(((sl[1].start + sl[1].stop) / 2, (sl[0].start + sl[0].stop) / 2, w, h, round(float(fuell), 2)))
print(len(kaesten), "Kästen")
g = json.load(open("runde.json")); d = np.array(g["d"]); Q = np.array(g["pts"])
ss = np.arange(0, d[-1], 5.0); E, N = T.transform(np.interp(ss, d, Q[:, 1]), np.interp(ss, d, Q[:, 0])); L = np.c_[E, N]
baum = cKDTree(L)
# Linienpixel: größte Fläche (Strecke) ohne dicke Stellen (Symbole): nur Pixel, die in ihrer 9×9-Umgebung < 60 % blau haben
linie = lab == haupt[0]
dicht = ndimage.uniform_filter(blau.astype(float), 9)
ys, xs = np.where(linie & (dicht < 0.6))
pix = np.c_[xs, ys].astype(float)[::3]
print(len(pix), "Linienpixel")
# Start: Rahmen auf Rahmen (Bild nach unten = Süden)
def affin(src, dst):
    A = np.c_[src, np.ones(len(src))]; M, *_ = np.linalg.lstsq(A, dst, rcond=None); return M
p0 = np.array([[pix[:, 0].min(), pix[:, 1].min()], [pix[:, 0].max(), pix[:, 1].max()], [pix[:, 0].min(), pix[:, 1].max()]])
u0 = np.array([[E.min(), N.max()], [E.max(), N.min()], [E.min(), N.min()]])
M = affin(p0, u0)
for it in range(60):
    U = np.c_[pix, np.ones(len(pix))] @ M
    dd, j = baum.query(U)
    gut = dd < max(8, np.percentile(dd, 90))
    M = affin(pix[gut], L[j[gut]])
U = np.c_[pix, np.ones(len(pix))] @ M; dd, j = baum.query(U)
print(f"Einpassung: Linienpixel zur RaceDayMap-Linie Median {np.median(dd):.1f} m, 90 % {np.percentile(dd, 90):.1f} m, 99 % {np.percentile(dd, 99):.1f} m")
print("Maßstab m/px:", np.round(np.hypot(*M[:2].T), 3))
# Rückrichtung: Linie der RaceDayMap zu Linienpixeln
pb = cKDTree(U); d2, _ = pb.query(L)
print(f"RaceDayMap-Linie zu Planlinie: Median {np.median(d2):.1f} m, 90 % {np.percentile(d2, 90):.1f} m, max {d2.max():.0f} m bei Linienmeter {ss[np.argmax(d2)]:.0f}")
weit = np.where(d2 > 25)[0]; grp = []
for i in weit:
    if grp and i - grp[-1][-1] <= 3: grp[-1].append(i)
    else: grp.append([i])
for gg in grp: print(f"   abweichend Linienmeter {ss[gg[0]]:.0f}–{ss[gg[-1]]:.0f}: bis {d2[gg].max():.0f} m")
# Kästen auf die Linie loten
km = []
for x, y, w, h, f in kaesten:
    e, nn = np.array([x, y, 1.0]) @ M
    dist, i = baum.query([e, nn]); km.append([float(ss[i]), float(dist), x, y])
km.sort()
for i, (s, dist, x, y) in enumerate(km): print(f"  Kasten {i + 1:2d}: Linienmeter {s:7.0f}  ({dist:4.0f} m neben der Linie)  Bild {x:.0f}/{y:.0f}")
json.dump({"M": M.tolist(), "kaesten": km, "linie_m": float(d[-1])}, open("plan_km.json", "w"))
