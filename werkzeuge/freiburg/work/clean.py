# Höhen bereinigen -> clean.json {k (offizielle Meter), h, raw, regions}. Grundlage DGM1 Baden-Württemberg (dgm.py, alle 10 Linienmeter).
# Ein Geländemodell kennt keine Brücken und keine Unterführungen:
# - Brücken (OSM bridge=*, strassen.json): Das DGM misst darunter Wasser (Dreisam, Dorfbach, Mühlbach), Gleise (Wiwilíbrücke über den
#   Hauptbahnhof, Güterumgehungsbahn an Uffhauser und Kaiserstuhlstraße) oder die B 31a. Dort gilt die Fahrbahn aus dem Oberflächenmodell
#   DOM1 derselben Befliegung (deck.py, 25-%-Quantil 5 × 5 m), wenn das DOM über dem DGM liegt und nicht mehr als 3 m über den
#   Brückenenden (Bäume, Leuchten, Oberleitungen). Auf schmalen Stegen trifft die gezeichnete Linie nicht überall das Deck (Betzenhauser
#   Steg, Binzengrün): Dort bleibt die Höhe nicht unter der Geraden zwischen den Brückenenden; einzelne Spitzen im DOM (Leuchte, Fahrzeug)
#   werden auf den höheren Nachbarn gekappt. Gemessen, nicht geschätzt.
# - Unterführungen (OSM tunnel=yes, layer < 0, höchstens 6 m neben der Linie): Wo das DGM dort einen Buckel über 1,5 m zeigt, misst es die
#   Straße darüber: Fußgängerunterführung unter der Sundgauallee (km 3,0) und unter der Schwarzwaldstraße an der Musikhochschule
#   (km 14,0). Gerade zwischen den tiefsten gemessenen Punkten davor und danach (je 60 m): geschätzt, in D.bridges (schraffiert).
#   Ein Weg im Tunnel bei km 6,55 kreuzt die Strecke nur (sie geht dort auf einem Steg über die Güterumgehungsbahn, km 6,59, aus dem
#   DOM); unter den Gleisen an der Mathildenstraße/Kenzinger Straße (km 18,7, in OSM ohne Tunnel) zeigt das DGM keinen Buckel: wie gemessen.
# Runde 2 übernimmt die bereinigten Höhen von Runde 1 an derselben Stelle der Runde. Danach Kontrolle: Stufen über 1,5 m je 10 m. Muster: werkzeuge/hannover/work/clean.py.
import json
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
from common import official
T = Transformer.from_crs(4326, 25832, always_xy=True)
r = json.load(open("dgm2026_10m.json")); st = json.load(open("strassen.json"))
s = np.array([x[0] for x in r]); raw = np.array([x[3] for x in r], float); k = official(s)
h = raw.copy(); regions = []
def gruppen(idx):
    g = []
    for i in idx:
        if g and i - g[-1][-1] <= 3: g[-1].append(i)
        else: g.append([i])
    return g
deck = {round(a): (q, name) for a, q, _, name in json.load(open("deck.json"))}
for gg in gruppen([i for i, x in enumerate(st) if x[3] not in ("", "no")]):
    a, b = gg[0] - 1, gg[-1] + 1
    ende = max(raw[max(0, a - 2):a + 1].max(), raw[b:b + 3].max())
    n = 0
    for i in range(a, b + 1):
        q = deck.get(round(s[i]), (None,))[0]
        if q is not None and q - raw[i] > 0.3 and q < ende + 3: h[i] = q; n += 1
    for i in range(a + 1, b): h[i] = min(h[i], max(h[i - 1], h[i + 1]))   # einzelne Spitzen im DOM (Leuchte, Fahrzeug) abschneiden
    gerade = h[a] + (h[b] - h[a]) * (np.arange(a, b + 1) - a) / (b - a)
    m = h[a:b + 1] < gerade - 0.3; h[a:b + 1] = np.maximum(h[a:b + 1], gerade)
    print(f"Brücke {st[gg[0]][2] or '(ohne Namen)':24s} km {k[gg[0]]/1000:6.2f}–{k[gg[-1]]/1000:6.2f}: {n} Punkte aus dem DOM, {int(m.sum())} auf die Gerade, "
          f"DGM tiefster {raw[a:b+1].min():6.2f} m, Deck {h[a:b+1].min():6.2f}–{h[a:b+1].max():6.2f} m")
# Unterführungen
NAME = {"36331074": "Unterführung Sundgauallee", "37655557": "Unterführung Schwarzwaldstraße"}
E, N = T.transform([x[2] for x in r], [x[1] for x in r]); baum = cKDTree(np.c_[E, N])
o = json.load(open("../dl/osm_netz.json")); NO = o["nodes"]
for wid, (tg, refs) in o["ways"].items():
    if tg.get("tunnel") != "yes" or "highway" not in tg or not tg.get("layer", "0").startswith("-"): continue
    pts = [NO[str(q)] for q in refs if str(q) in NO]; x, y = T.transform([p[1] for p in pts], [p[0] for p in pts]); P = np.c_[x, y]
    dicht = [a + f * (c - a) for a, c in zip(P[:-1], P[1:]) for f in np.linspace(0, 1, max(2, int(np.hypot(*(c - a))) + 1))]
    idx = sorted(set(j for q in dicht for j in baum.query_ball_point(q, 6)))
    for gg in gruppen(idx):
        a0, b0 = gg[0], gg[-1]
        a = max(0, a0 - 6) + int(np.argmin(h[max(0, a0 - 6):a0 + 1])); b = b0 + int(np.argmin(h[b0:b0 + 7]))
        if b <= a + 1: continue
        gerade = h[a] + (h[b] - h[a]) * (np.arange(a, b + 1) - a) / (b - a)
        buckel = float((h[a:b + 1] - gerade).max())
        if buckel < 1.5: print(f"Unterführung ohne Buckel über 1,5 m: Weg {wid} km {k[a0]/1000:.2f} ({buckel:.1f} m)"); continue
        h[a:b + 1] = gerade
        regions.append({"a": float(k[a]), "b": float(k[b]), "kind": "Unterführung", "name": NAME.get(wid, ""), "ha": float(h[a]), "hb": float(h[b]), "extrem": float(raw[a:b + 1].max()), "weg": wid})
# Runde 2 ist dieselbe Strecke: Höhen aus Runde 1 an derselben Stelle der Runde (sonst unterscheiden sich die Runden nur durch die
# Lage der 10-m-Punkte, auf schmalen Brücken um bis zu 2 m). Die letzten Meter ins Ziel (nach dem Abzweig) bleiben gemessen.
S = json.load(open("strecke2026.json")); r2 = S["runde2"]; dab = S["d"][S["abzweig"]]
l1 = s <= dab; l2 = (s >= r2) & (s - r2 <= dab)
neu2 = np.interp(s[l2] - r2, s[l1], h[l1]); print(f"Runde 2 aus Runde 1: {int(l2.sum())} Punkte, Unterschied zur eigenen Messung bis {np.abs(neu2 - h[l2]).max():.2f} m, "
                                                 f"im Mittel {np.abs(neu2 - h[l2]).mean():.3f} m"); h[l2] = neu2
regions.sort(key=lambda o: o["a"])
for o_ in regions:
    print(f"Unterführung km {o_['a']/1000:6.2f}–{o_['b']/1000:6.2f} ({o_['b']-o_['a']:.0f} m): {o_['ha']:.2f} -> {o_['hb']:.2f} m, im Modell bis {o_['extrem']:.2f} m (Weg {o_['weg']})")
d = np.diff(h)
for i in np.where(np.abs(d) > 1.5)[0]: print(f"  Stufe bleibt: km {k[i]/1000:.2f} {h[i]:.2f} -> {h[i+1]:.2f}")
print("größte Stufe je 10 m:", round(float(np.abs(d).max()), 2), "m bei km", round(float(k[np.argmax(np.abs(d))]) / 1000, 2))
json.dump({"k": k.tolist(), "h": h.tolist(), "raw": raw.tolist(), "regions": regions}, open("clean.json", "w"), ensure_ascii=False)
