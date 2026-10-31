# Gemeinde und Ort alle 100 m (Linienmeter). Gemeinden aus swissBOUNDARIES3D (swisstopo, geo.admin.ch „find“, Ebene
# ch.swisstopo.swissboundaries3d-gemeinde-flaeche.fill, aktueller Stand, ../dl/orte/gem_*.json: St. Niklaus, Randa, Täsch, Zermatt).
# Orte aus swissNAMES3D (namen3d.py, ../dl/orte/names3d_*.json): Siedlungen („Ort“: St. Niklaus, Mattsand, Herbriggen, Breitmatten,
# Randa, Täsch, Zermatt, Riffelalp …), die die Linie berühren oder höchstens 60 m daneben liegen; ausserhalb davon der nächste Lokalname,
# See oder Bahnhalt höchstens 250 m neben der Linie (Ried, Patrullarve, Sunnegga, Leisee, Grindjesee, Grüensee, Riffelberg …). Quartierteile
# (Zermatt hat viele kleine) zählen nicht. Angezeigt: „Gemeinde, Ort“, wo der Ort anders heisst als die Gemeinde, sonst nur die Gemeinde
# (Muster: werkzeuge/luzern/work/orte.py).
# Abruf der Gemeinden (einmal):
#   curl "https://api3.geo.admin.ch/rest/services/api/MapServer/find?layer=ch.swisstopo.swissboundaries3d-gemeinde-flaeche.fill
#         &searchText=<Name>&searchField=gemname&contains=false&returnGeometry=true&geometryFormat=geojson&sr=4326" -o ../dl/orte/gem_<Name>.json
# -> orte2026.json [Linienmeter, Anzeige, Gemeinde, Ort]
import glob, json, re
import numpy as np
from matplotlib.path import Path
from pyproj import Transformer
T = Transformer.from_crs(4326, 2056, always_xy=True)
def flaechen(gm):
    for poly in (gm["coordinates"] if gm["type"] == "MultiPolygon" else [gm["coordinates"]]):
        yield Path(np.array(poly[0])[:, :2]), [Path(np.array(r)[:, :2]) for r in poly[1:]]
GEM = []
for fn in sorted(glob.glob("../dl/orte/gem_*.json")):
    for r in json.load(open(fn))["results"]:
        if not r["properties"].get("is_current_jahr"): continue
        nm = r["properties"]["gemname"]
        for A, I in flaechen(r["geometry"]):
            x, y = T.transform(A.vertices[:, 0], A.vertices[:, 1]); A2 = Path(np.c_[x, y])
            I2 = [Path(np.c_[T.transform(i.vertices[:, 0], i.vertices[:, 1])]) for i in I]
            GEM.append((nm, A2, I2))
SIED, LOK, seen = [], [], set()
def nm_(n): return re.sub(r" VS$", "", n)
for fn in sorted(glob.glob("../dl/orte/names3d_*.json")):
    for r in json.load(open(fn)):
        if r["id"] in seen: continue
        seen.add(r["id"]); p = r["properties"]; art = p.get("objektart"); gm = r["geometry"]
        if p.get("status") != "offiziell" or p.get("namen_typ") == "Exonym": continue   # „Praborgne“ (französisch für Zermatt)
        if art == "Ort":
            pts = np.vstack([np.array(poly[0])[:, :2] for poly in gm["coordinates"]])
            A = sum(abs(np.dot(np.array(poly[0])[:-1, 0], np.array(poly[0])[1:, 1]) - np.dot(np.array(poly[0])[1:, 0], np.array(poly[0])[:-1, 1])) / 2 for poly in gm["coordinates"])
            SIED.append((nm_(p["name"]), [Path(np.array(poly[0])[:, :2]) for poly in gm["coordinates"]], pts, A))
        elif art in ("Lokalname swisstopo", "See") or (art == "Haltestelle Bahn" and p["name"] in ("Sunnegga", "Riffelalp", "Riffelberg")):
            if gm["type"] == "MultiPoint": pts = np.array(gm["coordinates"])[:, :2]
            else: pts = np.vstack([np.array(poly[0])[:, :2] for poly in gm["coordinates"]])
            LOK.append((nm_(p["name"]), pts))
print(len(GEM), "Gemeindeflächen,", len(SIED), "Siedlungen,", len(LOK), "Lokalnamen, Seen und Bahnhalte")
def in_(L, x, y):
    for nm, A, I in L:
        if A.contains_point((x, y)) and not any(i.contains_point((x, y)) for i in I): return nm
    return ""
def ort(x, y):
    q = []
    for nm, polys, pts, A in SIED:
        drin = any(pp.contains_point((x, y)) for pp in polys)
        dist = 0.0 if drin else float(np.min(np.hypot(pts[:, 0] - x, pts[:, 1] - y)))
        if dist <= 60: q.append((dist, -A, nm))
    if q: return sorted(q)[0][2]                      # bei zwei Flächen die grössere
    best = min(((float(np.min(np.hypot(pts[:, 0] - x, pts[:, 1] - y))), nm) for nm, pts in LOK), default=(1e9, ""))
    return best[1] if best[0] < 250 else ""
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
out = []
for s in np.arange(0, d[-1], 100.0):
    x, y = T.transform(np.interp(s, d, P[:, 1]), np.interp(s, d, P[:, 0]))
    gm, o = in_(GEM, x, y), ort(x, y)
    out.append([float(s), gm if (not o or o == gm) else f"{gm}, {o}", gm, o])
json.dump(out, open("orte2026.json", "w"), ensure_ascii=False)
if __name__ == "__main__":
    from itertools import groupby
    from common import official
    for key, grp in groupby(out, key=lambda o: o[1]):
        grp = list(grp); print(f"km {float(official(grp[0][0])) / 1000:6.2f} {len(grp) * 100:6d} m  {key}")
