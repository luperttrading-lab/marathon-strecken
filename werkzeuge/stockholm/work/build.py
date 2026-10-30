# Höhen im 10-m-Raster, Straßen, Marken und Brücken -> data.json (geht als const D in stockholm/index.html). Muster: werkzeuge/wien/work/build.py
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
# Straßen aus den OSM-Wegen unter der Linie (strassen.json, alle 10 m, Namen wie in OSM), Stadtteil aus den Stadsdelar
# (orte2026.json, alle 100 m). Unbekannte und kurze Stücke unter 80 m (Kreuzungen) übernehmen den Namen davor; Stadtteile unter
# 300 m dem Vorgänger zugeschlagen und auf den nächsten Straßenwechsel gelegt. Ab dem Tor des Stadions (Linienmeter 41 890, die
# Linie verlässt dort Drottning Sofias Väg) heißt das Stück „Stockholms Stadion“ (Laufbahn bis zum Ziel).
st = json.load(open("strassen.json")); orte = json.load(open("orte2026.json"))
gx = gpx_of(np.minimum(grid, L))
STADION = 41890.0
roads = ["Stockholms Stadion" if x >= STADION else (st[min(len(st) - 1, int(round(x / 10)))][1] or "") for x in gx]
# Riddarhusgränd und Riddarhustorget liegen in Gamla stan; die Grenze zum Inselchen Riddarholmen verläuft im Wasser daneben
ORT_MAP = {"Gamla stan / Riddarholmen": "Gamla stan"}
qs = [ORT_MAP.get(orte[min(len(orte) - 1, int(round(x / 100)))][1], orte[min(len(orte) - 1, int(round(x / 100)))][1]) for x in gx]
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
# geschätzte Stücke (schraffiert): mit den GPX-Höhen keine (clean.py), mit FABDEM die gerade gezogenen Brücken
bridges = [{"a": round(r["a"]), "b": round(r["b"]), "name": r["name"] or r["kind"], "kind": r["kind"]} for r in c["regions"]]
bridges.sort(key=lambda x: x["a"])
# Getränke und Verpflegung an der km-Angabe des Veranstalters (Participant Information 2026, „Hydration & energy“; die Orte passen
# zur Linie, siehe UEBERGABE.md): 13 Getränkestellen, an 1, 3, 5, 7, 8, 9 und 12 nur Wasser, sonst zuerst Enervit G Sport (Orange)
# und dahinter Wasser; 10 Energiestellen, „kurz vor einer Getränkestelle“, zwei davon ohne Getränkestelle (Hornsgatan km 26,1
# Apfelschnitze, Kornhamnstorg km 36 Red Bull). Nicht übernommen: der persönliche Verpflegungsdienst von Enervit (km 6,6 / 15 /
# 37,6, nur mit gebuchtem Armband) und die Getränke in den Startfeldern.
def kmtext(x): return f"{x:.1f}".replace(".", ",").replace(",0", "")
GETR = [(3.5, "Östra Järnvägsgatan", False), (5.7, "Skeppsbron", True), (8.6, "Karlaplan", False), (12.9, "Sjöhistoriska", True),
        (16.9, "Skansen", False), (19.9, "Skeppsbron", True), (24.2, "Magnus Ladulåsgatan", False), (26.9, "Varvsgatan", False),
        (28.6, "Rålambshovsparken", False), (31.8, "Fleminggatan", True), (34.5, "Östra Järnvägsgatan", True), (36.7, "Skeppsbron", False),
        (39.8, "Karlaplan", True)]
ENERGIE = {8.6: "Bananen", 16.9: "Enervit-Gel (Cola)", 24.2: "Salzgurken", 26.1: "Apfelschnitze", 28.6: "Traubenzucker",
           31.8: "Gemüsebrühe", 34.5: "Bananen", 36.0: "Red Bull", 36.7: "Kaffee", 39.8: "Cola"}
ORT_E = {26.1: "Hornsgatan", 36.0: "Kornhamnstorg"}
marks = []
for km, wo, sport in GETR:
    trinken = "Enervit G Sport, Wasser" if sport else "Wasser"
    if km in ENERGIE:
        marks.append({"k": round(km * 1000), "s": "Verpflegung", "c": "food", "n": f"Verpflegung km {kmtext(km)}, {wo} ({ENERGIE[km]}; {trinken})"})
    else:
        marks.append({"k": round(km * 1000), "s": "Getränke" if sport else "Wasser", "c": "water", "n": f"{'Getränke' if sport else 'Wasser'} km {kmtext(km)}, {wo} ({trinken})"})
for km, wo in ORT_E.items():
    marks.append({"k": round(km * 1000), "s": "Verpflegung", "c": "food", "n": f"Verpflegung km {kmtext(km)}, {wo} ({ENERGIE[km]})"})
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
