# Streckenkarte (PDF-Punkte) auf die Erde einpassen -> georef.json (affine Abbildung PDF -> UTM 50N und Restfehler).
# Die Karte liegt auf einem Satellitenbild unbekannter Herkunft; Straßen, Flüsse und Strecke sind darauf von Hand gezeichnet.
# Chinesische Kartendienste verschieben Koordinaten (GCJ-02, hier gut 500 m fast gleichförmig), OpenStreetMap nicht (WGS 84).
# Eingepasst wird deshalb nur gegen OSM: Eine affine Abbildung schluckt eine gleichförmige Verschiebung samt Maßstab und Drehung;
# die Änderung der GCJ-02-Verschiebung über die 10 km der Karte liegt unter 1 m.
# 1. Startwert: Ähnlichkeitsabbildung aus den Dorfnamen der Karte und den Ortspunkten in OSM (Namen stehen neben dem Dorf, grob).
# 2. ICP: gezeichnete Hauptstraßen und Straßen gegen OSM-Straßen, Flüsse gegen OSM-Flüsse (halbes Gewicht: das Flussbett ist breit);
#    affine Abbildung, Gewichte nach Huber, Fangradius von 400 m schrittweise auf 60 m. Das Mauerstück der Strecke zählt nicht mit:
#    Die Karte zeichnet die Strecke dort schematisch neben das Mauersymbol (mit Gewicht lagen die Straßen im Norden schlechter).
import json, math
import numpy as np
from scipy.spatial import cKDTree
from geo import utm, wgs, dicht, osm
P = json.load(open("plan2026.json"))
N, W, NT = osm()
# 1. Dorfnamen (chinesischer Name der Karte) -> OSM place
DORF = {"黄崖关": "黄崖关村", "小平安": "小平安村", "中营": "中营村", "下营": "下营村", "大平安": "大平安村", "段庄": "段庄村",
        "北车道峪": "北车道峪村", "董家坟": "董家坟", "白滩": "白滩村"}
src, dst = [], []
for s, bb, size in P["text"]:
    if s in DORF:
        k = [k for k, t in NT.items() if t.get("name") == DORF[s] and "place" in t][0]
        src.append(((bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2)); x, y = utm(*N[k]); dst.append((float(x), float(y)))
src, dst = np.array(src), np.array(dst)
def affin(a, b, w=None):
    A = np.c_[a, np.ones(len(a))]; w = np.ones(len(a)) if w is None else w
    M = np.linalg.lstsq(A * np.sqrt(w)[:, None], b * np.sqrt(w)[:, None], rcond=None)[0]; return M
def aehnlich(a, b):
    ca, cb = a.mean(0), b.mean(0); A = a - ca; B = b - cb
    # komplexe Rechnung: B = s·e^{iθ}·conj-frei; y der Karte zeigt nach unten -> spiegeln
    za = A[:, 0] - 1j * A[:, 1]; zb = B[:, 0] + 1j * B[:, 1]
    k = (np.conj(za) @ zb) / (np.conj(za) @ za)
    M = np.array([[k.real, k.imag], [k.imag, -k.real], [0, 0]], float)
    M[2] = cb - ca @ M[:2]; return M
def ab(M, p): p = np.asarray(p, float); return p @ M[:2] + M[2]
M = aehnlich(src, dst)
r0 = np.hypot(*(ab(M, src) - dst).T)
print("Startwert aus", len(src), "Dorfnamen: Maßstab", round(float(np.hypot(M[0, 0], M[0, 1])), 2), "m/pt, Abstand Name–Ortspunkt Median",
      round(float(np.median(r0))), "m")
# 2. Zielgeometrien aus OSM (verdichtet auf 5 m)
def osmlinien(filt):
    out = []
    for tg, refs in W.values():
        if filt(tg):
            ll = np.array([N[r] for r in refs if r in N])
            if len(ll) > 1: x, y = utm(ll[:, 0], ll[:, 1]); out.append(dicht(np.c_[x, y], 5))
    return np.vstack(out)
STR = osmlinien(lambda t: t.get("highway") in ("trunk", "primary", "secondary", "tertiary", "unclassified", "residential", "trunk_link",
                                               "secondary_link", "tertiary_link", "service", "living_street", "road"))
FLU = osmlinien(lambda t: t.get("waterway") in ("river", "stream"))
MAU = osmlinien(lambda t: t.get("historic") == "citywalls" or t.get("barrier") == "city_wall")
T = {"str": cKDTree(STR), "flu": cKDTree(FLU), "mau": cKDTree(MAU)}
G = {"str": STR, "flu": FLU, "mau": MAU}
# Quellpunkte der Karte (verdichtet auf 1 pt)
q = {"str": [], "flu": [], "mau": []}
for r in P["roads"]:
    if r["k"] in ("main", "tarmac"): q["str"].append(dicht(r["pts"], 1.0))
for r in P["rivers"]: q["flu"].append(dicht(r["pts"], 1.0))
# Mauerstück der Strecke: oberer Kasten der Karte (y < 70 pt), ohne den Platz im Westen (x > 240 pt)
m = np.array(P["marathon"]); sel = (m[:, 1] < 66) & (m[:, 0] > 238)
q["mau"].append(dicht(m[sel], 1.0)[::1])
Q = {k: np.vstack(v) for k, v in q.items()}
GEW = {"str": 1.0, "flu": 0.5, "mau": 0.0}   # Mauer nur zur Kontrolle
for fang in (400, 300, 200, 150, 100, 80, 60, 60, 60):
    for it in range(6):
        A, B, w = [], [], []
        for k in Q:
            X = ab(M, Q[k]); d, i = T[k].query(X)
            ok = d < fang
            A.append(Q[k][ok]); B.append(G[k][i[ok]]); ww = np.where(d[ok] < 25, 1.0, 25 / np.maximum(d[ok], 1e-9)); w.append(ww * GEW[k])
        A, B, w = np.vstack(A), np.vstack(B), np.concatenate(w)
        M = affin(A, B, w)
res = {}
for k in Q:
    d, _ = T[k].query(ab(M, Q[k])); res[k] = d
    if k == "str":
        for lo, hi, nm in ((0, 250, "Norden"), (250, 500, "Mitte"), (500, 900, "Süden")):
            sel = (Q[k][:, 1] >= lo) & (Q[k][:, 1] < hi)
            print(f"   Straßen {nm}: Median {np.median(d[sel]):.0f} m, 75 % {np.percentile(d[sel], 75):.0f} m")
    print(f"{k}: {len(d)} Kartenpunkte, Abstand zu OSM Median {np.median(d):.0f} m, 75 % {np.percentile(d, 75):.0f} m, 90 % {np.percentile(d, 90):.0f} m")
sx = math.hypot(M[0, 0], M[0, 1]); sy = math.hypot(M[1, 0], M[1, 1])
dreh = math.degrees(math.atan2(M[0, 1], M[0, 0])); scher = math.degrees(math.acos(abs(M[0] @ M[1]) / sx / sy * 0 + (M[0, :] @ M[1, :]) / (sx * sy))) if False else None
print(f"Maßstab x {sx:.3f} m/pt, y {sy:.3f} m/pt, Drehung {dreh:.2f}°; Winkel zwischen den Achsen {math.degrees(math.acos(abs(M[0] @ M[1]) / (sx * sy))):.2f}°")
json.dump({"M": M.tolist(), "rest": {k: {"median": float(np.median(v)), "p90": float(np.percentile(v, 90))} for k, v in res.items()},
           "dorf": r0.tolist()}, open("georef.json", "w"))
