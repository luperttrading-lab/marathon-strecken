# Höhenprofil für die App -> clean.json. Grundlage FABDEM (dgm2025_10m.json bzw. dgm_vergleich.json, 1″-Raster; Wahl in vergleich.py
# und UEBERGABE.md). Shanghai ist auf der ganzen Strecke flach (Gelände 1–3 m über dem Meer); was FABDEM darüber hinaus zeigt, sind
# zum größten Teil Reste von Häusern, die das 30-m-Modell nicht ganz herausrechnet (bis 10 m an der Nanjing Lu/Hubei Lu, 4–6 m an
# der Nanjing Xilu, an der Xizang Nanlu und am Ufer), und Wasser an den Bächen unter den Brücken. Deshalb:
# 1. Brücken aus OSM (bridge=yes auf der Linie, strassen.json; Hochstraßen benutzt die Strecke nicht, Tunnel keine): das Stück samt
#    50 m davor und dahinter bleibt aus der Glättung heraus (darunter liegen Bach, Ufer und Rampen).
# 2. Gelände: robust geglättet wie in Athen (Innenstadt) und Stockholm (Gegenprobe), lokal gewichtete Ausgleichsgerade über ±HW m
#    (Standard 500 m; LOWESS, Tricube, vier Runden mit Bisquare-Gewichten gegen Ausreißer). Weil Hausreste nur nach oben ragen, zählen
#    Werte über der Kurve schon ab dem Doppelten der mittleren Abweichung (MAD) nichts mehr, Werte darunter erst ab dem Sechsfachen
#    (mit ±300 m und gleichen Gewichten blieben Buckel von 2,5 m an der Nanjing Xi Lu und der Xizang Nan Lu stehen, ↑ Gelände 29 statt
#    16 m). Was dabei verloren geht, sind Wellen unter etwa einem Meter auf einigen hundert Metern – ob es sie gibt, kann ein 30-m-Modell
#    nicht sagen.
# 3. Brückendecks: Kein frei zugängliches Modell kennt sie (FABDEM rechnet sie heraus, Copernicus sieht über den schmalen Bächen das
#    Wasser). Das Höhenbild des Veranstalters (planprofil.py) zeigt an genau diesen Brücken Spitzen, auf Hin- und Rückweg gleich hoch:
#    Longteng Dadao über den Longhua Gang gut 9 m, die zwei Bachbrücken weiter südlich 2,5–3 m, die Brücke auf der Wanping Nanlu
#    knapp 2 m. Das Deck wird als Buckel (halbe Kosinuswelle) über die OSM-Brücke samt 20 m an jedem Ende auf das Gelände gesetzt,
#    Höhe aus dem Höhenbild (Spitze minus Mittel daneben); „geschätzt“, in der App schraffiert.
# Aufruf: python3 clean.py [HW [OBEN]]   (Standard 500 m und 2·MAD; „python3 clean.py 300 6“ ist die symmetrische Glättung)
import json, sys, numpy as np
from common import official
HW = float(sys.argv[1]) if len(sys.argv) > 1 else 500.0
OBEN = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
v = json.load(open("dgm_vergleich.json"))
s = np.array(v["s"]); k = official(s)
raw = np.array(v["fabdem"], float)
st = json.load(open("strassen.json"))
n = min(len(raw), len(st))
br = np.zeros(len(raw), bool); br[:n] = [o[3] not in ("", "no") for o in st[:n]]
def gruppen(m, luecke):
    idx = np.where(m)[0]
    return np.split(idx, np.where(np.diff(idx) > luecke)[0] + 1) if len(idx) else []
def lowess(x, y, hw, gew, runden=4):
    """Robuste LOWESS nur über die Punkte mit Gewicht; dazwischen (Brücken) linear zwischen den geglätteten Rändern."""
    m = gew > 0; X0, Y0 = x[m], y[m]
    w_rob = np.ones_like(Y0); out = Y0.copy()
    for _ in range(runden + 1):
        for i in range(len(X0)):
            lo, hi = np.searchsorted(X0, X0[i] - hw), np.searchsorted(X0, X0[i] + hw)
            xx = X0[lo:hi]; dd = np.abs(xx - X0[i]); ww = (1 - (dd / hw) ** 3) ** 3 * w_rob[lo:hi]
            X = np.c_[np.ones(len(xx)), xx - X0[i]]
            out[i] = np.linalg.lstsq(X.T @ (X * ww[:, None]), X.T @ (Y0[lo:hi] * ww), rcond=None)[0][0]
        res = Y0 - out; mad = np.median(np.abs(res)) or 0.1
        u = np.where(res > 0, res / (OBEN * mad), res / (6 * mad)); w_rob = np.where(np.abs(u) < 1, (1 - u ** 2) ** 2, 0)
    return np.interp(x, X0, out)
# Höhenbild des Veranstalters: Spitzen an den Brücken (seine km-Achse liegt bis 0,7 km neben der Linie; zugeordnet wird nach der
# Reihenfolge: Longhua Gang, Bach A hin, Bach B hin, Bach B zurück, Bach A zurück, Wanping Nanlu)
pp = np.array(json.load(open("planprofil.json"))); pk, ph = pp[:, 0], pp[:, 1]
def spitze(a, b):
    sel = (pk >= a) & (pk <= b); i = int(np.argmax(np.where(sel, ph, -1e9))); x0 = pk[i]
    rand = ((pk > x0 - 0.5) & (pk < x0 - 0.2)) | ((pk > x0 + 0.2) & (pk < x0 + 0.5))
    return float(ph[i] - np.median(ph[rand])), float(x0)
SP = [spitze(27.0, 27.8), spitze(30.5, 30.95), spitze(31.1, 31.5), spitze(33.1, 33.55), spitze(33.6, 34.1), spitze(38.2, 38.6)]
print("Spitzen im Höhenbild des Veranstalters (Höhe über dem Mittel daneben, km auf seiner Achse):", [(round(a, 1), x) for a, x in SP])
gew = np.ones(len(raw))
brueck = []
for g in gruppen(br, 3):
    a0, b0 = int(g.min()), int(g.max()) + 1
    nm = st[int(np.median(g))][2] or "Brücke"
    brueck.append([a0, b0, nm]); gew[max(0, a0 - 5):b0 + 6] = 0.0
assert len(brueck) == len(SP), (len(brueck), len(SP))
# A und B: Mittel aus Hin- und Rückweg
amp = [SP[0][0], (SP[1][0] + SP[4][0]) / 2, (SP[2][0] + SP[3][0]) / 2, (SP[2][0] + SP[3][0]) / 2, (SP[1][0] + SP[4][0]) / 2, SP[5][0]]
h = lowess(k, raw, HW, gew)
boden = h.copy()
regions = []
for (a0, b0, nm), A in zip(brueck, amp):
    a, b = max(0, a0 - 2), min(len(h) - 1, b0 + 2)          # 20 m vor und hinter der OSM-Brücke
    t = (k[a:b + 1] - k[a]) / (k[b] - k[a]); h[a:b + 1] = boden[a:b + 1] + A * (1 - np.cos(2 * np.pi * t)) / 2
    regions.append({"a": float(k[a]), "b": float(k[b]), "kind": "Brücke", "name": nm, "ha": float(h[a]), "hb": float(h[b]),
                    "deck": round(A, 1), "laenge": round(float(k[b] - k[a]))})
    print(f"  Brücke km {k[a] / 1000:6.2f}–{k[b] / 1000:6.2f} ({k[b] - k[a]:4.0f} m) {nm:12s} FABDEM darunter {raw[a0:b0 + 1].min():4.1f}–{raw[a0:b0 + 1].max():4.1f} m, "
          f"Gelände {boden[a]:.1f}/{boden[b]:.1f} m, Deck +{A:.1f} m -> {h[a:b + 1].max():.1f} m, steilste Rampe {np.abs(np.diff(h[a:b + 1])).max() * 10:.1f} %")
dv = np.abs(boden - raw)[gew > 0]
print(f"  geglättet (±{HW:.0f} m): Abweichung vom Modell Median {np.median(dv):.2f} m, 90 % {np.percentile(dv, 90):.1f} m, höchstens {dv.max():.1f} m "
      f"bei km {k[gew > 0][np.argmax(dv)] / 1000:.2f}")
json.dump({"k": k.tolist(), "h": h.tolist(), "boden": boden.tolist(), "raw": raw.tolist(), "regions": regions, "hw": HW, "quelle": "fabdem"},
          open("clean.json", "w"), ensure_ascii=False)
