# Eichung des Pace-Modells an Bergmarathons (Jungfrau 2024–2026, Zermatt 2025–2026, LGT Alpin 2026).
# Liest die Zeiten ohne Namen aus /tmp (laden.py), die Höhen aus den App-Daten (modell.py) und die Ermüdung flacher
# Marathons aus ../zellen.csv. Schreibt nur verdichtete Tabellen (Mediane je Zelle, mindestens 20 Läufer).
#   python3 auswerten.py /tmp/berg/roh [Bootstrap-Wiederholungen] > ergebnis.txt
import sys, os, json
import numpy as np, pandas as pd
from scipy.optimize import least_squares
import modell as M

ROH = sys.argv[1] if len(sys.argv) > 1 else "/tmp/berg/roh"
NBOOT = int(sys.argv[2]) if len(sys.argv) > 2 else 200
HIER = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20261031)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
L = 42195.0

# ---------------------------------------------------------------- Strecken und Messpunkte (Meter der App)
# roh: welche Spalten der Rangliste einen Abschnitt bilden (Jungfrau: Wilderswil–Zweilütschinen–Lauterbrunnen zusammen, weil
# die beiden sanften Abschnitte nur 101 bzw. 161 Höhenmeter haben und einzeln stark von der genauen Lage der Matte abhängen)
RENNEN = {
    "Jungfrau": dict(app="jungfrau", jahre=[2024, 2025, 2026], muster="jungfrau-marathon-{j}__{l}.csv", listen=("frauen", "maenner"),
                     grenzen=[0, 3300, 5000, 10400, 21100, 25900, 30700, 38500, L], roh=[[1], [2], [3], [4, 5], [6], [7], [8], [9]], anker=[1, 2],
                     namen=["Start–Runde Interlaken", "Runde–km 5", "km 5–Wilderswil", "Wilderswil–Lauterbrunnen", "Lauterbrunnen–Stocki",
                            "Stocki–Wengen", "Wengen–Wixi", "Wixi–Ziel"]),
    "Zermatt": dict(app="zermatt", jahre=[2025, 2026], muster="gornergrat-zermatt-marathon-{j}__{l}.csv", listen=("marathon-frauen", "marathon-maenner"),
                    grenzen=[0, 20600, 32000, 39100, L], roh=[[1], [2], [3], [4]], anker=[0],
                    namen=["Start–Zermatt", "Zermatt–Sunnegga", "Sunnegga–Riffelalp", "Riffelalp–Ziel"]),
    "LGT": dict(app="liechtenstein", jahre=[2026], muster="lgt-alpin-marathon-{j}__{l}.csv", listen=("marathon-frauen", "marathon-maenner"),
                grenzen=[0, 10070, 25480, L], roh=[[1], [2], [3]], anker=[0], namen=["Start–Vaduz", "Vaduz–Steg", "Steg–Ziel"]),
}
KANTEN = [0, 5, 10, 15, 20, 100]
KNAMEN = ["0–5 %", "5–10 %", "10–15 %", "15–20 %", "> 20 %"]
GMITTE = np.array([2.5, 7.5, 12.5, 17.5, 25.0])

# ---------------------------------------------------------------- Raster je Strecke (10 m, wie der Kern)
for rn, R in RENNEN.items():
    S = M.lade(R["app"]); R["S"] = S
    g = S.win[100]["g"]; gm = (g[:-1] + g[1:]) / 2
    fr = S.ratio(); f_app = (fr[:-1] + fr[1:]) / 2
    R["gm"] = gm; R["xm"] = (S.x[:-1] + S.x[1:]) / 2; R["hm"] = (S.H[:-1] + S.H[1:]) / 2; R["fapp"] = f_app
    R["hmcum"] = np.concatenate([[0], np.cumsum(np.maximum(0, gm) / 100 * S.STEP)])[:-1]   # Höhenmeter bis hier (100-m-Fenster)
    R["seg"] = np.digitize(R["xm"], R["grenzen"][1:-1]); R["seg"][R["xm"] >= L] = -1
    R["kl"] = np.clip(np.digitize(gm, KANTEN[1:-1]), 0, 4)
    R["ns"] = len(R["grenzen"]) - 1

def faktor(R, th):
    """Pace-Faktor je 10-m-Stück. th: dict mit
       a   – Faktor auf die App-Kurve bergauf (1 = App)
       k   – oder eigene Flach-m je Höhenmeter je Steigungsklasse (5 Werte, ersetzt a)
       c   – Zuschlag in Flach-m je Höhenmeter je 10 % Steigung über 10 % („Knick“)
       ab  – Faktor auf die Bergab-Kurve der App (1 = „halb“)
       hoe – Zuschlag auf die Pace je 1000 m Höhe über dem Meer (App für Mexiko: 0,062/2,24 = 0,028)
       ger – Zuschlag auf die Pace je 1000 Höhenmeter, die man schon gestiegen ist („Bergermüdung“, überall)
       gauf – nur der Bergauf-Aufschlag wächst je 1000 schon gestiegene Höhenmeter um diesen Anteil"""
    gm, f = R["gm"], R["fapp"]; up = gm > 0
    zus = np.where(up, f - 1, 0.0)
    if th.get("k") is not None:
        k = np.asarray(th["k"]); zus = np.where(up, k[R["kl"]] * gm / 100, 0.0)
        zus = np.where(up & (gm < 1), (f - 1) * k[0] / K_APP[0], zus)    # Übergang bei 0 wie im Kern
    else:
        zus = zus * th.get("a", 1.0)
    zus = zus + np.where(up, th.get("c", 0.0) * np.maximum(0, gm - 10) / 10 * gm / 100, 0.0)
    if th.get("gauf"): zus = np.where(up, zus * (1 + th["gauf"] * R["hmcum"] / 1000), zus)
    zus = zus + np.where(~up, th.get("ab", 1.0) * (f - 1), 0.0)
    p = 1 + zus
    if th.get("hoe"): p = p * (1 + th["hoe"] * R["hm"] / 1000)
    if th.get("ger"): p = p * (1 + th["ger"] * R["hmcum"] / 1000)
    return p

def E_seg(R, th):
    p = faktor(R, th) * R["S"].STEP; s = R["seg"]
    return np.array([p[s == i].sum() for i in range(R["ns"])])

def k_app_klassen():
    num = np.zeros(5); den = np.zeros(5)
    for R in RENNEN.values():
        for c in range(5):
            m = (R["kl"] == c) & (R["gm"] > 0); num[c] += ((R["fapp"] - 1) * 10)[m].sum(); den[c] += (R["gm"] / 100 * 10)[m].sum()
    return num / den
K_APP = k_app_klassen()
def k_min_klassen():
    num = np.zeros(5); den = np.zeros(5)
    for R in RENNEN.values():
        for c in range(5):
            m = (R["kl"] == c) & (R["gm"] > 0.01); num[c] += ((M.minetti(R["gm"][m] / 100) / 3.6 - 1) * 10).sum(); den[c] += (R["gm"][m] / 100 * 10).sum()
    return num / den
K_MIN = k_min_klassen()

# ---------------------------------------------------------------- Ermüdung flacher Marathons (zellen.csv)
z = pd.read_csv(os.path.join(HIER, "..", "zellen.csv"))
zf = z[z.city.isin(["Berlin", "Chicago", "Amsterdam", "Valencia"])]
YK = zf.groupby(["klasse", "von"]).apply(lambda d: np.average(d.med, weights=d.n), include_groups=False).unstack().values   # 11 × 9
T_KL = np.array([2.6, 2.875, 3.125, 3.375, 3.625, 3.875, 4.25, 4.75, 5.25, 5.75, 6.4]) * 3600
MID = np.array([2.5, 7.5, 12.5, 17.5, 22.5, 27.5, 32.5, 37.5, 41.1]) * 1000
XG = np.arange(0, L + 1, 50.0)
TG = np.arange(2.2, 7.01, 0.05) * 3600
def profil(T):
    y = np.array([np.interp(T, T_KL, YK[:, j]) for j in range(9)]); Y = np.interp(XG, MID, y)
    return Y - np.log(np.trapezoid(np.exp(Y), XG) / L)
PROF = np.array([profil(T) for T in TG])
KUM = np.array([np.concatenate([[0], np.cumsum((np.exp(P[:-1]) + np.exp(P[1:])) / 2 * 50)]) for P in PROF])
T_EINH = 3.25 * 3600                                   # einheitliches Profil: flacher Marathon um 3:15
TI_EINH = int(round((T_EINH - TG[0]) / (TG[1] - TG[0])))
def phi_km(ti, a, b):
    ti = np.atleast_1d(ti)
    return np.log((np.array([np.interp(b, XG, KUM[t]) for t in ti]) - np.array([np.interp(a, XG, KUM[t]) for t in ti])) / (b - a))
TAU = np.linspace(0, 1, 2001)
GTAU = []
for P, K in zip(PROF, KUM):
    x_tau = np.interp(TAU, K / K[-1], XG); m = np.exp(np.interp(x_tau, XG, P))
    GTAU.append(np.concatenate([[0], np.cumsum((m[:-1] + m[1:]) / 2 * np.diff(TAU))]))
GTAU = np.array(GTAU)
def phi_zeit(ti, ta, tb):
    i0 = np.clip(np.searchsorted(TAU, ta), 0, 2000); i1 = np.clip(np.searchsorted(TAU, tb), 0, 2000)
    return np.log((GTAU[ti, i1] - GTAU[ti, i0]) / np.maximum(tb - ta, 1e-6))

# ---------------------------------------------------------------- Läufer einlesen (nur Zeiten)
TH_APP = {}
def lies(rn, R):
    out = []
    for j in R["jahre"]:
        for l in R["listen"]:
            f = os.path.join(ROH, R["muster"].format(j=j, l=l))
            if os.path.exists(f): d = pd.read_csv(f); d["jahr"] = j; out.append(d)
            else: print("fehlt", f)
    d = pd.concat(out, ignore_index=True)
    Traw = d[[c for c in d.columns if c.startswith("s")]].to_numpy(float)
    ok = np.isfinite(Traw).all(axis=1) & (Traw > 0).all(axis=1) & np.isfinite(d.ziel.to_numpy(float))
    ok &= np.abs(Traw.sum(axis=1) - d.ziel.to_numpy(float)) < 60   # Zermatt: Etappen bis 21 s kürzer als die Zielzeit (Startverzug)
    T = np.column_stack([Traw[:, [i - 1 for i in grp]].sum(axis=1) for grp in R["roh"]])
    Eapp = E_seg(R, TH_APP)
    r = (T / Eapp) / (T.sum(axis=1, keepdims=True) / Eapp.sum())
    ok2 = ok & (r > 0.45).all(axis=1) & (r < 3.0).all(axis=1)
    print(f"{rn}: {len(d)} Zeilen, im Ziel mit allen Zeiten {ok.sum()}, plausibel {ok2.sum()}")
    return d[ok2].reset_index(drop=True), T[ok2]
DAT = {rn: lies(rn, R) for rn, R in RENNEN.items()}

# ---------------------------------------------------------------- Anker, Klasse, Ermüdung je Läufer
KL_GR = np.array([0, 3.25, 3.75, 4.25, 4.75, 99]) * 3600
KL_N = ["< 3:15", "3:15–3:45", "3:45–4:15", "4:15–4:45", "≥ 4:45"]

def vorbereiten(th_anker):
    out = {}
    for rn, R in RENNEN.items():
        d, T = DAT[rn]; an = R["anker"]; gr = R["grenzen"]; n = len(d)
        ta = T[:, an].sum(axis=1); Es = E_seg(R, th_anker); Ea = Es[an].sum()
        p0 = ta / Ea                                                       # s je flacher Meter im Anker
        a0, b0 = gr[an[0]], gr[an[-1] + 1]
        # Klasse: flache Marathonzeit mit dem einheitlichen Profil (3:15), für alle Varianten gleich
        Teq = p0 * L * np.exp(-phi_km(TI_EINH, a0, b0)[0])
        ti = np.clip(np.round((Teq - TG[0]) / (TG[1] - TG[0])).astype(int), 0, len(TG) - 1)
        # klassenabhängig: Äquivalenzzeit mit dem eigenen Profil (iteriert)
        phiA = np.zeros(n)
        for _ in range(4):
            Tk = p0 * L * np.exp(-phiA); tk = np.clip(np.round((Tk - TG[0]) / (TG[1] - TG[0])).astype(int), 0, len(TG) - 1); phiA = phi_km(tk, a0, b0)
        cum = np.concatenate([np.zeros((n, 1)), np.cumsum(T, axis=1)], axis=1) / T.sum(axis=1, keepdims=True)
        phiAz = phi_zeit(tk, cum[:, an[0]], cum[:, an[-1] + 1])
        phiAe = phi_km(TI_EINH, a0, b0)[0]
        rec = []
        for s in range(R["ns"]):
            y = np.log(T[:, s] / ta)
            fe = phi_km(TI_EINH, gr[s], gr[s + 1])[0] - phiAe
            fk = phi_km(tk, gr[s], gr[s + 1]) - phiA
            fz = phi_zeit(tk, cum[:, s], cum[:, s + 1]) - phiAz
            rec.append(pd.DataFrame({"rennen": rn, "jahr": d.jahr, "id": np.arange(n), "g": d.g, "seg": s, "teq": Teq, "tk": Tk,
                                     "klasse": np.digitize(Teq, KL_GR) - 1, "ziel": d.ziel,
                                     "y": y, "ye": y - fe, "yk": y - fk, "yz": y - fz, "fk": fk, "fe": fe}))
        out[rn] = pd.concat(rec, ignore_index=True)
    return out

def zellen(V, ids=None, nmin=20):
    teile = []
    for rn, v in V.items():
        if ids is not None:
            ns = RENNEN[rn]["ns"]; nrun = len(v) // ns
            v = pd.concat([v.iloc[ids[rn] + s * nrun] for s in range(ns)], ignore_index=True)
        g = v.groupby(["rennen", "jahr", "klasse", "seg"])
        teile.append(pd.DataFrame({"n": g.size(), "y": g.y.median(), "ye": g.ye.median(), "yk": g.yk.median(), "yz": g.yz.median(),
                                   "fk": g.fk.median(), "fe": g.fe.median(), "teq": g.teq.median(), "ziel": g.ziel.median()}).reset_index())
    c = pd.concat(teile, ignore_index=True)
    return c[c.n >= nmin].reset_index(drop=True)

# ---------------------------------------------------------------- Modelle
MODELLE = {   # Name: (freie Größen, Startwerte, feste Größen)
    "App-Kurve × a":                 (["a"], [1.5], {}),
    "App × a + Knick c":             (["a", "c"], [1.0, 1.0], {}),
    "App × a + Höhe":                (["a", "hoe"], [1.0, 0.03], {}),
    "App × a + Bergermüdung":        (["a", "ger"], [1.0, 0.05], {}),
    "App × a + Knick + Bergermüdung": (["a", "c", "ger"], [1.0, 1.0, 0.05], {}),
    "App + Bergermüdung (a = 1)":    (["ger"], [0.1], {"a": 1.0}),
    "App, Aufschlag wächst (a = 1)": (["gauf"], [0.5], {"a": 1.0}),
    "App, Aufschlag wächst + Höhe wie Mexiko": (["gauf"], [0.5], {"a": 1.0, "hoe": 0.062 / 2.24}),
    "App × a, Aufschlag wächst":     (["a", "gauf"], [1.0, 0.5], {}),
    "App × a + Knick, Aufschlag wächst": (["a", "c", "gauf"], [1.0, 1.0, 0.5], {}),
    "Klassen monoton, 0–5 % = App":  (["d1", "d2", "d3", "d4"], [1, 1, 1, 1], {}),
    "Klassen monoton + Bergermüdung": (["d1", "d2", "d3", "d4", "ger"], [0.5, 0.5, 0.5, 0.5, 0.05], {}),
    "Klassen monoton, Aufschlag wächst": (["d1", "d2", "d3", "d4", "gauf"], [0.5, 0.5, 0.5, 0.5, 0.5], {}),
}
GRENZEN_P = {"a": (0.2, 6), "c": (0, 30), "hoe": (0, 0.5), "ger": (0, 1.0), "gauf": (0, 5.0), "ab": (0, 4), "d1": (0, 30), "d2": (0, 30), "d3": (0, 30), "d4": (0, 30)}

def th_aus(namen, p, fest):
    th = dict(fest); th.update(zip(namen, p))
    if "d1" in th:   # monotone Klassen: 0–5 % wie die App, darüber Zuwächse ≥ 0
        k = [K_APP[0]]; [k.append(k[-1] + th.pop(f"d{i}")) for i in range(1, 5)]; th["k"] = np.array(k)
    return th

def fit(c, modell, spalte="ye", klassen=None, ab=1.0, ohne=None):
    namen, start, fest = MODELLE[modell]; fest = dict(fest); fest["ab"] = ab
    c = c[np.array([s not in RENNEN[r]["anker"] for r, s in zip(c.rennen, c.seg)], bool)]
    if klassen is not None: c = c[c.klasse.isin(list(klassen))]
    if ohne is not None: c = c[~ohne(c)]
    grp = {rn: (c.rennen == rn).to_numpy() for rn in RENNEN}
    yv = c[spalte].to_numpy(); w = np.sqrt(np.minimum(c.n.to_numpy(), 200)); sg = c.seg.to_numpy()
    def pred(th):
        out = np.zeros(len(c))
        for rn, R in RENNEN.items():
            m = grp[rn]
            if m.any(): Es = E_seg(R, th); out[m] = np.log(Es[sg[m]] / Es[R["anker"]].sum())
        return out
    lo = [GRENZEN_P[n][0] for n in namen]; hi = [GRENZEN_P[n][1] for n in namen]
    r = least_squares(lambda p: w * (pred(th_aus(namen, p, fest)) - yv), start, bounds=(lo, hi), x_scale="jac")
    th = th_aus(namen, r.x, fest)
    return th, dict(zip(namen, r.x)), c.assign(pred=pred(th)), float(np.sum(r.fun ** 2) / np.sum(w ** 2))

def k_kurve(th):
    """Flach-m je Höhenmeter je Steigungsklasse (über die drei Strecken gemittelt), ohne Höhe und Bergermüdung"""
    if th.get("k") is not None: k = np.asarray(th["k"], float)
    else: k = th.get("a", 1.0) * K_APP
    return k + th.get("c", 0.0) * np.maximum(0, GMITTE - 10) / 10

# ================================================================= Ausgabe
print("\n== Abschnitte (Höhen der App; ↑/↓ mit 200-m-Fenster wie in den Übergaben; Höhenmeter je Steigungsklasse und Steigung mit 100 m wie das Modell)")
geo_rows = []
for rn, R in RENNEN.items():
    Es = E_seg(R, TH_APP); S = R["S"]
    for s, nm in enumerate(R["namen"]):
        m = R["seg"] == s; up = m & (R["gm"] > 0); dh = R["gm"] / 100 * 10
        ab = S.abschnitt(R["grenzen"][s], R["grenzen"][s + 1], 200)
        geo_rows.append(dict(rennen=rn, seg=s, abschnitt=nm, km=f"{R['grenzen'][s] / 1000:.1f}–{R['grenzen'][s + 1] / 1000:.1f}",
                             h0=round(ab["h0"]), h1=round(ab["h1"]), auf200=round(ab["auf"]), ab200=round(ab["ab"]),
                             **{f"hm_{k}": round(dh[up & (R["kl"] == i)].sum()) for i, k in enumerate(["0_5", "5_10", "10_15", "15_20", "20p"])},
                             steigung_hm_gew=round(float((R["gm"][up] * dh[up]).sum() / max(dh[up].sum(), 1)), 1),
                             hm_vorher=round(float(R["hmcum"][m].mean())), app_faktor=round(Es[s] / (R["grenzen"][s + 1] - R["grenzen"][s]), 3),
                             anker=s in R["anker"]))
geo = pd.DataFrame(geo_rows); print(geo.drop(columns="seg").to_string(index=False))
geo.to_csv(os.path.join(HIER, "abschnitte.csv"), index=False)
print("\nApp-Modell, wirksame Flach-m je Höhenmeter je Steigungsklasse (Mittel über die drei Strecken):", "  ".join(f"{n} {k:.2f}" for n, k in zip(KNAMEN, K_APP)))
print("Minetti (Labor, gleiche Energie):                                                  ", "  ".join(f"{n} {k:.2f}" for n, k in zip(KNAMEN, K_MIN)))

V = vorbereiten(TH_APP)
C = zellen(V)
print("\n== Läufer je Rennen, Jahr und Klasse (Klasse = flache Marathonzeit aus der Pace im Anker, Ermüdung wie ein 3:15-Läufer)")
nt = C[C.seg == 0].pivot_table(index=["rennen", "jahr"], columns="klasse", values="n", aggfunc="sum").rename(columns=dict(enumerate(KL_N)))
print(nt.fillna(0).astype(int).to_string())
alle = pd.concat([V[rn][V[rn].seg == 0] for rn in V])
print("\nMediane je Klasse: Zielzeit, flache Äquivalenzzeit (einheitlich / mit klasseneigener Ermüdung) [h]")
print(alle.groupby(["rennen", "klasse"]).agg(n=("ziel", "size"), ziel=("ziel", lambda x: round(x.median() / 3600, 2)),
                                             teq=("teq", lambda x: round(x.median() / 3600, 2)), teq_klasse=("tk", lambda x: round(x.median() / 3600, 2)))
      .rename(index=dict(enumerate(KL_N)), level=1).to_string())

cz = C.copy(); cz["klasse_teq"] = cz.klasse.map(dict(enumerate(KL_N)))
cz["abschnitt"] = [RENNEN[r]["namen"][s] for r, s in zip(cz.rennen, cz.seg)]
cz[["rennen", "jahr", "klasse", "klasse_teq", "seg", "abschnitt", "n", "teq", "ziel", "y", "ye", "yk", "yz", "fe", "fk"]].round(5) \
    .to_csv(os.path.join(HIER, "zellen_berg.csv"), index=False)

# ---- Kontrolle Ermüdung am flachen Abschnitt Jungfrau km 21,1–25,9
print("\n== Kontrolle: Jungfrau km 21,1–25,9 (flach), Pace gegen den Anker in % nach Abzug des Modells, und die Ermüdung flacher Marathons")
Es = E_seg(RENNEN["Jungfrau"], TH_APP); Ea = Es[RENNEN["Jungfrau"]["anker"]].sum()
j6 = C[(C.rennen == "Jungfrau") & (C.seg == 4)]
j6 = j6.assign(beob=100 * (j6.y - np.log(Es[4] / Ea)), flach_einheitlich=100 * j6.fe, flach_klasse=100 * j6.fk)
print(j6.pivot_table(index="klasse", columns="jahr", values=["beob", "flach_einheitlich", "flach_klasse"]).round(1).rename(index=dict(enumerate(KL_N))).to_string())

# ---- je Abschnitt: wirksame Flach-m je Höhenmeter (Anker und Bergab wie App)
def k_beob(c, spalte):
    rows = []
    for rn, R in RENNEN.items():
        Es = E_seg(R, TH_APP); Ea = Es[R["anker"]].sum(); m0 = R["seg"]
        for s in range(R["ns"]):
            if s in R["anker"]: continue
            m = m0 == s; up = m & (R["gm"] > 0); U = (R["gm"] / 100 * 10)[up].sum()
            if U < 100: continue
            Ln = 10.0 * m.sum(); Dn = ((R["fapp"] - 1) * 10)[m & (R["gm"] <= 0)].sum()
            cc = c[(c.rennen == rn) & (c.seg == s)]
            for _, r in cc.iterrows():
                Eo = Ea * np.exp(r[spalte])
                rows.append(dict(rennen=rn, seg=s, jahr=r.jahr, klasse=r.klasse, n=r.n, k=(Eo - Ln - Dn) / U, k_app=(Es[s] - Ln - Dn) / U,
                                 faktor=Eo / Es[s]))
    return pd.DataFrame(rows)
SPALTEN = {"ye": "Ermüdung einheitlich (3:15-Profil)", "y": "ohne Ermüdung", "yk": "Ermüdung je Klasse nach km", "yz": "Ermüdung je Klasse nach Zeitanteil"}
KB = {}
for sp, titel in SPALTEN.items():
    kb = k_beob(C, sp); KB[sp] = kb
    t = kb.groupby(["rennen", "seg", "klasse"]).apply(lambda d: np.average(d.k, weights=d.n), include_groups=False).unstack("klasse")
    t.columns = [KL_N[k] for k in t.columns]
    alle_k = kb.groupby(["rennen", "seg"]).apply(lambda d: np.average(d.k, weights=d.n), include_groups=False)
    t.insert(0, "alle", alle_k); t.insert(0, "App", kb.groupby(["rennen", "seg"]).k_app.first())
    t.insert(0, "Höhenmeter vorher", [geo[(geo.rennen == r) & (geo.seg == s)].hm_vorher.iloc[0] for r, s in t.index])
    t.insert(0, "Steigung %", [geo[(geo.rennen == r) & (geo.seg == s)].steigung_hm_gew.iloc[0] for r, s in t.index])
    t.index = [f"{r} {RENNEN[r]['namen'][s]}" for r, s in t.index]
    t = t.sort_values("Steigung %")
    print(f"\n== Flach-m je Höhenmeter bergauf je Abschnitt ({titel}); Steigung = Höhenmeter-gewichtetes Mittel bergauf")
    print(t.round(1).to_string())
    if sp == "ye": t.round(2).to_csv(os.path.join(HIER, "k_abschnitte.csv"))

# ---- Modelle vergleichen (alle Klassen zusammen)
print("\n== Modelle (alle Läufer; Ermüdung einheitlich; bergab wie App): mittlerer quadratischer Fehler je Zelle und Parameter")
FITS = {}
for mn in MODELLE:
    th, p, cf, mse = fit(C, mn); FITS[mn] = (th, p, cf, mse)
    # Weglassen je Rennen: aus den anderen schätzen, am weggelassenen prüfen
    loro = []
    for rn in RENNEN:
        th2, _, _, _ = fit(C, mn, ohne=lambda c, rn=rn: c.rennen == rn)
        cc = C[(C.rennen == rn).to_numpy() & np.array([s not in RENNEN[rn]["anker"] for s in C.seg])]
        Es = E_seg(RENNEN[rn], th2); pr = np.log(Es[cc.seg.to_numpy()] / Es[RENNEN[rn]["anker"]].sum())
        loro.append(f"{rn} {100 * np.median(pr - cc.ye):+.1f} %")
    print(f"  {mn:32s} RMS {100 * np.sqrt(mse):4.1f} % | " + ", ".join(f"{k} {v:.3f}" for k, v in p.items())
          + " | k: " + " ".join(f"{x:.1f}" for x in k_kurve(th)) + " | ohne je Rennen, Fehler dort: " + "; ".join(loro))

print("\n== Abweichung Modell − beobachtet je Abschnitt (Median über Jahre und Klassen, %)")
tab = {}
c0 = FITS["App-Kurve × a"][2]
Es_app = {rn: E_seg(R, TH_APP) for rn, R in RENNEN.items()}
tab["App"] = [100 * np.median(np.log(Es_app[r][s] / Es_app[r][RENNEN[r]["anker"]].sum()) - c0[(c0.rennen == r) & (c0.seg == s)].ye)
              for r, s in sorted(set(zip(c0.rennen, c0.seg)))]
for mn in MODELLE:
    cf = FITS[mn][2]; tab[mn] = [100 * np.median((cf.pred - cf.ye)[(cf.rennen == r) & (cf.seg == s)]) for r, s in sorted(set(zip(c0.rennen, c0.seg)))]
tab = pd.DataFrame(tab, index=[f"{r} {RENNEN[r]['namen'][s]}" for r, s in sorted(set(zip(c0.rennen, c0.seg)))])
print(tab.round(1).to_string())

# ---- je Leistungsklasse und Variante, mit Bootstrap
def boot_ids():
    ids = {}
    for rn, v in V.items():
        d = v[v.seg == 0]; ids[rn] = np.concatenate([rng.choice(dj.id.to_numpy(), len(dj), replace=True) for _, dj in d.groupby("jahr")])
    return ids
AUFGABEN = []   # (Modell, Spalte, Klassen, Etikett)
for mn in ["App-Kurve × a", "App, Aufschlag wächst (a = 1)", "App × a, Aufschlag wächst", "Klassen monoton, Aufschlag wächst"]:
    for sp in ["ye", "y", "yk", "yz"]:
        if mn == "Klassen monoton, Aufschlag wächst" and sp != "ye": continue
        AUFGABEN.append((mn, sp, None, "alle"))
        if mn in ("App-Kurve × a", "App, Aufschlag wächst (a = 1)"):
            for k in range(5): AUFGABEN.append((mn, sp, (k,), KL_N[k]))
ERG = {a: fit(C, a[0], a[1], a[2]) for a in AUFGABEN}
BOOT = {a: [] for a in AUFGABEN}
for b in range(NBOOT):
    cb = zellen(V, boot_ids())
    for a in AUFGABEN:
        try: BOOT[a].append(fit(cb, a[0], a[1], a[2]))
        except Exception as e: pass
    if (b + 1) % 20 == 0: print(f"  Bootstrap {b + 1}/{NBOOT}", file=sys.stderr)

def pct(x): return np.percentile(np.array(x), [2.5, 97.5], axis=0)
rows = []
print(f"\n== Flach-m je Höhenmeter bergauf nach Steigungsklasse und Leistungsklasse (ohne Höhe/Bergermüdung bzw. mit), 95 % aus {NBOOT} Bootstrap-Ziehungen über Läufer")
print("   App      ", "  ".join(f"{n} {k:.1f}" for n, k in zip(KNAMEN, K_APP)))
print("   Minetti  ", "  ".join(f"{n} {k:.1f}" for n, k in zip(KNAMEN, K_MIN)))
for a in AUFGABEN:
    th, p, _, mse = ERG[a]; kk = k_kurve(th); kb = np.array([k_kurve(x[0]) for x in BOOT[a]]); lo, hi = pct(kb)
    pz = "  ".join(f"{k} {v:.3f} [{pct([x[1][k] for x in BOOT[a]])[0]:.3f}–{pct([x[1][k] for x in BOOT[a]])[1]:.3f}]" for k, v in p.items() if not k.startswith("d"))
    print(f"-- {a[0]:31s} {SPALTEN[a[1]][:26]:26s} {a[3]:10s} " + "  ".join(f"{n} {kk[i]:.1f} [{lo[i]:.1f}–{hi[i]:.1f}]" for i, n in enumerate(KNAMEN)) + "  | " + pz)
    for i, n in enumerate(KNAMEN): rows.append(dict(modell=a[0], ermuedung=SPALTEN[a[1]], gruppe=a[3], groesse=n, wert=kk[i], lo=lo[i], hi=hi[i]))
    for k, v in p.items():
        if not k.startswith("d"):
            l2, h2 = pct([x[1][k] for x in BOOT[a]]); rows.append(dict(modell=a[0], ermuedung=SPALTEN[a[1]], gruppe=a[3], groesse=k, wert=v, lo=l2, hi=h2))
pd.DataFrame(rows).round(3).to_csv(os.path.join(HIER, "ergebnis_steigung.csv"), index=False)

print("\n== Langsamere gegen schnellere: Parameter je Leistungsklasse, Differenz zu 3:15–3:45 (gepaarter Bootstrap)")
for mn, par in (("App-Kurve × a", "a"), ("App, Aufschlag wächst (a = 1)", "gauf")):
    for sp in ["ye", "y", "yk", "yz"]:
        ref = np.array([x[1][par] for x in BOOT[(mn, sp, (1,), KL_N[1])]])
        zeile = []
        for k in range(5):
            a = (mn, sp, (k,), KL_N[k])
            if a not in ERG: continue
            v = np.array([x[1][par] for x in BOOT[a]]); n = min(len(v), len(ref)); d = v[:n] - ref[:n]
            zeile.append(f"{KL_N[k]} {ERG[a][1][par]:.2f} (Δ {np.median(d):+.2f} [{np.percentile(d, 2.5):+.2f}; {np.percentile(d, 97.5):+.2f}])")
        print(f"  {mn[:22]:22s} {par:4s} {SPALTEN[sp][:30]:30s} " + " | ".join(zeile))

# ---- Bergab frei (Gegenprobe)
print("\n== Bergab frei geschätzt (Faktor auf die App-Kurve bergab; 1 = „halb“), Modell App-Kurve × a, Ermüdung einheitlich")
for ab0 in (0.0, 0.5, 1.0, 1.5, 2.0):
    th, p, cf, mse = fit(C, "App-Kurve × a", ab=ab0)
    print(f"  bergab ×{ab0:.1f}: a = {p['a']:.3f}, RMS {100 * np.sqrt(mse):.2f} %")

# ---- Halbmarathon Zermatt (frisch ab Zermatt, gleiche Linie)
print("\n== Zermatt: Marathon (ab km 20,6) gegen Halbmarathon (dieselbe Linie, frisch), gleiche Zeit Zermatt–Sunnegga")
hm = []
for j in (2025, 2026):
    for l in ("halbmarathon-frauen", "halbmarathon-maenner"):
        f = os.path.join(ROH, f"gornergrat-zermatt-marathon-{j}__{l}.csv")
        if os.path.exists(f): d = pd.read_csv(f); d["jahr"] = j; hm.append(d)
if hm:
    h = pd.concat(hm); h = h[h[["s1", "s2", "s3"]].notna().all(axis=1) & h.ziel.notna()]
    h = h[np.abs(h[["s1", "s2", "s3"]].sum(axis=1) - h.ziel) < 5]
    dz, Tz = DAT["Zermatt"]; mar = pd.DataFrame({"s1": Tz[:, 1], "s2": Tz[:, 2], "s3": Tz[:, 3]})
    q = np.percentile(mar.s1, [20, 40, 60, 80])
    rows = []
    for nm, d in (("Marathon", mar), ("Halbmarathon", h)):
        d = d.assign(q=np.digitize(d.s1, q))
        for k, dk in d.groupby("q"):
            rows.append(dict(gruppe=f"Q{k + 1}", rennen=nm, n=len(dk), zermatt_sunnegga_min=round(dk.s1.median() / 60, 1),
                             sunnegga_riffelalp_rel=round(np.median(dk.s2 / dk.s1), 3), riffelalp_ziel_rel=round(np.median(dk.s3 / dk.s1), 3)))
    hmt = pd.DataFrame(rows); print(hmt.to_string(index=False)); hmt.to_csv(os.path.join(HIER, "zermatt_halbmarathon.csv"), index=False)
    # Test ohne Halbmarathondaten in der Schätzung: Verhältnisse, die die Modelle vorhersagen (Halbmarathon: Höhenmeter ab Zermatt)
    Rz = RENNEN["Zermatt"]; i0 = int(20600 / 10)
    print("   Vorhersage der Modelle für Riffelalp–Ziel / Zermatt–Sunnegga und Sunnegga–Riffelalp / Zermatt–Sunnegga (Marathon | Halbmarathon):")
    for mn in ["App-Kurve × a", "App × a + Bergermüdung", "App, Aufschlag wächst (a = 1)", "App × a, Aufschlag wächst"]:
        th = FITS[mn][0]; Em = E_seg(Rz, th)
        alt = Rz["hmcum"].copy(); Rz["hmcum"] = np.maximum(0, alt - alt[i0]); Eh = E_seg(Rz, th); Rz["hmcum"] = alt
        print(f"     {mn:32s} {Em[3] / Em[1]:.3f} | {Eh[3] / Eh[1]:.3f}    {Em[2] / Em[1]:.3f} | {Eh[2] / Eh[1]:.3f}")

# ---- Prognosen
def hms(s): s = int(round(s)); return f"{s // 3600}:{s % 3600 // 60:02d}"
def zielzeit(rn, th, Teq):
    """gleichmäßige Anstrengung wie die App: Zielzeit = Schnitt eines flachen Marathons × gewichtete Strecke"""
    return Teq / L * E_seg(RENNEN[rn], th).sum()
print("\n== Prognosen der Zielzeit (gleichmäßige Anstrengung wie in der App) gegen den Median der Läufer mit dieser flachen Äquivalenzzeit (±10 min)")
VORSCHLAG = {}
for mn in ["App-Kurve × a", "App × a + Bergermüdung", "App, Aufschlag wächst (a = 1)", "App × a, Aufschlag wächst", "Klassen monoton, Aufschlag wächst"]:
    VORSCHLAG[mn] = FITS[mn][0]
prog = []
for Teq in np.array([2.5, 2.75, 3.0, 3.5, 4.0, 4.5, 5.0]) * 3600:
    for rn in RENNEN:
        v = V[rn]; d = v[(v.seg == 0) & (np.abs(v.teq - Teq) < 600)]
        z = dict(flach=hms(Teq), rennen=rn, n=len(d), beobachtet=hms(d.ziel.median()) if len(d) >= 10 else "–",
                 viertel=f"{hms(d.ziel.quantile(0.25))}–{hms(d.ziel.quantile(0.75))}" if len(d) >= 10 else "–", App=hms(zielzeit(rn, TH_APP, Teq)))
        for mn, th in VORSCHLAG.items(): z[mn] = hms(zielzeit(rn, th, Teq))
        prog.append(z)
prog = pd.DataFrame(prog); print(prog.to_string(index=False)); prog.to_csv(os.path.join(HIER, "prognosen.csv"), index=False)

# Spitze: die schnellsten 5 je Rennen und Jahr (nur Zeiten, Median), mit ihrer Äquivalenzzeit
print("\n== Spitze: Median der 5 schnellsten Zielzeiten je Rennen und Jahr, ihre flache Äquivalenzzeit aus dem Anker und das App-Modell")
for rn in RENNEN:
    v = V[rn]; d0 = v[v.seg == 0]
    for j, dj in d0.groupby("jahr"):
        for g, dg in dj.groupby("g"):
            t5 = dg.nsmallest(5, "ziel")
            print(f"  {rn} {j} {g}: Ziel {hms(t5.ziel.median())}, Äquivalenz {hms(t5.teq.median())}, Verhältnis {t5.ziel.median() / t5.teq.median():.2f},"
                  f" App bei dieser Zeit {hms(zielzeit(rn, TH_APP, t5.teq.median()))}")

json.dump({"K_APP": K_APP.tolist(), "K_MIN": K_MIN.tolist(),
           "modelle": {mn: {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in FITS[mn][0].items()} for mn in MODELLE}},
          open(os.path.join(HIER, "parameter.json"), "w"), indent=1)
