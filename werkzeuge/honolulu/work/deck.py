# Fahrbahnhöhe aus der USGS-Punktwolke an den Brücken (Muster: werkzeuge/boston/work/deck.py). Das 1-m-Bodenmodell lässt Brücken
# über Wasser weg (Ala-Wai-Kanal: Wasserfläche 0,6 m) oder hat dort Lücken (Hawaiʻi Kai, Gewässer ohne Wert); kleine Brücken über
# Bäche sind meist als Durchlass mit Fahrbahn drin. Je 10-m-Punkt in Fenstern um die OSM-Brücken (bridge=yes auf der Linie,
# strassen.json, 60 m davor und danach): Laserpunkte im Umkreis von 4 m, ohne Boden (2), Wasser (9) und Rauschen (7, 18); davon das
# 10-%-Quantil (Fahrbahn; Geländer, Schilder, Fahrzeuge und Bäume liegen darüber), wenn mindestens 20 Punkte. Die Punktwolke hat
# denselben Höhenbezug wie das Modell (Bodenpunkte an drei Stellen auf 1 cm gleich, siehe UEBERGABE.md). -> deck.json
import json, math, time
import numpy as np
from common import official
from ept import query, merc
v = json.load(open("dgm_vergleich.json")); s = np.array(v["s"]); k = official(s)
la = np.array(v["lat"]); lo = np.array(v["lon"]); dem = np.array(v["lidar"], float)
st = json.load(open("strassen.json"))
n = min(len(s), len(st)); br = np.zeros(len(s), bool); br[:n] = [o[3] not in ("", "no") for o in st[:n]]
br |= np.isnan(dem)                                       # Lücken im Modell ebenfalls messen
idx = np.where(br)[0]; gr = np.split(idx, np.where(np.diff(idx) > 3)[0] + 1)
X, Y = np.array([merc(a, b) for a, b in zip(la, lo)]).T
rad = 4.0 / math.cos(math.radians(21.3))                 # 4 m in Web-Mercator-Einheiten
deck = np.full(len(s), np.nan); anz = np.zeros(len(s), int); t0 = time.time(); fenster = []
for g in gr:
    a, b = max(0, g.min() - 6), min(len(s) - 1, g.max() + 6); ii = np.arange(a, b + 1); fenster.append([int(a), int(b), int(g.min()), int(g.max())])
    P = query(X[ii].min() - rad, Y[ii].min() - rad, X[ii].max() + rad, Y[ii].max() + rad)
    P = P[~np.isin(P[:, 3].astype(int), (2, 7, 9, 18))]
    for i in ii:
        m = (P[:, 0] - X[i]) ** 2 + (P[:, 1] - Y[i]) ** 2 <= rad * rad
        anz[i] = m.sum()
        if m.sum() >= 20: deck[i] = np.percentile(P[m, 2], 10)
    print(f"km {k[g.min()] / 1000:6.2f}–{k[g.max()] / 1000:6.2f} {st[min(len(st) - 1, int(np.median(g)))][2]:24s} ({round(time.time() - t0)} s)", flush=True)
    for i in ii:
        print(f"   {k[i] / 1000:7.3f}  Modell {dem[i]:6.2f}  Fahrbahn {deck[i]:6.2f}  n {anz[i]:5d}  {'Brücke' if br[i] else ''}")
json.dump({"deck": [None if not np.isfinite(x) else round(float(x), 3) for x in deck], "n": anz.tolist(), "fenster": fenster}, open("deck.json", "w"))
