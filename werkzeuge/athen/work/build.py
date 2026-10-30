# Höhen im 10-m-Raster, Straßen, Marken und geschätzte Stücke -> data.json (geht als const D in athen/index.html)
import json
import numpy as np
from common import official, gpx_of
L = 42195.0; STEP = 10
c = json.load(open("clean.json"))
k = np.array(c["k"]); hc = np.array(c["h"])
grid = np.arange(0, 42200 + 1, STEP, dtype=float)
hg = np.interp(np.minimum(grid, L), k, hc)
hm = hg.copy()                                   # gleitender Median über 3 Punkte (30 m)
for i in range(1, len(hg) - 1): hm[i] = np.median(hg[i-1:i+2])
# Straßen aus strassen.json (alle 10 Linienmeter, Umschrift nach ELOT 743, namen.py), Ort aus orte2026.json (alle 100 m).
# Ohne Namen: am Start das Gelände am Stadion von Marathonas (Ring um die Laufbahn und Zufahrt, gut 290 m), am Ende der Vorplatz und die
# Laufbahn des Panathinaiko-Stadions; sonst übernehmen unbenannte und kurze Stücke unter 80 m (Kreuzungen) den Namen davor.
# Orte unter 300 m dem Vorgänger zugeschlagen und auf den nächsten Straßenwechsel gelegt.
st = json.load(open("strassen.json")); orte = json.load(open("orte2026.json"))
gx = gpx_of(np.minimum(grid, L))
def strasse(x):
    o = st[min(len(st) - 1, int(round(x / 10)))]
    if not o[2] and x < 400: return "Startgelände am Stadion"
    if not o[2] and x > gpx_of(41900): return "Panathinaiko-Stadion"
    return o[2]
roads = [strasse(x) for x in gx]
qs = [orte[min(len(orte) - 1, int(round(x / 100)))][1] for x in gx]
# Ab dem Überqueren der Leoforos Vasileos Konstantinou: Stadion (Vorplatz, Einlauf, 170 m Laufbahn)
ein = int(np.argmax([r == "Leoforos Vasileos Konstantinou" for r in roads]))
for i in range(ein, len(roads)): roads[i] = "Panathinaiko-Stadion"
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
# Versorgung laut Seite „Marathon Race“ des Veranstalters (Services at start, finish and intermediate stations): 15 Stationen alle
# 2,5 km, an ihrer Kilometerangabe. Wasser (AVRA) überall; Schwämme an den Zwischenstationen 7,5 / 12,5 / … / 37,5; Isotonisch
# (Powerade) an 10 / 15 / 20 / 25 / 30 / 35 / 40; Energie-Gel (Maurten) an 10 und 20; Bananen (Dole) an 20 / 25 / 30 / 35; Cola an
# 30 / 35 / 40; Salziges an 30 und 35; Physiotherapie an 25 und 30. Mit Bananen oder Salzigem „Verpflegung“, sonst „Getränke“.
def kmt(x): return f"{x:g}".replace(".", ",")
INHALT = {5: "Wasser", 7.5: "Wasser, Schwämme", 10: "Wasser, Isotonisch, Gel", 12.5: "Wasser, Schwämme", 15: "Wasser, Isotonisch",
          17.5: "Wasser, Schwämme", 20: "Wasser, Isotonisch, Gel, Bananen", 22.5: "Wasser, Schwämme", 25: "Wasser, Isotonisch, Bananen, Physiotherapie",
          27.5: "Wasser, Schwämme", 30: "Wasser, Isotonisch, Cola, Bananen, Salziges, Physiotherapie", 32.5: "Wasser, Schwämme",
          35: "Wasser, Isotonisch, Cola, Bananen, Salziges", 37.5: "Wasser, Schwämme", 40: "Wasser, Isotonisch, Cola"}
marks = []
for km, was in INHALT.items():
    essen = "Bananen" in was or "Salziges" in was
    marks.append({"k": int(round(km * 1000)), "s": "Verpflegung" if essen else "Getränke", "c": "food" if essen else "water",
                  "n": f"{'Verpflegung' if essen else 'Getränke'} km {kmt(km)} ({was})"})
marks.append({"k": 21098, "s": "Halbmarathon", "c": "half", "n": "Halbmarathon (Zeitnahme 21,1 km)"})
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
