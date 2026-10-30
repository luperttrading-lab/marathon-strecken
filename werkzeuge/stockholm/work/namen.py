# Straßennamen so, wie sie in OSM unter „name“ stehen (schwedisch, wie auf den Schildern). Leerer Wert: Name des Stücks davor.
def name(n, prefix=""):
    return (n or "").strip()
