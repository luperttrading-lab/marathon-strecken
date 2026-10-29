# Routing-Graph aus ../dl/osm_netz.json (osm.py) und Kreuzungen benannter Straßen. Kosten = Länge × Faktor je Straßenklasse,
# gegen eine Einbahnstraße × 2,5 (zweibahnige Straßen: die Fahrbahn in Laufrichtung wird bevorzugt, eine Einbahnstraße gegen die
# Richtung bleibt möglich, die Strecke ist gesperrt). Keine Autobahnen (Periférico, Viaducto, Circuito Interior: motorway), keine Treppen.
import json, numpy as np
from pyproj import Transformer
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
T = Transformer.from_crs(4326, 32614, always_xy=True)
FAKTOR = {"trunk": 1.0, "primary": 1.0, "secondary": 1.0, "tertiary": 1.0, "trunk_link": 1.3, "primary_link": 1.3, "secondary_link": 1.3,
          "tertiary_link": 1.3, "unclassified": 1.15, "residential": 1.15, "living_street": 1.2, "road": 1.2, "pedestrian": 1.3,
          "service": 1.6, "busway": 1.6, "footway": 2.0, "path": 2.0, "track": 2.0, "cycleway": 3.0}
N = json.load(open("../dl/osm_netz.json"))
ids = sorted(int(k) for k in N["nodes"]); idx = {k: i for i, k in enumerate(ids)}
LL = np.array([N["nodes"][str(k)] for k in ids]); XY = np.c_[T.transform(LL[:, 1], LL[:, 0])]
WEGE = {int(k): v for k, v in N["ways"].items()}
rows, cols, cost = [], [], []; KANTE = {}
for wid, (t, refs) in WEGE.items():
    f = FAKTOR.get(t.get("highway"))
    if f is None or t.get("area") == "yes" or t.get("access") in ("no", "private") and t.get("highway") not in ("busway",): continue
    if t.get("tunnel") == "yes": f *= 4          # Unterführungen nur, wenn eine Wegmarke es verlangt
    ow = t.get("oneway") in ("yes", "1", "true") or t.get("junction") == "roundabout"
    rr = [idx[r] for r in refs if r in idx]
    for a, b in zip(rr[:-1], rr[1:]):
        L = float(np.hypot(*(XY[a] - XY[b])))
        for p, q, gegen in ((a, b, False), (b, a, ow)):
            c = L * f * (2.5 if gegen else 1.0)
            if (p, q) not in KANTE or c < KANTE[(p, q)][0]: KANTE[(p, q)] = (c, wid)
# Glorieta de Insurgentes: In OSM zwei Halbringe (833370216 nach Norden um die Ostseite, 833370215 nach Süden um die Westseite),
# verbunden nur über die Insurgentes nördlich der Glorieta. Die Strecke läuft ganz herum (Plan): die Nordenden beider Halbringe
# (17 m auseinander) direkt verbinden.
def _knoten_naehe(la, lo):
    x, y = T.transform(lo, la); return int(np.argmin((XY[:, 0] - x) ** 2 + (XY[:, 1] - y) ** 2))
_a, _b = _knoten_naehe(19.42429, -99.16261), _knoten_naehe(19.42435, -99.16276)
KANTE[(_a, _b)] = (float(np.hypot(*(XY[_a] - XY[_b]))), 833370215)
for (p, q), (c, wid) in KANTE.items(): rows.append(p); cols.append(q); cost.append(c)
G = csr_matrix((cost, (rows, cols)), shape=(len(ids), len(ids)))
def namen_knoten(name):
    s = set()
    for wid, (t, refs) in WEGE.items():
        if t.get("name") == name and t.get("highway") in FAKTOR: s |= {idx[r] for r in refs if r in idx}
    return s
def kreuzung(a, b, nahe=None):
    """Knoten, den Wege mit Namen a und b gemeinsam haben (bei mehreren der nächste an nahe=(lat, lon))"""
    k = namen_knoten(a) & namen_knoten(b)
    assert k, f"keine Kreuzung {a} / {b}"
    k = sorted(k)
    if nahe is None: return k[0] if len(k) == 1 else k
    x, y = T.transform(nahe[1], nahe[0]); return min(k, key=lambda i: np.hypot(XY[i, 0] - x, XY[i, 1] - y))
def naechster(la, lo, name=None, weg_id=None):
    x, y = T.transform(lo, la)
    if weg_id: kand = [idx[r] for r in WEGE[weg_id][1] if r in idx]
    else: kand = list(namen_knoten(name)) if name else range(len(ids))
    return min(kand, key=lambda i: (XY[i, 0] - x) ** 2 + (XY[i, 1] - y) ** 2)
def weg(a, b, name=None):
    """kürzester Weg a -> b; mit name: Kanten anderer Straßen kosten das Dreifache (bleibt auf der genannten Straße)"""
    g = G
    if name:
        c = np.array([KANTE[(p, q)][0] * (1 if WEGE[KANTE[(p, q)][1]][0].get("name") == name else 3) for p, q in zip(rows, cols)])
        g = csr_matrix((c, (rows, cols)), shape=G.shape)
    d, pred = dijkstra(g, indices=a, return_predecessors=True)
    assert np.isfinite(d[b]), f"kein Weg {a} -> {b}"
    p = [b]
    while p[-1] != a: p.append(pred[p[-1]])
    return p[::-1]
def kanten_weg(p, q): return KANTE.get((p, q), (None, None))[1]
