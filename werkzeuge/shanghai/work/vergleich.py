# Vergleich der Höhenquellen entlang der Linie (dgm_vergleich.json aus dgm.py; „plan“ = Höhenbild im Streckenplan 2025 des
# Veranstalters, planprofil.py, auf seiner eigenen km-Achse; „app“ = clean.json nach der Bereinigung): Start, Ziel, Tiefst- und
# Höchstwert, Höhenmeter mit 200-m- und 1-km-Fenster, Abweichung von FABDEM, Unruhe (mittlere |2. Differenz| je 10 m) und die Mittel
# je 5 km.
import json, os
import numpy as np
from common import official
v = json.load(open("dgm_vergleich.json")); s = np.array(v["s"]); k = official(s)
L = 42195.0; grid = np.arange(0, L + 0.1, 10.0)
M = {m: np.interp(grid, k, np.array(v[m])) for m in ("fabdem", "cop30", "srtm")}
pp = np.array(json.load(open("planprofil.json"))); M["plan"] = np.interp(grid, pp[:, 0] * 1000, pp[:, 1])
if os.path.exists("clean.json"):
    c = json.load(open("clean.json")); M["app"] = np.interp(grid, np.array(c["k"]), np.array(c["h"]))
    M["gelaende"] = np.interp(grid, np.array(c["k"]), np.array(c["boden"]))
def fenster(h, w):
    at = lambda x: np.interp(x, grid, h)
    gr = np.array([(at(min(x + w / 2, L)) - at(max(x - w / 2, 0))) / (min(x + w / 2, L) - max(x - w / 2, 0)) for x in grid])
    return (gr[1:] + gr[:-1]) / 2 * 10
print(f"{'Quelle':9s} {'Start':>6s} {'Ziel':>6s} {'min':>6s} {'max':>6s} {'bei km':>6s} {'↑200':>5s} {'↓200':>5s} {'↑1km':>5s} {'gg. FABDEM':>11s} {'Unruhe':>7s}")
for m, h in M.items():
    d2 = fenster(h, 200); d1 = fenster(h, 1000); dv = h - M["fabdem"]
    print(f"{m:9s} {h[0]:6.1f} {h[-1]:6.1f} {h.min():6.1f} {h.max():6.1f} {grid[np.argmax(h)] / 1000:6.2f} {d2[d2 > 0].sum():5.0f} {-d2[d2 < 0].sum():5.0f} "
          f"{d1[d1 > 0].sum():5.0f} {np.median(dv):+11.1f} {np.mean(np.abs(np.diff(h, 2))):7.3f}")
print("\nMittel je 5 km:")
print("km        " + "  ".join(f"{m:>8s}" for m in M))
for a in range(0, 42, 5):
    sel = (grid >= a * 1000) & (grid < min(a + 5, 42.195) * 1000)
    print(f"{a:2d}–{min(a + 5, 42.195):<6g} " + "  ".join(f"{np.median(M[m][sel]):8.1f}" for m in M))
