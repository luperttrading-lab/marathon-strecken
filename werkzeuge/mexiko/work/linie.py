# Streckenlinie 2026 aus dem OSM-Netz (netz.py): kürzeste Wege zwischen Wegmarken entlang der Straßenfolge, die der Veranstalter
# für 2026 veröffentlicht hat (Beschreibung in der Presse, z. B. grupoanimal.mx und El Financiero, 29./30.08.2026; Plan mit
# Kilometermarken als Bild ../dl/ruta-maraton-cdmx-2026.jpg). Die Wegmarken sind Kreuzungen benannter OSM-Straßen; Wenden liegen
# auf der Kreuzung, an der laut Beschreibung gewendet wird. -> gpx2026.json {"pts": [[lat, lon, 0], …], "d": [Linienmeter]}
import json, numpy as np
from pyproj import Geod
from netz import LL, XY, kreuzung, naechster, weg, kanten_weg, WEGE, T
R = "Avenida Paseo de la Reforma"; INS = "Avenida Insurgentes Sur"; EJ = "Avenida Ejército Nacional Mexicano"
K = kreuzung
MARKEN = [
    ("Start: Insurgentes Sur vor dem Estadio Olímpico Universitario", naechster(19.3320, -99.1896, INS)),
    ("Glorieta de Insurgentes, Ostseite (nach Norden)", naechster(19.42380, -99.16250, weg_id=833370216)),
    ("Glorieta de Insurgentes, Westseite (nach Süden)", naechster(19.42370, -99.16330, weg_id=833370215)),
    ("Oaxaca / Nuevo León (Parque España)", K("Avenida Oaxaca", "Avenida Nuevo León")),
    ("Wende Nuevo León / Citlaltépetl", K("Avenida Nuevo León", "Calle Citlaltépetl", (19.40772, -99.17216))),
    ("Nuevo León / Sonora (Parque España)", naechster(19.4154, -99.1705, "Avenida Sonora")),
    ("Sonora / Chapultepec", K("Avenida Sonora", "Avenida Chapultepec", (19.42108, -99.17400))),
    ("Chapultepec / Florencia", K("Avenida Chapultepec", "Calle Florencia")),
    ("Florencia / Reforma (Ángel)", K("Calle Florencia", R, (19.42657, -99.16752))),
    ("Reforma / Gandhi, Ostseite", K("Calzada Mahatma Gandhi", R, (19.42391, -99.18046))),
    ("Andador Gandhi, Südende", naechster(19.42188, -99.18018)),
    ("Gran Avenida, Ostende", naechster(19.42013, -99.17921, "Gran Avenida")),
    ("Gran Avenida, Süden", naechster(19.41627, -99.18566, "Gran Avenida")),
    ("Gran Avenida, Westen", naechster(19.41918, -99.19066, "Gran Avenida")),
    ("Gran Avenida / Heroico Colegio Militar", naechster(19.4211, -99.18959, "Avenida Heroico Colegio Militar")),
    ("Heroico Colegio Militar / Chivatito", naechster(19.42096, -99.19263, "Avenida Heroico Colegio Militar")),
    ("Chivatito / Reforma", K("Calzada Chivatito", R, (19.42566, -99.19189))),
    ("Wende Reforma / Monte Elbruz", K("Calle Monte Elbruz", R, (19.42697, -99.20047))),
    ("Reforma / Julio Verne", K("Calle Julio Verne", R, (19.42663, -99.19715))),
    ("Julio Verne / Luis G. Urbina", K("Calle Julio Verne", "Avenida Luis Gonzaga Urbina", (19.42917, -99.19715))),
    ("Luis G. Urbina, Mitte", naechster(19.42940, -99.19860, "Avenida Luis Gonzaga Urbina")),
    ("Luis G. Urbina / Edgar Allan Poe", K("Avenida Luis Gonzaga Urbina", "Calle Edgar Allan Poe")),
    ("Edgar Allan Poe / Emilio Castelar", K("Calle Edgar Allan Poe", "Avenida Emilio Castelar")),
    ("Emilio Castelar, Mitte", naechster(19.43020, -99.19900, "Avenida Emilio Castelar")),
    ("Emilio Castelar / Anatole France", K("Avenida Emilio Castelar", "Calle Anatole France")),
    ("Anatole France / Masaryk", K("Calle Anatole France", "Avenida Presidente Masaryk", (19.43176, -99.19758))),
    ("Wende Masaryk / Sudermann", K("Avenida Presidente Masaryk", "Calle Sudermann", (19.43137, -99.18419))),
    ("Masaryk / Moliere", K("Avenida Presidente Masaryk", "Avenida Moliere", (19.43215, -99.20190))),
    ("Moliere / Ejército Nacional", K("Avenida Moliere", EJ, (19.43835, -99.20092))),
    ("Ejército Nacional / Ferrocarril de Cuernavaca", K(EJ, "Avenida Ferrocarril de Cuernavaca", (19.43858, -99.20592))),
    ("Ferrocarril de Cuernavaca / Cervantes Saavedra", K("Avenida Ferrocarril de Cuernavaca", "Boulevard Miguel de Cervantes Saavedra", (19.44013, -99.20488))),
    ("Cervantes Saavedra / Moliere", K("Boulevard Miguel de Cervantes Saavedra", "Prolongación Moliere", (19.44055, -99.20080))),
    ("Moliere / Ejército Nacional (zurück)", K("Prolongación Moliere", EJ, (19.43848, -99.20091))),
    ("Ejército Nacional / Thiers", K(EJ, "Avenida Thiers")),
    ("Thiers / Darwin", K("Avenida Thiers", "Calle Darwin", (19.42973, -99.17428))),
    ("Darwin / Mariano Escobedo", K("Calle Darwin", "Calzada General Mariano Escobedo", (19.42871, -99.17996))),
    ("Campos Elíseos / Rubén Darío", K("Avenida Campos Elíseos", "Calle Rubén Darío", (19.42975, -99.18260))),
    ("Rubén Darío / Schiller", K("Calle Rubén Darío", "Calle Schiller", (19.42847, -99.18555))),
    ("Schiller / Gandhi", K("Calle Schiller", "Calzada Mahatma Gandhi")),
    ("Gandhi / Reforma, Westseite", K("Calzada Mahatma Gandhi", R, (19.42558, -99.19020))),
    ("Reforma / Ignacio Ramírez", K(R, "Calle Ignacio Ramírez", (19.43281, -99.15513))),
    ("Ignacio Ramírez / Plaza de la República", K("Calle Ignacio Ramírez", "Plaza de la República", (19.43565, -99.15470))),
    ("Plaza de la República, Westseite (Monumento a la Revolución)", naechster(19.43620, -99.15562, "Plaza de la República")),
    ("Plaza de la República, Nordwestecke", naechster(19.43668, -99.15545, "Plaza de la República")),
    ("Plaza de la República, Nordseite", naechster(19.43665, -99.15431, "Plaza de la República")),
    ("Plaza de la República / Avenida de la República", K("Plaza de la República", "Avenida de la República")),
    ("Avenida de la República / Reforma", K("Avenida de la República", R, (19.43552, -99.15012))),
    ("Wende Glorieta Simón Bolívar", naechster(19.44072, -99.14383, "Avenida Paseo de la Reforma Norte")),
    ("Reforma / Avenida Juárez", K("Avenida Juárez", R, (19.43550, -99.14930))),
    ("Madero / Bolívar", K("Calle Francisco I. Madero", "Calle Simón Bolívar")),
    ("Bolívar / República de El Salvador", K("Calle Simón Bolívar", "Calle República de El Salvador")),
    ("República de El Salvador / 20 de Noviembre", K("Calle República de El Salvador", "Avenida 20 de Noviembre")),
    ("20 de Noviembre, Nordende am Zócalo", naechster(19.4318, -99.1334, "Calle 20 de Noviembre")),
]
ZIEL = (19.43260, -99.13320)   # Zócalo, Fahnenmast (Asta Bandera Monumental): „la meta … frente al asta bandera“
# Abschnitte, auf denen der Weg auf einer Straße bleiben muss (Einbahnstraßen gegen die Richtung, die das Routing sonst umgeht)
AUF = {"Wende Nuevo León / Citlaltépetl": "Avenida Nuevo León",
       "Ignacio Ramírez / Plaza de la República": "Calle Ignacio Ramírez", "Plaza de la República, Westseite (Monumento a la Revolución)": "Plaza de la República",
       "Plaza de la República, Nordseite": "Plaza de la República", "Plaza de la República, Nordwestecke": "Plaza de la República", "Plaza de la República / Avenida de la República": "Plaza de la República",
       "Avenida de la República / Reforma": "Avenida de la República", "Luis G. Urbina, Mitte": "Avenida Luis Gonzaga Urbina", "Luis G. Urbina / Edgar Allan Poe": "Avenida Luis Gonzaga Urbina",
       "Edgar Allan Poe / Emilio Castelar": "Calle Edgar Allan Poe", "Emilio Castelar, Mitte": "Avenida Emilio Castelar",
       "Emilio Castelar / Anatole France": "Avenida Emilio Castelar", "Anatole France / Masaryk": "Calle Anatole France"}
pfad = [MARKEN[0][1]]
for (na, a), (nb, b) in zip(MARKEN[:-1], MARKEN[1:]):
    p = weg(a, b, AUF.get(nb)); pfad += p[1:]
pts = [tuple(LL[i]) for i in pfad] + [ZIEL]
G = Geod(ellps="WGS84")
d = [0.0]
for (a1, b1), (a2, b2) in zip(pts[:-1], pts[1:]): d.append(d[-1] + G.inv(b1, a1, b2, a2)[2])
json.dump({"pts": [(float(a), float(b), 0.0) for a, b in pts], "d": d}, open("gpx2026.json", "w"))
# Straße je 10 Linienmeter: der OSM-Weg der Kante, auf der die Linie dort läuft (die Linie ist aus diesen Kanten gebaut);
# letztes Stück vom Nordende der 20 de Noviembre über den Platz zum Fahnenmast: Plaza de la Constitución (Zócalo)
kw = [kanten_weg(p, q) for p, q in zip(pfad[:-1], pfad[1:])] + [None]
strassen = []
for s in np.arange(0, d[-1], 10.0):
    i = min(len(kw) - 1, int(np.searchsorted(d, s, side="right")) - 1); w = kw[i]
    t_ = WEGE[w][0] if w else {"name": "Plaza de la Constitución", "highway": "pedestrian"}
    strassen.append([float(s), t_.get("name", ""), t_.get("bridge", ""), t_.get("tunnel", ""), t_.get("layer", ""), t_.get("highway", ""), w or 0])
json.dump(strassen, open("strassen.json", "w"), ensure_ascii=False)
# Marken mit Linienmeter, Straßenfolge
ml = {}; j = 0
for nm, k in MARKEN:
    j = pfad.index(k, j); ml[nm] = d[j]
json.dump(ml, open("wegmarken.json", "w"), ensure_ascii=False, indent=0)
print(f"Linie {d[-1]:.0f} m, {len(pts)} Punkte")
for nm, s in ml.items(): print(f"  {s / 1000:7.3f} km  {nm}")
from itertools import groupby
seq = [(WEGE[kanten_weg(p, q)][0].get("name", "–") if kanten_weg(p, q) else "–") for p, q in zip(pfad[:-1], pfad[1:])]
L = [float(np.hypot(*(XY[p] - XY[q]))) for p, q in zip(pfad[:-1], pfad[1:])]
s = 0
for n, g in groupby(zip(seq, L), key=lambda x: x[0]):
    g = list(g); l = sum(x[1] for x in g); print(f"    {s / 1000:6.2f} {l:6.0f} m  {n}"); s += l
