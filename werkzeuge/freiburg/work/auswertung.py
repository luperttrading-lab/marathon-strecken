# Kennzahlen des fertigen Profils (data.json) für Übergabe und Texte: Höhenmeter je Messfenster (wie „Ganze Strecke“ in der App:
# Steigung über das Fenster, aufsummiert), wie GPS-Uhren (Hysterese 0,5 / 1 / 3 m), Höhenbereich, steilste Stellen, je 5 km.
import json
import numpy as np
D = json.load(open("data.json")); L = D["len"]; h = np.array(D["h"]) / 100; x = np.arange(len(h)) * D["step"]; sel = x <= L
def at(v): return float(np.interp(v, x, h))
def fenster(w, a=0, b=L):
    xs = x[(x >= a) & (x <= b)]
    gr = np.array([(at(min(v + w / 2, L)) - at(max(v - w / 2, 0))) / (min(v + w / 2, L) - max(v - w / 2, 0)) for v in xs])
    dh = (gr[1:] + gr[:-1]) / 2 * D["step"]
    return dh[dh > 0].sum(), -dh[dh < 0].sum(), gr, xs
for w in (50, 100, 200, 1000):
    u, dn, gr, xs = fenster(w)
    print(f"Fenster {w:5d} m: ↑ {u:5.1f} / ↓ {dn:5.1f} m; steilste bergauf {gr.max()*100:+.1f} % bei km {xs[gr.argmax()]/1000:.2f}, bergab {gr.min()*100:+.1f} % bei km {xs[gr.argmin()]/1000:.2f}")
def hyst(t):
    up = 0; ref = h[0]
    for v in h[sel]:
        if v - ref >= t: up += v - ref; ref = v
        elif ref - v >= t: ref = v
    return up
print("wie GPS-Uhren: ab 0,5 m ↑ %.0f, ab 1 m ↑ %.0f, ab 3 m ↑ %.0f" % (hyst(0.5), hyst(1), hyst(3)))
print(f"Start {h[0]:.1f} m, Ziel {at(L):.1f} m, tiefster {h[sel].min():.1f} m bei km {x[sel][h[sel].argmin()]/1000:.2f}, höchster {h[sel].max():.1f} m bei km {x[sel][h[sel].argmax()]/1000:.2f}, Bereich {h[sel].max()-h[sel].min():.1f} m")
print("je 5 km (200-m-Fenster):", "  ".join(f"{a//1000}–{min(a+5000,L)/1000:g}: {fenster(200,a,min(a+5000,L))[0]:.0f}/{fenster(200,a,min(a+5000,L))[1]:.0f}" for a in range(0, 42195, 5000)))
for a, b in ((0, 3000), (3000, 6000), (6000, 9000), (9000, 14000), (14000, 17500), (17500, 21100)):
    s = (x >= a) & (x <= b); print(f"  km {a/1000:g}–{b/1000:g}: {h[s].min():.1f}–{h[s].max():.1f} m, Anfang {at(a):.1f}, Ende {at(b):.1f}")
