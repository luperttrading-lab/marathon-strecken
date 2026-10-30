# Streckenlinie aus dem OSM-Netz (netz.py) nach der Straßenliste des Veranstalters (Infoblatt zum Renntag 2026,
# ../dl/RRTM26_MARATHON_22.03.pdf, Seite 4, „Partenza / Start: Via dei Fori Imperiali … Arrivo / Finish km 42,195: Circo Massimo“,
# 151 Straßen und Plätze in Laufrichtung, ../dl/strassenliste.txt). Die Namen sind hier so geschrieben, wie sie in OSM stehen
# (OSM schreibt Ordnungszahlen aus: „Via Leone Quarto“ für „Via Leone IV“, „Via San Pio Decimo“ für „Via San Pio X“).
# Wegmarken: die Kreuzung je zweier aufeinanderfolgender Straßen der Liste (bei mehreren Knoten der, den man von der vorigen
# Marke aus auf der genannten Straße am günstigsten erreicht; das wählt auf zweibahnigen Straßen die Fahrbahn in Laufrichtung).
# Dazwischen der kürzeste Weg, auf dem andere Straßen das Dreifache kosten. Wo zwei Straßen der Liste in OSM keinen gemeinsamen
# Knoten haben (Plätze als Fläche, Brückenköpfe), entfällt die Marke. Zusätze von Hand in EXTRA (siehe dort).
# -> gpx2026.json {"pts": [[lat, lon, 0], …], "d": [Linienmeter]}, strassen.json (Weg je 10 m), wegmarken.json
import json, numpy as np
from pyproj import Geod
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
import netz
from netz import LL, XY, WEGE, T, namen_knoten, naechster, kanten_weg
SEQ = ["Via dei Fori Imperiali", "Piazza Venezia", "Piazza d'Aracoeli", "Via del Teatro di Marcello", "Via Luigi Petroselli",
       "Piazza della Bocca della Verità", "Via di Santa Maria in Cosmedin", "Lungotevere Aventino", "Piazza dell'Emporio", "Via Marmorata",
       "Via Raffaele Persichetti", "Piazzale Ostiense", "Viale Marco Polo", "Via Cristoforo Colombo", "Circonvallazione Ostiense",
       "Ponte Settimia Spizzichino", "Via Ostiense", "Via del Porto Fluviale", "Ponte dell'Industria", "Via Antonio Pacinotti",
       "Piazza della Radio", "Via Giovanni Volpato", "Via Portuense", "Via Ettore Rolli", "Via degli Stradivari", "Ponte Testaccio",
       "Largo Giovanni Battista Marzi", "Via Aldo Manuzio", "Via Beniamino Franklin", "Via Galvani", "Via Nicola Zabaglia",
       "Piazza di Santa Maria Liberatrice", "Via Giovanni Branca", "Via Marmorata", "Piazza dell'Emporio", "Lungotevere Aventino",
       "Lungotevere dei Pierleoni", "Piazza di Monte Savello", "Lungotevere De' Cenci", "Lungotevere dei Vallati", "Lungotevere dei Tebaldi",
       "Lungotevere dei Sangallo", "Lungotevere dei Fiorentini", "Piazza Pasquale Paoli", "Ponte Vittorio Emanuele Secondo",
       "Via San Pio Decimo", "Via della Conciliazione", "Piazza Pio Dodicesimo", "Largo del Colonnato", "Via dei Corridori",
       "Borgo Sant'Angelo", "Via di Porta Castello", "Largo di Porta Castello", "Via Giovanni Vitelleschi", "Via Properzio",
       "Via Crescenzio", "Piazza Cavour", "Via Vittoria Colonna", "Ponte Cavour", "Lungotevere in Augusta", "Ponte Regina Margherita",
       "Via Cola di Rienzo", "Piazza del Risorgimento", "Viale dei Bastioni di Michelangelo", "Via Leone Quarto", "Viale Giulio Cesare",
       "Via Fornovo", "Viale delle Milizie", "Largo Trionfale", "Via Andrea Doria", "Piazzale degli Eroi", "Circonvallazione Trionfale",
       "Circonvallazione Clodia", "Piazzale Clodio", "Viale Giuseppe Mazzini", "Piazza Giuseppe Mazzini", "Via Oslavia",
       "Piazza Bainsizza", "Viale Carso", "Piazza del Fante", "Via Monte Zebio", "Via Marcello Prestinari", "Piazza Monte Grappa",
       "Lungotevere Guglielmo Oberdan", "Lungotevere della Vittoria", "Piazzale Maresciallo Giardino", "Viale dei Gladiatori",
       "Via Roberto Morra di Lavriano", "Lungotevere Maresciallo Cadorna", "Piazza Lauro de Bosis", "Lungotevere Maresciallo Diaz",
       "Viale Paolo Boselli", "Piazzale della Farnesina", "Viale Antonino di San Giuliano", "Lungotevere Maresciallo Diaz",
       "Piazza Lauro de Bosis", "Lungotevere Maresciallo Cadorna", "Ponte della Musica Armando Trovajoli", "Lungotevere Flaminio",
       "Lungotevere Grande Ammiraglio Thaon di Revel", "Lungotevere Salvo D'Acquisto", "Lungotevere dell'Acqua Acetosa", "Via Venezuela",
       "Via India", "Viale XVII Olimpiade", "Viale Tiziano", "Piazza Apollodoro", "Via Flaminia", "Viale del Vignola",
       "Via Pier della Francesca", "Via Giovanni Paolo Pannini", "Viale Pinturicchio", "Piazza Gentile da Fabriano", "Lungotevere Flaminio",
       "Piazzale delle Belle Arti", "Lungotevere delle Navi", "Lungotevere Arnaldo da Brescia", "Passeggiata di Ripetta", "Piazza Augusto Imperatore", "Via dei Pontefici", "Via del Corso", "Piazza del Popolo", "Via del Babuino",
       "Piazza di Spagna", "Via dei Due Macelli", "Largo del Tritone", "Via del Tritone", "Via del Corso", "Largo Carlo Goldoni",
       "Via della Fontanella di Borghese", "Largo della Fontanella di Borghese", "Piazza Borghese", "Via del Clementino", "Piazza Nicosia",
       "Via di Monte Brianzo", "Piazza di Ponte Umberto I", "Via Giuseppe Zanardelli", "Piazza di Tor Sanguigna", "Piazza delle Cinque Lune",
       "Corso del Rinascimento", "Piazza di Sant'Andrea della Valle", "Corso Vittorio Emanuele II", "Largo di Torre Argentina",
       "Corso Vittorio Emanuele II", "Piazza del Gesù", "Via del Plebiscito", "Piazza Venezia", "Via del Teatro di Marcello",
       "Via Luigi Petroselli", "Piazza della Bocca della Verità", "Via della Greca", "Via dell'Ara Massima di Ercole"]
# Weitere Schreibweisen derselben Straße in OSM (gleich behandelt)
ALIAS = {"Corso Vittorio Emanuele II": ["Corso Vittorio Emanuele Secondo"], "Piazza del Popolo": ["Piazza del popolo"],
         "Lungotevere Grande Ammiraglio Thaon di Revel": ["Lungotevere Thaon di Revel"], "Piazza Pio Dodicesimo": ["Piazza Papa Pio Dodicesimo"]}
def namen(n): return [n] + ALIAS.get(n, [])
def knoten_von(n):
    s = set()
    for x in namen(n): s |= namen_knoten(x)
    return s
START = (41.89253, 12.48853)   # Startlinie auf der Via dei Fori Imperiali „altezza Cartine Geografiche Antica Roma“ (Basilica di Massenzio)
ZIEL = (41.88676, 12.48425)    # Ziel im Circo Massimo: gut 90 m hinter dem Westende auf dem Weg an der Südseite (Plan „Finish Area“)
# Von Hand: (nach der Kreuzung, Liste von Zwischenpunkten (lat, lon, Straße)) – Wenden und Stellen, an denen das Netz sonst abkürzt
EXTRA = {
    # Von der Piazza Venezia auf der Via del Teatro di Marcello am Vittoriano entlang zur Piazza d'Aracoeli (nicht über die
    # Piazza di San Marco, die das Netz sonst nimmt: zwischen Piazza Venezia und Piazza d'Aracoeli fehlt in OSM ein gemeinsamer Knoten)
    "Via dei Fori Imperiali / Piazza Venezia": [(41.89515, 12.48213, "Via del Teatro di Marcello")],
    # Via del Tritone stadtauswärts auf der Busspur (OSM: service) bis Largo Chigi, dort auf die Via del Corso
    "Largo del Tritone / Via del Tritone": [(41.90215, 12.48300, "Via del Tritone", 366692689), (41.90148, 12.48040, "Largo Chigi", 107578023),
                                            (41.90159, 12.48018, "Via del Corso")],
    # „Sottopasso di Ripetta“ (Liste des Veranstalters, im Plan gestrichelt): stadteinwärts durch die Unterführungen der Hauptfahrbahn
    # des Lungotevere Arnaldo da Brescia (OSM tunnel=yes, layer −1, zwischen Ponte Matteotti und Ponte Regina Margherita), nicht über
    # die Nebenfahrbahnen oben
    # (Südende der Unterführungen 117073728 und 24186802, OSM-Weg und Knoten)
    "Lungotevere delle Navi / Lungotevere Arnaldo da Brescia": [(41.9112939, 12.4727704, "Lungotevere Arnaldo da Brescia", 117073728),
                                                                (41.9098916, 12.4735281, "Lungotevere Arnaldo da Brescia", 24186802)],
}
TUNNEL_W = np.array([WEGE[w][0].get("tunnel") in ("yes", "building_passage") for w in netz.KW])
def kosten_graph(nn, tunnel=False):
    fak = np.array([1.0 if netz.NAME_W[w] in nn else 3.0 for w in netz.KW])
    if tunnel: fak = np.where(TUNNEL_W, fak / 4, fak)   # Unterführung erlaubt wie eine Straße
    return csr_matrix((netz.cost * fak, (netz.rows, netz.cols)), shape=netz.G.shape)
def pfad(pred, a, b):
    p = [b]
    while p[-1] != a: p.append(pred[p[-1]])
    return p[::-1]
cur = naechster(*START, name="Via dei Fori Imperiali"); weg_k = [cur]; marken = [("Start", cur)]
offen = set(namen(SEQ[0]))                       # Straßen, auf denen der nächste Abschnitt laufen darf
for i in range(len(SEQ) - 1):
    a, b = SEQ[i], SEQ[i + 1]
    kand = sorted(knoten_von(a) & knoten_von(b))
    offen |= set(namen(a))
    if not kand: offen |= set(namen(b)); continue
    g = kosten_graph(offen)
    d, pred = dijkstra(g, indices=cur, return_predecessors=True)
    k = min(kand, key=lambda q: d[q]); assert np.isfinite(d[k]), (a, b)
    weg_k += pfad(pred, cur, k)[1:]; cur = k; marken.append((f"{a} / {b}", k))
    for e in EXTRA.get(f"{a} / {b}", []):
        la, lo, st = e[:3]
        q = naechster(la, lo, weg_id=e[3]) if len(e) > 3 else naechster(la, lo, st)
        g = kosten_graph(set(namen(st)), len(e) > 3 and WEGE[e[3]][0].get("tunnel") == "yes"); d, pred = dijkstra(g, indices=cur, return_predecessors=True)
        weg_k += pfad(pred, cur, q)[1:]; cur = q; marken.append((f"{st} (Zwischenpunkt)", q))
    offen = set(namen(b)) | {x for e in EXTRA.get(f"{a} / {b}", [])[-1:] for x in namen(e[2])}
# Ende: ein Stück auf der Via dell'Ara Massima di Ercole, dann in den Circo Massimo zum Ziel
q = naechster(41.88742, 12.48236, "Via dell'Ara Massima di Ercole"); g = kosten_graph(set(namen("Via dell'Ara Massima di Ercole")))
d, pred = dijkstra(g, indices=cur, return_predecessors=True); weg_k += pfad(pred, cur, q)[1:]; cur = q; marken.append(("Einlauf Circo Massimo", q))
pts = [tuple(LL[i]) for i in weg_k] + [(41.88709, 12.48326), ZIEL]
# doppelte Knoten (Wende auf demselben Knoten) entfernen
pp = [pts[0]]
for p in pts[1:]:
    if p != pp[-1]: pp.append(p)
pts = pp
G = Geod(ellps="WGS84")
d = [0.0]
for (a1, b1), (a2, b2) in zip(pts[:-1], pts[1:]): d.append(d[-1] + G.inv(b1, a1, b2, a2)[2])
json.dump({"pts": [(float(a), float(b), 0.0) for a, b in pts], "d": d}, open("gpx2026.json", "w"))
# Straße je 10 Linienmeter: der OSM-Weg der Kante, auf der die Linie dort läuft
kw = [kanten_weg(p, q) for p, q in zip(weg_k[:-1], weg_k[1:])] + [None, None, None]
dk = [0.0]
for p, q in zip(weg_k[:-1], weg_k[1:]): dk.append(dk[-1] + G.inv(LL[p][1], LL[p][0], LL[q][1], LL[q][0])[2])
strassen = []
for s in np.arange(0, d[-1], 10.0):
    j = int(np.searchsorted(dk, s, side="right")) - 1; w = kw[j] if j < len(kw) else None
    t_ = WEGE[w][0] if w else {"name": "Circo Massimo", "highway": "track"}
    strassen.append([float(s), t_.get("name", ""), t_.get("bridge", ""), t_.get("tunnel", ""), t_.get("layer", ""), t_.get("highway", ""), w or 0,
                     t_.get("alt_name", "")])
json.dump(strassen, open("strassen.json", "w"), ensure_ascii=False)
ml = {}; j = 0
for nm, k in marken:
    j = weg_k.index(k, j); ml[nm] = dk[j]
json.dump(ml, open("wegmarken.json", "w"), ensure_ascii=False, indent=0)
print(f"Linie {d[-1]:.0f} m, {len(pts)} Punkte")
from itertools import groupby
s = 0
for n, g_ in groupby(strassen, key=lambda o: o[1]):
    g_ = list(g_); print(f"    {g_[0][0] / 1000:6.2f} {len(g_) * 10:5d} m  {n}")
