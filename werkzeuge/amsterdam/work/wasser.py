# Wasserflächen aus den OSM-Rohdaten (../dl/osmapi/): geschlossene Wege mit natural=water (auch water=*, waterway=riverbank)
# und die äußeren Ringe von Multipolygonen natural=water (die Amstel ist ein Multipolygon aus vielen Wegen).
# -> ../dl/osm_wasser.json: Liste von Linienzügen (Breite, Länge) der Uferlinien
import json, os, xml.etree.ElementTree as ET
CACHE = "../dl/osmapi"
knoten, wege, rel_wege = {}, {}, set()
for f in sorted(os.listdir(CACHE)):
    if not f.endswith(".xml"): continue
    r = ET.parse(f"{CACHE}/{f}").getroot()
    for nd in r.iter("node"): knoten[int(nd.get("id"))] = (float(nd.get("lat")), float(nd.get("lon")))
    for w in r.iter("way"):
        wege[int(w.get("id"))] = ({t.get("k"): t.get("v") for t in w.iter("tag")}, [int(x.get("ref")) for x in w.iter("nd")])
    for rel in r.iter("relation"):
        tg = {t.get("k"): t.get("v") for t in rel.iter("tag")}
        if tg.get("type") == "multipolygon" and (tg.get("natural") == "water" or tg.get("waterway") == "riverbank" or tg.get("water")):
            for m in rel.iter("member"):
                if m.get("type") == "way" and m.get("role") in ("outer", "inner", ""): rel_wege.add(int(m.get("ref")))
out = []
for wid, (tg, nds) in wege.items():
    if wid in rel_wege or ((tg.get("natural") == "water" or tg.get("waterway") == "riverbank") and nds[0] == nds[-1]):
        ll = [knoten[k] for k in nds if k in knoten]
        if len(ll) >= 2: out.append(ll)
json.dump(out, open("../dl/osm_wasser.json", "w"))
print(len(out), "Uferlinien, davon", sum(1 for w in rel_wege if w in wege), "aus Multipolygonen")
