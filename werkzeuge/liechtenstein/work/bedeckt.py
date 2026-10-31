# Überdeckte Stücke der Strecke: je 10 Linienmeter, ob der OSM-Weg unter der Linie (strassen.json) tunnel=* oder covered=yes trägt.
# Dort misst das Geländemodell die Decke (Fels, Erdreich, Galerie) statt des Wegs; clean.py zieht diese Stücke als Gerade zwischen den
# Portalen, wenn das Modell dort über dieser Geraden liegt.
# -> bedeckt.json [[Linienmeter, Weg-ID, Tags], …] nur für Treffer
import json
o = json.load(open("../dl/osm_netz.json"))["ways"]
out = []
for s, nm, _, br, tu, layer, hw, wid in json.load(open("strassen.json")):
    if tu not in ("", "no"):
        tg = o[wid][0]
        out.append([s, wid, {k: v for k, v in tg.items() if k in ("highway", "name", "tunnel", "covered", "layer", "ref", "description")}])
json.dump(out, open("bedeckt.json", "w"), ensure_ascii=False)
from itertools import groupby
from common import official
for key, grp in groupby(out, key=lambda o: o[1]):
    grp = list(grp); print(f"Linie {grp[0][0]:6.0f}–{grp[-1][0]:6.0f} km {official(grp[0][0]) / 1000:6.2f}  {len(grp) * 10:4d} m  {key} {grp[0][2]}")
