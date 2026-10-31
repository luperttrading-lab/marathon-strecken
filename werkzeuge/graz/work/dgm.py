# Höhen alle 10 Linienmeter der Marathonlinie (strecke2026.json) aus dem Laser-Geländemodell des BEV (ALS DTM, Höhenraster 1 m,
# Stichtag 15.09.2025, Befliegung Steiermark laut Aktualitätsübersicht 2024, CC BY 4.0) und zum Vergleich aus dem Oberflächenmodell
# (ALS DSM, gleiche Befliegung: Dächer, Bäume, Brücken). bev.py liest über HTTP-Range nur die 512-m-Teilkacheln entlang der Linie
# (Kachel ALS_D?M_CRS3035RES50000mN2650000E4700000, ../dl/bev/), bilinear. Höhen über EVRF2000 (EPSG 9274).
# -> dgm2026_10m.json [[Linienmeter, lat, lon, DTM, DSM], …]
import json, time
import numpy as np
import bev
g = json.load(open("strecke2026.json")); d = np.array(g["d"]); P = np.array(g["pts"])
ss = np.append(np.arange(0, d[-1], 10.0), d[-1])
la = np.interp(ss, d, P[:, 0]); lo = np.interp(ss, d, P[:, 1])
t0 = time.time()
dtm = bev.Modell("DTM"); dsm = bev.Modell("DSM")
h1 = dtm.hoehe(lo, la); h2 = dsm.hoehe(lo, la)
res = [[float(s), float(a), float(b), (None if np.isnan(x) else round(float(x), 3)), (None if np.isnan(y) else round(float(y), 3))]
       for s, a, b, x, y in zip(ss, la, lo, h1, h2)]
print(len(res), "Punkte,", round(time.time() - t0), "s,", dtm.geladen + dsm.geladen, "Teilkacheln neu; ohne DTM-Wert:", int(np.isnan(h1).sum()),
      " ohne DSM-Wert:", int(np.isnan(h2).sum()))
print("DTM min/max", np.nanmin(h1).round(2), np.nanmax(h1).round(2), " Start", h1[0].round(2), "Ziel", h1[-1].round(2))
print("Flugjahr an Start, Wende Süd, Wende Nord:", [bev.flugjahr(lo[i], la[i]) for i in (0, int(np.argmin(la)), int(np.argmax(la)))])
json.dump(res, open("dgm2026_10m.json", "w"))
