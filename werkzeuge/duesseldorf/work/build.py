# Höhen im 10-m-Raster, Straßen, Marken und Brücken -> data.json (geht als const D in duesseldorf/index.html). Muster:
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
# Straßen aus den OSM-Wegen unter der Linie (strassen.json, alle 10 m, Namen wie in OSM), Stadtteil aus den Stadtteilen der Stadt
# (orte2026.json, alle 100 m). Unbekannte und kurze Stücke unter 80 m (Kreuzungen) übernehmen den Namen davor; Stadtteile unter
# 300 m dem Vorgänger zugeschlagen und auf den nächsten Straßenwechsel gelegt.
# Die Fahrbahnen der Oberkasseler Brücke haben in OSM keinen Namen (nur die Brücke als Bauwerk). Ab dem Ende der Rheinuferpromenade
# am Johannes-Rau-Platz (km 41,76) führt ein Weg ohne Namen hinunter an den Fluss und auf der Rheinwerft ins Ziel; der Veranstalter
# nennt sie „Untere Rheinwerft“ (OSM „Rheinwerft“).
st = json.load(open("strassen.json")); orte = json.load(open("orte2026.json"))
OKB = {"142750745", "369744127"}
NAMEN = {"Rheinkniebrücke": "Reichsstraße", "Rheinwerft": "Untere Rheinwerft"}   # Reichsstraße läuft unter der Rampe der Rheinkniebrücke durch
RAMPE = float(gpx_of(41760))
gx = gpx_of(np.minimum(grid, L))
def strasse(x):
    e = st[min(len(st) - 1, int(round(x / 10)))]
    if x >= RAMPE: return "Untere Rheinwerft"
    if e[7] in OKB: return "Oberkasseler Brücke"
    return NAMEN.get(e[1], e[1]) or ""
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
# geschätzte Stücke (schraffiert): nur die Unterführung der Ernst-Gnoß-Straße unter dem Stadttor (clean.py); die Brücken sind aus dem
# Oberflächenmodell gemessen (dom.py)
NAMEN_B = {"Ernst-Gnoß-Straße": "Ernst-Gnoß-Straße unter dem Stadttor"}
bridges = [{"a": round(r["a"]), "b": round(r["b"]), "name": NAMEN_B.get(r["name"], r["name"]) or r["kind"], "kind": r["kind"]} for r in c["regions"]]
bridges.sort(key=lambda x: x["a"])
# Marken aus dem Streckenplan 2026 (stationen.py): Verpflegungspunkte (food), Erfrischungspunkte (water), Staffelwechselzonen (relay)
# mit den Orten, die der Veranstalter nennt (Wechselzonen) bzw. der Straße an der Stelle. Was es dort gibt, sagt der Veranstalter nicht
# („Eine genaue Übersicht stellen wir Dir rechtzeitig vor dem Event zur Verfügung“).
def kmtext(x): return f"{x / 1000:.1f}".replace(".", ",")
WZ = {1: "Fischerstraße", 2: "Steinstraße", 3: "Jacobistraße"}
def strasse_bei(m):
    for a, nm, q in reversed(segs):
        if a <= m: return nm
marks, nwz = [], 0
for m, art in json.load(open("stationen.json")):
    if art == "Verpflegung":
        marks.append({"k": m, "s": "Verpflegung", "c": "food", "n": f"Verpflegungspunkt ca. km {kmtext(m)}, {strasse_bei(m)}"})
    elif art == "Erfrischung":
        marks.append({"k": m, "s": "Erfrischung", "c": "water", "n": f"Erfrischungspunkt ca. km {kmtext(m)}, {strasse_bei(m)}"})
    else:
        nwz += 1
        marks.append({"k": m, "s": f"Wechsel {nwz}", "c": "relay", "n": f"Staffelwechsel {nwz} ({WZ[nwz]}, ca. km {kmtext(m)})"})
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
for m in marks: print("  ", m)
