# Fahrbahn der vier Brücken aus dem Oberflächenmodell DOM1 Hessen (Laserscan, 1-m-Raster, © HVBG, WCS wie das DGM1)
# -> dom_bruecken.json [[GPX-Meter, Höhe], …] für die Punkte zwischen den Brückenköpfen. Das DGM1 misst dort den Main
# bzw. die Nidda; bis 1.13 stand dafür eine Gerade zwischen den Köpfen. Je Punkt das 25-%-Quantil der 5 × 5 m um den
# Punkt (darüber Fahrzeuge und Geländer). Nur innerhalb der Brücken: daneben misst das DOM Bäume und Häuser (Höchst).
# An den Köpfen stimmen DOM und DGM auf 0,1 m überein.
import io, json, urllib.request, numpy as np
from PIL import Image
from pyproj import Transformer
from common import official
# Brückenköpfe (offizielle Meter) aus clean.py, Stand 1.13
BRUECKEN = [(13058, 13344, "Alte Brücke"), (23913, 24476, "Schwanheimer Brücke"), (26089, 26164, "Mainzer Landstraße (Nidda)"),
            (28129, 28222, "Bolongarostraße (Nidda)")]
r = json.load(open("dgm2026_10m.json"))
s = np.array([x[0] for x in r]); la = np.array([x[1] for x in r]); lo = np.array([x[2] for x in r]); k = official(s)
T = Transformer.from_crs(4326, 25832, always_xy=True); out = []
for a, b, name in BRUECKEN:
    sel = (k > a) & (k < b)
    E, N = map(np.asarray, T.transform(lo[sel], la[sel]))
    e0, e1, n0, n1 = int(E.min()) - 10, int(E.max()) + 11, int(N.min()) - 10, int(N.max()) + 11
    url = ("https://inspire-hessen.de/raster/dom1/ows?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&COVERAGEID=dom1"
           f"&FORMAT=image/tiff&SUBSET=E({e0},{e1})&SUBSET=N({n0},{n1})")
    A = np.array(Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "marathon-profile-check/1.0 (private use)"}), timeout=90).read())), dtype=float)
    hs = []
    for sg, x, y in zip(s[sel], E, N):   # Zeile r deckt N in [n1-1-r, n1-r), Spalte c deckt E in [e0+c, e0+c+1)
        rr, cc = int(n1 - y), int(x - e0); hs.append(float(np.percentile(A[rr - 2:rr + 3, cc - 2:cc + 3], 25))); out.append([float(sg), hs[-1]])
    hs = np.array(hs); print(f"{name:28s} km {a/1000:.2f}–{b/1000:.2f}: {len(hs)} Punkte, höchster {hs.max():.1f} m, größte Stufe {np.abs(np.diff(hs)).max():.2f} m je 10 m")
json.dump(out, open("dom_bruecken.json", "w"))
