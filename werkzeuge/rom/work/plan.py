# Streckenplan 2026 des Veranstalters (Bild im Infoblatt ../dl/RRTM26_MARATHON_22.03.pdf, Seite 4, eingebettet als 2263 × 2514 px,
# ../dl/img/x72.png) auf die Linie (gpx2026.json) einpassen: affin, ICP über die roten Pixel der Streckenlinie (Startwerte aus
# den Rahmen beider), Ausreißer (Kilometerschilder, Beschriftungen) über das 75-%-Quantil. Danach Abstand der Linie zum Plan je
# 100 m -> plan_abstand.json; mit Argument „bild“ zusätzlich Überlagerungen je Ausschnitt in ../dl/img/ueberlagerung_*.png
import json, sys, numpy as np
from PIL import Image, ImageDraw
from pyproj import Transformer
from scipy.spatial import cKDTree
T = Transformer.from_crs(4326, 32633, always_xy=True)
img = Image.open("../dl/img/x72.png").convert("RGB"); a = np.asarray(img).astype(int); r, g, b = a[..., 0], a[..., 1], a[..., 2]
rot = (r > 180) & (g < 90) & (b < 110) & (r - g > 120)
yy, xx = np.nonzero(rot); MP = np.c_[xx, yy].astype(float); baum = cKDTree(MP)
G = json.load(open("gpx2026.json")); d = np.array(G["d"]); P = np.array([p[:2] for p in G["pts"]]); L = d[-1]
ss = np.arange(0, L, 10.0); Q = np.c_[T.transform(np.interp(ss, d, P[:, 1]), np.interp(ss, d, P[:, 0]))]
# Startwerte aus fünf Passpunkten (Pixel im Bild, von Hand abgelesen): Piazzale degli Eroi, Wende Lungotevere dell'Acqua Acetosa /
# Via Venezuela, Startpunkt, Piazza della Radio, Piazza del Popolo. Restfehler der Passpunkte 5–17 px (30–110 m): der Plan ist
# gezeichnet, nicht vermessen.
PASS = {"px": [[708, 978], [1103, 527], [1241, 1286], [946, 1653], [1061, 948]],
        "geo": [[41.90935, 12.4489], [41.93463, 12.47898], [41.89253, 12.48853], [41.86949, 12.46742], [41.9103, 12.4765]]}
U = np.array([T.transform(lo, la) for la, lo in PASS["geo"]])
A, *_ = np.linalg.lstsq(np.c_[U, np.ones(len(U))], np.array(PASS["px"], float), rcond=None)
for it in range(60):
    dist, j = baum.query(np.c_[Q, np.ones(len(Q))] @ A); ok = dist < min(12, np.percentile(dist, 85))
    A, *_ = np.linalg.lstsq(np.c_[Q[ok], np.ones(ok.sum())], MP[j[ok]], rcond=None)
dist, j = baum.query(np.c_[Q, np.ones(len(Q))] @ A)
m_px = 1 / np.sqrt(abs(np.linalg.det(A[:2])))
print(f"Plan auf Linie: Abstand Median {np.median(dist):.1f} px = {np.median(dist) * m_px:.0f} m, 90 % {np.percentile(dist, 90) * m_px:.0f} m; Maßstab {m_px:.2f} m/px")
json.dump({"A": A.tolist(), "m_px": m_px}, open("plan_affin.json", "w"))
ab = [[float(s), round(float(x * m_px), 1)] for s, x in zip(ss[::10], dist[::10])]
json.dump(ab, open("plan_abstand.json", "w"))
schlecht = [(round(s / 1000, 2), x) for s, x in ab if x > 40]
print("Stellen mehr als 40 m neben dem Plan (km Linie, m):", schlecht)
if len(sys.argv) > 1:
    st = json.load(open("strassen.json"))
    PX = np.c_[Q, np.ones(len(Q))] @ A
    big = img.copy(); dr = ImageDraw.Draw(big)
    dr.line([tuple(p) for p in PX], fill=(0, 90, 255), width=3)
    for k in range(0, int(L), 1000):
        p = PX[k // 10]; dr.ellipse([p[0] - 6, p[1] - 6, p[0] + 6, p[1] + 6], outline=(0, 0, 0), width=2); dr.text((p[0] + 8, p[1] - 6), str(k // 1000), fill=(0, 0, 0))
    x0, y0 = PX.min(axis=0) - 60; x1, y1 = PX.max(axis=0) + 60
    n = 0
    for cy in np.arange(y0, y1, 330):
        for cx in np.arange(x0, x1, 330):
            box = (int(cx), int(cy), int(cx + 400), int(cy + 400))
            inn = (PX[:, 0] > box[0]) & (PX[:, 0] < box[2]) & (PX[:, 1] > box[1]) & (PX[:, 1] < box[3])
            if inn.sum() < 5: continue
            big.crop(box).resize((800, 800)).save(f"../dl/img/ueberlagerung_{n:02d}.png"); n += 1
    print(n, "Ausschnitte")
