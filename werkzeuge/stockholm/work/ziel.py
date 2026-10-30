# Nur Ausgabe: die letzten 600 m und die ersten 300 m der GPX-Linie neben den OSM-Wegen (Stadion-Laufbahn, Lidingövägen),
# um Startlinie und Ziellinie zu prüfen.
import json, numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
T = Transformer.from_crs(4326, 3006, always_xy=True)
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
o = json.load(open("../dl/osm_netz.json")); N = o["nodes"]
pk, pw, W = [], [], []
for wid, (tg, refs) in o["ways"].items():
    pts = [N[str(r)] for r in refs if str(r) in N]
    if len(pts) < 2: continue
    x, y = T.transform([p[1] for p in pts], [p[0] for p in pts]); k = len(W); W.append((wid, tg))
    for a, b in zip(np.c_[x, y][:-1], np.c_[x, y][1:]):
        for f in np.linspace(0, 1, max(2, int(np.hypot(*(b - a)) / 2) + 1)): pk.append(a + f * (b - a)); pw.append(k)
baum = cKDTree(np.array(pk))
def zeige(von, bis):
    for s in np.arange(von, bis, 20.0):
        la, lo = np.interp(s, d, P[:, 0]), np.interp(s, d, P[:, 1]); x, y = T.transform(lo, la)
        dd, ii = baum.query([x, y], k=6)
        nah = []
        for di, i in zip(dd, ii):
            wid, tg = W[pw[i]]; t = f"{tg.get('name') or tg.get('highway') or tg.get('railway') or tg.get('leisure') or ''}/{tg.get('highway') or tg.get('leisure') or ''} {di:.0f} m"
            if t.split()[0] not in [n.split()[0] for n in nah]: nah.append(t)
        print(f"{s:8.0f}  {la:.6f} {lo:.6f}  " + " | ".join(nah[:3]))
zeige(0, 300); print(); zeige(d[-1] - 600, d[-1] + 1)
print("Ende", P[-1])
for k, (tg, pt) in o["punkte"].items():
    if tg.get("leisure") in ("track",) or "finish" in json.dumps(tg).lower() or tg.get("sport") == "athletics": print(k, tg, pt)
for wid, (tg, refs) in o["ways"].items():
    if tg.get("leisure") == "track" or tg.get("highway") == "raceway" or tg.get("sport") == "running": print(wid, tg)
