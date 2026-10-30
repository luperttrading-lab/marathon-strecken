# Höhenprofil des Veranstalters aus dem Streckenplan „Authentic Marathon Race Route“ (SEGAS, maratonia_diadrome.jpg, 2000 × 1380 px,
# athensauthenticmarathon.gr/img/product/map/2025/03/). Das Profil läuft von rechts (Start, 0 km) nach links (Ziel, 42,195 km).
# Achsen aus dem Bild: senkrechte Linien 0/5/…/40 km bei x = 1401, 1240,5, 1081, 920, 760, 600, 439,5, 279,5, 118,5 (32,06 px je km),
# waagerechte Linien 0/50/…/250 m bei y = 400, 375, 350, 325, 300, 275 (0,5 px je m, also 2 m je Pixel). Die Linie ist gut 5 px dick;
# je Spalte die Mitte des orangen Strichs, verfolgt von rechts nach links (die Schilder „Start“ und „Finish“ sind auch orange).
# -> planprofil.json [[km, h], …]
import json
import numpy as np
from PIL import Image
a = np.asarray(Image.open("../dl/maratonia_diadrome.jpg").convert("RGB")).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
org = (R > 200) & (G > 60) & (G < 160) & (B < 100)
X0, PXKM = 1401.0, (1401.0 - 118.5) / 40
def km(x): return (X0 - x) / PXKM
def hoehe(y): return (400.0 - y) * 2.0
out, prev = [], None
for x in range(1404, 47, -1):
    ys = np.nonzero(org[265:405, x])[0] + 265
    if len(ys) == 0: continue
    # zusammenhängende Läufe; der dem vorigen Wert nächste (am Start: der unterste, das Schild steht darüber)
    laeufe, st = [], ys[0]
    for u, v in zip(ys, ys[1:]):
        if v != u + 1: laeufe.append((st, u)); st = v
    laeufe.append((st, ys[-1]))
    laeufe = [l for l in laeufe if 2 <= l[1] - l[0] + 1 <= 12]
    if not laeufe: continue
    l = max(laeufe, key=lambda l: l[0]) if prev is None else min(laeufe, key=lambda l: abs((l[0] + l[1]) / 2 - prev))
    y = (l[0] + l[1]) / 2
    if prev is not None and abs(y - prev) > 8: continue
    prev = y
    k = km(x)
    if -0.05 <= k <= 42.3: out.append([round(min(max(k, 0), 42.195), 3), round(hoehe(y), 1)])
out.sort()
json.dump(out, open("planprofil.json", "w"))
p = np.array(out)
print(len(p), "Punkte, km", p[0, 0], "–", p[-1, 0], "Höhe", p[:, 1].min(), "–", p[:, 1].max(), "bei km", p[np.argmax(p[:, 1]), 0])
for k in range(0, 43, 3): print(k, float(np.interp(k, p[:, 0], p[:, 1])))
