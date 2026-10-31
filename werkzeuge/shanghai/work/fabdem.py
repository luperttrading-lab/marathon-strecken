# FABDEM V1-2 (Hawker et al. 2022, University of Bristol / Fathom; Copernicus GLO-30 ohne Gebäude und Wald, 1″-Raster,
# Lizenz CC BY-NC-SA 4.0), öffentlich ohne Anmeldung auf data.bris.ac.uk in Zip-Dateien zu 10 × 10 Grad. Der Server kann
# Teilabrufe (Accept-Ranges), daher nur das Inhaltsverzeichnis am Ende der Zip-Datei für 30–40° N, 120–130° O und die eine
# benötigte Kachel N31E121 holen -> ../dl/dem/fabdem_N31E121.tif (Muster: werkzeuge/stockholm/work/fabdem.py). Dazu die
# Vergleichsmodelle Copernicus GLO-30 (AWS copernicus-dem-30m) und SRTM 1″ (AWS Terrain Tiles „skadi“), beide ohne Anmeldung.
import os, struct, urllib.request, zlib
URL = "https://data.bris.ac.uk/datasets/s5hqmjcdj8yo2ibzi9b4ew3sn/N30E120-N40E130_FABDEM_V1-2.zip"
OUT = "../dl/dem"; os.makedirs(OUT, exist_ok=True)
UA = {"User-Agent": "MarathonProfil/1.0 (private, non-commercial)"}
def teil(a, b):
    req = urllib.request.Request(URL, headers={**UA, "Range": f"bytes={a}-{b}"})
    return urllib.request.urlopen(req, timeout=300).read()
req = urllib.request.Request(URL, method="HEAD", headers=UA); groesse = int(urllib.request.urlopen(req, timeout=60).headers["Content-Length"])
ende = teil(groesse - 65536, groesse - 1)
i = ende.rfind(b"PK\x05\x06"); assert i >= 0, "kein Zip-Ende"
_, _, _, _, anzahl, cd_groesse, cd_start, _ = struct.unpack("<IHHHHIIH", ende[i:i + 22])
if cd_start == 0xFFFFFFFF or anzahl == 0xFFFF:          # Zip64
    j = ende.rfind(b"PK\x06\x07"); off64 = struct.unpack("<Q", ende[j + 8:j + 16])[0]
    z64 = teil(off64, off64 + 55); anzahl, cd_groesse, cd_start = struct.unpack("<QQQ", z64[32:56])
cd = teil(cd_start, cd_start + cd_groesse - 1)
eintraege, p = {}, 0
while p < len(cd) and cd[p:p + 4] == b"PK\x01\x02":
    meth, = struct.unpack("<H", cd[p + 10:p + 12]); csize, usize = struct.unpack("<II", cd[p + 20:p + 28])
    nl, el, kl = struct.unpack("<HHH", cd[p + 28:p + 34]); loff, = struct.unpack("<I", cd[p + 42:p + 46])
    name = cd[p + 46:p + 46 + nl].decode(); extra = cd[p + 46 + nl:p + 46 + nl + el]
    q = 0
    while q < len(extra):                                  # Zip64-Erweiterung: echte Größen und Lage
        hid, hl = struct.unpack("<HH", extra[q:q + 4]); werte = extra[q + 4:q + 4 + hl]
        if hid == 1:
            vals = list(struct.unpack("<" + "Q" * (hl // 8), werte[:hl // 8 * 8])); k = 0
            if usize == 0xFFFFFFFF: usize = vals[k]; k += 1
            if csize == 0xFFFFFFFF: csize = vals[k]; k += 1
            if loff == 0xFFFFFFFF: loff = vals[k]; k += 1
        q += 4 + hl
    eintraege[name] = (meth, csize, usize, loff); p += 46 + nl + el + kl
print(len(eintraege), "Einträge, z. B.", list(eintraege)[:3])
for kachel in ("N31E121",):
    name = [n for n in eintraege if kachel in n and n.endswith(".tif")][0]
    meth, csize, usize, loff = eintraege[name]
    kopf = teil(loff, loff + 29); nl, el = struct.unpack("<HH", kopf[26:30])
    roh = teil(loff + 30 + nl + el, loff + 30 + nl + el + csize - 1)
    daten = roh if meth == 0 else zlib.decompress(roh, -15)
    assert len(daten) == usize, (len(daten), usize)
    open(f"{OUT}/fabdem_{kachel}.tif", "wb").write(daten)
    print(name, meth, csize, usize, "->", f"{OUT}/fabdem_{kachel}.tif")
# Vergleichsmodelle (öffentlich auf AWS, ohne Anmeldung)
for url, ziel in (("https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_N31_00_E121_00_DEM/Copernicus_DSM_COG_10_N31_00_E121_00_DEM.tif",
                   f"{OUT}/cop30_N31_E121.tif"),
                  ("https://s3.amazonaws.com/elevation-tiles-prod/skadi/N31/N31E121.hgt.gz", f"{OUT}/srtm_N31E121.hgt.gz")):
    if not os.path.exists(ziel):
        open(ziel, "wb").write(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=600).read())
    print(url, "->", ziel, os.path.getsize(ziel))
