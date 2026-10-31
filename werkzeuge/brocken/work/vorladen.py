# Lädt die DGM1- und DOM1-Kacheln (2 × 2 km) im Umkreis von 60 m um die Linie einmal vor (lvermgeo.py), damit dgm.py und deck.py
# nur noch lesen. Aufruf: python3 vorladen.py [dgm1|dom1]
import json, sys
import numpy as np
from pyproj import Transformer
import lvermgeo
art = sys.argv[1] if len(sys.argv) > 1 else "dgm1"
T = Transformer.from_crs(4326, 25832, always_xy=True)
g = json.load(open("linie.json")); P = np.array(g["pts"]); d = np.array(g["d"])
ss = np.arange(0, d[-1], 10.0); E, N = T.transform(np.interp(ss, d, P[:, 1]), np.interp(ss, d, P[:, 0]))
need = sorted({(int((e + de) // 2000) * 2, int((n + dn) // 2000) * 2) for e, n in zip(E, N) for de in (-60, 0, 60) for dn in (-60, 0, 60)})
print(len(need), "Kacheln", art, flush=True)
for i, (e, n) in enumerate(need):
    f = lvermgeo._tif(art, e, n); print(i + 1, e, n, f, flush=True)
