# Höhen entlang der Linie alle 10 Linienmeter aus den freien Höhenmodellen von swisstopo (swissalti.py: STAC-API von data.geo.admin.ch,
# COG-Kacheln 1 × 1 km in LV95, nur die gebrauchten Teile geladen, Zwischenspeicher ../dl/swisstopo/):
#   swissALTI3D 0,5 m (Geländemodell, jeweils neuester Jahrgang der Kachel) – Grundlage;
#   swissALTI3D 2 m – nur Vergleich. Brücken (Oberflächenmodell): deck.py.
# Dazu die Höhen der GPX-Datei (MySchweizMobil; Herkunft: swisstopo-Modell der Routenplanung) zum Vergleich.
# Höhen in m ü. M. (LN02). -> dgm2026_10m.json [[Linienmeter, lat, lon, h], …] und dgm_vergleich.json  (Muster: werkzeuge/luzern/work/dgm.py)
import json
import numpy as np
from pyproj import Transformer
from swissalti import Modell
T = Transformer.from_crs(4326, 2056, always_xy=True); TI = Transformer.from_crs(2056, 4326, always_xy=True)
g = json.load(open("gpx2026.json")); P = np.array(g["pts"]); d = np.array(g["d"])
x, y = T.transform(P[:, 1], P[:, 0]); X = np.c_[x, y]
dl = np.r_[0, np.cumsum(np.hypot(*np.diff(X, axis=0).T))]       # Länge in LV95 (auf 0,02 % wie geodätisch)
s = np.append(np.arange(0, d[-1], 10.0), d[-1])
sl = np.interp(s, d, dl)
E = np.interp(sl, dl, X[:, 0]); N = np.interp(sl, dl, X[:, 1])
lon, lat = TI.transform(E, N)
gel = Modell("swissalti3d", 0.5); gel2 = Modell("swissalti3d", 2.0)
h = gel.lv95(E, N); print("swissALTI3D 0,5 m fertig", flush=True)
h2 = gel2.lv95(E, N); print("swissALTI3D 2 m fertig", flush=True)
gpx = np.interp(s, d, P[:, 2])
for nm, v in (("swissALTI3D 0,5 m", h), ("swissALTI3D 2 m", h2), ("GPX", gpx)):
    print(f"{nm:22s}: Start {v[0]:.2f}  min {np.nanmin(v):.2f}  max {np.nanmax(v):.2f} bei Linienmeter {s[np.nanargmax(v)]:.0f}  Ziel {v[-1]:.2f}  fehlend {np.isnan(v).sum()}")
info = {"gel05": gel.kacheln_info(), "gel2": gel2.kacheln_info()}
jahre = {}
for k, v in info["gel05"].items(): jahre[v["jahr"]] = jahre.get(v["jahr"], 0) + 1
print("swissALTI3D-Kacheln nach Jahrgang:", jahre)
json.dump({"s": s.round(1).tolist(), "lat": np.round(lat, 7).tolist(), "lon": np.round(lon, 7).tolist(), "E": E.round(2).tolist(), "N": N.round(2).tolist(),
           "gel05": np.round(h, 3).tolist(), "gel2": np.round(h2, 3).tolist(), "gpx": gpx.round(2).tolist(), "kacheln": info}, open("dgm_vergleich.json", "w"))
json.dump([[float(a), float(b), float(c), float(e)] for a, b, c, e in zip(s, np.round(lat, 7), np.round(lon, 7), np.round(h, 3))],
          open("dgm2026_10m.json", "w"))
print(len(s), "Punkte")
