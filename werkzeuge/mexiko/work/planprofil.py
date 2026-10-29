# Höhenprofil („Altimetría“) aus dem Streckenplan 2026 des Veranstalters auslesen (Pressebild, ../dl/ruta-maraton-cdmx-2026.jpg,
# 1200 × 795 px, von media.dondeir.com) -> planprofil.json [[km, Höhe], …], nur zum Vergleich. Die Kurve ist hellgrau (Grauwert 190–230 auf 240–255). Achsen nach den Beschriftungen:
# Höhe 2291 m bei y = 711,7 px und 2228 m bei y = 760,0 px (dazwischen 2280/2270/2260/2250/2240 passen auf ±1,5 px);
# km 2,5 bei x = 343,3 px und 40 bei x = 683,3 px. Die Kurve ist eine graue Linie von gut 1 px; je Spalte das dunkelste Pixel.
import json, numpy as np
from PIL import Image
a = np.asarray(Image.open("../dl/ruta-maraton-cdmx-2026.jpg").convert("L")).astype(float)
def h_von_y(y): return 2291 + (y - 711.7) * (2228 - 2291) / (760.0 - 711.7)
def km_von_x(x): return 2.5 + (x - 343.3) * (40 - 2.5) / (683.3 - 343.3)
out = []
for x in range(319, 702):
    sp = a[705:764, x]; y = int(np.argmin(sp)) + 705
    if sp.min() > 232: continue   # keine Kurve in dieser Spalte (Gitterlinien liegen bei 240–244)
    # Teilpixel: gewichtetes Mittel um das Minimum
    lo, hi = max(705, y - 2), min(763, y + 2); w = np.clip(238 - a[lo:hi + 1, x], 0, None)
    yy = float((np.arange(lo, hi + 1) * w).sum() / w.sum()) if w.sum() else float(y)
    out.append([round(km_von_x(x), 3), round(h_von_y(yy), 1)])
json.dump(out, open("planprofil.json", "w"))
k = np.array(out)
print(len(out), "Spalten; km", k[0, 0], "bis", k[-1, 0], "; Höhe", k[:, 1].min(), "bis", k[:, 1].max())
for km in (0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 27.5, 30, 32.5, 35, 37.5, 40, 42.195):
    i = np.argmin(abs(k[:, 0] - km)); print(f"  km {km:6.3f}: {k[i, 1]:6.1f} m")
