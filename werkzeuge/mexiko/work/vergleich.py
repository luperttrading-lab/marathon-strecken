# Gegenprobe: Höhenbild „Altimetría“ im Streckenplan des Veranstalters (planprofil.json, aus planprofil.py) gegen das Profil der App
# (data.json), beide über den offiziellen Kilometern. Mittlerer Unterschied je Abschnitt und Lage der Wellen (Hoch- und Tiefpunkte).
import json, numpy as np
D = json.load(open("data.json")); h = np.array(D["h"]) / 100; x = np.arange(len(h)) * 10 / 1000
pp = np.array(json.load(open("planprofil.json")))
for a, b in ((0, 10), (10, 17), (17, 21.1), (21.1, 30), (30, 34), (34, 42)):
    m = (pp[:, 0] >= a) & (pp[:, 0] <= b); dd = pp[m, 1] - np.interp(pp[m, 0], x, h)
    print(f"km {a:4.1f}–{b:4.1f}: Plan minus App im Mittel {dd.mean():+5.1f} m (min {dd.min():+5.1f}, max {dd.max():+5.1f})")
def extrema(k, v, fenster):
    out = []
    for i in range(len(k)):
        sel = np.abs(k - k[i]) <= fenster
        if v[i] == v[sel].max(): out.append(("Hoch", round(float(k[i]), 1), round(float(v[i]))))
        if v[i] == v[sel].min(): out.append(("Tief", round(float(k[i]), 1), round(float(v[i]))))
    return out
print("Plan:", [e for e in extrema(pp[:, 0], pp[:, 1], 1.2) if 17 < e[1] < 35])
print("App: ", [e for e in extrema(x[::10], h[::10], 1.2) if 17 < e[1] < 35])
for km in (0, 10, 20, 30, 40, 42.195): print(f"km {km:6.3f}: Plan {np.interp(km, pp[:, 0], pp[:, 1]):6.1f}  App {np.interp(km, x, h):6.1f}")
