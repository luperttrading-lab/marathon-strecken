# Vergleich der Höhenquellen entlang der Linie (dgm_vergleich.json aus dgm.py; „gpx“ = die in die GPX-Datei des Veranstalters
# eingebetteten Höhen, Quelle nicht angegeben; „app“ = clean.json nach der Bereinigung, falls vorhanden): Start, Ziel, Tiefst- und
# Höchstwert, Höhenmeter mit 200-m- und 1-km-Fenster, Abweichung von den GPX-Höhen, Unruhe (mittlere |2. Differenz| je 10 m),
# Höhenmeter je 5-km-Abschnitt und die Steigung auf den Stücken, die der Veranstalter in seiner Beschreibung „Kilometer für
# Kilometer“ (Seite „The course“) als bergauf oder bergab nennt.
import json, os
import numpy as np
from common import official
v = json.load(open("dgm_vergleich.json")); s = np.array(v["s"]); k = official(s)
L = 42195.0; grid = np.arange(0, L + 0.1, 10.0)
M = {m: np.interp(grid, k, np.array(v[m])) for m in ("fabdem", "cop30", "srtm", "gpx")}
if os.path.exists("clean.json"):
    c = json.load(open("clean.json")); M["app"] = np.interp(grid, np.array(c["k"]), np.array(c["h"]))
def fenster(h, w):
    at = lambda x: np.interp(x, grid, h)
    gr = np.array([(at(min(x + w / 2, L)) - at(max(x - w / 2, 0))) / (min(x + w / 2, L) - max(x - w / 2, 0)) for x in grid])
    return (gr[1:] + gr[:-1]) / 2 * 10
print(f"{'Quelle':8s} {'Start':>6s} {'Ziel':>6s} {'min':>6s} {'max':>6s} {'bei km':>6s} {'↑200':>5s} {'↓200':>5s} {'↑1km':>5s} {'gg. GPX Median':>15s} {'50%':>11s} {'r':>7s} {'Unruhe':>7s}")
for m, h in M.items():
    d2 = fenster(h, 200); d1 = fenster(h, 1000); dv = h - M["gpx"]
    print(f"{m:8s} {h[0]:6.1f} {h[-1]:6.1f} {h.min():6.1f} {h.max():6.1f} {grid[np.argmax(h)] / 1000:6.2f} {d2[d2 > 0].sum():5.0f} {-d2[d2 < 0].sum():5.0f} {d1[d1 > 0].sum():5.0f} "
          f"{np.median(dv):+15.1f} {np.percentile(dv, 25):+5.1f}/{np.percentile(dv, 75):+5.1f} {np.corrcoef(h, M['gpx'])[0, 1]:7.4f} {np.mean(np.abs(np.diff(h, 2))):7.3f}")
print("\n↑/↓ je 5 km (200-m-Fenster):")
print("km        " + "  ".join(f"{m:>11s}" for m in M))
D2 = {m: fenster(h, 200) for m, h in M.items()}
for a in range(0, 42, 5):
    b = min(a + 5, 42.195); sel = (grid[:-1] >= a * 1000) & (grid[:-1] < b * 1000)
    print(f"{a:2d}–{b:<6g} " + "  ".join(f"{D2[m][sel][D2[m][sel] > 0].sum():5.0f}/{-D2[m][sel][D2[m][sel] < 0].sum():5.0f}" for m in M))
# Stücke aus der Beschreibung des Veranstalters (offizielle km nach strassen.py), erwartete Richtung
STUECKE = [(1.04, 1.76, "Odengatan", "„pleasant downhill“", -1), (2.80, 3.22, "Kungsgatan", "„fast downhill“", -1),
           (8.27, 8.85, "Narvavägen", "„nearly 600 m, gradient about 2–3 %“", 1), (9.87, 10.20, "Sturegatan", "„uphill“", 1),
           (10.21, 11.68, "Valhallavägen", "„slopes gently downhill“", -1), (11.69, 11.95, "Oxenstiernsgatan", "„short incline“", 1),
           (11.95, 12.79, "Oxenstiernsg.–Nobelgatan", "„drops steeply downhill“", -1), (14.51, 15.21, "Manillavägen", "„long steady climb, 3 %“", 1),
           (15.21, 15.60, "Djurgårdsvägen", "„steep descent from the top of Manilla“", -1), (21.25, 21.84, "Katarinavägen", "„a full kilometre uphill, steepest at the beginning“", 1),
           (26.26, 26.55, "Lundagatan", "„tough climb … highest point of the course“", 1), (26.55, 27.00, "Lundagatan–Varvsgatan", "„equally steep descent“", -1),
           (30.85, 31.42, "Hantverkargatan", "„uphill toward Kungsholms kyrka“", 1), (31.42, 31.84, "Scheelegatan", "„continue the climb … up to the City Court“", 1),
           (33.29, 34.29, "Torsgatan", "„It’s downhill!“", -1), (39.24, 39.82, "Narvavägen", "wie km 8,3", 1), (40.85, 41.18, "Sturegatan", "„uphill stretch“", 1)]
print("\nSteigung in % auf den Stücken der Beschreibung (Mittel über das Stück, in Klammern das steilste 100-m-Stück):")
print(f"{'km':>12s} {'Stück':26s} " + " ".join(f"{m:>13s}" for m in M) + "  Beschreibung")
for a, b, n, txt, richt in STUECKE:
    aus = []
    for m, h in M.items():
        at = lambda x: np.interp(x, grid, h); g = (at(b * 1000) - at(a * 1000)) / ((b - a) * 10)
        xs = np.arange(a * 1000, b * 1000 - 99, 10.0); g100 = [(at(x + 100) - at(x)) for x in xs] if len(xs) else [0]
        st = max(g100) if richt > 0 else min(g100)
        aus.append(f"{g:+5.1f} ({st:+5.1f}){'!' if np.sign(g) != richt else ' '}")
    print(f"{a:5.2f}–{b:5.2f} {n:26s} " + " ".join(aus) + "  " + txt)
# Wo FABDEM und Copernicus (Oberflächenmodell) auf 1 m übereinstimmen, stehen weder Häuser noch Bäume: dort GPX gegen FABDEM.
f, c_ = M["fabdem"], M["cop30"]; frei = (np.abs(f - c_) < 1.0) & (f > 1.0)
dv = M["gpx"] - f
print(f"\nOffenes Gelände (FABDEM und Copernicus auf 1 m gleich, {frei.mean() * 100:.0f} % der Punkte): GPX − FABDEM Median {np.median(dv[frei]):+.1f} m, "
      f"Hälfte {np.percentile(dv[frei], 25):+.1f} bis {np.percentile(dv[frei], 75):+.1f} m; übrige Punkte Median {np.median(dv[~frei]):+.1f} m")
for a in range(0, 42, 5):
    sel = (grid >= a * 1000) & (grid < (a + 5) * 1000)
    print(f"  km {a:2d}–{a + 5:<2d}: GPX − FABDEM Median {np.median(dv[sel]):+5.1f} m (offen {np.median(dv[sel & frei]) if (sel & frei).any() else float('nan'):+5.1f} m, {(sel & frei).sum():3d} Punkte)")
