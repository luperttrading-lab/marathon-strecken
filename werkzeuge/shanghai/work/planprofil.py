# Höhenprofil des Veranstalters aus dem Streckenplan 2025 (kleines Bild „海拔高度 Altitude“ in der Legende, ../dl/bilder/bkeq2u5mfMbpVKf5.JPG,
# Ausschnitt x 3368–4350, y 4062–4282 px). Achsen aus dem Bild: waagerechte Linien 20/15/10/5 m bei y = 4127,5 / 4167,5 / 4207,5 /
# 4247,5 (8 px je m); die Kurve reicht von x = 3398 (Start) bis 4332 (Ziel), dazwischen gleichmäßig 42,195 km (die Beschriftung 0 … 42
# steht mit 21,7 px je km darunter; das passt auf 1 %). Je Spalte die Mitte der blauen Linie. Woher die Höhen stammen, sagt der
# Veranstalter nicht (vermutlich eine GPS-Aufzeichnung mit Luftdruckmesser: Die Werte liegen gut 8 m über den Höhenmodellen, und die
# Spitzen an Brücken sind schmal und hoch). -> planprofil.json [[km, h], …]
import json
import numpy as np
from PIL import Image
a = np.asarray(Image.open("../dl/bilder/bkeq2u5mfMbpVKf5.JPG").convert("RGB")).astype(int)
x0, x1, y0, y1 = 3368, 4350, 4062, 4282
sub = a[y0:y1, x0:x1]; R, G, B = sub[..., 0], sub[..., 1], sub[..., 2]
blau = (B - R > 90) & (R < 120)
XA, XE = 3398, 4332
def km(x): return (x - XA) / (XE - XA) * 42.195
def hoehe(y): return 20.0 - (y - 4127.5) / 8.0
out = []
for x in range(XA, XE + 1):
    ys = np.nonzero(blau[:, x - x0])[0]
    ys = ys[(ys + y0 > 4110) & (ys + y0 < 4262)]
    if len(ys) == 0: continue
    out.append([round(km(x), 3), round(hoehe(np.median(ys) + y0), 2), round(hoehe(ys.min() + y0), 2)])
json.dump([[k, h] for k, h, _ in out], open("planprofil.json", "w"))
p = np.array(out)
print(len(p), "Spalten, km", p[0, 0], "–", p[-1, 0], "Höhe", p[:, 1].min(), "–", p[:, 1].max(), "bei km", p[np.argmax(p[:, 1]), 0])
for k in range(0, 43, 3): print(k, round(float(np.interp(k, p[:, 0], p[:, 1])), 1))
