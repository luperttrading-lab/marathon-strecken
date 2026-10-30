# Höhen im 10-m-Raster, Namen, Marken, Brücken, Mauer und Tor -> data.json (geht als const D in greatwall/index.html)
# Höhe: SRTM 1″ (NASA, Radar Februar 2000, Kachel N40E117 aus den AWS Terrain Tiles „skadi“) entlang der Linie, Wahl und Vergleich
# in vergleich.py; Kilometer nach common.py. Brücken: OSM bridge=yes auf der Linie, wo das Modell innen mehr als 1 m unter der
# Geraden zwischen den Enden liegt -> Gerade (geschätzt, gestrichelt). Danach gleitender Median über 30 m wie in allen Strecken.
import json
import numpy as np
from common import official, gpx_of
from dgm import abtasten
from geo import osm
from namen import strassenname, doerfer
N, W, NT = osm()
L = 42195.0; STEP = 10
lin = json.load(open("linie.json")); d = np.array(lin["d"]); X = np.c_[lin["x"], lin["y"]]
WAY, ART, TEIL, KN = lin["way"], lin["art"], lin["teil"], lin["knoten"]
R = np.array(json.load(open("dgm_cop30_10m.json"))); s_r = R[:, 0]
raw = np.fromfile("../dl/dem/N40E117.hgt", ">i2").reshape(3601, 3601).astype(float)
h_r = abtasten(raw, 117.0, 41.0, 1 / 3600, 1 / 3600, R[:, 1], R[:, 2], mitte=False)
grid = np.arange(0, 42200 + 1, STEP, dtype=float); gl = gpx_of(np.minimum(grid, L))
hg = np.interp(gl, s_r, h_r); roh = hg.copy()
idx = np.clip(np.searchsorted(d, gl, side="right"), 1, len(d) - 1)     # Linienstück, in dem der Rasterpunkt liegt
# --- Brücken
bridges = []
brw = {w for w, (tg, _) in W.items() if tg.get("bridge") == "yes"}
i = 1
while i < len(d):
    if WAY[i] in brw:
        j = i
        while j + 1 < len(d) and WAY[j + 1] == WAY[i]: j += 1
        a, b = float(official(d[i - 1])), float(official(d[j]))
        ia, ib = int(np.floor(a / STEP)) - 1, int(np.ceil(b / STEP)) + 1
        gerade = np.interp(grid[ia:ib + 1], [grid[ia], grid[ib]], [hg[ia], hg[ib]])
        tg = W[WAY[i]][0]
        name = ("Mauerbrücke" if tg.get("historic") == "citywalls" else "Qingnian-Brücke" if tg.get("name") == "下营青年桥" else
                "Brücke Changcheng Lu" if tg.get("name") == "长城路" else "Brücke bei Duanzhuang")
        if (gerade - hg[ia:ib + 1]).max() > 1.0:
            hg[ia:ib + 1] = gerade
            bridges.append({"a": round(grid[ia]), "b": round(grid[ib]), "name": name, "kind": "Brücke"})
        print(f"Brücke {name} km {a / 1000:.2f}–{b / 1000:.2f}: Modell innen bis {(gerade - roh[ia:ib + 1]).max():.1f} m unter der Geraden"
              + (" -> Gerade" if bridges and bridges[-1]["a"] == round(grid[ia]) else " -> gemessen"))
        i = j + 1
    else: i += 1
hm = hg.copy()
for k in range(1, len(hg) - 1): hm[k] = np.median(hg[k - 1:k + 2])
# --- Stellen auf der Linie
def bei_knoten(node, teil=None):
    out = [k for k in range(len(d)) if KN[k] == node and (teil is None or teil in (TEIL[k], TEIL[min(k + 1, len(d) - 1)]))]
    return float(official(d[out[0]]))
def gegenueber(m1, teil2):
    """Stelle im zweiten Durchgang, die einer Stelle m1 (offiziell) im ersten am nächsten liegt."""
    xy = X[np.searchsorted(d, gpx_of(m1))]; sel = [k for k in range(len(d)) if TEIL[k] == teil2]
    k = min(sel, key=lambda k: np.hypot(*(X[k] - xy))); return float(official(d[k]))
WP1_FUSS = 2310481691; TREPPE_OBEN = 1044038641; GOAT = 2310481713; T5 = 1046093729; T6 = 8087204327
M1a = bei_knoten(WP1_FUSS, "Mauer, 1. Mal"); M1b = bei_knoten(T6, "Mauerbrücke")
M2a = bei_knoten(T6, "Mauerbrücke zurück"); M2b = bei_knoten(WP1_FUSS, "Mauer, 2. Mal")
TOR = float(official(d[[k for k in range(len(d)) if TEIL[k] == "Nordmauer zu Tower 6"][0] - 1]))
# Türme (Ausschnitt „Mauer“ der Karte) -> OSM-Turmknoten, erster Durchgang
TUERME1 = [(M1a, "Wall point 1"), (bei_knoten(1044038875, "Mauer, 1. Mal"), "Tower 1"), (bei_knoten(1044037739, "Mauer, 1. Mal"), "Beacon Tower"),
           (bei_knoten(1044038692, "Mauer, 1. Mal"), "Tower 2"), (bei_knoten(1044038426, "Mauer, 1. Mal"), "Tower 3"),
           (bei_knoten(1044037208, "Mauer, 1. Mal"), "Tower 4"), (6400.0, "Wall point 2"), (bei_knoten(T5, "Mauer, 1. Mal"), "Tower 5")]
# zweiter Durchgang: dieselben Stellen, in Laufrichtung jeweils ab dem Turm benannt
TUERME2 = [(bei_knoten(T5, "Mauer, 2. Mal"), "zum Wall point 2"), (gegenueber(6400.0, "Mauer, 2. Mal"), "Wall point 2")] + \
          [(gegenueber(m, "Mauer, 2. Mal"), n) for m, n in TUERME1[5:0:-1]] + [(bei_knoten(TREPPE_OBEN, "Mauer, 2. Mal"), "Wall point 1")]
TUERME2.sort()
def turm(m, liste):
    q = liste[0][1]
    for a, n in liste:
        if m >= a - 1: q = n
    return q
DORF = doerfer(); DN = list(DORF); DC = np.array([DORF[n] for n in DN])
PLATZ = {"Start über den Platz", "Platz zur Straße", "Platz zum Tor", "Ziel über den Platz"}
roads, qs = [], []
for g, m, k in zip(gl, np.minimum(grid, L), idx):
    t, w, a = TEIL[k], WAY[k], ART[k]
    if t in PLATZ: roads.append("Yin-&-Yang-Platz"); qs.append("Huangyaguan"); continue
    if t in ("Mauerbrücke", "Mauerbrücke zurück"): roads.append("Mauerbrücke"); qs.append("Tower 5 – Tower 6"); continue
    if t == "Festungsmauer": roads.append("Festungsmauer"); qs.append("Huangyaguan"); continue
    if t in ("Nordmauer zum Tor", "Nordmauer zu Tower 6"): roads.append("Festungsmauer"); qs.append("Tor zur Mauer"); continue
    if t in ("Mauer, 1. Mal", "Mauer, 2. Mal"):
        if w == 222071702: roads.append("Treppe am Wall point 1"); qs.append("Wall point 1")
        elif w == 90229166: roads.append("Goat Track"); qs.append("Tower 5")
        else: roads.append("Große Mauer"); qs.append(turm(m, TUERME1 if t == "Mauer, 1. Mal" else TUERME2))
        continue
    roads.append(strassenname(w, a, W) if a != "verb" else None)
    dist = np.hypot(*(DC - X[k]).T); j = int(np.argmin(dist)); qs.append(DN[j] if dist[j] < 1500 else None)
def glaetten(v, mind, fest=()):
    for i in range(1, len(v)): v[i] = v[i] or v[i - 1]
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[j + 1] == v[i]: j += 1
        if i > 0 and (j + 1 - i) * STEP < mind and v[i] not in fest: v[i:j + 1] = [v[i - 1]] * (j + 1 - i)
        i = j + 1
    for i in range(len(v) - 2, -1, -1): v[i] = v[i] or v[i + 1]
    return v
MAUERNAMEN = {"Yin-&-Yang-Platz", "Mauerbrücke", "Festungsmauer", "Treppe am Wall point 1", "Goat Track", "Große Mauer"}
roads = glaetten(roads, 80, MAUERNAMEN)
wall_q = {"zum Wall point 2", "Wall point 1", "Tower 1", "Beacon Tower", "Tower 2", "Tower 3", "Tower 4", "Wall point 2", "Tower 5", "Tower 5 – Tower 6", "Tor zur Mauer"}
qs = glaetten(qs, 400, wall_q)
# Dorfwechsel auf den nächsten Wechsel des Abschnittsnamens legen (bis 100 m), sonst entstehen Stücke von 10 m
wechsel = [i for i in range(1, len(roads)) if roads[i] != roads[i - 1]]
for i in [i for i in range(1, len(qs)) if qs[i] != qs[i - 1] and qs[i] not in wall_q and qs[i - 1] not in wall_q]:
    w = min(wechsel, key=lambda j: abs(j - i), default=None)
    if w is not None and 0 < abs(w - i) <= 10:
        if w > i: qs[i:w] = [qs[i - 1]] * (w - i)
        else: qs[w:i] = [qs[i]] * (i - w)
segs, prev = [], None
for x, road, q in zip(grid, roads, qs):
    if x > L: break
    if (road, q) != prev: segs.append([round(x), road, q]); prev = (road, q)
segs[0][0] = 0
# Die App fasst Abschnitte unter 250 m mit dem Vorgänger zusammen, bevor sie gleiche Namen vereint (ROADS); eine Folge kurzer
# „Große Mauer“-Stücke mit wechselndem Turm fiele so ganz weg. Deshalb kurze Turmstücke paarweise zusammenlegen („Tower 3, Tower 4“).
i = 0
while i < len(segs) - 1:
    a, nm, q = segs[i]; ende = segs[i + 1][0]
    if nm == "Große Mauer" and segs[i + 1][1] == nm and ende - a < 250:
        segs[i][2] = q + ", " + segs[i + 1][2]; del segs[i + 1]; continue
    i += 1
# --- Getränkestellen (Karte und Höhenkurve des Veranstalters, Runners Guide 2026): Nummer, km, Inhalt. Auf der Mauer nur Wasser
# („All stations except those on the wall itself will provide electrolyte“), Gel für Marathonläufer ab km 25 und 34,5, Bananen an
# zwei Stellen (6 und 14), Toiletten an den Stellen 3, 7 und 10 sowie an Start und Ziel (Guide). Erste Hilfe laut Karte an 3 und 5.
STELLEN = [(1, 2.6, "Wasser, Elektrolyt"), (2, 5.1, "Wasser, Elektrolyt"), (3, 5.5, "Wasser, Erste Hilfe, WC"), (4, 6.1, "Wasser"),
           (5, 6.4, "Wasser, Erste Hilfe"), (6, 8.1, "Wasser, Elektrolyt, Banane"), (7, 11.5, "Wasser, Elektrolyt, WC"),
           (8, 14.2, "Wasser, Elektrolyt"), (9, 16.6, "Wasser, Elektrolyt"), (10, 19.5, "Wasser, Elektrolyt, WC"),
           (11, 22.7, "Wasser, Elektrolyt"), (12, 25.3, "Wasser, Elektrolyt, Gel"), (13, 26.9, "Wasser"),
           (14, 28.9, "Wasser, Elektrolyt, Banane"), (7, 31.5, "Wasser, Elektrolyt, WC"), (6, 34.9, "Wasser, Elektrolyt, Gel, Banane"),
           (5, 35.8, "Wasser, Erste Hilfe"), (4, 36.1, "Wasser"), (3, 36.7, "Wasser, Erste Hilfe, WC"), (2, 37.1, "Wasser, Elektrolyt"),
           (1, 39.6, "Wasser, Elektrolyt")]
def kmtext(x): return f"{x:.1f}".replace(".", ",").replace(",0", "")
marks = []
for nr, km, was in STELLEN:
    v = "Banane" in was or "Gel" in was
    marks.append({"k": int(round(km * 1000)), "s": "Verpflegung" if v else "Getränke", "c": "food" if v else "water",
                  "n": f"{'Verpflegung' if v else 'Getränke'} {nr} km {kmtext(km)} ({was})"})
# Erste Hilfe ohne Getränke (rote Kreuze der Karte): an der Talstraße bei Duanzhuang (hin und zurück) und an der Kreuzung bei Baitan
P = json.load(open("plan2026.json")); M = np.array(json.load(open("georef.json"))["M"])
for a in P["aid"]:
    xy = np.asarray(a["pt"]) @ M[:2] + M[2]; dist = np.hypot(*(X - xy).T)
    for k in range(1, len(d) - 1):
        if dist[k] < 60 and dist[k] <= dist[k - 1] and dist[k] <= dist[k + 1] and TEIL[k] == "Tal und Dörfer":
            m = float(official(d[k]))
            if all(abs(m - mk["k"]) > 300 for mk in marks if mk["s"] == "Erste Hilfe"):
                marks.append({"k": int(round(m / 10) * 10), "s": "Erste Hilfe", "c": "water", "n": f"Erste Hilfe km {kmtext(m / 1000)}"})
marks.append({"k": 21098, "s": "Halbmarathon", "c": "half", "n": "Halbmarathon"})
marks.sort(key=lambda m: m["k"])
MAUER = [[int(round(M1a)), int(round(M1b)), "Mauer, 1. Mal"], [int(round(M2a)), int(round(M2b)), "Mauer, 2. Mal"]]
data = {"len": L, "step": STEP, "h": [int(round(v * 100)) for v in hm], "streets": segs, "marks": marks, "bridges": bridges,
        "mauer": MAUER, "tor": {"m": int(round(TOR / 10) * 10), "uhr": 830, "name": "Tor zur Mauer"}, "zielschluss": 950}
json.dump(data, open("data.json", "w"), ensure_ascii=False, separators=(",", ":"))
json.dump({"tuerme1": TUERME1, "tuerme2": TUERME2, "tor": TOR, "mauer": MAUER}, open("stellen.json", "w"), ensure_ascii=False)
# Kontrollen
def at(x): return float(np.interp(x, grid, hm))
def asc(w):
    xs = grid[grid <= L]; gr = np.array([(at(min(x + w / 2, L)) - at(max(x - w / 2, 0))) / (min(x + w / 2, L) - max(x - w / 2, 0)) for x in xs])
    dh = (gr[1:] + gr[:-1]) / 2 * STEP
    return dh[dh > 0].sum(), -dh[dh < 0].sum(), xs[np.argmax(gr)], gr.min() * 100, xs[np.argmin(gr)], gr.max() * 100
for w in (50, 100, 200, 1000):
    u, d_, xmax, gmin, xmin, gmax = asc(w)
    print(f"Fenster {w:5d} m: ↑ {u:6.1f} m  ↓ {d_:6.1f} m  steilste bergauf {gmax:5.1f} % bei km {xmax / 1000:.2f}, bergab {gmin:5.1f} % bei km {xmin / 1000:.2f}")
sel = grid <= L
rohd = round(np.clip(np.diff(roh[sel]), 0, None).sum())
open("rohdaten.txt", "w").write(str(rohd))
print("Rohdaten Punkt für Punkt ↑", rohd, "m")
print("Höhe min/max", round(hm.min(), 1), round(hm.max(), 1), "bei km", grid[np.argmin(hm)] / 1000, grid[np.argmax(hm)] / 1000, "Start", round(at(0), 1), "Ziel", round(at(L), 1))
print("Mauer:", MAUER, "Tor", round(TOR), "Türme 1:", [(round(a), n) for a, n in TUERME1], "Türme 2:", [(round(a), n) for a, n in TUERME2])
print("Abschnitte", len(segs), "Marken", len(marks), "Brücken", bridges)
for sg in segs: print("  ", sg)
for m in marks: print("  ", m["k"], m["n"])
