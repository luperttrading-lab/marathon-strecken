# Brücken, Unterführung und übrige Stufen im Höhenprofil -> clean.json. Grundlage dgm2026_10m.json (TINITALY, an die Höhen der Regione
# Lazio angeglichen, angleich.py). Auf den Brücken der Strecke liegen dort schon Passpunkte auf der Fahrbahn (DBGT 2014, „Ponte viadotto
# e cavalcavia“); gerade gezogen wird eine OSM-Brücke (bridge=yes auf der Linie, Enden oben auf den Rampen) nur, wo das Profil innen
# mehr als 1,0 m unter der Geraden liegt (wie Valencia und Mexiko-Stadt).
# Unterführung: der „Sottopasso di Ripetta“ (Liste des Veranstalters) = die Unterführungen der Hauptfahrbahn des Lungotevere Arnaldo da
# Brescia (OSM tunnel=yes, layer −1, mit kurzen offenen Stücken dazwischen). Ein Geländemodell kennt den Boden darin nicht, und die
# Regione Lazio hat dort keine Passpunkte: von Portal zu Portal gerade gezogen und als geschätzt markiert; die Tiefe (einige Meter
# hinunter und wieder hinauf) fehlt im Profil. Kurze Durchfahrten unter Bahnbrücken (OSM tunnel=passage, Via Portuense km 8) bleiben.
# Danach Stufen > 1,5 m je 10 m paarweise wie bei den anderen Strecken.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official
from namen import name as strname
r = json.load(open("dgm2026_10m.json"))
s = np.array([x[0] for x in r]); k = official(s)
raw = np.array([x[3] for x in r], float)
st = json.load(open("strassen.json"))
def street(gpx_m):
    o = st[min(len(st) - 1, int(round(gpx_m / 10)))]; return strname(o[1], o[7]) or ""
h = raw.copy(); bad = np.zeros(len(h), bool); est = np.zeros(len(h), bool); bname = {}; bkind = {}
n = min(len(h), len(st))
br = np.zeros(len(h), bool); br[:n] = [bool(o[2]) and o[2] != "no" for o in st[:n]]
tu = np.zeros(len(h), bool); tu[:n] = [o[3] in ("yes", "building_passage") for o in st[:n]]
BRUECKE = {"Ponte Vittorio Emanuele Secondo": "Ponte Vittorio Emanuele II", "Ponte della Musica Armando Trovajoli": "Ponte della Musica"}
def gruppen(m, luecke):
    idx = np.where(m)[0]
    return np.split(idx, np.where(np.diff(idx) > luecke)[0] + 1) if len(idx) else []
for g in gruppen(br, 2):
    a0, b0 = int(g.min()), int(g.max()) + 1
    a = max(0, a0 - 3) + int(np.argmax(h[max(0, a0 - 3):a0 + 1])); b = b0 + int(np.argmax(h[b0:min(len(h), b0 + 4)]))
    line = h[a] + (h[b] - h[a]) * (np.arange(a, b + 1) - a) / max(1, b - a)
    dev = (line - h[a:b + 1]).max(); nm = BRUECKE.get(st[a0][1], st[a0][1])
    if dev > 1.0:
        h[a:b + 1] = line; est[a + 1:b] = True
        for i in range(a + 1, b): bname[i] = nm; bkind[i] = "Brücke"
    print(f"  Brücke km {k[a0] / 1000:6.2f}–{k[b0] / 1000:6.2f} {nm:32s} Fahrbahn {h[a0]:5.1f}–{h[(a0 + b0) // 2]:5.1f} m, unter der Geraden {dev:4.1f} m  {'gerade gezogen' if dev > 1.0 else 'gemessen (DBGT)'}")
for g in gruppen(tu, 10):    # Unterführungen mit offenen Stücken bis 100 m dazwischen als ein Stück
    a, b = max(0, int(g.min()) - 2), min(len(h) - 1, int(g.max()) + 3)
    h[a:b + 1] = h[a] + (h[b] - h[a]) * (np.arange(a, b + 1) - a) / (b - a); est[a + 1:b] = True
    nm = "Sottopasso di Ripetta" if "Arnaldo" in st[int(g.min())][1] else street(s[int(g.min())])
    for i in range(a + 1, b): bname[i] = nm; bkind[i] = "Unterführung"
    print(f"  Unterführung km {k[a] / 1000:6.2f}–{k[b] / 1000:6.2f} {nm}: gerade von {h[a]:.1f} auf {h[b]:.1f} m")
bad |= est
d = np.diff(h)
steps = [(i, d[i]) for i in range(len(d)) if abs(d[i]) > 1.5 and not est[i] and not est[i + 1]]
def spike(i):
    best = None
    for a in range(i, max(-1, i - 9), -1):
        for b in range(i + 1, min(len(h), i + 10)):
            if abs(h[b] - h[a]) > 0.6: continue
            line = h[a] + (h[b] - h[a]) * (np.arange(a, b + 1) - a) / (b - a)
            if np.abs(h[a:b+1] - line).max() > 1.2 and (best is None or b - a < best[1] - best[0]): best = (a, b)
    return best or (max(0, i - 5), min(len(h) - 1, i + 6))
regions, used = [], set()
for nn_, (i, di) in enumerate(steps):
    if i in used: continue
    partner = None
    for j, dj in steps[nn_ + 1:]:
        if (k[j] - k[i]) > 600: break
        if np.sign(dj) != np.sign(di) and j not in used: partner = j; break
    if partner is not None: regions.append((i, partner + 1)); used |= {i, partner}
    else: regions.append(spike(i)); used.add(i)
for a, b in regions: bad[a + 1:b] = True; print(f"  Stufe bei km {k[a] / 1000:.2f} ({street(s[a])}), bereinigt bis km {k[b] / 1000:.2f}")
out, i = [], 0
while i < len(h):
    if not bad[i]: i += 1; continue
    j = i
    while j + 1 < len(h) and bad[j + 1]: j += 1
    a, b = max(0, i - 1), min(len(h) - 1, j + 1)
    kind = next((bkind[q] for q in range(i, j + 1) if q in bkind), None) or ("Brücke" if raw[i:j + 1].mean() < min(raw[a], raw[b]) else "Unterführung")
    nm = next((bname[q] for q in range(i, j + 1) if q in bname), None) or street((s[a] + s[b]) / 2)
    out.append({"a": float(k[a]), "b": float(k[b]), "kind": kind, "name": nm, "ha": float(h[a]), "hb": float(h[b]), "extrem": float(raw[i:j + 1].min() if kind == "Brücke" else raw[i:j + 1].max())})
    i = j + 1
good = ~bad | est
hc = np.interp(np.arange(len(h)), np.where(good)[0], h[good])
for o in out: print(f"km {o['a'] / 1000:6.2f}-{o['b'] / 1000:6.2f} {o['b'] - o['a']:5.0f} m  {o['kind']:12s} {o['name']:28s} {o['ha']:5.1f} -> {o['hb']:5.1f}  (Modell {o['extrem']:5.1f})")
json.dump({"k": k.tolist(), "h": hc.tolist(), "raw": raw.tolist(), "regions": out}, open("clean.json", "w"), ensure_ascii=False)
