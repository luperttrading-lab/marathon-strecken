# Quartier bzw. Gemeinde alle 100 m (Linienmeter). In der Stadt die 34 statistischen Quartiere mit ihrem Kreis (Stadt Zürich, Open Data:
# WFS „Statistische_Quartiere“, Ebene adm_statistische_quartiere_map, ../dl/orte/quartiere.json), angezeigt wie Wien „Kreis 8, Seefeld“.
# Außerhalb der Stadt die Gemeinden aus swissBOUNDARIES3D (swisstopo, geo.admin.ch „find“, Ebene
# ch.swisstopo.swissboundaries3d-gemeinde-flaeche.fill, aktueller Stand, ../dl/orte/gem_*.json), ohne den Zusatz „(ZH)“.
# Manche Straßen sind selbst die Grenze (Dufourstrasse/Falkenstrasse: Seefeld / Altstadt): je 40 m links und rechts nachsehen, bei zwei Quartieren
# „links / rechts“ (Muster: werkzeuge/honolulu/work/orte.py). Am See liegt die Seeseite oft im Wasser der Gemeinde: zählt mit.
# Abruf (einmal):
#   curl "https://www.ogd.stadt-zuerich.ch/wfs/geoportal/Statistische_Quartiere?service=WFS&version=1.1.0&request=GetFeature
#         &outputFormat=GeoJSON&typename=adm_statistische_quartiere_map" -o ../dl/orte/quartiere.json
#   curl "https://api3.geo.admin.ch/rest/services/api/MapServer/find?layer=ch.swisstopo.swissboundaries3d-gemeinde-flaeche.fill
#         &searchText=<Name>&searchField=gemname&contains=false&returnGeometry=true&geometryFormat=geojson&sr=4326" -o ../dl/orte/gem_<Name>.json
#   für Zollikon, Küsnacht (ZH), Erlenbach (ZH), Herrliberg, Meilen
# -> orte2026.json [Linienmeter, Name, Name in der Mitte]
import glob, json
import numpy as np
from matplotlib.path import Path
# Kreis 1 heißt als Ganzes „Altstadt“ (Stadt Zürich; OSM admin_level 9). Seine vier Quartiere (Rathaus, Hochschulen, Lindenhof, City)
# treffen sich genau an Quaibrücke, Bürkliplatz und Bellevue, wo die Strecke fünfmal durchkommt; quartiersgenau wechselte die Anzeige dort
# alle 100 m. Deshalb in Kreis 1 nur „Kreis 1, Altstadt“, in Kreis 2 und 8 das Quartier (Enge, Seefeld).
FL = []          # (Kreis oder None, Name, Außenring, Löcher)
for f in json.load(open("../dl/orte/quartiere.json"))["features"]:
    p = f["properties"]; gm = f["geometry"]
    for poly in (gm["coordinates"] if gm["type"] == "MultiPolygon" else [gm["coordinates"]]):
        FL.append((p["knr"], "Altstadt" if p["knr"] == 1 else p["qname"], Path(np.array(poly[0])[:, :2]), [Path(np.array(r)[:, :2]) for r in poly[1:]]))
for fn in sorted(glob.glob("../dl/orte/gem_*.json")):
    for r in json.load(open(fn))["results"]:
        if not r["properties"].get("is_current_jahr"): continue
        gm = r["geometry"]; nm = r["properties"]["gemname"].replace(" (ZH)", "")
        for poly in (gm["coordinates"] if gm["type"] == "MultiPolygon" else [gm["coordinates"]]):
            FL.append((None, nm, Path(np.array(poly[0])[:, :2]), [Path(np.array(q)[:, :2]) for q in poly[1:]]))
print(len(FL), "Flächen")
def wo(la, lo):
    for k, nm, A, I in FL:
        if A.contains_point((lo, la)) and not any(i.contains_point((lo, la)) for i in I): return k, nm
    return None, ""
def text(teile):
    teile = [t for t in dict.fromkeys(teile) if t[1]]
    if not teile: return ""
    if teile[0][0] is None: return " / ".join(t[1] for t in teile)                     # Gemeinde
    kreise = list(dict.fromkeys(str(t[0]) for t in teile if t[0] is not None))
    return f"Kreis {'/'.join(kreise)}, " + " / ".join(t[1] for t in teile)
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
out = []
for s in np.arange(0, d[-1], 100.0):
    la, lo = np.interp(s, d, P[:, 0]), np.interp(s, d, P[:, 1])
    la2, lo2 = np.interp(min(s + 20, d[-1]), d, P[:, 0]), np.interp(min(s + 20, d[-1]), d, P[:, 1])
    la1, lo1 = np.interp(max(s - 20, 0), d, P[:, 0]), np.interp(max(s - 20, 0), d, P[:, 1])
    ex, ny = (lo2 - lo1) * np.cos(np.radians(la)), (la2 - la1); n = np.hypot(ex, ny) or 1
    qx, qy = -ny / n, ex / n                                   # nach links
    seiten = []
    for f in (1, -1):
        seiten.append(wo(la + f * qy * 40 / 111320, lo + f * qx * 40 / (111320 * np.cos(np.radians(la)))))
    mitte = wo(la, lo)
    # Stadtgrenze: Gemeinde und Quartier nebeneinander -> das, worin die Mitte liegt
    if len({t[0] is None for t in seiten if t[1]}) > 1: seiten = [mitte]
    out.append([float(s), text(seiten) or text([mitte]), text([mitte])])
json.dump(out, open("orte2026.json", "w"), ensure_ascii=False)
from itertools import groupby
from common import official
for key, grp in groupby(out, key=lambda o: o[1]):
    grp = list(grp); print(f"km {float(official(grp[0][0])) / 1000:6.2f} {len(grp) * 100:6d} m  {key}")
