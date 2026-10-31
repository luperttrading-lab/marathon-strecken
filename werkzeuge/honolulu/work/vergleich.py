# Vergleich der Höhenquellen entlang der Linie: USGS-Laser-Modell 1 m („lidar“, dgm.py), Höhen der Strava-Linie („strava“, Stravas
# Modell), App-Profil nach der Bereinigung („app“, clean.json) und das Höhenbild des Veranstalters im Streckenplan („plan“,
# planprofil.json). Start, Ziel, Tiefst- und Höchstwert, Höhenmeter mit 200-m- und 1-km-Fenster, Abweichung von der App,
# Korrelation, Unruhe (mittlere |2. Differenz| je 10 m, beim Plan je 50 m) und Höhenmeter je 5 km.
import json
import numpy as np
from common import official
v = json.load(open("dgm_vergleich.json")); s = np.array(v["s"]); k = official(s)
L = 42195.0; grid = np.arange(0, L + 0.1, 10.0)
def auf(x, y):
    ok = np.isfinite(y); return np.interp(grid, x[ok], y[ok])
M = {"lidar": auf(k, np.array(v["lidar"], float)), "strava": auf(k, np.array(v["strava"]))}
c = json.load(open("clean.json")); M["app"] = auf(np.array(c["k"]), np.array(c["h"]))
p = json.load(open("planprofil.json")); M["plan"] = auf(np.array(p["m"]), np.array(p["h"]))
def fenster(h, w):
    at = lambda x: np.interp(x, grid, h)
    gr = np.array([(at(min(x + w / 2, L)) - at(max(x - w / 2, 0))) / (min(x + w / 2, L) - max(x - w / 2, 0)) for x in grid])
    return (gr[1:] + gr[:-1]) / 2 * 10
print(f"{'Quelle':7s} {'Start':>6s} {'Ziel':>6s} {'min':>6s} {'max':>6s} {'bei km':>6s} {'↑200':>5s} {'↓200':>5s} {'↑1km':>5s} {'gg. App':>8s} {'50 %':>11s} {'r':>6s} {'Unruhe':>7s}")
for m, h in M.items():
    d2 = fenster(h, 200); d1 = fenster(h, 1000); dv = h - M["app"]
    un = np.mean(np.abs(np.diff(h[::5], 2))) if m == "plan" else np.mean(np.abs(np.diff(h, 2)))
    print(f"{m:7s} {h[0]:6.1f} {h[-1]:6.1f} {h.min():6.1f} {h.max():6.1f} {grid[np.argmax(h)] / 1000:6.2f} {d2[d2 > 0].sum():5.0f} {-d2[d2 < 0].sum():5.0f} "
          f"{d1[d1 > 0].sum():5.0f} {np.median(dv):+8.1f} {np.percentile(dv, 25):+5.1f}/{np.percentile(dv, 75):+5.1f} {np.corrcoef(h, M['app'])[0, 1]:6.3f} {un:7.3f}")
print("\n↑/↓ je 5 km (200-m-Fenster):")
print("km        " + "  ".join(f"{m:>11s}" for m in M))
D2 = {m: fenster(h, 200) for m, h in M.items()}
for a in range(0, 42, 5):
    b = min(a + 5, 42.195); sel = (grid[:-1] >= a * 1000) & (grid[:-1] < b * 1000)
    print(f"{a:2d}–{b:<6g} " + "  ".join(f"{D2[m][sel][D2[m][sel] > 0].sum():5.0f}/{-D2[m][sel][D2[m][sel] < 0].sum():5.0f}" for m in M))
