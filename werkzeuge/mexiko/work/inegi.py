# Höhenmodelle des INEGI (Continuo de Elevaciones Mexicano, Modelos Digitales de Elevación, Tipo Terreno) für die fünf Blätter
# 1:10 000 unter der Strecke laden -> ../dl/inegi/<Blatt>_<Ausgabe>/. Je Blatt gibt es drei Ausgaben:
#   5m2011  „Alta Resolución LiDAR“, 5-m-Raster aus einer Laserbefliegung von 2007 (Leica ALS50 II), XYZ-Text, NAVD88
#   5m2017/5m2018  5-m-Raster aus einer fotogrammetrischen Punktwolke (Satelliten-Stereobilder Dezember 2017), BIL, NAVD88
#   15m2020  1,5-m-Raster aus Satelliten-Stereobildern 2017 und einer fotogrammetrischen Punktwolke 2019, BIL, Geoide GGM10
# (Liste der Blätter: getFormato10k.do, Downloads: getF10KDescarga.do, beide unter www.inegi.org.mx/app/geo2/elevacionesmex/)
import json, os, time, urllib.request, urllib.parse, zipfile, io
OUT = "../dl/inegi"; os.makedirs(OUT, exist_ok=True)
BLAETTER = ["E14A39E1", "E14A39B3", "E14A39B4", "E14A39B1", "E14A39B2"]   # E1 Ciudad Universitaria, B3/B4 Insurgentes bis Centro, B1/B2 nördlich 19,4375°
def frage(res, cve):
    d = urllib.parse.urlencode({"res": res, "mod": "T", "cve": cve}).encode()
    req = urllib.request.Request("https://www.inegi.org.mx/app/geo2/elevacionesmex/getF10KDescarga.do", data=d, headers={"User-Agent": "MarathonProfil/1.0"})
    return json.load(urllib.request.urlopen(req, timeout=60))
for cve in BLAETTER:
    for res in ("5", "1.5"):
        for e in frage(res, cve):
            for teil in filter(None, e["archivo"].split("|")):
                suf = teil.split(",")[0]
                if res == "5" and e["edicion"] >= 2017 and suf == "_b.zip": tag = f"5m{e['edicion']}"
                elif res == "5" and e["edicion"] == 2011 and suf == "_as.zip": tag = "5m2011"
                elif res == "1.5" and suf == "_b.zip": tag = f"15m{e['edicion']}"
                else: continue
                ziel = f"{OUT}/{cve}_{tag}"
                if os.path.isdir(ziel) and os.listdir(ziel): continue
                url = e["url_descarga"] + suf
                for att in range(4):
                    try: data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "MarathonProfil/1.0"}), timeout=900).read(); break
                    except Exception as ex: print("  Fehler", url, ex); time.sleep(10)
                os.makedirs(ziel, exist_ok=True)
                with zipfile.ZipFile(io.BytesIO(data)) as z:
                    for zi in z.infolist():
                        name = os.path.basename(zi.filename.replace("\\", "/"))
                        if name and not zi.is_dir(): open(f"{ziel}/{name}", "wb").write(z.read(zi))
                print(cve, tag, e["edicion"], round(len(data) / 1e6, 1), "MB", sorted(os.listdir(ziel)), flush=True)
                time.sleep(1)
