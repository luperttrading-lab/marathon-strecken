# Sonnys „DTM Germany 20m v3b“ (CC BY 4.0, sonny.4lima.de): 20-m-Raster aus den amtlichen Laser-Geländemodellen,
# für Thüringen DGM1 2014–2019 bzw. DGM2 2010–2013 (TLBG/GDI-Th). Eine GeoTIFF für ganz Deutschland (1,5 GB, Google
# Drive), Deflate, je Zeile ein Streifen. dgm.py lädt per Range-Abruf nur die Zeilen um die Strecke (../dl/dtm20_streifen.*).
# UTM32 (EPSG:32632), PixelIsPoint: Mittelpunkt von Pixel (r, c) bei (x0 + 20 c, y0 − 20 r). Ohne Daten: −32767.
import json, zlib, numpy as np
def lade(pfad="../dl/dtm20_streifen"):
    m = json.load(open(pfad + ".json")); raw = open(pfad + ".bin", "rb").read(); o0 = m["off"][0]
    A = np.stack([np.frombuffer(zlib.decompress(raw[o - o0:o - o0 + c]), "<f4") for o, c in zip(m["off"], m["cnt"])]).astype(float)
    A[A < -1000] = np.nan
    return A, m
def hoehe(A, m, E, N):
    c = (np.asarray(E) - m["x0"]) / 20.0; r = (m["y0"] - np.asarray(N)) / 20.0 - m["r0"]
    c0 = np.floor(c).astype(int); r0 = np.floor(r).astype(int); fc, fr = c - c0, r - r0
    return (A[r0, c0] * (1 - fc) * (1 - fr) + A[r0, c0 + 1] * fc * (1 - fr) + A[r0 + 1, c0] * (1 - fc) * fr + A[r0 + 1, c0 + 1] * fc * fr)
