# Höhen bereinigen -> clean.json {k (Streckenmeter), h, raw, regions}. Grundlage DGM1 Hessen (dgm.py, alle 10 Linienmeter).
# Die Runde hat keine Brücke, aber zweimal dieselbe Unterführung: Der Alte Steinbacher Weg läuft bei km 1,03 (hin) und km 9,06
# (zurück) unter den beiden Brücken des Gießener Rings (A 485, OSM bridge=yes, layer 1; der Weg hat maxheight 4 m, am Weg steht ein
# Kreuz „A485 Tunnel Alter Steinbacher Weg“). Das DGM1 zeigt dort einen Buckel von gut 3 m (bis 169,8 m statt 166 m): Unter den
# Brücken gibt es keine Bodenpunkte, das Modell ist dort aus den Rändern der Dämme gefüllt. Das DOM1 misst die Fahrbahn der Autobahn
# (171,4–172,0 m, also gut 5,5 m über dem Weg, passt zu 4 m Durchfahrt und dem Brückenkörper). Ersetzt durch eine Gerade zwischen den
# gemessenen Enden 12 m vor der ersten und 12 m nach der zweiten Brückenachse: geschätzt, in D.bridges (schraffiert).
# Erkannt wird jede Kreuzung der Linie mit einem OSM-Weg bridge=* (Straße oder Bahn), wo das DGM mehr als 1 m über der Geraden liegt.
# Danach Kontrolle: keine Stufe über 1,5 m je 10 m (sonst Ausgabe). Muster: werkzeuge/hannover/work/clean.py.
import json
import numpy as np
from pyproj import Transformer
from common import official
T = Transformer.from_crs(4326, 25832, always_xy=True)
r = json.load(open("dgm_10m.json"))
s = np.array([x[0] for x in r]); raw = np.array([x[3] for x in r], float); dom = np.array([x[5] for x in r], float); k = official(s)
h = raw.copy(); regions = []
# Kreuzungen der Linie mit OSM-Brücken
o = json.load(open("../dl/osm_netz.json")); Nd = o["nodes"]
g = json.load(open("linie.json")); d = np.array(g["d"]); Q = np.array(g["pts"])
rx, ry = T.transform(Q[:, 1], Q[:, 0]); R = np.c_[rx, ry]
def schnitt(p1, p2, q1, q2):
    a, b = p2 - p1, q2 - q1; den = a[0] * b[1] - a[1] * b[0]
    if abs(den) < 1e-9: return None
    t = ((q1 - p1)[0] * b[1] - (q1 - p1)[1] * b[0]) / den; u = ((q1 - p1)[0] * a[1] - (q1 - p1)[1] * a[0]) / den
    return t if 0 <= t <= 1 and 0 <= u <= 1 else None
kreuz = []
for wid, (tg, refs) in o["ways"].items():
    if tg.get("bridge") in (None, "", "no") or not (tg.get("highway") or tg.get("railway")): continue
    pts = [Nd[str(x)] for x in refs if str(x) in Nd]
    if len(pts) < 2: continue
    wx, wy = T.transform([p[1] for p in pts], [p[0] for p in pts]); W = np.c_[wx, wy]
    for i in range(len(R) - 1):
        for j in range(len(W) - 1):
            t = schnitt(R[i], R[i + 1], W[j], W[j + 1])
            if t is not None:
                nm = tg.get("name", "") + (f" ({tg['ref']})" if tg.get("ref") else "")
                kreuz.append((d[i] + t * (d[i + 1] - d[i]), nm, wid))
kreuz.sort()
gruppen = []
for lm, nm, wid in kreuz:
    if gruppen and lm - gruppen[-1][-1][0] < 40: gruppen[-1].append((lm, nm, wid))
    else: gruppen.append([(lm, nm, wid)])
for gg in gruppen:
    a = int(np.floor((gg[0][0] - 12) / 10)); b = int(np.ceil((gg[-1][0] + 12) / 10))
    gerade = raw[a] + (raw[b] - raw[a]) * (np.arange(a, b + 1) - a) / (b - a)
    buckel = float((raw[a:b + 1] - gerade).max())
    nm = gg[0][1]
    print(f"Kreuzung mit Brücke {nm}: Linienmeter {gg[0][0]:.0f}–{gg[-1][0]:.0f} (km {float(official(gg[0][0]))/1000:.3f}–{float(official(gg[-1][0]))/1000:.3f}), "
          f"DGM über der Geraden bis {buckel:.2f} m, DOM-Deck bis {dom[a:b + 1].max():.2f} m")
    if buckel < 1.0: print("   kein Buckel, DGM bleibt"); continue
    h[a:b + 1] = gerade
    regions.append({"a": float(k[a]), "b": float(k[b]), "kind": "Unterführung", "name": "Unterführung A 485",
                    "ha": float(raw[a]), "hb": float(raw[b]), "extrem": float(raw[a:b + 1].max()), "deck": float(dom[a:b + 1].max())})
for o_ in regions:
    print(f"{o_['name']} km {o_['a']/1000:6.3f}–{o_['b']/1000:6.3f} ({o_['b']-o_['a']:.0f} m): {o_['ha']:.2f} -> {o_['hb']:.2f} m, "
          f"im Modell bis {o_['extrem']:.2f} m, Autobahn (DOM) {o_['deck']:.2f} m")
dd = np.diff(h)
for i in np.where(np.abs(dd) > 1.5)[0]: print(f"  Stufe bleibt: km {k[i]/1000:.2f} {h[i]:.2f} -> {h[i+1]:.2f}")
print("größte Stufe je 10 m:", round(float(np.abs(dd).max()), 2), "m bei km", round(float(k[np.argmax(np.abs(dd))]) / 1000, 2))
# Abweichung vom gleitenden Mittel über 50 m: weitere Buckel?
m = np.convolve(h, np.ones(5) / 5, mode="same")
for i in np.where(np.abs(h - m) > 0.8)[0]:
    if 2 <= i < len(h) - 2: print(f"  Buckel/Senke km {k[i]/1000:.2f}: {h[i]:.2f} m, Mittel {m[i]:.2f} m")
json.dump({"k": k.tolist(), "h": h.tolist(), "raw": raw.tolist(), "regions": regions}, open("clean.json", "w"), ensure_ascii=False)
