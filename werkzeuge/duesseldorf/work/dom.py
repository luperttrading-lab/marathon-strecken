# Fahrbahn der Brücken aus dem Oberflächenmodell DOM1 NRW (Laserscan, 1-m-Raster, © Geobasis NRW, dl-de/zero-2-0; WCS wcs_nw_dom,
# Coverage nw_dom, Achsen x/y wie das DGM). Muster: werkzeuge/koeln/work/dom.py (Deutzer Brücke). Das Geländemodell DGM1 kennt keine
# Brücken und misst dort den Rhein, die Gleise oder den Graben darunter; das DOM zeigt die Oberfläche samt Brücke.
# Je 10-m-Punkt im Bereich: Lotfußpunkt auf den OSM-Weg, den strassen.py dort gefunden hat (Fahrbahnmitte statt gezeichneter Linie,
# die bis 8 m daneben liegen kann), dort das 25-%-Quantil der 5 × 5 m (darunter Wasser oder Gleise am Rand, darüber Fahrzeuge,
# Leuchten, Oberleitung). An den Enden der Bereiche liegt die Straße wieder auf dem Boden: DOM und DGM sollten dort gleich sein
# (Ausgabe „Enden“), sonst ist der Bereich zu kurz oder ein Baum steht über der Straße.
# -> dom2026.json [[Linienmeter, DOM-Höhe, OSM-Weg], …]
import io, json, urllib.request
import numpy as np
from PIL import Image
from pyproj import Transformer
from common import official
T = Transformer.from_crs(4326, 25832, always_xy=True)
# Bereiche in offiziellen km (Brücke samt Rampenfuß, aus den Sprüngen im DGM und den OSM-Brücken; darunter laut OSM: Rhein, Gleise,
# Kö-Graben, Düssel, die Fußgängerunterführung Weyhepassage und die Unterführung an der Hofgartenrampe)
BEREICHE = [(12.46, 12.56, "Maximilian-Weyhe-Allee über die Weyhepassage"), (12.86, 12.95, "Hofgartenrampe über eine Fußgängerunterführung"),
            (13.03, 13.76, "Oberkasseler Brücke (nach Westen)"), (22.02, 22.74, "Oberkasseler Brücke (nach Osten)"),
            (22.82, 22.91, "Hofgartenrampe über eine Fußgängerunterführung"), (23.97, 24.07, "Benrather Straße über den Kö-Graben"),
            (24.93, 25.04, "Maximilian-Weyhe-Allee über die Weyhepassage"), (27.35, 27.60, "Jülicher Brücke über die Bahn"),
            (32.16, 32.32, "Am Wehrhahn über die Bahn"), (33.32, 33.50, "Jacobistraße über die Düssel"), (40.38, 40.47, "Benrather Straße über den Kö-Graben")]
r = json.load(open("dgm2026_10m.json"))
s = np.array([x[0] for x in r]); la = np.array([x[1] for x in r]); lo = np.array([x[2] for x in r]); dgm = np.array([x[3] for x in r]); k = official(s)
E, N = map(np.asarray, T.transform(lo, la))
st = json.load(open("strassen.json")); o = json.load(open("../dl/osm_netz.json")); NO = o["nodes"]
def weg(wid):
    pts = [NO[str(q)] for q in o["ways"][wid][1] if str(q) in NO]
    x, y = T.transform([p[1] for p in pts], [p[0] for p in pts]); return np.c_[x, y]
def lot(p, A):
    a = A[:-1]; b = A[1:]; v = b - a; t = np.clip(((p - a) * v).sum(1) / np.maximum((v * v).sum(1), 1e-9), 0, 1); q = a + t[:, None] * v
    dq = np.hypot(*(q - p).T); i = dq.argmin(); return q[i], dq[i]
URL = "https://www.wcs.nrw.de/geobasis/wcs_nw_dom?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&COVERAGEID=nw_dom&FORMAT=image/tiff"
out = []
for a, b, nm in BEREICHE:
    sel = np.where((k >= a * 1000) & (k <= b * 1000))[0]
    Q = []
    for i in sel:
        p = np.array([E[i], N[i]]); wid = st[min(len(st) - 1, int(round(s[i] / 10)))][7]
        q, dq = (lot(p, weg(wid)) if wid else (p, 0.0))
        Q.append((i, q, dq, wid))
    X = np.array([q for _, q, _, _ in Q])
    e0, e1, n0, n1 = int(X[:, 0].min()) - 10, int(X[:, 0].max()) + 11, int(X[:, 1].min()) - 10, int(X[:, 1].max()) + 11
    raw = urllib.request.urlopen(urllib.request.Request(URL + f"&SUBSET=x({e0},{e1})&SUBSET=y({n0},{n1})",
                                 headers={"User-Agent": "marathon-profile-check/1.0 (private use)"}), timeout=90).read()
    A = np.array(Image.open(io.BytesIO(raw)), dtype=float)
    hs = []
    for i, q, dq, wid in Q:
        rr, cc = int(n1 - q[1]), int(q[0] - e0)          # Zeile r deckt N in [n1-1-r, n1-r), Spalte c deckt E in [e0+c, e0+c+1)
        h = float(np.percentile(A[rr - 2:rr + 3, cc - 2:cc + 3], 25)); hs.append(h)
        out.append([float(s[i]), h, wid])
    hs = np.array(hs); ver = np.array([dq for _, _, dq, _ in Q])
    print(f"{nm:45s} km {a:.2f}–{b:.2f}: DOM {hs.min():.1f}–{hs.max():.1f} m (DGM {dgm[sel].min():.1f}–{dgm[sel].max():.1f}), "
          f"Enden DOM−DGM {hs[0] - dgm[sel[0]]:+.1f} / {hs[-1] - dgm[sel[-1]]:+.1f} m, Linie bis {ver.max():.0f} m neben dem Weg, "
          f"größte Stufe {np.abs(np.diff(hs)).max():.2f} m je 10 m")
json.dump(out, open("dom2026.json", "w"))
