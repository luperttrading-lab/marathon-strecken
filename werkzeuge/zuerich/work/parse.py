# Strecke aus der GPX-Datei des Veranstalters: Seite „Marathon“ (zuerichmarathon.ch/marathon-2/marathon), Knopf „GPX Dateien“ ->
# Google Drive, Datei „zhm2025marathon.gpx“ (Track „ZHM 2025 - Marathon“, erstellt mit MySchweizMobil, 980 Punkte mit Höhen,
# ../dl/gpx/zhm2025marathon.gpx). Abruf: https://drive.usercontent.google.com/download?id=1Jx980yCBl68NO58oTrm3Ks9aWOSZWRs8&export=download
# Der Streckenplan 2026 (PDF vom 17.12.2025, ../dl/pdf/Marathon_ZHM.pdf) zeigt denselben Weg wie der Plan 2025 (PDF vom 28.11.2024,
# Streckenplan_Marathon_alt.pdf; nur Symbole der Verpflegung verschoben); die Seite für 2027 verlinkt beide Dateien weiter.
# MySchweizMobil setzt an jedem Zwischenpunkt doppelte und um 1 m versetzte Punkte (Zickzack von 0,2–1,4 m): entfernt.
# -> gpx2026.json {"pts": [[lat, lon, ele], …], "d": [laufende Länge, geodätisch GRS80]}
import json, re
import numpy as np
from pyproj import Geod, Transformer
T = Transformer.from_crs(4326, 2056, always_xy=True)       # LV95
t = open("../dl/gpx/zhm2025marathon.gpx", encoding="utf-8").read()
pts = [[float(a), float(b), float(e)] for a, b, e in re.findall(r'<trkpt lat="([^"]+)" lon="([^"]+)"[^>]*>\s*<ele>([^<]+)</ele>', t)]
n0 = len(pts)
x, y = T.transform([p[1] for p in pts], [p[0] for p in pts]); X = np.c_[x, y]
# Punkte unter 2 m zum Vorgänger weg, dann Spitzen (hin und zurück unter 3 m) weg
k = [0]
for i in range(1, len(X)):
    if np.hypot(*(X[i] - X[k[-1]])) >= 2.0: k.append(i)
if k[-1] != len(X) - 1: k[-1] = len(X) - 1
geaendert = True
while geaendert:
    geaendert = False
    for j in range(1, len(k) - 1):
        a, b, c = X[k[j - 1]], X[k[j]], X[k[j + 1]]
        if np.hypot(*(c - a)) < 3.0 and np.hypot(*(b - a)) < 3.0:
            del k[j]; geaendert = True; break
pts = [pts[i] for i in k]
G = Geod(ellps="GRS80")
_, _, dd = G.inv([p[1] for p in pts[:-1]], [p[0] for p in pts[:-1]], [p[1] for p in pts[1:]], [p[0] for p in pts[1:]])
d = np.r_[0, np.cumsum(dd)]
print(f"GPX: {n0} Punkte, nach Entfernen der Doppelten {len(pts)}; {d[-1]:.1f} m geodätisch, Abstand Median {np.median(dd):.0f} m, "
      f"bis {np.max(dd):.0f} m; Höhe {min(p[2] for p in pts):.1f}–{max(p[2] for p in pts):.1f} m")
json.dump({"pts": pts, "d": d.tolist()}, open("gpx2026.json", "w"))
