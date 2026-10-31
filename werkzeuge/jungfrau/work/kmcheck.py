# Nur Abgleich: Kilometer der App (gleichmäßig über die vermessene Linie, common.py) gegen die Kilometerangaben des Veranstalters an Orten,
# die in OSM als Punkt stehen (../dl/osm_netz.json „punkte“): Durchlaufzeiten der Race-Info 2026 und Wettkampfverpflegung 2026.
import json, numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
from common import official
T = Transformer.from_crs(4326, 2056, always_xy=True)
o = json.load(open("../dl/osm_netz.json")); g = json.load(open("gpx2026.json")); d = np.array(g["d"]); Q = np.array([p[:2] for p in g["pts"]])
ss = np.arange(0, d[-1], 2.0); x, y = T.transform(np.interp(ss, d, Q[:, 1]), np.interp(ss, d, Q[:, 0])); bt = cKDTree(np.c_[x, y])
# (km laut Veranstalter, Quelle, OSM-Name, Zusatzbedingung an die Tags)
SOLL = [(2.4, "Race-Info: Bahnhof Interlaken West", "Interlaken West", "railway"), (10.4, "Race-Info: Wilderswil Kirche Gsteig", "Gsteig", "place"),
        (11.7, "Race-Info: Gsteigwiler Dorfzentrum", "Gsteigwiler", "place"), (15.1, "Race-Info: Zweilütschinen Bahnhof", "Zweilütschinen", "railway"),
        (20.2, "Race-Info: Lauterbrunnen Bahnhof", "Lauterbrunnen", "railway"), (21.1, "Race-Info: Staubbach (Halbmarathon)", "Staubbach", "place"),
        (25.9, "Race-Info: Stocki", "Stocki", "place"), (25.7, "Verpflegung: Lauterbrunnen, «Stocki»", "Stocki", "place"),
        (28.8, "Race-Info: Wengen Station Wengwald", "Wengwald", "railway"), (30.7, "Race-Info: Zentrum Wengen", "Wengen", "railway"),
        (36.3, "Verpflegung: Mettla", "Mettla", "place"), (38.9, "Verpflegung: Wixi", "Wengernalp Wixi", "public_transport"),
        (40.3, "Verpflegung: Haaregg", "Haaregg", "natural")]
for km, quelle, nm, tag in SOLL:
    best = None
    for tg, (la, lo) in o["punkte"].values():
        if tg.get("name") != nm or tag not in tg: continue
        dist, i = bt.query(T.transform(lo, la))
        if best is None or dist < best[0]: best = (dist, float(official(ss[i])) / 1000)
    if best: print(f"{quelle:42s} km {km:5.1f}   App km {best[1]:6.2f} ({best[1] - km:+.2f})   Punkt {best[0]:4.0f} m neben der Linie")
    else: print(f"{quelle:42s} km {km:5.1f}   nicht in OSM gefunden")
