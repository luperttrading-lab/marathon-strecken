# Lädt Ziel- und Abschnittszeiten aus den öffentlichen Datasport-Ranglisten (keine Anmeldung) nach /tmp.
# Übernimmt je Zeile nur Geschlecht (aus der Liste), Zielzeit und Abschnittszeiten in Sekunden: keine Namen, keine
# Startnummer, kein Jahrgang, kein Verein. Die Seite wird nur im Speicher gelesen. 4 s Pause zwischen den Abrufen.
#   python3 laden.py /tmp/berg/roh        → /tmp/berg/roh/<anlass>__<liste>.csv
import sys, re, json, time, csv, os, urllib.request

ZIEL = sys.argv[1] if len(sys.argv) > 1 else "/tmp/berg/roh"
# Anlass, Liste, Geschlecht, Spalten der Abschnitte (in Reihenfolge, Summe = Zielzeit)
LISTEN = []
for j in (2024, 2025, 2026):
    for sl, g in (("frauen", "F"), ("maenner", "M")):
        LISTEN.append((f"jungfrau-marathon-{j}", sl, g, [f"split.{i}" for i in range(1, 10)]))
for j in (2025, 2026):
    for sl, g in (("marathon-frauen", "F"), ("marathon-maenner", "M")):
        LISTEN.append((f"gornergrat-zermatt-marathon-{j}", sl, g, ["split.1", "split.2", "split.3", "split.4"]))
    for sl, g in (("halbmarathon-frauen", "F"), ("halbmarathon-maenner", "M")):
        LISTEN.append((f"gornergrat-zermatt-marathon-{j}", sl, g, ["split.1", "split.2", "split.3"]))
for sl, g in (("marathon-frauen", "F"), ("marathon-maenner", "M")):
    LISTEN.append(("lgt-alpin-marathon-2026", sl, g, ["split.1", "split.2", "split.3"]))

UA = "Mozilla/5.0 (Eichung Steigungsprofile, privat; langsam, 4 s Pause)"

def hole(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for versuch in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r: s = r.read().decode("utf-8")
            m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', s, re.S)
            return json.loads(m.group(1))["props"]["pageProps"]["response"]
        except Exception as e:
            print("  Fehler", e, "– warte 30 s", file=sys.stderr); time.sleep(30)
    raise SystemExit("abgebrochen: " + url)

def sek(t):
    """'3:20:56,3' / '11:20,2' → Sekunden; sonst None"""
    if not t: return None
    t = str(t).strip().replace(",", ".")
    if not re.fullmatch(r"\d+(:\d\d){1,2}(\.\d+)?", t): return None
    p = t.split(":"); v = 0.0
    for x in p: v = v * 60 + float(x)
    return v

def text(row, col):
    v = row.get(col)
    return v.get("text") if isinstance(v, dict) else v

os.makedirs(ZIEL, exist_ok=True)
for anlass, liste, g, spl in LISTEN:
    datei = f"{ZIEL}/{anlass}__{liste}.csv"
    if os.path.exists(datei): print("vorhanden", datei); continue
    zeilen, seite, n_seiten, n_alle = [], 1, 1, 0
    while seite <= n_seiten:
        r = hole(f"https://results.datasport.com/de/anlass/{anlass}/ranking/list/{liste}?page={seite}&pageSize=200")
        t = r["table"]; n_seiten = -(-t["totalrowcount"] // 200) if seite == 1 else n_seiten
        if seite == 1:
            titel = {c["col"]: c.get("title") for c in t["columns"]}
            print(anlass, liste, t["totalrowcount"], "Zeilen,", n_seiten, "Seiten;", [titel.get(c) for c in spl])
        for row in t["rows"]:
            if "separator" in row: continue   # Zwischenzeile „Nicht im Ziel“ u. ä.
            n_alle += 1
            z = sek(text(row, "time.main")); s = [sek(text(row, c)) for c in spl]
            zeilen.append([g, z] + s)   # nur Zeiten; Name, Startnummer, Verein, Jahrgang werden nicht gelesen
        seite += 1; time.sleep(4)
    with open(datei, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["g", "ziel"] + [f"s{i + 1}" for i in range(len(spl))]); w.writerows(zeilen)
    assert n_alle == t["totalrowcount"], (n_alle, t["totalrowcount"])
    print("  ", n_alle, "Zeilen →", datei)
