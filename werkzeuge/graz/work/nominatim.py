# Lage benannter Orte über Nominatim (OpenStreetMap), eine Abfrage je Sekunde, Antworten in ../dl/nominatim/. Nur Hilfe für
# stationen.py (Hotspots der Übersichtsgrafik „Auf einen Blick“ als Anker). Aufruf als Modul: ort("Kunsthaus Graz") -> (lat, lon, Name)
import json, os, time, urllib.parse, urllib.request
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../dl/nominatim")
def ort(q):
    f = os.path.join(D, urllib.parse.quote(q, safe="") + ".json")
    if not os.path.exists(f):
        u = "https://nominatim.openstreetmap.org/search?format=jsonv2&limit=3&q=" + urllib.parse.quote(q)
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial)"}), timeout=60).read()
        open(f, "wb").write(r); time.sleep(1.1)
    a = json.load(open(f))
    return (float(a[0]["lat"]), float(a[0]["lon"]), a[0]["display_name"]) if a else None
if __name__ == "__main__":
    import sys
    for q in sys.argv[1:]: print(q, "->", ort(q))
