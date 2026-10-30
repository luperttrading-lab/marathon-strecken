# Linie des Veranstalters mit einer Berichtigung -> gpx2026.json {"pts": [[lat, lon, ele_strava], …], "d": [Linienmeter, GRS80],
# "ersatz": [s_von, s_bis] (Linienmeter der berichtigten Linie)}.
# Die Strava-Route des Veranstalters (parse.py) bleibt bei km 38,5 auf der Mesogeion bis zu ihrem Ende an der Feidippidou. Die
# Streckenbeschreibung des Veranstalters (Seite „Marathon Race“, Course Map & Route) sagt: „Immediately after Henry Dunant Hospital,
# runners continue left on Michalakopoulou Avenue, until the traffic light at the intersection of Michalakopoulou & Feidippidou
# Streets. Then they follow Feidippidou Street on the right until Kifissias junction & Alexandras Ave.“ Dieses Stück wird aus den
# OSM-Wegen ersetzt: Abzweig der Michalakopoulou von der Mesogeion (Knoten 212974582), die Michalakopoulou hinab bis zur Ampel an der
# Feidippidou (212986858), die Feidippidou hinauf bis zum Knoten Kifissias/Alexandras/Vasilissis Sofias (6370114997). Kürzeste Wege im
# OSM-Netz (Einbahnstraßen gelten nicht, die Straßen sind gesperrt), nur über Wege dieser Namen (am Ende der Feidippidou laufen die
# Fahrbahnen der Mesogeion und Abbiegespuren ohne Namen in sie hinein). Die Linie wird dadurch gut 70 m
# länger; das passt zu den Steinen der „Klassischen Marathonstrecke“ (common.py): vor dem Umweg liegt die Linie 140–165 m über
# ihren Kilometern, danach (Stein 39, Ziel) nur noch 88–91 m.
import heapq, json
import numpy as np
from pyproj import Geod, Transformer
G = Geod(ellps="GRS80"); T = Transformer.from_crs(4326, 2100, always_xy=True)
g = json.load(open("gpx_veranstalter.json")); P = [tuple(p) for p in g["pts"]]; d = np.array(g["d"])
o = json.load(open("../dl/osm_netz.json")); N = {int(k): v for k, v in o["nodes"].items()}
def pfad(a, b, namen):
    nb = {}
    for tg, refs in o["ways"].values():
        if tg.get("name") not in namen or tg.get("highway") not in ("primary", "primary_link", "secondary", "secondary_link", "tertiary"): continue
        for u, v in zip(refs, refs[1:]):
            if u in N and v in N:
                w = G.inv(N[u][1], N[u][0], N[v][1], N[v][0])[2]
                nb.setdefault(u, []).append((v, w)); nb.setdefault(v, []).append((u, w))
    dist, prev, q = {a: 0.0}, {}, [(0.0, a)]
    while q:
        du, u = heapq.heappop(q)
        if u == b: break
        if du > dist.get(u, 1e18): continue
        for v, w in nb.get(u, []):
            if du + w < dist.get(v, 1e18): dist[v] = du + w; prev[v] = u; heapq.heappush(q, (du + w, v))
    assert b in dist, ("kein Weg", a, b)
    p = [b]
    while p[-1] != a: p.append(prev[p[-1]])
    return p[::-1], dist[b]
A, J, B = 212974582, 212986858, 6370114997
F, K = 838455863, 6370133314     # Ende der Feidippidou-Fahrbahn Richtung Südost und Anfang der Fahrbahn Richtung Nordwest
p1, l1 = pfad(A, J, {"Μιχαλακοπούλου"}); p2, l2 = pfad(J, F, {"Φειδιππίδου"}); p3, l3 = pfad(K, B, {"Φειδιππίδου"})
# Zwischen F und K trennt OSM die Fahrbahnen (verbunden nur über eine Schleife der Mesogeion); auf der gesperrten Straße gerade hinüber.
umweg = [N[k] for k in p1 + p2[1:] + p3]
lfk = G.inv(N[F][1], N[F][0], N[K][1], N[K][0])[2]
print(f"Michalakopoulou {l1:.0f} m, Feidippidou {l2:.0f} + {lfk:.0f} (gerade über die Kreuzung) + {l3:.0f} m")
# Anschluss: Punkte der Linie, die A und B am nächsten liegen (je auf dem Stück zwischen zwei Linienpunkten)
xy = np.array([T.transform(p[1], p[0]) for p in P])
def naechst(la, lo, s_von, s_bis):
    q = np.array(T.transform(lo, la)); best = None
    for i in range(len(xy) - 1):
        if d[i + 1] < s_von or d[i] > s_bis: continue
        a_, v = xy[i], xy[i + 1] - xy[i]; t = float(np.clip(np.dot(q - a_, v) / (np.dot(v, v) or 1), 0, 1)); e = float(np.hypot(*(a_ + t * v - q)))
        if best is None or e < best[0]: best = (e, i, t)
    return best
ea, ia, ta = naechst(*N[A], 37500, 39500); eb, ib, tb = naechst(*N[B], 37500, 39500)
# Die Linie liegt hier auf der Fahrbahn der Mesogeion Richtung Südwest, der Abzweig A auf der Gegenfahrbahn: angeschlossen wird am
# letzten Linienpunkt davor, von dem aus A höchstens 45° neben der Laufrichtung liegt (sonst ein Zickzack quer über die Straße).
qa = np.array(T.transform(N[A][1], N[A][0]))
while ia > 0:
    r_lauf = xy[ia] - xy[ia - 1]; r_a = qa - xy[ia]
    if np.degrees(np.arccos(np.dot(r_lauf, r_a) / np.hypot(*r_lauf) / np.hypot(*r_a))) <= 45: break
    ia -= 1
ta = 0.0
print(f"Anschluss A am Linienpunkt {d[ia]:.0f} ({float(np.hypot(*(qa - xy[ia]))):.0f} m bis A), B {eb:.1f} m neben der Linie bei {d[ib] + tb * (d[ib + 1] - d[ib]):.0f}")
def ele(i, t): return P[i][2] + t * (P[i + 1][2] - P[i][2])
neu = P[:ia + 1] + [(la, lo, ele(ia, ta)) for la, lo in umweg[:1]] + [(la, lo, None) for la, lo in umweg[1:-1]] + [(umweg[-1][0], umweg[-1][1], ele(ib, tb))] + P[ib + 1:]
# Strava-Höhen auf dem neuen Stück linear
idx = [i for i, p in enumerate(neu) if p[2] is None]
_, _, dd = G.inv([p[1] for p in neu[:-1]], [p[0] for p in neu[:-1]], [p[1] for p in neu[1:]], [p[0] for p in neu[1:]])
dn = np.r_[0, np.cumsum(dd)]
if idx:
    i0, i1 = idx[0] - 1, idx[-1] + 1
    for i in idx: neu[i] = (neu[i][0], neu[i][1], neu[i0][2] + (neu[i1][2] - neu[i0][2]) * (dn[i] - dn[i0]) / (dn[i1] - dn[i0]))
s_von, s_bis = float(dn[ia + 1]), float(dn[ia + len(umweg)])
json.dump({"pts": [[round(a, 7), round(b, 7), round(e, 2)] for a, b, e in neu], "d": dn.tolist(), "ersatz": [s_von, s_bis]}, open("gpx2026.json", "w"))
print(f"Ersatzstück Linienmeter {s_von:.0f}–{s_bis:.0f}; Linie vorher {d[-1]:.1f} m, jetzt {dn[-1]:.1f} m (+{dn[-1] - d[-1]:.1f} m)")
