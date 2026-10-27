# Brücken und Überführungen: wo das Geländemodell ins Wasser oder in einen Einschnitt fällt, die gemessene Fahrbahn aus der
# Laser-Punktwolke nehmen. Je Punkt: Laserpunkte im Umkreis von 4 m, die mehr als 2 m über dem Boden liegen; davon das untere
# Zehntel (Fahrbahn; Seile, Fachwerk und Fahrzeuge liegen darüber). Ein Durchlauf von vorn wählt je Punkt Boden oder Fahrbahn,
# je nachdem, was stetig an den Vorgänger anschließt; so heben Schilderbrücken oder Bauwerke über der Strecke das Profil nicht.
import json, math, time
import numpy as np
from common import official, gpx_of
from ept import query, merc
r = json.load(open("dgm2026_10m.json")); s = np.array([x[0] for x in r]); la = np.array([x[1] for x in r]); lo = np.array([x[2] for x in r])
dem = np.array([x[3] for x in r]); k = official(s)
FENSTER = [(0, 4.0), (5.8, 6.6), (8.0, 8.7), (16.1, 16.9), (20.5, 22.1), (22.9, 26.7), (30.9, 32.5), (33.1, 34.3)]   # offizielle km
X, Y = np.array([merc(a, b) for a, b in zip(la, lo)]).T
f = 1 / math.cos(math.radians(40.7)); rad = 4.0 * f                                          # 4 m am Boden in Mercator-Metern
import os
deck = np.full(len(s), np.nan); t0 = time.time()
if os.path.exists("lidar.json"): deck = np.array([np.nan if v is None else v for v in json.load(open("lidar.json"))["deck"]])
for a_km, b_km in ([] if os.path.exists("lidar.json") else FENSTER):
    idx = np.where((k >= a_km * 1000) & (k <= b_km * 1000))[0]
    for c0 in range(0, len(idx), 10):
        ii = idx[c0:c0 + 10]
        P = query(X[ii].min() - rad, Y[ii].min() - rad, X[ii].max() + rad, Y[ii].max() + rad)
        for i in ii:
            m = ((P[:, 0] - X[i]) ** 2 + (P[:, 1] - Y[i]) ** 2 <= rad * rad) & (P[:, 2] > dem[i] + 2)
            if m.sum() >= 5: deck[i] = np.percentile(P[m, 2], 10)
    print(f"Fenster km {a_km:4.1f}-{b_km:4.1f}: {np.isfinite(deck[idx]).sum():4d} von {len(idx)} Punkten mit Fahrbahn über Boden, {round(time.time() - t0)} s")
# Auswahl fest je Bauwerk (offizielle km): auf der Spanne die gemessene Fahrbahn (Lücken linear), davor und danach eine Gerade
# vom Boden an der Rampe zur Fahrbahn an der Spannenkante. Eine automatische Wahl ist an den Rampen in Brooklyn und an der
# Queensboro Bridge auf darüberliegende Bauwerke gesprungen.
ZONEN = [  # Name, Spanne von, bis, Rampe vom Boden ab, bis zum Boden (None: Spanne endet am Boden)
    ("Verrazzano-Narrows Bridge", 0.18, 3.20, None, None),
    ("Überführung 4th Avenue", 6.18, 6.21, None, None),
    ("Überführung", 8.36, 8.37, None, None),
    ("Überführung", 16.46, 16.49, None, None),
    ("Pulaski Bridge", 20.92, 21.50, None, None),
    ("Queensboro Bridge", 24.14, 25.52, 23.78, 25.95),   # untere Ebene nicht messbar, siehe Übergabe
    ("Willis Avenue Bridge", 31.31, 31.92, None, None),
    ("Madison Avenue Bridge", 33.61, 33.74, None, None),
]
h = dem.copy(); src = np.zeros(len(s), int)   # 0 Boden, 1 Fahrbahn gemessen, 2 Rampe geschätzt
at = lambda km: int(np.argmin(np.abs(k - km * 1000)))
for nm, a, b, ra, rb in ZONEN:
    ia, ib = at(a), at(b); ii = np.arange(ia, ib + 1); ok = np.isfinite(deck[ii])
    h[ii] = np.interp(ii, ii[ok], deck[ii][ok]); src[ii] = 1
    if ra is not None: j = np.arange(at(ra), ia); h[j] = np.interp(j, [j[0], ia], [dem[j[0]], h[ia]]); src[j] = 2
    if rb is not None: j = np.arange(ib + 1, at(rb) + 1); h[j] = np.interp(j, [ib, j[-1]], [h[ib], dem[j[-1]]]); src[j] = 2
hm = h.copy()
for i in range(1, len(h) - 1): hm[i] = np.median(h[i - 1:i + 2])
json.dump({"h": hm.tolist(), "src": src.tolist(), "deck": [None if not np.isfinite(v) else float(v) for v in deck]}, open("lidar.json", "w"))
i = 0
while i < len(src):
    if not src[i]: i += 1; continue
    j = i
    while j + 1 < len(src) and src[j + 1]: j += 1
    print(f"Bauwerk km {k[i]/1000:6.2f}-{k[j]/1000:6.2f}  höchster Punkt {hm[i:j+1].max():5.1f} m (Boden darunter min {dem[i:j+1].min():5.1f} m)")
    i = j + 1
