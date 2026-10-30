# OSM-Straßennetz (alle highway-Wege mit Knoten) im Rechteck um die Strecke -> ../dl/osm_netz.json
# {"nodes": {id: [lat, lon]}, "ways": {id: [tags, [Knoten-IDs]]}}, Aufbau wie bei Mexiko-Stadt (netz.py).
# Overpass-Spiegel maps.mail.ru in 12 Rechtecken (overpass-api.de brach am 30.10.2026 die Verbindung ab, kumi.systems antwortete
# nicht); Rohantworten je Rechteck in ../dl/overpass/, der Spiegel antwortet oft erst nach 20–60 s oder mit 504.
import json, os, time, urllib.request, urllib.parse
CACHE = "../dl/overpass"; os.makedirs(CACHE, exist_ok=True)
LA0, LA1, LO0, LO1 = 41.366, 41.428, 2.146, 2.234          # Paral·lel/Drassanes bis Fòrum, Port Olímpic bis Sagrera
NLA, NLO = 3, 4
nodes, ways = {}, {}
for i in range(NLA):
    for j in range(NLO):
        a0 = LA0 + (LA1 - LA0) * i / NLA; a1 = LA0 + (LA1 - LA0) * (i + 1) / NLA
        o0 = LO0 + (LO1 - LO0) * j / NLO; o1 = LO0 + (LO1 - LO0) * (j + 1) / NLO
        f = f"{CACHE}/teil_{i}_{j}.json"
        if not os.path.exists(f):
            q = f'[out:json][timeout:180];way["highway"]({a0:.5f},{o0:.5f},{a1:.5f},{o1:.5f});out body;>;out skel qt;'
            for att in range(15):
                try:
                    req = urllib.request.Request("https://maps.mail.ru/osm/tools/overpass/api/interpreter",
                                                 data=urllib.parse.urlencode({"data": q}).encode(), headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial)"})
                    E = json.loads(urllib.request.urlopen(req, timeout=240).read()); json.dump(E, open(f, "w")); break
                except Exception as e: print("  Fehler", i, j, e, flush=True); time.sleep(min(60, 5 + 5 * att))
            else: raise SystemExit("Overpass nicht erreichbar")
        E = json.load(open(f))["elements"]
        for e in E:
            if e["type"] == "node": nodes[e["id"]] = [e["lat"], e["lon"]]
            elif e["type"] == "way": ways[e["id"]] = [e.get("tags", {}), e["nodes"]]
        print(i, j, len(E), "Elemente, zusammen", len(ways), "Wege", len(nodes), "Knoten", flush=True)
json.dump({"nodes": nodes, "ways": ways}, open("../dl/osm_netz.json", "w"), ensure_ascii=False)
print(len(ways), "Wege,", len(nodes), "Knoten")
