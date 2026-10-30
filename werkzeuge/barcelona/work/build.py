# Höhen im 10-m-Raster, Straßen, Marken und Brücken -> data.json (geht als const D in barcelona/index.html)
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official, gpx_of
from namen import name, ORT
L = 42195.0; STEP = 10
c = json.load(open("clean.json"))
k = np.array(c["k"]); hc = np.array(c["h"])
grid = np.arange(0, 42200 + 1, STEP, dtype=float)
hg = np.interp(np.minimum(grid, L), k, hc)
hm = hg.copy()                                   # gleitender Median über 3 Punkte (30 m)
for i in range(1, len(hg) - 1): hm[i] = np.median(hg[i-1:i+2])
# Straßen aus den OSM-Wegen, aus denen die Linie gebaut ist (strassen.json, alle 10 m, katalanischer Name wie in OSM, namen.py), Barri
# aus orte2026.json (alle 100 m). Unbekannte und kurze Stücke unter 80 m (Kreuzungen, Plätze im Durchgang) übernehmen den Namen davor;
# Barris unter 300 m dem Vorgänger zugeschlagen und auf den nächsten Straßenwechsel gelegt.
st = json.load(open("strassen.json"))
orte = json.load(open("orte2026.json"))
gx = gpx_of(np.minimum(grid, L))
roads = [name({"name": st[min(len(st) - 1, int(round(x / 10)))][1]}) for x in gx]
qs = [ORT(orte[min(len(orte) - 1, int(round(x / 100)))]) for x in gx]
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
# Getränkestellen laut Streckenplan 2026 des Veranstalters (Tabelle „Avit. bàsic / Avit. complert“, Kilometerangabe wie dort; das
# Reglement 2027 nennt dieselben Kilometer „aproximadament“, km 30 statt 30,8). Alle mit WC und Sanität.
AV = [(5, "b", "Wasser, Iso"), (7.5, "b", "Wasser, Iso"), (10, "b", "Wasser, Iso"), (12.5, "b", "Wasser und Iso in Flaschen, Gel"),
      (15, "c", "Wasser, Iso, Bananen, Nüsse"), (17.5, "b", "Wasser und Iso in Flaschen, Gel"),
      (20, "c", "Wasser, Iso, Bananen, Trauben, Nüsse, persönliche Mehrwegflaschen"), (22.5, "b", "Wasser, Iso"),
      (25, "c", "Wasser, Iso, Cola, Bananen, Trauben, Nüsse, Fruchtgummi"), (27.5, "b", "Wasser und Iso in Flaschen, Gel"),
      (30.8, "c", "Wasser, Iso, Cola, Bananen, Trauben, Nüsse, Fruchtgummi, Kühlstation"), (32.5, "b", "Wasser, Iso"),
      (35, "c", "Wasser, Iso, Cola, Bananen, Trauben, Nüsse, Fruchtgummi, Kühlstation, persönliche Mehrwegflaschen"),
      (37.5, "b", "Wasser und Iso in Flaschen, Gel"), (40, "c", "Wasser, Iso, Cola, Bananen, Trauben, Nüsse, Fruchtgummi, Kühlstation")]
def kmtext(x): return (f"{x:.1f}".replace(".", ",")).replace(",0", "")
marks = []
for km, art, was in AV:
    v = art == "c"
    marks.append({"k": int(round(km * 1000)), "s": "Verpflegung" if v else "Getränke", "c": "food" if v else "water",
                  "n": f"{'Verpflegung' if v else 'Getränke'} km {kmtext(km)} ({was})"})
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
for w in (50, 200, 1000):
    u, d_, gabs, xmax, gmin, xmin, gmax = asc(w)
    print(f"Fenster {w:5d} m: ↑ {u:5.1f} m  ↓ {d_:5.1f} m  steilste bergauf {gmax:4.1f} % bei km {xmax/1000:.2f}, bergab {gmin:4.1f} % bei km {xmin/1000:.2f}")
raw = np.array(c["raw"]); kr = np.array(c["k"]); sel = kr <= L
roh = round(np.clip(np.diff(raw[sel]), 0, None).sum())
open("rohdaten.txt", "w").write(str(roh))
print("Rohdaten Punkt für Punkt ↑", roh, "m; bereinigt ↑", round(np.clip(np.diff(hc[sel]), 0, None).sum(), 1), "m")
print("Höhe min/max", round(hm.min(), 1), round(hm.max(), 1), "bei km", grid[np.argmin(hm)]/1000, grid[np.argmax(hm)]/1000, "Start", round(at(0), 1), "Ziel", round(at(L), 1))
print("Straßenabschnitte", len(segs), "Marken", len(marks), "Brücken", len(bridges))
for sg in segs: print("  ", sg)
print("Marken:", [(m["k"], m["s"]) for m in marks])
