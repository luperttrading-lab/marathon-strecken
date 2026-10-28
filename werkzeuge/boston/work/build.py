# Höhen im 10-m-Raster, Straßen, Marken und Brücken -> data.json (geht als const D in boston/index.html)
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
# Straßen: Abschnitte mit Name und Ort
st = json.load(open("streets2026.json"))
STRASSEN = json.load(open("strassen_namen.json")) if os.path.exists("strassen_namen.json") else {}
segs, prev, last_road, last_q = [], None, "", ""
for s_gpx, road, q in st:
    road = STRASSEN.get(road, road) or last_road; q = q or last_q
    km_ = float(official(s_gpx))
    if (road, q) != prev: segs.append([round(km_), road, q]); prev = (road, q)   # neuer Abschnitt auch beim Ortswechsel (Beacon Street: Brighton, Brookline, Boston)
    last_road, last_q = road, q
segs[0][0] = 0
bridges = [{"a": round(r["a"]), "b": round(r["b"]), "name": r["name"] or r["kind"], "kind": r["kind"]} for r in c["regions"]]
bridges.sort(key=lambda x: x["a"])
# Getränkestellen laut B.A.A. (Race-Course.pdf 2026, Meile): Wasser (Poland Spring) und Gatorade; an dreien zusätzlich
# Maurten-Gel. Die Meilen beziehen sich auf die vermessene Strecke, also offizielle Meter = Meile × 1609,344.
MI = 1609.344
GETRAENKE = [2.1, 3.1, 4.4, 5.2, 6.01, 7.1, 8.01, 8.9, 10.1, 11.2, 12.1, 13.3, 14.1, 15.01, 16.01, 17.1, 18.1, 19.1, 20.1, 21.1, 22.01, 23.1, 24.1, 25.1]
GEL = {12.1, 17.1, 22.01}
mi_txt = lambda m: f"{m:g}".replace(".", ",")
marks = [({"k": round(m * MI), "s": "Gel", "c": "food", "n": f"Getränke und Gel Meile {mi_txt(m)}"} if m in GEL else
          {"k": round(m * MI), "s": "Getränke", "c": "water", "n": f"Getränkestelle Meile {mi_txt(m)}"}) for m in GETRAENKE]
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
