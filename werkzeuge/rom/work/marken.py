# Kilometer der Linie (gpx2026.json, 43,6 km entlang der Straßenmitte in OSM) eichen. Eine GPX-Datei oder Karte mit vermessenen
# Kilometermarken veröffentlicht der Veranstalter nicht. Quellen (alle im Infoblatt zum Renntag 2026, ../dl/RRTM26_MARATHON_22.03.pdf,
# und im Event Guide ../dl/Event-Guide_WEB_def.pdf):
#   - Straßenliste mit „Km N“ an 42 Straßen (die Straße, auf der Kilometer N liegt) -> Gegenprobe für alle Kilometer
#   - Plan mit Kilometerschildern (grob gezeichnet, Schilder neben der Linie) -> Gegenprobe, ../dl/img/
#   - Staffelwechsel S1 „km 11,000“ Piazza di Monte Savello, S2 „km 23,500“ Lungotevere Guglielmo Oberdan, S3 „km 31,400“ Viale
#     XVII Olimpiade (Lageplan der Staffel, ../dl/staff_map.pdf); Ausstiegspunkte „circa“ km 23,3 Piazza Montegrappa, km 30 Lungotevere
#     Acqua Acetosa Ecke Via Venezuela, km 35 Piazza delle Belle Arti
# Stützpunkte: wo eine Kilometermarke auf einem Platz steht (Liste) bzw. der Plan sie an eine Ecke setzt: km 5 Ecke Via Cristoforo
# Colombo / Circonvallazione Ostiense (Plan, Liste „Circonvallazione Ostiense Km 5“), km 10 Piazza dell'Emporio, km 11 Piazza di
# Monte Savello (S1), km 15 Piazza Cavour, km 25 Piazzale Maresciallo Giardino, km 26 Piazza Lauro de Bosis, km 37 Piazza del Popolo,
# km 41 Piazza Venezia; Start = Linienanfang, Ziel = Linienende. Dazwischen linear. Die Angaben „circa“ (23,3 / 23,5 / 30 / 35) passen
# nicht alle zur Liste (km 23,3 Piazza Montegrappa und km 24 auf dem Lungotevere Oberdan lägen nach der Linie 1,2 km statt 0,7 km
# auseinander) und werden nur geprüft. -> marken.json {"km": [[km, Linienmeter, Quelle], …], "liste": [[km, Straße, von, bis, geeicht]]}
import json, numpy as np
from pyproj import Transformer
T = Transformer.from_crs(4326, 32633, always_xy=True)
G = json.load(open("gpx2026.json")); d = np.array(G["d"]); P = np.array([p[:2] for p in G["pts"]]); L = d[-1]
ss = np.arange(0, L, 5.0); Q = np.c_[T.transform(np.interp(ss, d, P[:, 1]), np.interp(ss, d, P[:, 0]))]
N = json.load(open("../dl/osm_netz.json")); st = json.load(open("strassen.json")); wm = json.load(open("wegmarken.json"))
def zentrum(name):
    p = np.array([N["nodes"][str(r)] for wid, (t, refs) in N["ways"].items() if t.get("name") == name for r in refs if str(r) in N["nodes"]])
    return p.mean(0)
def proj(la, lo, erw, fen=1500):
    x, y = T.transform(lo, la); sel = np.abs(ss - erw) < fen; dd = np.hypot(Q[sel, 0] - x, Q[sel, 1] - y); i = np.argmin(dd)
    return float(ss[sel][i]), float(dd[i])
STUETZ = []
s5 = wm["Via Cristoforo Colombo / Circonvallazione Ostiense"] if "Via Cristoforo Colombo / Circonvallazione Ostiense" in wm else None
if s5 is None:   # die Kreuzung heißt in OSM „Largo Angelo Fochetti“: Beginn der Circonvallazione Ostiense auf der Linie
    s5 = next(o[0] for o in st if o[1] == "Circonvallazione Ostiense")
STUETZ.append([5.0, round(s5, 1), "Ecke Via Cristoforo Colombo / Circonvallazione Ostiense (Plan, Liste)"])
for km, platz, erw in [(10.0, "Piazza dell'Emporio", 10100), (11.0, "Piazza di Monte Savello", 11300), (15.0, "Piazza Cavour", 15200),
                       (25.0, "Piazzale Maresciallo Giardino", 25800), (26.0, "Piazza Lauro de Bosis", 26700), (37.0, "Piazza del Popolo", 38100),
                       (41.0, "Piazza Venezia", 42300)]:
    s_, e_ = proj(*zentrum(platz), erw); STUETZ.append([km, round(s_, 1), f"{platz} ({e_:.0f} m neben der Linie)"])
_s = np.array([0.0] + [m[1] for m in STUETZ] + [L]); _k = np.array([0.0] + [m[0] * 1000 for m in STUETZ] + [42195.0])
assert np.all(np.diff(_s) > 0)
def official(s): return np.interp(np.asarray(s, float), _s, _k)
print("Stützpunkte (km, Linienmeter, Faktor seit vorigem):")
for i in range(1, len(_s)): print(f"  {_k[i] / 1000:7.3f} {_s[i]:8.0f}  {(_k[i] - _k[i - 1]) / (_s[i] - _s[i - 1]):.3f}")
# Gegenprobe mit der Straßenliste: liegt Kilometer N nach der Eichung auf der genannten Straße?
LISTE = [(1, "Via del Teatro di Marcello"), (2, "Lungotevere Aventino"), (3, "Via Marmorata"), (4, "Viale Marco Polo"), (5, "Circonvallazione Ostiense"),
         (6, "Ponte Settimia Spizzichino"), (7, "Via del Porto Fluviale"), (8, "Via Giovanni Volpato"), (9, "Via Beniamino Franklin"),
         (10, "Piazza dell'Emporio"), (11, "Lungotevere dei Pierleoni"), (12, "Lungotevere dei Tebaldi"), (13, "Via San Pio Decimo"), (14, "Via di Porta Castello"),
         (15, "Piazza Cavour"), (16, "Lungotevere in Augusta"), (17, "Via Cola di Rienzo"), (18, "Viale Giulio Cesare"), (19, "Via Fornovo"),
         (20, "Viale delle Milizie"), (21, "Circonvallazione Trionfale"), (21.0975, "Circonvallazione Trionfale"), (22, "Viale Giuseppe Mazzini"),
         (23, "Via Oslavia"), (24, "Lungotevere Guglielmo Oberdan"), (25, "Piazzale Maresciallo Giardino"), (26, "Piazza Lauro de Bosis"),
         (27, "Viale Antonino di San Giuliano"), (28, "Lungotevere Maresciallo Cadorna"), (29, "Lungotevere Grande Ammiraglio Thaon di Revel"),
         (30, "Lungotevere dell'Acqua Acetosa"), (31, "Viale XVII Olimpiade"), (32, "Via Flaminia"), (33, "Via Giovanni Paolo Pannini"),
         (34, "Lungotevere Flaminio"), (35, "Lungotevere delle Navi"), (36, "Passeggiata di Ripetta"), (37, "Piazza del Popolo"),
         (38, "Via dei Due Macelli"), (39, "Via della Fontanella di Borghese"), (40, "Corso del Rinascimento"), (41, "Piazza Venezia")]
s_st = np.array([o[0] for o in st]); n_st = [o[1] for o in st]; k_st = official(s_st)
liste = []; aus = []
for km, name in LISTE:
    idx = [i for i, x in enumerate(n_st) if x == name and abs(k_st[i] - km * 1000) < 1500]
    if not idx: aus.append((km, name, "nicht auf der Linie")); continue
    # zusammenhängendes Stück, das km am nächsten liegt
    grp = np.split(np.array(idx), np.where(np.diff(idx) > 2)[0] + 1)
    g = min(grp, key=lambda g: min(abs(k_st[g[0]] - km * 1000), abs(k_st[g[-1]] + 10 - km * 1000)))
    a, b = float(k_st[g[0]]), float(official(s_st[g[-1]] + 10))
    fehl = 0 if a - 1 <= km * 1000 <= b + 1 else (a - km * 1000 if km * 1000 < a else km * 1000 - b)
    liste.append([km, name, round(a), round(b), round(fehl)])
    if fehl > 0: aus.append((km, name, f"geeicht {a / 1000:.2f}–{b / 1000:.2f}, {fehl:.0f} m daneben"))
print("Straßenliste: Kilometer außerhalb ihrer Straße:"); [print("  ", x) for x in aus]
f = [x[4] for x in liste]; print(f"  {sum(v > 0 for v in f)} von {len(f)} daneben, höchstens {max(f)} m, Mittel {np.mean(f):.0f} m")
# Weitere Angaben des Veranstalters zur Lage
for km, wo, la_lo, erw in [(23.3, "Piazza Montegrappa (Ausstieg, circa)", zentrum("Piazza Monte Grappa"), 24500),
                           (30.0, "Lungotevere Acqua Acetosa Ecke Via Venezuela (Ausstieg, circa)", None, 31170),
                           (35.0, "Piazza delle Belle Arti (Ausstieg, circa)", zentrum("Piazzale delle Belle Arti"), 35600)]:
    s_ = wm["Lungotevere dell'Acqua Acetosa / Via Venezuela"] if la_lo is None else proj(*la_lo, erw)[0]
    print(f"  {wo}: Angabe km {km}, nach der Eichung km {official(s_) / 1000:.2f}")
json.dump({"km": STUETZ, "liste": liste}, open("marken.json", "w"), ensure_ascii=False, indent=0)
