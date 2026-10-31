# Linie des Kurses 2026 aus dem Streckenplan des Veranstalters (Münster-Marathon e.V., „marathon_streckenplan_verlauf_2026_02.pdf“,
# InDesign 23./24.07.2026, A3 quer, Kartengrund „Streckenplan ©Stadt Münster“, Vektorkarte;
# https://www.volksbank-muenster-marathon.de/_data/marathon_streckenplan_verlauf_2026_02.pdf -> ../dl/pdf/).
# Die Strecke ist ein orangefarbener Pfad (Farbe 0,91/0,30/0,06, 2 pt) aus zehn Teilstücken, dazu drei dünnere Linien (1,5 pt) in der
# Aegidiistraße, wo die Strecke dreimal durchläuft (Hinweg km 0,5, Rückweg km 10, Zielanlauf km 41,6), und fünf gepunktete Stücke
# („Unter-, Überführungen“ laut Legende). Gelaufen wird (Pfeile, Kilometerkreise, Verpflegungstabelle):
#   Start Schlossplatz – Am Stadtgraben – Aegidiitor – Aegidiistraße – Rothenburg – Kreuzviertel/Kanonierplatz (km 4,3) – Promenade –
#   Servatiiplatz (km 7,5) – Ludgeristraße (km 9,5) – Rothenburg (km 10) – Aegidiistraße – Aegidiitor – Aasee – Scharnhorststraße
#   (km 11,8) – Vesaliusweg (km 14,5) – Coesfelder Kreuz – Gievenbeck – Haus Uhlenkotten (km 20,3) – Nienberge (Halbmarathon) –
#   Haus Rüschhaus – Haus Vögeding (km 25,3) – Roxel (km 30) – Roxeler Straße – Gievenbeck (km 35) – Vesaliusweg (km 40) –
#   Adenauerallee – Aegidiitor – Aegidiistraße – Rothenburg – Ziel Prinzipalmarkt.
# Die Reihenfolge der Teilstücke ist hier von Hand festgelegt (FOLGE, je Stück Anfangs- und Endpunkt in PDF-Punkten, geprüft).
# Außerdem die Marken: Kilometerkreise (05 … 40, HM), Verpflegungssymbole (gelb, Nummern 01–15 wie in der Tabelle), Staffelwechsel
# (blau, 01–03), Pfeile (Laufrichtung).
# -> plan_pdf.json {"pts": [[x, y]], "punkt": [Kennung des Teilstücks je Punkt, "…:punkt" für gepunktete Stücke],
#                   "km": [[x, y, Text]], "vp": [[x, y, Nummer]], "sw": [[x, y, Nummer]], "pfeile": [[x, y, dx, dy]]}
import json, collections
import numpy as np
import pymupdf
doc = pymupdf.open("../dl/pdf/marathon_streckenplan_verlauf_2026_02.pdf"); p = doc[0]
dr = p.get_drawings(); W = p.get_text("words")
def c3(c): return tuple(round(v, 2) for v in c) if c else None
ORANGE, BLAU, GELB = (0.91, 0.3, 0.06), (0.0, 0.41, 0.71), (1.0, 0.83, 0.0)
def legende(r): return r.x0 > 800 and r.y1 < 400
def samp(it):
    if it[0] == "l": return [(it[1].x, it[1].y), (it[2].x, it[2].y)]
    P = np.array([[q.x, q.y] for q in it[1:5]]); t = np.linspace(0, 1, 9)[:, None]
    return [tuple(b) for b in (1 - t) ** 3 * P[0] + 3 * (1 - t) ** 2 * t * P[1] + 3 * (1 - t) * t ** 2 * P[2] + t ** 3 * P[3]]
stuecke, punktiert = [], []
for x in dr:
    if x["type"] != "s" or c3(x.get("color")) != ORANGE or (x.get("width") or 0) < 1.4 or legende(x["rect"]): continue
    if "[]" not in repr(x.get("dashes")):                                    # gepunktet: Strichmuster [0 n]
        punktiert.append(x["rect"]); continue
    cur = []
    for it in x["items"]:
        s = samp(it)
        if cur and abs(cur[-1][0] - s[0][0]) + abs(cur[-1][1] - s[0][1]) > 0.01:
            if len(cur) > 2: stuecke.append(np.array(cur))
            cur = []
        cur += s if not cur else s[1:]
    if len(cur) > 2: stuecke.append(np.array(cur))
def L(a): return float(np.hypot(*np.diff(a, axis=0).T).sum())
print(len(stuecke), "Teilstücke,", len(punktiert), "gepunktete Linien")
# Reihenfolge (Anfang -> Ende in PDF-Punkten, Bezeichnung)
FOLGE = [((934, 614), (953, 705), "Start Schlossplatz – Am Stadtgraben – Aegidiitor"),
         ((953, 705), (993, 660), "Aegidiistraße hin (1,5 pt)"),
         ((994, 659), (1099, 627), "Rothenburg – Kreuzviertel – Kanonierplatz – Promenade"),
         ((1098, 648), (1001, 662), "Servatiiplatz – Ludgeriviertel – Rothenburg"),
         ((999, 661), (951, 714), "Aegidiistraße zurück (1,5 pt)"),
         ((951, 714), (762, 598), "Aegidiitor – Aasee – Scharnhorststraße – Vesaliusweg – Coesfelder Kreuz"),
         ((770, 572), (472, 224), "Gievenbeck – Haus Uhlenkotten"),
         ((472, 200), (451, 93), "zur Altenberger Straße (Nienberge)"),
         ((430, 76), (298, 167), "Nienberge"),
         ((288, 185), (905, 702), "Schonebeck – Roxel – Roxeler Straße – Gievenbeck – Vesaliusweg – Adenauerallee"),
         ((905, 702), (997, 658), "Aegidiistraße zum Ziel (1,5 pt)"),
         ((997, 658), (1034, 642), "Rothenburg – Prinzipalmarkt, Ziel")]
pts, kenn, frei = [], [], list(range(len(stuecke)))
for n, (a, b, nm) in enumerate(FOLGE):
    i = min(frei, key=lambda j: np.hypot(*(stuecke[j][0] - a)) + np.hypot(*(stuecke[j][-1] - b)))
    s = stuecke[i]; assert np.hypot(*(s[0] - a)) < 2 and np.hypot(*(s[-1] - b)) < 2, (nm, s[0], s[-1])
    frei.remove(i)
    if pts:
        luecke = np.hypot(*(s[0] - pts[-1]))
        if luecke > 5:                                                         # gepunktetes Stück als Gerade (kleinere Lücken: Anschluss der dünnen Linien)
            mitte = (s[0] + np.array(pts[-1])) / 2
            assert any(r.x0 - 3 < mitte[0] < r.x1 + 3 and r.y0 - 3 < mitte[1] < r.y1 + 3 for r in punktiert), (nm, luecke)
            kenn[-1] = f"{n - 1}:punkt"
            print(f"  gepunktet {luecke:5.1f} pt vor „{nm}“ bei {np.round(mitte)}")
        s = s[1:] if luecke < 0.5 else s
    pts += [tuple(q) for q in s]; kenn += [str(n)] * len(s)
    print(f"{n:2d} {L(s):6.0f} pt  {nm}")
print("übrig (nicht Teil der Strecke):", [(np.round(stuecke[j][0]), np.round(stuecke[j][-1]), round(L(stuecke[j]))) for j in frei])
P = np.array(pts); print(f"Linie {len(P)} Punkte, {L(P):.0f} pt")
NR = {f"{i:02d}" for i in range(1, 16)}                                       # Nummern der Verpflegungstabelle
def text_bei(r, d=3):
    return " ".join(w[4] for w in W if w[0] > r.x0 - d and w[2] < r.x1 + d and w[1] > r.y0 - d and w[3] < r.y1 + d)
km, vp, sw, pfeile = [], [], [], []
for x in dr:
    r = x["rect"]; f = c3(x.get("fill"))
    if legende(r) or r.y0 < 0: continue
    n = collections.Counter(i[0] for i in x["items"])
    if f == ORANGE and x["type"] == "f" and n.get("c") == 4 and len(x["items"]) == 4 and 10 < r.width < 16:
        km.append([(r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2, text_bei(r, 1).split()[-1]])
    if f == GELB and n.get("re") == 1 and 15 < r.width < 22:
        vp.append([(r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2, " ".join(w for w in text_bei(r, 1).replace(",", " ").split() if w in NR)])
    if f == BLAU and n.get("re") == 1 and 15 < r.width < 22 and 15 < r.height < 22:
        sw.append([(r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2, " ".join(w for w in text_bei(r, 1).split() if w.isdigit() and len(w) == 2)])
    if f == ORANGE and x["type"] == "f" and len(x["items"]) == 3 and all(i[0] == "l" for i in x["items"]) and r.width < 14:
        Q = np.array([[i[1].x, i[1].y] for i in x["items"]]); s = Q.mean(0)
        sp = Q[np.argmax(np.hypot(*(Q - s).T))]; pfeile.append([*s, *(sp - s)])
km.sort(key=lambda k: (k[2] == "HM", k[2])); vp.sort(key=lambda v: v[2]); sw.sort(key=lambda v: v[2])
print("Kilometerkreise:", [k[2] for k in km]); print("Verpflegungssymbole:", [v[2] for v in vp]); print("Staffelwechsel:", [s[2] for s in sw])
print("Pfeile:", len(pfeile))
json.dump({"pts": [list(q) for q in pts], "teil": kenn, "km": km, "vp": vp, "sw": sw, "pfeile": pfeile}, open("plan_pdf.json", "w"))
