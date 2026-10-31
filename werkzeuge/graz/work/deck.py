# Brücken der Strecke aus dem Laser-Oberflächenmodell des BEV (ALS DSM, Höhenraster 1 m, Stichtag 15.09.2025, gleiche Befliegung wie das
# Geländemodell, CC BY 4.0): Das Geländemodell lässt Brücken weg und misst darunter die Mur, das DSM hat die Fahrbahn. Je 10-m-Punkt im
# Bereich der OSM-Brücken (strassen.json, bridge=*) plus 30 m davor und danach das 25-%-Quantil der DSM-Zellen im Umkreis von 2 m
# (Fahrbahn ohne Geländer, Leuchten, Fahrzeuge; wie werkzeuge/wien/work/dsm.py). Kopie von werkzeuge/freiburg/work/deck.py mit bev.py.
# -> deck.json [[Linienmeter, DSM-Quantil, DTM, Brückenname], …]
import json
import numpy as np
import bev
from common import official
r = json.load(open("dgm2026_10m.json")); st = json.load(open("strassen.json"))
s = np.array([x[0] for x in r]); la = np.array([x[1] for x in r]); lo = np.array([x[2] for x in r]); g = np.array([x[3] for x in r], float)
br = [i for i, x in enumerate(st) if x[3] not in ("", "no")]
grp = []
for i in br:
    if grp and i - grp[-1][-1] <= 3: grp[-1].append(i)
    else: grp.append([i])
dsm = bev.Modell("DSM"); out = []
for gg in grp:
    a, b = gg[0], gg[-1]; name = st[a][2]
    idx = list(range(max(0, a - 3), min(len(s) - 1, b + 4) + 1))
    q = dsm.quantil(lo[idx], la[idx], r=2.0, q=25)
    print(f"{name} (Linienmeter {s[a]:.0f}–{s[b]:.0f}, km {float(official(s[a]))/1000:.2f}–{float(official(s[b]))/1000:.2f}):")
    for j, i in enumerate(idx):
        mark = "Brücke" if a <= i <= b else ""
        print(f"   km {float(official(s[i]))/1000:6.3f}  DTM {g[i]:6.2f}  DSM-Q25 {q[j]:6.2f}  {mark}")
        out.append([float(s[i]), round(float(q[j]), 3), float(g[i]), name])
json.dump(out, open("deck.json", "w"), ensure_ascii=False)
