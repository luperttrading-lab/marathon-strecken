# Straße je 10 Linienmeter -> strassen.json: [Linienmeter, name, name (namen.py), bridge, tunnel, layer, highway, OSM-Weg].
# Die Linie besteht hier selbst aus OSM-Wegen (linie.py merkt sich je Stück den Weg); deshalb kein Suchen nach dem nächsten Weg wie in
# Stockholm, sondern der Weg, auf dem die Linie liegt. So kann die Hochstraße über der Zhongshan Nan'er Lu (Innerer Ring) nicht an
# die Stelle der Straße darunter treten. Das gezeichnete Stück im Park (Zielplan) heißt „Xujiahui-Sportpark“ (build.py).
import json
import numpy as np
from namen import name
o = json.load(open("../dl/osm_netz.json")); WG = o["ways"]
g = json.load(open("linie2025.json")); d = np.array(g["d"]); info = g["info"]
ss = np.arange(0, d[-1], 10.0)
out = []
for s in ss:
    i = min(max(0, int(np.searchsorted(d, s, side="right")) - 1), len(info) - 1)
    art, wid = info[i]
    if art != "osm": out.append([float(s), "", "", "", "", "", "plan", ""]); continue
    tg = WG[str(wid)][0]
    out.append([float(s), tg.get("name", ""), name(tg.get("name", "")), tg.get("bridge", ""), tg.get("tunnel", ""), tg.get("layer", ""),
                tg.get("highway", ""), wid])
json.dump(out, open("strassen.json", "w"), ensure_ascii=False)
from itertools import groupby
from common import official
for key, grp in groupby(out, key=lambda o: (o[1], o[2], o[3], o[4], o[5], o[6])):
    grp = list(grp)
    print(f"{grp[0][0]:7.0f} km {float(official(grp[0][0])) / 1000:6.2f} {len(grp) * 10:5d} m  {key[1]:24s} {key[0]:10s} {key[5]:12s} "
          f"{'Brücke' if key[2] not in ('', 'no') else ''} {'Tunnel ' + key[3] if key[3] not in ('', 'no') else ''} {key[4]}")
