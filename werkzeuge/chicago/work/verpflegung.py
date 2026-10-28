# 20 Verpflegungsstellen (Wasser, Gatorade, Sanität) und 2 Gel-Depots (Maurten) aus der offiziellen Karte: Symbole in der
# Vektor-PDF (orange bzw. schwarz), georeferenziert und auf die Strecke projiziert. Auf der Michigan Avenue zwischen 26th und
# 31st Street läuft man zweimal; dort liegen zwei Stellen gut 60 m neben der Linie: die an der Ecke 26th Street gehört zum
# Hinweg (Station 17), die weiter südlich zum Rückweg (Station 19, zwischen 35th Street und Roosevelt Road).
# Abgleich: Wasser-Nachfüllstellen „kurz vor Station 4, 7, 12, 16“ bei Meile 5,7 / 10,1 / 15,7 / 20,3 (Veranstalter).
import json, numpy as np
from pyproj import Transformer
from common import official
T = Transformer.from_crs(4326, 32616, always_xy=True)
coef = np.array(json.load(open("../dl/karte_affin.json")))
g = json.load(open("gpx2026.json")); P = np.array([p[:2] for p in g["pts"]]); d = np.array(g["d"]); R = np.c_[T.transform(P[:, 1], P[:, 0])]
s = np.arange(0, d[-1], 2.0); Rd = np.c_[np.interp(s, d, R[:, 0]), np.interp(s, d, R[:, 1])]
def kandidaten(x, y, rad):
    q = np.array([x, y, 1.0]) @ coef; dist = np.hypot(*(Rd - q).T); c = []
    for i in np.where(dist < rad)[0]:
        if not c or s[i] - c[-1][0] > 300: c.append([s[i], dist[i]])
        elif dist[i] < c[-1][1]: c[-1] = [s[i], dist[i]]
    return c
out = []
for x, y in json.load(open("../dl/pdf/aid_pt.json")):
    c = kandidaten(x, y, 60)
    if not c:
        c = kandidaten(x, y, 120); c = [c[0]] if y < 700 else [c[-1]]   # 26th St: Hinweg; weiter südlich: Rückweg
    out.append({"k": round(float(official(c[0][0]))), "typ": "water", "abstand": round(float(c[0][1]))})
for x, y in [(430.0, 378.0), (327.0, 540.0)]:
    c = kandidaten(x, y, 60); out.append({"k": round(float(official(c[0][0]))), "typ": "food", "abstand": round(float(c[0][1]))})
out.sort(key=lambda o: o["k"])
n = 0
for o in out:
    if o["typ"] == "water": n += 1; o["nr"] = n
    print(f"{o['k']/1000:6.2f} km  Meile {o['k']/1609.344:5.2f}  {o['typ']:5s} {o.get('nr', '')!s:3s} {o['abstand']} m neben der Linie")
json.dump(out, open("../dl/verpflegung.json", "w"))
