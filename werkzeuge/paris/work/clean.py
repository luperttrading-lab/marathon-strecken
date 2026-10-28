# Tunnel, Brücken und die Rampe zum Ufer im Höhenprofil überbrücken -> clean.json
# Das RGE ALTI ist ein Geländemodell: in Tunneln misst es den Quai oder Platz darüber (Buckel), auf Brücken den Graben
# darunter (Senke: Coulée verte unter der Rue de Picpus, Périphérique unter der Avenue de Gravelle, ein Einschnitt unter der
# Rue de Charenton). Tunnel nach OSM (tunnel=yes auf der Linie, nur wo das Modell innen mehr als 1,2 m von der Geraden
# zwischen den Enden abweicht), übrige Stufen > 1,5 m auf 10 m paarweise wie bei den anderen Strecken; dazwischen linear.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official
r = json.load(open("dgm2026_10m.json"))
s = np.array([x[0] for x in r]); k = official(s)
raw = np.array([x[3] for x in r], float)
g = json.load(open("gpx2026.json")); dg = np.array(g["d"]); kan = json.load(open("../dl/kanten.json"))
def name_at(m):
    i = min(max(np.searchsorted(dg, m) - 1, 0), len(kan["names"]) - 1)
    return kan["names"][i]
h = raw.copy()
# Rampe vom Quai Henri IV hinunter ans Ufer (Linie springt am Ende der Esplanade 3,7 m in 10 m): gleichmäßig über 120 m
for a_, b_ in [(25130, 25250)]:
    i, j = np.searchsorted(s, a_), np.searchsorted(s, b_)
    h[i:j + 1] = np.linspace(h[i], h[j], j - i + 1)
bad = np.zeros(len(h), bool); tunnel = np.zeros(len(h), bool)
# Tunnel aus OSM
runs, cur = [], None
for i_, v in enumerate(kan["tunnel"]):
    if v and v != "no":
        if cur and dg[i_] - cur[1] < 40: cur[1] = dg[i_ + 1]
        else:
            if cur: runs.append(cur)
            cur = [dg[i_], dg[i_ + 1]]
if cur: runs.append(cur)
for a_, b_ in runs:
    i, j = np.searchsorted(s, a_ - 10), np.searchsorted(s, b_ + 10)
    line = h[i] + (h[j] - h[i]) * (np.arange(i, j + 1) - i) / (j - i)
    if np.abs(h[i:j + 1] - line).max() > 1.2: bad[i + 1:j] = True; tunnel[i + 1:j] = True
d = np.diff(h)
steps = [(i, d[i]) for i in range(len(d)) if abs(d[i]) > 1.5 and not tunnel[i] and not tunnel[i + 1]]
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
    inner = h[i:j+1]
    if tunnel[i:j + 1].any(): kind = "Tunnel"
    elif inner.mean() < min(h[a], h[b]): kind = "Brücke"
    else: kind = "Unterführung"
    out.append({"a": float(k[a]), "b": float(k[b]), "kind": kind, "name": name_at((s[a] + s[b]) / 2), "ha": float(h[a]), "hb": float(h[b]), "extrem": float(inner.min() if kind == "Brücke" else inner.max())})
    i = j + 1
good = ~bad
hc = np.interp(np.arange(len(h)), np.where(good)[0], h[good])
for o in out:
    print(f"km {o['a']/1000:6.2f}-{o['b']/1000:6.2f} {o['b']-o['a']:5.0f} m  {o['kind']:12s} {o['name'][:30]:30s} {o['ha']:5.1f} -> {o['hb']:5.1f}  (im Modell {o['extrem']:5.1f})")
json.dump({"k": k.tolist(), "h": hc.tolist(), "raw": raw.tolist(), "regions": out}, open("clean.json", "w"), ensure_ascii=False)
