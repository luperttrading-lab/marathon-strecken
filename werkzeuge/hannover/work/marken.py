# Nur Abgleich: Kilometerpunkte der My-Maps-Karte des Veranstalters (kml_punkte.json) und des Digitalen Zwillings der Stadt
# (../dl/zwilling/Marathon_Punkte.geojson, EPSG:25832) auf die Marathonlinie projiziert: Linienmeter, Abstand zur Linie, Abstand Marke zu
# Marke. Die Linie läuft zweimal über manche Straßen (Fritz-Behrens-Allee km 13–14 und 24,7–25,7), deshalb wird jede Marke nur in einem
# Fenster um ihre Sollstelle (km × Linienlänge / 42,195) gesucht. Ergebnis: Die Punkte der Karte sind von Hand gesetzt (Abstand 736–1211
# Linienmeter), die des Zwillings gleichmäßig über dieselbe Linie verteilt (982–1021 m, Linienmeter ≈ km × 1002); beide taugen nicht
# zum Eichen, der Zwilling bestätigt nur die gleichmäßige Streckung (common.py). -> kmproj.json {km: Linienmeter} (Karte)
import json, sys
import numpy as np
from pyproj import Transformer
T = Transformer.from_crs(4326, 25832, always_xy=True)
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array(g["pts"])
X = np.array(T.transform(P[:, 1], P[:, 0])).T
dl = np.r_[0, np.cumsum(np.hypot(*np.diff(X, axis=0).T))]      # Länge in UTM 32N (für die Projektion), auf geodätisch umgerechnet
fak = d[-1] / dl[-1]
def proj(lat, lon, soll, fenster=2500):
    q = np.array(T.transform(lon, lat)); best = None
    for i in range(len(X) - 1):
        if abs(d[i] - soll) > fenster and abs(d[i + 1] - soll) > fenster: continue
        a, b = X[i], X[i + 1]; v = b - a; L = np.hypot(*v)
        t = 0 if L < 1e-9 else min(1, max(0, np.dot(q - a, v) / L ** 2))
        p = a + t * v; ab = float(np.hypot(*(q - p)))
        if best is None or ab < best[0]: best = (ab, (dl[i] + t * L) * fak)
    return best
k = json.load(open("kml_punkte.json"))["punkte"]
GL = d[-1]
out = {}
print(f"Linie {GL:.1f} m")
prev = 0
for n, la, lo in k["Km-Punkte Marathon"]:
    km = int(n); ab, s = proj(la, lo, km * GL / 42.195)
    out[km] = s
    print(f"km {km:2d}: Linienmeter {s:8.1f}  Abstand zur Linie {ab:5.1f} m  seit voriger Marke {s - prev:7.1f} m  Soll×Faktor {km * GL / 42.195:8.1f}  Diff {s - km * GL / 42.195:+6.1f}")
    prev = s
print(f"Ziel: Linienmeter {GL:.1f}, seit km 42 {GL - prev:.1f} m (Soll 195)")
json.dump(out, open("kmproj.json", "w"))
mp = json.load(open("../dl/zwilling/Marathon_Punkte.geojson"))
R = Transformer.from_crs(25832, 4326, always_xy=True); prev = 0
print("Digitaler Zwilling:")
for f in mp["features"]:
    n = f["properties"]["Name"]; x, y = f["geometry"]["coordinates"][:2]; lo, la = R.transform(x, y)
    ab, s_ = proj(la, lo, (21.0975 if n == "HM" else int(n)) * GL / 42.195)
    print(f"  {n:>3}: Linienmeter {s_:8.1f}  Abstand {ab:5.1f} m  seit vorher {s_ - prev:7.1f} m"); prev = s_
