# Strecke 2026 aus der Abbiegeliste des Veranstalters (../dl/pdf/26-BACM-STREET-CLOSURE-BROCHURE.pdf, „Street closures“,
# Meile für Meile Straße von … bis …) über das OSM-Straßennetz: je Abschnitt der kürzeste Weg, wobei Kanten der genannten
# Straße ihre Länge kosten, andere das Sechsfache und untere Ebenen („Lower …“) das Fünfzigfache. Ziel jedes Abschnitts ist
# die Kreuzung mit der nächsten Straße (gemeinsamer OSM-Knoten). Start: Columbus Drive an der Monroe Street (Startbox der
# offiziellen Karte und Presseberichte), Ziel: Columbus Drive kurz südlich der Balbo Drive. -> gpx2026.json
import json, math, numpy as np, networkx as nx
from pyproj import Transformer
T = Transformer.from_crs(4326, 32616, always_xy=True)
W = json.load(open("../dl/osm_wege.json"))["elements"]
COL = ["South Columbus Drive", "North Columbus Drive", "North Upper Columbus Drive", "Upper North Columbus Drive"]
LEGS = [("Columbus Dr", COL), ("Grand Ave", ["East Grand Avenue", "West Grand Avenue"]), ("Dearborn St", ["North Dearborn Street", "South Dearborn Street"]),
        ("Jackson Blvd", ["West Jackson Boulevard"]), ("LaSalle St", ["South LaSalle Street", "North LaSalle Street", "North LaSalle Drive", "West LaSalle Drive"]),
        ("Stockton Dr", ["North Stockton Drive"]), ("Fullerton Dr", ["West Fullerton Parkway"]), ("Cannon Dr", ["North Cannon Drive"]),
        ("Sheridan Rd", ["North Sheridan Road", "West Sheridan Road"]), ("Inner Lake Shore Dr", ["North Lake Shore Drive"]), ("Sheridan Rd", ["North Sheridan Road", "West Sheridan Road"]),
        ("Broadway", ["North Broadway"]), ("Clark St", ["North Clark Street"]), ("Webster Ave", ["West Webster Avenue"]),
        ("Sedgwick St", ["North Sedgwick Street"]), ("North Ave", ["West North Avenue"]), ("Wells St", ["North Wells Street", "South Wells Street"]),
        ("Wacker Dr", ["North Wacker Drive", "North Upper Wacker Drive", "South Wacker Drive", "West Wacker Drive", "West Upper Wacker Drive", "South Upper Wacker Drive"]), ("Adams St", ["West Adams Street"]),
        ("Damen Ave", ["South Damen Avenue"]), ("Jackson Blvd", ["West Jackson Boulevard"]), ("Halsted St", ["South Halsted Street"]),
        ("Taylor St", ["West Taylor Street"]), ("Loomis St", ["South Loomis Street"]), ("18th St", ["West 18th Street"]),
        ("Halsted St", ["South Halsted Street"]), ("21st St", ["West 21st Street"]), ("Canalport Ave", ["South Canalport Avenue"]),
        ("Cermak Rd", ["West Cermak Road", "East Cermak Road"]), ("Wentworth Ave", ["South Wentworth Avenue"]),
        ("26th St", ["West 26th Street", "East 26th Street"]), ("Michigan Ave", ["South Michigan Avenue"]),
        ("35th St", ["East 35th Street", "West 35th Street"]), ("Indiana Ave", ["South Indiana Avenue"]), ("31st St", ["East 31st Street"]),
        ("Michigan Ave", ["South Michigan Avenue"]), ("Roosevelt Rd", ["East Roosevelt Road"]), ("Columbus Dr", ["South Columbus Drive"])]
xy, ll, nodes_by_name, edges = {}, {}, {}, []
for w in W:
    nm = w["tags"].get("name", ""); g = w["geometry"]
    xe, yn = T.transform([q["lon"] for q in g], [q["lat"] for q in g])
    for n, x, y, q in zip(w["nodes"], xe, yn, g): xy[n] = (x, y); ll[n] = (q["lat"], q["lon"]); nodes_by_name.setdefault(nm, set()).add(n)
    for a, b in zip(w["nodes"][:-1], w["nodes"][1:]): edges.append((a, b, nm, w["tags"]))
G = nx.Graph()
for a, b, nm, tg in edges:
    ln_ = math.dist(xy[a], xy[b]); lay = tg.get("layer", "0")
    # untere Ebene: „Lower …“, level -1 oder unter der Erde ohne Tunnel-Tag (Columbus Drive unten); echte kurze Tunnel wie die
    # Grand Avenue unter der Michigan Avenue gehören zur Strecke
    G.add_edge(a, b, length=ln_, name=nm, lower=("Lower" in nm) or tg.get("level") == "-1" or (lay.startswith("-") and tg.get("tunnel") != "yes"))
# Lücken im Netz einer Straße (mehrstöckige Kreuzungen in der Innenstadt: obere Ebene, Brücke und Rampe ohne gemeinsamen
# Knoten) mit kurzen Verbindern unter 25 m schließen, sonst weicht der Weg über Parallelstraßen aus
from scipy.spatial import cKDTree
for nm_set in {tuple(n) for _, n in LEGS}:
    H = nx.Graph(); H.add_edges_from((a, b) for a, b, d in G.edges(data=True) if d["name"] in nm_set and not d["lower"])
    cc = list(nx.connected_components(H))
    for i in range(len(cc)):
        for j in range(i + 1, len(cc)):
            A, B = list(cc[i]), list(cc[j]); dd, jj = cKDTree([xy[n] for n in B]).query([xy[n] for n in A]); k = int(dd.argmin())
            if dd[k] < 25 and not G.has_edge(A[k], B[jj[k]]): G.add_edge(A[k], B[jj[k]], length=float(dd[k]), name=nm_set[0], lower=False)
def nodes(names): s = set(); [s.update(nodes_by_name.get(n, set())) for n in names]; return s
def leg_path(src, names, targets):
    ok = set(names)
    wt = lambda a, b, d: d["length"] * (50 if d["lower"] else 1 if d["name"] in ok else 6)
    dist, paths = nx.single_source_dijkstra(G, src, weight=wt)
    # nächste Kreuzung in Laufrichtung: nicht die, an der man gerade steht (Straßen, die sich zweimal treffen)
    cand = [t for t in targets if t in dist and math.dist(xy[t], xy[src]) > 15]
    best = min(cand, key=lambda t: dist[t])
    return paths[best]
def kreuzung_nahe(names, lat, lon):
    p = np.array(T.transform(lon, lat)); c = [n for n in nodes(names) if n in G]
    return min(c, key=lambda n: math.dist(xy[n], p))
start = min(nodes(COL) & nodes(["East Monroe Drive"]), key=lambda n: ll[n][1])   # im Grant Park heißt sie Monroe Drive
path = [start]
for k, (nm, names) in enumerate(LEGS[:-1]):
    nxt = LEGS[k + 1][1]; tg = nodes(names) & nodes(nxt)
    if not tg:   # ohne gemeinsamen Knoten: Knoten der nächsten Straße, die der aktuellen am nächsten liegen
        A = [n for n in nodes(names) if n in G]; B = [n for n in nodes(nxt) if n in G]
        pa = np.array([xy[n] for n in A]); pb = np.array([xy[n] for n in B])
        from scipy.spatial import cKDTree
        dd, ii = cKDTree(pa).query(pb); tg = {B[j] for j in np.argsort(dd)[:3]}; print(f"  {nm} -> {LEGS[k+1][0]}: kein gemeinsamer Knoten, {dd.min():.0f} m")
    seg = leg_path(path[-1], names, tg); path += seg[1:]
    print(f"{k+1:2d} {nm:20s} bis {LEGS[k+1][0]:20s} {sum(math.dist(xy[a], xy[b]) for a, b in zip(seg, seg[1:])):6.0f} m  Ecke {ll[seg[-1]][0]:.5f}, {ll[seg[-1]][1]:.5f}")
# letzter Abschnitt: Columbus Drive von der Roosevelt Road nach Norden bis zur Balbo Drive
balbo = kreuzung_nahe(["South Columbus Drive"], 41.8737, -87.6203)
seg = leg_path(path[-1], LEGS[-1][1], {balbo}); path += seg[1:]
xyp = np.array([xy[n] for n in path]); dp = np.r_[0, np.cumsum(np.hypot(*np.diff(xyp, axis=0).T))]
print("Knoten", len(path), "Länge bis Balbo", round(dp[-1]), "m; Start", ll[path[0]], "Balbo", ll[path[-1]])
json.dump({"path": [int(n) for n in path], "ll": [ll[n] for n in path], "d": dp.tolist(), "names": [G[a][b]["name"] for a, b in zip(path, path[1:])]}, open("../dl/strecke_roh.json", "w"))
