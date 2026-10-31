# Höhen im 10-m-Raster, Straßen, Marken und Brücken -> data.json (geht als const D in zuerich/index.html). Muster: werkzeuge/honolulu/work/build.py
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
# Straßen aus den OSM-Wegen unter der Linie (strassen.json, alle 10 m, Namen wie in OSM und auf den Schildern), Quartiere bzw. Gemeinden
# (orte2026.json, alle 100 m). Unbekannte und kurze Stücke unter 80 m (Kreuzungen) übernehmen den Namen davor; Quartiere unter 300 m
# dem Vorgänger zugeschlagen und auf den nächsten Straßenwechsel gelegt. Die letzten 70 m (Schoeckstrasse, 30 m, und die Fußgängerfläche
# des Sechseläutenplatzes, in OSM kein Weg mit Namen) heißen „Sechseläutenplatz“.
st = json.load(open("strassen.json")); orte = json.load(open("orte2026.json"))
gx = gpx_of(np.minimum(grid, L))
roads = [(st[min(len(st) - 1, int(round(x / 10)))][2] or "") for x in gx]
ende = min(i for i, x in enumerate(gx) if st[min(len(st) - 1, int(round(x / 10)))][1] == "Schoeckstrasse") - 1
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
roads = glaetten(roads, 80)
for i in range(ende + 1, len(roads)): roads[i] = "Sechseläutenplatz"     # nach dem Glätten: zusammen nur 70 m
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
# Geschätzte Stücke (schraffiert): keine. Die Brücken (Quaibrücke, Schanzengraben, Seestrasse über Bäche) sind aus dem Oberflächenmodell
# gemessen (clean.py).
bridges = []
# Verpflegung laut Streckenplan 2026 (plan.py: Becher-Symbole, alle Durchgänge der Linie nahe beim Symbol). Der Veranstalter nennt
# „insgesamt 12 Verpflegungsposten“ mit Wasser, isotonischen Getränken und weiteren Energiespendern, dazu Sanität und WC; der Plan zeigt
# sechs Stellen, die je zweimal passiert werden (hin und zurück). Die Stelle am Zürichhorn liegt auch neben dem ersten Kilometer
# (Linienmeter ~1500): dort nicht gezählt (sonst 13; ein Posten nach 1,5 km wäre ungewöhnlich). Lage nur aus dem Plan: Die Symbole
# stehen 60–170 m (Stadt) bzw. 240–600 m (am See) neben der Strecke, also etwa ±0,2 km bzw. ±0,5 km; in der App „ca.“.
NAMEN = [((136, 213), "Talstrasse"), ((168, 390), "Mythenquai"), ((327, 467), "Bellerivestrasse (Zürichhorn)"),
         ((152, 264), "Seestrasse bei Goldbach"), ((242, 380), "Seestrasse in Erlenbach"), ((281, 497), "Seestrasse in Feldmeilen")]
mp = json.load(open("marken_plan.json"))
def kmtext(x): return f"{x:.1f}".replace(".", ",")
marks = []
for seite, lage, abst, durch in mp["verpflegung"]:
    nm = next((n for (x, y), n in NAMEN if abs(x - lage[0]) < 3 and abs(y - lage[1]) < 3), None)
    if nm is None: continue                       # Ziel (Zielverpflegung)
    for s_ in durch:
        if s_ < 3000: continue
        k_ = round(float(official(s_)))
        marks.append({"k": k_, "s": "Verpflegung", "c": "food",
                      "n": f"Verpflegung ca. km {kmtext(k_ / 1000)}, {nm} (Wasser, isotonische Getränke, Energie; Lage aus dem Streckenplan)"})
assert len(marks) == 12, len(marks)
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
roh = round(np.clip(np.diff(hc[sel]), 0, None).sum())
open("rohdaten.txt", "w").write(str(roh))
print("Rohdaten Punkt für Punkt (bereinigt, ohne Messfenster) ↑", roh, "m; Geländemodell ohne Brücken ↑", round(np.clip(np.diff(raw[sel]), 0, None).sum(), 1), "m")
print("Höhe min/max", round(hm.min(), 1), round(hm.max(), 1), "bei km", grid[np.argmin(hm)]/1000, grid[np.argmax(hm)]/1000, "Start", round(at(0), 1), "Ziel", round(at(L), 1))
print("Straßenabschnitte", len(segs), "Marken", len(marks), "Brücken", len(bridges))
for sg in segs: print("  ", sg)
for m in marks: print("  ", m["k"], m["n"])
