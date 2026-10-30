# Höhen im 10-m-Raster, Straßen, Marken und Brücken -> data.json (geht als const D in amsterdam/index.html)
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official, gpx_of
L = 42195.0; STEP = 10
c = json.load(open("clean.json"))
k = np.array(c["k"]); hc = np.array(c["h"])
grid = np.arange(0, 42200 + 1, STEP, dtype=float)
hg = np.interp(np.minimum(grid, L), k, hc)
hm = hg.copy()                                   # gleitender Median über 3 Punkte (30 m)
for i in range(1, len(hg) - 1): hm[i] = np.median(hg[i-1:i+2])
# Straßen aus den OSM-Wegen der Linie (strassen.json, alle 10 m, Namen wie in OSM), Ortsteil aus orte2026.json (alle 100 m).
# Wege ohne Namen (Fuß- und Radwege an Kreuzungen, Zugang zum Stadion) und Stücke unter 80 m übernehmen den Namen davor;
# Ortsteile unter 300 m dem Vorgänger zugeschlagen und auf den nächsten Straßenwechsel gelegt.
st = json.load(open("strassen.json"))
orte = json.load(open("orte2026.json"))
gx = gpx_of(np.minimum(grid, L))
roads = [st[min(len(st) - 1, int(round(x / 10)))][1] or "" for x in gx]
qs = [orte[min(len(orte) - 1, int(round(x / 100)))][1] for x in gx]
def glaetten(v, mind):
    for i in range(1, len(v)): v[i] = v[i] or v[i - 1]
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[j + 1] == v[i]: j += 1
        if i > 0 and (j + 1 - i) * STEP < mind: v[i:j + 1] = [v[i - 1]] * (j + 1 - i)
        i = j + 1
    for i in range(len(v) - 2, -1, -1): v[i] = v[i] or v[i + 1]
    return v
roads = glaetten(roads, 80); qs = glaetten(qs, 300)
wechsel = [i for i in range(1, len(roads)) if roads[i] != roads[i - 1]]
for i in [i for i in range(1, len(qs)) if qs[i] != qs[i - 1]]:
    w = min(wechsel, key=lambda j: abs(j - i), default=None)
    if w is not None and 0 < abs(w - i) <= 10:
        if w > i: qs[i:w] = [qs[i - 1]] * (w - i)
        else: qs[w:i] = [qs[i]] * (i - w)
segs, prev = [], None
for x, road, q in zip(grid, roads, qs):
    if x > L: break
    if (road, q) != prev: segs.append([round(x), road, q]); prev = (road, q)
segs[0][0] = 0
bridges = [{"a": round(r["a"]), "b": round(r["b"]), "name": r["name"] or r["kind"], "kind": r["kind"]} for r in c["regions"]]
bridges.sort(key=lambda x: x["a"])
# Getränke und Verpflegung laut Veranstalter (Seite „TCS Marathon“, Tabelle „Refreshment stations“ 2026) an ihrer km-Angabe:
# Wasser (Becher), Maurten-Getränk, Bananen, Schwämme; Maurten-Gel nur bei km 18 und 30.
STELLEN = [(5, "Wasser, Maurten-Getränk"), (8, "Wasser"), (11, "Wasser, Maurten-Getränk, Banane, Schwamm"),
           (16, "Wasser, Maurten-Getränk, Banane"), (20, "Wasser, Maurten-Getränk, Banane, Schwamm"), (25, "Wasser"),
           (27, "Wasser, Maurten-Getränk, Banane, Schwamm"), (31, "Wasser, Maurten-Getränk, Banane"), (33, "Wasser, Schwamm"),
           (35, "Wasser, Maurten-Getränk, Banane"), (38, "Wasser, Maurten-Getränk, Banane, Schwamm"), (40.5, "Wasser, Banane")]
def kmtext(x): return f"{x:g}".replace(".", ",")
marks = []
for km, was in STELLEN:
    essen = "Banane" in was; nur_wasser = was == "Wasser"
    s_ = "Verpflegung" if essen else ("Wasser" if nur_wasser else "Getränke")
    marks.append({"k": int(round(km * 1000)), "s": s_, "c": "food" if essen else "water", "n": f"{s_} km {kmtext(km)} ({was})"})
for km in (18, 30):
    marks.append({"k": km * 1000, "s": "Gel", "c": "food", "n": f"Gel km {km} (Maurten)"})
marks.append({"k": 21098, "s": "Halbmarathon", "c": "half", "n": "Halbmarathon"})
marks.sort(key=lambda m: m["k"])
data = {"len": L, "step": STEP, "h": [int(round(v * 100)) for v in hm], "streets": segs, "marks": marks, "bridges": bridges}
json.dump(data, open("data.json", "w"), ensure_ascii=False, separators=(",", ":"))
# Kontrollen
def at(x): return float(np.interp(x, grid, hm))
def asc(w):
    xs = grid[grid <= L]; gr = np.array([(at(min(x + w/2, L)) - at(max(x - w/2, 0))) / (min(x + w/2, L) - max(x - w/2, 0)) for x in xs])
    dh = (gr[1:] + gr[:-1]) / 2 * STEP
    return dh[dh > 0].sum(), -dh[dh < 0].sum(), np.abs(gr).max() * 100, xs[np.argmax(gr)], gr.min()*100, xs[np.argmin(gr)], gr.max()*100
for w in (50, 100, 200, 1000):
    u, d_, gabs, xmax, gmin, xmin, gmax = asc(w)
    print(f"Fenster {w:5d} m: ↑ {u:5.1f} m  ↓ {d_:5.1f} m  steilste bergauf {gmax:4.1f} % bei km {xmax/1000:.2f}, bergab {gmin:4.1f} % bei km {xmin/1000:.2f}")
raw = np.array([np.nan if v is None else v for v in c["raw"]], float); kr = np.array(c["k"]); sel = (kr <= L) & ~np.isnan(raw)
roh = round(np.clip(np.diff(raw[sel]), 0, None).sum())
open("rohdaten.txt", "w").write(str(roh))
print("Rohdaten Punkt für Punkt (ohne Lücken) ↑", roh, "m; bereinigt ↑", round(np.clip(np.diff(hc[kr <= L]), 0, None).sum(), 1), "m")
print("Höhe min/max", round(hm.min(), 2), round(hm.max(), 2), "bei km", grid[np.argmin(hm)]/1000, grid[np.argmax(hm)]/1000, "Start", round(at(0), 2), "Ziel", round(at(L), 2))
print("Straßenabschnitte", len(segs), "Marken", len(marks), "Brücken", len(bridges))
for sg in segs: print("  ", sg)
