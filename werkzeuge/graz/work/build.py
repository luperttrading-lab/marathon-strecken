# Höhen im 10-m-Raster, Straßen, Marken und Brücken -> data.json (geht als const D in graz/index.html). Kopie von
# werkzeuge/freiburg/work/build.py.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official, gpx_of
L = 42195.0; STEP = 10; HM = 21097.5
c = json.load(open("clean.json")); S = json.load(open("strecke2026.json")); R2 = S["runde2"]; DAB = S["d"][S["abzweig"]]
k = np.array(c["k"]); hc = np.array(c["h"])
grid = np.arange(0, 42200 + 1, STEP, dtype=float)
hg = np.interp(np.minimum(grid, L), k, hc)
hm = hg.copy()                                   # gleitender Median über 3 Punkte (30 m)
for i in range(1, len(hg) - 1): hm[i] = np.median(hg[i-1:i+2])
# Straßen aus den OSM-Wegen unter der Linie (strassen.json, alle 10 m, Namen wie in OSM), Bezirke aus OSM (orte2026.json, alle 100 m).
# Wege ohne Namen (Gehwegstücke an Kreuzungen, Zugang zum Ella-Flesch-Platz am Start) und Stücke unter 80 m übernehmen den Namen davor;
# Bezirke unter 300 m werden dem Vorgänger zugeschlagen (die Mur ist Bezirksgrenze, am Kai sieht orte.py sonst stückweise beide Ufer)
# und auf den nächsten Straßenwechsel bis 150 m daneben gelegt (Grieskai/Lendkai an der Erzherzog-Johann-Brücke).
st = json.load(open("strassen.json")); orte = json.load(open("orte2026.json"))
gx = gpx_of(np.minimum(grid, L))
def name_an(x):
    nm = st[min(len(st) - 1, int(round(x / 10)))][2] or ""
    if nm in ("Ella-Flesch-Platz", "Evangelimanngasse", "Weldenstraße", "Sporgasse", "Neue-Welt-Gasse", "Zweiglgasse"): nm = ""   # Querstraßen
    return nm
roads = [name_an(x) for x in gx]
qs = [orte[min(len(orte) - 1, int(round(x / 100)))][1] for x in gx]
def glaetten(v, mind, bleibt=()):
    for i in range(1, len(v)): v[i] = v[i] or v[i - 1]
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[j + 1] == v[i]: j += 1
        if i > 0 and (j + 1 - i) * STEP < mind and j < len(v) - 1 and v[i] not in bleibt: v[i:j + 1] = [v[i - 1]] * (j + 1 - i)
        i = j + 1
    for i in range(len(v) - 2, -1, -1): v[i] = v[i] or v[i + 1]
    return v
roads = glaetten(roads, 80)
qs = glaetten(qs, 300)
wechsel = [i for i in range(1, len(roads)) if roads[i] != roads[i - 1]]
for i in [i for i in range(1, len(qs)) if qs[i] != qs[i - 1]]:
    w = min(wechsel, key=lambda j: abs(j - i), default=None)
    if w is not None and 0 < abs(w - i) <= 15:
        if w > i: qs[i:w] = [qs[i - 1]] * (w - i)
        else: qs[w:i] = [qs[i]] * (i - w)
segs, prev = [], None
for x, road, q in zip(grid, roads, qs):
    if x > L: break
    if (road, q) != prev: segs.append([round(x), road, q]); prev = (road, q)
segs[0][0] = 0
# geschätzte Stücke (schraffiert): nur die Brücke der Grabenstraße auf dem Rückweg (clean.py); alle anderen Brücken sind gemessen.
bridges = [{"a": round(r["a"]), "b": round(r["b"]), "name": r["name"] or r["kind"], "kind": r["kind"]} for r in c["regions"]]
bridges.sort(key=lambda x: x["a"])
# Labestationen und Staffelübergaben (stationen.py), Lage auf etwa ±0,2 km
def kmtext(x): return f"{x:.1f}".replace(".", ",")
def strasse(kk): return roads[min(len(roads) - 1, int(round(kk / STEP)))]
marks = []
for art, nr, lm, was in json.load(open("stationen.json")):
    m = int(round(float(official(lm)))); wo = strasse(m)
    if art == "Labe":
        voll = "Bananen" in was
        inhalt = ", ".join(x for x in was if x not in ("Eigenverpflegung", "Peeroton Gel"))
        zus = []
        if "Peeroton Gel" in was:
            zus.append("Peeroton Gel" + (" (laut Seite „Labestationen“ nur hier, „Kilometer 35“)" if m > HM else " (laut Übersichtsgrafik; laut Seite „Labestationen“ gibt es Gel nur bei km 35)"))
        if "Eigenverpflegung" in was: zus.append("Eigenverpflegung für Marathonläufer")
        zus.append("Erste Hilfe")
        n = f"Labestation {nr}, km {kmtext(m / 1000)}, {wo}: {inhalt}; " + ", ".join(zus) + " (Lage nach der Übersichtsgrafik des Veranstalters, etwa ±0,2 km)"
        marks.append({"k": m, "s": "Labestation" if voll else "Getränke", "c": "food" if voll else "water", "n": n})
    else:
        etappe = {"1": "Etappe 1: ca. 10 km", "2": "Etappe 2: ca. 9,1 km", "3": "Etappe 3: ca. 12 km, Etappe 4 ins Ziel 11,1 km"}[nr]
        marks.append({"k": m, "s": f"Wechsel {nr}", "c": "relay", "n": f"Staffelübergabe {nr}, {was} ({etappe} laut Veranstalter)"})
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
