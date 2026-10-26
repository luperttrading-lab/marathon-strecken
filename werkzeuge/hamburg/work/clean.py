import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official
r = json.load(open("dgm2026_10m.json"))
s = np.array([x[0] for x in r]); raw = np.array([x[3] for x in r], float); k = official(s)
streets = json.load(open("streets2026.json"))
def street(gpx_m):
    best = streets[0]
    for e in streets:
        if e[0] <= gpx_m + 75: best = e
    return best[1]
h = raw.copy()
bad = np.zeros(len(h), bool)
# 1) Wasser (NoData -20) plus je ein Randpunkt
w = h < -5
bad |= w | np.r_[w[1:], False] | np.r_[False, w[:-1]]
# 2) Stufen > 1,5 m auf ~10 m (> 15 %), Wasserpunkte ausgenommen
hh = np.where(w, np.nan, h)
d = np.diff(hh)
steps = [(i, d[i]) for i in range(len(d)) if np.isfinite(d[i]) and abs(d[i]) > 1.5]
regions = []
used = set()
for n, (i, di) in enumerate(steps):
    if i in used: continue
    # passender Gegensprung innerhalb 600 m
    for j, dj in steps[n+1:]:
        if (k[j] - k[i]) > 600: break
        if np.sign(dj) != np.sign(di) and j not in used:
            regions.append((i, j + 1, "paar", di, dj)); used |= {i, j}; break
    else:
        regions.append((max(0, i - 5), min(len(h) - 1, i + 6), "einzel", di, 0)); used.add(i)
for a, b, typ, di, dj in regions:
    bad[a + 1:b] = True
# Ränder erweitern, solange der Randpunkt noch auf der Kante liegt (max. 3 Punkte je Seite)
def edges(mask):
    m = mask.copy(); i = 0
    while i < len(m):
        if not m[i]: i += 1; continue
        j = i
        while j + 1 < len(m) and m[j + 1]: j += 1
        a = i - 1
        for _ in range(3):
            if a - 1 >= 0 and h[a] > -5 and h[a-1] > -5 and abs(h[a] - h[a-1]) > 0.6: m[a] = True; a -= 1
            else: break
        b = j + 1
        for _ in range(3):
            if b + 1 < len(m) and h[b] > -5 and h[b+1] > -5 and abs(h[b] - h[b+1]) > 0.6: m[b] = True; b += 1
            else: break
        i = b + 1
    return m
bad = edges(bad)
# zusammenhängende schlechte Bereiche
out = []
i = 0
while i < len(h):
    if not bad[i]: i += 1; continue
    j = i
    while j + 1 < len(h) and bad[j + 1]: j += 1
    a, b = max(0, i - 1), min(len(h) - 1, j + 1)
    inner = raw[i:j+1]
    kind = "Brücke" if (inner < -5).any() or np.nanmean(np.where(inner < -5, np.nan, inner)) < min(raw[a], raw[b]) else "Tunnel/Kante"
    if (inner < -5).all() or (inner < -5).any(): kind = "Brücke über Wasser"
    out.append({"a": float(k[a]), "b": float(k[b]), "kind": kind, "name": street((s[a] + s[b]) / 2), "ha": float(raw[a]), "hb": float(raw[b])})
    i = j + 1
# Interpolieren
good = ~bad
hc = np.interp(np.arange(len(h)), np.where(good)[0], h[good])
for o in out:
    print(f"km {o['a']/1000:6.2f}-{o['b']/1000:6.2f} {o['b']-o['a']:5.0f} m  {o['kind']:20s} {o['name']:28s} {o['ha']:5.1f} -> {o['hb']:5.1f}")
json.dump({"k": k.tolist(), "h": hc.tolist(), "raw": raw.tolist(), "regions": out}, open("clean.json", "w"), ensure_ascii=False)
