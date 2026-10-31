# Höhen im 10-m-Raster, Straßen, Marken und Brücken -> data.json (geht als const D in freiburg/index.html). Muster: werkzeuge/hannover/work/build.py
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
# Straßen aus den OSM-Wegen unter der Linie (strassen.json, alle 10 m, Namen wie in OSM), Stadtteile aus OSM (orte2026.json, alle
# 100 m). Wege ohne Namen bekommen den Namen aus der Lage (ERSATZ, Linienmeter der Runde; Rad- und Fußwege in Parks, Wege am
# Messplatz); Wegenamen in Klammern folgen der Liste der gesperrten Straßen in der Anwohnerinformation 2026 („Fahrradweg parallel zur
# Emma-Herwegh-Straße“, „FR1 – Radweg“, „Verschiedene Wege im Dietenbachpark“, „Vorplatz“, „Hirzbergstraße“). Unbekannte und kurze
# Stücke unter 80 m (Kreuzungen) übernehmen den Namen davor; Stadtteile unter 300 m dem Vorgänger zugeschlagen und auf den nächsten
# Straßenwechsel gelegt.
ERSATZ = [(0, 70, "Neuer Messplatz"), (1960, 2620, "Seepark"), (3150, 3660, "Radweg an der Emma-Herwegh-Straße"),
          (3840, 4050, "Radweg an der Dreisam"), (4870, 5370, "Dietenbachpark"), (6610, 6910, "Weg am Dorfbach"),
          (13180, 13430, "Andlawstraße"), (14100, 14400, "Alter Messplatz"), (14400, 14690, "Hirzbergstraße"),
          (17860, 18100, "Wiwilíbrücke"), (21520, 1e9, "Neuer Messplatz")]
def runde(lm):    # Linienmeter -> Linienmeter in der Runde (Rückweg über den Messplatz: hinter dem Abzweig)
    return lm - R2 if lm >= R2 else (lm if lm <= DAB else DAB + 1)
st = json.load(open("strassen.json")); orte = json.load(open("orte2026.json"))
gx = gpx_of(np.minimum(grid, L))
def name_an(x):
    nm = st[min(len(st) - 1, int(round(x / 10)))][2] or ""
    p = runde(x)
    for a, b, n in ERSATZ:
        if a <= p < b and (not nm or n in ("Neuer Messplatz", "Wiwilíbrücke")): return n
    return nm
roads = [name_an(x) for x in gx]
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
# geschätzte Stücke (schraffiert): die zwei Fußgängerunterführungen je Runde (clean.py), gerade zwischen den gemessenen Enden.
# Die Brücken sind aus dem DOM gemessen und zählen nicht dazu.
bridges = [{"a": round(r["a"]), "b": round(r["b"]), "name": r["name"] or r["kind"], "kind": r["kind"]} for r in c["regions"]]
bridges.sort(key=lambda x: x["a"])
# Verpflegung, Wasser und Wechselstellen (stationen.py, je Runde), Lage auf etwa ±0,2 km
def kmtext(x): return f"{x:.1f}".replace(".", ",")
def strasse(kk): return roads[min(len(roads) - 1, int(round(kk / STEP)))]
marks = []
for art, name, p, ab in json.load(open("stationen.json")):
    for rd, lm in ((1, p if p <= DAB else DAB), (2, R2 + p)):
        m = int(round(float(official(lm)))); wo = strasse(m)
        if art == "Verpflegung":
            km_v = round(official(p) / 1000 * 2) / 2 if not name else 21
            extra = "Wasser, Bananen, isotonisches Getränk" + (", Gele" if abs(km_v - 15) < 1 else "") + ", Eigenverpflegung"
            rk = " der Runde" if rd == 2 else ""
            n = f"Verpflegung, km {kmtext(m / 1000)}, {wo} ({extra}; Starterinformation: km {kmtext(km_v).replace(',0', '')}{rk})"
            if name: n = (f"Verpflegung, km {kmtext(m / 1000)}, am Messplatz (laut Streckenplan vor dem Zieleinlauf; {extra}; Starterinformation: km 21"
                          + (", also vor der zweiten Runde)" if rd == 1 else "; in der zweiten Runde kurz vor dem Ziel)"))
            marks.append({"k": m, "s": "Verpflegung", "c": "food", "n": n})
        elif art == "Wasser":
            ganter = abs(official(p) / 1000 - 17.5) < 0.7
            n = f"Wasser, km {kmtext(m / 1000)}, {wo}" + (" (dazu alkoholfreies Bier und Weizen von Ganter und Cola; Starterinformation: km 17,5"
                                                          + (" der Runde)" if rd == 2 else ")") if ganter else "")
            marks.append({"k": m, "s": "Wasser", "c": "water", "n": n})
        else:
            # Wechselstellen des badenova Schülermarathons: seit 31.10.2026 nicht mehr in der App (Hauptsitzung). Als „relay“
            # zeigten sie den Staffel-Schalter, obwohl es keine Marathonstaffel gibt; Schüler laufen nur eine Runde.
            continue
            b, wn = name.split("|")
            marks.append({"k": m, "s": f"Wechsel {b}", "c": "relay",
                          "n": f"Wechselstelle {b} des badenova Schülermarathons ({wn}; Staffel aus sieben Schülern über die Runde, Start 11:00 und 11:15 Uhr)"})
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
