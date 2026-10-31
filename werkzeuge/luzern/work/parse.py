# Strecke aus der GPX-Datei des Veranstalters: Seite „Streckenpläne“ (swisscitymarathon.ch/event-guide/strecke/streckenplaene/) bettet die
# Karte von TrackMaxx ein (trackmaxx.ch/maps/?m=092b4c28-cd0c-4d0b-b4e4-965d0c5cfcbc, Bemerkung „Neue Strecke 2025“); deren Einstellungen
# (api.ashx?action=getmap, ../dl/trackmaxx/getmap.json) nennen für „42.2 km“ die Datei „scml_42km_definitiv.gpx“ (Version 12.03.2025,
# drei Tage nach der Vermessung am 09.03.2025; Track „SCML_42KM_DEFINITIV“, erstellt mit MySchweizMobil, mit Höhen; ../dl/gpx/).
# Abruf: https://tmxx-static.s3.amazonaws.com/ous/swisscitymarathon/mapstudio/gpx/scml_42km_definitiv.gpx?v=2503121124
# MySchweizMobil setzt an Zwischenpunkten doppelte, um bis 1 m versetzte Punkte (Zickzack): entfernt wie in Zürich.
# -> gpx2026.json {"pts": [[lat, lon, ele], …], "d": [laufende Länge, geodätisch GRS80]}
import json, re
import numpy as np
from pyproj import Geod, Transformer
T = Transformer.from_crs(4326, 2056, always_xy=True)       # LV95
t = open("../dl/gpx/scml_42km_definitiv.gpx", encoding="utf-8").read()
pts = [[float(a), float(b), float(e)] for a, b, e in re.findall(r'<trkpt lat="([^"]+)" lon="([^"]+)"[^>]*>\s*<ele>([^<]+)</ele>', t)]
n0 = len(pts)
x, y = T.transform([p[1] for p in pts], [p[0] for p in pts]); X = np.c_[x, y]
G = Geod(ellps="GRS80")
_, _, d0 = G.inv([p[1] for p in pts[:-1]], [p[0] for p in pts[:-1]], [p[1] for p in pts[1:]], [p[0] for p in pts[1:]])
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
_, _, dd = G.inv([p[1] for p in pts[:-1]], [p[0] for p in pts[:-1]], [p[1] for p in pts[1:]], [p[0] for p in pts[1:]])
d = np.r_[0, np.cumsum(dd)]
print(f"GPX: {n0} Punkte, {np.sum(d0):.1f} m roh; nach Entfernen der Doppelten {len(pts)} Punkte, {d[-1]:.1f} m geodätisch, Abstand Median "
      f"{np.median(dd):.0f} m, bis {np.max(dd):.0f} m; Höhe {min(p[2] for p in pts):.1f}–{max(p[2] for p in pts):.1f} m")
print("Anfang", pts[0][:2], "Ende", pts[-1][:2])
json.dump({"pts": pts, "d": d.tolist()}, open("gpx2026.json", "w"))
