# Ort alle 50 m (GPX-Meter): Arrondissement bzw. Gemeinde aus ADMIN EXPRESS der IGN (WFS der Géoplateforme, Licence Ouverte;
# ../dl/arrondissement_municipal.geojson, ../dl/commune.geojson) -> orte2026.json. Ersetzt Nominatim (drosselt bei 280 Abfragen).
import json, numpy as np
from matplotlib.path import Path
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
def flaechen(f, name):
    out = []
    for ft in json.load(open(f))["features"]:
        geo = ft["geometry"]; polys = geo["coordinates"] if geo["type"] == "MultiPolygon" else [geo["coordinates"]]
        for poly in polys: out.append((name(ft["properties"]), Path(np.array(poly[0])[:, :2])))
    return out
def arr(p):
    n = p["numero_de_l_arrondissement_municipal"] if "numero_de_l_arrondissement_municipal" in p else int(p["code_insee"][-2:])
    return f"{int(n)}. Arrondissement"
F = flaechen("../dl/arrondissement_municipal.geojson", arr) + [x for x in flaechen("../dl/commune.geojson", lambda p: p["nom_officiel"]) if x[0] != "Paris"]
xy0 = F[0][1].vertices[0]; lonlat = abs(xy0[0]) < 10   # Reihenfolge der Achsen (lon, lat) prüfen
out = []
for s in np.arange(0, d[-1], 50.0):
    la, lo = np.interp(s, d, P[:, 0]), np.interp(s, d, P[:, 1]); q = (lo, la) if lonlat else (la, lo)
    hit = [n for n, pa in F if pa.contains_point(q)]
    out.append([float(s), hit[0] if hit else ""])
json.dump(out, open("orte2026.json", "w"), ensure_ascii=False)
from itertools import groupby
print([(k, len(list(v)) * 50) for k, v in groupby(o[1] for o in out)])
