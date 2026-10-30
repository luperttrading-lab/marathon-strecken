# Streckenlinie, Kilometermarken und Getränkestellen aus dem Streckenplan 2026 des Veranstalters (Le Champion,
# parcours-tcs-amsterdam-marathon-zondag-2026-v2.pdf, Vektorgrafik aus InDesign, 1800 × 2367 pt). Die Marathonlinie ist rot
# (RGB 0,93/0,11/0,14, 5 pt breit), der Halbmarathon blau daneben. Kilometer: rote Kästchen „N km“ mit Hinweislinie auf einen
# kleinen weißen Kreis auf der Linie. -> ../dl/pdf_linie.json (Stücke der roten Linie in PDF-Koordinaten), ../dl/pdf_marken.json
import json, re, sys
import numpy as np, pymupdf
doc = pymupdf.open("../dl/parcours-2026-v2.pdf"); p = doc[0]
dr = p.get_drawings()
def farbe(c): return tuple(round(x, 2) for x in (c or ()))
ROT, BLAU, DUNKEL = (0.93, 0.11, 0.14), (0.0, 0.43, 0.72), (0.14, 0.12, 0.13)
def bez(p0, p1, p2, p3, n=12):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3
def polylinie(d):
    """Pfad als Liste zusammenhängender Linienzüge (ein Pfad kann mehrere Teilpfade haben)"""
    zuege, cur = [], []
    for it in d["items"]:
        if it[0] == "l": seg = np.array([[it[1].x, it[1].y], [it[2].x, it[2].y]])
        elif it[0] == "c": seg = bez(*[np.array([q.x, q.y]) for q in it[1:5]])
        else: continue
        if cur and np.hypot(*(cur[-1][-1] - seg[0])) > 0.05: zuege.append(np.vstack(cur)); cur = []
        cur.append(seg if not cur else seg[1:])
    if cur: zuege.append(np.vstack(cur))
    return zuege
linien = {"rot": [], "blau": []}
for d in dr:
    if d["type"] != "s" or not d.get("width") or d["width"] < 4.9 or d["width"] > 5.1: continue
    k = "rot" if farbe(d["color"]) == ROT else "blau" if farbe(d["color"]) == BLAU else None
    if k: linien[k] += [z.tolist() for z in polylinie(d)]
for k, v in linien.items():
    print(k, len(v), "Züge", [len(z) for z in v])
    for z in v: print("   ", [round(x) for x in z[0]], "->", [round(x) for x in z[-1]], round(float(np.hypot(*np.diff(np.array(z), axis=0).T).sum())), "pt")
json.dump(linien, open("../dl/pdf_linie.json", "w"))
# Kilometermarken: Text „N km“ in einem gefüllten Kästchen (rot = Marathon, blau = Halbmarathon), Hinweislinie (dunkel, ~1,2 pt)
# vom Kästchen zu einem kleinen Kreis (weiß gefüllt, dunkel umrandet, ~4,4 pt)
spans = [(s["text"].strip(), pymupdf.Rect(s["bbox"])) for b in p.get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"]]
kaesten = [(farbe(d["fill"]), d["rect"]) for d in dr if d["type"] == "f" and farbe(d.get("fill")) in (ROT, BLAU) and d["rect"].width < 60 and d["rect"].height < 25]
kreise = [d["rect"] for d in dr if d["type"] == "fs" and farbe(d.get("fill")) == (1.0, 1.0, 1.0) and farbe(d.get("color")) == DUNKEL and 3.5 < d["rect"].width < 6]
striche = []
for d in dr:
    if d["type"] == "s" and farbe(d.get("color")) == DUNKEL and 1.0 < (d.get("width") or 0) < 1.4:
        for z in polylinie(d): striche.append(np.array(z))
print(len(kaesten), "Kästchen", len(kreise), "Kreise", len(striche), "Striche")
kz = np.array([[(r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2] for r in kreise])
def abstand_rect(pt, r):
    dx = max(r.x0 - pt[0], 0, pt[0] - r.x1); dy = max(r.y0 - pt[1], 0, pt[1] - r.y1); return np.hypot(dx, dy)
marken = []
for t, r in spans:
    m = re.fullmatch(r"(\d+) km", t)
    if not m or (r.y0 > 1900 and r.x0 < 240): continue   # Legende unten links
    box = [(f, b) for f, b in kaesten if b.contains(pymupdf.Point((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2))]
    if not box: print("kein Kästchen", t, r); continue
    f, b = box[0]
    best = None
    for z in striche:
        for a, e in ((z[0], z[-1]), (z[-1], z[0])):
            da = abstand_rect(a, b)
            if da < 4:
                dk = np.hypot(*(kz - e).T); j = int(np.argmin(dk))
                if dk[j] < 4 and (best is None or da + dk[j] < best[0]): best = (da + dk[j], kz[j].tolist())
    if best is None:   # Kreis direkt neben dem Kästchen (ohne Strich, bis 16 pt daneben)
        dk = [abstand_rect(q, b) for q in kz]; j = int(np.argmin(dk))
        best = (dk[j], kz[j].tolist()) if dk[j] < 16 else None
    marken.append({"km": int(m.group(1)), "lauf": "marathon" if f == ROT else "halb", "kreis": best[1] if best else None, "kasten": [b.x0, b.y0, b.x1, b.y1]})
for mk in sorted(marken, key=lambda m: (m["lauf"], m["km"])): print(mk["lauf"], mk["km"], [round(x, 1) for x in mk["kreis"]] if mk["kreis"] else None)
json.dump(marken, open("../dl/pdf_marken.json", "w"))
