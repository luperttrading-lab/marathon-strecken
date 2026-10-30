# Linie der Strecke: eingepasste Karte (georef.json) + OSM -> linie.json (UTM 50N und WGS 84, Art und OSM-Weg je Punkt).
#
# Aufbau der Strecke 2026 (Karte, Ausschnitte, Runners Guide; Ausschnitt Start/Ziel-Platz und Mauer):
#   Start auf dem Yin-&-Yang-Platz (Festung Huangyaguan) -> Straße nach Süden, über Huayuan und Xiaoping'an hinauf zum Wall point 1
#   (Treppe hinauf zur Mauer, km 5) -> auf der Mauer nach Westen über Tower 1, Beacon Tower, Tower 2–4, hinab zum Wall point 2,
#   weiter auf der Mauer, „Goat Track“ hinab zu Tower 5 -> über die Mauerbrücke (Wasserpass über den Ju He) zu Tower 6 -> einmal
#   auf der Festungsmauer rund um den Platz (Tower 7, Tempel 3 und 4) -> über den Platz zur Straße -> Tal hinab nach Süden, Schleife
#   über Zhongying, Xiaying, Dongjiafen, Baitan, Beichedaoyu, Da Ping'an und Duanzhuang -> Tal hinauf zum Platz (km 35, Tor zur
#   Mauer, Cut-off) -> Mauer im Gegenlauf (Tower 6, Mauerbrücke, Goat Track hinauf, … Wall point 1) -> Straße wie am Anfang zurück
#   (Xiaoping'an, Huayuan) -> Ziel auf dem Platz. Das zeigt auch die Höhenkurve des Veranstalters: km 0–5,1 und 37,1–42,2 sind
#   spiegelgleich, die Getränkestellen 1–7 liegen auf dem Rückweg in umgekehrter Folge an denselben Orten.
# Deshalb wird jedes Stück nur einmal gebaut und für den Rückweg umgedreht:
#   R1   Platz (Straße am Ostausgang) -> Fuß der Treppe am Wall point 1          (Korridor-Suche entlang der Karte, s. u.)
#   MAU  Fuß der Treppe -> Tower 5, nur OSM-Mauer und -Treppen (historic=citywalls, highway=steps)
#   BR   Tower 5 -> Mauerbrücke -> Tower 6 (OSM 222071714, 90229118, 90229187)
#   RING Festungsmauer 90229198 von Tower 6 rundum bis zur Nordwestecke, Nordmauer bis zum Tor (Tempel 1)
#   TAL  Ostausgang -> ganze Schleife im Süden -> zurück zum Ostausgang       (Korridor-Suche)
#   Platz: Wege über den Platz nach dem Ausschnitt der Karte (affin aus den Festungsecken, Restfehler bis 12 m).
# Korridor-Suche: Die gezeichnete Linie wird alle 10 m abgetastet und in Abschnitte von 200 m geteilt; je Abschnitt ein kürzester
# Weg (Dijkstra) im Netz aus OSM-Wegen (Kosten Länge · (1 + (d/45 m)²), d = Abstand zur gezeichneten Linie des Abschnitts), der
# gezeichneten Linie selbst (Länge · 2,5; die Karte schneidet Haarnadelkurven der Bergstraßen ab) und Verbindungen dazwischen bis
# 30 m (Länge · 2 + 150 m: teuer, sonst springt der Weg an der engsten Stelle über eine Haarnadelkurve). Abschnittsgrenzen liegen auf einem
# OSM-Weg, wenn einer in gleicher Richtung (±35°) höchstens 35 m entfernt ist. Wo OSM keinen Weg kennt, bleibt die gezeichnete
# Linie; Hin- und Rückweg auf derselben Straße fallen zusammen. Wo Hin- und Rückweg ohne OSM-Weg nebeneinander gezeichnet sind
# (Abzweig am Talausgang), wird vorher ihre Mitte als Weg eingefügt (EXTRA).
import json, math, heapq
import numpy as np
from scipy.spatial import cKDTree
from geo import utm, wgs, dicht, gleich, laenge, osm
P = json.load(open("plan2026.json")); M = np.array(json.load(open("georef.json"))["M"])
N, W, NT = osm()
def ab(p): return np.asarray(p, float) @ M[:2] + M[2]
plan_pt = np.array(P["marathon"]); plan_s_pt = laenge(plan_pt)
plan = ab(plan_pt); pp, ps = gleich(plan, 10.0); pspt = np.interp(ps, laenge(plan), plan_s_pt)
def pidx(s_pt): return int(np.argmin(np.abs(pspt - s_pt)))
# --- Netz
ERLAUBT = {"trunk", "primary", "secondary", "tertiary", "unclassified", "residential", "trunk_link", "primary_link", "secondary_link",
           "tertiary_link", "service", "living_street", "road", "track", "path", "footway", "steps", "pedestrian", "construction"}
def wegart(tg):
    if tg.get("historic") == "citywalls" or tg.get("barrier") in ("city_wall", "wall"): return "mauer"
    if tg.get("highway") in ERLAUBT: return tg["highway"]
    return None
XY, ADJ, EDGE = {}, {}, {}
def knoten(k, xy): XY[k] = np.asarray(xy, float); ADJ.setdefault(k, [])
def kante(a, b, info):
    L = float(np.hypot(*(XY[a] - XY[b]))); ADJ[a].append(b); ADJ[b].append(a); EDGE[(a, b)] = EDGE[(b, a)] = (L, info)
neu = [-1]
def neuer(xy): neu[0] -= 1; knoten(neu[0], xy); return neu[0]
def weg_einfuegen(refs, info):
    for a, b in zip(refs[:-1], refs[1:]):
        L = float(np.hypot(*(XY[a] - XY[b]))); n = max(1, int(math.ceil(L / 10))); prev = a
        for k in range(1, n): q = neuer(XY[a] + (XY[b] - XY[a]) * k / n); kante(prev, q, info); prev = q
        kante(prev, b, info)
for wid, (tg, refs) in W.items():
    art = wegart(tg)
    if not art: continue
    refs = [r for r in refs if r in N]
    for r in refs:
        if r not in XY: x, y = utm(*N[r]); knoten(r, (float(x), float(y)))
    weg_einfuegen(refs, ("osm", wid, art))
OSMK = list(XY)
def naechster(xy, filt=None):
    best = None
    for k in OSMK:
        if filt and not filt(k): continue
        d = float(np.hypot(*(XY[k] - xy)))
        if best is None or d < best[0]: best = (d, k)
    return best[1]
# EXTRA: Mitte zweier nebeneinander gezeichneter Linien ohne OSM-Weg, an beiden Enden an den nächsten OSM-Knoten gehängt
EXTRA = [((1262, 1302), (3452, 3496), "Abzweig am Talausgang (Hin- und Rückweg 30–50 m auseinander gezeichnet)")]
for (a0, a1), (b0, b1), _ in EXTRA:
    A = gleich(pp[pidx(a0):pidx(a1) + 1], 5)[0]; B = gleich(pp[pidx(b0):pidx(b1) + 1], 5)[0][::-1]
    n = max(len(A), len(B)); t = np.linspace(0, 1, n)
    def ab_t(X): s = laenge(X) / laenge(X)[-1]; return np.c_[np.interp(t, s, X[:, 0]), np.interp(t, s, X[:, 1])]
    mid = (ab_t(A) + ab_t(B)) / 2
    k0 = naechster(mid[0]); k1 = naechster(mid[-1])
    ks = [k0] + [neuer(q) for q in mid[1:-1]] + [k1]
    weg_einfuegen(ks, ("osm", None, "weg"))
ON = [k for k in XY]; OTREE = cKDTree(np.array([XY[k] for k in ON]))
PN = [f"p{i}" for i in range(len(pp))]
for i, k in enumerate(PN): knoten(k, pp[i])
for i in range(len(pp) - 1): kante(PN[i], PN[i + 1], ("plan", None, "plan"))
def richtung(i):
    a, b = pp[max(0, i - 2)], pp[min(len(pp) - 1, i + 2)]; v = b - a; return v / max(np.hypot(*v), 1e-9)
def fang(i):
    v = richtung(i); best = None
    for j in OTREE.query_ball_point(pp[i], 35):
        k = ON[j]; d = float(np.hypot(*(XY[k] - pp[i])))
        for nb in ADJ[k]:
            if isinstance(nb, str): continue
            e = XY[nb] - XY[k]; e = e / max(np.hypot(*e), 1e-9)
            if abs(e @ v) > math.cos(math.radians(35)):
                if best is None or d < best[0]: best = (d, k)
                break
    return best[1] if best else PN[i]
def dijkstra(s, t, nachbarn):
    dist = {s: 0.0}; prev = {}; h = [(0.0, 0, s)]; cnt = 0
    while h:
        d, _, a = heapq.heappop(h)
        if a == t: break
        if d > dist.get(a, 1e18): continue
        for b, c, info in nachbarn(a):
            nd = d + c
            if nd < dist.get(b, 1e18): dist[b] = nd; prev[b] = (a, info); cnt += 1; heapq.heappush(h, (nd, cnt, b))
    if t != s and t not in prev: raise SystemExit(f"kein Weg {s} -> {t}")
    path = [t]; infos = []
    while path[-1] != s: a, info = prev[path[-1]]; infos.append(info); path.append(a)
    return path[::-1], infos[::-1]
D0, KP = 45.0, 2.5
def korridor(i0, i1, s, t):
    grenzen = list(range(i0, i1, 20)) + [i1]
    wp = [s] + [fang(i) for i in grenzen[1:-1]] + [t]
    nodes, infos = [s], []
    for j in range(len(wp) - 1):
        lo, hi = max(0, grenzen[j] - 5), min(len(pp), grenzen[j + 1] + 6)
        seg = pp[lo:hi]; tree = cKDTree(dicht(seg, 2.0))
        erlaubt = set(PN[lo:hi]) | {wp[j], wp[j + 1]}
        for lst in OTREE.query_ball_point(seg, 120):
            for j2 in lst: erlaubt.add(ON[j2])
        extra = {}
        for k in PN[lo:hi]:
            for j2 in OTREE.query_ball_point(XY[k], 30):
                o = ON[j2]; c = 2 * float(np.hypot(*(XY[k] - XY[o]))) + 150
                extra.setdefault(k, []).append((o, c, ("verb", None, "verb"))); extra.setdefault(o, []).append((k, c, ("verb", None, "verb")))
        def nachbarn(a):
            for b in ADJ[a]:
                if b not in erlaubt: continue
                L, info = EDGE[(a, b)]
                if info[0] == "plan": yield b, L * KP, info
                else: yield b, L * (1 + (tree.query((XY[a] + XY[b]) / 2)[0] / D0) ** 2), info
            for b, c, info in extra.get(a, []): yield b, c, info
        pth, inf = dijkstra(wp[j], wp[j + 1], nachbarn); nodes += pth[1:]; infos += inf
    return nodes, infos
def nur(arten):
    def nachbarn(a):
        for b in ADJ[a]:
            L, info = EDGE[(a, b)]
            if info[0] == "osm" and info[2] in arten: yield b, L, info
    return nachbarn
def entlang(wid, i_von, i_bis):
    """Knoten eines OSM-Wegs (einschließlich der eingefügten Zwischenknoten) von Index i_von bis i_bis."""
    refs = W[wid][1]; seq = refs[i_von:i_bis + 1] if i_bis >= i_von else refs[i_bis:i_von + 1][::-1]
    nodes, infos = [seq[0]], []
    for a, b in zip(seq[:-1], seq[1:]):
        pth, inf = dijkstra(a, b, lambda x: ((y, EDGE[(x, y)][0], EDGE[(x, y)][1]) for y in ADJ[x] if EDGE[(x, y)][1][1] == wid))
        nodes += pth[1:]; infos += inf
    return nodes, infos
# --- Platz: Ausschnitt der Karte (Rasterbild, 6-fach gerendert) affin auf die Festungsecken in OSM
#     NW-Ecke, Tower 6, Tower 7 (SO), SW-Ecke, Stufe an Tempel 3 (zwei Ecken)
SRC = np.array([(205, 415), (740, 215), (925, 1140), (125, 1440), (540, 1170), (540, 1390)], float)
DST = np.array([XY[r] for r in (1046095704, 8087204327, 8087204330, 1046093944, 1046094120, 1046093995)])
MA = np.linalg.lstsq(np.c_[SRC, np.ones(len(SRC))], DST, rcond=None)[0]
REST_PLATZ = np.hypot(*(np.c_[SRC, np.ones(len(SRC))] @ MA - DST).T)
def platz(px): return np.c_[np.asarray(px, float), np.ones(len(px))] @ MA
# Ostausgang: Punkt auf der Talstraße 克黄线 (G233) vor dem Platz, wo die Bahnen aus dem Platz auf die Straße treffen
G233 = {wid for wid, (tg, _) in W.items() if tg.get("name") == "克黄线"}
E = naechster(platz([(1000, 420)])[0], lambda k: any(EDGE[(k, b)][1][1] in G233 for b in ADJ[k]))
# Tor (Tempel 1, Marke 35 km, Cut-off) auf der Nordmauer zwischen NW-Ecke und Tower 6
jx = platz([(430, 345)])[0]; a_, b_ = XY[1046095704], XY[8087204327]
tt = float(np.clip((jx - a_) @ (b_ - a_) / ((b_ - a_) @ (b_ - a_)), 0, 1)); TOR = neuer(a_ + tt * (b_ - a_))
kante(1046095704, TOR, ("osm", 90229187, "mauer")); kante(TOR, 8087204327, ("osm", 90229187, "mauer"))
def poly(px_list, von, bis, art="platz"):
    """Weg über den Platz: Knoten von -> Punkte aus dem Ausschnitt -> bis."""
    ks = [von] + [neuer(q) for q in platz(px_list)] + [bis]
    return ks, [("platz", None, art)] * (len(ks) - 1)
START = neuer(platz([(640, 405)])[0]); ZIEL = neuer(platz([(560, 545)])[0])
# --- Planstellen der Übergänge (gezeichnete Linie, pt)
def bei(lo, hi, xy):
    sel = np.where((pspt > lo) & (pspt < hi))[0]; return int(sel[np.argmin(np.hypot(*(pp[sel] - xy).T))])
WP1 = 2310481691; T5 = 1046093729; T6 = 8087204327; NW = 1046095704
i_E1 = bei(0, 120, XY[E]); i_W1 = bei(400, 800, XY[WP1]); i_E2 = bei(860, 1000, XY[E]); i_E3 = bei(3780, 3900, XY[E])
print("Übergänge (pt):", round(pspt[i_E1]), round(pspt[i_W1]), round(pspt[i_E2]), round(pspt[i_E3]))
TEILE = []
def teil(name, nodes, infos): TEILE.append((name, nodes, infos))
teil("Start über den Platz", *poly([(760, 400), (1000, 405)], START, E))
R1 = korridor(i_E1, i_W1, E, WP1); teil("Straße zum Wall point 1", *R1)
MAU = dijkstra(WP1, T5, nur({"mauer", "steps"})); teil("Mauer, 1. Mal", *MAU)
BR = entlang(222071714, 0, 1); b2 = entlang(90229118, 0, 1); b3 = entlang(90229187, 0, 1)
BR = (BR[0] + b2[0][1:] + b3[0][1:], BR[1] + b2[1] + b3[1]); teil("Mauerbrücke", *BR)
RING = entlang(90229198, 0, 26); teil("Festungsmauer", *RING)
teil("Nordmauer zum Tor", [NW, TOR], [EDGE[(NW, TOR)][1]])
teil("Platz zur Straße", *poly([(450, 400), (560, 420), (760, 415), (1000, 415)], TOR, E))
TAL = korridor(i_E2, i_E3, E, E); teil("Tal und Dörfer", *TAL)
teil("Platz zum Tor", *poly([(1000, 440), (760, 440), (520, 440), (450, 400)], E, TOR))
teil("Nordmauer zu Tower 6", [TOR, T6], [EDGE[(TOR, T6)][1]])
teil("Mauerbrücke zurück", BR[0][::-1], BR[1][::-1])
teil("Mauer, 2. Mal", MAU[0][::-1], MAU[1][::-1])
teil("Straße zurück zum Platz", R1[0][::-1], R1[1][::-1])
teil("Ziel über den Platz", *poly([(1000, 470), (760, 465), (600, 470)], E, ZIEL))
nodes, infos, teilname = [TEILE[0][1][0]], [], []
for name, nd, inf in TEILE:
    assert nd[0] == nodes[-1], (name, nd[0], nodes[-1])
    nodes += nd[1:]; infos += inf; teilname += [name] * len(inf)
ch = True
while ch:                                   # Stichwege A -> B -> A an Abschnittsgrenzen entfernen
    ch = False
    for i in range(1, len(nodes) - 1):
        if nodes[i - 1] == nodes[i + 1] and teilname[i - 1] == teilname[i]:
            del nodes[i:i + 2]; del infos[i - 1:i + 1]; del teilname[i - 1:i + 1]; ch = True; break
X = np.array([XY[k] for k in nodes]); d = laenge(X)
lat, lon = wgs(X[:, 0], X[:, 1])
art = [infos[0][2]] + [inf[2] for inf in infos]; way = [infos[0][1]] + [inf[1] for inf in infos]; teil_ = [teilname[0]] + teilname
json.dump({"x": X[:, 0].round(2).tolist(), "y": X[:, 1].round(2).tolist(), "lat": lat.round(7).tolist(), "lon": lon.round(7).tolist(),
           "d": d.round(2).tolist(), "art": art, "way": way, "teil": teil_, "knoten": [k if isinstance(k, int) else None for k in nodes]},
          open("linie.json", "w"), ensure_ascii=False)
print(f"Linie {d[-1]:.0f} m aus {len(nodes)} Punkten (gezeichnete Linie {laenge(plan)[-1]:.0f} m); Platz-Ausschnitt Restfehler bis {REST_PLATZ.max():.0f} m")
anteil = {}
for a, b, k in zip(d[:-1], d[1:], art[1:]): anteil[k] = anteil.get(k, 0) + (b - a)
print("Anteile (m):", {k: round(v) for k, v in sorted(anteil.items(), key=lambda x: -x[1])})
pos = 0
for name, nd, inf in TEILE:
    L = sum(float(np.hypot(*(XY[a] - XY[b]))) for a, b in zip(nd[:-1], nd[1:]))
    print(f"  {name:28s} {pos / 1000:6.2f} – {(pos + L) / 1000:6.2f} km ({L:5.0f} m)"); pos += L
