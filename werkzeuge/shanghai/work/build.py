# Höhen im 10-m-Raster, Straßen, Marken und Brücken -> data.json (geht als const D in shanghai/index.html). Muster:
# werkzeuge/stockholm/work/build.py
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
# Straßen aus den OSM-Wegen der Linie (strassen.json, alle 10 m, Pinyin aus namen.py), Straßenviertel (Jiedao) aus orte2025.json (alle
# 100 m). Unbekannte und kurze Stücke unter 80 m (Kreuzungen) übernehmen den Namen davor; Viertel unter 300 m dem Vorgänger
# zugeschlagen und auf den nächsten Straßenwechsel gelegt. Ohne Namen in OSM: der Uferweg zwischen Lujiabang Lu und Miaojiang Lu
# (im Plan „黄浦滨江步道 Huangpu Riverside“) heißt „Huangpu-Uferweg“, das gezeichnete Stück im Park „Xujiahui-Sportpark“.
st = json.load(open("strassen.json")); orte = json.load(open("orte2025.json"))
gx = gpx_of(np.minimum(grid, L))
def strasse(x):
    o = st[min(len(st) - 1, int(round(x / 10)))]
    if o[6] == "plan": return "Xujiahui-Sportpark"
    if not o[2] and o[6] in ("footway", "path") and 20000 < float(official(x)) < 21500: return "Huangpu-Uferweg"
    return o[2] or ""
roads = [strasse(x) for x in gx]
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
# geschätzte Stücke (schraffiert): die Brückendecks (clean.py)
# Gewässer unter den Brücken aus OSM (waterway=river höchstens 40 m neben der Brückenmitte; der Longhua Gang ist an der Longteng Dadao
# dort ohne Namen eingetragen, 220 m weiter mit): Longhua Gang (龙华港), Zhangjiatang Gang (张家塘港), Chunshen Gang (春申港)
GEWAESSER = [(26000, 27500, "Longhua Gang"), (30000, 30700, "Zhangjiatang Gang"), (30700, 31500, "Chunshen Gang"),
             (32500, 33200, "Chunshen Gang"), (33200, 34000, "Zhangjiatang Gang"), (38000, 39000, "Longhua Gang")]
bridges = []
for r in c["regions"]:
    m = (r["a"] + r["b"]) / 2; gw = [n for a, b, n in GEWAESSER if a <= m < b][0]
    bridges.append({"a": round(r["a"]), "b": round(r["b"]), "name": f"{r['name']} über den {gw}", "kind": r["kind"]})
bridges.sort(key=lambda x: x["a"])
# Getränke laut Wettkampfordnung 2026 („补给站“): alle 5 km (5–40) Getränke und Wasser („饮料/饮水“), dazwischen alle 5 km (7,5–37,5)
# Wasser und Schwämme („饮水/用水“), an der km-Angabe. Energie (Riegel o. Ä.) nennt die Ordnung 2026 nicht; der Plan 2025 zeigt sie an
# 12,5, 15, 17,5, 25, 27,5, 30, 32,5, 35, 37,5 und 40 km: dort „Verpflegung“ (food), sonst „Getränke“ bzw. „Wasser“ (water).
def kmtext(x): return f"{x:.1f}".replace(".", ",").replace(",0", "")
ENERGIE_2025 = {12.5, 15, 17.5, 25, 27.5, 30, 32.5, 35, 37.5, 40}
marks = []
for i in range(15):
    km = 5 + 2.5 * i; getraenke = i % 2 == 0
    inhalt = "Getränke und Wasser" if getraenke else "Wasser und Schwämme"
    if km in ENERGIE_2025:
        marks.append({"k": round(km * 1000), "s": "Verpflegung", "c": "food", "n": f"Verpflegung km {kmtext(km)} ({inhalt}; Energie laut Plan 2025)"})
    else:
        marks.append({"k": round(km * 1000), "s": "Getränke" if getraenke else "Wasser", "c": "water", "n": f"{'Getränke' if getraenke else 'Wasser'} km {kmtext(km)} ({inhalt})"})
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
raw = np.array(c["raw"]); kr = np.array(c["k"]); sel = kr <= L
roh = round(np.clip(np.diff(raw[sel]), 0, None).sum())
open("rohdaten.txt", "w").write(str(roh))
print("Rohdaten Punkt für Punkt ↑", roh, "m; bereinigt ↑", round(np.clip(np.diff(hc[sel]), 0, None).sum(), 1), "m")
print("Höhe min/max", round(hm.min(), 1), round(hm.max(), 1), "bei km", grid[np.argmin(hm)]/1000, grid[np.argmax(hm)]/1000, "Start", round(at(0), 1), "Ziel", round(at(L), 1))
print("Straßenabschnitte", len(segs), "Marken", len(marks), "Brücken", len(bridges))
for sg in segs: print("  ", sg)
