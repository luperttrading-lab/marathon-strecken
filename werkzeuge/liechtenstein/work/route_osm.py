# Linie der Strecke aus OSM-Wegen, geführt vom Streckenplan des Veranstalters (plan.py). Eine GPX-Datei veröffentlicht der Veranstalter
# nicht (die Seite verweist nur auf eine Aufzeichnung bei AllTrails, Download mit Konto; nicht genutzt).
# 1. Die Plan-Linie wird geordnet: Pixelraster 3 × 3 px, Nachbarn bis 60 px (Lücken an Pfeilspitzen und Kästen), kürzeste Wege zwischen
#    Ankerpunkten in Laufrichtung (Start, Spitze der Schleife in Vaduz, Steg, Nordende Valorsch, Turna, Westspitze Malbun, Ziel).
# 2. Die Lage der Plan-Linie wird an das OSM-Wegnetz angepasst (affin, iterativ: je Zelle der nächste Weg bis 120 m, gewichtet).
# 3. Route auf dem OSM-Wegnetz zwischen denselben Ankern; Kosten je Wegstück = Länge × (1 + ((Abstand zur Plan-Linie − 15 m) / 35 m)²),
#    also der kürzeste Weg, der der gezeichneten Linie folgt; ein schon gelaufenes Stück kostet danach das Vierfache (Schleife in Malbun).
#    Feste Zwischenpunkte (via.json) dort, wo der Plan zwei Wege offenlässt, mit Begründung (Laufbericht 2023, Postenliste, Lagepläne).
# -> gpx2026.json {"pts": [[lat, lon, 0], …], "d": [laufende Länge, geodätisch], "wege": [OSM-Weg je Punkt]}, plan_geordnet.json
import json, sys
import numpy as np, networkx as nx
from pyproj import Transformer, Geod
from scipy.spatial import cKDTree
T = Transformer.from_crs(4326, 2056, always_xy=True); TI = Transformer.from_crs(2056, 4326, always_xy=True)
pl = json.load(open("../dl/plan_lv95.json")); PX = np.array(pl["px"], float); cx, cy = map(np.array, pl["affin"])
o = json.load(open("../dl/osm_netz.json")); N = o["nodes"]
OHNE = {"motorway", "motorway_link", "trunk_link", "construction", "proposed", "raceway", "bus_guideway", "platform", "corridor", "elevator", "via_ferrata"}
# Graph
G = nx.Graph(); XY = {}
for wid, (tg, refs) in o["ways"].items():
    hw = tg.get("highway")
    if not hw or hw in OHNE or tg.get("area") == "yes": continue
    ids = [r for r in refs if str(r) in N]
    if len(ids) < 2: continue
    for r in ids:
        if r not in XY:
            la, lo = N[str(r)]; XY[r] = T.transform(lo, la)
    for a, b in zip(ids[:-1], ids[1:]):
        if a == b: continue
        G.add_edge(a, b, w=wid, L=float(np.hypot(XY[a][0] - XY[b][0], XY[a][1] - XY[b][1])))
knr = np.array(list(XY.keys())); kxy = np.array([XY[k] for k in knr]); kbaum = cKDTree(kxy)
# dichte Punkte der Wege für die Anpassung
dp = []
for a, b in G.edges():
    pa, pb = np.array(XY[a]), np.array(XY[b]); n = max(2, int(G[a][b]["L"] / 5) + 1)
    dp.extend(pa + f * (pb - pa) for f in np.linspace(0, 1, n))
dp = np.array(dp); dbaum = cKDTree(dp)
print(G.number_of_nodes(), "Knoten,", G.number_of_edges(), "Kanten", flush=True)
# 1. Plan-Linie ordnen (im Bild): Zellen 3 × 3 px, Nachbarn bis 60 px; Sprünge über Lücken (Pfeilspitzen, entfernte Kästen) kosten
#    d³/36, damit der Weg nie über eine Kehre abkürzt
zell = {}
for i, (x, y) in enumerate(PX.astype(int) // 3): zell.setdefault((x, y), []).append(i)
zk = list(zell); zpx = np.array(zk, float) * 3 + 1
zb = cKDTree(zpx); H = nx.Graph()
for i, j in zb.query_pairs(60):
    d = np.hypot(*(zpx[i] - zpx[j])); H.add_edge(i, j, w=d if d <= 6 else d ** 3 / 36)
ANKER = [((705, 285), "Start Bendern"), ((1044, 1476), "Vaduz, Nordspitze der Schleife"), ((1791, 2304), "Steg, Südspitze"),
         ((1890, 1560), "Valorsch, Nordende"), ((2346, 2565), "Malbun, Turna (Südostende)"), ((2282, 2537), "Malbun, vor dem Pfeil (Südwestseite)"),
         ((2250, 2500), "Malbun, nach dem Pfeil"), ((2210, 2480), "Malbun, Panoramaweg Südwest"),
         ((2097, 2365), "Malbun, Westspitze"),
         ((2215, 2337), "Ziel Malbun")]
ai = [int(zb.query(p)[1]) for p, _ in ANKER]
ordn = []
for a, b in zip(ai[:-1], ai[1:]):
    seg = [a, b] if np.hypot(*(zpx[a] - zpx[b])) < 60 else nx.shortest_path(H, a, b, weight="w")    # Anker beiderseits einer Lücke: direkt
    ordn.extend(seg if not ordn else seg[1:])
OPX = zpx[ordn]
# 2. affine Anpassung (ICP) der geordneten Linie an das Wegnetz
A = np.c_[OPX, np.ones(len(OPX))]
for it in range(12):
    P = np.c_[A @ cx, A @ cy]
    dist, j = dbaum.query(P, distance_upper_bound=120 if it < 6 else 60)
    ok = np.isfinite(dist)
    w = 1 / (1 + (dist[ok] / 20) ** 2)
    Z = dp[j[ok]]
    cx = np.linalg.lstsq(A[ok] * w[:, None], Z[:, 0] * w, rcond=None)[0]
    cy = np.linalg.lstsq(A[ok] * w[:, None], Z[:, 1] * w, rcond=None)[0]
    print(f"  Anpassung {it}: {ok.mean() * 100:.0f} % der Zellen bei einem Weg, Median {np.median(dist[ok]):.1f} m", flush=True)
PL = np.c_[A @ cx, A @ cy]
dist, _ = dbaum.query(PL); print(f"  danach: Median-Abstand Plan–Weg {np.median(dist):.1f} m, 90 % unter {np.percentile(dist, 90):.0f} m, "
                                f"{np.hypot(cx[0], cy[0]):.3f} m je Pixel, Drehung {np.degrees(np.arctan2(cy[0], cx[0])):.2f}°")
# glätten (gleitendes Mittel über 5 Zellen) und dicht legen
PLs = np.array([PL[max(0, i - 2):i + 3].mean(axis=0) for i in range(len(PL))])
lp = np.r_[0, np.cumsum(np.hypot(*np.diff(PLs, axis=0).T))]
ss = np.arange(0, lp[-1], 5.0); PLd = np.c_[np.interp(ss, lp, PLs[:, 0]), np.interp(ss, lp, PLs[:, 1])]
print(f"Plan-Linie geordnet: {lp[-1] / 1000:.2f} km (Grafik, geglättet)")
json.dump({"lv95": PLd.round(1).tolist(), "s": ss.tolist(), "affin": [cx.tolist(), cy.tolist()],
           "anker": [[float(lp[ordn.index(a)]), n] for a, (_, n) in zip(ai, ANKER)]}, open("plan_geordnet.json", "w"), ensure_ascii=False)
zxy = np.c_[np.c_[zpx, np.ones(len(zpx))] @ cx, np.c_[zpx, np.ones(len(zpx))] @ cy]
pb = cKDTree(PLd)
# 3. Route
for a, b, dd in G.edges(data=True):
    pa, pb_ = np.array(XY[a]), np.array(XY[b]); n = max(2, int(dd["L"] / 10) + 1)
    d = pb.query(np.array([pa + f * (pb_ - pa) for f in np.linspace(0, 1, n)]))[0].mean()
    dd["c"] = dd["L"] * (1 + (max(0.0, d - 15) / 35) ** 2)
# feste Zwischenpunkte aus via.json: [lat, lon, Begründung, nach Anker]; sie folgen in der Reihenfolge der Datei auf den genannten Anker.
# Die Anker „vor/nach dem Pfeil“ dienen nur dem Ordnen der Plan-Linie, nicht der Route.
NUR_ORDNEN = {"Malbun, vor dem Pfeil (Südwestseite)", "Malbun, nach dem Pfeil"}
VIA = json.load(open("via.json")) if "--ohne-via" not in sys.argv else []
reihe = []
for a_, (_, n) in zip(ai, ANKER):
    if n not in NUR_ORDNEN: reihe.append((PLd[pb.query(zxy[a_])[1]], n, False))
    for la, lo, t, nach in VIA:
        if nach == n: reihe.append((np.array(T.transform(lo, la)), t, True))
assert all(v[3] in [n for _, n in ANKER] for v in VIA), "via.json: unbekannter Anker"
def knoten_bei(p):
    for r in (25, 60, 120):
        c = kbaum.query_ball_point(p, r)
        if c: return int(knr[min(c, key=lambda i: np.hypot(*(kxy[i] - p)))])
    raise SystemExit(f"kein Weg bei {p}")
weg, wege = [], []
nx.set_edge_attributes(G, 1.0, "mal")
for (pa, na, va), (pb2, nb, vb) in zip(reihe[:-1], reihe[1:]):
    ka, kb = knoten_bei(pa), knoten_bei(pb2)
    # zwischen zwei festen Zwischenpunkten zählt nur die Länge (die Plan-Linie ist dort zu grob, z. B. im Zentrum von Vaduz)
    gew = (lambda u, v, e: e["L"] * e["mal"]) if (va and vb) else (lambda u, v, e: e["c"] * e["mal"])
    seg = nx.shortest_path(G, ka, kb, weight=gew)
    weg.extend(seg if not weg else seg[1:])
    for u, v in zip(seg[:-1], seg[1:]): G[u][v]["mal"] *= 4      # schon gelaufen: ein zweites Mal nur, wenn es keinen anderen Weg gibt
    print(f"  {na} -> {nb}: {sum(G[u][v]['L'] for u, v in zip(seg[:-1], seg[1:])) / 1000:.2f} km")
for u, v in zip(weg[:-1], weg[1:]): wege.append(G[u][v]["w"])
wege.append(wege[-1])
xy = np.array([XY[k] for k in weg]); lo, la = TI.transform(xy[:, 0], xy[:, 1])
g = Geod(ellps="GRS80"); _, _, dd = g.inv(lo[:-1], la[:-1], lo[1:], la[1:]); d = np.r_[0, np.cumsum(dd)]
abst = pb.query(xy)[0]
print(f"Linie aus OSM: {len(weg)} Punkte, {d[-1]:.0f} m; Abstand zur Plan-Linie Median {np.median(abst):.0f} m, 95 % unter {np.percentile(abst, 95):.0f} m, "
      f"größter {abst.max():.0f} m bei Linienmeter {d[np.argmax(abst)]:.0f}")
json.dump({"pts": [[float(a), float(b), 0.0] for a, b in zip(la, lo)], "d": d.tolist(), "wege": wege, "knoten": [int(k) for k in weg]},
          open("gpx2026.json", "w"))
