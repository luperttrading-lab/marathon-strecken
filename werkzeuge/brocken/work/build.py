# Höhen im 10-m-Raster, Wege, Marken und Brücken -> data.json (geht als const D in brocken/index.html). Muster: werkzeuge/freiburg/work/build.py
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
# Wege aus OSM unter der Linie (strassen.json, alle 10 m, Namen wie in OSM), Orte aus OSM (orte2026.json, alle 100 m: Ortschaften der
# Gemeinden Wernigerode und Ilsenburg). Viele Wald- und Wanderwege haben in OSM keinen Namen; längere Stücke ohne Namen heißen nach einem
# Ort an der Strecke (ERSATZ, offizielle Meter; Orte aus der Streckenkarte des Veranstalters und aus OSM: Haidknüll, Öhrenfeld/Tänntal,
# Gelber Brink, Brockenplateau, Hanneckenbruch, Mönchsbuche, Schwengskopf, Kuhbornteich). Die Straße „Ilsetal“ heißt auch dort so, wo
# OSM sie zwischen Waldhotel und Schutzhütte ohne Namen führt. Kurze Stücke unter 80 m (Kreuzungen, Brücken) übernehmen den Namen davor;
# Orte unter 300 m dem Vorgänger zugeschlagen und auf den nächsten Wegwechsel gelegt.
ERSATZ = [(1220, 3690, "Waldweg am Haidknüll"), (3690, 5290, "Waldweg Öhrenfeld – Tänntal"), (6440, 7980, "Waldweg nach Ilsenburg"),
          (9370, 10650, "Ilsetal"), (13700, 14640, "Waldweg am Gelben Brink"), (18950, 19300, "Brockenplateau"),
          (32530, 33940, "Waldweg zum Hanneckenbruch"), (35990, 38540, "Waldweg über die Mönchsbuche"),
          (38550, 41150, "Waldweg über den Schwengskopf"), (41150, 1e9, "Waldweg am Kuhbornteich")]
st = json.load(open("strassen.json")); orte = json.load(open("orte2026.json"))
gx = gpx_of(np.minimum(grid, L))
def name_an(x, kk):
    nm = st[min(len(st) - 1, int(round(x / 10)))][2] or ""
    if nm: return nm
    for a, b, n in ERSATZ:
        if a <= kk < b: return n
    return ""
roads = [name_an(x, kk) for x, kk in zip(gx, grid)]
qs = [orte[min(len(orte) - 1, int(round(x / 100)))][1] for x in gx]
def glaetten(v, mind):
    for i in range(1, len(v)): v[i] = v[i] or v[i - 1]
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[j + 1] == v[i]: j += 1
        if i > 0 and (j + 1 - i) * STEP < mind and j < len(v) - 1: v[i:j + 1] = [v[i - 1]] * (j + 1 - i)
        i = j + 1
    for i in range(len(v) - 2, -1, -1): v[i] = v[i] or v[i + 1]
    return v
roads = glaetten(roads, 80)
qs = glaetten(qs, 300)
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
# geschätzte Stücke (schraffiert): Brücken, auf denen die Gerade zwischen den Enden mehr als 1 m über dem DGM liegt (clean.py)
bridges = [{"a": round(r["a"]), "b": round(r["b"]), "name": r["name"] or r["kind"], "kind": r["kind"]} for r in c["regions"]]
bridges.sort(key=lambda x: x["a"])
# Verpflegung (stationen.py): Lage aus dem Ort, Kilometer und Ausgabezeit laut Veranstalter
def kmtext(x): return f"{x:.1f}".replace(".", ",")
marks = []
for art, name, km_v, zeit, lm, her, ab in json.load(open("stationen.json")):
    m = int(round(float(official(lm))))
    zus = " (gelbe Schutzjacken für die Brockenpassage, Rückgabe am Knochenbrecher)" if name == "Eiserner Tisch" else ""
    if art == "water":
        n = f"Tränke (nur Getränke), km {kmtext(m / 1000)}, {name}{zus}; laut Veranstalter km {km_v}, geöffnet {zeit} Uhr"
        marks.append({"k": m, "s": "Getränke", "c": "water", "n": n})
    else:
        n = f"Verpflegung, km {kmtext(m / 1000)}, {name}; laut Veranstalter km {km_v}, geöffnet {zeit} Uhr"
        marks.append({"k": m, "s": "Verpflegung", "c": "food", "n": n})
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
for m in marks: print("  ", m["k"], m["s"], "|", m["n"])
