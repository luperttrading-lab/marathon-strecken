# Nur Abgleich: Höhenbild „Honolulu Marathon Elevation Profile“ im Streckenplan 2026 des Veranstalters (../dl/pdf/2026-HM-Course-Map.pdf,
# Stand 02.10.2026; Angaben im Bild: „Elevation start 14 ft, max 132 ft, gain 641 ft“) gegen das App-Profil (clean.json).
# Das PDF wird mit  pdftoppm -r 120 -png 2026-HM-Course-Map.pdf map_hi  zu ../dl/pdf/map_hi-1.png (11 520 × 5760 px); das Bild liegt
# unten rechts. Achsen aus den weißen Gitterlinien (senkrecht alle 2 mi, waagrecht alle 50 ft), je Spalte die Oberkante der roten Fläche.
# -> planprofil.json {"m": [offizielle Meter], "h": [m]}
import json
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
im = Image.open("../dl/pdf/map_hi-1.png").convert("RGB"); W, H = im.size
x0, y0 = int(W * 0.66), int(H * 0.76)
A = np.asarray(im.crop((x0, y0, int(W * 0.9), int(H * 0.96)))).astype(int)
ys, xs = slice(193, 512), slice(207, 2710)
weiss = A[ys, xs].min(axis=2) > 215
sp = np.where(weiss.mean(axis=0) > 0.5)[0] + xs.start; ze = np.where(weiss.mean(axis=1) > 0.5)[0] + ys.start
# Gitter zusammenfassen (Linien sind 1–2 px breit)
def mitten(v): return [float(np.mean(g)) for g in np.split(v, np.where(np.diff(v) > 3)[0] + 1)]
sp, ze = mitten(sp), mitten(ze)
mi = np.array(sp[:14]); fx = np.polyfit(mi, np.arange(0, 28, 2)[:len(mi)], 1)     # 0, 2, …, 26 mi
ft = np.array(ze[:4]); fy = np.polyfit(ft, [150, 100, 50, 0], 1)
print("Gitter senkrecht", [round(x) for x in sp], "waagrecht", [round(y) for y in ze])
print(f"  {1 / fx[0]:.1f} px je Meile, {-1 / fy[0]:.2f} px je Fuß")
rot = (A[:, :, 0] > 200) & (A[:, :, 1] < 90) & (A[:, :, 2] < 90)
xe = int(round(np.polyval(np.polyfit(np.arange(0, 28, 2)[:len(mi)], mi, 1), 26.2188)))
m, h = [], []
for x in range(int(round(mi[0])), xe + 1):
    r = np.where(rot[193:512, x])[0]
    if len(r) == 0: continue
    m.append(np.polyval(fx, x) * 1609.344); h.append(np.polyval(fy, r[0] + 193) * 0.3048)
m, h = np.array(m), np.array(h)
json.dump({"m": m.round(1).tolist(), "h": h.round(2).tolist()}, open("planprofil.json", "w"))
print(f"Bild: {len(m)} Spalten, Start {h[0]:.1f} m, max {h.max():.1f} m bei km {m[np.argmax(h)] / 1000:.2f}, Ende bei km {m[-1] / 1000:.2f}")
c = json.load(open("clean.json")); k = np.array(c["k"]); hc = np.array(c["h"])
L = 42195.0; grid = np.arange(0, L, 50.0)
# Das Bild ist geglättet und in der Länge eigen: beste Verschiebung und Streckung suchen
best = None
for fak in np.arange(0.97, 1.031, 0.005):
    for ver in range(-600, 601, 50):
        b = np.interp(grid, m * fak + ver, h, left=np.nan, right=np.nan); a = np.interp(grid, k, hc); ok = np.isfinite(b)
        r = np.corrcoef(a[ok], b[ok])[0, 1]
        if best is None or r > best[0]: best = (r, fak, ver)
r, fak, ver = best
b = np.interp(grid, m * fak + ver, h, left=np.nan, right=np.nan); a = np.interp(grid, k, hc); ok = np.isfinite(b); dv = (b - a)[ok]
b0 = np.interp(grid, m, h, left=np.nan, right=np.nan); ok0 = np.isfinite(b0)
print(f"ohne Verschiebung: r = {np.corrcoef(a[ok0], b0[ok0])[0, 1]:.3f}; beste: r = {r:.3f} bei Faktor {fak:.3f}, Verschiebung {ver:+d} m")
print(f"Bild minus App: Median {np.median(dv):+.1f} m, Hälfte {np.percentile(dv, 25):+.1f} bis {np.percentile(dv, 75):+.1f} m, 95 % innerhalb "
      f"{np.percentile(np.abs(dv), 95):.1f} m")
for name, (p, q) in {"Diamond Head hin": (11000, 17000), "Diamond Head zurück": (37000, 42195)}.items():
    s1 = (grid >= p) & (grid < q) & ok
    print(f"  {name}: Bild max {b[s1].max():.1f} m bei km {grid[s1][np.argmax(b[s1])] / 1000:.2f}, App max {a[s1].max():.1f} m bei km {grid[s1][np.argmax(a[s1])] / 1000:.2f}")
