# Streckenkarte des Veranstalters (Seite „Wissenswertes“ bzw. „Strecken“, HGL_Streckenkarte_2024.jpg, 2000 × 1533 px, Kartengrafik
# „© Passeck & Wernecke 2016“, ../dl/bilder/) auf die gelegte Linie (gelegt.json) einpassen: rote Linienpixel des Brocken-Marathons
# (Farbe um 225/30/45) affin nach ETRS89/UTM 32N (ICP gegen die Linie), dann die Kilometerdreiecke (rot gefüllt, schwarzer Rand, nach der
# Linie die größten roten Flecken nach einem Öffnen mit 7 px) und die Verpflegungszeichen (grüne Kreise mit weißem „V“) gesucht und auf die
# Linie gelotet. Die Karte ist eine Grafik: die Linie ist geglättet und gegenüber den Wegen bis etwa 100 m verschoben; die Lote gelten
# deshalb nur auf einige hundert Meter. Nur Abgleich (karte_km.json), die App nimmt die Verpflegung aus den Orten (stationen.py).
# Muster: werkzeuge/freiburg/work/georef.py.
import json
import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.spatial import cKDTree
from pyproj import Transformer
T = Transformer.from_crs(4326, 25832, always_xy=True)
im = np.asarray(Image.open("../dl/bilder/HGL_Streckenkarte_2024.jpg").convert("RGB")).astype(int)
H, W, _ = im.shape
R, Gr, B = im[..., 0], im[..., 1], im[..., 2]
rot = (R > 175) & (Gr < 80) & (B < 90) & (R - Gr > 120)
rot[:140] = False                                   # Kopf mit Titel und Logo
lab, n = ndimage.label(rot); groesse = ndimage.sum(rot, lab, range(1, n + 1))
haupt = int(np.argmax(groesse)) + 1
print("rote Flächen:", n, " größte", int(groesse.max()), "px")
g = json.load(open("gelegt.json")); d = np.array(g["d"]); Q = np.array(g["pts"])
ss = np.arange(0, d[-1], 5.0); E, N = T.transform(np.interp(ss, d, Q[:, 1]), np.interp(ss, d, Q[:, 0])); L = np.c_[E, N]
baum = cKDTree(L)
# Linie: alle roten Flecken über 150 px (weiße Pfeile und Beschriftungen zerteilen sie), ohne dicke Stellen (Dreiecke, Kreuze)
gross = np.isin(lab, np.where(groesse > 150)[0] + 1)
dicht = ndimage.uniform_filter(rot.astype(float), 15)
ys, xs = np.where(gross & (dicht < 0.75))
pix = np.c_[xs, ys].astype(float)[::2]
print(len(pix), "Linienpixel")
def affin(src, dst):
    A = np.c_[src, np.ones(len(src))]; M, *_ = np.linalg.lstsq(A, dst, rcond=None); return M
# Anfang: vier von Hand abgelesene Stellen im Bild (Start/Ziel, Blochhauer Brücke, Gipfel 1142, Skihütten an der Hohne) gegen die Linie an
# derselben Stelle (Linienmeter: Start, Wegweiser „Blochhauer“, Gipfel, Haltestelle Hohnepfahl)
f0 = d[-1] / 42195.0
p0 = np.array([[1540, 690], [850, 300], [368, 1076], [1170, 1265]], float)
u0 = np.array([[np.interp(k * f0, ss, E), np.interp(k * f0, ss, N)] for k in (0, 7960, 19200, 30000)])
M = affin(p0, u0)
for it in range(80):
    U = np.c_[pix, np.ones(len(pix))] @ M
    dd, j = baum.query(U)
    gut = dd < max(40, np.percentile(dd, 80))
    M = affin(pix[gut], L[j[gut]])
U = np.c_[pix, np.ones(len(pix))] @ M; dd, j = baum.query(U)
print(f"Einpassung: Linienpixel zur Linie Median {np.median(dd):.0f} m, 90 % {np.percentile(dd, 90):.0f} m, 99 % {np.percentile(dd, 99):.0f} m;"
      f" Maßstab {np.round(np.hypot(*M[:2].T), 2)} m/px")
pb = cKDTree(U); d2, _ = pb.query(L)
print(f"Linie zur Kartenlinie: Median {np.median(d2):.0f} m, 90 % {np.percentile(d2, 90):.0f} m, max {d2.max():.0f} m bei Linienmeter {ss[np.argmax(d2)]:.0f}")
f = 42195.0 / d[-1]
def lot(x, y):
    e, nn = np.array([x, y, 1.0]) @ M; dist, i = baum.query([e, nn]); return float(ss[i]), float(dist)
# Kilometerdreiecke: rote Flecken, die ein Öffnen mit einem Kreis von 13 px überstehen (die Linie ist ~10 px breit und verschwindet,
# die Dreiecke sind ~25 × 20 px), mit schwarzem Rand
yy, xx = np.mgrid[-6:7, -6:7]; offen = ndimage.binary_opening(rot, structure=(xx ** 2 + yy ** 2 <= 36))
lb, nb = ndimage.label(offen); dreiecke = []
for k, sl in enumerate(ndimage.find_objects(lb), 1):
    h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
    if 8 <= h <= 40 and 8 <= w <= 40:
        cy, cx = ndimage.center_of_mass(lb == k)
        rand = im[max(0, sl[0].start - 6):sl[0].stop + 6, max(0, sl[1].start - 6):sl[1].stop + 6]
        schwarz = ((rand.sum(axis=2) < 150)).mean()
        dreiecke.append((cx, cy, w, h, round(float(schwarz), 3)))
# grüne Kreise mit V
gruen = (Gr > 70) & (Gr < 150) & (R < 60) & (B > 50) & (B < 120)
lg, ng = ndimage.label(ndimage.binary_closing(gruen, structure=np.ones((5, 5)))); vs = []
for k, sl in enumerate(ndimage.find_objects(lg), 1):
    h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
    if 25 <= h <= 60 and 25 <= w <= 60 and abs(h - w) < 8:
        vs.append(((sl[1].start + sl[1].stop) / 2, (sl[0].start + sl[0].stop) / 2))
aus = {"M": M.tolist(), "dreiecke": [], "v": []}
# Die Dreiecke sitzen auf der Linie und verschmelzen mit ihr; Mitte des Dreiecks von Hand abgelesen (Bild 2000 × 1533 px)
HAND = {5: (1135, 428), 10: (697, 452), 15: (400, 790), 20: (415, 1078), 25: (670, 1215), 30: (1170, 1265), 35: (1060, 915), 40: (1315, 735)}
print("Kilometerdreiecke (von Hand abgelesen):")
aus["km_hand"] = {}
for k, (x, y) in HAND.items():
    s, dist = lot(x, y); aus["km_hand"][k] = [s, dist]
    print(f"   km {k:2d} der Karte: hier km {s * f / 1000:6.2f} ({s * f / 1000 - k:+.2f}), {dist:4.0f} m neben der Linie")
print("Dreiecke (rot, Kandidaten):")
for x, y, w, h, sw in sorted(dreiecke, key=lambda t: lot(t[0], t[1])[0]):
    s, dist = lot(x, y); aus["dreiecke"].append([s, dist, x, y, sw])
    print(f"   Bild {x:6.0f}/{y:5.0f} ({w}×{h} px, Rand dunkel {sw:.2f}): km {s * f / 1000:6.2f}, {dist:4.0f} m neben der Linie")
print("Verpflegung (V):")
for x, y in sorted(vs, key=lambda t: lot(*t)[0]):
    s, dist = lot(x, y); aus["v"].append([s, dist, x, y])
    print(f"   Bild {x:6.0f}/{y:5.0f}: km {s * f / 1000:6.2f}, {dist:4.0f} m neben der Linie")
json.dump(aus, open("karte_km.json", "w"))
