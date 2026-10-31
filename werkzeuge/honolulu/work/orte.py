# Stadtteil alle 100 m (Linienmeter) aus den Bezirken der Neighborhood Boards der City and County of Honolulu (Unterbezirke laut
# Neighborhood Plan 2008, Neighborhood Commission Office; Open Data der Stadt, HOLIS: services.arcgis.com/tNJpAOha4mODLkXz/arcgis/
# rest/services/AdministrativePolitical/FeatureServer/5, ../dl/orte/nb.geojson). OSM hat Grenzen nur für Ost-Honolulu, die Bezirke
# der Stadt decken die ganze Strecke einheitlich ab. Angezeigt wird der geläufige Name des Viertels (wie in der Streckenbeschreibung
# des Veranstalters: Kakaʻako, Downtown, Waikīkī, Diamond Head, Kāhala, Waiʻalae Iki, ʻĀina Haina, Niu Valley, Hawaiʻi Kai), nicht der
# Verwaltungsname des Bezirks (NAME unten). Viele Straßen sind selbst die Grenze: je 40 m links und rechts nachsehen, bei zwei
# Vierteln „links / rechts“ (Muster: werkzeuge/stockholm/work/orte.py). Auf dem Kalanianaʻole Highway liegt die Meerseite oft
# außerhalb aller Bezirke; dann gilt die Landseite.
# Abruf (einmal):  curl "<FeatureServer>/5/query?where=1%3D1&outFields=*&outSR=4326&f=geojson&geometry=-157.87,21.24,-157.68,21.31
#                   &geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects" -o ../dl/orte/nb.geojson
# -> orte2026.json [Linienmeter, Name, Bezirk in der Mitte, Unterbezirk in der Mitte]
import json
import numpy as np
from matplotlib.path import Path
# (Board-Nummer, Unterbezirk) -> Name in der App. Unterbezirk None: alle Unterbezirke des Boards.
NAME = {(11, "Kakaako/Kewalo Basin"): "Kakaʻako", (11, "Ala Moana"): "Ala Moana", (11, "Kaheka"): "Ala Moana", (11, "Rycroft"): "Ala Moana",
        (13, None): "Downtown", (12, None): "Punchbowl", (10, None): "Makiki", (8, None): "McCully", (9, None): "Waikīkī",
        (5, "Diamond Head/Ft Ruger/Kapiolani Park"): "Diamond Head", (5, "Kapahulu/East Ala Wai"): "Kapahulu",
        (3, "Kahala"): "Kāhala", (3, "Diamond Head"): "Diamond Head", (3, "Waialae Nui Valley"): "Waiʻalae", (3, "Waialae Nui Ridge"): "Waiʻalae",
        (4, None): "Kaimukī", (2, "Waialae Iki Ridge"): "Waiʻalae Iki", (2, "Waialae Iki Ridge--New Increment"): "Waiʻalae Iki",
        (2, "Wiliwilinui"): "Waiʻalae Iki", (2, "Aina Haina"): "ʻĀina Haina", (2, "Kainani/Wailupe"): "ʻĀina Haina",
        (2, "Kalani Valley"): "ʻĀina Haina", (2, "Hawaii Loa Ridge"): "Niu Valley", (2, "Kuliouou Valley"): "Kuliʻouʻou", (1, None): "Hawaiʻi Kai"}
def ort(board, sd):
    return NAME.get((board, sd)) or NAME.get((board, None)) or (sd or "")
FL = []
for f in json.load(open("../dl/orte/nb.geojson"))["features"]:
    p = f["properties"]; gm = f["geometry"]
    polys = gm["coordinates"] if gm["type"] == "MultiPolygon" else [gm["coordinates"]]
    for poly in polys:
        FL.append((p["board_num"], p["sd_desc"], p["towns"], Path(np.array(poly[0])), [Path(np.array(r)) for r in poly[1:]]))
print(len(FL), "Flächen")
def wo(la, lo):
    for b, sd, towns, A, I in FL:
        if A.contains_point((lo, la)) and not any(i.contains_point((lo, la)) for i in I): return b, sd, towns
    return None, None, ""
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
out = []
for s in np.arange(0, d[-1], 100.0):
    la, lo = np.interp(s, d, P[:, 0]), np.interp(s, d, P[:, 1])
    la2, lo2 = np.interp(min(s + 20, d[-1]), d, P[:, 0]), np.interp(min(s + 20, d[-1]), d, P[:, 1])
    la1, lo1 = np.interp(max(s - 20, 0), d, P[:, 0]), np.interp(max(s - 20, 0), d, P[:, 1])
    ex, ny = (lo2 - lo1) * np.cos(np.radians(la)), (la2 - la1); n = np.hypot(ex, ny) or 1
    qx, qy = -ny / n, ex / n                                   # nach links (Grad Länge auf Grad Breite umgerechnet)
    seiten = []
    for f in (1, -1):
        b, sd, _ = wo(la + f * qy * 40 / 111320, lo + f * qx * 40 / (111320 * np.cos(np.radians(la))))
        if b is not None: seiten.append(ort(b, sd))
    b, sd, towns = wo(la, lo)
    mitte = ort(b, sd) if b is not None else ""
    namen = [x for x in dict.fromkeys(seiten) if x] or [mitte]
    out.append([float(s), " / ".join(namen), towns, sd or ""])
json.dump(out, open("orte2026.json", "w"), ensure_ascii=False)
from itertools import groupby
from common import official
for key, grp in groupby(out, key=lambda o: o[1]):
    grp = list(grp); print(f"km {float(official(grp[0][0])) / 1000:6.2f} {len(grp) * 100:6d} m  {key:28s} {grp[0][2]} / {grp[0][3]}")
