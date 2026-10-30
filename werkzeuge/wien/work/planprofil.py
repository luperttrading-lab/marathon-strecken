# Höhenbild des Veranstalters (vienna-marathon.com/res/img/content/course/profile.png, 2529 × 449 px, auch im Streckenplan 2026
# und 2027) ausgelesen: je Spalte das oberste Pixel der dunklen Linie (36/38/82) in der weißen Zeichenfläche. x: Zeichenfläche
# (weiß, x 223–2305 px) von Start bis Ziel = 0 bis 42,195 km (Achse 0 … 42). y: Pfeil „44 m“ vom tiefsten Punkt bis zum höchsten -> Meter je Pixel. Vergleich mit data.json.
import json, numpy as np
from PIL import Image
a = np.asarray(Image.open("../dl/profile.png").convert("RGB")).astype(int)
navy = (np.abs(a - [36, 38, 82]).sum(2) < 40); lila = (np.abs(a - [131, 122, 152]).sum(2) < 40)
weiss = np.where((a[200] == 255).all(1))[0]; x0, x1 = weiss.min(), weiss.max()
top = []
for x in range(x0, x1 + 1):
    ys = np.where(navy[150:345, x])[0]
    top.append(150 + ys.min() if len(ys) else np.nan)
top = np.array(top, float); km = (np.arange(x0, x1 + 1) - x0) / (x1 - x0) * 42.195
ok = np.isfinite(top); top = np.interp(km, km[ok], top[ok])
spanne = top.max() - top.min(); mpp = 44.0 / spanne
D = json.load(open("data.json")); h = np.array(D["h"]) / 100; g = np.arange(len(h)) * 10.0
eig = np.interp(km * 1000, g, h); plan = eig.min() + (top.max() - top) * mpp   # tiefster Punkt gleich gesetzt
print(f"Fläche x {x0}–{x1} px, Linie {spanne:.0f} px hoch -> {mpp:.3f} m/px")
print(f"Korrelation {np.corrcoef(plan, eig)[0, 1]:.3f}; Abstand (Plan − App) Median {np.median(plan - eig):+.1f} m, Hälfte zwischen "
      f"{np.percentile(plan - eig, 25):+.1f} und {np.percentile(plan - eig, 75):+.1f} m, 95 % bis {np.percentile(np.abs(plan - eig), 95):.1f} m")
for k in (0, 0.8, 2, 5, 10, 12, 15, 17.9, 20, 21, 22.7, 25, 30, 35, 38, 40, 41.5, 42.195):
    print(f"  km {k:6.2f}: Plan {np.interp(k, km, plan):6.1f}  App {np.interp(k * 1000, g, h):6.1f}")
print("höchster Punkt im Bild bei km %.1f, in der App bei km %.1f" % (km[np.argmax(plan)], g[np.argmax(h)] / 1000))
json.dump({"km": km.round(3).tolist(), "h": plan.round(2).tolist()}, open("planprofil.json", "w"))
