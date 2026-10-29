# Brücken und übrige Stufen im Höhenprofil überbrücken -> clean.json. Das Laser-Geländemodell des INEGI (Befliegung 2007) misst unter
# Brücken den Boden darunter. Brücken aus OSM (bridge=yes/viaduct auf den Kanten der Linie, strassen.json), Enden oben auf den
# Rampen (höchster Punkt bis 30 m außerhalb); gerade gezogen, wo das Modell innen mehr als 1,0 m unter oder über der Geraden liegt
# (wie Valencia; das Laser-Modell rauscht auf Brücken um ±0,7 m, z. B. Ejército Nacional km 29,3–29,6, das bleibt gemessen).
# Zwei Sonderfälle: (1) Der Start liegt auf dem Südende der Brücke der Insurgentes am Estadio Olímpico; das südliche Ende ist die
# Rampe 25 m vor dem Start (dgm_vorstart.json). (2) An der Überführung der Insurgentes über die Av. San Jerónimo (OSM-Brücke nur
# 30 m, km 0,58) misst das Laser-Modell nördlich davon unter der Rampe, 5 m tiefer als das fotogrammetrische Modell 2017, das dort
# die Rampe zeigt; beide Modelle treffen sich wieder 480 und 800 Linienmeter nach dem Start: Fahrbahn dazwischen gerade gezogen.
# Danach Stufen > 1,5 m je 10 m paarweise wie bei den anderen Strecken.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official
from namen import name as strname
r = json.load(open("dgm2026_10m.json"))
s = np.array([x[0] for x in r]); k = official(s)
raw = np.array([x[3] for x in r], float)
st = json.load(open("strassen.json"))
def street(gpx_m): return strname(st[min(len(st) - 1, int(round(gpx_m / 10)))][1]) or ""
h = raw.copy(); bad = np.zeros(len(h), bool); osm = np.zeros(len(h), bool); bname = {}; hset = {}
BRUECKE = {26529107: "Insurgentes Sur am Estadio Olímpico", 26528420: "Insurgentes Sur über die Avenida San Jerónimo",
           833370216: "Glorieta de los Insurgentes", 1339002625: "Glorieta de los Insurgentes",
           1263009799: "Paseo de la Reforma über den Circuito Interior", 1263009798: "Paseo de la Reforma über den Circuito Interior",
           1168756541: "Ejército Nacional, Überführung"}
NORD_ENDE = {26528420: 80}          # Index (10 m) des Nordendes der Rampe nördlich der Av. San Jerónimo
SUED_ENDE = {26528420: 48}          # und des Südendes: oben auf der Rampe, beide Modelle dort gleich (2288 m), bis km 0,62 eben
VOR = json.load(open("dgm_vorstart.json"))   # [−25, Höhe]
br = np.array([(o[2] in ("yes", "viaduct")) for o in st] + [False] * (len(h) - len(st)))[:len(h)]
wid = np.array([o[6] for o in st] + [0] * (len(h) - len(st)))[:len(h)]
idx = np.where(br)[0]
for grp in np.split(idx, np.where(np.diff(idx) > 1)[0] + 1) if len(idx) else []:
    a0, b0 = int(grp.min()), int(grp.max()) + 1; w = int(wid[a0])
    b = b0 + int(np.argmax(h[b0:min(len(h), b0 + 4)]))
    if w in NORD_ENDE: b = NORD_ENDE[w]
    if a0 == 0:   # Start auf der Brücke: Gerade von der Rampe vor dem Start (−25 m) bis zum Nordende
        line = VOR[1] + (h[b] - VOR[1]) * (s[:b + 1] + 25) / (s[b] + 25); a = 0
        dev = np.abs(line - h[:b + 1]).max()
        if dev > 1.0:
            osm[0:b] = True; hset.update({i: float(line[i]) for i in range(0, b)})
            for i in range(0, b): bname[i] = BRUECKE.get(w, street(s[a0]))
        print(f"  OSM-Brücke {s[a0]:6.0f}-{s[b0]:6.0f} m  {BRUECKE.get(w, '?'):45s} Abweichung {dev:4.1f} m  {'gerade' if dev > 1.0 else 'gemessen'}")
        continue
    a = max(0, a0 - 3) + int(np.argmax(h[max(0, a0 - 3):a0 + 1]))
    if w in SUED_ENDE: a = SUED_ENDE[w]
    line = h[a] + (h[b] - h[a]) * (np.arange(a, b + 1) - a) / max(1, b - a)
    dev = np.abs(line - h[a:b + 1]).max()
    if dev > 1.0:
        osm[a + 1:b] = True
        for i in range(a + 1, b): bname[i] = BRUECKE.get(w, street(s[a0]))
    print(f"  OSM-Brücke {s[a0]:6.0f}-{s[b0]:6.0f} m  {BRUECKE.get(w, '?'):45s} Abweichung {dev:4.1f} m  {'gerade' if dev > 1.0 else 'gemessen'}")
for i, v in hset.items(): h[i] = v
bad |= osm
d = np.diff(h)
steps = [(i, d[i]) for i in range(len(d)) if abs(d[i]) > 1.5 and not osm[i] and not osm[i + 1]]
def spike(i):
    """kürzester Bereich um die Stufe i, an dessen Enden die Höhe wieder gleich ist (Buckel oder Delle ohne Gegenstufe)"""
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
for a, b in regions: bad[a + 1:b] = True; print(f"  Stufe bei {s[a]:6.0f} m ({street(s[a])}), bereinigt bis {s[b]:6.0f} m")
def edges(mask):
    m = mask.copy(); i = 0
    while i < len(m):
        if not m[i]: i += 1; continue
        j = i
        while j + 1 < len(m) and m[j + 1]: j += 1
        if osm[i]: i = j + 1; continue       # Brücken nicht erweitern (Enden sind schon oben auf den Rampen)
        a = i - 1
        for _ in range(3):
            if a - 1 >= 0 and abs(h[a] - h[a-1]) > 0.6: m[a] = True; a -= 1
            else: break
        b = j + 1
        for _ in range(3):
            if b + 1 < len(m) and abs(h[b] - h[b+1]) > 0.6: m[b] = True; b += 1
            else: break
        i = b + 1
    return m
bad = edges(bad)
out, i = [], 0
while i < len(h):
    if not bad[i]: i += 1; continue
    j = i
    while j + 1 < len(h) and bad[j + 1]: j += 1
    a, b = max(0, i - 1), min(len(h) - 1, j + 1)
    inner = raw[i:j+1]
    if inner.mean() < min(raw[a], raw[b]) or osm[i:j + 1].any(): kind = "Brücke"
    else: kind = "Unterführung"
    nm = next((bname[q] for q in range(i, j + 1) if q in bname), None) or street((s[a] + s[b]) / 2)
    out.append({"a": float(k[a]) if i > 0 else 0.0, "b": float(k[b]), "kind": kind, "name": nm, "ha": float(h[a] if i > 0 else h[0]), "hb": float(raw[b]), "extrem": float(inner.min() if kind == "Brücke" else inner.max())})
    i = j + 1
good = ~bad
for i_, v in hset.items(): good[i_] = True    # Start: Fahrbahnhöhe der geraden Brücke als Stützwert
hc = np.interp(np.arange(len(h)), np.where(good)[0], np.where(good, h, 0)[good])
for o in out:
    print(f"km {o['a']/1000:6.2f}-{o['b']/1000:6.2f} {o['b']-o['a']:5.0f} m  {o['kind']:12s} {o['name']:45s} {o['ha']:7.1f} -> {o['hb']:7.1f}  (im Modell {o['extrem']:7.1f})")
json.dump({"k": k.tolist(), "h": hc.tolist(), "raw": raw.tolist(), "regions": out}, open("clean.json", "w"), ensure_ascii=False)
