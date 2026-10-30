# Höhenlinien der Regione Lazio (DBGT v. 2014, Klasse „Curva di livello“, 1:5000, Abstand 5 m, Höhen über dem Meer) im Rechteck
# um die Strecke, über den WFS des Geoportale Regione Lazio (geoportale.regione.lazio.it/geoserver/ows, Ebene geonode:curve_livello,
# EPSG:25833), seitenweise zu 100 Linien. Nur zur Gegenprobe des Höhenmodells (vergleich.py): wo die Strecke eine Höhenlinie kreuzt,
# kennt man die Höhe dort auf etwa einen Meter. -> ../dl/curve_livello.json (GeoJSON)
import json, os, time, urllib.request, urllib.parse
OUT = "../dl/curve_livello.json"
feat = []
for start in range(0, 2000, 100):
    q = {"service": "WFS", "version": "2.0.0", "request": "GetFeature", "typeNames": "geonode:curve_livello", "outputFormat": "application/json",
         "count": 100, "startIndex": start, "sortBy": "classid", "bbox": "41.855,12.440,41.945,12.500,urn:ogc:def:crs:EPSG::4326"}
    url = "https://geoportale.regione.lazio.it/geoserver/ows?" + urllib.parse.urlencode(q)
    for att in range(5):
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial)"}), timeout=300)); break
        except Exception as e: print("  Fehler", start, e, flush=True); time.sleep(10 + 10 * att)
    else: raise SystemExit("WFS nicht erreichbar")
    feat += d["features"]; print(start, len(d["features"]), "zusammen", len(feat), "von", d.get("numberMatched"), flush=True)
    if len(d["features"]) < 100: break
    time.sleep(1)
json.dump({"type": "FeatureCollection", "crs": d.get("crs"), "features": feat}, open(OUT, "w"))
print(len(feat), "Höhenlinien")
