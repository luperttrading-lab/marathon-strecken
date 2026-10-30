# Zeit je Mauerdurchgang aus den Zwischenzeiten 2026 -> mauer.json (Vorschlag für D.mauerMin).
# Messpunkte des Zeitnehmers (splits.py): 7,5 km (nach der ersten Mauer, auf der Festungsmauer), 22, 29, 35 km (Tor zur Mauer), Ziel.
# Je Läufer: Pace im Flachen p0 aus 7,5 → 35 km (nur Straße) mit dem Pace-Modell der App (Minetti, 1,0 s je Höhenmeter bei
# 4:00 /km, bergab „halb“, Steigung über 100 m wie RECHEN), dann
#   Mauer 1 = Zeit 0 → 7,5 km − p0 · (Straße 0 → Mauerbeginn und Mauerende → 7,5 km, nach Modell),
#   Mauer 2 = Zeit 35 → Ziel − p0 · (Straße 35 km → Mauerbeginn und Mauerende → Ziel, nach Modell).
# Grenzen der Durchgänge aus data.json (D.mauer). Müdigkeit am Ende (km 37–42 bergab) steckt in Mauer 2 mit drin; die Lage der
# Matte „7,5 km“ ist nicht veröffentlicht (angenommen: offiziell km 7,5 auf der Festungsmauer; an der Ausfahrt km 8,1 wären es
# für Mauer 1 gut 3 min mehr).
import json, math
import numpy as np
D = json.load(open("data.json")); H = np.array(D["h"]) / 100; STEP = D["step"]; L = D["len"]; N = len(H)
MAUER = D["mauer"]
def hAt(x): return float(np.interp(min(max(x, 0), L), np.arange(N) * STEP, H))
g = np.array([(hAt(min(max(i * STEP + 50, 0), L)) - hAt(min(max(i * STEP - 50, 0), L))) / (min(max(i * STEP + 50, 0), L) - min(max(i * STEP - 50, 0), L)) * 100 for i in range(N)])
SEC = 1.0; DOWN = 0.5; R, W_, XM, GM = 0.5, 1, -8, 12
def minetti(i): return 155.4 * i ** 5 - 30.4 * i ** 4 - 43.3 * i ** 3 + 46.3 * i ** 2 + 19.5 * i + 3.6
def pfAuf(x): return SEC / 0.24 / (19.5 / 3.6) * (minetti(x / 100) / 3.6 - 1)
def pfAb(x):
    k = SEC; s0 = R * k / 24; tief = GM / 100 * k; h = -XM
    if x >= XM: t = (x - XM) / h; return -tief * (2 * t ** 3 - 3 * t ** 2 + 1) + s0 * h * (t ** 3 - t ** 2)
    return -tief
def paceFaktor(gi):
    x = gi * 100; d = DOWN * 2; w = W_
    unten = lambda xx: d * pfAb(xx)
    if abs(x) < w:
        e = 1e-3; sm = (SEC / 24 + d * R * SEC / 24) / 2
        if x >= 0: a, ya, ma, yb, mb = 0, 0, sm, pfAuf(w), (pfAuf(w + e) - pfAuf(w - e)) / (2 * e)
        else: a, ya, ma, yb, mb = -w, unten(-w), (unten(-w + e) - unten(-w - e)) / (2 * e), 0, sm
        t = (x - a) / w
        return 1 + (2 * t ** 3 - 3 * t ** 2 + 1) * ya + (t ** 3 - 2 * t ** 2 + t) * w * ma + (-2 * t ** 3 + 3 * t ** 2) * yb + (t ** 3 - t ** 2) * w * mb
    return 1 + (pfAuf(x) if x >= 0 else unten(x))
ratio = np.array([paceFaktor(v / 100) for v in g])
seg = (ratio[1:] + ratio[:-1]) / 2 * STEP          # gewichtete Meter je 10-m-Stück (Stück i: Punkt i … i+1)
mitte = (np.arange(N - 1) + 0.5) * STEP
auf_mauer = np.zeros(N - 1, bool)
for a, b, _ in MAUER: auf_mauer |= (mitte >= a) & (mitte < b)
def eff(a, b, ohne_mauer=True):
    sel = (mitte >= a) & (mitte < b) & (~auf_mauer if ohne_mauer else True); return seg[sel].sum() / 1000   # „flache km“
S = json.load(open("../dl/splits2026.json"))
rows = []
for pid, v in S.items():
    sp = v["split"]
    if all(k in sp for k in ("7.5", "22", "29", "35", "42.195")):
        t = [0, sp["7.5"], sp["22"], sp["29"], sp["35"], sp["42.195"]]
        if np.all(np.diff(t) > 0): rows.append(t)
A = np.array(rows, float)
E_mitte = eff(7500, 35000); E1 = eff(0, 7500); E2 = eff(35000, L)
p0 = (A[:, 4] - A[:, 1]) / E_mitte                     # s je flachem km
W1 = (A[:, 1] - p0 * E1) / 60; W2 = (A[:, 5] - A[:, 4] - p0 * E2) / 60
# zum Vergleich: was das Steigungsmodell allein auf der Mauer rechnen würde (flache km auf der Mauer · p0)
EM1 = sum(seg[(mitte >= a) & (mitte < b)].sum() for a, b, _ in MAUER[:1]) / 1000
EM2 = sum(seg[(mitte >= a) & (mitte < b)].sum() for a, b, _ in MAUER[1:]) / 1000
print(f"Modell: 7,5–35 km = {E_mitte:.2f} flache km, Straße in 0–7,5 = {E1:.2f}, in 35–Ziel = {E2:.2f}; Mauer nach Steigungsmodell {EM1:.2f} / {EM2:.2f} flache km "
      f"(Längen {MAUER[0][1] - MAUER[0][0]} / {MAUER[1][1] - MAUER[1][0]} m)")
out = {"gruppen": []}
for lo, hi in ((4.0, 4.5), (4.5, 4.75), (4.75, 5.25), (5.25, 5.5), (5.5, 6.0), (6.0, 6.5), (6.5, 7.0), (7.0, 7.5)):
    sel = (A[:, 5] >= lo * 3600) & (A[:, 5] < hi * 3600)
    if sel.sum() < 3: continue
    q = lambda v: [round(float(x), 1) for x in np.percentile(v[sel], [25, 50, 75])]
    r = {"ziel": f"{lo:g}–{hi:g} h", "n": int(sel.sum()), "p0": round(float(np.median(p0[sel])), 1), "mauer1": q(W1), "mauer2": q(W2),
         "modell1": round(float(np.median(p0[sel] * EM1 / 60)), 1), "modell2": round(float(np.median(p0[sel] * EM2 / 60)), 1)}
    out["gruppen"].append(r)
    print(f"Ziel {r['ziel']:9s} n={r['n']:3d}  Flach-Pace {int(r['p0'] // 60)}:{int(r['p0'] % 60):02d}/km  Mauer 1: {r['mauer1'][1]:5.1f} min (Hälfte {r['mauer1'][0]}–{r['mauer1'][2]})"
          f"  Mauer 2: {r['mauer2'][1]:5.1f} min (Hälfte {r['mauer2'][0]}–{r['mauer2'][2]})  Steigungsmodell allein: {r['modell1']} / {r['modell2']} min")
sel = (A[:, 5] >= 4.75 * 3600) & (A[:, 5] < 5.25 * 3600)
out["median1"] = round(float(np.median(W1[sel])), 1); out["median2"] = round(float(np.median(W2[sel])), 1); out["n"] = int(sel.sum())
# Die App rechnet mit einem Wert für beide Durchgänge: das Mittel trifft die Summe (Zielzeit); für das Tor bei km 35 liegt man damit
# um die Hälfte des Unterschieds auf der sicheren Seite (erster Durchgang tatsächlich schneller).
out["vorschlag"] = int(round((out["median1"] + out["median2"]) / 2))
# Regression über alle: Mauerzeit gegen Zielzeit
for nm, Wv in (("Mauer 1", W1), ("Mauer 2", W2)):
    ok = (A[:, 5] < 7.5 * 3600)
    k, c = np.polyfit(A[ok, 5] / 3600, Wv[ok], 1)
    print(f"{nm}: linear {c + 5 * k:.1f} min bei 5:00 Zielzeit, {k:+.1f} min je Stunde Zielzeit")
    out[nm] = {"bei5h": round(float(c + 5 * k), 1), "jeStunde": round(float(k), 1)}
json.dump(out, open("mauer.json", "w"), ensure_ascii=False, indent=1)
print("Vorschlag D.mauerMin =", out["vorschlag"], "(Mittel der Mediane beider Durchgänge bei 4:45–5:15, n =", out["n"], ")")
