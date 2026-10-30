# Schätzt, wie stark die Steigungskosten der App (E⁺ bergauf, E⁻ bergab, je 5-km-Abschnitt, bei 1,0 s je Höhenmeter)
# in echten Zwischenzeiten sichtbar sind: log(relative Pace) = Ermüdung + kp·E⁺ + km·E⁻.
# kp = 1 heißt: 1,0 s je Höhenmeter stimmt; km = 1 heißt: „bergab die Hälfte“ stimmt.
# Liest zellen.csv (verdichten.py) und modell_seg9.json (modell_segmente.js). Bereiche in Klammern: 2,5–97,5 % aus
# 150 Bootstrap-Ziehungen über ganze Jahrgänge (fester Startwert, also wiederholbar). Ergebnis vom 30.10.2026: ergebnis.txt
import json, sys, numpy as np, pandas as pd
z = pd.read_csv("zellen.csv"); M = json.load(open("modell_seg9.json"))
NAME = {"Boston": "boston", "New York": "newyork", "London": "london", "Berlin": "berlin", "Chicago": "chicago", "Amsterdam": "amsterdam", "Valencia": "valencia", "Athens": "athen"}
assert all(M[a]["secRef"] == 1 and M[a]["ref"] == 240 for a in NAME.values())
# Abschnitt = Felder von..bis−1 im 9er-Raster (5 km, zuletzt 2,195 km); länger, wo einer Stadt eine Matte fehlt (Athen: 15–25)
LEN = np.array([5, 5, 5, 5, 5, 5, 5, 5, 2.195]); KUM = np.concatenate([[0], np.cumsum(LEN)])
mittel = lambda c, a, b, f: float(np.dot(LEN[a:b], [M[NAME[c]]["seg"][j][f] for j in range(a, b)]) / LEN[a:b].sum())
z["Ep"] = [mittel(c, a, b, "excAuf") for c, a, b in zip(z.city, z.von, z.bis)]
z["Em"] = [mittel(c, a, b, "excAb") for c, a, b in zip(z.city, z.von, z.bis)]
z["x"] = (KUM[z.von] + KUM[z.bis]) / 2 / 42.195
z["g"] = z.city + "|" + z.year.astype(str) + "|" + z.klasse.astype(str); z["ed"] = z.city + "|" + z.year.astype(str)
K = sorted(z.klasse.unique())
ALLE = z.copy(); z = ALLE[ALLE.city != "Athens"]   # die ersten drei Teile wie am 30.10.2026, ohne Athen

def fit(d, segs=range(9), staedte=None, nmax=1000, proKlasse=False, rng=None, y="med"):
    q = z[z.von.isin(list(segs)) & (z.bis - 1).isin(list(segs))]
    if staedte is not None: q = q[q.city.isin(staedte)]
    if rng is not None:   # Bootstrap: Jahrgänge mit Zurücklegen
        eds = q.ed.unique(); pick = rng.choice(eds, len(eds)); cnt = pd.Series(pick).value_counts()
        q = q[q.ed.isin(cnt.index)].copy(); q["rep"] = q.ed.map(cnt)
    else: q = q.copy(); q["rep"] = 1
    q = q.sort_values(["g", "von"])
    cols = {}
    for k in K:
        for s in segs: cols[f"a{k}_{s}"] = (q.klasse == k).to_numpy() * np.where((q.von <= s) & (s < q.bis), LEN[s] / (KUM[q.bis] - KUM[q.von]), 0)
    if proKlasse:
        for k in K: cols[f"kp{k}"] = (q.Ep * (q.klasse == k)).to_numpy(); 
        cols["km"] = q.Em.to_numpy()
    else: cols["kp"] = q.Ep.to_numpy(); cols["km"] = q.Em.to_numpy()
    A = np.column_stack(list(cols.values())); Y = q[y].to_numpy().copy()
    w = np.minimum(q.n.to_numpy(), nmax) * q.rep.to_numpy()
    if d >= 0:   # glatte Ermüdung je Gruppe herausrechnen (Frisch-Waugh): Projektion auf 1, x, x² je Gruppe
        gid = q.g.to_numpy(); xs = q.x.to_numpy()
        for g in np.unique(gid):
            i = np.where(gid == g)[0]; B = np.column_stack([xs[i] ** p for p in range(d + 1)])
            P = B @ np.linalg.pinv(B)
            Y[i] -= P @ Y[i]; A[i] -= P @ A[i]
    sw = np.sqrt(w); b = np.linalg.lstsq(A * sw[:, None], Y * sw, rcond=None)[0]
    res = dict(zip(cols, b)); return res

def zeige(titel, **kw):
    b = fit(**kw); rng = np.random.default_rng(1); bs = [fit(rng=rng, **kw) for _ in range(150)]
    out = []
    for k in [c for c in b if c.startswith("kp") or c == "km"]:
        v = np.array([r[k] for r in bs]); out.append(f"{k} {b[k]:.2f} [{np.percentile(v, 2.5):.2f}; {np.percentile(v, 97.5):.2f}]")
    print(f"{titel:44s}", " | ".join(out), flush=True)

print("== Alle Strecken")
zeige("Ohne Ermüdung je Jahrgang", d=-1)
zeige("Ermüdung linear je Jahrgang×Klasse", d=1)
zeige("Ermüdung quadratisch je Jahrgang×Klasse", d=2)
zeige("quadratisch, ohne 1. und letzten Abschnitt", d=2, segs=range(1, 8))
zeige("quadratisch, Mittelwert statt Median", d=2, y="mean")
for weg in ["Boston", "New York", "London", "Berlin", "Chicago"]:
    zeige(f"quadratisch, ohne {weg}", d=2, staedte=[c for c in NAME if c != weg])
zeige("quadratisch, je Leistungsklasse", d=2, proKlasse=True)

print("== Je hügelige Strecke gegen die flachen")
FLACH = ["Berlin", "Chicago", "Amsterdam", "Valencia"]
for h in ["Boston", "New York", "London"]:
    zeige(f"{h} + flache, quadratisch", d=2, staedte=[h] + FLACH)
    zeige(f"{h} + flache, linear", d=1, staedte=[h] + FLACH)
    zeige(f"{h} + flache, quadr., je Klasse", d=2, staedte=[h] + FLACH, proKlasse=True)

# New York: unser Profil steht bei km 25 auf dem Scheitel der Queensboro Bridge; liegt die Zeitmatte etwas anders, landet
# der Anstieg im falschen Abschnitt (Messfehler in E, drückt kp). Probe: die Abschnitte km 20–30 weglassen.
print("== New York ohne die Brückenabschnitte km 20–30")
voll = z.copy()
z = voll[~((voll.city == "New York") & voll.seg.isin([4, 5]))]
zeige("NY ohne km 20–30 + flache, quadratisch", d=2, staedte=["New York"] + FLACH)
z = voll[~((voll.city == "New York") & voll.seg.isin([0, 4, 5]))]
zeige("NY ohne km 0–5 und 20–30 + flache, quadr.", d=2, staedte=["New York"] + FLACH)
z = voll[~((voll.city == "New York") & voll.seg.isin([4, 5]))]
zeige("Boston + NY (ohne 20–30) + flache, quadr.", d=2, staedte=["Boston", "New York"] + FLACH)
zeige("dito, je Leistungsklasse", d=2, staedte=["Boston", "New York"] + FLACH, proKlasse=True)
zeige("alle (NY ohne 20–30), quadratisch", d=2)
zeige("alle (NY ohne 20–30), linear", d=1)

# Athen (App athen/ seit 30.10.2026): ein langer, glatter Anstieg km 10–31, dann bergab; im Datensatz nie eine 20-km-Zeit, daher
# km 15–25 als ein Abschnitt. Die glatte Ermüdung je Jahrgang kann einen so glatten Buckel zum Teil schlucken: daher alle drei Ansätze.
print("== Athen")
z = ALLE[~((ALLE.city == "New York") & ALLE.von.isin([4, 5]))]
for d, art in [(-1, "ohne Ermüdung je Jahrgang"), (1, "Ermüdung linear"), (2, "Ermüdung quadratisch")]:
    zeige(f"Athen + flache, {art}", d=d, staedte=["Athens"] + FLACH)
zeige("Athen + flache, linear, je Klasse", d=1, staedte=["Athens"] + FLACH, proKlasse=True)
zeige("alle mit Athen (NY ohne 20–30), quadratisch", d=2)
zeige("alle mit Athen (NY ohne 20–30), linear", d=1)
