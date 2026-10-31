# Wirkung des Vorschlags „Bergauf-Aufschlag wächst mit den schon gestiegenen Höhenmetern“ auf alle Strecken der App:
# Modellzeit bei 4:00 /km im Flachen bisher und neu (ohne Mauer-Minuten der Great Wall, die das Modell dort nicht rechnet).
#   python3 wirkung.py [gauf]      (Standard 0,685 aus auswerten.py, Ermüdung einheitlich)
import sys, os, json, re
import numpy as np
import modell as M

GAUF = float(sys.argv[1]) if len(sys.argv) > 1 else 0.685
apps = sorted(d for d in os.listdir(M.REPO) if os.path.exists(f"{M.REPO}/{d}/index.html") and
              re.search(r"^const D = ", open(f"{M.REPO}/{d}/index.html", encoding="utf-8").read(), re.M))
def hms(s): s = int(round(s)); return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"
zeilen = []
for a in apps:
    S = M.lade(a)
    if S.D.get("mauer"): continue
    g = S.win[100]["g"]; gm = (g[:-1] + g[1:]) / 2; f = S.ratio(); fm = (f[:-1] + f[1:]) / 2
    hmcum = np.concatenate([[0], np.cumsum(np.maximum(0, gm) / 100 * S.STEP)])[:-1]
    neu = np.where(gm > 0, 1 + (fm - 1) * (1 + GAUF * hmcum / 1000), fm)
    xm = (S.x[:-1] + S.x[1:]) / 2; m = xm < S.L
    alt_t = 240 * (fm[m] * S.STEP).sum() / 1000; neu_t = 240 * (neu[m] * S.STEP).sum() / 1000
    zeilen.append((a, round(S.at(S.win[200]["up"], S.L)), alt_t, neu_t))
zeilen.sort(key=lambda z: z[1])
print(f"Bergauf-Aufschlag × (1 + {GAUF} × schon gestiegene Höhenmeter / 1000); 4:00 /km im Flachen")
print(f"{'Strecke':14s} {'↑ 200 m':>8s} {'bisher':>9s} {'neu':>9s} {'Steigungskosten bisher → neu':>30s}")
for a, up, t0, t1 in zeilen:
    flach = 240 * 42.195
    print(f"{a:14s} {up:8d} {hms(t0):>9s} {hms(t1):>9s}   {t0 - flach:7.0f} s → {t1 - flach:7.0f} s ({t1 / t0 - 1:+.1%} Zielzeit)")
