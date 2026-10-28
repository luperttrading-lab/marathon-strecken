# Linie von goandrace.com (Kurs 2025, in Garmin Connect gezeichnet, 1436 Punkte, 42,25 km) auf das OSM-Straßennetz gelegt
# (../dl/osm_wege.json aus dem BBBike-Auszug): kürzester Weg, jede Kante kostet Länge × (1 + (Abstand zur Linie / 20 m)²),
# Fußwege, Radwege und Pfade das Dreifache. Autobahnen erlaubt: die Strecke läuft ein Stück über den Nelson Mandela Boulevard.
# Etappen von Anker zu Anker (alle 500 m ein Knoten höchstens 15 m neben der Linie, lieber auf der Fahrbahn), Gegenprobe Linie
# gegen Weg mit zusätzlichen Ankern wie in Paris. -> gpx2026.json (Punkte und laufende Länge) und ../dl/kanten.json
import json, math, re, sys, numpy as np, networkx as nx
from pyproj import Transformer
from scipy.spatial import cKDTree
T = Transformer.from_crs(4326, 32734, always_xy=True)   # UTM 34S
GPX = sys.argv[1] if len(sys.argv) > 1 else "../dl/kapstadt2025_goandrace.gpx"
t = open(GPX).read()
P = np.array([(float(a), float(b)) for a, b in re.findall(r'lat="([-\d.]+)"\s+lon="([-\d.]+)"', t)])
le, ln = T.transform(P[:, 1], P[:, 0]); M = np.c_[le, ln]
dl = np.r_[0, np.cumsum(np.hypot(*np.diff(M, axis=0).T))]
s = np.arange(0, dl[-1], 5.0); line = np.c_[np.interp(s, dl, M[:, 0]), np.interp(s, dl, M[:, 1])]
lt = cKDTree(line)
G = nx.Graph(); xy = {}; fahrbahn = set()
LANGSAM = ("footway", "cycleway", "path", "pedestrian", "track", "steps")
ZWANG = []   # keine Pflichtpunkte
# Anker alle 500 m. Dichter (200 m) liefen sie auf Gehwege neben der Voie Georges-Pompidou und erzeugten Zickzacks.
ANKER = 500.0
for w in json.load(open("../dl/osm_wege.json"))["elements"]:
    tg = w.get("tags", {})
    if tg.get("access") == "no" and tg.get("highway") not in ("motorway", "trunk", "primary"): continue
    g = w.get("geometry") or []
    if len(g) < 2: continue
    xe, yn = T.transform([q["lon"] for q in g], [q["lat"] for q in g])
    for n, x, y in zip(w["nodes"], xe, yn): xy[n] = (x, y)
    f = 3.0 if tg.get("highway") in LANGSAM else 1.0
    if f == 1.0: fahrbahn.update(w["nodes"])
    for a, b in zip(w["nodes"][:-1], w["nodes"][1:]):
        pa, pb = np.array(xy[a]), np.array(xy[b]); ln_ = float(np.hypot(*(pb - pa)))
        k = max(2, int(ln_ / 5) + 1); q = pa + (pb - pa) * np.linspace(0, 1, k)[:, None]
        dist = lt.query(q)[0].mean()
        if dist > 300: continue
        G.add_edge(a, b, length=ln_, cost=ln_ * f * (1 + (dist / 20.0) ** 2), name=tg.get("name", ""), tunnel=tg.get("tunnel", ""), bridge=tg.get("bridge", ""))
haupt = max(nx.connected_components(G), key=len)   # nur das zusammenhängende Netz (abgeschnittene Stummel am Rand der Kante-Auswahl fallen weg)
ids = np.array([n for n in xy if n in haupt]); nt = cKDTree(np.array([xy[i] for i in ids]))
anchors = []
for sa in list(np.arange(0, dl[-1], ANKER)) + [dl[-1]]:
    p = np.array([np.interp(sa, dl, M[:, 0]), np.interp(sa, dl, M[:, 1])])
    cand = nt.query_ball_point(p, 15.0 if 0 < sa < dl[-1] else 60.0)
    cand = [j for j in cand if ids[j] in fahrbahn] or cand   # Anker lieber auf der Fahrbahn als auf Gehweg-Stummeln
    if not cand: continue
    best = min(cand, key=lambda j: np.hypot(*(np.array(xy[ids[j]]) - p)))
    if not anchors or anchors[-1][1] != ids[best]: anchors.append((sa, ids[best]))
zs = [float(s[lt.query(xy[z])[1]]) for z in ZWANG]   # Lage der Pflichtpunkte auf der Linie
if ZWANG: anchors = [a for a in anchors if not (zs[0] - 300 < a[0] < zs[-1] + 300)] + list(zip(zs, ZWANG))
lauf = lambda p: sum(math.dist(xy[a], xy[b]) for a, b in zip(p, p[1:]))
def route(knoten):
    path = [knoten[0]]
    for a, b in zip(knoten[:-1], knoten[1:]):
        seg = nx.shortest_path(G, a, b, weight="cost"); path += seg[1:]
    changed = True   # Hin und zurück über dieselbe Kante (Anker auf einem Stummel) herausnehmen
    while changed:
        changed = False
        for i in range(1, len(path) - 1):
            if path[i - 1] == path[i + 1]: del path[i:i + 2]; changed = True; break
    changed = True   # kurze Schleifen zurück zum selben Knoten (unter 400 m, Anker auf einer Rampe neben der Strecke)
    while changed:
        changed = False; pos = {}
        for i, q in enumerate(path):
            if q in pos and lauf(path[pos[q]:i + 1]) < 400:
                print(f"  Schleife entfernt: {lauf(path[pos[q]:i + 1]):.0f} m"); del path[pos[q] + 1:i + 1]; changed = True; break
            pos[q] = i
    return path
for runde in range(10):
    path = route([n for _, n in sorted(anchors, key=lambda a: a[0])])
    xyp = np.array([xy[n] for n in path]); dp = np.r_[0, np.cumsum(np.hypot(*np.diff(xyp, axis=0).T))]
    wt = cKDTree(np.c_[np.interp(np.arange(0, dp[-1], 5.0), dp, xyp[:, 0]), np.interp(np.arange(0, dp[-1], 5.0), dp, xyp[:, 1])])
    back = wt.query(line)[0]; neu = []
    i = 0
    while i < len(back):   # Stücke der Linie, die der Weg auslässt (Start- und Zielbereich ausgenommen)
        if back[i] <= 40 or not (200 < s[i] < s[-1] - 200): i += 1; continue
        j = i
        while j + 1 < len(back) and back[j + 1] > 40: j += 1
        k = i + int(np.argmax(back[i:j + 1])); cand = nt.query_ball_point(line[k], 25.0)
        cand = [c for c in cand if ids[c] in fahrbahn] or cand
        if cand:
            best = ids[min(cand, key=lambda c: np.hypot(*(np.array(xy[ids[c]]) - line[k])))]
            if all(best != n for _, n in anchors): neu.append((float(s[k]), best)); print(f"  Runde {runde + 1}: Anker bei Linien-km {s[k] / 1000:.2f} ({back[k]:.0f} m daneben)")
        i = j + 1
    if not neu: break
    anchors += neu
off = lt.query(xyp)[0]
print(f"Anker {len(anchors)}, Knoten {len(path)}, Länge {dp[-1]:.0f} m (Linie {dl[-1]:.0f} m); Abstand zur Linie Median {np.median(off):.1f} m, 95 % {np.percentile(off, 95):.1f} m, max {off.max():.0f} m bei {dp[np.argmax(off)]:.0f} m")
print(f"Gegenprobe Linie -> Weg: 95 % {np.percentile(back, 95):.1f} m, max {back.max():.0f} m bei Linien-km {s[np.argmax(back)] / 1000:.2f}")
innen = (s > 200) & (s < s[-1] - 200)   # Start- und Zielbereich: Linie beginnt im Stadionvorplatz, der Weg auf der nächsten Straße
assert back[innen].max() < 60 and back.max() < 90, "Weg lässt ein Stück der Linie aus"
TI = Transformer.from_crs(32734, 4326, always_xy=True)
lo, la = TI.transform(xyp[:, 0], xyp[:, 1])
pts = [(float(a), float(b), 0.0) for a, b in zip(la, lo)]
def hav(p, q):
    R = 6371008.8; la1, lo1, la2, lo2 = map(math.radians, (p[0], p[1], q[0], q[1]))
    return 2 * R * math.asin(math.sqrt(math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))
d = [0.0]
for i in range(1, len(pts)): d.append(d[-1] + hav(pts[i - 1], pts[i]))
print("Punkte", len(pts), "Länge km", round(d[-1] / 1000, 3), "Start", pts[0][:2], "Ende", pts[-1][:2])
json.dump({"pts": pts, "d": d}, open("gpx2026.json", "w"))
json.dump({"names": [G[a][b]["name"] for a, b in zip(path, path[1:])], "tunnel": [G[a][b]["tunnel"] for a, b in zip(path, path[1:])], "bridge": [G[a][b]["bridge"] for a, b in zip(path, path[1:])]}, open("../dl/kanten.json", "w"))
