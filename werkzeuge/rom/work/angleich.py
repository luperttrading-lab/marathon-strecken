# TINITALY (dgm_tinitaly.json) an die Höhen der Regione Lazio angleichen -> dgm2026_10m.json [Linienmeter, Breite, Länge, Höhe].
# Warum: TINITALY ist aus Höhenlinien und Höhenpunkten trianguliert (10-m-Raster). Wo eine Straße am Fuß eines Hügels läuft, zieht das
# Modell sie den Hang hinauf (Via del Teatro di Marcello am Kapitol +18 m, Via Marmorata am Aventin +10 m, Testaccio am Monte Testaccio
# +8 m), auf Dämmen und Brückenrampen fehlt sie (Via Cristoforo Colombo −11 m, Rampe des Ponte Settimia Spizzichino −8 m).
# Passpunkte aus der DBGT 2014 der Regione Lazio (photogrammetrisch 1:5000, Koordinaten mit Höhe über dem Meer; curve.py, dbgt.py):
#   - Stellen, an denen die Linie eine Höhenlinie kreuzt (nicht auf Brücken und in Unterführungen: dort ist die Höhenlinie der
#     Boden darunter),
#   - Verkehrsinseln und Fahrbahnteiler („Manufatto di infrastruttura di trasporto“, Typ 01) höchstens 10 m neben der Linie,
#   - Radwegflächen („Area di circolazione ciclabile“) höchstens 10 m neben der Linie,
#   - Fahrbahnen der Brücken („Ponte viadotto e cavalcavia“), Eckpunkte höchstens 15 m neben der Linie mit 10–28 m Höhe und höchstens
#     4 m unter dem Median der Brücke (ohne Pfeiler und Wasser unten, ohne Fachwerk oben), nur wo die Linie laut OSM auf einer Brücke liegt (dort keine anderen Passpunkte: was
#     neben einer Brücke liegt, liegt meist unter ihr),
#   - Kleinbauten auf Gehwegen und Plätzen („Edificio minore“: Kioske, Häuschen), der tiefste Eckpunkt höchstens 15 m neben der Linie
#     (die Eckpunkte liegen am Boden: an 9 Stellen mit anderen Passpunkten daneben im Median 0,9 m darunter).
# Vorher werden schmale Buckel von TINITALY entfernt (graue Öffnung über 500 m: Erhebungen, die schmaler als 500 m sind, fallen weg;
# Täler und breite Anstiege bleiben), denn das Modell zieht die Straßen an Hängen nur nach oben. Dann je 20 Linienmeter der Median
# der Passpunkte; Abschnitte ohne Höhenlinie, die auf höchstens 2 Punkten beruhen und mehr als 4 m vom Median der Nachbarn (±300 m)
# abweichen, entfallen. Höhe = Gerade zwischen den Passpunkten plus die halbe Abweichung, die TINITALY dort von seiner eigenen
# Geraden zwischen denselben Stellen zeigt (vor dem ersten und nach dem letzten Passpunkt waagerecht plus dieselbe halbe Abweichung).
# Warum halb: Probe durch Weglassen ganzer Abschnitte von Passpunkten (Lücken 0,8 / 1,5 / 2,5 km, Median / quadratisches Mittel
# der Abweichung an den weggelassenen Punkten): reine Gerade 1,1/2,2 · 2,1/3,5 · 2,5/4,4 m, Gerade plus volle TINITALY-Form 1,2/2,4 ·
# 2,0/3,0 · 2,7/3,8 m, plus halbe Form 1,0/2,1 · 1,6/3,0 · 2,4/3,9 m. TINITALY trägt also nur in großen Lücken etwas bei. Zum Vergleich
# TINITALY allein an den Passpunkten: Median 2,2 m, 90 % 6,6 m, größte Abweichung 17,6 m.
# -> angleich.json (Passpunkte, Abweichungen) zur Kontrolle
import json, numpy as np
from scipy.ndimage import grey_opening
from pyproj import Transformer
from scipy.spatial import cKDTree
T = Transformer.from_crs(4326, 25833, always_xy=True)
r = json.load(open("dgm_tinitaly.json")); s = np.array([x[0] for x in r]); hroh = np.array([x[3] for x in r], float)
h0 = grey_opening(hroh, size=50, mode="nearest")   # 50 Punkte = 500 m
X = np.c_[T.transform([x[2] for x in r], [x[1] for x in r])]; baum = cKDTree(X)
st = json.load(open("strassen.json"))
bruecke = np.array([bool(o[2]) and o[2] != "no" for o in st] + [False] * (len(s) - len(st)))[:len(s)]
tunnel = np.array([bool(o[3]) and o[3] != "no" for o in st] + [False] * (len(s) - len(st)))[:len(s)]
def nahe(m, w):   # Maske um w Punkte erweitert
    out = m.copy()
    for j in range(1, w + 1): out[j:] |= m[:-j]; out[:-j] |= m[j:]
    return out
br3, tu3 = nahe(bruecke, 3), nahe(tunnel, 3)
pp = []   # [Index, Höhe, Quelle]
# 1. Höhenlinien: Schnitt Linie / Höhenlinie
def schnitt(p1, p2, q1, q2):
    d1 = p2 - p1; d2 = q2 - q1; den = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(den) < 1e-9: return None
    t = ((q1[0] - p1[0]) * d2[1] - (q1[1] - p1[1]) * d2[0]) / den; u = ((q1[0] - p1[0]) * d1[1] - (q1[1] - p1[1]) * d1[0]) / den
    return t if 0 <= t <= 1 and 0 <= u <= 1 else None
x0, y0 = X.min(0) - 50; x1, y1 = X.max(0) + 50
for f in json.load(open("../dl/curve_livello.json"))["features"]:
    z = float(f["properties"]["cv_liv_q"]); g = f["geometry"]
    for line in (g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]):
        L = np.array([c[:2] for c in line])
        if L[:, 0].max() < x0 or L[:, 0].min() > x1 or L[:, 1].max() < y0 or L[:, 1].min() > y1: continue
        for a, b in zip(L[:-1], L[1:]):
            lo, hi = np.minimum(a, b) - 10, np.maximum(a, b) + 10
            for i in np.where((X[:-1, 0] >= lo[0]) & (X[:-1, 0] <= hi[0]) & (X[:-1, 1] >= lo[1]) & (X[:-1, 1] <= hi[1]))[0]:
                t = schnitt(X[i], X[i + 1], a, b)
                j = i if t is None or t < 0.5 else i + 1
                if t is not None and not br3[j] and not tu3[j]: pp.append([int(j), z, "Höhenlinie"])
def ecken(g):
    t, c = g["type"], g["coordinates"]
    if t in ("Point",): return [c]
    if t in ("MultiPoint", "LineString"): return c
    if t in ("MultiLineString", "Polygon"): return [p for l in c for p in l]
    return [p for poly in c for l in poly for p in l]
for f in json.load(open("../dl/dbgt_wms_edi_min_a.json"))["features"]:
    V = np.array(ecken(f["geometry"]))
    if V.shape[1] < 3: continue
    dd, ii = baum.query(V[:, :2]); m = (dd <= 15) & (V[:, 2] > 0)
    if m.any():
        j = np.argmin(V[m, 2]); i = int(ii[m][j])
        if not br3[i] and not tu3[i]: pp.append([i, float(V[m, 2][j]), "Kleinbau"])
for kl, quelle, dmax in [("web_020205_man_tr_l", "Verkehrsinsel", 10), ("web_010103_ac_cic_a", "Radweg", 10), ("web_020301_ponte_a", "Brücke", 15)]:
    for f in json.load(open(f"../dl/dbgt_{kl}.json"))["features"]:
        if kl == "web_020205_man_tr_l" and f["properties"].get("man_tr_ty") != "01": continue
        neu = []
        for v in ecken(f["geometry"]):
            if len(v) < 3 or v[2] <= 0: continue
            d, i = baum.query(v[:2])
            if d > dmax or tu3[i]: continue
            if kl == "web_020301_ponte_a" and not (bruecke[i] and 10 < v[2] < 28): continue
            if kl != "web_020301_ponte_a" and br3[i]: continue   # auf Brücken nur die Fahrbahn der Brücke, nicht Inseln darunter
            neu.append([int(i), float(v[2]), quelle])
        if kl == "web_020301_ponte_a" and neu:   # Pfeilerfüße und Uferpunkte der Brückenfläche weglassen
            med = np.median([z for _, z, _ in neu]); neu = [p for p in neu if p[1] >= med - 4]
        pp += neu
# je 20 m (zwei Punkte des 10-m-Rasters) der Median
grp = {}
for i, z, q in pp: grp.setdefault(i // 2, []).append((z, q))
ab = sorted((b, float(np.median([z for z, _ in v])), len(v), sorted({q for _, q in v})) for b, v in grp.items())
idx = np.array([b * 2 for b, _, _, _ in ab]); zz = np.array([z for _, z, _, _ in ab]); nn = np.array([n for _, _, n, _ in ab])
res = zz - h0[idx]
gut = np.ones(len(res), bool)
for j in range(len(res)):
    nb = (np.abs(idx - idx[j]) <= 30) & (np.arange(len(res)) != j)
    if nb.sum() >= 2 and abs(res[j] - np.median(res[nb])) > 4 and nn[j] <= 2 and "Höhenlinie" not in ab[j][3]: gut[j] = False
print(f"{len(pp)} Passpunkte in {len(ab)} Abschnitten zu 20 m, {(~gut).sum()} verworfen; Quellen:",
      {q: sum(1 for p in pp if p[2] == q) for q in ("Höhenlinie", "Verkehrsinsel", "Radweg", "Brücke", "Kleinbau")})
ig, zg = idx[gut], zz[gut]
alle = np.arange(len(h0))
gerade = np.interp(alle, ig, zg); gerade_t = np.interp(alle, ig, h0[ig])
h = gerade + 0.5 * (h0 - gerade_t)
korr = h - hroh
print(f"TINITALY roh zu den Passpunkten: Median {np.median(zz - hroh[idx]):+.1f} m, Betrag 90 % {np.percentile(abs(zz - hroh[idx]), 90):.1f} m")
print(f"Ergebnis gegen TINITALY roh: {korr.min():+.1f} bis {korr.max():+.1f} m, Betrag im Mittel {np.abs(korr).mean():.1f} m")
json.dump([[float(a), float(b[1]), float(b[2]), round(float(v), 3)] for a, b, v in zip(s, r, h)], open("dgm2026_10m.json", "w"))
json.dump({"pp": [[float(s[i]), round(float(z), 2), round(float(hroh[i]), 2), int(n), q, bool(g_), round(float(h0[i]), 2)] for i, z, n, q, g_ in zip(idx, zz, nn, [a[3] for a in ab], gut)]},
          open("angleich.json", "w"), ensure_ascii=False)
