# Gemeinde und Ortschaft alle 100 m (Linienmeter). Gemeinden aus swissBOUNDARIES3D (swisstopo, geo.admin.ch „find“, Ebene
# ch.swisstopo.swissboundaries3d-gemeinde-flaeche.fill, aktueller Stand, ../dl/orte/gem_*.json), Ortschaften aus dem amtlichen
# Ortschaftenverzeichnis (swisstopo, Ebene ch.swisstopo-vd.ortschaftenverzeichnis_plz, ../dl/orte/plz_bbox.json), ohne Kantonskürzel.
# Angezeigt: die Gemeinde, und wo die Ortschaft anders heißt, „Gemeinde, Ortschaft“ (Horw, Kastanienbaum; Alpnach, Alpnachstad).
# Quartiere der Stadt Luzern gibt es als Open Data nur über map.stadtluzern.ch, das aus dieser Umgebung nicht erreichbar war: in der
# Stadt deshalb nur „Luzern“. Grenzen auf der Straße: je 40 m links und rechts nachsehen, bei zwei Gebieten „links / rechts“
# (Muster: werkzeuge/zuerich/work/orte.py). Am See liegt die Seeseite im Wasser der Gemeinde: zählt mit.
# Abruf (einmal):
#   curl "https://api3.geo.admin.ch/rest/services/api/MapServer/find?layer=ch.swisstopo.swissboundaries3d-gemeinde-flaeche.fill
#         &searchText=<Name>&searchField=gemname&contains=false&returnGeometry=true&geometryFormat=geojson&sr=4326" -o ../dl/orte/gem_<Name>.json
#   für Luzern, Horw, Hergiswil (NW), Stansstad, Alpnach;
#   curl "https://api3.geo.admin.ch/rest/services/api/MapServer/identify?geometryType=esriGeometryEnvelope&geometry=8.28,46.955,8.345,47.06
#         &imageDisplay=1000,1000,96&mapExtent=8.28,46.955,8.345,47.06&tolerance=0&layers=all:ch.swisstopo-vd.ortschaftenverzeichnis_plz
#         &returnGeometry=true&geometryFormat=geojson&sr=4326&limit=200" -o ../dl/orte/plz_bbox.json
# -> orte2026.json [Linienmeter, Name, Name in der Mitte]
import glob, json, re
import numpy as np
from matplotlib.path import Path
def flaechen(gm):
    for poly in (gm["coordinates"] if gm["type"] == "MultiPolygon" else [gm["coordinates"]]):
        yield Path(np.array(poly[0])[:, :2]), [Path(np.array(r)[:, :2]) for r in poly[1:]]
GEM, ORT = [], []
for fn in sorted(glob.glob("../dl/orte/gem_*.json")):
    for r in json.load(open(fn))["results"]:
        if not r["properties"].get("is_current_jahr"): continue
        nm = re.sub(r" \((NW|LU|OW)\)$", "", r["properties"]["gemname"])
        for A, I in flaechen(r["geometry"]): GEM.append((nm, A, I))
for r in json.load(open("../dl/orte/plz_bbox.json"))["results"]:
    nm = re.sub(r" (LU|NW|OW)$", "", r["properties"]["langtext"])
    for A, I in flaechen(r["geometry"]): ORT.append((nm, A, I))
print(len(GEM), "Gemeindeflächen,", len(ORT), "Ortschaftsflächen")
GEMNAMEN = {g[0] for g in GEM}
def in_(L, la, lo):
    for nm, A, I in L:
        if A.contains_point((lo, la)) and not any(i.contains_point((lo, la)) for i in I): return nm
    return ""
def wo(la, lo):
    g, o = in_(GEM, la, lo), in_(ORT, la, lo)
    if not g: return ""
    return g if (not o or o in GEMNAMEN) else f"{g}, {o}"       # PLZ-Gebiet einer Nachbargemeinde (6052 Hergiswil reicht nach Horw): nur Gemeinde
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
out = []
for s in np.arange(0, d[-1], 100.0):
    la, lo = np.interp(s, d, P[:, 0]), np.interp(s, d, P[:, 1])
    la2, lo2 = np.interp(min(s + 20, d[-1]), d, P[:, 0]), np.interp(min(s + 20, d[-1]), d, P[:, 1])
    la1, lo1 = np.interp(max(s - 20, 0), d, P[:, 0]), np.interp(max(s - 20, 0), d, P[:, 1])
    ex, ny = (lo2 - lo1) * np.cos(np.radians(la)), (la2 - la1); n = np.hypot(ex, ny) or 1
    qx, qy = -ny / n, ex / n                                   # nach links
    seiten = [wo(la + f * qy * 40 / 111320, lo + f * qx * 40 / (111320 * np.cos(np.radians(la)))) for f in (1, -1)]
    mitte = wo(la, lo)
    seiten = [x for x in dict.fromkeys(seiten) if x]
    out.append([float(s), " / ".join(seiten) or mitte, mitte])
json.dump(out, open("orte2026.json", "w"), ensure_ascii=False)
from itertools import groupby
from common import official
for key, grp in groupby(out, key=lambda o: o[1]):
    grp = list(grp); print(f"km {float(official(grp[0][0])) / 1000:6.2f} {len(grp) * 100:6d} m  {key}")
