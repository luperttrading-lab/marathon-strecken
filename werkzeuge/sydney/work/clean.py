# Brücken, Hochstraßen und übrige Stufen im Höhenprofil überbrücken -> clean.json. Das NSW-5-m-Modell ist ein Geländemodell: auf
# der Harbour Bridge misst es das Wasser, auf den Hochstraßen (Cahill Expressway, Western Distributor) den Boden darunter.
# Ein Oberflächenmodell gibt es offen nicht (NSW-Punktwolken nur über ELVIS; Copernicus 30 m liegt 5–15 m zu hoch und über
# Wasser auf 0). Die Suche wie in Tokio (Brücken aus OSM, bridge=yes auf der Linie, wo das Modell innen mehr als 0,5 m unter
# der Geraden zwischen den Enden liegt) zerlegte die Hochstraßen falsch; sie stehen deshalb von Hand in HOCH, dazwischen gerade.
# Auf der Harbour Bridge fehlt so der Scheitel der Fahrbahn (einige Meter). Danach übrige Stufen > 1,5 m paarweise.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official
r = json.load(open("dgm2026_10m.json"))
s = np.array([x[0] for x in r]); k = official(s)
raw = np.array([x[3] for x in r], float)   # Geländemodell, keine Punktwolke
streets = [[o[0], o[1]] for o in json.load(open("strassen.json"))]
def street(gpx_m):
    best = streets[0]
    for e in streets:
        if e[0] <= gpx_m + 5: best = e   # Straßen alle 10 m
    return best[1]
h = raw.copy(); bad = np.zeros(len(h), bool); osm = np.zeros(len(h), bool)
# Hochstraßen von Hand (Linienmeter, wo die Fahrbahn den Boden verlässt und wieder aufsetzt; dort stimmen Modell und Fahrbahn
# überein). Die automatische Suche über OSM-Brücken zerlegte sie in Stücke und hätte die Harbour Bridge auf 8 m gelegt.
HOCH = [(1600, 3300, "Harbour Bridge mit Rampen"),
        (3550, 5450, "Western Distributor (Pyrmont)"),
        (7900, 9050, "Western Distributor (King Street)")]
bname = {}
for a_, b_, nm in HOCH:
    a, b = int(np.searchsorted(s, a_)), int(np.searchsorted(s, b_))
    h[a:b + 1] = np.linspace(h[a], h[b], b - a + 1); osm[a + 1:b] = True
    for q in range(a + 1, b): bname[q] = nm
bad |= osm
d = np.diff(h)
steps = [(i, d[i]) for i in range(len(d)) if abs(d[i]) > 1.5 and not osm[i] and not osm[i + 1]]
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
out, i = [], 0
while i < len(h):
    if not bad[i]: i += 1; continue
    j = i
    while j + 1 < len(h) and bad[j + 1]: j += 1
    a, b = max(0, i - 1), min(len(h) - 1, j + 1)
    inner = raw[i:j+1]
    if inner.mean() < min(raw[a], raw[b]) or osm[i:j + 1].any(): kind = "Brücke"
    else: kind = "Unterführung"
    nm = next((bname[q] for q in range(i, j + 1) if q in bname), None) or street((s[a] + s[b]) / 2)
    out.append({"a": float(k[a]), "b": float(k[b]), "kind": kind, "name": nm, "ha": float(raw[a]), "hb": float(raw[b]), "extrem": float(inner.min() if kind == "Brücke" else inner.max())})
    i = j + 1
good = ~bad
hc = np.interp(np.arange(len(h)), np.where(good)[0], h[good])
for o in out:
    print(f"km {o['a']/1000:6.2f}-{o['b']/1000:6.2f} {o['b']-o['a']:5.0f} m  {o['kind']:12s} {o['name']:28s} {o['ha']:5.1f} -> {o['hb']:5.1f}  (im Modell {o['extrem']:5.1f})")
json.dump({"k": k.tolist(), "h": hc.tolist(), "raw": raw.tolist(), "regions": out}, open("clean.json", "w"), ensure_ascii=False)
