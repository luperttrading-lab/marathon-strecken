# Korrekturen des Nutzers an der MapPlanner-Linie (02.11.2026) -> linie.json. Eingabe linie_roh.json (parse.py), korrektur.json.
# Der Nutzer hat auf Luftbildern (DOP20 Hessen, 10–12,5 cm je Bildpunkt) markiert: den echten Start 20 m nach dem Linienanfang
# und vier Kurven, die er abkürzt (km 0,67 und 2,29 Kehren; km 1,00 und 1,19 Anschluss an den Weg unter dem Gießener Ring, wo die
# Runde hin und zurück läuft). Dazu zwei Haken von je gut 2 m (km 3,34 und 3,64), wo MapPlanner auf dem Hin- und Rückweg über
# die Abzweigung hinaus und zurück gezeichnet hat. Ersetzen in UTM 32N: Strichenden auf die Linie setzen, Punkte neben den Enden
# streichen, solange dort ein Knick über 45° bleibt (sonst Zacken). Ergebnis 9 845 m statt 9 911 m (die Uhr des Nutzers: 9,85 km).
import json, math
import numpy as np
from pyproj import Transformer, Geod
t = Transformer.from_crs(4326, 25832, always_xy=True); ti = Transformer.from_crs(25832, 4326, always_xy=True)
R = json.load(open("linie_roh.json")); K = json.load(open("korrektur.json"))
V = [t.transform(lo, la) for la, lo in R["pts"]]
def cum(P):
    d = [0.0]
    for i in range(1, len(P)): d.append(d[-1] + math.dist(P[i - 1], P[i]))
    return d
def at(P, d, s):
    s = min(max(s, 0), d[-1])
    for i in range(1, len(d)):
        if d[i] >= s:
            f = (s - d[i - 1]) / ((d[i] - d[i - 1]) or 1)
            return (P[i - 1][0] + f * (P[i][0] - P[i - 1][0]), P[i - 1][1] + f * (P[i][1] - P[i - 1][1]))
    return P[-1]
def proj(P, d, q, s0, s1):
    return min((math.dist(q, at(P, d, s)), s) for s in np.arange(s0, s1, 0.2))[1]
def w(a, b, c):
    a1 = math.atan2(b[1] - a[1], b[0] - a[0]); a2 = math.atan2(c[1] - b[1], c[0] - b[0])
    return math.degrees(abs((a2 - a1 + math.pi) % (2 * math.pi) - math.pi))
neu = list(V); dn = cum(neu); L0 = dn[-1]
for kurve in sorted(K["kurven"], key=lambda k: -k["bei_m"]):          # von hinten, damit die Meter davor gelten
    s0 = kurve["bei_m"]; kv = [t.transform(lo, la) for la, lo in kurve["pkt"]]
    sA = proj(neu, dn, kv[0], s0 - 60, s0 + 60); sB = proj(neu, dn, kv[-1], s0 - 60, s0 + 60)
    if sA > sB: kv = kv[::-1]; sA, sB = sB, sA
    alt = sB - sA
    kv = [at(neu, dn, sA)] + kv[1:-1] + [at(neu, dn, sB)]
    vor = [q for q, s in zip(neu, dn) if s < sA - 0.05]; nach = [q for q, s in zip(neu, dn) if s > sB + 0.05]
    while len(kv) > 3 and (w(vor[-1], kv[0], kv[1]) > 45 or w(kv[0], kv[1], kv[2]) > 45): kv.pop(1)
    while len(kv) > 3 and (w(kv[-2], kv[-1], nach[0]) > 45 or w(kv[-3], kv[-2], kv[-1]) > 45): kv.pop(-2)
    neu = vor + kv + nach; d2 = cum(neu)
    print(f"Kurve bei {s0} m: {alt:.1f} m Linie durch {alt - (dn[-1] - d2[-1]):.1f} m ersetzt, {dn[-1] - d2[-1]:.1f} m kürzer")
    dn = d2
for h in K["haken"]:
    sp = t.transform(h["spitze"][1], h["spitze"][0])
    i = min(range(1, len(neu) - 1), key=lambda j: math.dist(neu[j], sp))
    vorher = dn[-1]; neu.pop(i); dn = cum(neu)
    print(f"Haken bei {h['bei_m']} m entfernt ({vorher - dn[-1]:.1f} m)")
S = at(neu, dn, K["start_m"]); neu = [S] + [q for q, s in zip(neu, dn) if s > K["start_m"]]
pts = [[round(la, 7), round(lo, 7)] for lo, la in (ti.transform(*q) for q in neu)]
G = Geod(ellps="WGS84")
_, _, dd = G.inv([p[1] for p in pts[:-1]], [p[0] for p in pts[:-1]], [p[1] for p in pts[1:]], [p[0] for p in pts[1:]])
d = np.r_[0, np.cumsum(dd)]
print(f"Linie {R['d'][-1]:.1f} m -> {d[-1]:.1f} m geodätisch ({len(pts)} Punkte); Start {pts[0]}")
json.dump({"pts": pts, "d": d.tolist()}, open("linie.json", "w"))
