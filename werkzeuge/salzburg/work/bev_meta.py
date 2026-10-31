# Aktualität der BEV-Laserdaten an der Strecke: Metadatenübersicht des BEV (ALS_2025_Meta_DTM_DSM_3035.shp aus
# https://data.bev.gv.at/download/ALS/DTM/20250915/Metadatenuebersicht_SHP_DTM_DSM_20250915.zip, ../dl/bev/meta/), Flächen je
# Befliegung mit Datum und Bundesland. Kleiner Leser für Shapefile (Polygone) und DBF ohne Zusatzpakete.
# Ausgabe: Felder der Flächen, in denen Start, Hellbrunn und Moosstraße liegen.
import struct, sys
from pyproj import Transformer
B = "../dl/bev/meta/ALS_2025_Meta_DTM_DSM_3035"
def dbf(f):
    b = open(f, "rb").read(); n, hl, rl = struct.unpack("<IHH", b[4:12])
    felder = []; p = 32
    while b[p] != 0x0D:
        name = b[p:p + 11].split(b"\0")[0].decode("latin1"); l = b[p + 16]; felder.append((name, l)); p += 32
    out = []
    for i in range(n):
        r = b[hl + i * rl + 1: hl + (i + 1) * rl]; q = 0; d = {}
        for name, l in felder: d[name] = r[q:q + l].decode("utf-8", "replace").strip(); q += l
        out.append(d)
    return out
def shp(f):
    b = open(f, "rb").read(); p = 100; out = []
    while p < len(b):
        _, laenge = struct.unpack(">ii", b[p:p + 8]); p += 8; inhalt = b[p:p + 2 * laenge]; p += 2 * laenge
        typ = struct.unpack("<i", inhalt[:4])[0]
        if typ == 0: out.append([]); continue
        np_, npt = struct.unpack("<ii", inhalt[36:44]); teile = list(struct.unpack(f"<{np_}i", inhalt[44:44 + 4 * np_]))
        pts = struct.unpack(f"<{2 * npt}d", inhalt[44 + 4 * np_: 44 + 4 * np_ + 16 * npt]); pts = list(zip(pts[::2], pts[1::2]))
        out.append([pts[a:b_] for a, b_ in zip(teile, teile[1:] + [npt])])
    return out
def innen(x, y, ringe):
    c = False
    for r in ringe:
        for (x1, y1), (x2, y2) in zip(r, r[1:] + r[:1]):
            if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1): c = not c
    return c
rec = dbf(B + ".dbf"); geo = shp(B + ".shp")
print(len(rec), "Flächen; Felder:", list(rec[0].keys()))
T = Transformer.from_crs(4326, 3035, always_xy=True)
for name, la, lo in (("Start Staatsbrücke", 47.80122, 13.04473), ("Hellbrunn", 47.7626, 13.0609), ("Moosstraße", 47.785, 13.0270)):
    x, y = T.transform(lo, la)
    for d, g in zip(rec, geo):
        if g and innen(x, y, g): print(name, "->", d)
