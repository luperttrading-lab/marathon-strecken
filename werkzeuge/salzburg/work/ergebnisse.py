# Marathon-Finisher aus der offiziellen Ergebnisliste zählen (Datasport, Zeitnehmung des Veranstalters; die Seite
# „Ergebnisse, Fotos und Video-Highlights 2026“ auf salzburg-marathon.at verlinkt „Alle Ergebnisse“ auf
# datasport.de/anmeldeservice/salzburgmarathon2026/ergebnisse, die dort Race Result einbindet: 385271 = 2026, 325880 = 2025,
# 276167 = 2024). Wettbewerb 1 „PUMA Salzburg Marathon“, Liste „10 Ergebnislisten|00 Ergebnisliste MW“; dazu die Staffeln
# (Wettbewerb 4). Die Antwort wird nur im Speicher ausgewertet: gezählt werden Zeilen mit Platz und Zielzeit, die übrigen nach
# Status. Keine Namen werden gespeichert; ../dl/erg/zahlen.json enthält nur Zählwerte. Muster: werkzeuge/freiburg/work/ergebnisse.py
import json, re, time, urllib.request, urllib.parse
UA = {"User-Agent": "Mozilla/5.0 MarathonProfil/1.0 (private, non-commercial)"}
def hole(url):
    for att in range(4):
        try: return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read())
        except Exception as e: print("  Fehler", e); time.sleep(5 + 5 * att)
def zeilen(o):
    if isinstance(o, list):
        if o and all(not isinstance(x, (list, dict)) for x in o): yield o
        else:
            for x in o: yield from zeilen(x)
    elif isinstance(o, dict):
        for v in o.values(): yield from zeilen(v)
def zaehle(ev, contest):
    cfg = hole(f"https://my.raceresult.com/{ev}/RRPublish/data/config?page=results&noVisitor=1&lang=de")
    listen = [l["Name"] for l in cfg["lists"] if l["Contest"] == contest and not l["Mode"] and "AgeGrade" not in l["Name"]]
    liste = listen[0]
    q = urllib.parse.urlencode({"key": cfg["key"], "listname": liste, "page": "results", "contest": contest, "r": "all", "l": "0"})
    d = hole(f"https://my.raceresult.com/{ev}/RRPublish/data/list?{q}")
    kopf = [f.get("Expression", "") + "|" + f.get("Label", "") for f in d.get("list", {}).get("Fields", [])]
    rows = list(zeilen(d.get("data", {})))
    zeit = re.compile(r"^\d{1,2}:\d{2}:\d{2}"); platz = re.compile(r"^\d+\.?$")
    mit = sum(1 for r in rows if any(platz.match(str(x).strip()) for x in r[1:3]) and any(zeit.match(str(x).strip()) for x in r))
    status = {}
    for r in rows:
        if any(zeit.match(str(x).strip()) for x in r): continue
        s = next((str(x).strip() for x in r if str(x).strip() in ("DNF", "DSQ", "DNS", "aufgegeben", "disqualifiziert", "nicht gestartet", "n.a.", "a.k.")), "sonstige")
        status[s] = status.get(s, 0) + 1
    # Gruppenköpfe (Männer/Frauen …) liefert Race Result als Schlüssel der Daten: deren Anzahl mitschreiben
    gruppen = {k: sum(1 for _ in zeilen(v)) for k, v in d.get("data", {}).items()} if isinstance(d.get("data"), dict) else {}
    return {"ereignis": ev, "name": cfg.get("eventname"), "wettbewerb": cfg["contests"].get(contest), "liste": liste, "spalten": kopf,
            "gruppen": gruppen, "eintraege": len(rows), "mit_platz_und_zeit": mit, "ohne_zeit": status}
if __name__ == "__main__":
    out = {}
    for jahr, ev in (("2026", 385271), ("2025", 325880), ("2024", 276167)):
        for c in ("1", "4"):
            try: out[f"{jahr}-{c}"] = zaehle(ev, c)
            except Exception as e: out[f"{jahr}-{c}"] = {"fehler": str(e)}
            print(jahr, c, json.dumps(out[f"{jahr}-{c}"], ensure_ascii=False)); time.sleep(1)
    json.dump(out, open("../dl/erg/zahlen.json", "w"), ensure_ascii=False, indent=1)
