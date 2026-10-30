# Vergleich der Höhenmodelle entlang der Linie (Caches von dgm.py): AMB 25 cm (LiDAR 2022, genommen), ICGC Katalonien 50 cm und 1 m
# (LiDAR 2021–2023) und IGN MDT02 (PNOA-LiDAR, zweite Abdeckung). Je Modell gegen AMB 25 cm: Abstand (Median, Streuung, 95 %),
# Unruhe von Punkt zu Punkt (Mittel der |2. Differenz| je 10 m), Rohdaten bergauf auf gemeinsamen Stücken. Brücken (clean.json)
# zählen nicht.
import json, os, numpy as np
from pyproj import Transformer
from common import official
T = Transformer.from_crs(4326, 25831, always_xy=True)
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
ss = np.append(np.arange(0, d[-1], 10.0), d[-1]); la = np.interp(ss, d, P[:, 0]); lo = np.interp(ss, d, P[:, 1])
x, y = T.transform(lo, la); keys = [f"{a:.2f},{b:.2f}" for a, b in zip(x, y)]
k = official(ss)
reg = json.load(open("clean.json"))["regions"]
frei = np.ones(len(ss), bool)
for r in reg: frei &= ~((k >= r["a"] - 20) & (k <= r["b"] + 20))
def lade(q):
    f = f"../dl/dgm_{q}_cache.json"
    if not os.path.exists(f): return None
    c = json.load(open(f)); return np.array([c.get(kk) if isinstance(c.get(kk), (int, float)) else np.nan for kk in keys], float)
ref = lade("amb25")
for q, txt in (("icgc50", "ICGC 50 cm 2021–2023"), ("icgc1", "ICGC 1 m 2021–2023"), ("ign2", "IGN MDT02 (PNOA 2. Abdeckung)")):
    v = lade(q)
    if v is None: print(q, "fehlt"); continue
    m = np.isfinite(v) & np.isfinite(ref) & frei
    if m.sum() < 100: print(q, "zu wenige Punkte", m.sum()); continue
    dd = v[m] - ref[m]
    # Unruhe nur auf Dreiergruppen, die ganz vorhanden sind
    m3 = m[:-2] & m[1:-1] & m[2:]
    un = lambda a: np.nanmean(np.abs(a[:-2][m3] - 2 * a[1:-1][m3] + a[2:][m3]))
    # Rohdaten bergauf auf zusammenhängenden Stücken
    m2 = m[:-1] & m[1:]
    up = lambda a: np.clip(np.diff(a)[m2], 0, None).sum()
    print(f"{txt:32s} {m.sum():5d} Punkte (bis km {k[m].max()/1000:4.1f}): Abstand Median {np.median(dd):+.2f} m, Streuung {np.std(dd):.2f} m, "
          f"95 % |Abstand| {np.percentile(np.abs(dd), 95):.2f} m; Unruhe {un(v):.3f} m (AMB 25 cm {un(ref):.3f} m); "
          f"↑ roh {up(v):.0f} m (AMB 25 cm {up(ref):.0f} m)")
    gross = np.where(m & (np.abs(np.nan_to_num(v - ref)) > 1.0))[0]
    if len(gross): print("   über 1 m Unterschied bei km:", sorted({round(float(k[i]) / 1000, 1) for i in gross})[:40])
