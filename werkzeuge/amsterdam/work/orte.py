# Ortsteil alle 100 m (Linienmeter): in Amsterdam die Wijk (CBS Wijk- en Buurtkaart 2024 über den WFS von PDOK,
# service.pdok.nl/cbs/wijkenbuurten/2024/wfs/v1_0, Ebene „wijken“; in Amsterdam sind das die Wijken der Stadt, z. B.
# Museumkwartier, Oude Pijp, Indische Buurt-Oost). Stadsdelen wären zu grob (Zuid allein von km 0 bis 15 und ab km 37),
# Buurten zu fein (die Strecke läuft oft auf ihren Grenzstraßen). Außerhalb Amsterdams der Ort: Amstelveen, in Ouder-Amstel
# (dort hat das CBS nur eine Wijk) Ouderkerk aan de Amstel bzw. Duivendrecht nach der Buurt, sonst „Ouder-Amstel“, Diemen.
# -> orte2026.json [Linienmeter, Name]
import json, numpy as np
from matplotlib.path import Path
def flaechen(geom):
    cs = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    return [[Path(np.array(r)) for r in poly] for poly in cs]
def innen(ff, x, y): return any(p[0].contains_point((x, y)) and not any(h.contains_point((x, y)) for h in p[1:]) for p in ff)
W = [(f["properties"]["gemeentenaam"], f["properties"]["wijknaam"], flaechen(f["geometry"])) for f in json.load(open("../dl/cbs_wijken_2024.json"))["features"]]
B = [(f["properties"]["gemeentenaam"], f["properties"]["buurtnaam"], flaechen(f["geometry"])) for f in json.load(open("../dl/cbs_buurten_2024.json"))["features"]
     if f["properties"]["gemeentenaam"] == "Ouder-Amstel"]
def name(lo, la):
    gm, wk = next(((g, n) for g, n, ff in W if innen(ff, lo, la)), ("", ""))
    if gm == "Amsterdam": return wk.replace(" e.o.", "")
    if gm == "Ouder-Amstel":
        bu = next((n for g, n, ff in B if innen(ff, lo, la)), "")
        return bu if bu in ("Ouderkerk aan de Amstel", "Duivendrecht") else "Ouder-Amstel"
    return gm
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
out = [[float(s), name(np.interp(s, d, P[:, 1]), np.interp(s, d, P[:, 0]))] for s in np.arange(0, d[-1], 100.0)]
json.dump(out, open("orte2026.json", "w"), ensure_ascii=False)
from itertools import groupby
print([(k, len(list(v)) * 100) for k, v in groupby(o[1] for o in out)])
