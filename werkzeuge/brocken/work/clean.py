# Höhen bereinigen -> clean.json {k (offizielle Meter), h, raw, regions}. Grundlage DGM1 Sachsen-Anhalt (dgm.py, alle 10 Linienmeter).
# Ein Geländemodell kennt keine Brücken: Auf den kleinen Brücken der Strecke (OSM bridge=*, strassen.json; sechsmal über die Ilse bei
# Ilsenburg und im Ilsetal, über Sandtalbach, Schlüsiebach und Holtemme, alle 20–40 m lang) misst es das Bachbett. Dort
# gilt eine Gerade zwischen den Brückenenden (Höhe des DGM je einen Punkt davor und danach, einen weiter, wenn der höher liegt), wo das DGM
# darunter liegt. Ein
# Oberflächenmodell hilft im Wald nicht (es misst die Baumkronen). Brücken, auf denen die Gerade mehr als 1 m über dem DGM liegt, kommen
# in D.bridges (geschätzt, schraffiert), die übrigen sind nur geglättet. Danach Kontrolle: Stufen über 3 m je 10 m und einzelne Spitzen.
# Muster: werkzeuge/freiburg/work/clean.py.
import json
import numpy as np
from common import official
r = json.load(open("dgm2026_10m.json")); st = json.load(open("strassen.json"))
s = np.array([x[0] for x in r]); raw = np.array([x[3] for x in r], float); k = official(s)
assert not np.isnan(raw).any(), "Punkte ohne DGM-Wert"
h = raw.copy(); regions = []
def gruppen(idx):
    g = []
    for i in idx:
        if g and i - g[-1][-1] <= 2: g[-1].append(i)
        else: g.append([i])
    return g
# Name der Brücke: OSM-Name, sonst nach dem Gewässer darunter (nächster OSM-Wasserlauf höchstens 30 m neben der Brückenmitte)
from pyproj import Transformer
T = Transformer.from_crs(4326, 25832, always_xy=True)
o = json.load(open("../dl/osm_netz.json")); NO = o["nodes"]; WASSER = []
for tg, refs in o["ways"].values():
    if "waterway" in tg and tg.get("name"):
        pts = [NO[str(q)] for q in refs if str(q) in NO]
        if pts: x, y = T.transform([p[1] for p in pts], [p[0] for p in pts]); WASSER.append((tg["name"], np.c_[x, y]))
def gewaesser(i):
    e, n = T.transform(r[i][2], r[i][1]); best = min(((float(np.hypot(*(P - [e, n]).T).min()), nm) for nm, P in WASSER), default=(1e9, ""))
    return best[1] if best[0] < 30 else ""
def bruecke(osmname, i):
    if osmname and osmname != "Ilsetal": return osmname     # der Weg „Ilsetal“ heißt auf der Brücke wie davor
    g_ = gewaesser(i)
    return "Ilsebrücke" if g_ == "Ilse" else (f"Brücke über den {g_}" if g_.endswith("bach") else (f"Brücke über die {g_}" if g_ else "Brücke"))
for gg in gruppen([i for i, x in enumerate(st) if x[3] not in ("", "no")]):
    a, b = max(0, gg[0] - 1), min(len(h) - 1, gg[-1] + 1)
    if a > 0 and raw[a - 1] > raw[a]: a -= 1                 # Brückenende noch im Bachbett: einen Punkt weiter außen, wenn dort höher
    if b < len(h) - 1 and raw[b + 1] > raw[b]: b += 1
    gerade = h[a] + (h[b] - h[a]) * (np.arange(a, b + 1) - a) / (b - a)
    tief = float((gerade - raw[a:b + 1]).max())
    h[a:b + 1] = np.maximum(h[a:b + 1], gerade)
    nm = bruecke(st[gg[0]][2], (gg[0] + gg[-1]) // 2)
    print(f"Brücke {nm:22s} km {k[a]/1000:6.2f}–{k[b]/1000:6.2f} ({k[b]-k[a]:.0f} m, {st[gg[0]][6]}): Enden {h[a]:.2f} / {h[b]:.2f} m, DGM bis {tief:.2f} m darunter")
    if tief > 1.0:
        regions.append({"a": float(k[a]), "b": float(k[b]), "kind": "Brücke", "name": nm, "tief": round(tief, 2)})
regions.sort(key=lambda o: o["a"])
dd = np.diff(h)
# Stufen: am Berg sind 1,5–2,3 m je 10 m echtes Gelände (Anstieg zum Brocken bis 20 %); gemeldet werden Sprünge über 3 m und einzelne Spitzen
for i in np.where(np.abs(dd) > 3.0)[0]: print(f"  Stufe über 3 m: km {k[i]/1000:.2f} {h[i]:.2f} -> {h[i+1]:.2f}")
sp = [i for i in range(1, len(h) - 1) if (h[i] - h[i - 1]) * (h[i] - h[i + 1]) > 0 and min(abs(h[i] - h[i - 1]), abs(h[i] - h[i + 1])) > 1.0]
for i in sp: print(f"  Spitze über 1 m: km {k[i]/1000:.2f} {h[i-1]:.2f} / {h[i]:.2f} / {h[i+1]:.2f}")
print("größte Stufe je 10 m:", round(float(np.abs(dd).max()), 2), "m bei km", round(float(k[np.argmax(np.abs(dd))]) / 1000, 2))
json.dump({"k": k.tolist(), "h": h.tolist(), "raw": raw.tolist(), "regions": regions}, open("clean.json", "w"), ensure_ascii=False)
