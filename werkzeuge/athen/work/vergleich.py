# Vergleich der Höhenquellen entlang der Linie (dgm_vergleich.json aus dgm.py, Höhenbild des Veranstalters aus planprofil.py):
# Start, Ziel, Tiefst- und Höchstwert, Höhenmeter mit 200-m- und 1-km-Fenster, Abweichung vom Veranstalter, Unruhe
# (mittlere |2. Differenz| je 10 m) und Höhenmeter je 5-km-Abschnitt (200-m-Fenster, offizielle Kilometer).
import json
import numpy as np
from common import official
v = json.load(open("dgm_vergleich.json")); s = np.array(v["s"]); k = official(s)
L = 42195.0; grid = np.arange(0, L + 0.1, 10.0)
pp = np.array(json.load(open("planprofil.json")))
M = {m: np.interp(grid, k, np.array(v[m])) for m in ("fabdem", "cop30", "srtm", "strava")}
M["veranstalter"] = np.interp(grid / 1000, pp[:, 0], pp[:, 1])
def fenster(h, w):
    at = lambda x: np.interp(x, grid, h)
    gr = np.array([(at(min(x + w / 2, L)) - at(max(x - w / 2, 0))) / (min(x + w / 2, L) - max(x - w / 2, 0)) for x in grid])
    return (gr[1:] + gr[:-1]) / 2 * 10
print(f"{'Quelle':13s} {'Start':>6s} {'Ziel':>6s} {'min':>6s} {'max':>6s} {'↑200':>5s} {'↓200':>5s} {'↑1km':>5s} {'gg. Veranst. Median':>20s} {'r':>7s} {'Unruhe':>7s}")
for m, h in M.items():
    d2 = fenster(h, 200); d1 = fenster(h, 1000); dv = h - M["veranstalter"]
    print(f"{m:13s} {h[0]:6.1f} {h[-1]:6.1f} {h.min():6.1f} {h.max():6.1f} {d2[d2 > 0].sum():5.0f} {-d2[d2 < 0].sum():5.0f} {d1[d1 > 0].sum():5.0f} "
          f"{np.median(dv):+20.1f} {np.corrcoef(h, M['veranstalter'])[0, 1]:7.4f} {np.mean(np.abs(np.diff(h, 2))):7.3f}")
print("\n↑/↓ je 5 km (200-m-Fenster):")
print("km        " + "  ".join(f"{m:>12s}" for m in M))
D2 = {m: fenster(h, 200) for m, h in M.items()}
for a in range(0, 42, 5):
    b = min(a + 5, 42.195); sel = (grid[:-1] >= a * 1000) & (grid[:-1] < b * 1000)
    print(f"{a:2d}–{b:<6g} " + "  ".join(f"{D2[m][sel][D2[m][sel] > 0].sum():5.0f}/{-D2[m][sel][D2[m][sel] < 0].sum():5.0f}" for m in M))
