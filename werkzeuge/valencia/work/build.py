# Höhen im 10-m-Raster, Straßen, Marken und Brücken -> data.json (geht als const D in valencia/index.html)
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
# Straßen aus den OSM-Wegen unter der Linie (strassen.json, alle 10 m, valencianischer Name wie in OSM, namen.py), Distrikt aus
# den Flächen der Stadt (orte2026.json, alle 100 m). Unbekannte und kurze Stücke unter 80 m (Kreuzungen) übernehmen den Namen
# davor; Distrikte unter 300 m dem Vorgänger zugeschlagen und auf den nächsten Straßenwechsel gelegt.
st = json.load(open("strassen.json")); sgx = np.array([o[0] for o in st])
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
# Ziel: ab der Rampe hinunter ins alte Flussbett (Zufahrt ohne Namen, km 41,7) läuft die Strecke durch die Ciutat de les Arts i
# les Ciències und auf dem Steg über dem Wasser unter dem Pont de Montolivet hindurch; OSM nennt dort nur die Brücke darüber.
ziel_ab = next(float(official(o[0])) for o in st if float(official(o[0])) > 41600 and not o[1])
roads = ["Ciutat de les Arts i les Ciències" if x >= ziel_ab - 5 else r for x, r in zip(grid, roads)]
print("Ziel-Abschnitt ab km", round(ziel_ab / 1000, 3))
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
# Getränkestellen laut Google-Karte des Veranstalters (Lage, auf der Linie geeicht) und Streckenplan 2026 (Angebot, km-Angabe):
# km 5,5 / 10 / 14,5 / 18,7 Wasser (Aquabona, Flasche) und Aquarius (Becher); km 23 / 28,3 / 33,1 / 37,1 / 40,4 dazu Obst;
# Gel (Enervit, „Red Point“) bei km 16,2 / 25,8 / 34. Die Karte nennt km 28,2, der Plan 2026 km 28,3.
mk = json.load(open("marken.json"))
PLAN = {28.2: 28.3}
def kmtext(x): x = PLAN.get(x, x); return (f"{x:.1f}".replace(".", ",")).replace(",0", "")
marks = []
for km, s_, _ in mk["verpflegung"]:
    obst = km >= 23
    marks.append({"k": int(round(float(official(s_)))), "s": "Verpflegung" if obst else "Getränke", "c": "food" if obst else "water",
                  "n": f"{'Verpflegung' if obst else 'Getränke'} km {kmtext(km)} (Wasser, Aquarius{', Obst' if obst else ''})"})
for km, s_, _ in mk["gel"]:
    marks.append({"k": int(round(float(official(s_)))), "s": "Gel", "c": "food", "n": f"Gel km {kmtext(km)} (Enervit)"})
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
