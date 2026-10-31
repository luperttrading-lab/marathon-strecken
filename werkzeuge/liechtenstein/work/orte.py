# Gemeinde und Ort alle 100 m (Linienmeter). Gemeinden aus swissBOUNDARIES3D (swisstopo, geo.admin.ch „find“, Ebene
# ch.swisstopo.swissboundaries3d-gemeinde-flaeche.fill, aktueller Stand, deckt Liechtenstein mit ab; ../dl/orte/gem_*.json: Gamprin, Eschen,
# Schaan, Vaduz, Triesenberg, Balzers, Planken, Triesen). Orte aus swissNAMES3D (namen3d.py, ../dl/orte/names3d_*.json), nur eine Auswahl
# bekannter Namen mit größtem Abstand zur Linie (ORTE unten; sonst wechselte der Name alle paar hundert Meter, swissNAMES3D hat hier fast nur
# Flurnamen). Angezeigt „Gemeinde, Ort“, wo der Ort anders heißt als die Gemeinde.
# Liechtenstein hat Exklaven in den Bergen: Valorsch, Güschgle und Sass sind Alpen der Gemeinden Schaan, Vaduz und Balzers, das Täli und die
# Pradamee in Malbun gehören zu Vaduz, Malbun selbst ist ein eigenes Stück von Triesenberg. In den Exklaven steht statt der Gemeinde der
# Talname („Valorsch, Güschgle“, „Malbun, Täli“), sonst stünde „Balzers“ mitten in den Bergen.
# Abruf der Gemeinden (einmal):
#   curl "https://api3.geo.admin.ch/rest/services/api/MapServer/find?layer=ch.swisstopo.swissboundaries3d-gemeinde-flaeche.fill
#         &searchText=<Name>&searchField=gemname&contains=false&returnGeometry=true&geometryFormat=geojson&sr=4326" -o ../dl/orte/gem_<Name>.json
# -> orte2026.json [Linienmeter, Anzeige, Gemeinde, Ort]   (Muster: werkzeuge/zermatt/work/orte.py)
import glob, json
import numpy as np
from matplotlib.path import Path
from pyproj import Transformer
T = Transformer.from_crs(4326, 2056, always_xy=True)
GEM = []
for fn in sorted(glob.glob("../dl/orte/gem_*.json")):
    for r in json.load(open(fn))["results"]:
        if not r["properties"].get("is_current_jahr"): continue
        gm = r["geometry"]; teile = []
        for poly in (gm["coordinates"] if gm["type"] == "MultiPolygon" else [gm["coordinates"]]):
            A = np.array(poly[0])[:, :2]; x, y = T.transform(A[:, 0], A[:, 1])
            teile.append((Path(np.c_[x, y]), abs(np.dot(x[:-1], y[1:]) - np.dot(x[1:], y[:-1])) / 2))
        haupt = max(a for _, a in teile)
        for p, a in teile: GEM.append((r["properties"]["gemname"], p, a == haupt))
# Ort: Name in swissNAMES3D -> (Anzeige, größter Abstand in m)
ORTE = {"Bendern": ("Bendern", 80), "Schaan": ("Schaan", 60), "Rheinpark-Stadion": ("Rheinpark-Stadion", 60), "Städtle": ("Städtle", 40),
        "Schloss Vaduz": ("Schloss", 80), "Im Frommenhaus": ("Frommenhaus", 80), "Rotenboden": ("Rotenboden", 40), "Fari": ("Fari", 60),
        "Masescha": ("Masescha", 90), "Vordersilum": ("Silum", 90), "Silum": ("Silum", 160), "Wissfläcka": ("Wissfläcka", 160),
        "Kulm": ("Kulm", 160), "Berggasthaus Sücka": ("Sücka", 160), "Sücka": ("Sücka", 160), "Steg": ("Steg", 100), "Gänglesee": ("Gänglesee", 90),
        "Vordervalorsch": ("Vordervalorsch", 160), "Valorschhötta": ("Vordervalorsch", 160), "Rietle": ("Rietle", 200), "Rietleböda": ("Rietle", 200),
        "Güschgle": ("Güschgle", 160), "Güschglehötta": ("Güschgle", 160), "Sassförkle": ("Sassförkle", 160), "Sass": ("Sass", 260),
        "Malbun": ("Malbun", 120), "Vaduzer Täli": ("Täli", 120), "Alp Pradamee": ("Pradamee", 300)}
def region(y): return "Valorsch" if y > 1220600 else "Malbun"      # Name eines Exklaven-Stücks: nördlich des Sassförkle Valorsch
L, seen = [], set()
for fn in sorted(glob.glob("../dl/orte/names3d_*.json")):
    for r in json.load(open(fn)):
        if r["id"] in seen: continue
        seen.add(r["id"]); p = r["properties"]; gm = r["geometry"]
        if p.get("name") not in ORTE or p.get("status") != "offiziell": continue
        if gm["type"] in ("MultiPoint", "Point"): pts = np.atleast_2d(np.array(gm["coordinates"]))[:, :2]; poly = []
        else:
            ringe = [gm["coordinates"]] if gm["type"] == "Polygon" else gm["coordinates"]
            pts = np.vstack([np.array(q[0])[:, :2] for q in ringe]); poly = [Path(np.array(q[0])[:, :2]) for q in ringe]
        L.append((p["name"], pts, poly))
print(len(GEM), "Gemeindeflächen,", len(L), "Namen")
def gemeinde(x, y):
    for nm, A, haupt in GEM:
        if A.contains_point((x, y)): return nm, haupt
    return "", True
def ort(x, y):
    best = (1e9, "")
    for nm, pts, poly in L:
        dist = 0.0 if any(q.contains_point((x, y)) for q in poly) else float(np.min(np.hypot(pts[:, 0] - x, pts[:, 1] - y)))
        if dist <= ORTE[nm][1] and dist < best[0]: best = (dist, ORTE[nm][0])
    return best[1]
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
out = []
for s in np.arange(0, d[-1], 100.0):
    x, y = T.transform(np.interp(s, d, P[:, 1]), np.interp(s, d, P[:, 0]))
    (gm, haupt), o = gemeinde(x, y), ort(x, y)
    vorn = gm if haupt else region(y)
    anz = vorn if (not o or o == vorn) else (o if o.startswith(vorn) else f"{vorn}, {o}")
    out.append([float(s), anz, gm, o])
json.dump(out, open("orte2026.json", "w"), ensure_ascii=False)
if __name__ == "__main__":
    from itertools import groupby
    from common import official
    for key, grp in groupby(out, key=lambda o: o[1]):
        grp = list(grp); print(f"km {float(official(grp[0][0])) / 1000:6.2f} {len(grp) * 100:6d} m  {key}   ({grp[0][2]})")
