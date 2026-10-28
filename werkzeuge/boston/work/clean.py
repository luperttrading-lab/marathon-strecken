# Übrige Stufen im Höhenprofil (nach lidar.py) erkennen und überbrücken -> clean.json
# DGM1 ist ein Geländemodell: auf Brücken misst es Wasser oder Gleise darunter (Senke), an Unterführungen den Bahndamm
# oder die Autobahn darüber (Buckel). Stufen > 1,5 m auf 10 m paarweise -> Bereich, dazwischen linear.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official
r = json.load(open("dgm2026_10m.json"))
s = np.array([x[0] for x in r]); k = official(s)
raw = np.array(json.load(open("lidar.json"))["h"], float)   # Boden, auf Brücken die gemessene Fahrbahn (lidar.py)
streets = json.load(open("streets2026.json"))
def street(gpx_m):
    best = streets[0]
    for e in streets:
        if e[0] <= gpx_m + 75: best = e
    return best[1]
h = raw.copy(); bad = np.zeros(len(h), bool)
d = np.diff(h)
steps = [(i, d[i]) for i in range(len(d)) if abs(d[i]) > 1.5]
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
    if inner.mean() < min(raw[a], raw[b]): kind = "Brücke"
    else: kind = "Unterführung"
    out.append({"a": float(k[a]), "b": float(k[b]), "kind": kind, "name": street((s[a] + s[b]) / 2), "ha": float(raw[a]), "hb": float(raw[b]), "extrem": float(inner.min() if kind == "Brücke" else inner.max())})
    i = j + 1
good = ~bad
hc = np.interp(np.arange(len(h)), np.where(good)[0], h[good])
for o in out:
    print(f"km {o['a']/1000:6.2f}-{o['b']/1000:6.2f} {o['b']-o['a']:5.0f} m  {o['kind']:12s} {o['name']:28s} {o['ha']:5.1f} -> {o['hb']:5.1f}  (im Modell {o['extrem']:5.1f})")
json.dump({"k": k.tolist(), "h": hc.tolist(), "raw": raw.tolist(), "regions": out}, open("clean.json", "w"), ensure_ascii=False)
