# Straßennamen so, wie sie in OSM unter „name“ stehen. Leerer Wert: Name des Stücks davor.
def name(n, prefix=""):
    return (n or "").strip()
