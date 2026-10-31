# Straßennamen so, wie sie in OSM unter „name“ stehen (zum Teil mit Kahakō wie auf den neueren Schildern, „Kalākaua Avenue“).
# Das ʻokina schreibt OSM mal als ʻ (U+02BB), mal als Apostroph ’ oder ': hier einheitlich ʻ („Kalanianaʻole Highway“, „Hawaiʻi Kai
# Drive“). Leerer Wert: Name des Stücks davor.
def name(n, prefix=""):
    n = (n or "").strip()
    for a in ("’", "‘", "'"): n = n.replace(a, "ʻ")
    return n
