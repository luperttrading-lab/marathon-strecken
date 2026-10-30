# Streckenlinie auf dem OSM-Wegenetz, nach dem Streckenplan 2026 des Veranstalters (pdflinie.py) Straße für Straße:
# Abschnitte von Kreuzung zu Kreuzung, je Abschnitt die Straßennamen laut Plan; kürzeste Wege auf dem Netz (alle Wege außer
# Autobahnen und Treppen, Einbahnstraßen gelten nicht, die Strecke ist gesperrt), andere Namen kosten das Fünffache, Fuß-, Rad-
# und Wirtschaftswege das 1,3- bis 1,6-Fache. Der Plan ist verzerrt (eingepasst bis 200 m daneben, im Polder an der Amstel
# 300 m), deshalb führt er nur im Vondelpark direkt (dort ohne Straßennamen; Kosten Länge × (1 + (Abstand zur Linie des Plans /
# 12 m)²), Abschnitte von 150 m).
# Amstel (km 13,7–25,8): hin am Westufer (Amsteldijk, Amsteldijk Noord) bis Ouderkerk aan de Amstel, dort am Fuß des Damms der
# Oranjebaan weiter (Amsteldijk Noord, im Plan liegt der Hinweg nördlich) bis zur Wende am Westende der Oranjebaan, zurück auf
# dem Damm der Oranjebaan (das Höhenbild des Veranstalters zeigt genau diese Senke: gut 200 m auf −1,5 m, dann hinauf zur Brücke),
# über die Brücke der Burgemeester Stramanweg und zurück am Ostufer (Hoger Einde-Noord, Binnenweg, Ouderkerkerdijk,
# Jan Vroegopsingel). Die Wende liegt im Plan etwa 58 pt (≈ 230 m) hinter der Brücke; genommen ist das Westende der
# zweibahnigen Oranjebaan 260 m hinter der Brücke, wo Damm und Weg am Fuß zusammenkommen.
# Stadion: Start auf der Westgeraden gut 25 m nach ihrem Nordende laut Startplan des Veranstalters, auf der Bahn (innerer Rand
# der Laufbahn aus OSM, Relation 1717342, 399,5 m) durch die Südkurve und die Ostgerade hinauf bis zur Mitte, dort durch das
# Marathontor nach Osten. Ziel am selben Strich, über dieselbe Kurve in Gegenrichtung (im Plan liegen Start und Ziel
# nebeneinander).
# -> gpx2026.json (Punkte und laufende Länge, geodätisch), linie_wege.json (OSM-Weg je Linienstück oder "stadion")
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, heapq, math
import xml.etree.ElementTree as ET
import numpy as np
from pyproj import Transformer, Geod
from scipy.spatial import cKDTree
from plan import nach_rd
T = Transformer.from_crs(4326, 28992, always_xy=True); TI = Transformer.from_crs(28992, 4326, always_xy=True)
GEOD = Geod(ellps="GRS80")
# ---------- Führung: rote Linie in Laufrichtung (Start im Stadion -> km 10, km 10 -> Utrechtse brug, Utrechtse brug -> Ziel)
Z = [np.array(z) for z in json.load(open("../dl/pdf_linie.json"))["rot"]]
def finde(a, b):
    for z in Z:
        if np.hypot(*(z[0] - a)) < 3 and np.hypot(*(z[-1] - b)) < 3: return z
        if np.hypot(*(z[-1] - a)) < 3 and np.hypot(*(z[0] - b)) < 3: return z[::-1]
    raise SystemExit(f"Stück {a} -> {b} fehlt")
stuecke = [finde((123, 1006), (596, 923)), finde((580, 927), (1075, 1193)), finde((1075, 1193), (135, 1003))]
fuehr = stuecke[0]
for z in stuecke[1:]:
    j = int(np.argmin(np.hypot(*(z - fuehr[-1]).T))); fuehr = np.vstack([fuehr, z[j + 1:]])
G = nach_rd(fuehr); G = G[np.r_[True, np.hypot(*np.diff(G, axis=0).T) > 0.01]]
gs = np.r_[0, np.cumsum(np.hypot(*np.diff(G, axis=0).T))]
dicht = np.arange(0, gs[-1], 2.0); GD = np.c_[np.interp(dicht, gs, G[:, 0]), np.interp(dicht, gs, G[:, 1])]
def punkt(s): return np.array([np.interp(s, gs, G[:, 0]), np.interp(s, gs, G[:, 1])])
def naechst(p, s0, s1):
    sel = np.where((dicht >= s0) & (dicht <= s1))[0]; j = sel[np.argmin(np.hypot(*(GD[sel] - p).T))]; return float(dicht[j])
print(f"Führung {gs[-1]:.0f} m (Plan, eingepasst)")
# ---------- Netz
net = json.load(open("../dl/osm_netz.json")); K = net["knoten"]
AUS = {"motorway", "motorway_link", "steps", "construction", "proposed", "platform", "elevator", "bus_stop", "raceway", "corridor"}
KLASSE = {"footway": 1.6, "path": 1.6, "service": 1.6, "track": 1.6, "cycleway": 1.3, "bridleway": 2.0}
pos, kanten, wegname, wegklasse = {}, {}, {}, {}
nid = [10 ** 12]
def neu_knoten(xy):
    nid[0] += 1; pos[nid[0]] = xy; return nid[0]
for wid, w in net["wege"].items():
    tg = w["tags"]
    if "highway" not in tg or tg.get("highway") in AUS or tg.get("area") == "yes": continue
    nds = [k for k in w["nd"] if str(k) in K]
    if len(nds) < 2: continue
    xy = np.array([T.transform(K[str(k)][1], K[str(k)][0]) for k in nds])
    wegname[wid] = tg.get("name", ""); wegklasse[wid] = tg.get("highway"); kf = KLASSE.get(tg.get("highway"), 1.0)
    for k, p_ in zip(nds, xy): pos.setdefault(k, p_)
    for a, b in zip(nds[:-1], nds[1:]):
        pa, pb = pos[a], pos[b]; L = float(np.hypot(*(pb - pa)))
        if L == 0: continue
        n = max(1, int(math.ceil(L / 10)))
        kette = [a] + [neu_knoten(pa + (pb - pa) * f) for f in np.linspace(0, 1, n + 1)[1:-1]] + [b]
        for u, v in zip(kette[:-1], kette[1:]):
            l = float(np.hypot(*(pos[v] - pos[u]))); kanten.setdefault(u, []).append((v, l, wid, kf)); kanten.setdefault(v, []).append((u, l, wid, kf))
ids = np.array(list(pos)); P = np.array([pos[i] for i in ids]); baumN = cKDTree(P)
print(len(ids), "Knoten im Netz")
def knoten_bei(p): return int(ids[baumN.query(p)[1]])
def dijkstra(start, ziele, kosten, lim=1e12):
    """kürzester Weg von start zu einem der Ziele (dict Knoten -> Zuschlag); kosten(u, v, l, wid, kf) -> Kosten oder None"""
    dist = {start: 0.0}; vor = {}; hq = [(0.0, start)]; fertig = set()
    while hq:
        c, u = heapq.heappop(hq)
        if u in fertig: continue
        fertig.add(u)
        if c > lim: break
        for v, l, wid, kf in kanten.get(u, []):
            k = kosten(u, v, l, wid, kf)
            if k is None: continue
            if c + k < dist.get(v, 1e18): dist[v] = c + k; vor[v] = (u, wid); heapq.heappush(hq, (c + k, v))
    cand = [(dist[z] + zs, z) for z, zs in ziele.items() if z in dist]
    if not cand: return None
    z = min(cand)[1]; weg = []
    while z != start: u, wid = vor[z]; weg.append((z, wid)); z = u
    return weg[::-1]
SIG = 12.0
def nach_fuehrung(start, s_von, s_bis):
    """Knotenweg entlang der Führung von s_von bis s_bis (Führungsmeter)"""
    richt = np.arctan2(*np.diff(GD, axis=0).T[::-1]); wende = []
    for i in range(5, len(GD) - 6):
        if not s_von < dicht[i] < s_bis: continue
        d = abs((richt[i + 5] - richt[i - 5] + np.pi) % (2 * np.pi) - np.pi)
        if d > np.radians(150) and (not wende or dicht[i] - wende[-1] > 60): wende.append(float(dicht[i]))
    wp = sorted(set(np.r_[np.arange(s_von, s_bis, 150.0), wende, s_bis].round(1)))
    wp = [w for n, w in enumerate(wp) if n == 0 or w - wp[n - 1] > 30 or w in wende or w == wp[-1]]
    weg, akt = [], start
    for n in range(1, len(wp)):
        s0, s1 = wp[n - 1], wp[n]
        sel = (dicht >= s0 - 60) & (dicht <= s1 + 60); bT = cKDTree(GD[sel])
        for korr in (150, 400):
            def kosten(u, v, l, wid, kf):
                dv = bT.query(pos[v])[0]
                if dv > korr: return None
                d = max(bT.query(pos[u])[0], dv); return l * kf * (1 + (d / SIG) ** 2)
            ziel = punkt(s1); zk = {int(ids[j]): 3 * float(np.hypot(*(P[j] - ziel))) for j in baumN.query_ball_point(ziel, korr / 3)}
            if not zk: zk = {knoten_bei(ziel): 0.0}
            teil = dijkstra(akt, zk, kosten)
            if teil is not None: break
            print(f"  Führungsmeter {s0:.0f}–{s1:.0f}: kein Weg im 150-m-Streifen, 400 m")
        if teil is None: raise SystemExit(f"kein Weg bei Führungsmeter {s0:.0f}–{s1:.0f}")
        weg += teil; akt = teil[-1][0] if teil else akt
    # Stiche entfernen: Wegpunkte abseits der Straße führen sonst hin und gleich wieder zurück (a, b, a -> a)
    kn = [start] + [z for z, _ in weg]; ws = [None] + [w for _, w in weg]
    i = 1
    while i < len(kn) - 1:
        if kn[i - 1] == kn[i + 1]: del kn[i:i + 2]; del ws[i:i + 2]; i = max(1, i - 1)
        else: i += 1
    return list(zip(kn[1:], ws[1:]))
def nach_namen(start, ziel, namen, klassen=None):
    # Ziel: nächster Knoten an einem Weg mit erlaubtem Namen (und Klasse) bis 40 m, sonst der nächste überhaupt
    ok = lambda wid: wegname.get(wid) in namen and (klassen is None or wegklasse.get(wid) in klassen)
    zk = {}
    for j in baumN.query_ball_point(ziel, 40):
        k = int(ids[j])
        if any(ok(wid) for _, _, wid, _ in kanten.get(k, [])): zk[k] = 3 * float(np.hypot(*(P[j] - ziel)))
    if not zk: zk = {knoten_bei(ziel): 0.0}
    def kosten(u, v, l, wid, kf): return l * kf * (1 if ok(wid) else 5)
    return dijkstra(start, zk, kosten)
# ---------- Stadion: innerer Rand der Laufbahn
r = ET.parse("../dl/osmapi/map_13085_808.xml").getroot()
nodes = {n.get("id"): (float(n.get("lat")), float(n.get("lon"))) for n in r.iter("node")}
ring = [x.get("ref") for w in r.iter("way") if w.get("id") == "126786235" for x in w.iter("nd")]
ll = np.array([nodes[k] for k in ring]); BAHN = np.c_[T.transform(ll[:, 1], ll[:, 0])]
if BAHN[0].tolist() == BAHN[-1].tolist(): BAHN = BAHN[:-1]
# gerade Stücke: lange Kanten des Rings; Westgerade = gerades Stück mit kleinerem x
n = len(BAHN); seg = np.roll(BAHN, -1, axis=0) - BAHN
lang = np.hypot(*seg.T)
gerade = [i for i in range(n) if lang[i] > 20]
west = min(gerade, key=lambda i: (BAHN[i] + BAHN[(i + 1) % n])[0]); ost = max(gerade, key=lambda i: (BAHN[i] + BAHN[(i + 1) % n])[0])
# Richtung auf der Westgeraden nach Süden?
w_a, w_b = BAHN[west], BAHN[(west + 1) % n]
sued = +1 if w_b[1] < w_a[1] else -1          # +1: Ringrichtung läuft auf der Westgeraden nach Süden
L_w = lang[west]; t_start = (25.0 / L_w) if sued > 0 else 1 - 25.0 / L_w   # 25 m nach dem Nordende
start_pkt = w_a + t_start * seg[west]
def ring_weg(i0, t0, i1, t1, r_):
    """Weg auf dem Ring in Richtung r_ (+1 = Indexrichtung), als Punktliste"""
    pts = [BAHN[i0] + t0 * seg[i0]]
    if r_ > 0:
        i = (i0 + 1) % n
        while True:
            pts.append(BAHN[i])
            if i == i1: break
            i = (i + 1) % n
    else:
        i = i0
        while True:
            pts.append(BAHN[i])
            if i == (i1 + 1) % n: break
            i = (i - 1) % n
    pts.append(BAHN[i1] + t1 * seg[i1]); return np.array(pts)
# Start: Westgerade nach Süden, Südkurve, Ostgerade nach Norden bis zur Mitte
stadion_aus = ring_weg(west, t_start, ost, 0.5, sued)
mitte = BAHN[ost] + 0.5 * seg[ost]
tor = mitte + np.array([40.0, 0.0])            # Marathontor in der Ostseite, gut 40 m östlich der Bahn
stadion_aus = np.vstack([stadion_aus, tor])
L_aus = np.hypot(*np.diff(stadion_aus, axis=0).T).sum()
print(f"Stadion: Start {start_pkt.round(1)}, Bahn bis Tor {L_aus:.0f} m")
# ---------- Abschnitte
BRUECKE_W = np.array([121671.0, 479066.0])
def baue(wende_m):
    teile = []   # Liste (Punkte, Wegkennung je Stück)
    def knotenweg(start, weg):
        pts = [pos[start]] + [pos[z] for z, _ in weg]; return np.array(pts), [w for _, w in weg]
    tor_k = knoten_bei(tor)
    teile.append((stadion_aus, ["stadion"] * (len(stadion_aus) - 1)))
    akt = tor_k
    def namen(ziel, nm, klassen=None):
        nonlocal akt
        w = nach_namen(akt, np.array(ziel, float), set(nm), klassen)
        if w is None: raise SystemExit(f"kein Weg nach {ziel}")
        if w: teile.append(knotenweg(akt, w)); akt = w[-1][0]
    def fuehrung(s_bis):
        nonlocal akt
        s_von = naechst(pos[akt], s_bis - 3500, s_bis)
        w = nach_fuehrung(akt, s_von, s_bis); teile.append(knotenweg(akt, w)); akt = w[-1][0]
    namen((118910, 484300), ["Stadionplein", "Amstelveenseweg"])
    namen((118905, 485385), ["Amstelveenseweg"])                              # Vondelpark, Eingang an der Amstelveenseweg
    park_a, n_park = akt, len(teile)
    fuehrung(naechst(np.array([120160.0, 485944.0]), 1500, 5000))             # durch den Vondelpark bis vor die Van Baerlestraat
    namen((120543, 486121), ["Vondelpark", "Zandpad"])                        # an der Stadhouderskade hinaus
    park_b, park = akt, [x for t_ in teile[n_park:] for x in zip(t_[0][1:], t_[1])]
    namen((120862, 485974), ["Stadhouderskade"])
    namen((120731, 485817), ["Museumstraat"])                                 # Passage unter dem Rijksmuseum
    namen((120883, 485769), ["Hobbemastraat"])
    namen((120838, 484795), ["Hobbemakade"])
    namen((120226, 484453), ["Stadionweg"])
    namen((120235, 483324), ["Beethovenstraat"])
    namen((119680, 483320), ["Gustav Mahlerlaan"])
    namen((119680, 483140), ["Parnassusweg"])
    namen((120330, 483143), ["De Boelelaan"])
    namen((120226, 484453), ["Beethovenstraat"])
    namen((120650, 484653), ["Stadionweg"])
    namen((121196, 484475), ["Apollolaan", "Muzenplein", "Churchill-laan"])
    namen((122161, 484363), ["Churchill-laan", "Vrijheidslaan", "Rijnstraat"])
    namen((122305, 483714), ["Rijnstraat"])
    namen((121912, 483706), ["President Kennedylaan"])
    namen((121905, 483470), ["De Mirandalaan"])
    namen((122210, 483310), ["Zuidelijke Wandelweg"])
    # Wende: Punkt auf der Oranjebaan im Abstand wende_m vom Westende der Brücke (entlang der Straße)
    ow = {wid for wid, ww in net["wege"].items() if ww["tags"].get("name") == "Oranjebaan" and ww["tags"].get("highway") == "secondary"}
    bk = knoten_bei(BRUECKE_W); dist = {bk: 0.0}; hq = [(0.0, bk)]
    while hq:
        c, u = heapq.heappop(hq)
        if c > dist.get(u, 1e18): continue
        for v, l, wid, kf in kanten.get(u, []):
            if wid in ow and c + l < dist.get(v, 1e18): dist[v] = c + l; heapq.heappush(hq, (c + l, v))
    tip = min(dist, key=lambda k: abs(dist[k] - wende_m))
    STRASSE = {"secondary", "tertiary", "unclassified", "residential"}
    namen(BRUECKE_W, ["Amsteldijk", "Amsteldijk Noord", "Oranjebaan"], STRASSE)  # Ouderkerk: Amsteldijk Noord am Fuß des Damms
    namen(pos[tip], ["Oranjebaan"], {"secondary"})                            # Wende am Westende der Oranjebaan
    namen((122437, 483426), ["Oranjebaan", "Burgemeester Stramanweg", "Hoger Einde-Noord", "Binnenweg", "Ouderkerkerdijk", "Jan Vroegopsingel"], STRASSE)
    namen((123135, 482027), ["Joan Muyskenweg"])
    namen((125072, 482708), ["Van der Madeweg"])
    namen((124937, 483007), ["Randweg"])
    namen((124069, 484043), ["Rozenburglaan"])
    namen((123800, 484495), ["Maxwellstraat"])
    namen((124339, 485011), ["Hugo de Vrieslaan", "Wethouder Frankeweg"])
    namen((124600, 485700), ["Galileïplantsoen", "Molukkenstraat"])
    namen((124499, 486306), ["Molukkenstraat"])
    namen((124042, 486567), ["Borneostraat"])
    namen((123640, 486547), ["Zeeburgerdijk"])
    namen((122215, 485808), ["Mauritskade"])
    namen((122085, 485760), ["Mauritskade", "Stadhouderskade"])               # Torontobrug (in OSM ohne Namen)
    w = dijkstra(akt, {park_b: 0.0}, lambda u, v, l, wid, kf: l * kf * (1 if wegname.get(wid) == "Stadhouderskade" else 5))
    teile.append(knotenweg(akt, w)); akt = park_b
    # durch den Vondelpark auf demselben Weg zurück (im Plan liegen Hin- und Rückweg nebeneinander)
    pp = [pos[park_b]] + [p_ for p_, _ in park[::-1]][1:] + [pos[park_a]]
    teile.append((np.array(pp), [w_ for _, w_ in park[::-1]])); akt = park_a
    namen((118910, 484300), ["Amstelveenseweg"])
    w = dijkstra(akt, {tor_k: 0.0}, lambda u, v, l, wid, kf: l * kf * (1 if wegname.get(wid) in ("Stadionplein", "Amstelveenseweg") else 5))
    teile.append(knotenweg(akt, w))
    rein = stadion_aus[::-1]; teile.append((rein, ["stadion"] * (len(rein) - 1)))
    xy = [teile[0][0][0]]; wege = []
    for pts, ws in teile:
        if np.hypot(*(pts[0] - xy[-1])) > 1: xy.append(pts[0]); wege.append("stadion")
        xy += list(pts[1:]); wege += ws
    # Stiche entfernen (a, b, a): ein Wegpunkt neben der Straße führt sonst hin und zurück
    i = 1; weg_m = 0.0
    while i < len(xy) - 1:
        if np.hypot(*(np.asarray(xy[i - 1]) - np.asarray(xy[i + 1]))) < 0.01:
            weg_m += 2 * float(np.hypot(*(np.asarray(xy[i]) - np.asarray(xy[i - 1])))); del xy[i:i + 2]; del wege[i - 1:i + 1]; i = max(1, i - 1)
        else: i += 1
    if weg_m: print(f"Stiche entfernt: {weg_m:.0f} m")
    xy = np.array(xy)
    keep = np.r_[True, np.hypot(*np.diff(xy, axis=0).T) > 0.05]
    wege = [w for w, k in zip(wege, keep[1:]) if k]; xy = xy[keep]
    return xy, wege, float(dist[tip]), pos[tip]
def laenge(xy):
    lo, la = TI.transform(xy[:, 0], xy[:, 1]); _, _, dd = GEOD.inv(lo[:-1], la[:-1], lo[1:], la[1:]); return np.r_[0, np.cumsum(dd)], la, lo
# Wende am Westende der zweibahnigen Oranjebaan, 260 m hinter der Brücke (im Plan etwa 58 pt ≈ 230 m; dort endet der Mittelstreifen)
xy, wege, wm, tip = baue(1e9)
d, la, lo = laenge(xy)
print(f"Wende {wm:.0f} m hinter der Brücke bei {np.round(tip)}; Linie {d[-1]:.0f} m geodätisch, {len(xy)} Punkte")
json.dump({"pts": [(float(a), float(b), 0.0) for a, b in zip(la, lo)], "d": d.tolist(), "wende": [float(tip[0]), float(tip[1])], "wende_m": wm},
          open("gpx2026.json", "w"))
json.dump(wege, open("linie_wege.json", "w"))
