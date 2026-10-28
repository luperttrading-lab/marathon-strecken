# Höhen im 10-m-Raster, Straßen, Marken und Tunnel/Brücken -> data.json (geht als const D in paris/index.html)
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
# Straßen aus den OSM-Kanten der Linie (../dl/kanten.json; Nominatim greift in Paris oft Gehweg oder Quai daneben),
# Ort (Arrondissement bzw. Gemeinde) aus den Flächen der IGN (orte.py, alle 50 m). Namenlose Verbinder und Stücke unter 80 m
# übernehmen den Namen davor; Orte unter 600 m dem Vorgänger zugeschlagen (die Grenzen laufen oft entlang der Strecke).
g = json.load(open("gpx2026.json")); dg = np.array(g["d"]); kan = json.load(open("../dl/kanten.json"))
KURZ = {"Parc Rives de Seine - Georges Pompidou": "Parc Rives de Seine", "Esplanade des Villes-Compagnons-de-la-Libération": "",
        "Promenade des Champs-Élysées": "Avenue des Champs-Élysées"}   # am Start fängt die Linie auf dem Gehweg an
st = json.load(open("orte2026.json")); sgx = np.array([e[0] for e in st])
gx = gpx_of(np.minimum(grid, L))
ei = np.clip(np.searchsorted(dg, gx, side="right") - 1, 0, len(kan["names"]) - 1)
roads = [KURZ.get(kan["names"][i], kan["names"][i]) for i in ei]
qs = [st[min(len(st) - 1, max(0, int(round(x / 50))))][1] for x in gx]
def glaetten(v, mind):   # mind: Mindestlänge in m, Zahl oder Funktion des Namens
    for i in range(1, len(v)): v[i] = v[i] or v[i - 1]
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[j + 1] == v[i]: j += 1
        if i > 0 and (j + 1 - i) * STEP < (mind(v[i]) if callable(mind) else mind): v[i:j + 1] = [v[i - 1]] * (j + 1 - i)
        i = j + 1
    for i in range(len(v) - 2, -1, -1): v[i] = v[i] or v[i + 1]
    return v
# Gemeinden am Rand des Bois de Vincennes liegen oft nur auf einer Straßenseite (Grenze auf der Avenue de Gravelle): 600 m;
# Arrondissements schon ab 250 m, sonst verschwindet das 9. an der Opéra Garnier
roads = glaetten(roads, 80); qs = glaetten(qs, lambda o: 250 if "Arrondissement" in o else 600)
# Ortswechsel auf den nächsten Straßenwechsel im Umkreis von 100 m legen (die Grenzen laufen über Plätze und Kreuzungen)
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
bridges = [{"a": round(r["a"]), "b": round(r["b"]), "name": KURZ.get(r["name"], r["name"]) or r["kind"], "kind": r["kind"]} for r in c["regions"]]
# Namen nach dem, was darüber bzw. darunter liegt (OSM): Plätze über den Tunneln an der Seine, Gräben unter den Brücken
NAMEN = [(9800, "Rue de Picpus über die Coulée verte"), (20570, "Avenue de Gravelle über den Périphérique"), (20955, "Rue de Charenton"),
         (27700, "Tunnel des Tuileries"), (28890, "Tunnel unter der Place de la Concorde"), (29490, "Tunnel unter der Place du Canada"),
         (30220, "Tunnel unter der Place de l’Alma"), (31130, "Unterführung Place de Varsovie"), (34180, "Boulevard Exelmans")]
for km, nm in NAMEN:
    b_ = [b_ for b_ in bridges if b_["a"] <= km <= b_["b"]]; assert len(b_) == 1, (km, nm); b_[0]["name"] = nm
bridges.sort(key=lambda x: x["a"])
# Verpflegung alle 5 km (Wasser, Iso, Bananen, Trockenobst, Zucker; runpack.fr zum Marathon 2025), Lage nach Kilometer
marks = [{"k": km * 1000, "s": "Verpflegung", "c": "food", "n": f"Verpflegung km {km}"} for km in range(5, 41, 5)]
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
for w in (50, 200, 1000):
    u, d_, gabs, xmax, gmin, xmin, gmax = asc(w)
    print(f"Fenster {w:5d} m: ↑ {u:5.1f} m  ↓ {d_:5.1f} m  steilste bergauf {gmax:4.1f} % bei km {xmax/1000:.2f}, bergab {gmin:4.1f} % bei km {xmin/1000:.2f}")
raw = np.array(c["raw"]); kr = np.array(c["k"]); sel = kr <= L
roh = round(np.clip(np.diff(raw[sel]), 0, None).sum())
open("rohdaten.txt", "w").write(str(roh))
print("Rohdaten Punkt für Punkt ↑", roh, "m; bereinigt ↑", round(np.clip(np.diff(hc[sel]), 0, None).sum(), 1), "m")
print("Höhe min/max", round(hm.min(), 1), round(hm.max(), 1), "bei km", grid[np.argmin(hm)]/1000, grid[np.argmax(hm)]/1000, "Start", round(at(0), 1), "Ziel", round(at(L), 1))
print("Straßenabschnitte", len(segs), "Marken", len(marks), "Tunnel/Brücken", len(bridges))
for sg in segs: print("  ", sg)
