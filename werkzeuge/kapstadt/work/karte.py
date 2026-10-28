# Streckenkarte 2026 des Veranstalters (../dl/route.jpg, 2400 × 1411, Bild ohne Koordinaten) auf die Linie legen: gelbe
# Streckenpixel, affine Abbildung Bild -> Meter, Startwert aus drei Stellen (Wendepunkt Sea Point, Südspitze Claremont, Cut-off 5),
# dann iterativ nächster Linienpunkt + kleinste Quadrate (Ausreißer über 120 m verworfen). Ergebnis: Abstand der Karte zur Linie
# (zeigt Abweichungen der Strecke 2026) und die Lage der 15 Getränkestellen (Pixel von Hand abgelesen) -> karte.json
import json, math, numpy as np
from PIL import Image
from scipy.spatial import cKDTree
S = 2400 / 1400   # Pixel abgelesen im auf 1400 Breite verkleinerten Bild
k = math.cos(math.radians(-33.93)) * 111320
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
ss = np.arange(0, d[-1], 10.0); R = np.c_[np.interp(ss, d, P[:, 1]) * k, np.interp(ss, d, P[:, 0]) * 110540]
rb = cKDTree(R)
def at(m): i = int(m / 10); return R[min(i, len(R) - 1)]
f = d[-1] / 42195
a = np.asarray(Image.open("../dl/route.jpg").convert("RGB")).astype(int)
m = (a[..., 0] > 200) & (a[..., 1] > 170) & (a[..., 2] < 110) & (a[..., 0] - a[..., 2] > 120)
m[:330, :700] = False   # Logo oben links
yy, xx = np.nonzero(m); pix = np.c_[xx, yy].astype(float)[::3]
print("gelbe Pixel", len(pix))
start_bild = np.array([[112, 688], [1308, 632], [897, 128]]) * S
start_welt = np.array([at(38700 * f), at(15000 * f + 60), at(25500 * f)])
def affin(src, dst):
    A = np.c_[src, np.ones(len(src))]; M, *_ = np.linalg.lstsq(A, dst, rcond=None); return M
M = affin(start_bild, start_welt)
for it in range(30):
    W = np.c_[pix, np.ones(len(pix))] @ M; dd, j = rb.query(W)
    keep = dd < (300 if it < 5 else 120)
    M = affin(pix[keep], R[j[keep]])
W = np.c_[pix, np.ones(len(pix))] @ M; dd, j = rb.query(W)
print(f"Karte -> Linie: Median {np.median(dd):.0f} m, 90 % {np.percentile(dd, 90):.0f} m, Anteil < 60 m {np.mean(dd < 60) * 100:.0f} %")
# Linie -> Karte: Stücke der Linie ohne gelbe Pixel in der Nähe (Strecke 2026 anders?)
kb = cKDTree(W); back = kb.query(R)[0]; i = 0
while i < len(back):
    if back[i] <= 80: i += 1; continue
    j2 = i
    while j2 + 1 < len(back) and back[j2 + 1] > 80: j2 += 1
    if (j2 - i + 1) * 10 >= 100: print(f"   Linie km {ss[i] / f / 1000:5.2f}-{ss[j2] / f / 1000:5.2f}: keine Karte in 80 m (max {back[i:j2 + 1].max():.0f} m)")
    i = j2 + 1
# Getränkestellen: Becher-Symbole im verkleinerten Bild (Mitte des Bechers), in Reihenfolge der Nummern
BECHER = [(313, 323), (662, 285), (840, 232), (1120, 365), (1265, 510), (1225, 372), (1145, 250), (1070, 220), (745, 193),
          (485, 400), (415, 532), (432, 383), (300, 370), (140, 468), (105, 603)]
ws = np.c_[np.array(BECHER) * S, np.ones(len(BECHER))] @ M
pos, last = [], 0.0
for n, w in enumerate(ws, 1):
    dist = np.hypot(*(R - w).T); kand = np.where(dist < 250)[0]
    kand = [c for c in kand if ss[c] > last] or list(np.argsort(dist)[:1])
    c = min(kand, key=lambda c: dist[c] + 0.02 * (ss[c] - last))   # nächster Punkt nach der vorigen Stelle
    pos.append([n, round(float(ss[c]), 1), round(float(dist[c]))]); last = ss[c]
    print(f"   Getränkestelle {n:2d}: Linienmeter {ss[c]:7.0f} (km {ss[c] / f / 1000:5.2f}), Symbol {dist[c]:.0f} m neben der Linie")
json.dump({"affin": M.tolist(), "getraenke": pos}, open("karte.json", "w"))
