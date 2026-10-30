# Kilometermarken des Streckenplans auf die Linie: Die eingepasste Planlinie (plan.py) liegt stellenweise bis 200 m neben der
# Straße, ein Kreis darf daher nicht einfach auf den nächsten Linienpunkt fallen. Stattdessen werden Planlinie und Linie der
# Reihe nach einander zugeordnet (dynamic time warping, beide alle 10 m, Kosten = Abstand), und jeder Kilometerkreis wandert
# von seiner Stelle auf der Planlinie über diese Zuordnung auf die Linie. Zwischen zwei Ecken folgt die Zuordnung dem Plan
# anteilig. -> marken.json {"km": [[km, Linienmeter, Abstand Kreis–Planlinie in pt]]}
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json
import numpy as np
from pyproj import Transformer
from plan import nach_rd
T = Transformer.from_crs(4326, 28992, always_xy=True)
Z = [np.array(z) for z in json.load(open("../dl/pdf_linie.json"))["rot"]]
def finde(a, b):
    for z in Z:
        if np.hypot(*(z[0] - a)) < 3 and np.hypot(*(z[-1] - b)) < 3: return z
        if np.hypot(*(z[-1] - a)) < 3 and np.hypot(*(z[0] - b)) < 3: return z[::-1]
stuecke = [finde((123, 1006), (596, 923)), finde((580, 927), (1075, 1193)), finde((1075, 1193), (135, 1003))]
F = stuecke[0]
for z in stuecke[1:]:
    j = int(np.argmin(np.hypot(*(z - F[-1]).T))); F = np.vstack([F, z[j + 1:]])
F = F[np.r_[True, np.hypot(*np.diff(F, axis=0).T) > 0.01]]
fu = np.r_[0, np.cumsum(np.hypot(*np.diff(F, axis=0).T))]            # Planlinie in pt
G = nach_rd(F); gu = np.r_[0, np.cumsum(np.hypot(*np.diff(G, axis=0).T))]   # eingepasst in m
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); L = np.array([T.transform(p[1], p[0]) for p in g["pts"]])
# beide alle 10 m
A_u = np.arange(0, gu[-1], 10.0); A = np.c_[np.interp(A_u, gu, G[:, 0]), np.interp(A_u, gu, G[:, 1])]
B_s = np.arange(0, d[-1], 10.0); B = np.c_[np.interp(B_s, d, L[:, 0]), np.interp(B_s, d, L[:, 1])]
N, M = len(A), len(B); BAND = 400
INF = 1e18
D = np.full((N, M), INF, dtype=np.float64); W = np.zeros((N, M), dtype=np.int8)   # 0 diag, 1 oben, 2 links
for i in range(N):
    jm = int(i * M / N); j0, j1 = max(0, jm - BAND), min(M, jm + BAND)
    c = np.hypot(*(B[j0:j1] - A[i]).T)
    if i == 0:
        D[0, j0:j1] = np.cumsum(c) if j0 == 0 else INF; W[0, j0:j1] = 2; D[0, 0] = c[0]; continue
    diag = np.r_[D[i - 1, j0 - 1] if j0 > 0 else INF, D[i - 1, j0:j1 - 1]]; oben = D[i - 1, j0:j1]
    best = np.minimum(diag, oben); wahl = np.where(diag <= oben, 0, 1)
    row = c + best
    # links (i, j-1) sequentiell
    r = row.tolist(); cc = c.tolist(); wl = wahl.tolist()
    for k in range(1, len(r)):
        v = r[k - 1] + cc[k]
        if v < r[k]: r[k] = v; wl[k] = 2
    D[i, j0:j1] = r; W[i, j0:j1] = wl
# Rückweg
i, j = N - 1, M - 1; paar = [(i, j)]
while i > 0 or j > 0:
    w = W[i, j]
    if i == 0: j -= 1
    elif j == 0: i -= 1
    elif w == 0: i -= 1; j -= 1
    elif w == 1: i -= 1
    else: j -= 1
    paar.append((i, j))
paar = np.array(paar[::-1])
# je Planmeter der mittlere Linienmeter
u2s_u, u2s_s = [], []
for i in np.unique(paar[:, 0]):
    u2s_u.append(A_u[i]); u2s_s.append(B_s[paar[paar[:, 0] == i, 1]].mean())
u2s_u, u2s_s = np.array(u2s_u), np.maximum.accumulate(np.array(u2s_s))
abst = np.hypot(*(A[paar[:, 0]] - B[paar[:, 1]]).T)
print(f"Zuordnung: Abstand Plan–Linie Median {np.median(abst):.0f} m, 95 % {np.percentile(abst, 95):.0f} m, max {abst.max():.0f} m")
def plan_zu_linie(q):
    """Linienmeter für einen Punkt des Plans (pt): Stelle auf der Planlinie, dann über die Zuordnung"""
    best = None
    for k in range(len(F) - 1):
        a, b = F[k], F[k + 1]; v = b - a; t = np.clip(np.dot(q - a, v) / (np.dot(v, v) or 1), 0, 1); e = np.hypot(*(q - a - t * v))
        if best is None or e < best[0]: best = (e, k, t)
    e, k, t = best
    u = gu[k] + t * (gu[k + 1] - gu[k])
    return float(np.interp(u, u2s_u, u2s_s)), float(e)
if __name__ == "__main__":
    mk = [m for m in json.load(open("../dl/pdf_marken.json")) if m["lauf"] == "marathon" and m["kreis"]]
    out = []
    for m in sorted(mk, key=lambda m: m["km"]):
        if m["km"] >= 42: continue
        s, e = plan_zu_linie(np.array(m["kreis"])); out.append([m["km"], round(s, 1), round(e, 1)])
    out.sort()
    prev = (0, 0.0)
    for km, s, e in out:
        print(f"km {km:2d}: Linienmeter {s:7.0f}  (+{s - prev[1]:5.0f} m für {km - prev[0]} km)  Kreis {e:.1f} pt neben der Planlinie"); prev = (km, s)
    print(f"Ziel: Linienmeter {d[-1]:.0f} (+{d[-1] - prev[1]:.0f} m für 0,195 km)")
    json.dump({"km": out}, open("marken.json", "w"), indent=0)
