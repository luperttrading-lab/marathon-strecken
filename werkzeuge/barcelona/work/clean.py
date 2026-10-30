# Brücken und übrige Stufen im Höhenprofil überbrücken -> clean.json (wie Valencia). Das Geländemodell (AMB 25 cm) misst den Boden:
# unter einer Brücke den Bahneinschnitt oder den Trog der Ronda Litoral darunter.
# Zuerst die Brücken aus OSM (bridge=yes höchstens 12 m neben der Linie, ohne Fuß- und Radwege), Enden oben auf den Rampen (höchster
# Punkt bis 30 m außerhalb), nur wo das Modell innen (Median über 30 m) mehr als 1,0 m unter der Geraden zwischen den Enden liegt;
# sonst misst das Modell die Fahrbahn selbst. Auf diesen Brücken gilt das Oberflächenmodell derselben Befliegung (dsm.py, Median über
# 30 m gegen Fahrzeuge und Geländer), wenn es an beiden Enden (ohne Median) höchstens 0,5 m neben dem Geländemodell liegt: Das Deck des Pont de
# Bac de Roda ist gewölbt (Scheitel gut 4 m über den Enden), eine Gerade wäre dort falsch. Sonst wie bisher eine Gerade.
# Danach übrige Stufen > 1,5 m je 10 m paarweise wie bei den anderen Strecken.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official
from namen import name
r = json.load(open("dgm2026_10m.json"))
s = np.array([x[0] for x in r]); k = official(s)
raw = np.array([x[3] for x in r], float)   # Geländemodell, keine Punktwolke
streets = [[o[0], name({"name": o[1]})] for o in json.load(open("strassen.json"))]
def street(gpx_m):
    best = streets[0]
    for e in streets:
        if e[0] <= gpx_m + 5 and e[1]: best = e   # Straßen alle 10 m
    return best[1]
h = raw.copy(); bad = np.zeros(len(h), bool); osm = np.zeros(len(h), bool)
from pyproj import Transformer
from scipy.spatial import cKDTree
T = Transformer.from_crs(4326, 25831, always_xy=True)
gx, gy = T.transform([x[2] for x in r], [x[1] for x in r]); baum = cKDTree(np.c_[gx, gy])
N = json.load(open("../dl/osm_netz.json")); KN = N["nodes"]
bname = {}; gefunden = []
from scipy.signal import medfilt
hm = medfilt(h, 3)   # Brücken nach dem Median über 3 Punkte beurteilen: eine einzelne Lücke im Modell (Carrer de València, km 9,8) ist
                     # keine Senke unter der Fahrbahn, sie fällt unten als Stufe auf
for wid, (tg, refs) in N["ways"].items():
    if tg.get("bridge") in (None, "no") or tg.get("highway") in ("motorway", "motorway_link", "footway", "steps", "cycleway", "path", "pedestrian", "corridor", "proposed", "construction"): continue
    P = [KN[str(q)] for q in refs if str(q) in KN]
    if len(P) < 2: continue
    wx, wy = T.transform([q[1] for q in P], [q[0] for q in P])
    if baum.query(np.c_[wx, wy])[0].min() > 60: continue
    wx, wy = np.interp(np.linspace(0, len(wx) - 1, 4 * len(wx)), np.arange(len(wx)), wx), np.interp(np.linspace(0, len(wy) - 1, 4 * len(wy)), np.arange(len(wy)), wy)
    dd, ii = baum.query(np.c_[wx, wy]); ii = np.unique(ii[dd < 12])
    if len(ii) < 2: continue
    for grp in np.split(ii, np.where(np.diff(ii) > 3)[0] + 1):
        a0, b0 = int(grp.min()), int(grp.max())
        a = max(0, a0 - 3) + int(np.argmax(h[max(0, a0 - 3):a0 + 1])); b = b0 + int(np.argmax(h[b0:min(len(h), b0 + 4)]))
        line = h[a] + (h[b] - h[a]) * (np.arange(a, b + 1) - a) / max(1, b - a)
        tief = float((line - hm[a:b + 1]).max()); nm = tg.get("bridge:name") or name(tg) or ""
        gefunden.append((round(k[a0] / 1000, 2), nm, round(tief, 1)))
        if tief > 1.0:
            osm[a + 1:b] = True
            for i in range(a + 1, b): bname[i] = nm
print("OSM-Brücken auf der Linie (km, Name, Modell unter der Geraden m):", sorted(set(gefunden)))
# Brückendeck aus dem Oberflächenmodell
DSM = json.load(open("../dl/dsm_bruecken.json"))
ds = np.array([DSM.get(f"{x:.2f},{y:.2f}") if DSM.get(f"{x:.2f},{y:.2f}") is not None else np.nan for x, y in zip(gx, gy)], float)
dsm_m = ds.copy()
for i in range(1, len(ds) - 1): dsm_m[i] = np.nanmedian(ds[i - 1:i + 2]) if np.isfinite(ds[i - 1:i + 2]).sum() == 3 else np.nan
deck = np.zeros(len(h), bool); i = 0
while i < len(h):
    if not osm[i]: i += 1; continue
    j = i
    while j + 1 < len(h) and osm[j + 1]: j += 1
    a, b = i - 1, j + 1
    if np.isfinite(dsm_m[i:j + 1]).all() and np.isfinite(ds[[a, b]]).all() and abs(ds[a] - h[a]) <= 0.5 and abs(ds[b] - h[b]) <= 0.5:
        h[i:j + 1] = dsm_m[i:j + 1]; deck[i:j + 1] = True
        print(f"Deck aus dem Oberflächenmodell: km {k[a]/1000:.2f}–{k[b]/1000:.2f} ({bname.get(i, '')}), {h[a]:.1f} -> max {h[i:j+1].max():.1f} -> {h[b]:.1f} m")
    i = j + 1
bad |= osm & ~deck
d = np.diff(h)
steps = [(i, d[i]) for i in range(len(d)) if abs(d[i]) > 1.5 and not osm[i] and not osm[i + 1]]
print("übrige Stufen > 1,5 m:", [(round(k[i] / 1000, 2), round(float(di), 1)) for i, di in steps])
def spike(i):
    """kürzester Bereich um die Stufe i, an dessen Enden die Höhe wieder gleich ist (Buckel oder Delle ohne Gegenstufe)"""
    best = None
    for a in range(i, max(-1, i - 9), -1):
        for b in range(i + 1, min(len(h), i + 10)):
            if abs(h[b] - h[a]) > 0.6: continue
            line = h[a] + (h[b] - h[a]) * (np.arange(a, b + 1) - a) / (b - a)
            if np.abs(h[a:b+1] - line).max() > 1.2 and (best is None or b - a < best[1] - best[0]): best = (a, b)
    return best or (max(0, i - 5), min(len(h) - 1, i + 6))
regions, used = [], set()
for n, (i, di) in enumerate(steps):
    if i in used: continue
    partner = None
    for j, dj in steps[n+1:]:
        if (k[j] - k[i]) > 600: break
        if np.sign(dj) != np.sign(di) and j not in used: partner = j; break
    if partner is not None: regions.append((i, partner + 1)); used |= {i, partner}
    else: regions.append(spike(i)); used.add(i)
for a, b in regions: bad[a + 1:b] = True
def edges(mask):
    m = mask.copy(); i = 0
    while i < len(m):
        if not m[i]: i += 1; continue
        j = i
        while j + 1 < len(m) and m[j + 1]: j += 1
        a = i - 1
        for _ in range(3):
            if a - 1 >= 0 and abs(h[a] - h[a-1]) > 0.6: m[a] = True; a -= 1
            else: break
        b = j + 1
        for _ in range(3):
            if b + 1 < len(m) and abs(h[b] - h[b+1]) > 0.6: m[b] = True; b += 1
            else: break
        i = b + 1
    return m
bad = edges(bad)
out, i = [], 0; zeige = bad | deck
while i < len(h):
    if not zeige[i]: i += 1; continue
    j = i
    while j + 1 < len(h) and zeige[j + 1]: j += 1
    a, b = max(0, i - 1), min(len(h) - 1, j + 1)
    inner = raw[i:j+1]
    if inner.mean() < min(raw[a], raw[b]) or osm[i:j + 1].any(): kind = "Brücke"
    else: kind = "Unterführung"
    nm = next((bname[q] for q in range(i, j + 1) if q in bname), None) or street((s[a] + s[b]) / 2)
    out.append({"a": float(k[a]), "b": float(k[b]), "kind": kind, "name": nm, "ha": float(raw[a]), "hb": float(raw[b]), "extrem": float(inner.min() if kind == "Brücke" else inner.max()),
                "deck": bool(deck[i:j + 1].any())})
    i = j + 1
good = ~bad
hc = np.interp(np.arange(len(h)), np.where(good)[0], h[good])
for o in out:
    print(f"km {o['a']/1000:6.2f}-{o['b']/1000:6.2f} {o['b']-o['a']:5.0f} m  {o['kind']:12s} {o['name']:28s} {o['ha']:5.1f} -> {o['hb']:5.1f}  (im Geländemodell {o['extrem']:5.1f}){'  Deck aus dem Oberflächenmodell' if o['deck'] else ''}")
json.dump({"k": k.tolist(), "h": hc.tolist(), "raw": raw.tolist(), "regions": out}, open("clean.json", "w"), ensure_ascii=False)
