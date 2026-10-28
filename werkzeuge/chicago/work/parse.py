# Geroutete Strecke (strecke.py) zwischen Start- und Ziellinie der offiziellen Karte (marken.py) -> gpx2026.json
import json, math, numpy as np
r = json.load(open("../dl/strecke_roh.json")); P = np.array(r["ll"])
LOC = {l["name"]: l for l in json.load(open("../dl/locations.json"))}
K = math.cos(math.radians(41.88)); XY = np.c_[P[:, 1] * K * 111320, P[:, 0] * 110574]
def proj(lat, lon, lo=0, hi=None):
    q = np.array([lon * K * 111320, lat * 110574]); best = None
    for i in range(max(1, lo), hi or len(XY)):
        a, b = XY[i - 1], XY[i]; d = b - a; t = max(0, min(1, (q - a) @ d / (d @ d or 1e-9))); p = a + t * d; e = np.hypot(*(q - p))
        if best is None or e < best[0]: best = (e, i, t)
    return best
e0, i0, t0 = proj(LOC["Start"]["lat"], LOC["Start"]["lon"], 1, 200)
# Ziel: das Ende der Kartenlinie läge 487 m hinter der Marke Meile 26 (auf der Roosevelt Road), vermessen sind 352 m.
# Die Kartenlinie läuft also über die Ziellinie hinaus; das Ziel steht 352 m / 0,99 hinter Meile 26 (Faktor wie auf
# geraden Stücken), gut 180 m nördlich der Ecke Roosevelt Road / Columbus Drive.
e26, i26, t26 = proj(LOC["Mile 26"]["lat"], LOC["Mile 26"]["lon"], len(XY) - 200)
dXY = np.r_[0, np.cumsum(np.hypot(*np.diff(XY, axis=0).T))]; s_ziel = dXY[i26 - 1] + t26 * (dXY[i26] - dXY[i26 - 1]) + 352 / 0.99
i1 = int(np.searchsorted(dXY, s_ziel)); t1 = (s_ziel - dXY[i1 - 1]) / (dXY[i1] - dXY[i1 - 1]); e1 = 0.0
eZ = proj(LOC["Ziel"]["lat"], LOC["Ziel"]["lon"], len(XY) - 200); print(f"Ende der Kartenlinie {dXY[eZ[1]-1] - s_ziel:.0f} m hinter dem Ziel")
pt = lambda i, t: P[i - 1] + t * (P[i] - P[i - 1])
line = [pt(i0, t0)] + list(P[i0:i1]) + [pt(i1, t1)]
print(f"Start {e0:.1f} m neben der Strecke, Meile 26 {e26:.1f} m")
def hav(p, q):
    R = 6371008.8; la1, lo1, la2, lo2 = map(math.radians, (p[0], p[1], q[0], q[1]))
    return 2 * R * math.asin(math.sqrt(math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))
d = [0.0]
for a, b in zip(line, line[1:]): d.append(d[-1] + hav(a, b))
print("Punkte", len(line), "Länge", round(d[-1], 1), "m, also", round((d[-1] / 42195 - 1) * 100, 2), "% länger als vermessen")
json.dump({"pts": [[float(a), float(b), 0.0] for a, b in line], "d": d}, open("gpx2026.json", "w"))
