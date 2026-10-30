# Routing-Graph aus ../dl/osm_netz.json (osm.py) und Kreuzungen benannter Straßen (wie Mexiko-Stadt). Kosten = Länge × Faktor je
# Straßenklasse, gegen eine Einbahnstraße × 2,5 (die Strecke ist gesperrt, auf zweibahnigen Straßen wird die Fahrbahn in
# Laufrichtung bevorzugt). Fußgängerzonen zählen wie Straßen (Via dei Fori Imperiali, Via del Corso, Piazza del Popolo), keine
# Autobahnen, keine Treppen; Tunnel nur, wo eine Wegmarke es verlangt („Sottopasso di Ripetta“).
import json, numpy as np
from pyproj import Transformer
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
T = Transformer.from_crs(4326, 32633, always_xy=True)   # UTM 33 N
FAKTOR = {"trunk": 1.0, "primary": 1.0, "secondary": 1.0, "tertiary": 1.0, "trunk_link": 1.3, "primary_link": 1.3, "secondary_link": 1.3,
          "tertiary_link": 1.3, "unclassified": 1.1, "residential": 1.1, "living_street": 1.1, "road": 1.2, "pedestrian": 1.05,
          "service": 1.6, "busway": 1.6, "footway": 1.6, "path": 2.0, "track": 2.0, "cycleway": 2.5}
N = json.load(open("../dl/osm_netz.json"))
ids = sorted(int(k) for k in N["nodes"]); idx = {k: i for i, k in enumerate(ids)}
LL = np.array([N["nodes"][str(k)] for k in ids]); XY = np.c_[T.transform(LL[:, 1], LL[:, 0])]
WEGE = {int(k): v for k, v in N["ways"].items()}
rows, cols, cost = [], [], []; KANTE = {}
for wid, (t, refs) in WEGE.items():
    f = FAKTOR.get(t.get("highway"))
    if f is None or t.get("access") in ("no", "private") and t.get("highway") not in ("busway", "pedestrian"): continue
    if t.get("area") == "yes": f *= 1.2             # Platzflächen: am Rand entlang, wie die Wege der Fläche
    if t.get("tunnel") in ("yes", "building_passage"): f *= 4   # Unterführungen nur, wenn eine Wegmarke es verlangt
    ow = t.get("oneway") in ("yes", "1", "true") or t.get("junction") == "roundabout"
    rr = [idx[r] for r in refs if r in idx]
    for a, b in zip(rr[:-1], rr[1:]):
        L = float(np.hypot(*(XY[a] - XY[b])))
        for p, q, gegen in ((a, b, False), (b, a, ow)):
            c = L * f * (2.5 if gegen else 1.0)
            if (p, q) not in KANTE or c < KANTE[(p, q)][0]: KANTE[(p, q)] = (c, wid)
for (p, q), (c, wid) in KANTE.items(): rows.append(p); cols.append(q); cost.append(c)
rows, cols, cost = np.array(rows), np.array(cols), np.array(cost)
G = csr_matrix((cost, (rows, cols)), shape=(len(ids), len(ids)))
KW = np.array([KANTE[(p, q)][1] for p, q in zip(rows, cols)])
NAME_W = {wid: t.get("name", "") for wid, (t, _) in WEGE.items()}
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
    if nahe is None:
        assert len(k) == 1, f"{len(k)} Kreuzungen {a} / {b}: nahe angeben"
        return k[0]
    x, y = T.transform(nahe[1], nahe[0]); return min(k, key=lambda i: np.hypot(XY[i, 0] - x, XY[i, 1] - y))
def naechster(la, lo, name=None, weg_id=None):
    x, y = T.transform(lo, la)
    if weg_id: kand = [idx[r] for r in WEGE[weg_id][1] if r in idx]
    else: kand = list(namen_knoten(name)) if name else range(len(ids))
    assert len(kand), f"kein Knoten {name}"
    return min(kand, key=lambda i: (XY[i, 0] - x) ** 2 + (XY[i, 1] - y) ** 2)
def weg(a, b, name=None):
    """kürzester Weg a -> b; mit name (Text oder Liste): Kanten anderer Straßen kosten das Dreifache (bleibt auf der Straße)"""
    g = G
    if name:
        nn = {name} if isinstance(name, str) else set(name)
        fak = np.array([1.0 if NAME_W[w] in nn else 3.0 for w in KW])
        g = csr_matrix((cost * fak, (rows, cols)), shape=G.shape)
    d, pred = dijkstra(g, indices=a, return_predecessors=True)
    assert np.isfinite(d[b]), f"kein Weg {a} -> {b}"
    p = [b]
    while p[-1] != a: p.append(pred[p[-1]])
    return p[::-1]
def kanten_weg(p, q): return KANTE.get((p, q), (None, None))[1]
