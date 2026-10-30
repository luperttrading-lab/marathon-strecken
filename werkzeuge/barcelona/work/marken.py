# Kilometermarken aus dem Streckenplan (plan.py: 42 Kästchen, Ziffern nur als Umrisse) auf die Linie (linie.py).
# Die Kästchen stehen auf oder neben der Planlinie, auf der Diagonal neben der Hin- bzw. Rücklinie, die der Plan nebeneinander
# zeichnet. Deshalb im Plan selbst: jedes Kästchen auf die Planlinie projiziert (mögliche Stellen: jedes Stück der Planlinie
# höchstens 130 pt daneben), die Stelle auf der Planlinie über die Wegmarken (wegmarken.json: Planstelle <-> Linienmeter) stückweise
# linear in Linienmeter umgerechnet. Zuordnung zu km 1–42 siehe unten (Viterbi). Gegenprobe: ../dl/kontrolle_kaesten.png (jedes
# Kästchen mit der zugeordneten Nummer, von Hand mit den Ziffern im Plan verglichen).
# Halbmarathon: Schild „MITJA MARATÓ“ westlich der Carrer de Rocafort, nur zur Kontrolle (das Schild steht neben der Linie).
# -> marken.json {"km": [[km, Linienmeter, Abstand zur Planlinie in pt], …]}
import json, numpy as np
g = json.load(open("gpx2026.json")); L = g["d"][-1]
PL = json.load(open("plan2026.json")); PLAN = np.array(PL["linie"])
def dicht(P, step):                                    # wie in linie.py
    out = [P[0]]
    for a, b in zip(P[:-1], P[1:]):
        n = max(1, int(np.hypot(*(b - a)) / step)); out += [a + f * (b - a) for f in np.linspace(0, 1, n + 1)[1:]]
    return np.array(out)
PD = dicht(PLAN, 2.0); PS = np.r_[0, np.cumsum(np.hypot(*np.diff(PD, axis=0).T))]
wm = json.load(open("wegmarken.json")); W = np.array(sorted(wm.values(), key=lambda v: v[1]))
assert np.all(np.diff(W[:, 0]) > 0), "Wegmarken nicht in Reihenfolge"
plan_zu_linie = lambda sp: float(np.interp(sp, W[:, 1], W[:, 0]))
def stellen(p, maxd=130.0):
    """je zusammenhängendem Stück der Planlinie unter maxd die nächste Stelle: [(Linienmeter, Abstand pt)]"""
    dd = np.hypot(*(PD - p).T); out = []; m = dd < maxd; i = 0
    while i < len(m):
        if not m[i]: i += 1; continue
        j = i
        while j + 1 < len(m) and m[j + 1]: j += 1
        k = i + int(np.argmin(dd[i:j + 1])); out.append((plan_zu_linie(PS[k]), float(dd[k]))); i = j + 1
    return out
K = np.array(PL["kaesten"]); kand = [stellen(p) for p in K]
print("Kästchen ohne Planlinie in 130 pt:", [i for i, c in enumerate(kand) if not c])
# Zuordnung als kürzester Pfad über km 1–42 (Viterbi): je km ein Kästchen mit einer seiner Stellen; Kosten (Abstand zur Planlinie
# / 30 pt)² + (Abweichung von der erwarteten Stelle / 400 m)² + (Abweichung des Abstands zur vorigen Marke vom Mittel / 150 m)²,
# vorwärts. Jedes Kästchen genau einmal (wird geprüft).
Z = [(i, s, dist) for i, c in enumerate(kand) for s, dist in c]
step = L / 42.195
kost = np.full((42, len(Z)), np.inf); vor = np.zeros((42, len(Z)), int)
for z, (i, s, dist) in enumerate(Z):
    kost[0, z] = (dist / 30) ** 2 + ((s - step) / 400) ** 2 + ((s - step) / 150) ** 2
for k in range(1, 42):
    for z, (i, s, dist) in enumerate(Z):
        em = (dist / 30) ** 2 + ((s - (k + 1) * step) / 400) ** 2
        tr = np.array([kost[k - 1, y] + ((s - Z[y][1] - step) / 150) ** 2 if Z[y][1] < s and Z[y][0] != i else np.inf for y in range(len(Z))])
        vor[k, z] = int(np.argmin(tr)); kost[k, z] = tr[vor[k, z]] + em
z = int(np.argmin(kost[41] + ((L - np.array([q[1] for q in Z]) - 0.195 * step) / 150) ** 2)); weg = [z]
for k in range(41, 0, -1): z = vor[k, z]; weg.append(z)
weg = weg[::-1]
km = [[k + 1, round(Z[z][1], 1), round(Z[z][2], 1), Z[z][0]] for k, z in enumerate(weg)]
assert len({m[3] for m in km}) == 42, "Kästchen doppelt vergeben"
diffs = np.diff([0] + [m[1] for m in km] + [L])
print("Linienmeter je km (Marke zu Marke):", [int(round(x)) for x in diffs[:-1]], "Rest bis Ziel", int(round(diffs[-1])))
print("Abstand Kästchen–Planlinie: Median %.0f pt, max %.0f pt" % (np.median([m[2] for m in km]), max(m[2] for m in km)))
print("Schild MITJA MARATÓ: Stellen", [(round(s), round(dd)) for s, dd in stellen(np.array(PL["mitja"][0]), 200)])
json.dump({"km": [m[:3] for m in km]}, open("marken.json", "w"), indent=0)
# Gegenprobe: jedes Kästchen aus dem Plan ausschneiden, mit der zugeordneten Nummer beschriften
import pymupdf
from PIL import Image, ImageDraw
p = pymupdf.open("../dl/mapa-circuit-zmb26.pdf")[0]
bilder = []
for k, s, dist, i in km:
    x, y = PL["kaesten"][i]
    pix = p.get_pixmap(matrix=pymupdf.Matrix(0.6, 0.6), clip=pymupdf.Rect(x - 70, y - 70, x + 70, y + 70))
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples).resize((84, 84))
    c = Image.new("RGB", (84, 104), "white"); c.paste(im, (0, 0)); ImageDraw.Draw(c).text((30, 88), f"km {k}", fill="red"); bilder.append(c)
M = Image.new("RGB", (84 * 14, 104 * 3), "white")
for n, b in enumerate(bilder): M.paste(b, ((n % 14) * 84, (n // 14) * 104))
M.save("../dl/kontrolle_kaesten.png")
