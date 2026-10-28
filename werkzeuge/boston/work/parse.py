"""Strecke aus der OSM-Relation „Boston Marathon“ (11680552, route=running): die Wege sind nicht geordnet; ein Graph aus
allen Wegpunkten, kürzester Weg vom Startpunkt (Rolle start) zum Ziel (Rolle end). → gpx2026.json (danach mit Haversine-Metern umgeschrieben: {"pts": [[lat, lon, 0]], "d": [...]})"""
import json, math, heapq

d = json.load(open("../dl/relation.json"))["elements"][0]
K = math.cos(math.radians(42.3))
P = lambda a: (a[1] * K * 111320, a[0] * 110574)
key = lambda g: (round(g["lat"], 7), round(g["lon"], 7))
adj = {}
for m in d["members"]:
    if m["type"] != "way": continue
    g = [key(x) for x in m["geometry"]]
    for a, b in zip(g, g[1:]):
        w = math.dist(P(a), P(b)); adj.setdefault(a, []).append((b, w)); adj.setdefault(b, []).append((a, w))
start = next(key(m) for m in d["members"] if m.get("role") == "start")
ziel = next(key(m) for m in d["members"] if m.get("role") == "end")
assert start in adj and ziel in adj, (start in adj, ziel in adj)
dist, prev, q = {start: 0}, {}, [(0, start)]
while q:
    du, u = heapq.heappop(q)
    if u == ziel: break
    if du > dist[u]: continue
    for v, w in adj[u]:
        if du + w < dist.get(v, 1e18): dist[v] = du + w; prev[v] = u; heapq.heappush(q, (du + w, v))
pfad = [ziel]
while pfad[-1] != start: pfad.append(prev[pfad[-1]])
pfad.reverse()
print("Punkte", len(pfad), "Länge m", round(dist[ziel], 1))
json.dump([list(p) for p in pfad], open("gpx2026.json", "w"))
