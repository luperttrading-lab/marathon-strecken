# Gegenproben des Höhenmodells (TINITALY/1.1, dgm_tinitaly.json, und des Profils der App):
# 1. Höhenlinien der Regione Lazio (DBGT 2014, 1:5000, 5 m Abstand, ../dl/curve_livello.json aus curve.py): an jeder Stelle, an der
#    die Linie eine Höhenlinie kreuzt, die Höhe der Höhenlinie gegen TINITALY. Die Höhenlinien sind photogrammetrisch erfasst und
#    unabhängig von den älteren Quellen, aus denen TINITALY gerechnet ist; in der bebauten Stadt sind sie lückenhaft.
# 2. Höhenbild des Veranstalters (planprofil.json aus planprofil.py) gegen TINITALY je km (geeicht).
# 3. dasselbe gegen das Profil der App (data.json, nach angleich.py, clean.py und build.py).
# -> vergleich.json; Ausgabe mit Mittel und Streuung
import json, sys, numpy as np
from pyproj import Transformer
from common import official
T33 = Transformer.from_crs(4326, 32633, always_xy=True); T25833 = Transformer.from_crs(4326, 25833, always_xy=True)
r = json.load(open("dgm_tinitaly.json")); s = np.array([x[0] for x in r]); h = np.array([x[3] for x in r], float); k = official(s)
X = np.c_[T25833.transform([x[2] for x in r], [x[1] for x in r])]
C = json.load(open("../dl/curve_livello.json"))
kreuz = []
def schnitt(p1, p2, q1, q2):
    d1 = p2 - p1; d2 = q2 - q1; den = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(den) < 1e-9: return None
    t = ((q1[0] - p1[0]) * d2[1] - (q1[1] - p1[1]) * d2[0]) / den; u = ((q1[0] - p1[0]) * d1[1] - (q1[1] - p1[1]) * d1[0]) / den
    return t if 0 <= t <= 1 and 0 <= u <= 1 else None
x0, y0 = X.min(0) - 50; x1, y1 = X.max(0) + 50
for f in C["features"]:
    z = f["properties"]["cv_liv_q"]; g = f["geometry"]
    for line in (g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]):
        L = np.array([c[:2] for c in line])
        if L[:, 0].max() < x0 or L[:, 0].min() > x1 or L[:, 1].max() < y0 or L[:, 1].min() > y1: continue
        for a, b in zip(L[:-1], L[1:]):
            lo, hi = np.minimum(a, b) - 10, np.maximum(a, b) + 10
            near = np.where((X[:-1, 0] >= lo[0]) & (X[:-1, 0] <= hi[0]) & (X[:-1, 1] >= lo[1]) & (X[:-1, 1] <= hi[1]))[0]
            for i in near:
                t = schnitt(X[i], X[i + 1], a, b)
                if t is not None: kreuz.append([float(k[i] + t * (k[i + 1] - k[i])), float(z), float(h[i] + t * (h[i + 1] - h[i]))])
kreuz.sort()
dz = np.array([c[2] - c[1] for c in kreuz])
print(f"Höhenlinien gekreuzt: {len(kreuz)}; TINITALY minus Höhenlinie: Mittel {dz.mean():+.2f} m, Median {np.median(dz):+.2f}, Streuung {dz.std():.2f}, "
      f"Betrag 90 % {np.percentile(abs(dz), 90):.2f} m, größte {dz[np.argmax(abs(dz))]:+.2f} m")
for c in kreuz: print(f"  km {c[0] / 1000:6.2f}  Höhenlinie {c[1]:5.1f}  TINITALY {c[2]:5.1f}  {c[2] - c[1]:+5.1f}") if "-v" in sys.argv else None
pp = json.load(open("planprofil.json"))
pk = np.array([p[0] for p in pp]); ph = np.array([p[1] for p in pp])
hk = np.interp(pk * 1000, k, h)
print("Höhenbild des Veranstalters minus TINITALY je 5 km:")
for a in range(0, 45, 5):
    sel = (pk >= a) & (pk < a + 5)
    if sel.any(): print(f"  km {a:2d}–{min(a + 5, 42.2):4.1f}: Plan {ph[sel].mean():5.1f} m, TINITALY {hk[sel].mean():5.1f} m, Unterschied {np.mean(ph[sel] - hk[sel]):+5.1f} m")
print(f"  Korrelation über die ganze Strecke: {np.corrcoef(ph, hk)[0, 1]:.2f}")
json.dump({"kreuzungen": kreuz, "plan": [[float(a), float(b), round(float(c), 2)] for a, b, c in zip(pk, ph, hk)]}, open("vergleich.json", "w"))
D = json.load(open("data.json")); hd = np.array(D["h"]) / 100; gd = np.arange(len(hd)) * 10.0
ha = np.interp(pk * 1000, gd, hd); dd = ph - ha
print(f"Höhenbild des Veranstalters minus Profil der App: Median {np.median(dd):+.1f} m (Hälfte zwischen {np.percentile(dd, 25):+.1f} und {np.percentile(dd, 75):+.1f}), "
      f"Korrelation {np.corrcoef(ph, ha)[0, 1]:.2f}")
