# Höhen im 10-m-Raster, Straßen, Stadtteile, Marken und geschätzte Stücke -> data.json (geht als const D in salzburg/index.html).
# Muster: werkzeuge/freiburg/work/build.py.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from pyproj import Transformer
from common import official, gpx_of
L = 42195.0; STEP = 10
c = json.load(open("clean.json")); k = np.array(c["k"]); hc = np.array(c["h"])
# nur streng steigende offizielle Meter (vor dem Start und nach dem Ziel ist k konstant)
sel = np.r_[True, np.diff(k) > 1e-6]; sel &= (k > 0) | (np.arange(len(k)) == np.where(k <= 0)[0][-1])
kk, hh = k[sel], hc[sel]
grid = np.arange(0, 42200 + 1, STEP, dtype=float)
hg = np.interp(np.minimum(grid, L), kk, hh)
hm = hg.copy()                                   # gleitender Median über 3 Punkte (30 m)
for i in range(1, len(hg) - 1): hm[i] = np.median(hg[i-1:i+2])
# Straßen aus den OSM-Wegen unter der Linie (strassen.json, alle 10 Linienmeter, Namen wie in OSM), Stadtteile aus OSM (orte.json, alle
# 100 Linienmeter). Wege ohne Namen: Name des Stücks davor; im Schlossbereich von Hellbrunn (Fußgängerbereich ohne Namen in OSM)
# „Hellbrunn“ wie in der Streckenbeschreibung des Veranstalters („Hellbrunner Allee | Hellbrunn | Fürstenweg“). Stücke unter 80 m
# (Kreuzungen, Plätze, Durchgänge) übernehmen den Namen davor; Stadtteile unter 300 m dem Vorgänger zugeschlagen und auf den nächsten
# Straßenwechsel gelegt.
st = json.load(open("strassen.json")); orte = json.load(open("orte.json"))
gx = gpx_of(np.minimum(grid, L))
def name_an(x):
    q = st[min(len(st) - 1, int(round(x / 10)))]
    if not q[1] and q[6] == "pedestrian" and 47.760 < q[9] < 47.765 and 13.055 < q[10] < 13.064: return "Hellbrunn"
    return q[1] or ""
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
# geschätzte Stücke (schraffiert): nur die Unterführung der Gaswerkgasse unter der Bahn (clean.py); Staatsbrücke und Lehener Brücke
# sind aus dem Oberflächenmodell gemessen und zählen nicht dazu.
bridges = [{"a": round(r["a"]), "b": round(r["b"]), "name": r["name"], "kind": r["kind"]} for r in c["regions"] if not r.get("deck")]
bridges.sort(key=lambda x: x["a"])
def kmtext(x): return f"{x:.1f}".replace(".", ",")
def strasse(kk_): return roads[min(len(roads) - 1, int(round(kk_ / STEP)))]
# Verpflegung und Wasser: Lage aus der Google-Karte des Veranstalters (Punkte „Aid Station …“, „Water Station …“, parse.py), Inhalt
# und Seite laut Verpflegungsplan („Versorgungsaufbau“, verlinkt auf der Seite „Wichtige Informationen PUMA Salzburg Marathon“ 2026).
# V5 (nur Runde 1, „Universitätsplatz – Höhe Brunnen“) fehlt in der Karte („Aid Station Finish Area“ ist die Verpflegung im Ziel):
# gelegt auf den Marktbrunnen am Universitätsplatz (OSM). Staffelwechsel aus den Punkten „Relay Zone 1/2“ der Karte.
VOLL = "Wasser, Wasser mit Kohlensäure, Powerade, Coca-Cola, Bio-Bananen, Eigenverpflegung"
M = json.load(open("marken.json"))["punkte"]
T = Transformer.from_crs(4326, 31258, always_xy=True)
lin = json.load(open("linie.json")); dl_ = np.array(lin["d"]); P = np.array(lin["pts"])
def lot(la, lo, s_von, s_bis):
    ss = np.arange(s_von, s_bis, 1.0); x, y = T.transform(np.interp(ss, dl_, P[:, 1]), np.interp(ss, dl_, P[:, 0])); px, py = T.transform(lo, la)
    i = int(np.argmin(np.hypot(x - px, y - py))); return float(ss[i]), float(np.hypot(x[i] - px, y[i] - py))
TEXT = {"Aid Station Hellbrunn": ("V1", "Hellbrunn, beidseitig", VOLL, (5.5, 26.6)),
        "Aid Station Leopoldskron": ("V2", "Leopoldskron, Kobergerweg, rechts", VOLL, (10.9, 32.0)),
        "Aid Station Maxglan": ("V3", "Maxglan, Franz-Huemer-Straße, links", VOLL, (15.2, 36.3)),
        "Aid Station Markus-Sittikus-Straße": ("V4", "Arbeiterkammer, Markus-Sittikus-Straße, rechts", VOLL, (19.4, 40.5)),
        "Water Station Gneis": ("W2", "Tennishalle, Berchtesgadener Straße, rechts", "nur Wasser", (9.8, 30.9)),
        "Water Station NaWi (2nd lap only)": ("W1", "Naturwissenschaftliche Fakultät (NaWi), rechts, erst in der zweiten Runde", "nur Wasser", (23.2,))}
marks = []
for km_plan, s, e, n, la, lo in M:
    if n in TEXT:
        kurz, wo, was, plan = TEXT[n]; m = int(round(float(official(s))))
        pk = min(plan, key=lambda p: abs(p * 1000 - m))
        art = "Wasser" if kurz.startswith("W") else "Verpflegung"
        marks.append({"k": m, "s": art, "c": "water" if art == "Wasser" else "food",
                      "n": f"{art} {kurz}, km {kmtext(m / 1000)}, {wo} ({was}; Verpflegungsplan: km {kmtext(pk)})"})
    elif n.startswith("Relay Zone"):
        m = int(round(float(official(s))))
        if n.endswith("1") and km_plan < 20: nr, wo = 1, "vor der Stiegl-Brauwelt, Läufer A an B"
        elif n.endswith("1"): nr, wo = 3, "vor der Stiegl-Brauwelt, Läufer C an D"
        else: nr, wo = 2, "Universitätsplatz, Läufer B an C (Halbmarathon-Zwischenzeit)"
        marks.append({"k": m, "s": f"Wechsel {nr}", "c": "relay", "n": f"Staffelwechsel {nr}, km {kmtext(m / 1000)}, {wo} (Veranstalter: km {kmtext(km_plan)})"})
# V5 am Marktbrunnen Universitätsplatz (OSM-Knoten 2377499299), nur Runde 1
S = json.load(open("strecke.json"))
s5, e5 = lot(47.7995343, 13.0428364, S["B1"], S["B1"] + 400); m5 = int(round(float(official(s5))))
print(f"V5 Marktbrunnen: Linienmeter {s5:.0f}, {e5:.1f} m neben der Linie, km {m5 / 1000:.3f}")
marks.append({"k": m5, "s": "Verpflegung", "c": "food",
              "n": f"Verpflegung V5, km {kmtext(m5 / 1000)}, Universitätsplatz, Höhe Brunnen, links, nur in der ersten Runde (Wasser, Wasser mit Kohlensäure, Powerade, Bio-Bananen, Eigenverpflegung; Verpflegungsplan: km 21,2)"})
marks.append({"k": 21098, "s": "Halbmarathon", "c": "half", "n": "Halbmarathon"})
marks.sort(key=lambda m: m["k"])
data = {"len": L, "step": STEP, "h": [int(round(v * 100)) for v in hm], "streets": segs, "marks": marks, "bridges": bridges}
json.dump(data, open("data.json", "w"), ensure_ascii=False, separators=(",", ":"))
# Kontrollen
def at(x): return float(np.interp(x, grid, hm))
def asc(w):
    xs = grid[grid <= L]; gr = np.array([(at(min(x + w/2, L)) - at(max(x - w/2, 0))) / (min(x + w/2, L) - max(x - w/2, 0)) for x in xs])
    dh = (gr[1:] + gr[:-1]) / 2 * STEP
    return dh[dh > 0].sum(), -dh[dh < 0].sum(), xs[np.argmax(gr)], gr.min()*100, xs[np.argmin(gr)], gr.max()*100
for w in (50, 100, 200, 1000):
    u, d_, xmax, gmin, xmin, gmax = asc(w)
    print(f"Fenster {w:5d} m: ↑ {u:5.1f} m  ↓ {d_:5.1f} m  steilste bergauf {gmax:4.1f} % bei km {xmax/1000:.2f}, bergab {gmin:4.1f} % bei km {xmin/1000:.2f}")
raw = np.array(c["raw"])[sel]
roh = round(np.clip(np.diff(raw), 0, None).sum())
open("rohdaten.txt", "w").write(str(roh))
print("Rohdaten Punkt für Punkt ↑", roh, "m; bereinigt ↑", round(np.clip(np.diff(hh), 0, None).sum(), 1), "m")
print("Höhe min/max", round(hm[grid <= L].min(), 1), round(hm[grid <= L].max(), 1), "bei km", grid[np.argmin(hm[grid <= L])]/1000, grid[np.argmax(hm[grid <= L])]/1000, "Start", round(at(0), 1), "Ziel", round(at(L), 1))
print("Straßenabschnitte", len(segs), "Marken", len(marks), "geschätzt", len(bridges))
for sg in segs: print("  ", sg)
for m in marks: print("  ", m["k"], m["s"], "|", m["n"])
