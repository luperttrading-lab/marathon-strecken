# Brücken, Durchlässe und übrige Stufen im Höhenprofil überbrücken -> clean.json. RGE ALTI ist ein Geländemodell: Brücken sind
# nicht enthalten, an Bächen (Jalles, Chenaux) misst es das Bachbett unter der Fahrbahn.
# Brücken aus OSM (bridge=yes auf der Linie, alle Wegarten außer Bahn: auf Feldwegen liegen auch Brücken), Enden oben auf den
# Rampen (höchster gemessener Punkt bis 30 m außerhalb), gerade gezogen, wo das Modell innen mehr als 0,5 m unter der Geraden liegt.
# Bahnbrücken über der Linie (Unterführungen) misst das Modell am Boden. Danach übrige Stufen > 1,5 m auf 10 m paarweise wie bei
# den anderen Strecken (Durchlässe ohne OSM-Brücke).
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official
from pyproj import Transformer
from scipy.spatial import cKDTree
r = json.load(open("dgm2026_10m.json"))
s = np.array([x[0] for x in r]); k = official(s)
raw = np.array([x[3] for x in r], float)
streets = [[o[0], o[1]] for o in json.load(open("strassen.json"))]
def street(gpx_m):
    best = streets[0]
    for e in streets:
        if e[0] <= gpx_m + 5: best = e
    return best[1]
h = raw.copy(); bad = np.zeros(len(h), bool); osm = np.zeros(len(h), bool)
T = Transformer.from_crs(4326, 2154, always_xy=True)
gx, gy = T.transform([x[2] for x in r], [x[1] for x in r]); baum = cKDTree(np.c_[gx, gy])
bname = {}
auf, bn = np.zeros(len(h), bool), {}
W = json.load(open("../dl/osm_wege.json"))["elements"]
for w in W:
    tg = w.get("tags", {}); hw = tg.get("highway")
    if tg.get("bridge") in (None, "no") or not hw: continue
    wx, wy = T.transform([q["lon"] for q in w["geometry"]], [q["lat"] for q in w["geometry"]])
    lw = np.r_[0, np.cumsum(np.hypot(np.diff(wx), np.diff(wy)))]; t = np.arange(0, lw[-1] + 2, 2.0)
    dd, ii = baum.query(np.c_[np.interp(t, lw, wx), np.interp(t, lw, wy)]); ii = np.unique(ii[dd < 12])
    if len(ii) < 1 or (len(ii) < 2 and lw[-1] > 30): continue
    auf[ii] = True
    for q in ii: bn[q] = tg.get("bridge:name") or tg.get("name") or ""
idx = np.where(auf)[0]
for grp in (np.split(idx, np.where(np.diff(idx) > 3)[0] + 1) if len(idx) else []):
    a0, b0 = int(grp.min()), int(grp.max())
    a = max(0, a0 - 3) + int(np.argmax(h[max(0, a0 - 3):a0 + 1])); b = b0 + int(np.argmax(h[b0:min(len(h), b0 + 4)]))
    if b - a < 2: a, b = max(0, a - 1), min(len(h) - 1, b + 1)
    line = h[a] + (h[b] - h[a]) * (np.arange(a, b + 1) - a) / max(1, b - a)
    tief = (line - h[a:b + 1]).max(); nm = bn[int(np.median(grp))]
    print(f"  OSM-Brücke {nm or '(ohne Namen)':22s} km {k[a0]/1000:6.2f}-{k[b0]/1000:6.2f}, Enden km {k[a]/1000:6.2f}-{k[b]/1000:6.2f}, Modell bis {tief:4.1f} m unter der Geraden")
    if tief > 0.5:
        osm[a + 1:b] = True
        for q in range(a + 1, b): bname[q] = nm
bad |= osm
kreuz = []
for w in W:
    tg = w.get("tags", {})
    if tg.get("bridge") in (None, "no") or len(w.get("geometry") or []) < 2: continue
    wx, wy = T.transform([q["lon"] for q in w["geometry"]], [q["lat"] for q in w["geometry"]])
    lw = np.r_[0, np.cumsum(np.hypot(np.diff(wx), np.diff(wy)))]; t = np.arange(0, lw[-1] + 1, 1.0)
    dd, ii = baum.query(np.c_[np.interp(t, lw, wx), np.interp(t, lw, wy)]); nah = ii[dd < 4]
    if len(nah) and not osm[nah].any() and not auf[nah].any():
        kreuz.append((round(float(k[int(np.median(nah))]) / 1000, 2), tg.get("name") or "", tg.get("railway") or tg.get("highway"), round(float(raw[int(np.median(nah))]), 1)))
print("Brücken über der Linie (Unterführungen, gemessen):", sorted(set(kreuz)))
# Stufen, die das LiDAR-HD-Geländemodell (50 cm, dgm.py) nicht hat, sind Fehler im 1-m-Raster (Graben oder Durchlass neben der
# Fahrbahn): dort LiDAR HD übernommen, an den Enden angeglichen. Bisher nur km 26,38–26,39 (Route de Bordeaux, Anstieg vom Chenal
# du Gaer: RGE ALTI 1,6 m tiefer, dann 3,3 m Stufe; LiDAR HD glatt).
lid = np.array(json.load(open("dgm_vergleich.json"))["lidar"], float)
ersetzt = []
for i in [i for i in range(len(h) - 1) if abs(h[i + 1] - h[i]) > 1.5 and not osm[i] and not osm[i + 1]]:
    if abs(lid[i + 1] - lid[i]) > 1.5: continue
    a, b = max(0, i - 3), min(len(h) - 1, i + 4)
    f = (np.arange(a, b + 1) - a) / (b - a); off = (h[a] - lid[a]) * (1 - f) + (h[b] - lid[b]) * f
    h[a:b + 1] = lid[a:b + 1] + off; ersetzt.append((round(k[i] / 1000, 2), round(float(raw[i + 1] - raw[i]), 1)))
print("Stufen nur im RGE ALTI, dort LiDAR HD:", ersetzt)
d = np.diff(h)
steps = [(i, d[i]) for i in range(len(d)) if abs(d[i]) > 1.5 and not osm[i] and not osm[i + 1]]
print("übrige Stufen > 1,5 m:", [(round(k[i] / 1000, 2), round(float(v), 1)) for i, v in steps])
def spike(i):
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
out, i = [], 0
while i < len(h):
    if not bad[i]: i += 1; continue
    j = i
    while j + 1 < len(h) and bad[j + 1]: j += 1
    a, b = max(0, i - 1), min(len(h) - 1, j + 1)
    inner = raw[i:j+1]
    kind = "Brücke" if (inner.mean() < min(raw[a], raw[b]) or osm[i:j + 1].any()) else "Unterführung"
    nm = next((bname[q] for q in range(i, j + 1) if bname.get(q)), None) or street((s[a] + s[b]) / 2)
    out.append({"a": float(k[a]), "b": float(k[b]), "kind": kind, "name": nm, "ha": float(raw[a]), "hb": float(raw[b]), "extrem": float(inner.min() if kind == "Brücke" else inner.max())})
    i = j + 1
good = ~bad
hc = np.interp(np.arange(len(h)), np.where(good)[0], h[good])
for o in out:
    print(f"km {o['a']/1000:6.2f}-{o['b']/1000:6.2f} {o['b']-o['a']:5.0f} m  {o['kind']:12s} {o['name']:30s} {o['ha']:6.1f} -> {o['hb']:6.1f}  (im Modell {o['extrem']:6.1f})")
json.dump({"k": k.tolist(), "h": hc.tolist(), "raw": raw.tolist(), "regions": out}, open("clean.json", "w"), ensure_ascii=False)
