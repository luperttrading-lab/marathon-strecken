# Streckenplan 2025 (Rasterbild, plan.py) auf die Erde einpassen -> georef.json (affine Abbildung Pixel -> UTM 51N und Restfehler).
# Der Plan ist auf einer Stadtkarte unbekannter Herkunft gezeichnet; chinesische Kartendienste verschieben ihre Koordinaten (GCJ-02,
# in Shanghai gut 500 m nach Südosten, fast gleichförmig). Eingepasst wird deshalb nur gegen OSM (WGS 84): Eine affine Abbildung
# schluckt eine gleichförmige Verschiebung samt Maßstab und Drehung (Muster: werkzeuge/greatwall/work/georef.py).
# 1. Startwert aus vier Ecken der Strecke, deren Straßen der Plan beschriftet (Pixel von Hand abgelesen, OSM-Kreuzung der Namen).
# 2. ICP: alle blauen Pixel der Linie (ohne Kilometerkreise, Symbole und Legende) gegen die OSM-Straßen; affine Abbildung, Gewichte
#    nach Huber, Fangradius schrittweise von 250 m auf 40 m. Hin- und Rückweg zeichnet der Plan nebeneinander (gut 10 px = 40 m);
#    das gleicht sich im Mittel aus.
import json, math
import numpy as np
from scipy.spatial import cKDTree
from geo import utm, wgs, dicht, osm, kreuzung
P = json.load(open("plan2025.json")); BL = np.load("../dl/plan_blau.npy").astype(float)
N, W, _ = osm()
ECKEN = [((1187, 1619), "南京西路", "华山路"), ((1358, 2079), "常熟路", "淮海中路"), ((3119, 1320), "中山东二路", "新开河路"),
         ((1187, 3825), "龙华西路", "中山南二路")]
src = np.array([e[0] for e in ECKEN], float); dst = np.array([kreuzung(e[1], e[2]) for e in ECKEN])
def affin(a, b, w=None):
    A = np.c_[a, np.ones(len(a))]; w = np.ones(len(a)) if w is None else w
    return np.linalg.lstsq(A * np.sqrt(w)[:, None], b * np.sqrt(w)[:, None], rcond=None)[0]
def ab(M, p): p = np.asarray(p, float); return p @ M[:2] + M[2]
M = affin(src, dst)
r0 = np.hypot(*(ab(M, src) - dst).T)
print("Startwert aus", len(src), "Ecken: Maßstab", round(float(np.hypot(M[0, 0], M[0, 1])), 3), "m/px, Restfehler", np.round(r0).tolist(), "m")
# blaue Pixel ohne Kilometerkreise (Radius + 8 px), ohne Legende (rechts unten) und Kopf/Fuß
kr = np.array([[v[0], v[1], v[2]] for v in P["km"].values()])
ok = np.ones(len(BL), bool)
for x, y, r in kr: ok &= np.hypot(BL[:, 0] - x, BL[:, 1] - y) > r + 8
S = P["breite"] / 1400
ok &= ~((BL[:, 0] > 690 * S) & (BL[:, 1] > 1010 * S))          # Legende
ok &= (BL[:, 1] > 200 * S) & (BL[:, 1] < 1740 * S) & (BL[:, 0] > 60 * S)
Q = BL[ok][::2]
# Symbole (Becher, Tropfen, Schwamm) sind kleine blaue Rahmen neben der Linie: nur Pixel nahe der Linie zwischen den Kreisen behalten
def osmlinien(filt):
    out = []
    for tg, refs in W.values():
        if filt(tg):
            ll = np.array([N[r] for r in refs if r in N])
            if len(ll) > 1: x, y = utm(ll[:, 0], ll[:, 1]); out.append(dicht(np.c_[x, y], 5))
    return np.vstack(out)
STR = osmlinien(lambda t: t.get("highway") in ("trunk", "primary", "secondary", "tertiary", "unclassified", "residential", "trunk_link",
                                               "secondary_link", "tertiary_link", "living_street", "road", "pedestrian")
                and t.get("tunnel") in (None, "no") and t.get("layer", "0") in ("0", "-0"))
T = cKDTree(STR)
for fang in (250, 200, 150, 100, 80, 60, 50, 40, 40):
    for it in range(4):
        X = ab(M, Q); d, i = T.query(X); sel = d < fang
        w = np.where(d[sel] < 15, 1.0, 15 / np.maximum(d[sel], 1e-9))
        M = affin(Q[sel], STR[i[sel]], w)
d, _ = T.query(ab(M, Q))
print(f"{len(Q)} Linienpixel: Abstand zur nächsten OSM-Straße Median {np.median(d):.1f} m, 75 % {np.percentile(d, 75):.1f} m, 90 % {np.percentile(d, 90):.1f} m")
r1 = np.hypot(*(ab(M, src) - dst).T)
print("Ecken danach:", np.round(r1).tolist(), "m")
sx = math.hypot(M[0, 0], M[0, 1]); sy = math.hypot(M[1, 0], M[1, 1])
print(f"Maßstab x {sx:.4f} m/px, y {sy:.4f} m/px, Drehung {math.degrees(math.atan2(M[0, 1], M[0, 0])):.2f}°, Winkel zwischen den Achsen "
      f"{math.degrees(math.acos(abs(M[0] @ M[1]) / (sx * sy))):.2f}°")
json.dump({"M": M.tolist(), "rest": {"median": float(np.median(d)), "p90": float(np.percentile(d, 90))}, "ecken": r1.tolist()},
          open("georef.json", "w"))
