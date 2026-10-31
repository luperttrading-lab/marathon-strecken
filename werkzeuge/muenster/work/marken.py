# Nur Abgleich: Verpflegungssymbole des Streckenplans (gelbe Kästen 01–15, plan_pdf.json) gegen die km der Tabelle des Veranstalters.
# Jedes Symbol steht 15–20 pt neben der Linie und zeigt mit einem kleinen orangen Punkt (schwarz umrandet) auf seine Stelle; gemessen wird
# der Lotfußpunkt dieses Punkts, umgerechnet einmal stückweise zwischen den Kilometerkreisen (common.py, so gilt es in der App) und
# einmal gleichmäßig über die ganze Linie. Das Symbol „05, 15“ gilt für beide Durchgänge am Vesaliusweg.
import json
import numpy as np
import pymupdf
from common import official
pl = json.load(open("plan_pdf.json")); P = np.array(pl["pts"])
U = np.array(json.load(open("georef.json"))["plan"]); GL = json.load(open("strecke2026.json"))["d"][-1]
SU = np.r_[0, np.cumsum(np.hypot(*np.diff(U, axis=0).T))]; SG = SU * GL / SU[-1]
def c3(c): return tuple(round(v, 2) for v in c) if c else None
p = pymupdf.open("../dl/pdf/marathon_streckenplan_verlauf_2026_02.pdf")[0]
pkt = np.array([[(d["rect"].x0 + d["rect"].x1) / 2, (d["rect"].y0 + d["rect"].y1) / 2] for d in p.get_drawings()
                if d["type"] == "fs" and c3(d.get("fill")) == (0.91, 0.3, 0.06) and c3(d.get("color")) == (0, 0, 0) and d["rect"].width < 6])
def proj(x, y):
    q = np.array([x, y]); a = P[:-1]; b = P[1:]; v = b - a
    t = np.clip(((q - a) * v).sum(1) / np.maximum((v * v).sum(1), 1e-9), 0, 1); Q = a + t[:, None] * v
    return np.hypot(*(Q - q).T), SG[:-1] + t * np.diff(SG)
TAB = {"01": (4.3, "Kanonierplatz"), "02": (7.5, "Servatiiplatz"), "03": (9.5, "Ludgeristraße"), "04": (11.8, "Scharnhorststraße"),
       "05": (14.5, "Vesaliusweg"), "06": (17.5, "Mendelstraße/Gievenbecker Weg"), "07": (20.3, "Haus Uhlenkotten"),
       "08": (22.5, "Hermann-Hesse-Straße"), "09": (25.3, "Haus Vögeding"), "10": (27.5, "Stodtbrockweg"), "11": (30.0, "Wulfertstraße"),
       "12": (32.5, "Ramertsweg"), "13": (35.0, "Mergelberg"), "14": (37.5, "Gievenbecker Reihe"), "15": (40.0, "Vesaliusweg")}
ab_s, ab_g = [], []
for x, y, nrn in pl["vp"]:
    j = np.argmin(np.hypot(*(pkt - [x, y]).T)); d, s = proj(*pkt[j]); kand = s[d < d.min() + 1]
    for nr in nrn.split():
        km, wo = TAB[nr]; m = kand[np.argmin(abs(official(kand) - km * 1000))]
        ks, kg = float(official(m)) / 1000, m * 42195 / GL / 1000
        ab_s.append(ks - km); ab_g.append(kg - km)
        print(f"{nr} {wo:30s} Tabelle {km:5.1f}  Plan stückweise {ks:6.2f} ({ks - km:+.2f})  gleichmäßig {kg:6.2f} ({kg - km:+.2f})")
ab_s, ab_g = np.abs(ab_s), np.abs(ab_g)
print(f"|Abweichung| Median: stückweise {np.median(ab_s):.2f} km, gleichmäßig {np.median(ab_g):.2f} km; Mittel {ab_s.mean():.2f} / {ab_g.mean():.2f} km")
