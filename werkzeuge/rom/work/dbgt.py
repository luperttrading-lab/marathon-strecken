# Weitere 3D-Klassen der Datenbank DBGT v. 2014 der Regione Lazio (1:5000, photogrammetrisch, Koordinaten mit Höhe über dem Meer,
# EPSG:25833) im Rechteck um die Strecke, über den WFS des Geoportale Regione Lazio: Brücken („Ponte viadotto e cavalcavia“),
# Bauwerke der Verkehrswege („Manufatto di infrastruttura di trasporto“, Linien), Denkmäler und Stadtmöbel („Manufatto monumentale
# e di arredo urbano“, Punkte und Flächen), Kleinbauten („Localizzazione di manufatto edilizio o di arredo-igiene urbana“), Radwege
# („Area di circolazione ciclabile“). Zur Gegenprobe des Höhenmodells und für die Fahrbahnhöhe der Brücken. -> ../dl/dbgt_<klasse>.json
import json, os, time, urllib.request, urllib.parse
KLASSEN = ["web_020301_ponte_a", "web_020205_man_tr_l", "web_020202_mn_mau_p", "web_020202_mn_mau_a", "web_020212_mn_arr_p", "web_010103_ac_cic_a"]
for kl in KLASSEN:
    out = f"../dl/dbgt_{kl}.json"
    if os.path.exists(out): continue
    feat = []
    for start in range(0, 20000, 500):
        q = {"service": "WFS", "version": "2.0.0", "request": "GetFeature", "typeNames": "geonode:" + kl, "outputFormat": "application/json",
             "count": 500, "startIndex": start, "sortBy": "fk", "bbox": "41.855,12.440,41.945,12.500,urn:ogc:def:crs:EPSG::4326"}
        url = "https://geoportale.regione.lazio.it/geoserver/ows?" + urllib.parse.urlencode(q)
        for att in range(5):
            try: d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial)"}), timeout=300)); break
            except Exception as e: print("  Fehler", kl, start, e, flush=True); time.sleep(10 + 10 * att)
        else: raise SystemExit("WFS nicht erreichbar")
        feat += d["features"]
        if len(d["features"]) < 500: break
        time.sleep(1)
    json.dump({"type": "FeatureCollection", "features": feat}, open(out, "w")); print(kl, len(feat), flush=True)
