# Höhen im 10-m-Raster, Straßen, Marken und Brücken -> data.json (geht als const D in muenster/index.html). Muster:
# werkzeuge/duesseldorf/work/build.py
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
# Straßen aus den OSM-Wegen unter der Linie (strassen.json, alle 10 m, Namen wie in OSM), Stadtteil bzw. Viertel (orte2026.json, alle
# 100 m). Unbekannte und kurze Stücke unter 80 m (Kreuzungen, die Fußwege neben der Aegidiistraße, wo die drei Linien des Plans
# nebeneinander liegen) übernehmen den Namen davor; Stadtteile unter 300 m dem Vorgänger zugeschlagen und auf den nächsten
# Straßenwechsel gelegt; nur das letzte Stück auf dem Prinzipalmarkt (70 m bis zum Ziel) bleibt. In OSM ohne Namen (asphaltierte Wege, highway=path): km 12,40–12,70 vom Kardinal-von-Galen-Ring durch die
# Wiesen am Aasee zur Annette-Allee und km 27,41–27,92 zwischen Stodtbrockweg und Bredeheide in Roxel, beide „Fuß- und Radweg“.
st = json.load(open("strassen.json")); orte = json.load(open("orte2026.json"))
OHNE_NAMEN = [(12400, 12700), (27410, 27920)]
gx = gpx_of(np.minimum(grid, L))
def strasse(x):
    e = st[min(len(st) - 1, int(round(x / 10)))]
    if not e[1] and any(a <= float(official(x)) <= b for a, b in OHNE_NAMEN): return "Fuß- und Radweg"
    return e[1] or ""
roads = [strasse(x) for x in gx]
qs = [orte[min(len(orte) - 1, int(round(x / 100)))][1] for x in gx]
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
ziel = len(roads) - next(i for i, r in enumerate(reversed(roads)) if r != "Prinzipalmarkt")   # Zieleinlauf auf dem Prinzipalmarkt (70 m)
roads = glaetten(roads, 80); qs = glaetten(qs, 300)
roads[ziel:] = ["Prinzipalmarkt"] * (len(roads) - ziel)
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
# geschätzte Stücke (schraffiert): die beiden Unterführungen, in denen das DGM die Straße darüber misst (clean.py); die Brücken sind aus
# dem Oberflächenmodell gemessen (dom.py), die Unterführung am Servatiiplatz misst das DGM selbst. Zwei weitere Stellen glättet clean.py
# nur (Sprung zwischen Fuß- und Radwegen am Aegidiitor km 10,4–10,5, ein einzelner Punkt in einer Rinne an der Ecke Ahausweg/Rüschhausweg
# km 35,87); sie sind keine Bauwerke und erscheinen nicht als geschätzte Stücke.
def name_b(r):
    if 15000 < r["a"] < 15800: return "Domagkstraße unter dem Coesfelder Kreuz"
    if 23000 < r["a"] < 23400: return "Am Rüschhaus unter der B 54"
    return None
bridges = [{"a": round(r["a"]), "b": round(r["b"]), "name": name_b(r), "kind": r["kind"]} for r in c["regions"] if name_b(r)]
print("nur geglättet:", [(round(r["a"]), round(r["b"]), r["name"]) for r in c["regions"] if not name_b(r)])
bridges.sort(key=lambda x: x["a"])
# Verpflegung laut Tabelle des Veranstalters (Streckenplan 2026 und Marathonguide 2026, S. 14): km, Art, Ort, Angebot. Zwei Angaben
# passen nicht zum Ort: Kanonierplatz liegt nach der Linie bei km 4,7 (Tabelle 4,3; auch das Symbol im Plan steht bei 4,7), Wulfertstraße
# bei km 29,1 (Tabelle 30,0; Symbol ebenso bei 29,1, der Kilometerkreis 30 steht 0,9 km weiter an der Schelmenstiege). Dort gilt der Ort.
# Staffelwechsel an den Kreuzungen, die der Veranstalter nennt (OSM-Wege an der Linie): Weseler Straße/Ecke Bismarckallee, Nienberge
# Altenberger Straße (Lage des Symbols im Plan), Roxeler Straße/Dingbängerweg.
VP = [(4.3, 4740, "EP", "Kanonierplatz"), (7.5, None, "EP", "Servatiiplatz / Promenade"), (9.5, None, "VP", "Ludgeristraße"),
      (11.8, None, "EP", "Scharnhorststraße / Platz der Weißen Rose"), (14.5, None, "VP", "Vesaliusweg"),
      (17.5, None, "EP", "Mendelstraße / Gievenbecker Weg"), (20.3, None, "VP", "Haus Uhlenkotten"),
      (22.5, None, "EP", "Hermann-Hesse-Straße / Mörikestraße"), (25.3, None, "VP", "Haus Vögeding"), (27.5, None, "EP", "Stodtbrockweg"),
      (30.0, 29100, "VP", "Wulfertstraße"), (32.5, None, "EP", "Ramertsweg"), (35.0, None, "VP", "Mergelberg / Ecke Nünningweg"),
      (37.5, None, "EP", "Gievenbecker Reihe an der Feuerwehr"), (40.0, None, "VP", "Vesaliusweg")]
SW = [(10710, "Weseler Straße / Ecke Bismarckallee", "ca. 10,5 km"), (21150, "Nienberge, Altenberger Straße", "ca. 11,0 km"),
      (31290, "Roxeler Straße / Dingbängerweg", "ca. 10,0 km")]
def kmtext(x): return f"{x / 1000:.1f}".replace(".", ",")
marks, nep, nvp = [], 0, 0
for km_t, m, art, wo in VP:
    m = m or round(km_t * 1000); abw = f" (Tabelle: km {kmtext(km_t * 1000)})" if abs(m - km_t * 1000) > 150 else ""
    if art == "EP":
        nep += 1
        marks.append({"k": m, "s": "Wasser", "c": "water", "n": f"Erfrischungspunkt {nep}, km {kmtext(m)}{abw}, {wo} (Wasser)"})
    else:
        nvp += 1; cola = ", Cola" if km_t >= 20 else ""
        marks.append({"k": m, "s": "Verpflegung", "c": "food",
                      "n": f"Verpflegungspunkt {nvp}, km {kmtext(m)}{abw}, {wo} (Wasser, Elektrolytgetränk, Obst{cola}, Eigenverpflegung)"})
for n, (m, wo, etappe) in enumerate(SW, 1):
    marks.append({"k": m, "s": f"Wechsel {n}", "c": "relay", "n": f"Staffelwechsel {n}, {wo} (Etappe {n}: {etappe} laut Veranstalter)"})
marks.append({"k": 21098, "s": "Halbmarathon", "c": "half", "n": "Halbmarathon"})
marks.sort(key=lambda m: m["k"])
data = {"len": L, "step": STEP, "h": [int(round(v * 100)) for v in hm], "streets": segs, "marks": marks, "bridges": bridges}
json.dump(data, open("data.json", "w"), ensure_ascii=False, separators=(",", ":"))
# Kontrollen
def at(x): return float(np.interp(x, grid, hm))
def asc(w):
    xs = grid[grid <= L]; gr = np.array([(at(min(x + w/2, L)) - at(max(x - w/2, 0))) / (min(x + w/2, L) - max(x - w/2, 0)) for x in xs])
    dh = (gr[1:] + gr[:-1]) / 2 * STEP
    return dh[dh > 0].sum(), -dh[dh < 0].sum(), np.abs(gr).max() * 100, xs[np.argmax(gr)], gr.min()*100, xs[np.argmin(gr)], gr.max()*100
for w in (50, 100, 200, 1000):
    u, d_, gabs, xmax, gmin, xmin, gmax = asc(w)
    print(f"Fenster {w:5d} m: ↑ {u:5.1f} m  ↓ {d_:5.1f} m  steilste bergauf {gmax:4.1f} % bei km {xmax/1000:.2f}, bergab {gmin:4.1f} % bei km {xmin/1000:.2f}")
raw = np.array(c["raw"]); kr = np.array(c["k"]); sel = kr <= L
roh = round(np.clip(np.diff(raw[sel]), 0, None).sum())
open("rohdaten.txt", "w").write(str(roh))
print("Rohdaten Punkt für Punkt ↑", roh, "m; bereinigt ↑", round(np.clip(np.diff(hc[sel]), 0, None).sum(), 1), "m")
print("Höhe min/max", round(hm.min(), 1), round(hm.max(), 1), "bei km", grid[np.argmin(hm)]/1000, grid[np.argmax(hm)]/1000, "Start", round(at(0), 1), "Ziel", round(at(L), 1))
print("Straßenabschnitte", len(segs), "Marken", len(marks), "Brücken", len(bridges))
for sg in segs: print("  ", sg)
for m in marks: print("  ", m)
for b in bridges: print("  ", b)
