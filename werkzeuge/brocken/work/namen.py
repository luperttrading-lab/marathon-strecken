# Straßennamen so, wie sie in OSM unter „name“ stehen (deutsch wie auf den Schildern). Leerer Wert: Name des Stücks davor (build.py).
def name(n, prefix=""):
    return (n or "").strip()
