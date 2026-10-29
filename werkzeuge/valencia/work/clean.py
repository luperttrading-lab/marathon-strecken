# Brücken und übrige Stufen im Höhenprofil überbrücken -> clean.json. Das MDT02 des IGN ist ein Geländemodell (Bodenpunkte):
# auf den Brücken über das alte Turia-Bett misst es den Park im Flussbett darunter (Senke von mehreren Metern).
# Zuerst die Brücken aus OSM (bridge=yes auf der Linie, nur wo das Modell innen mehr als 0,5 m unter der Geraden zwischen den
# Enden liegt), Enden oben auf den Rampen. Danach übrige Stufen > 1,5 m paarweise wie bei den anderen Strecken.
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
from pyproj import Transformer
from scipy.spatial import cKDTree
T = Transformer.from_crs(4326, 25830, always_xy=True)
gx, gy = T.transform([x[2] for x in r], [x[1] for x in r]); baum = cKDTree(np.c_[gx, gy])
BRUECKE = {}   # OSM-Namen sind schon valencianisch („Pont de …“)
bname = {}
for w in json.load(open("../dl/osm_wege.json"))["elements"]:
    tg = w.get("tags", {})
    if tg.get("bridge") in (None, "no") or tg.get("highway") in ("motorway", "motorway_link", "footway", "steps", "cycleway", "path", "pedestrian", "corridor"): continue
    wx, wy = T.transform([q["lon"] for q in w["geometry"]], [q["lat"] for q in w["geometry"]])
    wx, wy = np.interp(np.linspace(0, len(wx) - 1, 4 * len(wx)), np.arange(len(wx)), wx), np.interp(np.linspace(0, len(wy) - 1, 4 * len(wy)), np.arange(len(wy)), wy)
    dd, ii = baum.query(np.c_[wx, wy]); ii = np.unique(ii[dd < 12])
    if len(ii) < 2: continue
    # je Durchgang ein Stück (Pont de Montolivet am Start und im Ziel). Enden: der höchste Punkt bis 30 m außerhalb der
    # OSM-Brücke, also oben auf der Rampe
    for grp in np.split(ii, np.where(np.diff(ii) > 3)[0] + 1):
        a0, b0 = int(grp.min()), int(grp.max())
        a = max(0, a0 - 3) + int(np.argmax(h[max(0, a0 - 3):a0 + 1])); b = b0 + int(np.argmax(h[b0:min(len(h), b0 + 4)]))
        line = h[a] + (h[b] - h[a]) * (np.arange(a, b + 1) - a) / max(1, b - a)
        if (line - h[a:b + 1]).max() > 1.0:   # deutlich darunter: das Flussbett liegt 3–6 m tiefer; Pont del Nou d'Octubre (0,6 m) bleibt gemessen
            osm[a + 1:b] = True; nm = tg.get("bridge:name") or tg.get("name") or ""
            for i in range(a + 1, b): bname[i] = BRUECKE.get(nm, nm)
# Zielsteg: Die letzten gut 200 m laufen auf einem Steg über dem Wasserbecken vor dem Hemisfèric und unter dem Pont de
# Montolivet hindurch. Das Modell misst dort die Wasserfläche (2,7 m, östlich der Brücke 3,2–3,4 m) und darüber die Brücke
# (9–12 m). Wasser laut OSM (natural=water, ../dl/osm_ziel.xml aus der OSM-API). Der Steg ist nicht vermessen: geschätzt
# waagerecht in Höhe des Uferwegs, auf dem die Läufer ihn erreichen (letzter Punkt vor dem Wasser).
import xml.etree.ElementTree as ET
from matplotlib.path import Path
_r = ET.parse("../dl/osm_ziel.xml").getroot(); _n = {n.get("id"): (float(n.get("lon")), float(n.get("lat"))) for n in _r.findall("node")}
wasser = []
for w in _r.findall("way"):
    if not any(t.get("k") == "natural" and t.get("v") == "water" for t in w.findall("tag")): continue
    pp = [_n[q.get("ref")] for q in w.findall("nd") if q.get("ref") in _n]
    wasser.append(Path(np.c_[T.transform([p[0] for p in pp], [p[1] for p in pp])]))
nass = np.array([k[i] > 41500 and any(p.contains_point((gx[i], gy[i])) for p in wasser) for i in range(len(h))])
w0 = int(np.argmax(nass)); assert nass[w0:].mean() > 0.9 and nass[-1], "Wasser nicht bis zum Ziel"   # Lücke unter der Brücke
h[w0:] = h[w0 - 1]; osm[w0:] = True
for i in range(w0, len(h)): bname[i] = "Zielsteg über dem Wasser"
print(f"Zielsteg ab km {k[w0 - 1] / 1000:.3f} auf {h[w0 - 1]:.2f} m, im Modell {raw[w0:].min():.2f}–{raw[w0:].max():.2f} m")
# Von Hand: Zufahrt zum Pont de les Arts auf der Carrer de Mauro Guillén (km 27,54–27,69). Die Linie liegt dort auf der Kante
# zum Flussbett, das Modell fällt um gut 2 m und springt an der Kreuzung in 10 m um 2,9 m zurück; die Straße selbst liegt bei
# 15,4–16,1 m. Wird mit der Brücke zu einem geschätzten Stück.
for i in np.where((k > 27535) & (k < 27700))[0]: osm[i] = True; bname[i] = "Pont de les Arts"
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
