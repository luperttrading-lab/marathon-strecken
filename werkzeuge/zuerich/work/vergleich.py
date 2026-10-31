# Nur Abgleich: Höhenmeter und Kennzahlen der Höhenquellen im selben Verfahren wie die App (offizielle km, 10-m-Raster, Median über 30 m,
# Steigung über das Messfenster): bereinigt (App), Geländemodell ohne Brücken, swissALTI3D 2 m mit denselben Brücken, GPX-Höhen
# (MySchweizMobil). Dazu das Höhenbild im Streckenplan (Text: „sehr flache Strecke“; Bild 400–450 m-Achse, ohne Zahlen).
import json
import numpy as np
from common import official
v = json.load(open("dgm_vergleich.json")); c = json.load(open("clean.json"))
k = official(np.array(v["s"])); L = 42195.0; grid = np.arange(0, L + 1, 10.0)
raw = np.array(v["gel05"]); app = np.array(c["h"]); gpx = np.array(v["gpx"]); g2 = np.array(v["gel2"])
g2b = g2.copy(); ers = np.abs(app - raw) > 0.01; g2b[ers] = app[ers]          # 2 m mit denselben Brücken
def kenn(h):
    hg = np.interp(grid, k, h); hm = hg.copy()
    for i in range(1, len(hg) - 1): hm[i] = np.median(hg[i - 1:i + 2])
    at = lambda x: float(np.interp(x, grid, hm))
    def asc(w):
        gr = np.array([(at(min(x + w / 2, L)) - at(max(x - w / 2, 0))) / (min(x + w / 2, L) - max(x - w / 2, 0)) for x in grid])
        dh = (gr[1:] + gr[:-1]) / 2 * 10; return dh[dh > 0].sum(), -dh[dh < 0].sum()
    return hm, asc(200), asc(1000)[0], asc(50)[0]
ref = None
print("| Quelle | Start | Ziel | min (km) | max (km) | ↑/↓ 200 m | ↑ 50 m | ↑ 1 km | gegen App (Median) | r |")
print("|---|---|---|---|---|---|---|---|---|---|")
for nm, h in (("App (swissALTI3D 0,5 m, Brücken aus swissSURFACE3D)", app), ("swissALTI3D 0,5 m ohne Brücken", raw),
              ("swissALTI3D 2 m, gleiche Brücken", g2b), ("GPX-Höhen (MySchweizMobil)", gpx)):
    hm, (u, d), u1k, u50 = kenn(h)
    if ref is None: ref = hm
    print(f"| {nm} | {hm[0]:.1f} | {hm[-1]:.1f} | {hm.min():.1f} ({grid[hm.argmin()] / 1000:.2f}) | {hm.max():.1f} ({grid[hm.argmax()] / 1000:.2f}) | "
          f"{u:.0f}/{d:.0f} | {u50:.0f} | {u1k:.0f} | {np.median(hm - ref):+.2f} | {np.corrcoef(hm, ref)[0, 1]:.3f} |")
# je 5 km
hm = kenn(app)[0]
for a in range(0, 42, 5):
    s = (grid >= a * 1000) & (grid <= min(L, (a + 5) * 1000)); x = hm[s]
    print(f"km {a:2d}–{min(42.2, a + 5):4.1f}: {x.min():.1f}–{x.max():.1f} m")
