# Höhen im 10-m-Raster, Straßen, Marken und geschätzte Stücke -> data.json (geht als const D in rom/index.html)
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official, gpx_of
from namen import name as strname, ort
L = 42195.0; STEP = 10
c = json.load(open("clean.json"))
k = np.array(c["k"]); hc = np.array(c["h"])
grid = np.arange(0, 42200 + 1, STEP, dtype=float)
hg = np.interp(np.minimum(grid, L), k, hc)
hm = hg.copy()                                   # gleitender Median über 3 Punkte (30 m)
for i in range(1, len(hg) - 1): hm[i] = np.median(hg[i-1:i+2])
# Straßen aus den OSM-Kanten der Linie (strassen.json, alle 10 m, namen.py), Ortsteil (Rione, Quartiere) aus orte2026.json (alle 100 m).
# Unbekannte und kurze Stücke unter 80 m (Kreuzungen) übernehmen den Namen davor; Ortsteile unter 300 m dem Vorgänger zugeschlagen
# und auf den nächsten Straßenwechsel gelegt.
st = json.load(open("strassen.json")); orte = json.load(open("orte2026.json"))
gx = gpx_of(np.minimum(grid, L))
roads = [strname(st[min(len(st) - 1, int(round(x / 10)))][1], st[min(len(st) - 1, int(round(x / 10)))][7]) for x in gx]
qs = [ort(orte[min(len(orte) - 1, int(round(x / 100)))][1]) for x in gx]
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
# Ristori und Spugnaggi laut Event Guide 2026 des Veranstalters (an der Kilometerangabe): Wasser überall, Mineralsalze ab km 15 (der
# Guide schreibt „dal rifornimento del km 15,500“, die Liste der Stellen nennt km 15,000), feste Nahrung bei km 15 und im Ziel.
def kmt(x): return f"{x:g}".replace(".", ",")
marks = []
for km in [5.3, 9.9, 15.0, 16.4, 17.45, 17.9, 20.3, 22.4, 25.0, 30.0, 31.6, 33.8, 35.5, 38.6, 39.6, 40.25]:
    if km == 15.0: marks.append({"k": 15000, "s": "Verpflegung", "c": "food", "n": "Verpflegung km 15 (Wasser, Mineralsalze, feste Nahrung)"})
    else: marks.append({"k": int(round(km * 1000)), "s": "Getränke", "c": "water", "n": f"Getränke km {kmt(km)} (Wasser{', Mineralsalze' if km > 15 else ''})"})
for km in [7.4, 10.1, 13.9, 16.5, 19.4, 23.9, 29.9, 33.6, 34.0, 36.4, 38.7, 39.8]:
    marks.append({"k": int(round(km * 1000)), "s": "Schwämme", "c": "water", "n": f"Schwämme km {kmt(km)} (Wasserbecken, Schwamm aus dem Startbeutel)"})
# Staffel Run4Rome (Lageplan der Staffel 2026): S1 km 11,000 Piazza di Monte Savello (Stützpunkt der Eichung), S2 Lungotevere Guglielmo
# Oberdan (Angabe km 23,500), S3 Viale XVII Olimpiade (Angabe km 31,400). S2 und S3 an ihrer Lage: Beginn des Lungotevere Oberdan
# und Ende des Viale XVII Olimpiade an der Viale Tiziano (die Angaben passen nicht genau zur Liste der Kilometer, siehe marken.py).
wm = json.load(open("wegmarken.json"))
s2 = int(round(float(official(wm["Piazza Monte Grappa / Lungotevere Guglielmo Oberdan"]))))
s3 = int(round(float(official(wm["Viale XVII Olimpiade / Viale Tiziano"]))))
marks += [{"k": 11000, "s": "Wechsel 1", "c": "relay", "n": "Staffelwechsel 1 (Piazza di Monte Savello, km 11)"},
          {"k": s2, "s": "Wechsel 2", "c": "relay", "n": "Staffelwechsel 2 (Lungotevere Guglielmo Oberdan; Angabe km 23,5)"},
          {"k": s3, "s": "Wechsel 3", "c": "relay", "n": "Staffelwechsel 3 (Viale XVII Olimpiade; Angabe km 31,4)"}]
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
print("Straßenabschnitte", len(segs), "Marken", len(marks), "Geschätzt", len(bridges), bridges)
for sg in segs: print("  ", sg)
