# Brücken, Unterführungen und übrige Stufen im Höhenprofil -> clean.json. Grundlage dgm2026_10m.json (FABDEM, 1″-Raster).
# Brücken aus OSM (bridge=yes auf der Linie, strassen.json; Enden oben auf den Rampen, je bis 30 m außerhalb): gerade gezogen nur,
# wo das Modell innen mehr als 1,0 m unter der Geraden liegt (wie Valencia, Rom). Auf der Strecke liegen vier Brücken der Leoforos
# Marathonos: über zwei Bäche bei km 13,2 und 18,7, über den Valanaris bei km 20,3 und bei km 28,3 in Pallini über die Attiki Odos und
# die Flughafenbahn, die dort im Einschnitt liegen. Die Bachbrücken sind kurz (10–40 m), das 30-m-Raster misst die Fahrbahn.
# Unterführungen (OSM tunnel=yes auf der Linie): am Knoten Stavros (km 30,6, unter der A621) und an der Katechaki (km 37,3, unter der
# Brücke der Katechaki); FABDEM zeigt dort keinen Buckel der Brücke darüber und keine Senke, sondern die gleichmäßige Steigung bzw. das
# Gefälle der Straße. Sie bleiben gemessen; ob die Fahrbahn unter den Brücken tiefer gelegt ist, verrät ein 30-m-Modell nicht.
# Innenstadt Athen (ab km 38,3, Michalakopoulou bis Ziel): Dort zeigt FABDEM an den Häuserblöcken Stufen und Buckel bis 10 m (die
# Gebäude sind im 30-m-Raster nicht ganz herausgerechnet; Copernicus zeigt sie noch stärker), z. B. 6 m Stufe auf der Vasilissis
# Sofias bei km 39,4 und 10 m Buckel am Kriegsmuseum bei km 41,2, wo die Straße eben ist. Dieser Abschnitt wird robust geglättet:
# lokal gewichtete Ausgleichsgerade über ±250 m (LOWESS, Tricube-Gewichte, drei Runden mit Bisquare-Gewichten gegen Ausreißer).
# Auf den übrigen 38 km gibt es keine Stufe über 1,5 m je 10 m.
# Danach Stufen > 1,5 m je 10 m paarweise wie bei den anderen Strecken.
import json, numpy as np
from common import official
r = json.load(open("dgm2026_10m.json"))
s = np.array([x[0] for x in r]); k = official(s)
raw = np.array([x[3] for x in r], float)
st = json.load(open("strassen.json"))
def street(gpx_m):
    o = st[min(len(st) - 1, int(round(gpx_m / 10)))]; return o[2] or ""
h = raw.copy(); bad = np.zeros(len(h), bool); est = np.zeros(len(h), bool); bname = {}; bkind = {}
n = min(len(h), len(st))
br = np.zeros(len(h), bool); br[:n] = [o[3] not in ("", "no") for o in st[:n]]
tu = np.zeros(len(h), bool); tu[:n] = [o[4] not in ("", "no") for o in st[:n]]
UEBER = {13: "Leoforos Marathonos über einen Bach", 18: "Leoforos Marathonos über den Rema Agias Paraskevis",
         20: "Leoforos Marathonos über den Valanaris", 28: "Leoforos Marathonos über die Attiki Odos"}
def gruppen(m, luecke):
    idx = np.where(m)[0]
    return np.split(idx, np.where(np.diff(idx) > luecke)[0] + 1) if len(idx) else []
for g in gruppen(br, 2):
    a0, b0 = int(g.min()), int(g.max()) + 1
    a = max(0, a0 - 3) + int(np.argmax(h[max(0, a0 - 3):a0 + 1])); b = b0 + int(np.argmax(h[b0:min(len(h), b0 + 4)]))
    line = h[a] + (h[b] - h[a]) * (np.arange(a, b + 1) - a) / max(1, b - a)
    dev = (line - h[a:b + 1]).max(); nm = UEBER.get(int(k[a0] // 1000), "Brücke")
    if dev > 1.0:
        h[a:b + 1] = line; est[a + 1:b] = True
        for i in range(a + 1, b): bname[i] = nm; bkind[i] = "Brücke"
    print(f"  Brücke km {k[a0] / 1000:6.2f}–{k[b0] / 1000:6.2f} ({(b0 - a0) * 10} m) {nm:40s} Modell {raw[a0:b0 + 1].min():6.1f}–{raw[a0:b0 + 1].max():6.1f} m, unter der Geraden {dev:4.1f} m  {'gerade gezogen' if dev > 1.0 else 'gemessen'}")
for g in gruppen(tu, 3):
    a0, b0 = int(g.min()), int(g.max()) + 1
    q = raw[max(0, a0 - 5):b0 + 6]; lin = np.linspace(q[0], q[-1], len(q))
    print(f"  Unterführung km {k[a0] / 1000:6.2f}–{k[b0] / 1000:6.2f} ({(b0 - a0) * 10} m) {street(s[a0])}: Modell {raw[a0]:.1f} -> {raw[b0]:.1f} m, größte Abweichung von der Geraden ±60 m {np.abs(q - lin).max():.1f} m, gemessen")
bad |= est
STADT = 38300.0
def lowess(x, y, hw, runden=3):
    w_rob = np.ones_like(y); out = y.copy()
    for _ in range(runden + 1):
        for i in range(len(x)):
            dd = np.abs(x - x[i]); m = dd < hw; ww = (1 - (dd[m] / hw) ** 3) ** 3 * w_rob[m]
            X = np.c_[np.ones(m.sum()), x[m] - x[i]]
            out[i] = np.linalg.lstsq(X.T @ (X * ww[:, None]), X.T @ (y[m] * ww), rcond=None)[0][0]
        res = y - out; sres = np.median(np.abs(res)) * 6 or 1; u = res / sres; w_rob = np.where(np.abs(u) < 1, (1 - u ** 2) ** 2, 0)
    return out
sel = k >= STADT - 250
glatt = lowess(k[sel], h[sel], 250.0)
ueber = np.clip((k[sel] - (STADT - 250)) / 250, 0, 1)        # weicher Übergang auf den ersten 250 m
vorher = h[sel].copy(); h[sel] = vorher * (1 - ueber) + glatt * ueber
print(f"  Innenstadt ab km {STADT / 1000:.1f} geglättet: Abweichung vom Modell bis {np.abs(h[sel] - vorher).max():.1f} m, Median {np.median(np.abs(h[sel] - vorher)):.1f} m")
d = np.diff(h)
steps = [(i, d[i]) for i in range(len(d)) if abs(d[i]) > 1.5 and not est[i] and not est[i + 1] and k[i] < STADT - 250]
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
print("  Stufen > 1,5 m je 10 m:", len(steps))
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
for o in out: print(f"km {o['a'] / 1000:6.2f}-{o['b'] / 1000:6.2f} {o['b'] - o['a']:5.0f} m  {o['kind']:12s} {o['name']:28s} {o['ha']:6.1f} -> {o['hb']:6.1f}  (Modell {o['extrem']:6.1f})")
json.dump({"k": k.tolist(), "h": hc.tolist(), "raw": raw.tolist(), "regions": out}, open("clean.json", "w"), ensure_ascii=False)
