# Streckenplan 2026 des Veranstalters („6.5 Mapa Circuit (ZMB26)“, ../dl/mapa-circuit-zmb26.pdf, Adobe Illustrator, 15/03/2026,
# verlinkt auf zurichmaratobarcelona.es/soc-corredor-a/recorregut/ als „Mapa del recorregut“) ist eine Vektorgrafik:
# - Streckenlinie: Striche in Blau (0/0,2/0,63), 15,93 pt, gestrichelt zwischen den Ecken, Ecken als kurze volle Striche;
# - 42 Kilometerkästchen (Füllung 0,14/0,25/0,55, 120 × 120 pt, Ziffern als Umrisse);
# - Startzeichen und Zielflagge (Kreise derselben Farbe, 220–230 pt), Schild „MITJA MARATÓ“.
# Hier nur in Plan-Koordinaten (pt, y nach unten), in Laufrichtung geordnet -> plan2026.json. Die Lage auf der Erde bestimmt marken.py.
import json, numpy as np, pymupdf
p = pymupdf.open("../dl/mapa-circuit-zmb26.pdf")[0]
def punkte(x):
    out = []
    for it in x["items"]:
        if it[0] == "l": out += [(it[1].x, it[1].y), (it[2].x, it[2].y)]
        elif it[0] == "c":
            a, b, c_, e = it[1:5]
            for t in np.linspace(0, 1, 9):
                out.append(((1-t)**3*a.x + 3*(1-t)**2*t*b.x + 3*(1-t)*t**2*c_.x + t**3*e.x, (1-t)**3*a.y + 3*(1-t)**2*t*b.y + 3*(1-t)*t**2*c_.y + t**3*e.y))
    q = [out[0]] if out else []
    for v in out[1:]:
        if np.hypot(v[0] - q[-1][0], v[1] - q[-1][1]) > 1e-6: q.append(v)
    return np.array(q)
farbe = lambda x, k: tuple(round(v, 2) for v in x[k]) if x.get(k) else None
stuecke, kaesten, kreise = [], [], []
for x in p.get_drawings():
    if x["type"] == "s" and farbe(x, "color") == (0.0, 0.2, 0.63) and abs(x["width"] - 15.93) < 0.1 and x["rect"].y1 < 4300:
        P = punkte(x)
        if len(P) >= 2: stuecke.append(P)
    if x["type"] == "f" and farbe(x, "fill") == (0.14, 0.25, 0.55):
        r = x["rect"]
        if 110 < r.width < 130 and 110 < r.height < 130: kaesten.append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2))
        if 210 < r.width < 240 and r.y1 < 4300: kreise.append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2))
# Kette in Laufrichtung: Anfang am Ende nächst dem Startzeichen (Passeig de Gràcia), dann jeweils das nächste freie Stück
start_zeichen = min(kreise, key=lambda c: c[0])          # Startzeichen links, Zielflagge am Arc de Triomf rechts davon
frei = list(range(len(stuecke)))
def naechstes(pkt):
    best = None
    for i in frei:
        for rev in (False, True):
            P = stuecke[i][::-1] if rev else stuecke[i]
            dd = float(np.hypot(*(P[0] - pkt)))
            if best is None or dd < best[0]: best = (dd, i, P)
    return best
# Startstück: das Stückende am nächsten zum Startzeichen (Startlinie im Passeig de Gràcia)
i0, e0 = min(((i, e) for i in range(len(stuecke)) for e in (False, True)), key=lambda t: np.hypot(*(stuecke[t[0]][-1 if t[1] else 0] - np.array(start_zeichen))))
kette = [stuecke[i0][::-1] if e0 else stuecke[i0]]; frei.remove(i0); luecken = []
while frei:
    dd, i, P = naechstes(kette[-1][-1])
    luecken.append(round(dd)); kette.append(P); frei.remove(i)
linie = np.vstack(kette)
print(len(stuecke), "Stücke, Lücken zwischen den Stücken (pt):", luecken, "; Linie", round(float(np.hypot(*np.diff(linie, axis=0).T).sum())), "pt")
mm = [((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2) for r in p.search_for("MITJA")]
print("Kästchen", len(kaesten), "Kreise", kreise, "MITJA MARATÓ", mm)
json.dump({"linie": linie.round(2).tolist(), "kaesten": kaesten, "start_zeichen": start_zeichen,
           "ziel_zeichen": [c for c in kreise if c != start_zeichen], "mitja": [m for m in mm if m[1] < 4300]}, open("plan2026.json", "w"))
