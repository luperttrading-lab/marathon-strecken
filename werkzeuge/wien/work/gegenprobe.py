# Gegenprobe mit dem privaten Datensatz (course_segments.parquet, city == "Vienna": Höhenmeter je 5-km-Abschnitt aus dem GPX des
# Veranstalters mit dessen eingebetteten Höhen, Schwelle 1 m auf Punkten alle ~100 m). Liest nur diese Datei, schreibt nichts
# dorthin. Eigene Werte zweimal: wie in der App (Steigung über 200 m, alle 10 m summiert) und wie der Datensatz (alle 100 m,
# Schwelle 1 m). Aufruf: python3 gegenprobe.py <Ordner des Exports>/course_segments.parquet
import json, sys, numpy as np, pandas as pd
P = sys.argv[1]
seg = pd.read_parquet(P); seg = seg[seg.city == "Vienna"].sort_values("seg_from_km")
D = json.load(open("data.json")); h = np.array(D["h"]) / 100; L = D["len"]; g = np.arange(len(h)) * 10.0
def at(x): return np.interp(x, g, h)
def app(a, b, w=200):
    xs = np.arange(a, b + 1e-6, 10.0); gr = (at(np.minimum(xs + w / 2, L)) - at(np.maximum(xs - w / 2, 0))) / (np.minimum(xs + w / 2, L) - np.maximum(xs - w / 2, 0))
    dh = (gr[1:] + gr[:-1]) / 2 * 10; return dh[dh > 0].sum(), -dh[dh < 0].sum()
def schwelle(a, b, step=100, thr=1.0):
    xs = np.append(np.arange(a, b, step), b); v = at(xs); auf = ab = 0.0; ref = v[0]
    for y in v[1:]:
        if y - ref >= thr: auf += y - ref; ref = y
        elif ref - y >= thr: ab += ref - y; ref = y
    return auf, ab
print("| Abschnitt | Datensatz ↑/↓ | App 200 m ↑/↓ | 100 m + 1-m-Schwelle ↑/↓ | Datensatz min–max | App min–max |")
print("|---|---|---|---|---|---|")
S = np.zeros(6)
for _, r in seg.iterrows():
    a, b = r.seg_from_km * 1000, min(r.seg_to_km * 1000, L); u, d = app(a, b); u2, d2 = schwelle(a, b); sel = (g >= a) & (g <= b)
    S += [r.elev_gain_m, r.elev_loss_m, u, d, u2, d2]
    print(f"| {r.seg_from_km:g}–{r.seg_to_km:g} km | {r.elev_gain_m:.1f} / {r.elev_loss_m:.1f} | {u:.1f} / {d:.1f} | {u2:.1f} / {d2:.1f} | "
          f"{r.elev_min_m:.1f}–{r.elev_max_m:.1f} | {h[sel].min():.1f}–{h[sel].max():.1f} |")
print(f"| Summe | {S[0]:.1f} / {S[1]:.1f} | {S[2]:.1f} / {S[3]:.1f} | {S[4]:.1f} / {S[5]:.1f} | | |")
