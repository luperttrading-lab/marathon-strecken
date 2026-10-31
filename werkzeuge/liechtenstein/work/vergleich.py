# Nur Abgleich: Höhenmeter und Kennzahlen der Höhenquellen im selben Verfahren wie die App (offizielle km, 10-m-Raster, Median über 30 m,
# Steigung über das Messfenster): bereinigt (App), Geländemodell ohne Bereinigung, swissALTI3D 2 m mit denselben Brücken. Dazu die einfache
# Summe aller Anstiege Punkt für Punkt (10-m-Raster), wie sie GPX-Programme zeigen, und wie GPS-Uhren (Anstieg erst ab 0,5 / 1 / 3 m).
# Der Veranstalter nennt „Steigung 1870 Meter, Gefälle 720 Meter“ (Höhenprofil, Programm 2027). Muster: werkzeuge/zermatt/work/vergleich.py.
import json
import numpy as np
from common import official
v = json.load(open("dgm_vergleich.json")); c = json.load(open("clean.json"))
k = official(np.array(v["s"])); L = 42195.0; grid = np.arange(0, L + 1, 10.0)
raw = np.array(v["gel05"]); app = np.array(c["h"]); g2 = np.array(v["gel2"])
g2b = g2.copy(); ers = np.abs(app - raw) > 0.01; g2b[ers] = app[ers]          # 2 m mit denselben Brücken
def kenn(h, kk=k):
    hg = np.interp(grid, kk, h); hm = hg.copy()
    for i in range(1, len(hg) - 1): hm[i] = np.median(hg[i - 1:i + 2])
    at = lambda x: float(np.interp(x, grid, hm))
    def asc(w):
        gr = np.array([(at(min(x + w / 2, L)) - at(max(x - w / 2, 0))) / (min(x + w / 2, L) - max(x - w / 2, 0)) for x in grid])
        dh = (gr[1:] + gr[:-1]) / 2 * 10; return dh[dh > 0].sum(), -dh[dh < 0].sum()
    return hm, asc(200), asc(1000), asc(50), asc(100)
def summe(h): return float(np.clip(np.diff(h), 0, None).sum()), float(-np.clip(np.diff(h), None, 0).sum())
def uhr(h, schwelle):
    auf = ab = 0.0; ref = h[0]
    for x in h[1:]:
        if x - ref >= schwelle: auf += x - ref; ref = x
        elif ref - x >= schwelle: ab += ref - x; ref = x
    return auf, ab
ref = None
print("| Quelle | Start | Ziel | min (km) | max (km) | ↑/↓ 200 m | ↑/↓ 100 m | ↑/↓ 50 m | ↑/↓ 1 km | ↑/↓ Punkt für Punkt | gegen App (Median) |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for nm, h in (("App (swissALTI3D 0,5 m, Brücken aus swissSURFACE3D)", app), ("swissALTI3D 0,5 m ohne Bereinigung", raw),
              ("swissALTI3D 2 m, gleiche Brücken", g2b)):
    hm, a200, a1k, a50, a100 = kenn(h)
    if ref is None: ref = hm
    pp = summe(h)
    print(f"| {nm} | {hm[0]:.1f} | {hm[-1]:.1f} | {hm.min():.1f} ({grid[hm.argmin()] / 1000:.2f}) | {hm.max():.1f} ({grid[hm.argmax()] / 1000:.2f}) | "
          f"{a200[0]:.0f}/{a200[1]:.0f} | {a100[0]:.0f}/{a100[1]:.0f} | {a50[0]:.0f}/{a50[1]:.0f} | {a1k[0]:.0f}/{a1k[1]:.0f} | {pp[0]:.0f}/{pp[1]:.0f} | {np.median(hm - ref):+.2f} |")
hm = kenn(app)[0]
print("Wie GPS-Uhren (App-Höhen im 10-m-Raster):", ", ".join(f"ab {s_} m ↑ {uhr(hm, s_)[0]:.0f} / ↓ {uhr(hm, s_)[1]:.0f}" for s_ in (0.5, 1, 3, 5)))
for a in range(0, 42, 5):
    s = (grid >= a * 1000) & (grid <= min(L, (a + 5) * 1000)); x = hm[s]
    print(f"km {a:2d}–{min(42.2, a + 5):4.1f}: {x.min():.1f}–{x.max():.1f} m")
