# Brücken, Unterführungen und Lücken im Höhenprofil -> clean.json. Das AHN-DTM ist ein Geländemodell aus Bodenpunkten: Auf
# Brücken über Grachten und Kanäle hat es keine Punkte (Lücke) oder fällt zum Wasser ab, unter Viadukten, Bahnbrücken, im
# Rijksmuseum und unter der Tribüne des Stadions fehlt der Boden ebenfalls (Lücke). Die Rampen davor misst es.
# 1. Brücken aus OSM (bridge=yes auf den Wegen der Linie, strassen.json): Enden oben auf den Rampen (höchster gemessener Punkt bis
#    50 m außerhalb; an den Widerlagern trifft die Linie sonst oft die Uferkante), Fahrbahn gerade gezogen, wo innen eine Lücke ist oder das Modell mehr als 0,3 m unter der Geraden liegt.
# 2. Übrige Lücken: gerade zwischen den gemessenen Enden. Art nach OSM und Oberflächenmodell (dsm_05m, in dgm.py nur in den
#    Lücken gelesen): Tunnel bzw. Passage laut OSM; „Unterführung“, wo das DSM mehr als 2,5 m über den Enden liegt (Viadukt,
#    Bahn, Tribüne darüber); sonst „Brücke“ (Fahrbahn über Wasser ohne Brückenkennung am Weg der Linie). Lücken von einem Punkt
#    (10 m) werden ohne Kennzeichnung überbrückt.
# 3. einzelne Stufen über 1,0 m je 10 m an Widerlagern (Uferkanten) gerade gezogen, übrige über 1,5 m als Rampe, siehe unten.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official
r = json.load(open("dgm2026_10m.json"))
s = np.array([x[0] for x in r]); k = official(s)
raw = np.array([np.nan if x[3] is None else x[3] for x in r], float)
dsm = np.array([np.nan if x[4] is None else x[4] for x in r], float)
st = json.load(open("strassen.json"))
def at(i): return st[min(len(st) - 1, i)]
h = raw.copy(); est = np.zeros(len(h), bool); art = {}; name = {}
# 1. OSM-Brücken
br = np.array([bool(at(i)[2]) for i in range(len(h))])
i = 0
while i < len(h):
    if not br[i]: i += 1; continue
    j = i
    while j + 1 < len(h) and br[j + 1]: j += 1
    lo_, hi_ = max(0, i - 5), min(len(h) - 1, j + 5)
    cand_a = [q for q in range(lo_, i + 1) if not np.isnan(raw[q])]; cand_b = [q for q in range(j, hi_ + 1) if not np.isnan(raw[q])]
    if cand_a and cand_b:
        a = max(cand_a, key=lambda q: raw[q]); b = max(cand_b, key=lambda q: raw[q])
        line = raw[a] + (raw[b] - raw[a]) * (np.arange(a, b + 1) - a) / max(1, b - a)
        inner = raw[a:b + 1]
        if np.isnan(inner).any() or np.nanmax(line - inner) > 0.3:
            h[a + 1:b] = line[1:-1]; est[a + 1:b] = True
            nm = next((at(q)[1] for q in range(i, j + 1) if at(q)[1]), "")
            for q in range(a + 1, b): art[q] = "Brücke"; name[q] = nm
    i = j + 1
# 2. übrige Lücken
i = 0
while i < len(h):
    if not np.isnan(h[i]): i += 1; continue
    j = i
    while j + 1 < len(h) and np.isnan(h[j + 1]): j += 1
    a, b = i - 1, j + 1
    assert a >= 0 and b < len(h), "Lücke am Rand"
    h[i:j + 1] = h[a] + (h[b] - h[a]) * (np.arange(i, j + 1) - a) / (b - a)
    if j > i:   # ab zwei Punkten gekennzeichnet
        tun = [at(q)[3] for q in range(i, j + 1) if at(q)[3]]
        nm = next((at(q)[1] for q in range(i, j + 1) if at(q)[1]), "")
        if tun: kind = "Tunnel"; nm = "Passage unter dem Rijksmuseum" if "building_passage" in tun else nm
        elif np.nanmax(np.r_[dsm[i:j + 1], -99]) > max(h[a], h[b]) + 2.5: kind = "Unterführung"
        else: kind = "Brücke"
        if nm == "Olympisch Stadion": nm = "Marathontor"
        est[a + 1:b] = True
        for q in range(a + 1, b): art[q] = kind; name[q] = nm
    i = j + 1
# 3. Stufen über 1,0 m je 10 m bis 50 m neben einem geschätzten Stück: kürzester Bereich um die Stufe, an dessen Enden die
#    Höhe wieder gleich ist (Delle aus ein bis drei Punkten, die Uferkante an einem Widerlager), gerade gezogen und dem
#    benachbarten Stück zugeschlagen. Übrige Stufen bleiben gemessen (Rampe vom Deich in den Polder in Ouderkerk).
d = np.diff(h); stufen = [q for q in range(len(d)) if abs(d[q]) > 1.0 and not est[q] and not est[q + 1] and est[max(0, q - 5):q + 7].any()]
for q in stufen:
    best = None
    for a in range(q, max(-1, q - 5), -1):
        for b in range(q + 1, min(len(h), q + 6)):
            if abs(h[b] - h[a]) > 0.6: continue
            line = h[a] + (h[b] - h[a]) * (np.arange(a, b + 1) - a) / (b - a)
            if np.abs(h[a:b + 1] - line).max() > 0.8 and (best is None or b - a < best[1] - best[0]): best = (a, b)
    if best is None: print("Stufe ohne Gegenstufe bei km", round(k[q] / 1000, 3), round(d[q], 2)); continue
    a, b = best; h[a + 1:b] = h[a] + (h[b] - h[a]) * (np.arange(a + 1, b) - a) / (b - a); est[a + 1:b] = True
    nb = next((x for x in list(range(a, max(-1, a - 4), -1)) + list(range(b, min(len(h), b + 4))) if x in art), None)
    for x in range(a + 1, b): art[x] = art[nb] if nb is not None else "Brücke"; name[x] = name[nb] if nb is not None else at(x)[1]
    print(f"Stufe bei km {k[q] / 1000:.3f} ({d[q]:+.2f} m) geglättet, km {k[a] / 1000:.3f}–{k[b] / 1000:.3f}")
# Stufen über 1,5 m je 10 m, die keine Delle sind (Ouderkerk: von der Deichstraße hinunter zur Amsteldijk Noord am Fuß des
# Damms der Oranjebaan fällt das Modell neben einer Mauer oder Böschung auf 10 m um 2,4 m): als Rampe über 50 m verteilt
d = np.diff(h)
for q in [q for q in range(len(d)) if abs(d[q]) > 1.5 and not est[q] and not est[q + 1]]:
    a, b = max(0, q - 2), min(len(h) - 1, q + 3)
    h[a + 1:b] = h[a] + (h[b] - h[a]) * (np.arange(a + 1, b) - a) / (b - a); est[a + 1:b] = True
    for x in range(a + 1, b): art[x] = "Rampe"; name[x] = at(x)[1] or at(a)[1]
    print(f"Rampe bei km {k[q] / 1000:.3f} ({d[q]:+.2f} m auf 10 m) über km {k[a] / 1000:.3f}–{k[b] / 1000:.3f} verteilt")
# benachbarte Stücke gleicher Art und gleichen Namens mit höchstens sechs gemessenen Punkten (60 m) dazwischen zusammenfassen (die
# Punkte dazwischen bleiben gemessen, das Stück wird als Ganzes gekennzeichnet; z. B. die Viadukte am Bahnhof Zuid)
i = 0
while i < len(h):
    if not est[i]: i += 1; continue
    j = i
    while j + 1 < len(h) and est[j + 1]: j += 1
    for g in range(1, 7):
        if j + 1 + g < len(h) and est[j + 1 + g] and art.get(j + 1 + g) == art.get(j) and name.get(j + 1 + g) == name.get(j):
            for x in range(j + 1, j + 1 + g): est[x] = True; art[x] = art[j]; name[x] = name[j]
            break
    i = j + 1
out, i = [], 0
while i < len(h):
    if not est[i]: i += 1; continue
    j = i
    while j + 1 < len(h) and est[j + 1] and art.get(j + 1) == art.get(i) and name.get(j + 1) == name.get(i): j += 1
    a, b = max(0, i - 1), min(len(h) - 1, j + 1)
    innen = raw[i:j + 1]
    out.append({"a": float(k[a]), "b": float(k[b]), "kind": art[i], "name": name[i], "ha": float(h[a]), "hb": float(h[b]),
                "modell_min": None if np.isnan(innen).all() else float(np.nanmin(innen)), "luecke": int(np.isnan(innen).sum()),
                "dsm_max": None if np.isnan(dsm[i:j + 1]).all() else float(np.nanmax(dsm[i:j + 1]))})
    i = j + 1
for o in out:
    print(f"km {o['a']/1000:6.2f}-{o['b']/1000:6.2f} {o['b']-o['a']:4.0f} m  {o['kind']:12s} {o['name'][:30]:30s} {o['ha']:5.2f} -> {o['hb']:5.2f}"
          f"  Lücke {o['luecke']:2d}  Modell min {'' if o['modell_min'] is None else round(o['modell_min'], 2)}  DSM max {'' if o['dsm_max'] is None else round(o['dsm_max'], 1)}")
json.dump({"k": k.tolist(), "h": h.tolist(), "raw": [None if np.isnan(v) else float(v) for v in raw], "regions": out}, open("clean.json", "w"), ensure_ascii=False)
