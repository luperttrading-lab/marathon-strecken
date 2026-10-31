# Höhen im 10-m-Raster, Straßen, Marken und geschätzte Stücke -> data.json (geht als const D in jungfrau/index.html).
# Muster: werkzeuge/luzern/work/build.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official, gpx_of
L = 42195.0; STEP = 10
c = json.load(open("clean.json"))
k = np.array(c["k"]); hc = np.array(c["h"])
grid = np.arange(0, 42200 + 1, STEP, dtype=float)
hg = np.interp(np.minimum(grid, L), k, hc)
hm = hg.copy()                                   # gleitender Median über 3 Punkte (30 m)
for i in range(1, len(hg) - 1): hm[i] = np.median(hg[i-1:i+2])
# Straßen aus den OSM-Wegen unter der Linie (strassen.json, alle 10 m, Namen wie in OSM und auf den Schildern), sonst aus dem amtlichen
# Strassenverzeichnis (strassenverz.json), Gemeinden und Ortschaften (orte2026.json, alle 100 m). Unbekannte und kurze Stücke unter 50 m
# übernehmen den Namen davor, Orte unter 300 m dem Vorgänger zugeschlagen und auf den nächsten Straßenwechsel gelegt.
# Ohne Namen in OSM und im Strassenverzeichnis sind fast alle Wege ab Wilderswil. Von Hand benannt (nach offiziellen Metern):
#   „Hauptstrasse“ in Lauterbrunnen hin und zurück (so in der Verkehrsinformation der Race-Info 2026: „Lauterbrunnen: Hauptstrasse,
#   Zufahrt zum Parkhaus Lauterbrunnen sowie nach Stechelberg“; Kantonsstrasse 222), „Stocki“ (Name des Postens und des Weilers),
#   „Zentrum Wengen“ (Durchlaufzeiten der Race-Info), „Waldschluecht“ (OSM-Weiler und -Weg), „Wixi“ (Abzweigung und Haltestelle
#   Wengernalp Wixi), „Eigergletscher“ (Fahrweg zur Station und Zielgelände, ab km 41,79). Die übrigen Wege beschreibend nach Art und Lage: Wander- und Bergwege so, wie der
#   Veranstalter sie im Höhenprofil 2024 nennt (Asphaltstrasse, Wanderweg, Bergweg); der Weg Wixi–Haaregg heißt in OSM
#   „Junfrau-Marathon Teil Wixi–Haaregg (Strecke Süd)“ (daneben die „Strecke Nord“, die Entlastungsstrecke bei viel Andrang).
st = json.load(open("strassen.json")); sv = json.load(open("strassenverz.json")); orte = json.load(open("orte2026.json"))
VON_HAND = [(3440, 3560, "Höheweg"), (10370, 12690, "Strasse über Gsteigwiler"), (12690, 15040, "Wanderweg an der Lütschine"),
            (15040, 15470, "Bahnhof Zweilütschinen"), (15470, 15670, "Hauptstrasse"), (15670, 19900, "Wanderweg an der Weissen Lütschine"),
            (20000, 20800, "Hauptstrasse"), (22680, 23380, "Wanderweg zum Trümmelbach"), (23380, 25780, "Hauptstrasse"),
            (25780, 26390, "Stocki"), (26390, 29250, "Bergweg nach Wengen"), (29980, 30770, "Zentrum Wengen"), (30770, 31180, "Waldschluecht"),
            (31180, 32900, "Strasse Wengen–Allmend"), (32900, 33520, "Weg zur Allmend"), (38480, 38880, "Wixi"),
            (38880, 40220, "Bergweg Wixi–Haaregg"), (40220, 41790, "Bergweg über die Moräne"), (41790, 42200, "Eigergletscher")]
def strasse(x):                                   # x in offiziellen Metern
    for a, b, n in VON_HAND:
        if a <= x < b: return n
    i = min(len(st) - 1, int(round(float(gpx_of(x)) / 10)))
    return st[i][2] or sv[min(len(sv) - 1, i)][1] or ""
# Orte: Gemeinde und Ortschaft (orte.py); oberhalb von Wengen wie in den Durchlaufzeiten der Race-Info 2026 („Dorf“: Wengernalp,
# Eigergletscher). Wengen endet an der Allmend (km 33,5), die Wengernalp reicht bis Haaregg (km 40,2), danach Eigergletscher.
ORT_HAND = [(33520, 40220, "Lauterbrunnen, Wengernalp"), (40220, 42200, "Lauterbrunnen, Eigergletscher")]
def ort(x):
    for a, b, n in ORT_HAND:
        if a <= x < b: return n
    return orte[min(len(orte) - 1, int(round(float(gpx_of(x)) / 100)))][1]
roads = [strasse(x) for x in np.minimum(grid, L)]
qs = [ort(x) for x in np.minimum(grid, L)]
def glaetten(v, mind):
    for i in range(1, len(v)): v[i] = v[i] or v[i - 1]
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[j + 1] == v[i]: j += 1
        if i > 0 and (j + 1 - i) * STEP < mind: v[i:j + 1] = [v[i - 1]] * (j + 1 - i)
        i = j + 1
    for i in range(len(v) - 2, -1, -1): v[i] = v[i] or v[i + 1]
    return v
roads = glaetten(roads, 50)
qs = glaetten(qs, 300)
wechsel = [i for i in range(1, len(roads)) if roads[i] != roads[i - 1]]
for i in [i for i in range(1, len(qs)) if qs[i] != qs[i - 1]]:
    w = min(wechsel, key=lambda j: abs(j - i), default=None)
    if w is not None and 0 < abs(w - i) <= 10:
        if w > i: qs[i:w] = [qs[i - 1]] * (w - i)
        else: qs[w:i] = [qs[i]] * (i - w)
segs, prev = [], None
for x, road, q in zip(grid, roads, qs):
    if x > L: break
    if (road, q) != prev: segs.append([round(x), road, q]); prev = (road, q)
segs[0][0] = 0
# Geschätzte Stücke (schraffiert, clean.py): Brücken, unter denen das Geländemodell den Bach misst und auf denen Bäume oder Geländer
# das Oberflächenmodell stören. Die übrigen Brücken sind aus dem Oberflächenmodell gemessen.
bridges = []
for r in c["regions"]:
    if r["art"] == "Brücke geschätzt":
        nm = strasse(r["a"] + 20)
        bridges.append({"a": round(r["a"]), "b": round(r["b"]), "name": nm, "kind": "Brücke"})
bridges.sort(key=lambda b: b["a"])
# Verpflegung laut „Wettkampfverpflegung 2026“ des Veranstalters (Marathon_Wettkampfverpflegung-Sponser_2026_WEB.pdf, 25.03.2026, Seite
# „Strecke“, Download „Verpflegungsplan 2026“): 11 Posten und 5 Wasser- bzw. Colastellen mit Kilometer und Inhalt; Lage auf der Linie
# über die Kilometer (sie stimmen mit den Orten der Karte „Verpflegungsposten 2026“ überein). Selbstbedienung.
# Wasser und Getränke ohne Essen als „water“, mit Riegel, Banane, Gel oder Bouillon als „food“.
CO = "Sponser Competition"
VP = [(5500, "Interlaken, im Moos", f"Wasser, {CO}"),
      (10000, "Wilderswil", f"Wasser, {CO}, Riegel, Banane"),
      (16000, "Zweilütschinen, hinter der Egg", f"Wasser, {CO}, Riegel"),
      (20800, "Lauterbrunnen", f"Wasser, {CO}, Bouillon, Banane, Gel mit Koffein, Schwämme"),
      (23200, "Trümmelbach", f"Wasser, {CO}, Riegel, Gel mit Koffein"),
      (25700, "Lauterbrunnen, «Stocki»", f"Wasser, {CO}, Bouillon, Riegel, Banane"),
      (27900, "Undre Fuhren", "Wasser"),
      (29200, "Wengen, Wengwald", f"Wasser, {CO}, Bouillon, Riegel, Banane, Gel, Schwämme"),
      (32900, "Wengen, Café Oberland", f"Wasser, {CO}, Cola, Bouillon, Riegel, Banane, Gel"),
      (34700, "Baawald/Hannegg", "Wasser"),
      (36300, "Mettla", f"Wasser, {CO}, Cola, Bouillon, Riegel, Banane, Gel"),
      (38900, "Wixi", f"Wasser, {CO}, Cola, Bouillon, Riegel, Banane, Gel, Schwämme"),
      (40300, "Haaregg", "Wasser, Cola"), (41000, "Moräne", "Wasser, Cola"), (41400, "Loucherflueh, «Schoggistei»", "Wasser, Cola")]
def kmtext(x): return f"{x:g}".replace(".", ",")
marks = []
for k_, wo, was in VP:
    essen = any(w in was for w in ("Riegel", "Banane", "Gel", "Bouillon"))
    s_ = "Verpflegung" if essen else ("Wasser" if was == "Wasser" else "Getränke")
    marks.append({"k": k_, "s": s_, "c": "food" if essen else "water", "n": f"{s_} km {kmtext(k_ / 1000)}, {wo} ({was})"})
marks.append({"k": 21098, "s": "Halbmarathon", "c": "half", "n": "Halbmarathon"})
marks.sort(key=lambda m: m["k"])
data = {"len": L, "step": STEP, "h": [int(round(v * 100)) for v in hm], "streets": segs, "marks": marks, "bridges": bridges}
json.dump(data, open("data.json", "w"), ensure_ascii=False, separators=(",", ":"))
# Kontrollen
def at(x): return float(np.interp(x, grid, hm))
def asc(w):
    xs = grid[grid <= L]; gr = np.array([(at(min(x + w/2, L)) - at(max(x - w/2, 0))) / (min(x + w/2, L) - max(x - w/2, 0)) for x in xs])
    dh = (gr[1:] + gr[:-1]) / 2 * STEP
    return dh[dh > 0].sum(), -dh[dh < 0].sum(), gr, xs
for w in (50, 100, 200, 1000):
    u, d_, gr, xs = asc(w)
    print(f"Fenster {w:5d} m: ↑ {u:6.1f} m  ↓ {d_:5.1f} m  steilste bergauf {gr.max()*100:4.1f} % bei km {xs[np.argmax(gr)]/1000:.2f}, "
          f"bergab {gr.min()*100:5.1f} % bei km {xs[np.argmin(gr)]/1000:.2f}")
    if w == 200:
        for g_ in (0.10, 0.15, 0.20, 0.25):
            print(f"   über {g_*100:.0f} %: {(gr > g_).sum() * STEP / 1000:5.2f} km   (unter −{g_*100:.0f} %: {(gr < -g_).sum() * STEP / 1000:4.2f} km)")
raw = np.array(c["raw"]); kr = np.array(c["k"]); sel = kr <= L
roh = round(np.clip(np.diff(hc[sel]), 0, None).sum())
open("rohdaten.txt", "w").write(str(roh))
print("Rohdaten Punkt für Punkt (bereinigt, ohne Messfenster) ↑", roh, "m ↓", round(-np.clip(np.diff(hc[sel]), None, 0).sum()), "m; Geländemodell ohne Bereinigung ↑",
      round(np.clip(np.diff(raw[sel]), 0, None).sum(), 1), "m")
print("Höhe min/max", round(hm.min(), 1), round(hm.max(), 1), "bei km", grid[np.argmin(hm)]/1000, grid[np.argmax(hm)]/1000, "Start", round(at(0), 1), "Ziel", round(at(L), 1))
print("Straßenabschnitte", len(segs), "Marken", len(marks), "geschätzte Stücke", len(bridges))
for sg in segs: print("  ", sg)
for m in marks: print("  ", m["k"], m["n"])
for b in bridges: print("  ", b)
