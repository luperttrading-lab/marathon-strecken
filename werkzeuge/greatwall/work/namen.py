# Namen unter dem Profil: Abschnitt (Straße, Mauer, Treppe, Platz) und Ort (Dorf, Turm).
# Straßen: OSM-Namen in Pinyin (ohne Töne) mit Straßennummer; ohne Namen nach Art des Wegs. Dörfer: die Namen der Karte des
# Veranstalters (Pinyin wie dort), Lage = Mitte der beiden Beschriftungen (lateinisch und chinesisch), eingepasst mit georef.json;
# dazu Shipaogou (石炮沟) aus OSM, durch das die Talstraße führt und das die Karte nicht beschriftet. Türme der Mauer nach dem
# Ausschnitt „Mauer“ der Karte (Reihenfolge Wall point 1, Tower 1, Beacon Tower, Tower 2, Tower 3, Tower 4, Wall point 2, Goat Track,
# Tower 5), zugeordnet zu den Turmknoten in OSM nach dem Anteil am Weg zwischen Tower 1 und Tower 4 (siehe build.py).
import json
import numpy as np
from geo import osm, utm
STRASSE = {"克黄线": "Kehuang Xian (G233)", "长城路": "Changcheng Lu (X590)", "马营公路": "Maying Gonglu (X583)",
           "下营青年桥": "Maying Gonglu (X583)", "白马路": "Baima Lu", "城龙路": "Chenglong Lu", "营树路": "Yingshu Lu", "津西路": "Jinxi Lu"}
ART = {"residential": "Dorfstraße", "living_street": "Dorfstraße", "service": "Dorfstraße", "tertiary": "Landstraße",
       "unclassified": "Landstraße", "secondary": "Landstraße", "trunk": "Landstraße", "track": "Feldweg", "path": "Pfad",
       "footway": "Pfad", "plan": "Weg", "weg": "Weg", "construction": "Landstraße"}
def strassenname(way, art, W):
    if way in W:
        nm = W[way][0].get("name")
        if nm in STRASSE: return STRASSE[nm]
    return ART.get(art)
# Dörfer der Karte: Beschriftung lateinisch + chinesisch
DOERFER = {"Huangyaguan": ("Huangyaguan", "黄崖关"), "Xiaoping'an": ("Xiaoping’an", "小平安"), "Huayuan": ("Huayuan", "village   花园"),
           "Zhongying": ("Zhongying", "中营"), "Xiaying": ("Xiaying", "下营"), "Dongjiafen": ("Dongjiafen", "董家坟"),
           "Baitan": ("Baitan", "白滩"), "Beichedaoyu": ("Beichedaoyu", "北车道峪"), "Da Ping'an": ("Da Ping’an", "大平安"),
           "Duanzhuang": ("Duanzhuang", "段庄")}
def doerfer():
    P = json.load(open("plan2026.json")); M = np.array(json.load(open("georef.json"))["M"])
    out = {}
    for nm, labs in DOERFER.items():
        c = [np.array([(bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2]) for s, bb, size in P["text"] if s in labs]
        out[nm] = np.mean(c, axis=0) @ M[:2] + M[2]
    N, W, NT = osm()
    k = [k for k, t in NT.items() if t.get("name") == "石炮沟村"][0]; x, y = utm(*N[k]); out["Shipaogou"] = np.array([float(x), float(y)])
    return out
