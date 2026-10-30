# Straßennamen so, wie sie in OSM unter „name“ stehen (deutsch). Leerer Wert: Name des Stücks davor.
def name(tags):
    return (tags or {}).get("name", "").strip()
