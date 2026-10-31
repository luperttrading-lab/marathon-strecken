# Fahrbahn der Brücken aus dem Oberflächenmodell DOM1 NRW (Laserscan, 1-m-Raster, © Geobasis NRW, dl-de/zero-2-0; WCS wcs_nw_dom,
# Coverage nw_dom, Achsen x/y wie das DGM). Kopie von werkzeuge/duesseldorf/work/dom.py (dort alle Brücken; Muster werkzeuge/koeln/work/dom.py, Deutzer Brücke). Das Geländemodell DGM1 kennt keine
# Brücken und misst dort den Rhein, die Gleise oder den Graben darunter; das DOM zeigt die Oberfläche samt Brücke.
# Je 10-m-Punkt im Bereich: Lotfußpunkt auf den OSM-Weg, den strassen.py dort gefunden hat (Fahrbahnmitte statt gezeichneter Linie,
# die bis 18 m daneben liegen kann), dort das 25-%-Quantil der 5 × 5 m (darunter Wasser oder Gleise am Rand, darüber Fahrzeuge,
# Leuchten, Oberleitung). An den Enden der Bereiche liegt die Straße wieder auf dem Boden: DOM und DGM sollten dort gleich sein
# (Ausgabe „Enden“), sonst ist der Bereich zu kurz oder ein Baum steht über der Straße. Werte mehr als 1 m über dem höheren Ende
# gelten als Baum und werden zwischen den Nachbarn ersetzt (Promenade, Twerenfeldweg, Arnheimweg, Roxeler Straße am Gievenbach).
# -> dom2026.json [[Linienmeter, DOM-Höhe, OSM-Weg], …]
import io, json, urllib.request
import numpy as np
from PIL import Image
from pyproj import Transformer
from common import official
T = Transformer.from_crs(4326, 25832, always_xy=True)
# Bereiche in offiziellen km (Brücke samt Rampenfuß, aus den Sprüngen im DGM und den OSM-Brücken; darunter laut OSM: Münstersche Aa (achtmal),
# Gievenbach, ein Graben, die B 54 und zweimal die A 1)
BEREICHE = [(0.51, 0.59, "Am Stadtgraben über die Aa"), (1.25, 1.33, "Bispinghof über die Aa"), (2.84, 2.92, "Neubrückenstraße über die Aa"),
            (6.73, 6.82, "Promenade über die Aa"), (11.95, 12.17, "Kardinal-von-Galen-Ring über die Aa"),
            (19.78, 19.89, "Haus Uhlenkotten über die B 54"), (21.00, 21.10, "Steinfurter Straße über die A 1"),
            (26.37, 26.44, "Twerenfeldweg über die Aa"), (28.16, 28.22, "Bredeheide über einen Graben"),
            (30.80, 30.92, "Roxeler Straße über die A 1"), (31.96, 32.03, "Roxeler Straße über die Aa"),
            (36.70, 36.76, "Arnheimweg über den Gievenbach"), (37.53, 37.60, "Roxeler Straße über den Gievenbach"),
            (41.12, 41.20, "Adenauerallee über die Aa")]
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
        hs.append(float(np.percentile(A[rr - 2:rr + 3, cc - 2:cc + 3], 25)))
    # Bäume, Leuchten über der Fahrbahn (Promenade, kleine Brücken über Bäche): Werte mehr als 1 m über dem höheren Ende oder 0,5 m unter
    # dem tieferen Ende (Geländehöhe an den Enden aus dem DGM) gelten nicht; dort linear zwischen den gültigen Nachbarn. An den Enden selbst
    # gilt das DGM, wenn das DOM mehr als 0,5 m davon abweicht.
    hs = np.array(hs); ea, eb = dgm[sel[0]], dgm[sel[-1]]
    ok = (hs <= max(ea, eb) + 1.0) & (hs >= min(ea, eb) - 0.5); ok[0] = ok[-1] = True
    roh = hs.copy(); hs[0], hs[-1] = (hs[0] if abs(hs[0] - ea) <= 0.5 else ea), (hs[-1] if abs(hs[-1] - eb) <= 0.5 else eb)
    hs = np.interp(np.arange(len(hs)), np.where(ok)[0], hs[ok])
    for (i, q, dq, wid), h in zip(Q, hs): out.append([float(s[i]), float(h), wid])
    ver = np.array([dq for _, _, dq, _ in Q])
    if (~ok).any() or (roh != hs).any(): print(f"   {nm}: {int((~ok).sum()) + int(roh[0] != hs[0]) + int(roh[-1] != hs[-1])} von {len(hs)} Werten ersetzt (Bäume über der Fahrbahn), roh bis {roh.max():.1f} m")
    print(f"{nm:45s} km {a:.2f}–{b:.2f}: DOM {hs.min():.1f}–{hs.max():.1f} m (DGM {dgm[sel].min():.1f}–{dgm[sel].max():.1f}), "
          f"Enden DOM−DGM {hs[0] - dgm[sel[0]]:+.1f} / {hs[-1] - dgm[sel[-1]]:+.1f} m, Linie bis {ver.max():.0f} m neben dem Weg, "
          f"größte Stufe {np.abs(np.diff(hs)).max():.2f} m je 10 m")
json.dump(out, open("dom2026.json", "w"))
