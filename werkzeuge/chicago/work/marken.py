# Start, Ziel, Meilen- und 5-km-Marken aus der offiziellen Karte (Vektor-PDF): Kartenlinie und Beschriftungen über die affine
# Georeferenz (24 Ecken, Rest 15 m RMS, ../dl/karte_affin.json) in Koordinaten, dann auf die geroutete Strecke projiziert
# -> ../dl/locations.json (cat km: name, lat, lon, m = offizielle Meter)
import json, re, numpy as np
from pyproj import Transformer
TI = Transformer.from_crs(32616, 4326, always_xy=True)
coef = np.array(json.load(open("../dl/karte_affin.json")))
geo = lambda x, y: TI.transform(*(np.array([x, y, 1.0]) @ coef))[::-1]
pts = json.load(open("../dl/pdf/kurs_pt.json"))
MEILE = {1: (467.3, 403.1), 2: (454.2, 474.3), 3: (437.9, 424.5), 4: (435.9, 338.8), 5: (436.1, 254.8), 6: (421.5, 169.3), 7: (401.3, 85.3), 8: (358.9, 31.3),
         9: (383.5, 108.8), 10: (400.8, 191.9), 11: (409.1, 276.9), 12: (429.6, 349.6), 13: (402.5, 440.2), 14: (377.2, 480.1), 15: (285.6, 481.2), 16: (274.8, 491.0),
         17: (346.7, 488.7), 18: (340.7, 540.4), 19: (304.4, 591.7), 20: (372.6, 616.8), 21: (408.1, 643.4), 22: (446.6, 688.1), 23: (479.4, 762.4), 24: (490.3, 723.4),
         25: (478.5, 635.3), 26: (488.2, 552.0)}
KM = {5: (437.5, 413.8), 10: (411.7, 153.3), 15: (381.0, 145.5), 20: (429.8, 391.6), 25: (234.1, 477.3), 30: (303.4, 561.7), 35: (439.8, 677.4), 40: (477.7, 648.2)}
locs = [{"cat": "km", "name": "Start", "m": 0.0, **dict(zip(("lat", "lon"), geo(*pts[-1])))},
        {"cat": "km", "name": "Ziel", "m": 42195.0, **dict(zip(("lat", "lon"), geo(*pts[0])))}]
locs += [{"cat": "km", "name": f"Mile {k}", "m": k * 1609.344, **dict(zip(("lat", "lon"), geo(*p)))} for k, p in MEILE.items()]
locs += [{"cat": "km", "name": f"{k}K", "m": k * 1000.0, **dict(zip(("lat", "lon"), geo(*p)))} for k, p in KM.items()]
json.dump(locs, open("../dl/locations.json", "w"), indent=0)
print(len(locs), "Marken; Start", locs[0]["lat"], locs[0]["lon"], "Ziel", locs[1]["lat"], locs[1]["lon"])
