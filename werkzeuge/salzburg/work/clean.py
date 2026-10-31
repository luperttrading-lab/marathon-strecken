# Brücken und Unterführungen im Höhenprofil -> clean.json. Grundlage: Laser-Geländemodell des BEV an der Straßenmitte (dtm.py).
# - Brücken: Ein Geländemodell kennt keine Brücken. Auf der Staatsbrücke (Start, km 20,6 und 41,7) und der Lehener Brücke (km 18,9
#   und 40,0) misst es die Salzach (412–413 m statt 420–422 m). Dort gilt das Oberflächenmodell derselben Befliegung (ALS DSM,
#   25-%-Quantil im Umkreis von 2 m, dtm.py): wo es auf einem OSM-Brückenweg (Straße) und bis 3 Punkte davor und danach mehr als 1 m
#   über dem Geländemodell liegt. An den Enden stimmen beide auf 0,1–0,3 m überein. Die Brücken zählen damit als gemessen (nicht
#   schraffiert, wie in Wien, Freiburg und Rom). Die kleinen Brücken über Almkanal und Bäche (Hellbrunner Allee, Berchtesgadener
#   Straße, Nissenstraße, Zwieselweg) misst das Geländemodell ohne Senke (höchstens 1,3 m an einem Punkt, den der Median glättet).
# - Unterführung Gaswerkgasse (km 18,2 und 39,3; OSM tunnel=yes, layer −1, Durchfahrtshöhe 3,75 m): Die Straße führt unter dem
#   Bahndamm durch, das Geländemodell misst den Damm (bis 429 m). Geschätzt als Gerade zwischen dem letzten Punkt davor (Müllner
#   Hauptstraße, 426,0 m) und dem ersten danach (418,4 m), im Läuferblick gestrichelt (D.bridges, Art „Unterführung“).
# Die übrigen Tunnel der OSM-Daten sind Durchgänge (Gstättentor, Ritzerbogen, Dreifaltigkeitsgasse) oder die Unterführung des
# Elisabethkais unter der Eisenbahnbrücke; dort misst das Modell die Straße (keine Stufe).
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from itertools import groupby
from common import official
r = json.load(open("dtm_10m.json")); st = json.load(open("strassen.json"))
s = np.array([x[0] for x in r]); k = official(s)
raw = np.array([x[5] for x in r], float); dsm = np.array([x[6] if x[6] is not None else np.nan for x in r], float)
h = raw.copy(); regions = []
STRASSE = ("primary", "secondary", "tertiary", "residential", "unclassified", "living_street", "pedestrian", "service")
# Brücken aus dem Oberflächenmodell
br = [i for i, q in enumerate(st) if q[3] not in ("", "no") and q[6] in STRASSE]
for _, g in groupby(enumerate(br), key=lambda t: t[1] - t[0]):
    g = [x[1] for x in g]; a0, b0 = max(0, g[0] - 3), min(len(h) - 1, g[-1] + 3)
    # Senke: Geländemodell mehr als 1 m unter beiden Enden und unter dem Oberflächenmodell, das selbst nicht mehr als 3 m über den
    # Enden liegt (sonst misst es Bäume über dem Weg, z. B. am Zwieselweg)
    e_lo, e_hi = min(raw[a0], raw[b0]), max(raw[a0], raw[b0])
    tief = [i for i in range(a0, b0 + 1) if raw[i] < e_lo - 1.0 and dsm[i] - raw[i] > 1.0 and dsm[i] < e_hi + 3.0]
    nm = st[g[len(g) // 2]][1]
    if not tief: print(f"  Brücke {nm:28s} km {k[g[0]] / 1000:6.2f}: Modell ohne Senke (Geländemodell höchstens {e_lo - raw[a0:b0 + 1].min():.1f} m unter den Enden)"); continue
    a, b = min(tief), max(tief)
    # an den Enden weiter, solange das Oberflächenmodell noch mehr als 0,5 m über dem Geländemodell liegt (Böschung zum Fluss)
    while a > 0 and dsm[a - 1] - raw[a - 1] > 0.5 and dsm[a - 1] < e_hi + 3.0: a -= 1
    while b < len(h) - 1 and dsm[b + 1] - raw[b + 1] > 0.5 and dsm[b + 1] < e_hi + 3.0: b += 1
    h[a:b + 1] = dsm[a:b + 1]
    print(f"  Brücke {nm:28s} km {k[a] / 1000:6.2f}-{k[b] / 1000:6.2f}: Geländemodell bis {raw[a:b + 1].min():.1f} m, Fahrbahn (Oberflächenmodell) "
          f"{dsm[a]:.1f} -> {dsm[a:b + 1].max():.1f} -> {dsm[b]:.1f} m; Enden davor/danach {raw[a - 1]:.1f} / {raw[b + 1]:.1f} m")
    regions.append({"a": float(k[a - 1]), "b": float(k[b + 1]), "kind": "Brücke", "name": nm, "deck": True,
                    "ha": float(raw[a - 1]), "hb": float(raw[b + 1]), "extrem": float(raw[a:b + 1].min())})
# Unterführungen: Straßen im Tunnel (layer < 0), wo das Modell mehr als 1,5 m über der Geraden zwischen den Enden liegt
tu = [i for i, q in enumerate(st) if q[4] == "yes" and str(q[5]).startswith("-") and q[6] in STRASSE]
for _, g in groupby(enumerate(tu), key=lambda t: t[1] - t[0]):
    g = [x[1] for x in g]; a, b = g[0] - 1, g[-1] + 1
    line = h[a] + (h[b] - h[a]) * (np.arange(a, b + 1) - a) / (b - a)
    ueber = (h[a:b + 1] - line).max(); nm = st[g[0]][1]
    print(f"  Tunnel {nm:28s} km {k[a] / 1000:6.2f}-{k[b] / 1000:6.2f} ({s[b] - s[a]:.0f} m): Modell bis {ueber:.1f} m über der Geraden {h[a]:.1f} -> {h[b]:.1f} m"
          + (" -> geschätzt" if ueber > 1.5 else ""))
    if ueber > 1.5:
        regions.append({"a": float(k[a]), "b": float(k[b]), "kind": "Unterführung", "name": nm + " (unter der Bahn)", "ha": float(h[a]), "hb": float(h[b]),
                        "extrem": float(h[a:b + 1].max())})
        h[a:b + 1] = line
# übrige Stufen > 1,5 m auf 10 m (nur Ausgabe)
dd = np.diff(h)
print("übrige Stufen > 1,5 m auf 10 m:", [(round(k[i] / 1000, 2), round(float(v), 1)) for i, v in enumerate(dd) if abs(v) > 1.5])
for o in regions:
    print(f"km {o['a']/1000:6.2f}-{o['b']/1000:6.2f} {o['b']-o['a']:5.0f} m  {o['kind']:12s} {o['name']:34s} {o['ha']:6.1f} -> {o['hb']:6.1f}  (im Modell {o['extrem']:6.1f})")
json.dump({"s": s.tolist(), "k": k.tolist(), "h": h.tolist(), "raw": raw.tolist(), "regions": regions}, open("clean.json", "w"), ensure_ascii=False)
