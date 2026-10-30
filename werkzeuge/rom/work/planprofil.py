# Höhenbild „Altimetria / Altimetry“ aus dem Infoblatt des Veranstalters zum Renntag 2026 (../dl/RRTM26_MARATHON_22.03.pdf, Seite 4,
# https://www.runromethemarathon.com/wp-content/uploads/2026/03/RRTM26_MARATHON_22.03.pdf). Die Fläche ist eine Vektorgrafik:
# Oberkante auslesen. Achsen aus dem Rahmen: km 0 bei x = 283,43 pt, km 42,195 bei x = 526,99 pt (Rahmen und Fläche enden dort);
# 0 m auf der Grundlinie y = 531,34 pt, Hilfslinien alle 10 m im Abstand von 7,03 pt (Linien bei 524,04 / 517,01 / 509,98 /
# 502,96 pt, Rahmenoberkante 496,11 pt = 50 m). Die Beschriftungen im Bild passen nicht zur eigenen Achse (Start als „23 m“ beschriftet,
# Punkt bei 10 m; Tiefpunkt „12 m“ bei 6 m; Hochpunkt „31 m“ bei 33 m) -> planprofil.json [[km, Höhe], …]
import json, numpy as np
import pymupdf as fitz
doc = fitz.open("../dl/RRTM26_MARATHON_22.03.pdf"); p = doc[3]
prof = [d for d in p.get_drawings() if d["type"] == "fs" and d["rect"].width > 200 and 505 < d["rect"].y0 < 512][0]
pts = []
for it in prof["items"]:
    if it[0] == "l": pts += [(it[1].x, it[1].y), (it[2].x, it[2].y)]
    elif it[0] == "c": pts += [(it[1].x, it[1].y), (it[4].x, it[4].y)]
pts = np.array(pts)
X0, X1, Y0, DY = 283.43, 526.99, 531.34, 7.03
km = (pts[:, 0] - X0) / (X1 - X0) * 42.195; h = (Y0 - pts[:, 1]) / DY * 10
# Oberkante: Eckpunkte der Umrisslinie über der Grundlinie, nach km sortiert (bei gleichem km der höchste), dazwischen linear
sel = h > 0.5; k_, h_ = km[sel], h[sel]; o = np.lexsort((-h_, k_)); k_, h_ = k_[o], h_[o]
erst = np.r_[True, np.diff(k_) > 1e-6]; k_, h_ = k_[erst], h_[erst]
gr = np.round(np.arange(0, 42.2, 0.1), 1); gr[-1] = min(gr[-1], 42.195)
out = [[float(g), round(float(v), 2)] for g, v in zip(gr, np.interp(gr, k_, h_))]
json.dump(out, open("planprofil.json", "w"))
v = np.array([o[1] for o in out])
print(len(out), "Werte; Start", out[0], "Ziel", out[-1], "min", v.min(), "bei km", out[int(v.argmin())][0], "max", v.max(), "bei km", out[int(v.argmax())][0])
