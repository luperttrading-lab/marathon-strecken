# Straßennamen so, wie sie in OSM unter „name“ stehen: in der Schweiz wie auf den Schildern, ohne „ß“ („Seestrasse“,
# „General-Guisan-Quai“, „Alfred-Escher-Strasse“). Leerer Wert: Name des Stücks davor.
def name(n, prefix=""):
    return (n or "").strip()
