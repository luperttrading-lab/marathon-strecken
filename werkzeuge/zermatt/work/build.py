# Höhen im 10-m-Raster, Wege, Orte, Marken und geschätzte Stücke -> data.json (geht als const D in zermatt/index.html).
# Muster: werkzeuge/luzern/work/build.py
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
# Wege aus den OSM-Wegen unter der Linie (strassen.json, alle 10 m, Namen wie in OSM und auf den Schildern: „Talstrasse“, „Alte
# Kantonsstrasse“, „Uferweg“, „Bahnhofstrasse“, „Riedweg“). Viele Wege im Tal und am Berg haben in OSM keinen Namen: Sie heissen nach ihrer
# Art (OSM-Tags) „Nebenstrasse“ (Strasse mit Belag), „Fahrweg“ (track, Kiesstrasse), „Bergweg“ (Pfad mit sac_scale ab mountain_hiking,
# weiss-rot-weiss markiert), „Wanderweg“ (übrige Pfade), „Fussweg“ (Fussgängerbereich ohne Namen). Ein OSM-Name, der nur ein Flurname ist
# („Ried“, „Grüebe“, „Tuftra“, „Balmbrunnen“), zählt als Weg ohne Namen; der Ort steht ohnehin daneben. Ziel: „Ziel Riffelberg“.
# Gemeinden und Orte (orte2026.json, alle 100 m). Kurze Stücke unter 80 m (Kreuzungen, Brücken) übernehmen den Namen davor, Orte unter
# 300 m dem Vorgänger zugeschlagen und auf den nächsten Wegwechsel gelegt.
st = json.load(open("strassen.json")); orte = json.load(open("orte2026.json"))
W = json.load(open("../dl/osm_netz.json"))["ways"]
FLURNAMEN = {"Ried", "Grüebe", "Tuftra", "Balmbrunnen", "Aroleit"}
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
VON_HAND = [(41520, 41700, "Ziel Riffelberg")]   # Linienmeter: die letzten 100 m (in OSM ohne Weg)
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
# Geschätzte Stücke (schraffiert, clean.py): nur die Unterführung des Fusswegs in Randa. Alle 15 Brücken sind aus dem Oberflächenmodell gemessen.
bridges = []
for r in c["regions"]:
    if r["art"] == "überdeckt":
        bridges.append({"a": round(r["a"]), "b": round(r["b"]), "name": "Unterführung Randa", "kind": "Unterführung"})
    elif r["art"] == "Brücke geschätzt":
        bridges.append({"a": round(r["a"]), "b": round(r["b"]), "name": r["name"] or "Brücke", "kind": "Brücke"})
bridges.sort(key=lambda b: b["a"])
# Verpflegung laut Verpflegungsplan des Veranstalters (Seite „Streckenverpflegung & Kontrollzeiten“ und Verpflegungsplan.pdf, Stand 2026;
# ../dl/seiten/verpflegung.html): Name, km, Höhe und Angebot je Posten. Die km des Plans passen meist zur gleichmässig gedehnten Linie
# (Herbriggen 5,0 km auf 1235 m, Randa 10,0 auf 1410, Zermatt 20,3 auf 1604, Sunnegga 32,0 auf 2262, Riffelalp 39,0 auf 2222): Im Tal
# (Herbriggen bis Zermatt) gilt die Plan-km. Am Berg sagt die Höhe mehr: Dort steht der Posten, wo die Linie höchstens 0,6 km neben der
# Plan-km die Planhöhe trifft (Chalet Ried 26,5 statt 26,8, Patrullarve 28,3 statt 28,6, das passt auch zu den Orten). Ausnahme Grünsee
# (Plan km 36,7 auf 2300 m): Dort liegt die Linie auf 2239 m, unterhalb des Sees; der Posten steht am See (km 35,6, wo die Linie am
# Grüensee vorbeiführt; Restaurant und Seeufer 2300 m). Start (Wasser, Tee) und Riffelberg (km 42,0, Ziel) fehlen als Marke.
ANG = ["Wasser", "ISO", "Cola", "Tee", "Bouillon", "Banane", "Gel", "Riegel", "Schwamm"]
VP = [("Herbriggen", 5.0, 1235, "XX      X"), ("Randa", 10.0, 1410, "XX    XXX"), ("Täsch", 14.3, 1439, "XX   XXXX"),
      ("Zermatt", 20.3, 1604, "XX XXXXXX"), ("Zermatt", 24.5, 1603, "XXX   XXX"), ("Chalet Ried", 26.8, 1800, "X        "),
      ("Patrullarve", 28.6, 2000, "XXX  XXXX"), ("Sunnegga", 32.0, 2262, "XXXXXXXXX"), ("Grünsee", 36.7, 2300, "XXX XXXXX"),
      ("Riffelalp", 39.0, 2222, "XXXXXXXXX"), ("Riffelboden", 40.4, 2355, "XXX   XX ")]
def kmtext(x): return f"{x:.1f}".replace(".", ",")
def seg_at(x):
    s_ = [sg for sg in segs if sg[0] <= x][-1]; return s_[1], s_[2]
def hoehe(x): return float(np.interp(x, grid, hm))
marks = []
for nm, km, alt, x in VP:
    if nm == "Grünsee": kk = 35600.0
    elif km < 25: kk = km * 1000
    else:
        cand = np.arange(km * 1000 - 600, km * 1000 + 601, 10.0); kk = float(cand[np.argmin(np.abs(np.interp(cand, grid, hm) - alt) + 1e-4 * np.abs(cand - km * 1000))])
    kk = round(kk / 100) * 100
    was = ", ".join(a for a, f in zip(ANG, x) if f == "X")
    c_ = "food" if any(a in was for a in ("Banane", "Gel", "Riegel", "Bouillon")) else "water"
    s_ = "Verpflegung" if c_ == "food" else ("Wasser" if was == "Wasser" else "Getränke")
    plan = "" if abs(kk - km * 1000) < 150 else f", im Plan km {kmtext(km)}"
    stra, ort = seg_at(kk)
    marks.append({"k": int(kk), "s": s_, "c": c_, "n": f"{s_} {nm} km {kmtext(kk / 1000)}{plan}, {alt} m laut Plan ({was})"})
    print(f"  {nm:12s} Plan km {km:5.1f} {alt} m -> km {kk / 1000:6.2f}, Höhe hier {hoehe(kk):7.1f} m, {stra}, {ort}")
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
