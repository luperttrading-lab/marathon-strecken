# Höhen im 10-m-Raster, Wege, Orte, Marken und geschätzte Stücke -> data.json (geht als const D in liechtenstein/index.html).
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
# Wege aus den OSM-Wegen der Linie (strassen.json, alle 10 m, Namen wie in OSM und auf den Schildern: „Schaaner Strasse“, „Binnendamm“,
# „Rheindamm“, „Lettstrasse“, „Äulestrasse“, „Städtle“, „Beckagässli“, „Letziweg“, „Rotenbodenstrasse“, „Philosophenweg“, „Valorschstrasse“,
# „Guschgerstrasse“, „Turnastrasse“, „Pradameestrasse“). Gehwege neben einer Straße tragen deren Namen (strassen.py). Wege ohne Namen heißen
# nach ihrer Art (OSM-Tags): „Nebenstrasse“ (Strasse mit Belag), „Fahrweg“ (track, Kiesstrasse), „Bergweg“ (Pfad mit sac_scale ab
# mountain_hiking, weiß-rot-weiß markiert), „Wanderweg“ (übrige Pfade), „Fussweg“, „Treppe“. Gemeinden und Orte (orte2026.json, alle 100 m).
# Kurze Stücke unter 80 m übernehmen den Namen davor, Orte unter 300 m dem Vorgänger zugeschlagen und auf den nächsten Wegwechsel gelegt.
# Muster: werkzeuge/zermatt/work/build.py
st = json.load(open("strassen.json")); orte = json.load(open("orte2026.json"))
W = json.load(open("../dl/osm_netz.json"))["ways"]
FLURNAMEN = set()
def art(o):
    hw = o[6]; tg = W[o[7]][0] if o[7] in W else {}
    if hw in ("path", "footway", "bridleway", "steps", "cycleway"):
        if hw == "steps": return "Treppe"
        return "Bergweg" if tg.get("sac_scale", "hiking") not in ("hiking",) else ("Fussweg" if hw == "footway" else "Wanderweg")
    if hw == "track": return "Fahrweg"
    if hw == "pedestrian": return "Fussweg"
    if hw in ("service", "unclassified", "residential", "tertiary", "secondary", "living_street"):
        return "Nebenstrasse" if tg.get("surface", "asphalt") in ("asphalt", "paved", "concrete", "sett", "paving_stones") else "Fahrweg"
    return ""
VON_HAND = [(0, 90, "Schaaner Strasse")]   # Linienmeter: Start vor der LGT Bank (Lageplan Startbereich); in OSM die Zufahrt der Bank
def strasse(x):
    for a, b, n in VON_HAND:
        if a <= x <= b: return n
    o = st[min(len(st) - 1, int(round(x / 10)))]
    return o[2] if (o[2] and o[2] not in FLURNAMEN) else art(o)
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
# Geschätzte Stücke (schraffiert, clean.py): zwei Brücken unter Bäumen (Steg, Güschgle), keine Tunnel.
bridges = []
for r in c["regions"]:
    if r["art"] == "überdeckt":
        bridges.append({"a": round(r["a"]), "b": round(r["b"]), "name": r["name"] or "Unterführung", "kind": "Unterführung"})
    elif r["art"] == "Brücke geschätzt":
        bridges.append({"a": round(r["a"]), "b": round(r["b"]), "name": r["name"] or "Brücke", "kind": "Brücke"})
bridges.sort(key=lambda b: b["a"])
# Verpflegung nach der Postenliste des Veranstalters („Postenbezeichnungen LGT Alpin Marathon“, ../dl/dateien/f_12554.pdf, Download auf der
# Seite „LGT Alpin Marathon“; Programm 2027: „8 Verpflegungsposten und 5 Wasserstellen“). Die Kilometer der Liste sind runde Werte (5, 10,
# 12,5, 15 …); die Marke steht deshalb am genannten Ort, wo er sich auf der Linie finden lässt (Lage aus OSM und swissNAMES3D), sonst an der
# Kilometerzahl der Liste. Posten 1 (Sportplatz Schaan, km 5): im Plan bei „5 km“ am Rhein, Lage nicht genauer bekannt. Posten 12 „Kirche
# Malbun“: an der Friedenskapelle, wo die Strecke das erste Mal durch Malbun kommt (Laufbericht 2023: „Kilometer 37: Vorbei an der Malbuner
# Friedenskapelle, das Ziel liegt nicht mal 100 m rechts“), hier an der Einmündung der Turnastrasse.
from pyproj import Transformer
_T = Transformer.from_crs(4326, 2056, always_xy=True)
_r = json.load(open("dgm2026_10m.json")); _rs = np.array([x[0] for x in _r]); _E, _N = _T.transform([x[2] for x in _r], [x[1] for x in _r])
_E = np.array(_E); _N = np.array(_N)
def km_am_ort(e, n, ab=0.0, bis=99.0):
    """offizielle Meter des Linienpunkts, der dem Ort am nächsten liegt (nur zwischen ab und bis km), und sein Abstand"""
    k_ = np.asarray(official(_rs), float); dd = np.hypot(_E - e, _N - n); dd[(k_ < ab * 1000) | (k_ > bis * 1000)] = np.inf
    i = int(np.argmin(dd)); return float(k_[i]), float(dd[i])
# (Posten, Ort, km laut Liste, Angebot, Lage LV95 oder None, nur bis km, Wasserposten laut Liste)
VP = [(1, "Sportplatz Schaan", 5.0, "Wasser, Iso, Cola", None, 0, False),
      (2, "Marktplatzgarage Vaduz", 10.0, "Wasser, Iso, Cola", (2758010, 1222897), 0, False),
      (3, "Schloss Vaduz", 12.5, "Wasser, Cola", (2758204, 1223031), 0, True),
      (4, "Rotenboden", 15.0, "Wasser, Iso, Cola, Brot, Bananen, Orangen, Riegel, Gels", (2759327, 1221753), 0, False),
      (5, "Masescha", 17.5, "Wasser, Cola", (2759633, 1222318), 0, True),
      (6, "Silum", 20.0, "Wasser, Iso, Cola, Brot, Bananen, Orangen, Riegel, Gels", (2760517, 1222201), 0, False),
      (7, "Weissfleck", 22.5, "Wasser, Cola", (2760983, 1221665), 0, True),
      (8, "Steg, Parkplatz Grund", 25.0, "Wasser, Iso, Cola, Brot, Bananen, Orangen, Riegel, Bouillon, Gels", (2762396, 1219449), 0, False),
      (9, "Valorsch, Rietle Stall", 31.0, "Wasser, Iso, Cola, Brot, Bananen, Orangen, Riegel, Bouillon, Gels", (2763939, 1223218), 0, False),
      (10, "Ende Fussweg, Abzweigung Güschgle", 33.0, "Wasser, Cola", (2764756, 1222233), 0, True),
      (11, "Sassförkle", 35.0, "Wasser, Iso, Cola, Brot, Bananen, Orangen, Riegel, Bouillon, Gels", (2764745, 1220995), 0, False),
      (12, "Kirche Malbun", 37.0, "Wasser, Cola, Bouillon", (2764673, 1219151), 39.0, True),
      (13, "Kehrplatz unter dem Turna-Stall", 38.5, "Wasser, Iso, Cola", (2765417, 1217909), 0, False)]
def kmtext(x): return f"{x:.1f}".replace(".", ",")
def seg_at(x):
    s_ = [sg for sg in segs if sg[0] <= x][-1]; return s_[1], s_[2]
def hoehe(x): return float(np.interp(x, grid, hm))
marks = []
ESSEN = ("Brot", "Bananen", "Riegel", "Gels")
for nr, nm, km, was, lage, bis, wp in VP:
    if lage: kk, abst = km_am_ort(*lage, bis=bis or 99.0)
    else: kk, abst = km * 1000, 0.0
    kk = round(kk / 10) * 10
    essen = any(e in was for e in ESSEN)
    c_ = "food" if essen else "water"; s_ = "Verpflegung" if essen else ("Wasser" if wp else "Getränke")
    liste = "" if abs(kk - km * 1000) < 150 else f", in der Postenliste km {kmtext(km)}"
    marks.append({"k": int(kk), "s": s_, "c": c_, "n": f"{s_} {nm} km {kmtext(kk / 1000)}{liste} (Posten {nr}: {was})"})
    stra, ort = seg_at(kk)
    print(f"  Posten {nr:2d} {nm:34s} Liste km {km:5.1f} -> km {kk / 1000:6.2f} ({abst:.0f} m neben der Linie), Höhe {hoehe(kk):7.1f} m, {stra}, {ort}")
# Staffel 25 + 17: Wechselzone in Steg (Lageplan „Ziel 1/2-Marathon & 1. Staffel im Steg“: Ziel des Halbmarathons PLUS an der Strasse,
# Wechselzone gleich nördlich; Laufbericht 2023: „bei der Kapelle Steg (km 26) trennen sich die Strecken … Marathonläufer überqueren die
# Hauptstraße“). Gesetzt dort, wo die Linie die Malbunstrasse in Steg quert (Übergang Kleinsteg -> Grosssteg).
_w = [o for o in st if o[1] == "Grosssteg" and float(official(o[0])) > 24000][0][0]
kw = int(round(float(official(_w)) / 10) * 10)
marks.append({"k": kw, "s": "Wechsel", "c": "relay", "n": f"Wechselzone LGT Staffel 25 + 17 in Steg, km {kmtext(kw / 1000)} (daneben das Ziel des LGT Halbmarathons PLUS)"})
print(f"  Wechsel Staffel bei km {kw / 1000:.2f}, Höhe {hoehe(kw):.1f} m")
marks.append({"k": 21098, "s": "Halbmarathon", "c": "half", "n": "Halbmarathon"})
marks.sort(key=lambda m: m["k"])
data = {"len": L, "step": STEP, "h": [int(round(v * 100)) for v in hm], "streets": segs, "marks": marks, "bridges": bridges}
json.dump(data, open("data.json", "w"), ensure_ascii=False, separators=(",", ":"))
# Kontrollen
def at(x): return float(np.interp(x, grid, hm))
def asc(w):
    xs = grid[grid <= L]; gr = np.array([(at(min(x + w/2, L)) - at(max(x - w/2, 0))) / (min(x + w/2, L) - max(x - w/2, 0)) for x in xs])
    dh = (gr[1:] + gr[:-1]) / 2 * STEP
    return dh[dh > 0].sum(), -dh[dh < 0].sum(), np.abs(gr).max() * 100, xs[np.argmax(gr)], gr.min()*100, xs[np.argmin(gr)], gr.max()*100, gr, xs
for w in (50, 100, 200, 1000):
    u, d_, gabs, xmax, gmin, xmin, gmax, gr, xs = asc(w)
    print(f"Fenster {w:5d} m: ↑ {u:6.1f} m  ↓ {d_:5.1f} m  steilste bergauf {gmax:4.1f} % bei km {xmax/1000:.2f}, bergab {gmin:5.1f} % bei km {xmin/1000:.2f}")
    if w == 200:
        for thr in (0.10, 0.15, 0.20, 0.25):
            print(f"   über {thr * 100:.0f} %: {(gr > thr).sum() * STEP / 1000:.2f} km bergauf, {(gr < -thr).sum() * STEP / 1000:.2f} km bergab")
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
