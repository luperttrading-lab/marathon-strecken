# Höhen im 10-m-Raster, Straßen, Marken und Brücken -> data.json (geht als const D in london/index.html)
import sys, os, re; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official, gpx_of
L = 42195.0; STEP = 10
c = json.load(open("clean.json"))
k = np.array(c["k"]); hc = np.array(c["h"])
grid = np.arange(0, 42200 + 1, STEP, dtype=float)
hg = np.interp(np.minimum(grid, L), k, hc)
hm = hg.copy()                                   # gleitender Median über 3 Punkte (30 m)
for i in range(1, len(hg) - 1): hm[i] = np.median(hg[i-1:i+2])
# Straßen: Abschnitte mit Name und Stadtteil (Nominatim „suburb“). Stadtteile wechseln an Grenzen hin und her: Stücke unter
# 300 m übernehmen den Stadtteil davor; leere Namen übernehmen den Vorgänger.
import re
st = json.load(open("streets2026.json"))
def kurz(n): return n
roads = [kurz(r) for _, r, _ in st]; qs = [q for _, _, q in st]; ks = [float(official(s_)) for s_, _, _ in st]
for i_ in range(1, len(roads)): roads[i_] = roads[i_] or roads[i_ - 1]
i_ = 0
while i_ < len(qs):
    j_ = i_
    while j_ + 1 < len(qs) and qs[j_ + 1] == qs[i_]: j_ += 1
    if i_ > 0 and (ks[min(j_ + 1, len(ks) - 1)] - ks[i_]) < 300: qs[i_:j_ + 1] = [qs[i_ - 1]] * (j_ + 1 - i_)
    i_ = j_ + 1
for i_ in range(1, len(qs)): qs[i_] = qs[i_] or qs[i_ - 1]
segs, prev = [], None
for k_, road, q in zip(ks, roads, qs):
    if (road, q) != prev: segs.append([round(k_), road, q]); prev = (road, q)
segs[0][0] = 0
bridges = [{"a": round(r["a"]), "b": round(r["b"]), "name": kurz(r["name"]) or r["kind"], "kind": r["kind"]} for r in c["regions"]]
for b_ in bridges:
    if b_["name"] == "Westferry Road" and b_["kind"] == "Unterführung": b_.update(kind="Tunnel", name="Westferry Road unter dem Westferry Circus")
bridges.sort(key=lambda x: x["a"])
# Verpflegung (Meilen der vermessenen Strecke): Wasser (Buxton) laut Läuferguide 2026 an Meile 3, 6, 9, 12 und dann alle zwei
# Meilen bis 24; Lucozade Sport an Meile 7, 15, 21 und 23, Gels an Meile 14 und 19 (London Marathon Events)
MI = 1609.344
marks = [{"k": round(m * MI), "s": "Wasser", "c": "water", "n": f"Wasser Meile {m}"} for m in (3, 6, 9, 12, 14, 16, 18, 20, 22, 24)]
marks += [{"k": round(m * MI) + 40, "s": "Lucozade", "c": "water", "n": f"Lucozade Sport Meile {m}"} for m in (7, 15, 21, 23)]
marks += [{"k": round(m * MI) + 80, "s": "Gel", "c": "food", "n": f"Gel Meile {m}"} for m in (14, 19)]
marks.append({"k": 21098, "s": "Halbmarathon", "c": "half", "n": "Halbmarathon"})
marks.sort(key=lambda m: m["k"])
data = {"len": L, "step": STEP, "h": [int(round(v * 100)) for v in hm], "streets": segs, "marks": marks, "bridges": bridges}
json.dump(data, open("data.json", "w"), ensure_ascii=False, separators=(",", ":"))
# Kontrollen
def at(x): return float(np.interp(x, grid, hm))
def asc(w):
    xs = grid[grid <= L]; g = np.array([(at(min(x + w/2, L)) - at(max(x - w/2, 0))) / (min(x + w/2, L) - max(x - w/2, 0)) for x in xs])
    dh = (g[1:] + g[:-1]) / 2 * STEP
    return dh[dh > 0].sum(), -dh[dh < 0].sum(), np.abs(g).max() * 100, xs[np.argmax(g)], g.min()*100, xs[np.argmin(g)], g.max()*100
for w in (50, 200, 1000):
    u, d_, gabs, xmax, gmin, xmin, gmax = asc(w)
    print(f"Fenster {w:5d} m: ↑ {u:5.1f} m  ↓ {d_:5.1f} m  steilste bergauf {gmax:4.1f} % bei km {xmax/1000:.2f}, bergab {gmin:4.1f} % bei km {xmin/1000:.2f}")
raw = np.array(c["raw"]); kr = np.array(c["k"]); sel = kr <= L
roh = round(np.clip(np.diff(raw[sel]), 0, None).sum())
open("rohdaten.txt", "w").write(str(roh))
print("Rohdaten Punkt für Punkt ↑", roh, "m; bereinigt ↑", round(np.clip(np.diff(hc[sel]), 0, None).sum(), 1), "m")
print("Höhe min/max", round(hm.min(), 1), round(hm.max(), 1), "bei km", grid[np.argmin(hm)]/1000, grid[np.argmax(hm)]/1000, "Start", round(at(0), 1), "Ziel", round(at(L), 1))
print("Straßenabschnitte", len(segs), "Marken", len(marks), "Brücken/Unterführungen", len(bridges))
