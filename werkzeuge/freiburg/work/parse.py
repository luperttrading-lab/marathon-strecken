# Strecke aus der RaceDayMap des Veranstalters: mein-freiburgmarathon.de/lauf/marathon/ bettet app.racedaymap.com/2027-marathon ein
# (Dienst racemaps.se). Die Daten liefert https://app.racedaymap.com/api/map/2027-marathon (rdm_abruf.js bzw. curl ->
# ../dl/racedaymap/api_2027-marathon.json; die Karte „2027“ auf der Programmseite, api/map/2027, hat dieselbe Linie). Linien
# „Marathon“, „Halbmarathon“ und „Badenova Schülermarathon“ sind identisch: eine Runde (MultiLineString aus 396 Einzelpunkten,
# WGS 84, ohne Höhen; die Höhen der Karte sind ein eigenes Profil mit 216 Werten). Der Marathon läuft sie zweimal (Veranstalter:
# „2 x 21,1 km“, Zwischenzeiten 1, 5, 10, 15, 21,1, 22,1, 26,1, 31,1, 36,1 km).
# -> runde.json (Punkte [lat, lon] der Runde, laufende Länge geodätisch), rdm_marken.json (Wasser, Verpflegung, Wechselstellen, Bands)
import json
import numpy as np
from pyproj import Geod
def j(v): return json.loads(v) if isinstance(v, str) else v
d = json.load(open("../dl/racedaymap/api_2027-marathon.json"))["map"]
r = {f["properties"]["label"]: f for f in j(d["routes"])}
c = r["Marathon"]["geometry"]["coordinates"]
assert all(r[k]["geometry"]["coordinates"] == c for k in ("Halbmarathon", "Badenova Schülermarathon"))
pts = [(p[1], p[0]) for x in c for p in x]
n0 = len(pts)
pts = [p for i, p in enumerate(pts) if i == 0 or (round(p[0], 7), round(p[1], 7)) != (round(pts[i - 1][0], 7), round(pts[i - 1][1], 7))]
G = Geod(ellps="WGS84")
_, _, dd = G.inv([p[1] for p in pts[:-1]], [p[0] for p in pts[:-1]], [p[1] for p in pts[1:]], [p[0] for p in pts[1:]])
dd = np.array(dd); dist = np.r_[0, np.cumsum(dd)]
print(f"Runde: {n0} Punkte, {len(pts)} ohne doppelte, {dist[-1]:.1f} m, Abstand Median {np.median(dd):.1f} m, max {dd.max():.0f} m; geändert {d['changed']}")
print("Anfang", pts[0], "Ende", pts[-1], "Abstand Anfang–Ende", round(G.inv(pts[0][1], pts[0][0], pts[-1][1], pts[-1][0])[2], 1), "m")
json.dump({"pts": pts, "d": dist.tolist()}, open("runde.json", "w"))
m = []
for g in j(d["markers"]):
    for x in g["markers"]:
        lo, la = x["geometry"]["coordinates"][:2]
        m.append([g["label"], x["properties"].get("label", ""), la, lo, x["properties"].get("description", "")])
json.dump(m, open("rdm_marken.json", "w"), ensure_ascii=False)
from collections import Counter
print(Counter(x[0] for x in m))
d2 = json.load(open("../dl/racedaymap/api_2027.json"))["map"]
m2 = [[g["label"], x["properties"].get("label", ""), x["geometry"]["coordinates"][1], x["geometry"]["coordinates"][0]] for g in j(d2["markers"]) for x in g["markers"]]
json.dump(m2, open("rdm_marken_2027.json", "w"), ensure_ascii=False)
print("Karte 2027:", Counter(x[0] for x in m2))
