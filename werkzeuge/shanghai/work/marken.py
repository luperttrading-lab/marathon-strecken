# Nur Abgleich: Kilometerkreise des Streckenplans 2025 (plan.py) gegen die Linie (linie.py, gleichmäßig auf 42 195 m, common.py). Der
# Plan ist zu vereinfacht, um die Kreise einzupassen (georef.py: bis 450 m daneben); verglichen wird deshalb, wo der Plan einen Kreis
# an einer erkennbaren Stelle zeichnet (Kreuzung, Wende, Brücke), mit dem Kilometer dieser Stelle auf der Linie. Dazu die Spitzen im
# Höhenbild des Veranstalters (planprofil.py) an den Brücken und die Halbmarathon-Matte („半程点“) im Plan 2024.
import json, numpy as np
from common import official
L = json.load(open("linie2025.json")); WP = dict((n, float(official(x)) / 1000) for n, x in L["wegpunkte"])
st = json.load(open("strassen.json"))
def bruecken():
    out, an = [], None
    for o in st:
        b = o[3] not in ("", "no")
        if b and an is None: an = o[0]
        if not b and an is not None: out.append((float(official(an)) / 1000, float(official(o[0])) / 1000)); an = None
    return out
BR = bruecken()
VERGLEICH = [  # Kreis im Plan, was der Plan dort zeigt, Stelle auf der Linie (km)
    (1, "an der Ecke Xinkaihe Lu/Renmin Lu", WP["Xinkaihe Lu"]),
    (3, "auf der Nanjing Dong Lu zwischen Henan Lu und Hubei Lu", (WP["Henan Zhonglu/Nanjing Donglu"] + WP["Nanjing Donglu/Hubei Lu"]) / 2),
    (7, "an der Ecke Nanjing Xi Lu/Huashan Lu", WP["Nanjing Xilu/Huashan Lu"]),
    (8, "kurz vor der Ecke Changshu Lu/Huaihai Zhong Lu", WP["Changshu Lu/Huaihai Zhonglu"]),
    (11, "an der Ecke Madang Lu/Xingye Lu", WP["Madang Lu/Xingye Lu"]),
    (13, "kurz hinter der Ecke Huaihai Zhong Lu/Xizang Nan Lu", WP["Huaihai Zhonglu/Xizang Nanlu"]),
    (16, "auf der Gaoxiong Lu", (WP["Xizang Nanlu/Gaoxiong Lu"] + WP["Gaoxiong Lu/Zhizaoju Lu"]) / 2),
    (20, "auf der Bansongyuan Lu kurz vor der Lujiabang Lu", WP["Bansongyuan Lu/Lujiabang Lu"]),
    (26, "auf der Ruining Lu kurz vor der Longteng Dadao", WP["Ruining Lu/Longteng Dadao"]),
    (27, "auf der Longteng Dadao am Südende der Brücke über den Longhua Gang", BR[0][1]),
    (32, "kurz vor der Wende auf der Longteng Dadao", WP["Wende Longteng Dadao"]),
    (37, "am Ende der Stichstraße („Fenggu Rd.“)", WP["Wende Ruijiang Lu"]),
    (38, "an der Ecke Longteng Dadao/Longheng Dong Lu", WP["Longteng Dadao/Longheng Donglu"]),
    (40, "auf der Longhua Lu", (WP["Wanping Nanlu/Longhua Lu"] + WP["Longhua Lu/Longhua Xilu"]) / 2),
]
print("Kreis  Linie   Abstand  Stelle")
ab = []
for km, txt, x in VERGLEICH:
    ab.append(x - km); print(f"{km:4d}  {x:6.2f}  {x - km:+6.2f}  {txt}")
ab = np.array(ab); print(f"Abweichung Median {np.median(ab):+.2f} km, |Abweichung| Median {np.median(np.abs(ab)):.2f} km, höchstens {np.abs(ab).max():.2f} km")
print("Halbmarathon 21,0975 km: Plan 2024 zeigt die Matte auf dem Uferweg südlich der Lujiabang Lu; Linie: Uferweg bis km",
      round(WP["Uferweg (Huayuangang Lu)"], 2), "und weiter bis zur Miaojiang Lu")
pp = np.array(json.load(open("planprofil.json")))
print("Brücken (OSM auf der Linie, km) und Spitzen im Höhenbild des Veranstalters (seine km-Achse):")
SP = [27.42, 30.72, 31.26, 33.34, 33.88, 38.36]
for (a, b), s in zip(BR, SP): print(f"  {a:6.2f}–{b:6.2f}  Spitze bei {s:6.2f}  Versatz {s - (a + b) / 2:+.2f} km")
