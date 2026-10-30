# Höhenkurve des Veranstalters (../dl/hoehe.pdf, „GWM Elevation curves_all_2026“, Vektorgrafik) -> planprofil.json [[km, m], …].
# Marathon-Diagramm oben: Kurve = Oberkante der schwarzen Umrissfläche; x-Achse von 0,0 (x = 40,7 pt) bis 42,2 (x = 825,1 pt,
# senkrechte Rahmenlinien), linear (die senkrechten Linien der Getränkestellen stehen bis auf ±0,3 km an ihren Kilometern).
# y-Achse aus den waagerechten Hilfslinien (gerastert gemessen): 500 m bei 74,69 pt … 200 m bei 195,25 pt, 0,4019 pt je Meter; die
# Linie „193 m“ liegt dazu passend bei 198,12 pt, die Linie „515 m“ bei 66,44 pt ist nur eine Marke über dem höchsten Punkt
# (sie läge linear bei 520 m). Nennwerte: 1340 m hinauf und hinab, 193–515 m.
import json
import numpy as np, pymupdf
doc = pymupdf.open("../dl/hoehe.pdf"); pg = doc[0]
DR = pg.get_drawings()
X0, X1, KM1 = 40.7, 825.1, 42.2
Y500, Y200 = 74.69, 195.25
def km(x): return (x - X0) / (X1 - X0) * KM1
def hoehe(y): return 200 + (Y200 - y) * 300 / (Y200 - Y500)
def punkte(d, step=6):
    out = []
    for it in d["items"]:
        if it[0] == "l": out += [(it[1].x, it[1].y), (it[2].x, it[2].y)]
        elif it[0] == "c":
            a, b, c, e = it[1:5]
            for t in np.linspace(0, 1, step + 1):
                out.append(((1-t)**3*a.x + 3*(1-t)**2*t*b.x + 3*(1-t)*t*t*c.x + t**3*e.x, (1-t)**3*a.y + 3*(1-t)**2*t*b.y + 3*(1-t)*t*t*c.y + t**3*e.y))
    return np.array(out)
# Umrissfläche: dunkle Füllung, größte im Marathon-Diagramm
kand = [d for d in DR if d["type"] == "f" and d.get("fill") and max(d["fill"]) < 0.2 and d["rect"].y1 < 260 and d["rect"].width > 700]
d = max(kand, key=lambda d: len(d["items"]))
P = punkte(d)
xs = np.arange(X0, X1 + 1e-6, 0.25)
oben = np.full(len(xs), np.nan)
for i, x in enumerate(xs):
    sel = np.abs(P[:, 0] - x) < 0.4
    if sel.any(): oben[i] = P[sel, 1].min()
ok = ~np.isnan(oben); oben = np.interp(xs, xs[ok], oben[ok])
prof = [[round(km(x), 3), round(hoehe(y), 1)] for x, y in zip(xs, oben)]
json.dump(prof, open("planprofil.json", "w"))
h = np.array([p[1] for p in prof]); k = np.array([p[0] for p in prof])
dh = np.diff(h)
print(f"{len(prof)} Punkte; Start {h[0]:.0f} m, Ziel {h[-1]:.0f} m, min {h.min():.0f} m bei km {k[h.argmin()]:.1f}, max {h.max():.0f} m bei km {k[h.argmax()]:.1f}")
print(f"hinauf {dh[dh > 0].sum():.0f} m, hinab {-dh[dh < 0].sum():.0f} m (Punkt für Punkt alle 0,25 pt ≈ 13 m)")
