# Höhen im 10-m-Raster, Straßen, Marken und geschätzte Stücke -> data.json (geht als const D in luzern/index.html).
# Muster: werkzeuge/zuerich/work/build.py
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
# Straßen aus den OSM-Wegen unter der Linie (strassen.json, alle 10 m, Namen wie in OSM und auf den Schildern), Gemeinden und Ortschaften
# (orte2026.json, alle 100 m). Unbekannte und kurze Stücke unter 50 m (Kreuzungen, Kreisel; 50 statt 80 m wie in Zürich, damit in der
# Altstadt Krongasse, Reussbrücke und Kramgasse einzeln erscheinen) übernehmen den Namen davor; Orte unter 300 m
# dem Vorgänger zugeschlagen und auf den nächsten Straßenwechsel gelegt. Von Hand benannt (nach Linienmetern):
#   Veloweg Horw–Hergiswil (hin, vom Seerosenweg bis zum Kreisel Schlüssel; in OSM ohne Namen, Name aus der Sperrliste des Veranstalters),
#   Hergiswilerstrasse (zurück, Kreisel Schlüssel bis Kreisel Hinterbach, mit Tunnel; in OSM nur „4“, Name aus der Sperrliste),
#   Fuss- und Radweg (Horw Brändi bis Horwerstrasse, in OSM ohne Namen), thermoplan arena (Durchlauf Stadion, OSM-Fläche des Stadions),
#   KKL (Durchlauf, OSM-Fläche des Gebäudes) und Verkehrshaus (Zielgelände, OSM-Fläche des Museums).
st = json.load(open("strassen.json")); orte = json.load(open("orte2026.json"))
VON_HAND = [(12870, 14200, "Veloweg Horw–Hergiswil"), (30960, 32200, "Hergiswilerstrasse"), (34930, 35590, "Fuss- und Radweg"),
            (35960, 36190, "thermoplan arena"), (39160, 39270, "KKL"), (42660, 43000, "Verkehrshaus")]
def strasse(x):
    for a, b, n in VON_HAND:
        if a <= x <= b: return n
    return st[min(len(st) - 1, int(round(x / 10)))][2] or ""
gx = gpx_of(np.minimum(grid, L))
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
roads = glaetten(roads, 50)
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
# Geschätzte Stücke (schraffiert, clean.py): überdeckte Seestrasse in Hergiswil (zweimal je hin und zurück), Tunnel der Hergiswilerstrasse
# (nur zurück) und die Brücke der St. Niklausenstrasse unter Bäumen. Alle übrigen Brücken sind aus dem Oberflächenmodell gemessen.
bridges = []
for r in c["regions"]:
    if r["art"] == "überdeckt":
        lang = r["b"] - r["a"]
        nm = "Tunnel Hergiswilerstrasse" if not r["name"] else ("Seestrasse, überdeckt" if lang > 150 else "Seestrasse")
        kind = "Tunnel" if (lang > 150 or not r["name"]) else "Unterführung"
        bridges.append({"a": round(r["a"]), "b": round(r["b"]), "name": nm, "kind": kind})
    elif r["art"] == "Brücke geschätzt":
        bridges.append({"a": round(r["a"]), "b": round(r["b"]), "name": r["name"], "kind": "Brücke"})
bridges.sort(key=lambda b: b["a"])
# Verpflegung laut Verpflegungsplan des Veranstalters (SwissCityMarathon-Lucerne_Verpflegungsplan.pdf, 03.07.2025, für den Kurs seit
# 2025; die Seite „Verpflegung“ verlinkt ihn im Oktober 2026 weiter): Marathon bei km 4, 8, 11, 15, 17,5, 21, 23,5, 27, 30, 34, 35, 37, 39.
# 15/30, 17,5/27 und 21/23,5 sind dieselben Stellen auf Hin- und Rückweg (Halbmarathon-Spalte: 4, 8, 11, 13, 14, 16, 18). Lage nur als
# Kilometerzahl, keine Karte: auf etwa 0,2 km. Wasser und Getränke ohne Essen als „water“, mit Riegel, Banane oder Gel als „food“.
SP = "SPONSER Competition"
VP = [(4000, "water", f"Wasser, {SP}"), (8000, "food", f"Wasser, {SP}, Riegel, Banane"), (11000, "water", "Wasser"),
      (15000, "food", f"Wasser, {SP}, Riegel, Banane, Gel"), (17500, "food", f"Wasser, {SP}, Riegel, Banane, Gel"),
      (21000, "food", f"Wasser, {SP}, Riegel, Banane, Gel"), (23500, "food", f"Wasser, {SP}, Riegel, Banane, Gel"),
      (27000, "food", f"Wasser, {SP}, Riegel, Banane, Gel"), (30000, "food", f"Wasser, {SP}, Riegel, Banane, Gel"),
      (34000, "food", f"Wasser, {SP}, Riegel, Banane"), (35000, "water", "Wasser, Cola"),
      (37000, "food", f"Wasser, {SP}, Riegel, Banane, Gel"), (39000, "water", f"Wasser, {SP}")]
def kmtext(x): return f"{x:g}".replace(".", ",")
def seg_at(x):
    s_ = [sg for sg in segs if sg[0] <= x][-1]; return s_[1], s_[2]
marks = []
for k_, c_, was in VP:
    stra, ort = seg_at(k_)
    s_ = "Verpflegung" if c_ == "food" else ("Wasser" if was == "Wasser" else "Getränke")
    marks.append({"k": k_, "s": s_, "c": c_, "n": f"{s_} km {kmtext(k_ / 1000)}, {stra}, {ort} ({was})"})
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
print("Rohdaten Punkt für Punkt (bereinigt, ohne Messfenster) ↑", roh, "m ↓", round(-np.clip(np.diff(hc[sel]), None, 0).sum()), "m; Geländemodell ohne Bereinigung ↑",
      round(np.clip(np.diff(raw[sel]), 0, None).sum(), 1), "m")
print("Höhe min/max", round(hm.min(), 1), round(hm.max(), 1), "bei km", grid[np.argmin(hm)]/1000, grid[np.argmax(hm)]/1000, "Start", round(at(0), 1), "Ziel", round(at(L), 1))
print("Straßenabschnitte", len(segs), "Marken", len(marks), "geschätzte Stücke", len(bridges))
for sg in segs: print("  ", sg)
for m in marks: print("  ", m["k"], m["n"])
for b in bridges: print("  ", b)
