# Zwei Quellen für die Linie des Kurses 2026:
# 1. Streckenplan Marathon 2026 des Veranstalters (D.SPORTS / D.LIVE, InDesign „Streckenplan.indd“ vom 15.04.2026, A1, Vektorkarte;
#    die Datei liegt nicht mehr auf uniper-duesseldorfmarathon.de, eine Kopie auf sportsidioten.no:
#    https://www.sportsidioten.no/wp-content/uploads/2026/04/Streckenplan_Marathon.pdf -> ../dl/pdf/Streckenplan_Marathon_sportsidioten.pdf).
#    Die Strecke ist dort ein einziger roter Pfad (Farbe 0,93/0,11/0,14, Strichbreite 3,62 pt, 783 Geraden, Start -> Ziel),
#    dazu 42 Kilometerschilder („N km“, weiße Kästen mit rotem Rand; 10, 20, 30, 40 km rot gefüllt mit Uhr = Zeitmessung).
#    -> plan_pdf.json {"pts": [[x, y] PDF-Punkte], "km": [[x, y, b, h] Mitte und Größe der Schilder]}
# 2. Tour „Uniper Düsseldorf Marathon 2026“ von Visit Düsseldorf (Düsseldorf Tourismus GmbH, toubiz; angelegt 08.04.2025,
#    geändert 20.04.2026, „free_draw“, 945 Punkte, 42 233 m laut Tour):
#    https://www.visitduesseldorf.de/poi/detail/uniper-duesseldorf-marathon-2026-fcc86d8a2e -> ../dl/toubiz/
#    -> tour2026.json {"pts": [[lat, lon]], "d": [laufende Länge, GRS80]}
import json, re, collections
import numpy as np
import pymupdf
from pyproj import Geod
doc = pymupdf.open("../dl/pdf/Streckenplan_Marathon_sportsidioten.pdf"); p = doc[0]
dr = p.get_drawings()
rot = [d for d in dr if d.get("color") and tuple(round(c, 2) for c in d["color"]) == (0.93, 0.11, 0.14) and d["type"] == "s" and len(d["items"]) > 100]
assert len(rot) == 1
it = rot[0]["items"]
pts = [(i[1].x, i[1].y) for i in it] + [(it[-1][2].x, it[-1][2].y)]
assert all(abs(it[k][2].x - it[k + 1][1].x) < 0.01 and abs(it[k][2].y - it[k + 1][1].y) < 0.01 for k in range(len(it) - 1))
km = []
for d in dr:
    r = d["rect"]
    if r.x0 < 300: continue                       # Legende
    col = d.get("color") and tuple(round(c, 2) for c in d["color"]); fil = d.get("fill") and tuple(round(c, 2) for c in d["fill"])
    n = collections.Counter(i[0] for i in d["items"])
    if d["type"] == "fs" and fil == (1.0, 1.0, 1.0) and col and col[0] > 0.85 and col[1] < 0.2 and n.get("c") == 4 and n.get("l") == 4:
        km.append([(r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2, r.width, r.height])
P = np.array(pts); L = np.hypot(*np.diff(P, axis=0).T).sum()
print(f"Plan: {len(pts)} Punkte, {L:.0f} pt lang, {len(km)} Schilder")
json.dump({"pts": pts, "km": km}, open("plan_pdf.json", "w"))
t = open("../dl/toubiz/visitduesseldorf_de_fcc86d8a2e.html", encoding="utf-8").read()
m = re.search(r'"geometry":\{"type":"LineString","coordinates":(\[\[.*?\]\])\}', t)
c = json.loads(m.group(1))
tp = [(b, a) for a, b in c]
tp = [q for i, q in enumerate(tp) if i == 0 or q != tp[i - 1]]           # doppelte Punkte weg
G = Geod(ellps="GRS80")
_, _, dd = G.inv([q[1] for q in tp[:-1]], [q[0] for q in tp[:-1]], [q[1] for q in tp[1:]], [q[0] for q in tp[1:]])
d = np.r_[0, np.cumsum(dd)]
print(f"Tour: {len(c)} Punkte, ohne doppelte {len(tp)}, {d[-1]:.1f} m; Abstand Median {np.median(dd):.0f} m, max {max(dd):.0f} m; Start {tp[0]}, Ende {tp[-1]}")
json.dump({"pts": tp, "d": d.tolist()}, open("tour2026.json", "w"))
