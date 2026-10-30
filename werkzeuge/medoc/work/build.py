# Höhen im 10-m-Raster, Wege, Marken und Brücken -> data.json (geht als const D in medoc/index.html)
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
# Wege aus OSM (strassen.json, alle 10 m; ohne Namen nach dem nächsten Château bzw. Weiler, namen.py), Gemeinde aus ADMIN
# EXPRESS (orte2026.json, alle 100 m). Unbekannte und kurze Stücke unter 80 m übernehmen den Namen davor; Gemeinden unter 300 m
# dem Vorgänger zugeschlagen und auf den nächsten Wegwechsel gelegt. Die letzten 150 m (Zielgerade auf dem Quai, in OSM ein
# Hofweg ohne Namen neben dem Quai) heißen wie der Quai.
st = json.load(open("strassen.json")); orte = json.load(open("orte2026.json"))
gx = gpx_of(np.minimum(grid, L))
roads = [st[min(len(st) - 1, int(round(x / 10)))][1] or "" for x in gx]
qs = [orte[min(len(orte) - 1, int(round(x / 100)))][1] for x in gx]
for i, x in enumerate(grid):
    if x >= L - 160 or x < 20: roads[i] = "Quai Jean Fleuret"   # Startlinie: die ersten 10 m liegen in OSM noch auf dem Quai Antoine Ferchaud
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
def weg_bei(x): return [s_[1] for s_ in segs if s_[0] <= x][-1]
# Einzige Brücke: D 2 (Route de Bordeaux) über die Jalle du Breuil, Grenze Pauillac/Saint-Estèphe (OSM-API, Bach 5 m neben der Brücke)
BNAME = {26: "Jalle du Breuil"}
bridges = [{"a": round(r["a"]), "b": round(r["b"]), "name": BNAME.get(int(r["a"] // 1000), weg_bei((r["a"] + r["b"]) / 2)), "kind": r["kind"]} for r in c["regions"]]
bridges.sort(key=lambda x: x["a"])
# Marken: Lage aus der OpenRunner-Karte des Veranstalters (marken.json, auf die Linie projiziert, offizielle km).
#  - Verpflegungsstände mit Namen und km laut Plaquette Prestige 2026 (S. 12), Lage am Wasser-Punkt der Karte dazu (Cave La Rose:
#    keine Wasser-Marke in der Karte, Lage nach OSM, 16 m neben der Linie). Laut Läuferheft 2026 gibt es an den Ständen Wasser,
#    Cola, Orangen, Bananen, süße und salzige Kekse, Zucker und Energieriegel.
#  - „Rencontres gustatives insolites“ (Plaquette und Karte): Frühstück km 3, Cannelés km 21, Austern km 37, Entrecôte km 38,
#    Käse km 40, Eis km 41.
#  - Weinproben („Dégustation“ in der Karte, ohne Namen des Châteaux).
M = json.load(open("marken.json")); P = M["punkte"]
def bei(art, km, tol=0.6):
    kand = [p for p in P if p["art"] == art and abs(p["km"] - km) <= tol]
    assert kand, (art, km); return min(kand, key=lambda p: abs(p["km"] - km))["km"]
def kmtext(x): return f"{x:.1f}".replace(".", ",")
STAENDE = [("Château Grand-Puy-Lacoste", 3.06), ("Château Larose-Trintaudon", 6.71), ("Château Lagrange", 10.17), ("Beychevelle", 12.43),
           ("Château Ducru-Beaucaillou", 14.27), ("Saint-Julien", 16.26), ("Château Pichon-Longueville", 17.86), ("Cave La Rose Pauillac", None),
           ("Château d'Armailhac", 23.66), ("Château Lafite-Rothschild", 25.60), ("Château Lafon-Rochet", 27.68), ("Le Crock", 30.62),
           ("Château Tronquoy-Lalande", 33.12), ("Château Phélan-Ségur", 34.11), ("Château Montrose", 37.19), ("Gironde", 39.16)]
marks = []
for n, km in STAENDE:
    km = bei("Bouteille d'eau", km, 0.05) if km else next(s_["osm"]["km"] for s_ in M["staende"] if s_["name"] == "Cave La Rose Pauillac")
    marks.append({"k": round(km * 1000), "s": "Verpflegung", "c": "food", "n": f"Verpflegung km {kmtext(km)} ({n}): Wasser, Cola, Obst, Kekse"})
for art, s_, n in (("Petit déjeuner", "Frühstück", "Frühstück"), ("Cannelés", "Cannelés", "Cannelés (Gebäck aus Bordeaux)"), ("Huîtres", "Austern", "Austern"),
                   ("Entrecôte", "Entrecôte", "Entrecôte"), ("Fromage", "Käse", "Käse"), ("Glaces", "Eis", "Eis")):
    km = next(p["km"] for p in P if p["art"] == art)
    marks.append({"k": round(km * 1000), "s": s_, "c": "food", "n": f"{n} km {kmtext(km)}"})
for p in P:
    if p["art"] == "Dégustation": marks.append({"k": round(p["km"] * 1000), "s": "Wein", "c": "water", "n": f"Weinprobe km {kmtext(p['km'])}"})
marks.append({"k": 21098, "s": "Halbmarathon", "c": "half", "n": "Halbmarathon"})
marks.sort(key=lambda m: m["k"])
data = {"len": L, "step": STEP, "h": [int(round(v * 100)) for v in hm], "streets": segs, "marks": marks, "bridges": bridges}
json.dump(data, open("data.json", "w"), ensure_ascii=False, separators=(",", ":"))
def at(x): return float(np.interp(x, grid, hm))
def asc(w):
    xs = grid[grid <= L]; gr = np.array([(at(min(x + w/2, L)) - at(max(x - w/2, 0))) / (min(x + w/2, L) - max(x - w/2, 0)) for x in xs])
    dh = (gr[1:] + gr[:-1]) / 2 * STEP
    return dh[dh > 0].sum(), -dh[dh < 0].sum(), xs[np.argmax(gr)], gr.min()*100, xs[np.argmin(gr)], gr.max()*100
for w in (50, 100, 200, 1000):
    u, d_, xmax, gmin, xmin, gmax = asc(w)
    print(f"Fenster {w:5d} m: ↑ {u:5.1f} m  ↓ {d_:5.1f} m  steilste bergauf {gmax:4.1f} % bei km {xmax/1000:.2f}, bergab {gmin:4.1f} % bei km {xmin/1000:.2f}")
raw = np.array(c["raw"]); kr = np.array(c["k"]); sel = kr <= L
roh = round(np.clip(np.diff(raw[sel]), 0, None).sum())
open("rohdaten.txt", "w").write(str(roh))
print("Rohdaten Punkt für Punkt ↑", roh, "m; bereinigt ↑", round(np.clip(np.diff(hc[sel]), 0, None).sum(), 1), "m")
print("Höhe min/max", round(hm.min(), 1), round(hm.max(), 1), "bei km", grid[np.argmin(hm)]/1000, grid[np.argmax(hm)]/1000, "Start", round(at(0), 1), "Ziel", round(at(L), 1))
print("Wegabschnitte", len(segs), "Marken", len(marks), "Brücken", bridges)
for sg in segs: print("  ", sg)
