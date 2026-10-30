# Form der Höhenkurve des Veranstalters gegen das eigene Profil legen -> form.json (Bezugspunkte Linienmeter <-> km).
# Dynamic Time Warping zwischen SRTM entlang der Linie (alle 10 Linienmeter; SRTM passt zur Kurve des Veranstalters am besten,
# vergleich.py) und der Kurve des Veranstalters (alle 10 offizielle Meter), Kosten |Δh| nach Abzug des mittleren Versatzes,
# Band ±800 m um die Diagonale (Linie · 42195 / Länge), Schrittweiten 1:1, 1:2, 2:1. Verwertbar ist die Zuordnung nur, wo die
# Kurve deutlich steigt oder fällt (|Steigung| ≥ 3 % über 200 m): im flachen Tal ist sie beliebig. Bezugspunkte alle 500 m dort.
import json
import numpy as np
from dgm import abtasten
R = np.array(json.load(open("dgm_cop30_10m.json"))); s = R[:, 0]; lat = R[:, 1]; lon = R[:, 2]; GL = json.load(open("linie.json"))["d"][-1]
raw = np.fromfile("../dl/dem/N40E117.hgt", ">i2").reshape(3601, 3601).astype(float)
hA = abtasten(raw, 117.0, 41.0, 1 / 3600, 1 / 3600, lat, lon, mitte=False)
PP = np.array(json.load(open("planprofil.json"))); kB = np.arange(0, 42195.1, 10.0); hB = np.interp(kB / 1000, PP[:, 0], PP[:, 1])
hA = hA - np.median(hA - np.interp(s * 42195 / GL / 1000, PP[:, 0], PP[:, 1]))
nA, nB = len(hA), len(hB); BAND = 80
INF = 1e18; C = np.full((nA, 2 * BAND + 1), INF); Z = np.zeros((nA, 2 * BAND + 1), np.int8)
def j0(i): return int(round(i * (nB - 1) / (nA - 1))) - BAND
for i in range(nA):
    b = j0(i)
    for jj in range(2 * BAND + 1):
        j = b + jj
        if j < 0 or j >= nB: continue
        c = abs(hA[i] - hB[j])
        if i == 0 and j == 0: C[i, jj] = c; continue
        best, z = INF, 0
        # (i-1, j-1)
        if i > 0:
            jp = j - 1 - j0(i - 1)
            if 0 <= jp <= 2 * BAND and C[i - 1, jp] < best: best, z = C[i - 1, jp], 1
            jp = j - 2 - j0(i - 1)                                   # (i-1, j-2)
            if 0 <= jp <= 2 * BAND and C[i - 1, jp] + abs(hA[i] - hB[j - 1]) < best: best, z = C[i - 1, jp] + abs(hA[i] - hB[j - 1]), 2
        if i > 1:
            jp = j - 1 - j0(i - 2)                                   # (i-2, j-1)
            if 0 <= jp <= 2 * BAND and C[i - 2, jp] + abs(hA[i - 1] - hB[j]) < best: best, z = C[i - 2, jp] + abs(hA[i - 1] - hB[j]), 3
        if best < INF: C[i, jj] = best + c; Z[i, jj] = z
# Rückweg
i, j = nA - 1, nB - 1; pfad = [(i, j)]
while i > 0 or j > 0:
    z = Z[i, j - j0(i)]
    if z == 1: i, j = i - 1, j - 1
    elif z == 2: i, j = i - 1, j - 2
    elif z == 3: i, j = i - 2, j - 1
    else: break
    pfad.append((i, j))
pfad = np.array(pfad[::-1]); ls = s[pfad[:, 0]]; ko = kB[pfad[:, 1]]
# Steigung der Veranstalterkurve über 200 m
g = (np.interp(kB + 100, kB, hB) - np.interp(kB - 100, kB, hB)) / 200
anker = []
for k in np.arange(250, 42195, 500.0):
    if abs(np.interp(k, kB, g)) < 0.03: continue
    sel = ko == k
    if sel.any(): anker.append({"km": k / 1000, "d": float(ls[sel].mean()), "steigung": round(float(np.interp(k, kB, g)) * 100, 1)})
json.dump({"pfad": [[round(float(a), 1), float(b)] for a, b in zip(ls[::10], ko[::10])], "anker": anker}, open("form.json", "w"))
print(len(anker), "Formanker; Linie -> km (Faktor Linie):")
for a in anker: print(f"  km {a['km']:6.2f}  Linie {a['d'] / 1000:6.2f}  ({a['steigung']:+.0f} %)")
