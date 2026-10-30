# Vergleich der Höhenquellen entlang der Linie (offizielle km; 10-m-Raster, ohne Brückenbereinigung, Median über 30 m wie in der App):
#   RGE ALTI 1 m (IGN, gewählt), LiDAR HD MNT 50 cm (IGN), Copernicus GLO-30 (Oberflächenmodell, AWS, EGM2008),
#   OpenRunner (Höhen der Veranstalter-Karte alle 100 m, ganze Meter, Quelle unbekannt).
# Start, Ziel, min, max, ↑/↓ mit 200-m- und 1-km-Fenster, Abweichung von RGE ALTI, Unruhe (mittlere |2. Differenz| je 10 m),
# danach je 5 km ↑/↓ (200-m-Fenster).
import json, numpy as np, tifffile
from common import official
v = json.load(open("dgm_vergleich.json")); s = np.array(v["s"]); k = official(s)
L = 42195.0; grid = np.arange(0, L + 0.1, 10.0)
p = tifffile.TiffFile("../dl/dem/cop30_N45_W001.tif").pages[0]; Z = p.asarray().astype(float); S = 1 / 3600
def cop(lat, lon):   # RasterPixelIsPoint: Z[0,0] auf (46, -1)
    fy = (46.0 - np.asarray(lat)) / S; fx = (np.asarray(lon) + 1.0) / S
    i0 = np.floor(fy).astype(int); j0 = np.floor(fx).astype(int); ay = fy - i0; ax = fx - j0
    return Z[i0, j0] * (1 - ax) * (1 - ay) + Z[i0, j0 + 1] * ax * (1 - ay) + Z[i0 + 1, j0] * (1 - ax) * ay + Z[i0 + 1, j0 + 1] * ax * ay
o = json.load(open("openrunner.json")); orh = np.array(o["hoehe100"], float); ors = np.arange(len(orh)) * 100.0 * o["d"][-1] / o["laenge_or"]
def med3(h):
    m = h.copy()
    for i in range(1, len(h) - 1): m[i] = np.median(h[i - 1:i + 2])
    return m
M = {"RGE ALTI 1 m": med3(np.interp(grid, k, np.array(v["rge"], float))),
     "LiDAR HD MNT": med3(np.interp(grid, k, np.array(v["lidar"], float))),
     "Copernicus GLO-30": med3(np.interp(grid, k, cop(np.array(v["lat"]), np.array(v["lon"])))),
     "OpenRunner": np.interp(grid, official(ors), orh)}
json.dump({m: np.round(h, 2).tolist() for m, h in M.items()}, open("vergleich_10m.json", "w"))
def fenster(h, w):
    at = lambda x: np.interp(x, grid, h)
    gr = np.array([(at(min(x + w / 2, L)) - at(max(x - w / 2, 0))) / (min(x + w / 2, L) - max(x - w / 2, 0)) for x in grid])
    return (gr[1:] + gr[:-1]) / 2 * 10
ref = M["RGE ALTI 1 m"]
print(f"| Quelle | Start | Ziel | min | max | ↑/↓ 200 m | ↑/↓ 1 km | gegen RGE ALTI (Median, 95 % |Δ|) | r | Unruhe |")
print("|---|---|---|---|---|---|---|---|---|---|")
for m, h in M.items():
    d2 = fenster(h, 200); d1 = fenster(h, 1000); dv = h - ref
    print(f"| {m} | {h[0]:.1f} | {h[-1]:.1f} | {h.min():.1f} | {h.max():.1f} | {d2[d2 > 0].sum():.0f}/{-d2[d2 < 0].sum():.0f} | "
          f"{d1[d1 > 0].sum():.0f}/{-d1[d1 < 0].sum():.0f} | {np.median(dv):+.2f} / {np.percentile(np.abs(dv), 95):.2f} | {np.corrcoef(h, ref)[0, 1]:.4f} | {np.mean(np.abs(np.diff(h, 2))):.3f} |")
print("\n↑/↓ je 5 km (200-m-Fenster):")
print("| km | " + " | ".join(M) + " |")
D2 = {m: fenster(h, 200) for m, h in M.items()}
for a in range(0, 42, 5):
    b = min(a + 5, 42.195); sel = (grid[:-1] >= a * 1000) & (grid[:-1] < b * 1000)
    print(f"| {a}–{b:g} | " + " | ".join(f"{D2[m][sel][D2[m][sel] > 0].sum():.0f}/{-D2[m][sel][D2[m][sel] < 0].sum():.0f}" for m in M) + " |")
dl = M["LiDAR HD MNT"] - ref; i = np.argmax(np.abs(dl))
print(f"\nLiDAR HD − RGE ALTI: Median {np.median(dl):+.2f} m, 90 % zwischen {np.percentile(dl, 5):+.2f} und {np.percentile(dl, 95):+.2f} m, größte {dl[i]:+.1f} m bei km {grid[i]/1000:.2f}")
