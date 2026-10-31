# Verpflegungsstellen 1–18 laut Streckenplan 2026 des Veranstalters (../dl/pdf/2026-HM-Course-Map.pdf): Lage aus dem Plan. Die
# Kilometermarken („1k“ … „42k“) stehen als Text im PDF (pdftotext -bbox, ../dl/pdf/bbox.html) und
# liegen auf der gezeichneten Strecke; die Spitze des Zeigers jeder Station ist von Hand aus dem Bild abgelesen (TIP: Lage in den
# Kontaktbögen ../dl/pdf/stationen_bogen1.png und 2.png, Kachel 400 × 400 px um die Nummer der Station, 1040 px bei 120 dpi).
# Der km der Spitze ergibt sich aus der Lage zwischen den Marken (Projektion auf die Linie durch die Marken, im Bereich BEREICH,
# weil die Strecke auf dem Kalanianaʻole Highway hin und zurück läuft). Der Plan ist schematisch: Genauigkeit etwa ±0,3 km.
# -> stationen.json [[Nr., km, Symbole], …]
import json, re
import numpy as np
s = open("../dl/pdf/bbox.html", encoding="utf-8").read()
W = [(m.group(5), (float(m.group(1)) + float(m.group(3))) / 2, (float(m.group(2)) + float(m.group(4))) / 2)
     for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', s)]
MARKEN = []
for t, x, y in W:
    m = re.fullmatch(r"(\d+)([km])", t)
    if m and y < 3200 and not (4600 < x and y > 2650):          # ohne die Achsen der Höhenbilder
        if m.group(2) == "k": MARKEN.append((float(m.group(1)), x, y))
# Nur die Kilometermarken: Die Meilenmarken stehen im Plan zum Teil auf der Gegenrichtung (14m östlich von 23k), die Linie durch
# beide liefe im Zickzack. Es fehlen 32k und 39k (im Plan nicht als Text).
MARKEN.sort()
print(len(MARKEN), "Marken:", " ".join(f"{k:.1f}" for k, _, _ in MARKEN))
NR = {t: (x, y) for t, x, y in W if re.fullmatch(r"\d+", t) and y < 3000 and x < 6700}
NR = {"2": (569, 717), "3": (1276, 1252), "4": (1675, 2144), "5": (2199, 2280), "6": (2873, 2676), "7": (3281, 2242), "8": (4455, 1928),
      "9": (5364, 1753), "10": (6190, 1579), "11": (6607, 1321), "12": (6196, 1899), "13": (5437, 1992), "14": (4505, 2218),
      "15": (3745, 2236), "16": (3617, 2658), "17": (3039, 2931), "18": (2022, 2854)}   # Lage der Nummern (pt), aus bbox.html
TIP = {"2": (100, 185), "3": (188, 250), "4": (280, 185), "5": (135, 250), "6": (270, 215), "7": (255, 212), "8": (215, 290),
       "9": (210, 255), "10": (215, 225), "11": (185, 260), "12": (215, 105), "13": (190, 135), "14": (185, 120), "15": (135, 190),
       "16": (190, 135), "17": (262, 110), "18": (212, 200)}
BEREICH = {"2": (2, 5), "3": (5, 8), "4": (8, 10), "5": (9.5, 11), "6": (12.5, 15), "7": (15.5, 18), "8": (18, 22), "9": (21, 24.5),
           "10": (23.5, 26), "11": (25.5, 27.5), "12": (27, 29), "13": (29, 31.6), "14": (31.6, 34.5), "15": (34.5, 37), "16": (36, 38),
           "17": (37.5, 40), "18": (40.5, 42.2)}
# Symbole im Kasten (abgelesen): W Wasser, S Sportgetränk („Precision Fuel & Hydration“), G Gel, M Sanitäter, T Toiletten,
# E Elite-Station, U Musik, C Anfeuern
SYM = {"2": "WMUC", "3": "WMC", "4": "SWMC", "5": "SWMEC", "6": "SWGMTEC", "7": "SWMTC", "8": "SWGEC", "9": "SWC", "10": "SWMTEGC",
       "11": "WMC", "12": "SWMTUC", "13": "SWMEC", "14": "SWGMTC", "15": "SWMTEUC", "16": "WMUC", "17": "SWMTEUC", "18": "WM"}
S = 120 / 72
K = np.array([m[0] for m in MARKEN]); P = np.array([[m[1], m[2]] for m in MARKEN])
out = []
for n in NR:
    cx, cy = NR[n][0] * S, NR[n][1] * S; u, v = TIP[n]
    t = np.array([(cx - 520 + u * 2.6) / S, (cy - 520 + v * 2.6) / S])
    best = None
    for i in range(len(K) - 1):
        if K[i + 1] < BEREICH[n][0] or K[i] > BEREICH[n][1]: continue
        a, b = P[i], P[i + 1]; w = b - a; f = np.clip(np.dot(t - a, w) / (np.dot(w, w) or 1), 0, 1); q = a + f * w
        dist = float(np.hypot(*(t - q)))
        if best is None or dist < best[0]: best = (dist, K[i] + f * (K[i + 1] - K[i]))
    out.append([int(n), round(best[1], 2), SYM[n]])
    print(f"Station {n:>2s}: km {best[1]:5.2f} (Spitze {best[0]:4.0f} pt neben der Markenlinie)  {SYM[n]}")
json.dump(out, open("stationen.json", "w"))
