# Brücken und übrige Stufen im Höhenprofil überbrücken -> clean.json. Das GSI-Modell (DEM5A) ist ein Geländemodell: auf Brücken
# misst es Fluss oder Kanal darunter (Senke), in Nishi-Shinjuku auf der oberen Ebene (Tochō-dōri, Gijidō-dōri) die Querstraßen.
# Zuerst die Brücken aus OSM (bridge=yes auf der Linie, nur wo das Modell innen mehr als 0,5 m unter der Geraden zwischen den
# Enden liegt): Die Kanalbrücken in Kōtō sind gewölbt, ihre Rampen misst das Modell richtig, nur die Fahrbahn fehlt; die reine
# Stufensuche glättete dort die Rampe statt der Senke. Danach übrige Stufen > 1,5 m paarweise wie bei den anderen Strecken.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official
r = json.load(open("dgm2026_10m.json"))
s = np.array([x[0] for x in r]); k = official(s)
raw = np.array([x[3] for x in r], float)   # Geländemodell, keine Punktwolke
from namen import umschrift
streets = [[o[0], umschrift(o[1]) or ""] for o in json.load(open("strassen.json"))]
def street(gpx_m):
    best = streets[0]
    for e in streets:
        if e[0] <= gpx_m + 5: best = e   # Straßen alle 10 m
    return best[1]
h = raw.copy(); bad = np.zeros(len(h), bool); osm = np.zeros(len(h), bool)
from pyproj import Transformer
from scipy.spatial import cKDTree
T = Transformer.from_crs(4326, 32654, always_xy=True)
gx, gy = T.transform([x[2] for x in r], [x[1] for x in r]); baum = cKDTree(np.c_[gx, gy])
BRUECKE = {"日本橋": "Nihonbashi", "茅場橋": "Kayaba-bashi", "浅草橋": "Asakusa-bashi", "蔵前橋": "Kuramae-bashi", "高橋": "Takahashi",
           "海辺橋": "Umibe-bashi", "芝園橋": "Shibazono-bashi", "万世橋": "Mansei-bashi", "水道橋 (Suidobashi Bridge)": "Suidō-bashi",
           "都庁通り": "Tochō-dōri, obere Ebene", "議事堂通り": "Gijidō-dōri, obere Ebene", "外堀通り": "Sotobori-dōri"}
bname = {}
for w in json.load(open("../dl/osm_wege.json"))["elements"]:
    tg = w.get("tags", {})
    if tg.get("bridge") in (None, "no") or tg.get("highway") in ("motorway", "motorway_link", "footway", "steps", "cycleway", "path", "pedestrian", "corridor"): continue
    wx, wy = T.transform([q["lon"] for q in w["geometry"]], [q["lat"] for q in w["geometry"]])
    wx, wy = np.interp(np.linspace(0, len(wx) - 1, 4 * len(wx)), np.arange(len(wx)), wx), np.interp(np.linspace(0, len(wy) - 1, 4 * len(wy)), np.arange(len(wy)), wy)
    dd, ii = baum.query(np.c_[wx, wy]); ii = np.unique(ii[dd < 12])
    if len(ii) < 2: continue
    # je Durchgang ein Stück (Brücken auf Hin- und Rückweg, z. B. Shibazono-bashi km 36,6 und 38,4). Enden: der höchste Punkt
    # bis 30 m außerhalb der OSM-Brücke, also oben auf der Rampe (sonst läge die gewölbte Fahrbahn zu tief)
    for grp in np.split(ii, np.where(np.diff(ii) > 3)[0] + 1):
        a0, b0 = int(grp.min()), int(grp.max())
        a = max(0, a0 - 3) + int(np.argmax(h[max(0, a0 - 3):a0 + 1])); b = b0 + int(np.argmax(h[b0:min(len(h), b0 + 4)]))
        line = h[a] + (h[b] - h[a]) * (np.arange(a, b + 1) - a) / max(1, b - a)
        if (line - h[a:b + 1]).max() > 0.5:
            osm[a + 1:b] = True; nm = tg.get("bridge:name") or tg.get("name") or ""
            for i in range(a + 1, b): bname[i] = BRUECKE.get(nm, nm)
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
