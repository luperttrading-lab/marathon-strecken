# Straßennamen so, wie sie in OSM unter „name“ stehen (in Barcelona katalanisch). Zusätze in Klammern entfallen: „Gran Via de les
# Corts Catalanes (lateral mar)“ ist die Seitenfahrbahn derselben Straße. Leerer Wert: Name des Stücks davor (build.py).
import re
def name(tags):
    n = (tags or {}).get("name", "").strip()
    return re.sub(r"\s*\(.*?\)\s*$", "", n)
# Ort je Stelle: Barri (73 Stadtviertel, OSM admin_level 10, Nominatim „quarter“), Schreibweise wie in OSM und bei der Stadt, am
# Zeilenanfang mit großem Artikel („La Dreta de l'Eixample“, „El Poblenou“). Die 10 Districtes wären zu grob: l'Eixample deckt
# knapp 21 km der Strecke, Sant Martí 17 km. Fehlt der Barri, gilt der Districte.
def ORT(o):
    n = (o[1] if len(o) > 1 else "") or (o[2] if len(o) > 2 else "")
    return n[:1].upper() + n[1:]
