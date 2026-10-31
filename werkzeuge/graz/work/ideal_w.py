# Bandbreite w der Ideallinie, bei der die Runde der Garmin-Strecke (runde.json, parse.py) samt Übergang zum Start 21 097,5 m misst
# (Halbmarathon = eine Runde). Nur Abgleich und Grundlage für common.py: schreibt ideal_w.json {w: Länge} und je w die Zuordnung
# Linienmeter -> Meter auf der Ideallinie (ideal_<w>.json). Kopie von werkzeuge/freiburg/work/ideal_w.py, aber stückweise: Die Spitzen
# der Wenden Süd und Nord bleiben fest (ideal.py hält Anfang und Ende jedes Stücks fest), sonst zöge die Schnur die Wende Nord, wo Hin-
# und Rückweg auf derselben Linie liegen, bis zu 80 m zurück.
import json, sys, time
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
from ideal import ideal, laenge, dicht
T = Transformer.from_crs(4326, 25833, always_xy=True)   # UTM 33N (Graz 15,4° Ost)
g = json.load(open("runde.json")); Q = np.array(g["pts"]); d = np.array(g["d"])
E, N = T.transform(Q[:, 1], Q[:, 0]); X = np.c_[E, N]
du = np.r_[0, np.cumsum(np.hypot(*np.diff(X, axis=0).T))]
grenzen = [0] + sorted(g["wende"]) + [len(X) - 1]
erg = {}
for w in [float(x) for x in sys.argv[1:]]:
    t = time.time(); lm_all, ia_all, off = [], [], 0.0
    for a, b in zip(grenzen[:-1], grenzen[1:]):
        Xs = X[a:b + 1]; P, s0 = ideal(Xs, w, schritt=2.0, iter=2500)
        # Zuordnung: jeder Punkt der Ideallinie -> nächster Punkt der Ausgangslinie (im Fenster), monoton
        F, sf = dicht(Xs, 0.5); bb = cKDTree(F); dd, j = bb.query(P, k=40)
        ok = np.abs(sf[j] - s0[:, None]) < 80; dd = np.where(ok, dd, np.inf); m = np.argmin(dd, axis=1)
        lm = np.maximum.accumulate(sf[j[np.arange(len(P)), m]]); lm[0] = 0; lm[-1] = sf[-1]
        ia = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
        lm_all.append(lm + du[a]); ia_all.append(ia + off); off += ia[-1]
    lm = np.concatenate(lm_all); ia = np.concatenate(ia_all)
    erg[w] = float(ia[-1]); print(f"w = {w} m: Runde {erg[w]:.1f} m (Linie {du[-1]:.1f} m UTM; {time.time() - t:.0f} s)", flush=True)
    json.dump({"w": w, "lm": np.interp(lm, du, d).round(2).tolist(), "ideal": ia.round(2).tolist()}, open(f"ideal_{w:g}.json", "w"))
alt = json.load(open("ideal_w.json")) if len(sys.argv) > 1 and __import__("os").path.exists("ideal_w.json") else {}
alt.update({str(k): v for k, v in erg.items()}); json.dump(alt, open("ideal_w.json", "w"))
