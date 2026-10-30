# Brücken und übrige Stufen im Höhenprofil überbrücken -> clean.json. Das Geländemodell der Stadt Wien enthält keine Brücken
# („Brücken werden als Kunstbauten betrachtet“, Produktinformation der MA 41): Auf der Reichsbrücke misst es Donau, Donauinsel
# und Neue Donau, auf den Brücken über Donaukanal und Wienfluss Ufer und Wasser darunter (bis 15 m tiefer).
# Brücken aus OSM (bridge=yes auf der Linie, Straßen), Enden oben auf den Rampen (höchster gemessener Punkt bis 30 m außerhalb),
# gerade gezogen, wo das Modell innen mehr als 0,5 m unter der Geraden liegt. Ausnahme Reichsbrücke (830 m): Ihre Fahrbahn steigt
# zur Mitte über dem Hauptstrom gut 5 m an (Oberflächenmodell des BEV, dsm.py, glatt von 171 auf 176 m bei km 0,8; das Höhenbild
# des Veranstalters zeigt dort denselben Buckel). Dort gilt das Oberflächenmodell, an den Enden auf das Geländemodell gesetzt; die
# Brücke zählt dann als gemessen (nicht schraffiert, wie gemessene Brücken in Rom und Valencia; die App zieht die Schraffur und den
# Strich einer geschätzten Brücke gerade von Ende zu Ende und würde den Buckel durchschneiden).
# Auf den kurzen Brücken über Donaukanal und Wienfluss liegt es höchstens 1,5 m über der Geraden (nur Ausgabe). Danach übrige Stufen > 1,5 m auf 10 m paarweise wie
# bei den anderen Strecken. Unterführungen (die Strecke läuft unter Bahn- und Straßenbrücken durch) misst das Modell am Boden.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official
from pyproj import Transformer
from scipy.spatial import cKDTree
r = json.load(open("dgm2026_10m.json"))
s = np.array([x[0] for x in r]); k = official(s)
raw = np.array([x[3] for x in r], float)
streets = [[o[0], o[1]] for o in json.load(open("strassen.json"))]
def street(gpx_m):
    best = streets[0]
    for e in streets:
        if e[0] <= gpx_m + 5: best = e
    return best[1]
h = raw.copy(); bad = np.zeros(len(h), bool); osm = np.zeros(len(h), bool)
T = Transformer.from_crs(4326, 31256, always_xy=True)
gx, gy = T.transform([x[2] for x in r], [x[1] for x in r]); baum = cKDTree(np.c_[gx, gy])
bname = {}
# Punkte der Linie auf einer OSM-Brücke (bis 12 m neben dem Brückenweg, Wege alle 2 m); Brücken aus mehreren OSM-Wegen
# (Aspernbrücke, Franzensbrücke) werden zu einem Stück
auf, bn = np.zeros(len(h), bool), {}
for w in json.load(open("../dl/osm_wege.json"))["elements"]:
    tg = w.get("tags", {}); hw = tg.get("highway")
    if tg.get("bridge") in (None, "no") or not hw or hw in ("footway", "steps", "cycleway", "path", "pedestrian", "corridor", "bridleway", "track"): continue
    wx, wy = T.transform([q["lon"] for q in w["geometry"]], [q["lat"] for q in w["geometry"]])
    lw = np.r_[0, np.cumsum(np.hypot(np.diff(wx), np.diff(wy)))]; t = np.arange(0, lw[-1] + 2, 2.0)   # alle 2 m
    dd, ii = baum.query(np.c_[np.interp(t, lw, wx), np.interp(t, lw, wy)]); ii = np.unique(ii[dd < 12])
    if len(ii) < 3: continue   # quer darüber (Unterführung), nicht entlang
    auf[ii] = True
    for q in ii: bn[q] = tg.get("bridge:name") or tg.get("name") or ""
idx = np.where(auf)[0]
for grp in np.split(idx, np.where(np.diff(idx) > 3)[0] + 1):
    if len(grp) < 2: continue
    a0, b0 = int(grp.min()), int(grp.max())
    # Enden: höchster gemessener Punkt bis 30 m vor der OSM-Brücke (oben auf der Rampe), dann weiter hinein, solange das Modell
    # noch auf dem Damm steigt (Reichsbrücke: OSM beginnt 40 m vor dem Widerlager)
    a = max(0, a0 - 3) + int(np.argmax(h[max(0, a0 - 3):a0 + 1])); b = b0 + int(np.argmax(h[b0:min(len(h), b0 + 4)]))
    while a + 1 < b0 and -0.05 <= h[a + 1] - h[a] < 1.5: a += 1
    while b - 1 > a0 and -0.05 <= h[b - 1] - h[b] < 1.5: b -= 1
    line = h[a] + (h[b] - h[a]) * (np.arange(a, b + 1) - a) / max(1, b - a)
    tief = (line - h[a:b + 1]).max(); nm = bn[int(np.median(grp))]
    print(f"  OSM-Brücke {nm:22s} km {k[a0]/1000:6.2f}-{k[b0]/1000:6.2f}, Enden km {k[a]/1000:6.2f}-{k[b]/1000:6.2f}, Modell bis {tief:4.1f} m unter der Geraden")
    if tief > 0.5:
        osm[a + 1:b] = True
        for q in range(a + 1, b): bname[q] = nm
bad |= osm
# Unterführungen: Straßen- und Bahnbrücken, die die Linie kreuzen (die Strecke läuft darunter durch). Das Modell misst dort den
# Boden der Straße; nur zur Übersicht.
from itertools import groupby
kreuz = []
for w in json.load(open("../dl/osm_wege.json"))["elements"]:
    tg = w.get("tags", {})
    if tg.get("bridge") in (None, "no") or len(w.get("geometry") or []) < 2: continue
    wx, wy = T.transform([q["lon"] for q in w["geometry"]], [q["lat"] for q in w["geometry"]])
    lw = np.r_[0, np.cumsum(np.hypot(np.diff(wx), np.diff(wy)))]; t = np.arange(0, lw[-1] + 1, 1.0)
    dd, ii = baum.query(np.c_[np.interp(t, lw, wx), np.interp(t, lw, wy)])
    nah = ii[dd < 4]
    if len(nah) and len(np.unique(nah)) <= 3 and not osm[nah].any():   # quer zur Linie, nicht entlang
        kreuz.append((round(float(k[int(np.median(nah))]) / 1000, 2), tg.get("name") or tg.get("bridge:name") or "", tg.get("railway") or tg.get("highway"), round(float(raw[int(np.median(nah))]), 1)))
print("Unterführungen (Brücke über der Linie, gemessen):")
for g_, grp in groupby(sorted(set(kreuz)), key=lambda q: round(q[0], 1)): print("  ", list(grp))
d = np.diff(h)
steps = [(i, d[i]) for i in range(len(d)) if abs(d[i]) > 1.5 and not osm[i] and not osm[i + 1]]
print("übrige Stufen > 1,5 m:", [(round(k[i] / 1000, 2), round(float(v), 1)) for i, v in steps])
def spike(i):
    best = None
    for a in range(i, max(-1, i - 9), -1):
        for b in range(i + 1, min(len(h), i + 10)):
            if abs(h[b] - h[a]) > 0.6: continue
            line = h[a] + (h[b] - h[a]) * (np.arange(a, b + 1) - a) / (b - a)
            if np.abs(h[a:b+1] - line).max() > 1.2 and (best is None or b - a < best[1] - best[0]): best = (a, b)
    return best or (max(0, i - 5), min(len(h) - 1, i + 6))
regions, used = [], set()
for n, (i, di) in enumerate(steps):
    if i in used: continue
    partner = None
    for j, dj in steps[n+1:]:
        if (k[j] - k[i]) > 600: break
        if np.sign(dj) != np.sign(di) and j not in used: partner = j; break
    if partner is not None: regions.append((i, partner + 1)); used |= {i, partner}
    else: regions.append(spike(i)); used.add(i)
for a, b in regions: bad[a + 1:b] = True
out, i = [], 0
while i < len(h):
    if not bad[i]: i += 1; continue
    j = i
    while j + 1 < len(h) and bad[j + 1]: j += 1
    a, b = max(0, i - 1), min(len(h) - 1, j + 1)
    inner = raw[i:j+1]
    kind = "Brücke" if (inner.mean() < min(raw[a], raw[b]) or osm[i:j + 1].any()) else "Unterführung"
    nm = next((bname[q] for q in range(i, j + 1) if q in bname), None) or street((s[a] + s[b]) / 2)
    out.append({"a": float(k[a]), "b": float(k[b]), "kind": kind, "name": nm, "ha": float(raw[a]), "hb": float(raw[b]), "extrem": float(inner.min() if kind == "Brücke" else inner.max())})
    i = j + 1
good = ~bad
hc = np.interp(np.arange(len(h)), np.where(good)[0], h[good])
DSM_BRUECKEN = {"Reichsbrücke"}
dsm = {int(i): v for i, v in json.load(open("dsm_10m.json")).items() if v is not None}
for o in out:
    a = int(np.argmin(np.abs(k - o["a"]))); b = int(np.argmin(np.abs(k - o["b"])))
    if not all(i in dsm for i in range(a, b + 1)): print("  ohne Oberflächenmodell:", o["name"]); continue
    f = (np.arange(a, b + 1) - a) / (b - a)
    deck = np.array([dsm[i] for i in range(a, b + 1)]) - ((dsm[a] - hc[a]) * (1 - f) + (dsm[b] - hc[b]) * f)
    m = int(np.argmax(deck - hc[a:b + 1]))
    print(f"  {o['name']:16s} Oberflächenmodell höchstens {deck[m] - hc[a + m]:+.1f} m über der Geraden (km {k[a + m] / 1000:.2f}), an den Enden "
          f"{dsm[a] - hc[a]:+.1f} / {dsm[b] - hc[b]:+.1f} m über dem Geländemodell" + (" -> übernommen" if o["name"] in DSM_BRUECKEN else ""))
    o["dsm"] = round(float(deck[m] - hc[a + m]), 1)
    if o["name"] in DSM_BRUECKEN: hc[a:b + 1] = deck; o["deck"] = True
for o in out:
    print(f"km {o['a']/1000:6.2f}-{o['b']/1000:6.2f} {o['b']-o['a']:5.0f} m  {o['kind']:12s} {o['name']:24s} {o['ha']:6.1f} -> {o['hb']:6.1f}  (im Modell {o['extrem']:6.1f})")
json.dump({"k": k.tolist(), "h": hc.tolist(), "raw": raw.tolist(), "regions": out}, open("clean.json", "w"), ensure_ascii=False)
