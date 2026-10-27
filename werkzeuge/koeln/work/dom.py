# Fahrbahn der Deutzer Brücke aus dem Oberflächenmodell DOM1 NRW (Laserscan, 1-m-Raster, © Geobasis NRW, dl-de/zero-2-0)
# -> dom_deutz.json [[GPX-Meter, Höhe], …] für km 0,50–1,10 (offiziell). Das Geländemodell DGM1 kennt keine Brücken und
# misst dort den Rhein; das DOM zeigt die Oberfläche samt Brücke. Je Punkt das 25-%-Quantil der 5 × 5 m um den Punkt:
# darunter liegt nur der Rhein neben der Fahrbahn, darüber Fahrzeuge, Leuchten und Oberleitung der Stadtbahn.
# An Land stimmen DOM und DGM auf 0,1 m überein, deshalb ohne Übergang.
import io, json, urllib.request, numpy as np
from PIL import Image
from pyproj import Transformer
from common import official
r = json.load(open("dgm2026_10m.json"))
s = np.array([x[0] for x in r]); la = np.array([x[1] for x in r]); lo = np.array([x[2] for x in r]); k = official(s)
sel = (k >= 500) & (k <= 1100)
E, N = map(np.asarray, Transformer.from_crs(4326, 25832, always_xy=True).transform(lo[sel], la[sel]))
e0, e1, n0, n1 = int(E.min()) - 10, int(E.max()) + 11, int(N.min()) - 10, int(N.max()) + 11
url = ("https://www.wcs.nrw.de/geobasis/wcs_nw_dom?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&COVERAGEID=nw_dom"
       f"&FORMAT=image/tiff&SUBSET=x({e0},{e1})&SUBSET=y({n0},{n1})")
A = np.array(Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "marathon-profile-check/1.0 (private use)"}), timeout=90).read())), dtype=float)
# Zeile r deckt N in [n1-1-r, n1-r), Spalte c deckt E in [e0+c, e0+c+1)
out = []
for sg, x, y in zip(s[sel], E, N):
    rr, cc = int(n1 - y), int(x - e0)
    out.append([float(sg), float(np.percentile(A[rr - 2:rr + 3, cc - 2:cc + 3], 25))])
hd = np.array([o[1] for o in out]); kd = k[sel]
print(f"{len(out)} Punkte; höchster {hd.max():.1f} m bei km {kd[hd.argmax()] / 1000:.2f}; größte Stufe {np.abs(np.diff(hd)).max():.2f} m je 10 m")
json.dump(out, open("dom_deutz.json", "w"))
