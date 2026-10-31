# Eichung der Kilometer: Die gezeichnete Linie (strecke2026.json) ist 43,02 km lang, also 2,0 % länger als 42,195 km. Der Plan trägt
# Kilometerkreise bei 5, 10, …, 40 km und „HM“, alle genau auf der Linie (Mitte des Kreises 0–3 pt = 0–20 m neben ihr). Zwischen
# diesen Marken wird gleichmäßig gestreckt (stückweise linear, Start = Linienanfang, Ziel = Linienende).
# Die Streckung ist nicht überall gleich: 0–5 km 0,988 Linienmeter je Meter, 5–10 1,023, 10–15 0,996, 15–20 1,065, 20–25 1,004,
# 25–30 1,038, 30–35 1,017, 35–40 1,013, 40–Ziel 1,046. Gegenprobe mit den Verpflegungsstellen (km laut Tabelle des Veranstalters
# gegen die Lage ihrer Symbole im Plan, marken.py): stückweise im Median 0,1 km daneben, gleichmäßig über die ganze Linie 0,2 km.
# -> eichung.json [[Linienmeter, offizielle Meter], …]
import json
import numpy as np
pl = json.load(open("plan_pdf.json")); P = np.array(pl["pts"])
U = np.array(json.load(open("georef.json"))["plan"]); g = json.load(open("strecke2026.json")); GL = g["d"][-1]
# Linienmeter je PDF-Punkt: geodätische Länge (strecke2026.json) auf die UTM-Länge der Planpunkte umgelegt
SU = np.r_[0, np.cumsum(np.hypot(*np.diff(U, axis=0).T))]; SG = SU * GL / SU[-1]
def proj(x, y):
    q = np.array([x, y]); a = P[:-1]; b = P[1:]; v = b - a
    t = np.clip(((q - a) * v).sum(1) / np.maximum((v * v).sum(1), 1e-9), 0, 1); Q = a + t[:, None] * v
    return np.hypot(*(Q - q).T), SG[:-1] + t * np.diff(SG)
E = [[0.0, 0.0]]
for x, y, t in pl["km"]:
    d, s = proj(x, y); soll = 21097.5 if t == "HM" else int(t) * 1000.0
    k = s[d < d.min() + 3]; k = float(k[np.argmin(abs(k * 42195 / GL - soll))])
    E.append([k, soll]); print(f"{t:>3s}: Kreis {d.min() * 6.97:4.1f} m neben der Linie, Linienmeter {k:7.0f}, gleichmäßig wäre es km {k * 42195 / GL / 1000:6.3f}")
E.append([GL, 42195.0]); E.sort()
for (a0, b0), (a1, b1) in zip(E[:-1], E[1:]): print(f"  km {b0 / 1000:6.3f}–{b1 / 1000:6.3f}: {(a1 - a0) / (b1 - b0):.4f} Linienmeter je Meter")
json.dump(E, open("eichung.json", "w"))
