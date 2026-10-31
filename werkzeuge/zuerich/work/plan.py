# Kilometertafeln aus dem Streckenplan 2026 des Veranstalters (../dl/pdf/Marathon_ZHM.pdf, Reygrafik, PDF vom 17.12.2025). Die Karte ist
# ein Bild, Strecke und Tafeln liegen als Vektoren darüber (pdftocairo -svg -> ../dl/pdf/p1.svg Übersicht, p2.svg Detailplan City).
# Je Seite wird die gezeichnete Strecke (rote und violette Linien) affin auf die GPX-Linie in LV95 eingepasst (ICP, Ausgangslage aus den
# Umrissen), dann die Mitte jeder Tafel auf die GPX-Linie projiziert (im Fenster um den erwarteten Linienmeter, weil die Strecke in der
# Stadt mehrfach dieselben Strassen nutzt). Die Tafel steht neben der Linie, nicht darauf: Genauigkeit Detailplan etwa ±40 m
# (1 pt = 7 m), Übersicht etwa ±150 m (1 pt = 30 m). Welche Zahl in welcher Tafel steht, ist von Hand aus dem Bild abgelesen
# (Glyphen sind Pfade). Rot = Zürich–Meilen, violett = Meilen–Zürich.
# Dazu die Verpflegungssymbole (gelber Becher) mit allen Durchgängen der Linie in ihrer Nähe.
# -> marken_plan.json {"km": [[km, Linienmeter, Abstand Tafel–Linie in m, Seite], …], "verpflegung": [[Seite, Lage pt, Abstand m, [Linienmeter je Durchgang]], …]}
import json, re, sys
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
T = Transformer.from_crs(4326, 2056, always_xy=True)
ROT = "rgb(92.939758%, 10.978699%, 14.118958%)"; VIO = "rgb(67.96875%, 6.340027%, 55.674744%)"; GELB = "rgb(100%, 94.898987%, 0%)"
# Tafelmitte (pt, gerundet) -> km, von Hand aus den Bildern ../dl/pdf/plan-1.png und plan-2.png (110 dpi = pt × 1,528)
TAFELN = {"p2": {(178, 156): 5, (397, 475): 2, (198, 257): 6, (302, 381): 1, (317, 342): 3, (232, 273): 4, (145, 339): 7, (193, 282): 8,
                 (281, 332): 9, (354, 477): 10, (160, 159): 40, (326, 396): 35, (162, 336): 37, (138, 373): 38, (166, 256): 39,
                 (213, 251): 41, (242, 256): 42},
          "p1": {(110, 163): 10, (65, 66): 5, (48, 74): 40, (101, 147): 35, (126, 153): 2, (193, 334): 15, (199, 303): 30, (302, 498): 20,
                 (298, 469): 25, (337, 522): 21}}
def pfade(f):
    s = open(f).read(); out = []
    for a in re.findall(r"<path ([^>]*)/>", s):
        d = re.search(r' d="([^"]+)"', a).group(1)
        nums = [float(t) for t in re.findall(r"-?[\d.]+(?:e-?\d+)?", d)]
        if len(nums) % 2: continue
        P = np.array(nums).reshape(-1, 2)
        m = re.search(r'transform="matrix\(([^)]+)\)"', a); m = [float(v) for v in m.group(1).split(",")] if m else [1, 0, 0, 1, 0, 0]
        Q = np.c_[P[:, 0] * m[0] + P[:, 1] * m[2] + m[4], P[:, 0] * m[1] + P[:, 1] * m[3] + m[5]]
        out.append((a, Q))
    return out
g = json.load(open("gpx2026.json")); P = np.array(g["pts"]); d = np.array(g["d"])
x, y = T.transform(P[:, 1], P[:, 0]); X = np.c_[x, y]
# GPX-Linie alle 2 m
dl = np.r_[0, np.cumsum(np.hypot(*np.diff(X, axis=0).T))]
ss = np.arange(0, dl[-1], 2.0); D = np.c_[np.interp(ss, dl, X[:, 0]), np.interp(ss, dl, X[:, 1])]; Dd = np.interp(ss, dl, d)
aus = []; stationen = []
for seite in ("p2", "p1"):
    el = pfade(f"../dl/pdf/{seite}.svg")
    linie = np.vstack([Q for a, Q in el if (f'stroke="{ROT}"' in a or f'stroke="{VIO}"' in a) and len(Q) > 20])
    linie = linie[linie[:, 0] > 60] if seite == "p2" else linie        # ohne Legende
    # Bereich der GPX, den die Seite zeigt: Detailplan nur die Stadt (nördlich 47,35)
    sel = np.ones(len(D), bool) if seite == "p1" else (np.interp(ss, dl, P[:, 0] * 0 + np.array([p[0] for p in g["pts"]])) > 47.349)
    Dz = D[sel]; baum = cKDTree(Dz)
    # Ausgangslage: Umrisse aufeinander (Norden oben, y nach unten)
    A = np.zeros((2, 3)); sx = (Dz[:, 0].max() - Dz[:, 0].min()) / (linie[:, 0].max() - linie[:, 0].min())
    sy = (Dz[:, 1].max() - Dz[:, 1].min()) / (linie[:, 1].max() - linie[:, 1].min())
    A[0] = [sx, 0, Dz[:, 0].min() - sx * linie[:, 0].min()]; A[1] = [0, -sy, Dz[:, 1].max() + sy * linie[:, 1].min()]
    for it in range(60):
        L = np.c_[linie, np.ones(len(linie))] @ A.T
        dist, j = baum.query(L)
        ok = dist < np.percentile(dist, 90) + 1
        M = np.c_[linie[ok], np.ones(ok.sum())]
        A = np.linalg.lstsq(M, Dz[j[ok]], rcond=None)[0].T
    L = np.c_[linie, np.ones(len(linie))] @ A.T; dist, _ = baum.query(L)
    mpt = np.sqrt(abs(np.linalg.det(A[:, :2])))
    print(f"{seite}: {len(linie)} Linienpunkte, 1 pt = {mpt:.1f} m, Drehung {np.degrees(np.arctan2(A[1, 0], A[0, 0])):+.2f}°, "
          f"Abstand Plan–GPX Median {np.median(dist):.1f} m, 90 % {np.percentile(dist, 90):.1f} m")
    fak = dl[-1] / 42195
    for a, Q in el:
        if f'fill="{ROT}"' not in a and f'fill="{VIO}"' not in a or len(Q) != 5: continue
        w, h = np.ptp(Q[:, 0]), np.ptp(Q[:, 1])
        if not (5 < w < 9 and 5 < h < 9): continue
        c = Q[:4].mean(0); key = (int(round(c[0])), int(round(c[1])))
        km = next((v for k, v in TAFELN[seite].items() if abs(k[0] - c[0]) <= 1.5 and abs(k[1] - c[1]) <= 1.5), None)
        if km is None: print("  Tafel ohne Zahl", key); continue
        q = np.r_[c, 1] @ A.T
        erw = km * 1000 * fak; fenster = (np.abs(Dd - erw) < 1800)
        di = np.hypot(*(D - q).T); di[~fenster] = 1e9; i = int(np.argmin(di))
        aus.append([km, round(float(Dd[i]), 1), round(float(di[i]), 1), seite])
    # Verpflegung (gelber Becher, daneben das rote Kreuz der Sanität): alle Durchgänge der Linie nahe beim Symbol. Stadt aus dem
    # Detailplan, am See aus der Übersicht; die Legende (x < 60 pt) und die kleinen Stadtsymbole der Übersicht (5,7 pt) nicht.
    for a, Q in el:
        if f'fill="{GELB}"' not in a or len(Q) != 5: continue
        c = (Q.min(0) + Q.max(0)) / 2
        if c[0] < 60 or (seite == "p1" and np.ptp(Q[:, 0]) < 8): continue
        q = np.r_[c, 1] @ A.T; di = np.hypot(*(D - q).T); dmin = di.min()
        nah = np.where(di < dmin + (80 if seite == "p2" else 250))[0]
        gruppen = np.split(nah, np.where(np.diff(nah) > 30)[0] + 1)     # 30 × 2 m Lücke = anderer Durchgang
        durch = [round(float(Dd[gr[np.argmin(di[gr])]]), 1) for gr in gruppen]
        stationen.append([seite, [round(float(v), 1) for v in c], round(float(dmin), 1), durch])
        print(f"  Verpflegung {seite} ({c[0]:.0f}, {c[1]:.0f}) pt: {dmin:.0f} m neben der Linie, Durchgänge bei Linienmeter " + ", ".join(f"{v:.0f}" for v in durch))
    if seite == "p2":   # Start- und Zielstrich (dünne Linien 0,57 pt vom Schild zur Strecke): Ende an der Strecke
        for a, Q in el:
            if 'stroke-width="0.5668"' not in a or len(Q) != 2: continue
            farbe = "Start" if f'stroke="{ROT}"' in a else ("Ziel" if f'stroke="{VIO}"' in a else None)
            if farbe is None or Q[:, 0].min() < 60: continue
            for e in Q:
                q = np.r_[e, 1] @ A.T; di = np.hypot(*(D - q).T)
                if farbe == "Start": di[Dd > 3000] = 1e9
                else: di[Dd < 40000] = 1e9
                i = int(np.argmin(di)); print(f"  {farbe}strich Ende ({e[0]:.1f}, {e[1]:.1f}) pt: Linienmeter {Dd[i]:.1f}, {di[i]:.1f} m neben der Linie")
                aus.append([0 if farbe == "Start" else 42.195, round(float(Dd[i]), 1), round(float(di[i]), 1), seite + farbe])
aus.sort()
json.dump({"km": aus, "verpflegung": stationen}, open("marken_plan.json", "w"))
GL = d[-1]; vor = None
print(f"Linie {GL:.0f} m, Faktor 42195/Linie = {42195 / GL:.5f}")
for km, s, e, seite in aus:
    print(f"  km {km:6.3f} {seite}: Linienmeter {s:8.1f}  (Tafel {e:4.0f} m neben der Linie)  Linie/km {s / max(km * 1000, 1):.4f}  Linie − km×Faktor {s - km * 1000 * GL / 42195:+6.0f} m"
          + (f"  Stück {s - vor[1]:6.0f} m je {1000 * (km - vor[0]):.0f}" if vor and km != vor[0] else ""))
    vor = (km, s)
