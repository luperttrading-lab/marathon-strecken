# Routing-Graph aus ../dl/osm_netz.json (osm.py), wie bei Mexiko-Stadt. Kosten = Länge × Faktor je Straßenklasse. Einbahnstraßen
# zählen nicht (GEGEN = 1): Die Strecke ist gesperrt, und mehrere Abschnitte laufen gegen die Fahrtrichtung (Ronda de Sant Pere,
# Carrer d'Aragó …); auf zweibahnigen Straßen hält die Planlinie (linie.py) die Linie ohnehin in der Nähe. Ohne Autobahnen und ohne die Stadtautobahnen Ronda Litoral und Ronda de Dalt (in OSM „trunk“, die Ronda
# Litoral liegt in Trog und Tunnel neben der Avinguda del Litoral und unter dem Passeig de Colom) und ohne ihre Rampen (trunk_link),
# Tunnel × 4, keine Treppen.
# Namen: „Gran Via de les Corts Catalanes (lateral mar)“ usw. zählt als „Gran Via de les Corts Catalanes“ (Seitenfahrbahnen).
import json, re, numpy as np
from pyproj import Transformer
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
T = Transformer.from_crs(4326, 25831, always_xy=True)
FAKTOR = {"trunk": 1.0, "primary": 1.0, "secondary": 1.0, "tertiary": 1.0, "primary_link": 1.3, "secondary_link": 1.3,
          "tertiary_link": 1.3, "unclassified": 1.15, "residential": 1.15, "living_street": 1.2, "road": 1.2, "pedestrian": 1.3,
          "service": 1.6, "busway": 1.6, "footway": 2.0, "path": 2.0, "track": 2.0, "cycleway": 3.0}
N = json.load(open("../dl/osm_netz.json"))
ids = sorted(int(k) for k in N["nodes"]); idx = {k: i for i, k in enumerate(ids)}
LL = np.array([N["nodes"][str(k)] for k in ids]); XY = np.c_[T.transform(LL[:, 1], LL[:, 0])]
WEGE = {int(k): v for k, v in N["ways"].items()}
OHNE = ("Ronda Litoral", "Ronda del Litoral", "Ronda de Dalt")
basis = lambda n: re.sub(r"\s*\(.*?\)\s*$", "", n or "")
GEGEN = 1.0
rows, cols, cost = [], [], []; KANTE = {}
for wid, (t, refs) in WEGE.items():
    f = FAKTOR.get(t.get("highway"))
    if f is None or t.get("area") == "yes" or basis(t.get("name")) in OHNE or t.get("access") in ("no", "private") and t.get("highway") not in ("busway",): continue
    if t.get("tunnel") in ("yes", "building_passage") or t.get("layer", "0").startswith("-"): f *= 4   # Unterführungen nur, wenn eine Wegmarke es verlangt
    ow = t.get("oneway") in ("yes", "1", "true") or t.get("junction") == "roundabout"
    rr = [idx[r] for r in refs if r in idx]
    for a, b in zip(rr[:-1], rr[1:]):
        L = float(np.hypot(*(XY[a] - XY[b])))
        for p, q, gegen in ((a, b, False), (b, a, ow)):
            c = L * f * (GEGEN if gegen else 1.0)
            if (p, q) not in KANTE or c < KANTE[(p, q)][0]: KANTE[(p, q)] = (c, wid)
for (p, q), (c, wid) in KANTE.items(): rows.append(p); cols.append(q); cost.append(c)
rows, cols, cost = np.array(rows), np.array(cols), np.array(cost)
G = csr_matrix((cost, (rows, cols)), shape=(len(ids), len(ids)))
KW = np.array([KANTE[(p, q)][1] for p, q in zip(rows, cols)])
NAME = np.array([basis(WEGE[w][0].get("name", "")) for w in KW])
MITTE = (XY[rows] + XY[cols]) / 2
from scipy.sparse.csgraph import connected_components
_n, _lab = connected_components(G, directed=False); NETZ = set(np.where(_lab == np.bincount(_lab).argmax())[0].tolist())   # zusammenhängendes Netz
def namen_knoten(name):
    s = set()
    for wid, (t, refs) in WEGE.items():
        if basis(t.get("name")) == name and t.get("highway") in FAKTOR and t.get("highway") not in ("footway", "path", "cycleway") and t.get("area") != "yes":
            s |= {idx[r] for r in refs if r in idx}
    return s & NETZ
def kreuzung(a, b, nahe=None):
    """Knoten, den Wege mit Namen a und b gemeinsam haben (bei mehreren der nächste an nahe=(lat, lon))"""
    k = namen_knoten(a) & namen_knoten(b)
    assert k, f"keine Kreuzung {a} / {b}"
    k = sorted(k)
    if nahe is None:
        assert len(k) == 1 or np.ptp(XY[k], axis=0).max() < 60, f"{a} / {b}: {len(k)} Kreuzungen weit auseinander"
        return k[0]
    x, y = T.transform(nahe[1], nahe[0]); return min(k, key=lambda i: np.hypot(XY[i, 0] - x, XY[i, 1] - y))
FAHRBAHN = {"trunk", "primary", "secondary", "tertiary", "trunk_link", "primary_link", "secondary_link", "tertiary_link",
            "unclassified", "residential", "living_street", "road", "pedestrian"}
STRASSENKNOTEN = sorted({idx[r] for wid, (t, refs) in WEGE.items() if t.get("highway") in FAHRBAHN and basis(t.get("name")) not in OHNE
                         and t.get("area") != "yes" for r in refs if r in idx} & NETZ)
def naechster(la, lo, name=None, weg_id=None):
    """nächster Knoten einer Fahrbahn (ohne Fuß- und Radwege), wahlweise nur auf Straßen dieses Namens oder auf einem Weg"""
    x, y = T.transform(lo, la)
    if weg_id: kand = [idx[r] for r in WEGE[weg_id][1] if r in idx]
    else: kand = list(namen_knoten(name)) if name else STRASSENKNOTEN
    return min(kand, key=lambda i: (XY[i, 0] - x) ** 2 + (XY[i, 1] - y) ** 2)
def weg(a, b, name=None, faktor=None):
    """kürzester Weg a -> b; mit name: Kanten anderer Straßen kosten das Dreifache (bleibt auf der genannten Straße);
    faktor: zusätzlicher Kostenfaktor je Kante (z. B. Abstand zur Linie des Plans)"""
    c = cost.copy()
    if name: c = c * np.where(NAME == name, 1.0, 3.0)
    if faktor is not None: c = c * faktor
    g = csr_matrix((c, (rows, cols)), shape=G.shape)
    d, pred = dijkstra(g, indices=a, return_predecessors=True)
    assert np.isfinite(d[b]), f"kein Weg {a} -> {b}"
    p = [b]
    while p[-1] != a: p.append(pred[p[-1]])
    return p[::-1]
def kanten_weg(p, q): return KANTE.get((p, q), (None, None))[1]
