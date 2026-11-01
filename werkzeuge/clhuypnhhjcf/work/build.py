# Höhen im 10-m-Raster, Wege, Marken und Unterführungen -> data.json (geht als const D in clhuypnhhjcf/index.html).
# Muster: werkzeuge/hannover/work/build.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official, gpx_of, L
STEP = 10
c = json.load(open("clean.json"))
k = np.array(c["k"]); hc = np.array(c["h"])
grid = np.arange(0, L + STEP, STEP, dtype=float)
hg = np.interp(np.minimum(grid, L), k, hc)
hm = hg.copy()                                   # gleitender Median über 3 Punkte (30 m)
for i in range(1, len(hg) - 1): hm[i] = np.median(hg[i-1:i+2])
# Wege aus den OSM-Wegen unter der Linie (strassen.json, alle 10 m, Namen wie in OSM: Alter Steinbacher Weg, 1., 2. und 6. Schneise,
# Rathenaustraße). Wege ohne Namen beschreibend nach dem, was daneben liegt (ERSATZ, Streckenmeter; keine amtlichen Namen):
# Uni-Gelände Philosophikum, Gießener Ring (A 485), Schiffenberger Weg (Straße 22 m daneben), Brauhofsweiher (17–25 m), Weiher (7 m).
# Kurze Stücke unter 80 m (Kreuzungen, Kreisel) übernehmen den Namen davor.
ERSATZ = [(0, 670, "Weg am Philosophikum"), (670, 1010, "Weg am Gießener Ring"), (1950, 2295, "Weg am Schiffenberger Weg"),
          (4960, 5890, "Waldweg Richtung Schiffenberg"), (5890, 6570, "Weg am Brauhofsweiher"), (6570, 7120, "Waldweg am Weiher")]
st = json.load(open("strassen.json"))
gx = gpx_of(np.minimum(grid, L))
def name_an(x, kk):
    for a, b, n in ERSATZ:
        if a <= kk < b: return n
    return st[min(len(st) - 1, int(round(x / 10)))][2] or ""
roads = [name_an(x, kk) for x, kk in zip(gx, grid)]
# Gegend: alles liegt in der Stadt Gießen (OSM admin_level 8 und 9, orte.py). Westlich des Gießener Rings „Gießen“ (Uni-Gelände
# Philosophikum, Klinikum), östlich davon der Stadtwald „Schiffenberger Wald“ (beschreibend; in OSM eine Waldfläche ohne Namen).
U = [r for r in c["regions"]]
def gegend(kk): return "Gießen" if kk < (U[0]["a"] + U[0]["b"]) / 2 or kk > (U[1]["a"] + U[1]["b"]) / 2 else "Schiffenberger Wald"
qs = [gegend(kk) for kk in grid]
def glaetten(v, mind):
    for i in range(1, len(v)): v[i] = v[i] or v[i - 1]
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[j + 1] == v[i]: j += 1
        if i > 0 and (j + 1 - i) * STEP < mind and j < len(v) - 1: v[i:j + 1] = [v[i - 1]] * (j + 1 - i)   # Ziel (Mitte) bleibt
        i = j + 1
    for i in range(len(v) - 2, -1, -1): v[i] = v[i] or v[i + 1]
    return v
roads = glaetten(roads, 80)
segs, prev = [], None
for x, road, q in zip(grid, roads, qs):
    if x > L: break
    if (road, q) != prev: segs.append([round(x), road, q]); prev = (road, q)
segs[0][0] = 0
# geschätzte Stücke (schraffiert): die Unterführung unter dem Gießener Ring, hin und zurück (clean.py)
bridges = [{"a": round(r["a"]), "b": round(r["b"]), "name": r["name"], "kind": r["kind"]} for r in c["regions"]]
bridges.sort(key=lambda x: x["a"])
# Marken: kein Rennen, also keine Verpflegung, Wellen, Staffel, Halbmarathon. Nur der höchste Punkt und die Stelle, die dem Kloster
# Schiffenberg am nächsten kommt (OSM: Gipfel „Schiffenberg“ 280,8 m, Kloster und Biergarten, 0,3 km südlich der Runde).
def kmtext(x): return f"{x:.1f}".replace(".", ",")
ih = int(np.argmax(hm[grid <= L])); kh = float(grid[ih])
r = json.load(open("dgm_10m.json")); kk = official([x[0] for x in r]); la = np.array([x[1] for x in r]); lo = np.array([x[2] for x in r])
from pyproj import Geod
_, _, dd = Geod(ellps="WGS84").inv(lo, la, np.full_like(lo, 8.7225679), np.full_like(la, 50.5558916))
ks = float(kk[int(np.argmin(dd))]); ds = float(dd.min())
marks = [{"k": round(kh), "s": "Höchster Punkt", "c": "half", "n": f"Höchster Punkt der Runde, {hm[ih]:.0f} m, km {kmtext(kh / 1000)}".replace(".", ",")},
         {"k": round(ks), "s": "Schiffenberg", "c": "half",
          "n": f"Am nächsten am Schiffenberg: Kloster, Gipfel (281 m) und Biergarten {ds / 1000:.1f} km südlich".replace(".", ",")}]
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
print("Wegabschnitte", len(segs), "Marken", marks, "Unterführungen", bridges)
for sg in segs: print("  ", sg)
