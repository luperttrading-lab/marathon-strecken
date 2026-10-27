# Höhen im 10-m-Raster, Straßen, Marken und Brücken -> data.json (geht als const D in muenchen/index.html)
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
# Straßen: Abschnitte mit Name und Stadtteil
st = json.load(open("streets2026.json"))
segs, prev, last_road, last_q = [], None, "", ""
for s_gpx, road, q in st:
    road = road or last_road; q = q or last_q
    km_ = float(official(s_gpx))
    if road != prev: segs.append([round(km_), road, q]); prev = road
    last_road, last_q = road, q
segs[0][0] = 0
STRASSEN = {}
for sg in segs: sg[1] = STRASSEN.get(sg[1], sg[1])
# Brücken und Unterführungen (der Buckel am Zieleinlauf in die Festhalle ist nur geglättet, nicht gelistet)
NAMEN = {}   # Nominatim nennt sonst die anliegende Straße
bridges = [{"a": round(r["a"]), "b": round(r["b"]), "name": NAMEN.get(r["name"], r["name"]) or r["kind"], "kind": r["kind"]} for r in c["regions"] ]
# Am Start führt die Brücke über den Nymphenburg-Biedersteiner Kanal; Nominatim nennt den Toni-Merkens-Weg davor
for b_ in bridges:
    if b_["a"] < 1000 and b_["kind"] == "Brücke": b_["name"] = "Nymphenburg-Biedersteiner Kanal"
# Marken: Verpflegungsstellen und Staffelwechsel veröffentlicht der Veranstalter nur im Faltplan (ohne Koordinaten); bleibt der Halbmarathon
marks = []
marks.append({"k": 21098, "s": "Halbmarathon", "c": "half", "n": "Halbmarathon", "_d": 0})
marks.sort(key=lambda m: m["k"])
for m in marks: m.pop("_d")
data = {"len": L, "step": STEP, "h": [int(round(v * 100)) for v in hm], "streets": segs, "marks": marks, "bridges": bridges}
json.dump(data, open("data.json", "w"), ensure_ascii=False, separators=(",", ":"))
# Kontrollen
def at(x): return float(np.interp(x, grid, hm))
def asc(w):
    xs = grid[grid <= L]; g = np.array([(at(min(x + w/2, L)) - at(max(x - w/2, 0))) / (min(x + w/2, L) - max(x - w/2, 0)) for x in xs])
    dh = (g[1:] + g[:-1]) / 2 * STEP
    return dh[dh > 0].sum(), -dh[dh < 0].sum(), np.abs(g).max() * 100, xs[np.argmax(g)], g.min()*100, xs[np.argmin(g)]
for w in (50, 200, 1000):
    u, d_, gmax, xmax, gmin, xmin = asc(w)
    print(f"Fenster {w:5d} m: ↑ {u:5.1f} m  ↓ {d_:5.1f} m  steilste bergauf {gmax:4.1f} % bei km {xmax/1000:.2f}, bergab {gmin:4.1f} % bei km {xmin/1000:.2f}")
raw = np.array(c["raw"]); kr = np.array(c["k"]); sel = kr <= L
print("Rohdaten Punkt für Punkt ↑", round(np.clip(np.diff(raw[sel]), 0, None).sum(), 1), "m; bereinigt ↑", round(np.clip(np.diff(hc[sel]), 0, None).sum(), 1), "m")
print("Höhe min/max", round(hm.min(), 1), round(hm.max(), 1), "bei km", grid[np.argmin(hm)]/1000, grid[np.argmax(hm)]/1000, "Start", round(at(0), 1), "Ziel", round(at(L), 1))
print("Straßenabschnitte", len(segs), "Marken", len(marks), "Brücken/Unterführungen", len(bridges))
