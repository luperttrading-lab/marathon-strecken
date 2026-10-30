# Streckenlinie 2026 aus dem OSM-Netz (netz.py) nach dem Streckenplan des Veranstalters (plan.py, „6.5 Mapa Circuit (ZMB26)“).
# 1. Plan auf die Erde: affin über Kreuzungen benannter Straßen (Ecken der Planlinie <-> gemeinsame OSM-Knoten), dann ICP auf die
#    geroutete Linie. Der Plan ist maßstäblich auf einem echten Stadtplan gezeichnet (1,03 m/pt, um 44,5° gedreht).
# 2. Kürzeste Wege zwischen Wegmarken (Ecken der Strecke). Kosten zusätzlich nach dem Abstand d zum Planstück des Abschnitts:
#    bis FREI = 35 m nichts (der Plan ist auf ±15–30 m genau und zeichnet Hin- und Rückweg nebeneinander), darüber
#    1 + ((d − 35 m)/25 m)². So bleibt die Linie auf den Straßen des Plans, auch gegen Einbahnstraßen. Auf der Diagonal hält
#    der Name (AUF) den Weg auf der Straße, sonst wendete er über eine Querstraße.
# -> gpx2026.json {"pts": [[lat, lon, 0], …], "d": [Linienmeter]}, strassen.json (Weg und Name je 10 m aus den Kanten der Linie),
#    wegmarken.json (je Wegmarke Linienmeter und Stelle auf der Planlinie), georef.json (Plan -> UTM 31N)
import json, numpy as np
from pyproj import Geod, Transformer
from scipy.spatial import cKDTree
from netz import LL, XY, kreuzung, naechster, weg, kanten_weg, namen_knoten, WEGE, T, MITTE, basis, idx
TI = Transformer.from_crs(25831, 4326, always_xy=True)
PL = json.load(open("plan2026.json")); PLAN = np.array(PL["linie"])
def dicht(P, step):
    out = [P[0]]
    for a, b in zip(P[:-1], P[1:]):
        n = max(1, int(np.hypot(*(b - a)) / step)); out += [a + f * (b - a) for f in np.linspace(0, 1, n + 1)[1:]]
    return np.array(out)
GV, MA, AR, VA, ME, MO, DI = ("Gran Via de les Corts Catalanes", "Carrer de la Marina", "Carrer d'Aragó", "Carrer de València",
                              "Avinguda Meridiana", "Carrer de Mallorca", "Avinguda Diagonal")
# Passpunkte: Kreuzung (Namen wie in OSM) und Ecke der Planlinie in pt
PASS = [(GV, MA, 3611, 2414), (MA, AR, 3611, 2018), (AR, "Carrer de Viladomat", 772, 2017), ("Carrer de Viladomat", VA, 772, 1883),
        (MO, "Carrer de Calàbria", 658, 1756), ("Carrer de Calàbria", GV, 653, 2415), ("Carrer de Rocafort", "Carrer de Floridablanca", 512, 2689),
        ("Carrer de Floridablanca", "Carrer del Comte d'Urgell", 1028, 2686), ("Carrer del Comte d'Urgell", "Carrer de Manso", 1024, 2948),
        ("Carrer de Llull", "Carrer de la Llacuna", 4790, 3481), ("Carrer de la Llacuna", "Carrer de Pallars", 4785, 3228),
        ("Carrer de Pallars", "Carrer de Pamplona", 3990, 3230), ("Carrer dels Almogàvers", "Carrer de Roger de Flor", 3080, 3073),
        ("Carrer de Roger de Flor", "Carrer d'Ausiàs Marc", 3080, 2686), ("Carrer d'Ausiàs Marc", "Carrer del Bruc", 2548, 2690),
        ("Passeig de Gràcia", GV, 2157, 2414), (MO, ME, 4919, 1798)]
src, dst = [], []
for a, b, x, y in PASS:      # alle gemeinsamen Knoten gemittelt (zweibahnige Straßen: Mitte der Kreuzung)
    kk = sorted(namen_knoten(a) & namen_knoten(b))
    assert kk, (a, b)
    src.append((x, y)); dst.append(XY[kk].mean(0))
src, dst = np.array(src), np.array(dst)
A = np.linalg.lstsq(np.c_[src, np.ones(len(src))], dst, rcond=None)[0]
res = np.hypot(*(np.c_[src, np.ones(len(src))] @ A - dst).T)
print(f"Passpunkte: {len(src)}, Abstand nach affiner Einpassung Median {np.median(res):.1f} m, max {res.max():.1f} m")
def plan_utm(P, A): return np.c_[np.asarray(P), np.ones(len(P))] @ A
def ll(xy): lo, la = TI.transform(xy[0], xy[1]); return (la, lo)
PP = []                                                   # Planpunkte der Wegmarken in Reihenfolge
def P(x, y): PP.append((x, y)); return ll(plan_utm([(x, y)], A)[0])          # Planpunkt -> (lat, lon) für „nahe“
K = kreuzung
def marken():
    PP.clear()
    return [
        ("Start: Passeig de Gràcia zwischen Casp und Gran Via", naechster(*P(2157, 2538), name="Passeig de Gràcia")),
        ("Passeig de Gràcia / Gran Via", K("Passeig de Gràcia", GV, P(2157, 2414))),
        ("Gran Via / Marina", K(GV, MA, P(3611, 2414))),
        ("Marina / Aragó", K(MA, AR, P(3611, 2018))),
        ("Aragó / Viladomat", K(AR, "Carrer de Viladomat", P(772, 2017))),
        ("Viladomat / València", K("Carrer de Viladomat", VA, P(772, 1883))),
        ("València, Ostende (km 10)", naechster(*P(5542, 1933))),
        ("Felip II / Josep Estivill", naechster(*P(5542, 1539))),
        ("Josep Estivill / Gran de la Sagrera", naechster(*P(5660, 1538))),
        ("Gran de la Sagrera / Garcilaso", naechster(*P(5940, 1255))),
        ("Garcilaso / Meridiana", naechster(*P(5728, 995), name=ME)),
        ("Meridiana / Mallorca", K(ME, MO, P(4919, 1798))),
        ("Mallorca / Calàbria", K(MO, "Carrer de Calàbria", P(658, 1756))),
        ("Calàbria / Gran Via", K("Carrer de Calàbria", GV, P(653, 2415))),
        ("Gran Via / Rambla de Catalunya", K(GV, "Rambla de Catalunya", P(2016, 2416))),
        ("Rambla de Catalunya / Ronda de la Universitat", naechster(*P(2010, 2552))),
        ("Sepúlveda / Rocafort", K("Carrer de Sepúlveda", "Carrer de Rocafort", P(511, 2556))),
        ("Rocafort / Floridablanca", K("Carrer de Rocafort", "Carrer de Floridablanca", P(512, 2689))),
        ("Floridablanca / Comte d'Urgell", K("Carrer de Floridablanca", "Carrer del Comte d'Urgell", P(1028, 2686))),
        ("Comte d'Urgell / Manso", K("Carrer del Comte d'Urgell", "Carrer de Manso", P(1024, 2948))),
        ("Manso / Paral·lel", naechster(*P(500, 2960), name="Avinguda del Paral·lel")),
        ("Paral·lel, Drassanes", naechster(*P(1501, 4038))),
        ("Passeig de Colom", naechster(*P(2300, 3850), name="Passeig de Colom")),
        ("Marquès de l'Argentera / Picasso", naechster(*P(2870, 3700))),
        ("Picasso / Pujades", naechster(*P(2875, 3340))),
        ("Pujades / Marina", naechster(*P(3575, 3340))),
        ("Marina, Südende (Port Olímpic)", naechster(*P(3585, 4170))),
        ("Avinguda del Litoral", naechster(*P(5000, 4110), name="Avinguda del Litoral")),
        ("Litoral / Josep Pla", naechster(*P(6295, 4075))),
        ("Josep Pla / Taulat", naechster(*P(6290, 3770))),
        ("Taulat, Plaça de Llevant", naechster(*P(6680, 3730))),
        ("Diagonal, Ostende", naechster(*P(6650, 3660), name=DI)),
        # Wende: Der Plan zeichnet die Linie nur bis zur Carrer de la Llacuna, beschriftet die Wende aber mit „c/ de la Ciutat de
        # Granada“ (zwei Blöcke weiter). Parkverbote des Ajuntament (Presse, 14.03.2026): „Diagonal (calçada muntanya) … fins a Ciutat
        # de Granada“ und „Diagonal (calçada mar), des de Roc Boronat fins a Josep Pla“ -> Wende an der Ciutat de Granada (+540 m).
        ("Wende Diagonal / Ciutat de Granada", K(DI, "Carrer de la Ciutat de Granada", P(4765, 2680))),
        ("Diagonal / Llull", naechster(*P(6240, 3478))),
        ("Llull / Llacuna", K("Carrer de Llull", "Carrer de la Llacuna", P(4790, 3481))),
        ("Llacuna / Pallars", K("Carrer de la Llacuna", "Carrer de Pallars", P(4785, 3228))),
        ("Pallars / Pamplona", K("Carrer de Pallars", "Carrer de Pamplona", P(3990, 3230))),
        ("Pamplona / Salvador Espriu", naechster(*P(3985, 4140))),
        ("Salvador Espriu, Mitte", naechster(*P(3800, 4140), name="Carrer de Salvador Espriu")),
        ("Salvador Espriu / Marina", naechster(*P(3605, 4145))),
        ("Marina / Almogàvers", naechster(*P(3612, 3074))),
        ("Almogàvers / Roger de Flor", K("Carrer dels Almogàvers", "Carrer de Roger de Flor", P(3080, 3073))),
        ("Roger de Flor / Ausiàs Marc", K("Carrer de Roger de Flor", "Carrer d'Ausiàs Marc", P(3080, 2686))),
        ("Ausiàs Marc / Bruc", K("Carrer d'Ausiàs Marc", "Carrer del Bruc", P(2548, 2690))),
        ("Bruc / Ronda de Sant Pere", K("Carrer del Bruc", "Ronda de Sant Pere", P(2560, 2750))),
        ("Ronda de Sant Pere / Arc de Triomf", naechster(*P(2936, 2911))),
        ("Ziel: Passeig de Lluís Companys", naechster(*P(2946, 3002), name="Passeig de Lluís Companys")),
    ]
# Planlinie in Laufrichtung mit Bogenlänge (pt); jede Wegmarke bekommt ihre Stelle auf dem Plan (vorwärts gesucht, damit Hin- und
# Rückweg auf derselben Straße – Marina, Diagonal – nicht verwechselt werden)
FREI = 35.0
AUF = {"Wende Diagonal / Ciutat de Granada": DI, "Diagonal / Llull": DI}   # Abschnitt endet an dieser Marke: nur auf dieser Straße
PD = dicht(PLAN, 2.0); PS = np.r_[0, np.cumsum(np.hypot(*np.diff(PD, axis=0).T))]
def planstellen():
    out, s0 = [], 0.0
    for x, y in PP:
        m = (PS >= s0) & (PS <= s0 + 9000)
        j = np.where(m)[0][np.argmin(np.hypot(*(PD[m] - (x, y)).T))]; out.append(PS[j]); s0 = PS[j]
    return out
def route(A, MARKEN):
    """je Abschnitt zwischen zwei Wegmarken: Kosten nach dem Abstand zum Planstück dieses Abschnitts (±150 pt), damit eine Straße,
    die der Plan an anderer Stelle des Laufs nutzt (Gran Via vor der Plaça de la Universitat), den Weg nicht anzieht"""
    st = planstellen(); Q = plan_utm(PD, A); pfad = [MARKEN[0][1]]
    for i, ((na, a), (nb, b)) in enumerate(zip(MARKEN[:-1], MARKEN[1:])):
        m = (PS >= st[i] - 150) & (PS <= st[i + 1] + 150)
        dd, _ = cKDTree(Q[m]).query(MITTE); faktor = 1 + np.minimum(np.maximum(dd - FREI, 0) / 25.0, 7.0) ** 2
        p = weg(a, b, AUF.get(nb), faktor=faktor); pfad += p[1:]
    return pfad
MARKEN = marken(); pfad = route(A, MARKEN)
# ICP: Plan affin auf die geroutete Linie, dann neu routen
for durchgang in range(2):
    R = dicht(XY[pfad], 5.0); baum = cKDTree(R); Pp = dicht(PLAN, 5.0)
    for _ in range(30):
        Q = plan_utm(Pp, A); d, i = baum.query(Q); m = d < max(15.0, np.percentile(d, 90))
        A = np.linalg.lstsq(np.c_[Pp[m], np.ones(m.sum())], R[i[m]], rcond=None)[0]
    MARKEN = marken(); pfad = route(A, MARKEN)
R = dicht(XY[pfad], 5.0); Q = dicht(plan_utm(PLAN, A), 5.0)
d1, _ = cKDTree(R).query(Q); d2, _ = cKDTree(Q).query(R)
M2 = A[:2].T
print(f"Plan -> Linie: Median {np.median(d1):.1f} m, 95 % {np.percentile(d1, 95):.1f} m, max {d1.max():.0f} m; "
      f"Linie -> Plan: Median {np.median(d2):.1f} m, 95 % {np.percentile(d2, 95):.1f} m, max {d2.max():.0f} m; "
      f"Maßstab {np.sqrt(abs(np.linalg.det(M2))):.4f} m/pt, Drehung {np.degrees(np.arctan2(M2[1, 0], M2[0, 0])):.2f}°")
cumR = np.r_[0, np.cumsum(np.hypot(*np.diff(R, axis=0).T))]
weit = cumR[d2 > 40]
if len(weit): print("Linie mehr als 40 m neben dem Plan bei Linienmeter:", [int(x) for x in weit[::10]])
json.dump({"A": A.tolist()}, open("georef.json", "w"))
pts = [tuple(LL[i]) for i in pfad]
G = Geod(ellps="GRS80")
d = [0.0]
for (a1, b1), (a2, b2) in zip(pts[:-1], pts[1:]): d.append(d[-1] + G.inv(b1, a1, b2, a2)[2])
json.dump({"pts": [(float(a), float(b), 0.0) for a, b in pts], "d": d}, open("gpx2026.json", "w"))
kw = [kanten_weg(p, q) for p, q in zip(pfad[:-1], pfad[1:])] + [None]
strassen = []
for s in np.arange(0, d[-1], 10.0):
    i = min(len(kw) - 1, int(np.searchsorted(d, s, side="right")) - 1); w = kw[i] or kw[i - 1]
    t_ = WEGE[w][0]
    strassen.append([float(s), t_.get("name", ""), t_.get("bridge", ""), t_.get("tunnel", ""), t_.get("layer", ""), t_.get("highway", ""), w])
json.dump(strassen, open("strassen.json", "w"), ensure_ascii=False)
ml = {}; j = 0; st = planstellen()
for (nm, k), sp in zip(MARKEN, st):
    j = pfad.index(k, j); ml[nm] = [d[j], float(sp)]       # Linienmeter, Stelle auf der Planlinie (pt, PD/PS)
json.dump(ml, open("wegmarken.json", "w"), ensure_ascii=False, indent=0)
print(f"Linie {d[-1]:.0f} m, {len(pts)} Punkte")
for nm, (s, sp) in ml.items(): print(f"  {s / 1000:7.3f} km  Plan {sp:7.0f} pt  {nm}")
from itertools import groupby
s = 0
for n, g in groupby(zip([basis(WEGE[w][0].get("name", "")) if w else "–" for w in kw[:-1]],
                        [float(np.hypot(*(XY[p] - XY[q]))) for p, q in zip(pfad[:-1], pfad[1:])]), key=lambda x: x[0]):
    g = list(g); l = sum(x[1] for x in g)
    if l > 30: print(f"    {s / 1000:6.2f} {l:6.0f} m  {n}")
    s += l
