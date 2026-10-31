# Verpflegungspunkte, Erfrischungspunkte und Staffelwechselzonen aus dem Streckenplan 2026 (Symbole „Verpflegungspunkt / Nutrition
# zone“, dunkelblau; „Erfrischungspunkt / Refreshment zone“, blau; „Staffelwechselzone / Relay transition zone“, grün mit Nummer):
# Mitte jedes Kreises (Farbe aus der Legende), Lotfußpunkt auf die Planlinie. Die Symbole stehen neben der Linie; wo die Strecke an
# derselben Stelle mehrmals vorbeiführt (Luegallee, Heinrich-Heine-Allee, Königsallee, Klever Straße), ist der Durchgang von Hand gewählt
# (Liste WAHL: ungefährer km laut Planlinie), nach der Lage des Symbols zur Fahrtrichtung, dem Wechsel Verpflegung/Erfrischung etwa
# alle 2,5 km und den Angaben des Veranstalters (erste Verpflegung „nach ca. 5 Kilometern in Höhe des Aquazoos“, Wechselzonen
# Fischerstraße, Steinstraße, Jacobistraße nach ca. 11,2 / 13,1 / 9,2 km). Lage etwa ±0,2 km.
# -> stationen.json [[offizielle Meter, Art], …]
import json, collections
import numpy as np
import pymupdf
from common import official
doc = pymupdf.open("../dl/pdf/Streckenplan_Marathon_sportsidioten.pdf"); p = doc[0]
P = np.array(json.load(open("plan_pdf.json"))["pts"]); U = np.array(json.load(open("georef.json"))["plan"])
SU = np.r_[0, np.cumsum(np.hypot(*np.diff(U, axis=0).T))]; SU *= 42195 / SU[-1]
FARBE = {(0.22, 0.46, 0.73): "Erfrischung", (0.13, 0.17, 0.36): "Verpflegung", (0.27, 0.72, 0.36): "Staffel"}
WAHL = [4.5, 10.0, 11.3, 12.2, 14.9, 16.4, 19.9, 22.0, 24.2, 24.7, 27.0, 30.5, 32.5, 33.3, 35.3, 37.5, 40.1]
def lote(x, y):
    q = np.array([x, y]); a = P[:-1]; b = P[1:]; v = b - a
    t = np.clip(((q - a) * v).sum(1) / np.maximum((v * v).sum(1), 1e-9), 0, 1); Q = a + t[:, None] * v
    return np.hypot(*(Q - q).T), SU[:-1] + t * np.diff(SU)
out = []
for d in p.get_drawings():
    r = d["rect"]; f = d.get("fill") and tuple(round(c, 2) for c in d["fill"])
    if r.x0 < 300 and r.y0 > 900: continue                                    # Legende
    if f in FARBE and len(d["items"]) == 4 and all(i[0] == "c" for i in d["items"]) and r.width > 30:
        dist, km = lote((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)
        nah = dist < dist.min() + 20                                            # alle Durchgänge in Reichweite des Symbols
        kand = km[nah]
        w = min(WAHL, key=lambda z: abs(z * 1000 - kand).min())
        k = float(kand[np.argmin(abs(w * 1000 - kand))])
        assert abs(k - w * 1000) < 250, (FARBE[f], w, k)
        out.append([round(k), FARBE[f]])
        print(f"{FARBE[f]:12s} km {k / 1000:6.2f}  (Durchgänge in Reichweite: {', '.join(sorted(set(f'{z / 1000:.1f}' for z in kand)))})")
out.sort()
assert len(out) == len(WAHL), len(out)
json.dump(out, open("stationen.json", "w"), ensure_ascii=False)
