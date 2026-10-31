# Nur Abgleich: Kilometermarken des Streckenplans 2026 (PDF, Lage der Texte „1k“ … „42k“ aus ../dl/pdf/bbox.html) gegen die
# gleichmäßig gestauchte Strava-Linie (common.py). Der Plan ist eine Zeichnung ohne Koordinaten: Eine affine Abbildung Plan -> UTM
# wird an die Marken angepasst, getrennt für den Westteil (km 0–12 und 40–42, Innenstadt bis Kapiʻolani Park) und den Ostteil
# (km 12–40), weil der Plan maßstäblich verzerrt ist. Für jede Verschiebung der Kilometer längs der Linie (−600 bis +600 m) zeigt
# der mittlere Abstand, ob die Kilometer der Linie zu den Marken des Plans passen (Verschiebung 0 am besten = Start an der
# richtigen Stelle, keine Streckung nötig).
import json, re
import numpy as np
from pyproj import Transformer
from common import official
T = Transformer.from_crs(4326, 32604, always_xy=True)
s = open("../dl/pdf/bbox.html", encoding="utf-8").read()
M = []
for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(\d+)k</word>', s):
    x, y = (float(m.group(1)) + float(m.group(3))) / 2, (float(m.group(2)) + float(m.group(4))) / 2
    if y < 3200 and not (4600 < x and y > 2650): M.append((float(m.group(5)), x, y))
M.sort(); K = np.array([m[0] for m in M]); PL = np.array([[m[1], -m[2]] for m in M])
r = json.load(open("dgm2026_10m.json")); sl = np.array([x[0] for x in r]); k = official(sl)
X, Y = T.transform(np.array([x[2] for x in r]), np.array([x[1] for x in r]))
def lage(km_m): return np.interp(km_m, k, X), np.interp(km_m, k, Y)
for teil, sel in (("West (km 1–12, 40–42)", (K <= 12) | (K >= 40)), ("Ost (km 12–38)", (K >= 12) & (K <= 38))):
    erg = []
    for ver in range(-600, 601, 25):
        x, y = lage(K[sel] * 1000 + ver); A = np.c_[PL[sel], np.ones(sel.sum())]
        cx, *_ = np.linalg.lstsq(A, x, rcond=None); cy, *_ = np.linalg.lstsq(A, y, rcond=None)
        res = np.hypot(A @ cx - x, A @ cy - y); erg.append((np.sqrt(np.mean(res ** 2)), ver, res))
    rms, ver, res = min(erg, key=lambda e: e[0]); null = [e for e in erg if e[1] == 0][0]
    print(f"{teil}: {sel.sum()} Marken; beste Verschiebung {ver:+d} m (mittlerer Abstand {rms:.0f} m), ohne Verschiebung {null[0]:.0f} m")
    print("   je Verschiebung:", " ".join(f"{e[1]:+d}:{e[0]:.0f}" for e in erg[::4]))
    print("   Abstand je Marke ohne Verschiebung:", " ".join(f"{kk:g}:{rr:.0f}" for kk, rr in zip(K[sel], null[2])))
