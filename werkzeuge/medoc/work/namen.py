# Bezeichnung eines Wegs: Name aus OSM; sonst Nummer der Départementstraße („D 2“); Ortsstraßen ohne Namen „Weg in <Weiler>“;
# sonst nach dem nächsten Château (OSM-Objekte
# mit Namen „Château …“, „Cave …“, „Domaine …“ bis 600 m von der Linie, ../dl/osm_chateaux.json): „Weg am Château Latour“.
import json, os, re, numpy as np
from pyproj import Transformer
_T = Transformer.from_crs(4326, 2154, always_xy=True)
_D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../dl/osm_chateaux.json")
def _kurz(n):
    n = re.sub(r"\s+Estate$", "", n).replace("Château du Ch. ", "Château ").replace("’", "'")
    return EINHEIT.get(n, n)
# gleiche Châteaux mit verschiedenen Schreibweisen in OSM: wie in der Liste des Veranstalters (Plaquette 2026), mit Bindestrich
EINHEIT = {"Château Lafite Rothschild": "Château Lafite-Rothschild", "Château Mouton Rothschild": "Château Mouton-Rothschild",
           "Château Pontet Canet": "Château Pontet-Canet", "Château Pichon Longueville Comtesse de Lalande": "Château Pichon-Longueville Comtesse de Lalande",
           "Château Pédesclaux": "Château Pedesclaux", "Château Calon Ségur": "Château Calon-Ségur", "Château Phélan Ségur": "Château Phélan-Ségur",
           "Château Lafon Rochet": "Château Lafon-Rochet", "Château Larose Trintaudon": "Château Larose-Trintaudon",
           "Château Gruaud Larose": "Château Gruaud-Larose", "Château Langoa Barton": "Château Langoa-Barton",
           "Château Tronquoy Lalande": "Château Tronquoy-Lalande", "Château Lilian Ladouys": "Château Lilian-Ladouys",
           "Château Grand-Puy Lacoste": "Château Grand-Puy-Lacoste", "Château Grand-Puy Ducasse": "Château Grand-Puy-Ducasse",
           "Château Haut-Bages Libéral": "Château Haut-Bages-Libéral", "Château Laffitte Carcasset": "Château Laffitte-Carcasset",
           "Château Le Bosq": "Château Le Boscq", "Château Beaucaillou": "Château Ducru-Beaucaillou", "Château Tour Saint Fort": "Château Tour Saint-Fort"}
CHATEAUX = []
for e in json.load(open(_D))["elements"]:
    c = e.get("center") or {"lat": e.get("lat"), "lon": e.get("lon")}
    if c["lat"] is None or e["tags"].get("place"): continue
    x, y = _T.transform(c["lon"], c["lat"]); CHATEAUX.append((_kurz(e["tags"]["name"]), x, y))
_C = np.array([[x, y] for _, x, y in CHATEAUX])
def naechstes(x, y, r=600):
    dd = np.hypot(_C[:, 0] - x, _C[:, 1] - y); i = int(np.argmin(dd))
    return CHATEAUX[i][0] if dd[i] <= r else None
# Weiler und Orte (OSM place=hamlet/locality/village/…, ../dl/osm_orte.json), wenn kein Château in der Nähe ist: „Weg bei Marbuzet“
ORTE = []
for e in json.load(open(os.path.join(os.path.dirname(_D), "osm_orte.json")))["elements"]:
    if e["type"] == "node" and e["tags"].get("place") and e["tags"].get("name"):
        ORTE.append((e["tags"]["name"],) + tuple(_T.transform(e["lon"], e["lat"])))
_O = np.array([[x, y] for _, x, y in ORTE])
def ort(x, y, r=700):
    dd = np.hypot(_O[:, 0] - x, _O[:, 1] - y); i = int(np.argmin(dd))
    return ORTE[i][0] if dd[i] <= r else None
def bezeichnung(t, x, y):
    if not t: return ""
    n = (t.get("name") or "").strip()
    if n: return n
    ref = (t.get("ref") or "").strip()
    if re.fullmatch(r"D ?\d+[A-Z]?\d*", ref): return "D " + ref.lstrip("D ").strip()
    if t.get("highway") in ("residential", "tertiary", "secondary", "living_street", "pedestrian"):   # Ortsstraße ohne Namen
        o = ort(x, y); return "Weg in " + o if o else "Weg"
    c = naechstes(x, y)
    if c: return "Weg am " + c if c.startswith("Château") else "Weg an der " + c if c.startswith("Cave") else "Weg an " + c
    o = ort(x, y)
    return ("Weinbergsweg" if t.get("highway") == "track" else "Weg") + (" bei " + o if o else "")
