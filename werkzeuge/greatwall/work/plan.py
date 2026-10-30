# Streckenkarte 2026 des Veranstalters (../dl/route.pdf, „Great Wall Marathon Route map“, Adobe Illustrator, 08.05.2026) auslesen
# -> plan2026.json (alle Angaben in PDF-Punkten, y nach unten).
# Die Karte ist eine Vektorgrafik auf einem Satellitenbild mit Ebenen: „Rute“ (Marathon als eine durchgehende schwarze Linie in
# Laufrichtung, Hin- und Rückweg nebeneinander gezeichnet; darüber rot gestrichelt Halbmarathon, grün gestrichelt Fun Run),
# „Half town“ (Schleife des Halbmarathons in Duanzhuang), „Roads“ (Main Roads hellgrau, Tarmac streets grau, Feldwege braun),
# „Rivers“, „KM skilte“ (Kilometerschilder mit weißer gestrichelter Linie zur Strecke), „Water stations“ (Symbole mit blauer Linie
# zur Strecke), „First Aid“. Die beiden Ausschnitte (Start/Ziel-Platz, Mauer) sind Rasterbilder und werden hier nicht gelesen.
import json, math
import pymupdf
doc = pymupdf.open("../dl/route.pdf"); pg = doc[0]
DR = pg.get_drawings()
def flach(d, step=8):
    out = []
    for it in d["items"]:
        if it[0] == "l": seg = [it[1], it[2]]
        elif it[0] == "c":
            a, b, c, e = it[1:5]
            seg = [pymupdf.Point((1-t)**3*a.x + 3*(1-t)**2*t*b.x + 3*(1-t)*t*t*c.x + t**3*e.x,
                                 (1-t)**3*a.y + 3*(1-t)**2*t*b.y + 3*(1-t)*t*t*c.y + t**3*e.y) for t in [k / step for k in range(step + 1)]]
        else: continue
        for q in seg:
            if not out or math.dist(out[-1], (q.x, q.y)) > 1e-3: out.append((round(q.x, 3), round(q.y, 3)))
    return out
def farbe(d): return tuple(round(x, 2) for x in d["color"]) if d.get("color") else None
res = {"marathon": None, "half": [], "fun": [], "halftown": [], "roads": [], "rivers": [], "km": [], "water": [], "aid": [], "text": []}
for i, d in enumerate(DR):
    L = d.get("layer")
    if L == "Rute":
        c = farbe(d)
        if c == (0.14, 0.12, 0.13) and len(d["items"]) > 100: res["marathon"] = flach(d)
        elif c == (0.93, 0.11, 0.14) and len(d["items"]) > 2: res["half"].append(flach(d))
        elif c == (0.0, 0.65, 0.32): res["fun"].append(flach(d))
    elif L == "Half town": res["halftown"].append(flach(d))
    elif L == "Roads" and d["type"] == "s":
        klasse = {(0.66, 0.66, 0.67): "main", (0.5, 0.51, 0.52): "tarmac", (0.77, 0.6, 0.42): "gravel", (0.45, 0.4, 0.35): "gravel"}[farbe(d)]
        res["roads"].append({"k": klasse, "w": d["width"], "pts": flach(d)})
    elif L == "Rivers" and d["type"] == "s": res["rivers"].append({"w": d["width"], "pts": flach(d)})
# Texte (Dörfer, Kilometerschilder des Hauptplans)
for b in pg.get_text("dict")["blocks"]:
    for l in b.get("lines", []):
        s = " ".join(sp["text"] for sp in l["spans"]).strip()
        if s: res["text"].append([s, [round(v, 2) for v in l["bbox"]], round(l["spans"][0]["size"], 1)])
# Kilometerschilder: Ziffern über „KM“, gestrichelte weiße Linie; das Linienende fern vom Schild liegt an der Strecke
schilder = []
for s, bb, size in res["text"]:
    if size == 9.0 and s.replace(" ", "").isdigit():
        under = [t for t in res["text"] if t[0] == "KM" and abs(t[1][1] - bb[3]) < 2 and abs((t[1][0] + t[1][2]) / 2 - (bb[0] + bb[2]) / 2) < 4]
        if under: schilder.append((int(s.replace(" ", "")), ((bb[0] + bb[2]) / 2, (bb[1] + under[0][1][3]) / 2)))
for i, d in enumerate(DR):
    if d.get("layer") == "KM skilte" and d["type"] == "s" and d.get("dashes") == "[ 3 ] 0":
        a, b = flach(d)[0], flach(d)[-1]
        km, mitte = min(schilder, key=lambda s: min(math.dist(s[1], a), math.dist(s[1], b)))
        ende = a if math.dist(mitte, a) > math.dist(mitte, b) else b
        # Farbe des Schildfußes: schwarz = Marathon, rot = Halbmarathon, grün = Fun Run (Leitfaden: „colour-coded“)
        res["km"].append({"km": km, "pt": ende, "schild": [round(v, 1) for v in mitte]})
# Getränkestellen: weiße Kästen mit Symbolen, blaue Linie zur Strecke. Symbole: Flasche (Wasser), gelber Blitz (Elektrolyt),
# „G“ (Gel), gelbe Banane; Erste Hilfe als rotes Kreuz im selben Kasten.
boxes = [(i, d["rect"]) for i, d in enumerate(DR) if d.get("layer") == "Water stations" and d["type"] == "fs" and d.get("fill") == (1.0, 1.0, 1.0)]
def inhalt(r):
    z = {"Wasser": False, "Elektrolyt": False, "Gel": False, "Banane": False, "Erste Hilfe": False}
    for d in DR:
        if not r.contains(d["rect"]) or d["rect"] == r: continue
        f = tuple(round(x, 2) for x in d["fill"]) if d.get("fill") else None
        if d.get("layer") == "Water stations":
            if f in ((0.0, 0.68, 0.94), (0.16, 0.67, 0.89)): z["Wasser"] = True
            if f in ((1.0, 0.95, 0.0), (0.98, 0.93, 0.11)) and len(d["items"]) == 7: z["Elektrolyt"] = True
            if (f == (0.98, 0.93, 0.11) and len(d["items"]) == 8) or f == (0.92, 0.79, 0.1): z["Banane"] = True
            if f == (0.93, 0.11, 0.14) or f == (0.85, 0.11, 0.14) or f == (0.93, 0.13, 0.15): z["Erste Hilfe"] = True
    for s, bb, size in res["text"]:
        if s == "G" and r.contains(pymupdf.Point((bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2)): z["Gel"] = True
    return z
leads = []
for i, d in enumerate(DR):
    if d.get("layer") == "Water stations" and d["type"] == "s" and len(d["items"]) == 1 and d["items"][0][0] == "l":
        a, b = d["items"][0][1], d["items"][0][2]
        if a.distance_to(b) > 3: leads.append(((a.x, a.y), (b.x, b.y)))
def randabstand(r, p): return math.hypot(max(r.x0 - p[0], 0, p[0] - r.x1), max(r.y0 - p[1], 0, p[1] - r.y1))
for i, r in boxes:
    best = min(leads, key=lambda l: min(randabstand(r, l[0]), randabstand(r, l[1])))
    ende = best[0] if randabstand(r, best[0]) > randabstand(r, best[1]) else best[1]
    res["water"].append({"box": [round(v, 1) for v in (r.x0, r.y0, r.x1, r.y1)], "pt": [round(v, 2) for v in ende], "inhalt": inhalt(r)})
# Erste Hilfe allein (weißer Kreis mit rotem Kreuz, Linie zur Strecke)
for i, d in enumerate(DR):
    if d.get("layer") == "First Aid" and d["type"] == "s":
        a, b = d["items"][0][1], d["items"][0][2]
        kreis = [e["rect"] for e in DR if e.get("layer") == "First Aid" and e["type"] == "fs" and e.get("fill") == (1.0, 1.0, 1.0)]
        k = min(kreis, key=lambda r: min(randabstand(r, (a.x, a.y)), randabstand(r, (b.x, b.y))))
        ende = (a.x, a.y) if randabstand(k, (a.x, a.y)) > randabstand(k, (b.x, b.y)) else (b.x, b.y)
        res["aid"].append({"pt": [round(v, 2) for v in ende]})
json.dump(res, open("plan2026.json", "w"), ensure_ascii=False)
L = sum(math.dist(a, b) for a, b in zip(res["marathon"], res["marathon"][1:]))
print("Marathonlinie", len(res["marathon"]), "Punkte,", round(L), "pt; Straßen", len(res["roads"]), "Flüsse", len(res["rivers"]))
print("Kilometerschilder:", sorted((k["km"], tuple(round(v) for v in k["pt"])) for k in res["km"]))
for w in res["water"]: print("Getränke", w["pt"], [k for k, v in w["inhalt"].items() if v])
print("Erste Hilfe", res["aid"])
