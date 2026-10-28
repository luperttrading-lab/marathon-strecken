# Höhen im 10-m-Raster, Straßen, Marken und Brücken -> data.json (geht als const D in chicago/index.html)
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
# Straßen: Abschnitte mit Name und Viertel. Namen ohne Himmelsrichtung und Ebene (North Upper Columbus Drive -> Columbus Drive),
# wie auf der Karte des Veranstalters. Viertel (Nominatim „neighbourhood“) wechseln an Blockgrenzen hin und her: Stücke unter
# 600 m übernehmen das Viertel davor; Start und Ziel liegen im Grant Park.
import re
st = json.load(open("streets2026.json"))
def kurz(n): return re.sub(r"^(Upper |Lower )?(North |South |East |West )?(Upper )?", "", n)
roads = [kurz(r) for _, r, _ in st]; qs = [q for _, _, q in st]; ks = [float(official(s_)) for s_, _, _ in st]
for i_ in range(1, len(roads)): roads[i_] = roads[i_] or roads[i_ - 1]
i_ = 0
while i_ < len(qs):
    j_ = i_
    while j_ + 1 < len(qs) and qs[j_ + 1] == qs[i_]: j_ += 1
    if i_ > 0 and (ks[min(j_ + 1, len(ks) - 1)] - ks[i_]) < 600: qs[i_:j_ + 1] = [qs[i_ - 1]] * (j_ + 1 - i_)
    i_ = j_ + 1
for i_, k_ in enumerate(ks):
    if k_ < 450 or k_ > 41950: qs[i_] = "Grant Park"
segs, prev = [], None
for k_, road, q in zip(ks, roads, qs):
    if (road, q) != prev: segs.append([round(k_), road, q]); prev = (road, q)
segs[0][0] = 0
bridges = [{"a": round(r["a"]), "b": round(r["b"]), "name": kurz(r["name"]) or r["kind"], "kind": r["kind"]} for r in c["regions"]]
# obere Ebene des Columbus Drive zwischen Randolph Street und Fluss: im Geländemodell liegt dort eine Plattform 7 m höher
for b_ in bridges:
    if b_["a"] < 900 and b_["b"] < 1000: b_.update(kind="Brücke", name="Columbus Drive, obere Ebene")
bridges.sort(key=lambda x: x["a"])
# Verpflegung laut offizieller Karte (verpflegung.py): 20 Stationen mit Wasser, Gatorade und Sanität, 2 Gel-Depots (Maurten)
mi_txt = lambda k: f"{k / 1609.344:.1f}".replace(".", ",")
marks = [({"k": v["k"], "s": "Getränke", "c": "water", "n": f"Verpflegungsstation {v['nr']} (Meile {mi_txt(v['k'])})"} if v["typ"] == "water" else
          {"k": v["k"], "s": "Gel", "c": "food", "n": f"Gel-Depot (Meile {mi_txt(v['k'])})"}) for v in json.load(open("../dl/verpflegung.json"))]
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
