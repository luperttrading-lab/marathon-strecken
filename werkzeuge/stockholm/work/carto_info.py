# Übersicht über die Tabellen der „dynamischen Karte“ des Veranstalters (CARTO-Konto „marathon“, Tabellen km, energi, bana;
# abgerufen über die öffentliche SQL-API als GeoJSON nach ../dl/carto/). Nur Ausgabe.
import json, sys
from collections import Counter
D = "../dl/carto/"
for t in ("km", "energi", "bana"):
    F = json.load(open(D + t + ".geojson"))["features"]
    print(t, len(F), Counter((f["properties"].get("map"), f["properties"].get("stylegroup")) for f in F))
    print("  zuletzt geändert", max(f["properties"]["updated_at"] for f in F))
if len(sys.argv) > 1:
    t = sys.argv[1]
    F = json.load(open(D + t + ".geojson"))["features"]
    for f in sorted(F, key=lambda f: f["properties"]["updated_at"]):
        p = f["properties"]
        g = f["geometry"]["coordinates"] if f["geometry"]["type"] == "Point" else f["geometry"]["type"]
        print(p.get("map"), p.get("stylegroup"), p.get("name"), p.get("description"), p.get("name_en"), p["updated_at"][:10], g)
