# Bezirk alle 100 m (Linienmeter) aus den Bezirksgrenzen der Stadt Wien (Open Government Data, WFS ogdwien:BEZIRKSGRENZEOGD,
# EPSG 31256, ../dl/wfs_BEZIRKSGRENZEOGD.json). Schreibweise „2. Bezirk, Leopoldstadt“: In Wien orientiert man sich an den
# 23 Bezirken, mit Nummer und Namen (Nummer auf jedem Straßenschild und in der Postleitzahl, 1020 = 2. Bezirk).
# Läuft die Linie auf einer Bezirksgrenze (Innere Mariahilfer Straße zwischen 6. und 7. Bezirk, Landesgerichtsstraße zwischen
# 1. und 8.), liegen im Umkreis von 25 m beide Bezirke zu fast gleichen Teilen: dann beide („6./7. Bezirk, Mariahilf/Neubau“),
# sonst der Bezirk mit dem größten Anteil. -> orte2026.json
import json, numpy as np
from matplotlib.path import Path
from pyproj import Transformer
T = Transformer.from_crs(4326, 31256, always_xy=True)
def flaechen(geom):
    cs = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    return [[Path(np.array(r)[:, :2]) for r in poly] for poly in cs]
def innen(ff, x, y): return any(p[0].contains_point((x, y)) and not any(h.contains_point((x, y)) for h in p[1:]) for p in ff)
B = [(f["properties"]["BEZNR"], f["properties"]["NAMEK"], flaechen(f["geometry"])) for f in json.load(open("../dl/wfs_BEZIRKSGRENZEOGD.json"))["features"]]
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
RING = [(dx, dy) for dx in (-25, -12.5, 0, 12.5, 25) for dy in (-25, -12.5, 0, 12.5, 25) if dx * dx + dy * dy <= 625]
out = []
for s in np.arange(0, d[-1], 100.0):
    x, y = T.transform(np.interp(s, d, P[:, 1]), np.interp(s, d, P[:, 0]))
    z = {}
    for dx, dy in RING:
        for nr, n, ff in B:
            if innen(ff, x + dx, y + dy): z[(nr, n)] = z.get((nr, n), 0) + 1; break
    rang = sorted(z, key=lambda k: -z[k])
    if len(rang) > 1 and z[rang[1]] >= 4:   # Grenze: beide, nach Nummer
        (a1, n1), (a2, n2) = sorted(rang[:2]); text = f"{a1}./{a2}. Bezirk, {n1}/{n2}"
    else: text = f"{rang[0][0]}. Bezirk, {rang[0][1]}" if rang else ""
    out.append([float(s), text, {f"{a}": c for (a, b), c in z.items()}])
json.dump([o[:2] for o in out], open("orte2026.json", "w"), ensure_ascii=False)
from itertools import groupby
for k, v in groupby(out, key=lambda o: o[1]):
    v = list(v); print(f"{v[0][0]:7.0f} {len(v) * 100:5d} m  {k}   {v[0][2]}")
