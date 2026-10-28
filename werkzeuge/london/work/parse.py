"""Strecke aus der OSM-Relation „London Marathon (Blue Start)“ (13319641, route=running). Die Wege stehen fast in Laufrichtung
in der Relation, in Limehouse aber als Block an falscher Stelle: Narrow Street (Hinweg, Wege 702–728) steht hinter der Runde
über die Isle of Dogs. Reihenfolge deshalb 0–493, 702–728, 494–701, 729–Ende. Auf der Rückfahrt über The Highway (Butcher Row
bis Tower) fehlen Wege; Lücken werden über den kürzesten Weg im OSM-Straßennetz geschlossen (../dl/osm_wege.json).
-> gpx2026.json {"pts": [[lat, lon, 0]], "d": [...]}"""
import json, math, heapq
E = json.load(open("../dl/rel_13319641.json"))["elements"]; r = [e for e in E if e["type"] == "relation"][0]
K = math.cos(math.radians(51.5)); P = lambda a: (a[1] * K * 111320, a[0] * 110574)
key = lambda g: (round(g["lat"], 7), round(g["lon"], 7))
ws = [[key(g) for g in m["geometry"]] for m in r["members"] if m["type"] == "way"]
ORDNUNG = list(range(0, 494)) + list(range(702, 729)) + list(range(494, 702)) + list(range(729, len(ws)))
adj = {}
for w in json.load(open("../dl/osm_wege.json"))["elements"]:
    if w["tags"].get("highway") in ("footway", "cycleway") or w["tags"].get("level", "0").startswith("-"): continue
    g = [key(x) for x in w["geometry"]]
    for a, b in zip(g, g[1:]):
        d_ = math.dist(P(a), P(b)); adj.setdefault(a, []).append((b, d_)); adj.setdefault(b, []).append((a, d_))
def kuerzest(s, t):
    dist, prev, q = {s: 0}, {}, [(0, s)]
    while q:
        du, u = heapq.heappop(q)
        if u == t: break
        if du > dist[u] or du > 3000: continue
        for v, w in adj.get(u, []):
            if du + w < dist.get(v, 1e18): dist[v] = du + w; prev[v] = u; heapq.heappush(q, (du + w, v))
    if t not in dist: return None, None
    p = [t]
    while p[-1] != s: p.append(prev[p[-1]])
    return p[::-1], dist[t]
line = list(ws[ORDNUNG[0]])
n1 = ws[ORDNUNG[1]]
if min(math.dist(P(line[0]), P(x)) for x in (n1[0], n1[-1])) < min(math.dist(P(line[-1]), P(x)) for x in (n1[0], n1[-1])): line.reverse()
for k in ORDNUNG[1:]:
    w = ws[k]; a, b = math.dist(P(line[-1]), P(w[0])), math.dist(P(line[-1]), P(w[-1]))
    seg = w if a <= b else w[::-1]
    if min(a, b) > 1:
        fill, L = kuerzest(line[-1], seg[0])
        if fill: line += fill[1:-1]; print(f"Lücke vor Weg {k}: {min(a, b):.0f} m Luftlinie, über das Straßennetz {L:.0f} m")
        else: print(f"Lücke vor Weg {k}: {min(a, b):.0f} m, nicht verbunden")
    line += seg[1:] if seg[0] == line[-1] else seg
# Hin und zurück auf demselben Stück (Wege der Relation in Gegenrichtung, Lückenfüller): Schleifen, die nach höchstens
# 600 m an denselben Knoten zurückkehren, herausschneiden (... A B C B A ... -> ... A ...)
def lauf(p): return sum(math.dist(P(a), P(b)) for a, b in zip(p, p[1:]))
geaendert = True
while geaendert:
    geaendert = False; pos = {}
    for i, q in enumerate(line):
        if q in pos and lauf(line[pos[q]:i + 1]) < 600:
            print(f"  Schleife entfernt: {lauf(line[pos[q]:i + 1]):.0f} m bei {q}"); del line[pos[q] + 1:i + 1]; geaendert = True; break
        pos[q] = i
def hav(a, b):
    R = 6371008.8; la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    return 2 * R * math.asin(math.sqrt(math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))
d = [0.0]
for a, b in zip(line, line[1:]): d.append(d[-1] + hav(a, b))
print("Start", line[0], "Ziel", line[-1], "Punkte", len(line), "Länge", round(d[-1], 1))
json.dump({"pts": [[a, b, 0.0] for a, b in line], "d": d}, open("gpx2026.json", "w"))
