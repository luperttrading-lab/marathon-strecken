# Nachrechnung 31.10.2026 zur Berg-Eichung:
#  1. Dauer-Term (Riegel T ∝ D^b): (a) ändert er die Schätzung aus den Zwischenzeiten? (b) Umrechnung Streckenzeit ↔ flache Zeit
#  2. Welche Größe erklärt den Restaufschlag: schon gestiegene Höhenmeter, verstrichene Zeit, zurückgelegte km, zusätzliche Steigung
#  3. Tafel Flach-Meter je Höhenmeter (Steigung × schon gestiegen)
#  4. Wirkung auf alle Strecken und Beispiel 3:30 flach
# Nutzt die Definitionen aus auswerten.py (alles vor der Ausgabe) und dieselben Rohdaten ohne Namen unter /tmp.
#   python3 nachrechnung.py /tmp/berg/roh > nachrechnung.txt
import sys, os, re
import numpy as np, pandas as pd
from scipy.optimize import least_squares

HIER = os.path.dirname(os.path.abspath(__file__))
ROH_ARG = sys.argv[1] if len(sys.argv) > 1 else "/tmp/berg/roh"
sys.argv = [sys.argv[0], ROH_ARG, "0"]
exec(open(os.path.join(HIER, "auswerten.py"), encoding="utf-8").read().split("# ================================================================= Ausgabe")[0])

# Teil B (Spitze 2026, 7 eindeutige Treffer): nur die verdichteten Zahlen, keine Namen, keine Einzelwerte
TEILB = {"alle": (1.435, 7), "Jungfrau": (1.435, 5), "Zermatt": (1.436, 2)}   # Bergzeit / flache Bestzeit, Median, Anzahl
TEILB_TAL = 1.066                                                                # Äquivalenzzeit aus dem Anker / Bestzeit, Median

def hms(s): s = int(round(s)); return f"{s // 3600}:{s % 3600 // 60:02d}"
V = vorbereiten(TH_APP); C = zellen(V)
MN = "App, Aufschlag wächst (a = 1)"
th0, p0fit, _, mse0 = fit(C, MN)
GAUF = p0fit["gauf"]

# ================================================================= 1a Dauer-Term in den Zwischenzeiten
print("== 1a Dauer-Term (Riegel) und die Schätzung aus den Zwischenzeiten")
print("   Ein Faktor auf die Pace des ganzen Rennens kürzt sich in log(Abschnitt / Anker) heraus; er ändert nur die Klasse.")
for b in (1.07, 1.10, 1.15):
    V2 = {}
    for rn, v in V.items():
        v = v.copy(); R = v.ziel / v.teq                                    # Zielzeit / Äquivalenzzeit je Läufer
        tflach = (v.teq * v.ziel ** (1 - b)) ** (1 / (2 - b))               # selbstkonsistent: Teq = Tflach · (Ziel/Tflach)^(b−1)
        v["teq"] = tflach; v["klasse"] = np.digitize(tflach, KL_GR) - 1; V2[rn] = v
    C2 = zellen(V2); _, p2, _, mse2 = fit(C2, MN)
    print(f"   Exponent {b:.2f}: Faktor {p2['gauf']:.3f} statt {GAUF:.3f}, Fehler je Zelle {100 * np.sqrt(mse2):.2f} statt {100 * np.sqrt(mse0):.2f} %"
          f" (nur weil Läufer die Klasse wechseln; y je Läufer unverändert)")

# ================================================================= 1b Umrechnung Strecke ↔ flach
print("\n== 1b Umrechnung: Zielzeit / flache Marathonzeit = (E/L)^(1/(2−b)), selbstkonsistent mit dem Faktor (T_Strecke/T_flach)^(b−1)")
APPS_B = {"Jungfrau": "jungfrau", "Zermatt": "zermatt", "LGT": "liechtenstein", "Brocken": "brocken", "Rennsteig": "rennsteig"}
def strecke(app):
    S = M.lade(app); g = S.win[100]["g"]; gm = (g[:-1] + g[1:]) / 2; f = S.ratio(); fm = (f[:-1] + f[1:]) / 2
    xm = (S.x[:-1] + S.x[1:]) / 2; m = xm < S.L
    hmc = np.concatenate([[0], np.cumsum(np.maximum(0, gm) / 100 * S.STEP)])[:-1]
    mauer = np.zeros_like(xm, bool)
    for a, bb, *_ in (S.D.get("mauer") or []): mauer |= (xm >= a) & (xm <= bb)
    return dict(S=S, gm=gm, fm=fm, xm=xm, m=m, hmc=hmc, mauer=mauer, H=(S.H[:-1] + S.H[1:]) / 2)
ST = {k: strecke(v) for k, v in APPS_B.items()}
def EL(st, art="app", gam=GAUF, p0=0.24, ohne_mauer=False):
    """gewichtete Strecke / Länge; art: app | hm | km | zeit | steig; p0 in s je m (für zeit)"""
    gm, fm, m = st["gm"], st["fm"], st["m"]; up = gm > 0
    if art == "app": f = fm
    else:
        if art == "hm": X = st["hmc"] / 1000
        elif art == "km": X = st["xm"] / 10000
        elif art == "steig": X = np.maximum(gm, 0) / 10
        elif art == "zeit":
            f = fm.copy()
            for _ in range(3):
                t = np.concatenate([[0], np.cumsum(f * 10 * p0)])[:-1] / 3600; f = np.where(up, 1 + (fm - 1) * (1 + gam * t), fm)
            X = t
        f = np.where(up, 1 + (fm - 1) * (1 + gam * X), fm)
    sel = m & ~st["mauer"] if ohne_mauer else m
    return (f[sel] * 10).sum() / (10 * sel.sum())
zeilen = []
for rn, st in ST.items():
    ea, en = EL(st, "app"), EL(st, "hm")
    z = [f"   {rn:10s} E/L App {ea:.3f}, Vorschlag {en:.3f} |"]
    for b in (1.00, 1.07, 1.10, 1.15):
        z.append(f" b={b:.2f}: App {ea ** (1 / (2 - b)):.3f}, neu {en ** (1 / (2 - b)):.3f};")
    if rn in TEILB: z.append(f" Teil B {TEILB[rn][0]:.3f} (n={TEILB[rn][1]})")
    print("".join(z))
print(f"   Tal langsamer als Bestzeit, was der Dauer-Term erklärt (Verhältnis 1,435): "
      + ", ".join(f"b={b:.2f} → {100 * (1.435 ** (b - 1) - 1):.1f} %" for b in (1.07, 1.10, 1.15))
      + f"; gemessen {100 * (TEILB_TAL - 1):.1f} % → b = {1 + np.log(TEILB_TAL) / np.log(1.435):.2f}")

# ================================================================= 2 Welche Größe erklärt den Restaufschlag
print("\n== 2 Restaufschlag über der App-Kurve (Minetti × 0,77): Bergauf-Aufschlag × (1 + γ · X)")
# je Zelle die flache Pace p0 (s je m) für die Zeit-Variante
ANKER_PHI = {rn: phi_km(TI_EINH, R["grenzen"][R["anker"][0]], R["grenzen"][R["anker"][-1] + 1])[0] for rn, R in RENNEN.items()}
def E_var(R, rn, art, g, p0=None):
    gm, f = R["gm"], R["fapp"]; up = gm > 0; s = R["seg"]
    if art == "hm": X = R["hmcum"] / 1000
    elif art == "km": X = R["xm"] / 10000
    elif art == "steig": X = np.maximum(gm, 0) / 10
    elif art == "zeit":
        ff = f.copy()
        for _ in range(3):
            t = np.concatenate([[0], np.cumsum(ff * 10 * p0)])[:-1] / 3600; ff = np.where(up, 1 + (f - 1) * (1 + g * t), f)
        X = t
    p = np.where(up, 1 + (f - 1) * (1 + g * X), f) * 10
    return np.array([p[s == i].sum() for i in range(R["ns"])])
def fit_var(c, arten, ohne=None):
    c = c[np.array([s not in RENNEN[r]["anker"] for r, s in zip(c.rennen, c.seg)], bool)]
    if ohne: c = c[c.rennen != ohne]
    yv = c.ye.to_numpy(); w = np.sqrt(np.minimum(c.n.to_numpy(), 200))
    gruppen = list(c.groupby(["rennen", "jahr", "klasse"]).groups.items())
    def pred(gs):
        out = pd.Series(0.0, index=c.index)
        for (rn, j, k), idx in gruppen:
            R = RENNEN[rn]; cc = c.loc[idx]; p0 = float(cc.teq.median()) * np.exp(ANKER_PHI[rn]) / L
            Es = np.full(R["ns"], 0.0)
            # mehrere Größen: Aufschläge addieren sich (1 + Σ γ_i X_i)
            base = E_var(R, rn, "hm", 0.0)
            Es = base.copy()
            for art, g in zip(arten, gs): Es = Es + (E_var(R, rn, art, g, p0) - base)
            out.loc[idx] = np.log(Es[cc.seg.to_numpy()] / Es[R["anker"]].sum())
        return out.to_numpy()
    r = least_squares(lambda gs: w * (pred(gs) - yv), [0.3] * len(arten), bounds=([0] * len(arten), [10] * len(arten)))
    return r.x, float(np.sum(r.fun ** 2) / np.sum(w ** 2)), c.assign(pred=pred(r.x))
VARS = [("schon gestiegene Höhenmeter (je 1000)", ["hm"]), ("verstrichene Zeit (je Stunde)", ["zeit"]),
        ("zurückgelegte km (je 10 km)", ["km"]), ("zusätzliche Steigung (je 10 %)", ["steig"]),
        ("Höhenmeter + Steigung", ["hm", "steig"]), ("Höhenmeter + Zeit", ["hm", "zeit"]), ("Höhenmeter + km", ["hm", "km"])]
ERGV = {}
for nm, arten in VARS:
    g, mse, cf = fit_var(C, arten); ERGV[nm] = g
    loo = []
    for rn in RENNEN:
        g2, _, _ = fit_var(C, arten, ohne=rn)
        cc = C[(C.rennen == rn).to_numpy() & np.array([s not in RENNEN[rn]["anker"] for s in C.seg])]
        pr = []
        for (j, k), d in cc.groupby(["jahr", "klasse"]):
            R = RENNEN[rn]; p0 = float(d.teq.median()) * np.exp(ANKER_PHI[rn]) / L
            base = E_var(R, rn, "hm", 0.0); Es = base.copy()
            for art, gg in zip(arten, g2): Es = Es + (E_var(R, rn, art, gg, p0) - base)
            pr.append(np.log(Es[d.seg.to_numpy()] / Es[R["anker"]].sum()) - d.ye.to_numpy())
        loo.append(f"{rn} {100 * np.median(np.concatenate(pr)):+.1f} %")
    # Unterschied der Klassen: Fehler der langsamsten minus der schnellsten Klasse (Median über Abschnitte)
    kl = cf.assign(e=cf.pred - cf.ye).groupby("klasse").e.median() * 100
    # Wirkung bei 4:00 /km (Zeit-Variante mit p0 = 0,24 s/m)
    wk = []
    for app in ("boston", "newyork", "athen", "rennsteig", "brocken", "jungfrau"):
        st = ST.get(app.capitalize()) or strecke(app)
        e0 = EL(st, "app")
        if len(arten) == 1: e1 = EL(st, arten[0], g[0])
        else:
            e1 = e0 + sum(EL(st, a, gg) - e0 for a, gg in zip(arten, g))
        wk.append(f"{app} {100 * (e1 / e0 - 1):+.1f} %")
    print(f"  {nm:38s} γ = " + " / ".join(f"{x:.3f}" for x in g) + f" | Fehler je Zelle {100 * np.sqrt(mse):.2f} % | weggelassen: " + "; ".join(loo)
          + f" | Klassen (Modell − beob.): " + " ".join(f"{x:+.1f}" for x in kl.values) + " %"
          + " | Zielzeit bei 4:00 /km: " + ", ".join(wk))

# ================================================================= 3 Tafel
print(f"\n== 3 Flach-Meter je Höhenmeter: App-Kurve × (1 + {GAUF:.3f} × schon gestiegen / 1000)")
SG = [5, 10, 15, 20, 30]; HB = [0, 250, 500, 1000, 1500, 2000]
kapp = [float((M.pace_faktor(x / 100) - 1) / (x / 100)) for x in SG]
tafel = pd.DataFrame([[k * (1 + GAUF * h / 1000) for k in kapp] for h in HB], index=[f"{h} m" for h in HB], columns=[f"{x} %" for x in SG])
tafel.loc["Minetti"] = [(M.minetti(x / 100) / 3.6 - 1) / (x / 100) for x in SG]
print(tafel.round(1).to_string()); tafel.round(2).to_csv(os.path.join(HIER, "tafel_flachmeter.csv"))

# ================================================================= 4 Beispiel 3:30 flach
print("\n== 4 Beispiel flach 3:30 (gleichmäßige Anstrengung): App heute / neu ohne Dauer-Term / neu mit Dauer-Term b = 1,07 / beobachtet")
rows = []
T = 3.5 * 3600
for rn, st in ST.items():
    ea, en = EL(st, "app"), EL(st, "hm")
    beob = beob2 = "–"; n = n2 = 0
    if rn in RENNEN:
        v = V[rn]; d = v[(v.seg == 0) & (np.abs(v.teq - T) < 600)]; n = len(d); beob = hms(d.ziel.median())
        Tq = T * (en ** (1 / 0.93)) ** 0.07                                     # Anker-Zeit, wenn der Dauer-Term schon im Anker steckt
        d2 = v[(v.seg == 0) & (np.abs(v.teq - Tq) < 600)]; n2 = len(d2); beob2 = hms(d2.ziel.median())
    rows.append(dict(strecke=rn, heute=hms(T * ea), neu=hms(T * en), neu_dauer=hms(T * en ** (1 / 0.93)),
                     beobachtet_anker_3_30=f"{beob} (n={n})" if n else "–", beobachtet_mit_dauer=f"{beob2} (n={n2})" if n2 else "–"))
bsp = pd.DataFrame(rows); print(bsp.to_string(index=False)); bsp.to_csv(os.path.join(HIER, "beispiel_3_30.csv"), index=False)
print("   Brocken 2026 (nur Zielzeiten, davengo): schnellste 2:53:39, Median 4:42:12; Rennsteig: keine Daten")
