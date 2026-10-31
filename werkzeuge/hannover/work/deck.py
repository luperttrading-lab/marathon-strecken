# Brücken der Strecke aus dem Oberflächenmodell DOM1 (LGLN, dieselbe Befliegung 2016 wie das DGM1): Das Geländemodell lässt Brücken
# weg und misst darunter Wasser oder den Kanal (Mittellandkanal 50 m, Leine/Ihme), das DOM hat die Fahrbahn. Je 10-m-Punkt im Bereich
# der OSM-Brücken (strassen.json, bridge=*) plus 30 m davor und danach das 25-%-Quantil der 5 × 5 DOM-Werte um den Punkt (Muster:
# werkzeuge/koeln/work/dom.py). Wo DGM und DOM auf 0,3 m übereinstimmen, ist der Punkt Gelände (Rampe), sonst Deck.
# -> deck.json [[Linienmeter, DOM-Quantil, DGM1, Brückenname], …]
import json
import numpy as np
from pyproj import Transformer
import lgln
from common import official
T = Transformer.from_crs(4326, 25832, always_xy=True)
r = json.load(open("dgm2026_10m.json")); st = json.load(open("strassen.json"))
s = np.array([x[0] for x in r]); la = np.array([x[1] for x in r]); lo = np.array([x[2] for x in r]); g = np.array([x[3] for x in r], float)
br = [i for i, x in enumerate(st) if x[3] not in ("", "no")]
# zusammenhängende Brückenstücke
grp = []
for i in br:
    if grp and i - grp[-1][-1] <= 3: grp[-1].append(i)
    else: grp.append([i])
out = []
for gg in grp:
    a, b = gg[0], gg[-1]; name = st[a][2]
    idx = list(range(max(0, a - 3), min(len(s) - 1, b + 4) + 1))
    E, N = T.transform(lo[idx], la[idx])
    q = lgln.fenster("dom1", E, N)
    print(f"{name} (Linienmeter {s[a]:.0f}–{s[b]:.0f}, km {float(official(s[a]))/1000:.2f}–{float(official(s[b]))/1000:.2f}):")
    for j, i in enumerate(idx):
        mark = "Brücke" if a <= i <= b else ""
        print(f"   km {float(official(s[i]))/1000:6.3f}  DGM {g[i]:6.2f}  DOM-Q25 {q[j]:6.2f}  {mark}")
        out.append([float(s[i]), round(float(q[j]), 3), float(g[i]), name])
json.dump(out, open("deck.json", "w"), ensure_ascii=False)
