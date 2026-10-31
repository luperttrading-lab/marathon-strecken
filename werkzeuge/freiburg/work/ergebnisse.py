# Marathon-Finisher aus der offiziellen Ergebnisliste zählen (Race Result, eingebunden auf mein-freiburgmarathon.de/ergebnisse/:
# RRPublish 351479 = 2026, 298890 = 2025, 251383 = 2024). Liste „02_Ergebnisse|Einzel_Gesamtergebnisliste“ des Wettbewerbs 1
# (Marathon). Die Antwort wird nur im Speicher ausgewertet: gezählt werden Einträge mit Platz und Zielzeit, dazu die übrigen nach
# Status. Keine Namen werden gespeichert; ../dl/ergebnisse/zahlen.json enthält nur Zählwerte.
import json, re, sys, urllib.request, urllib.parse, time
UA = {"User-Agent": "Mozilla/5.0 MarathonProfil/1.0 (private, non-commercial)"}
def hole(url):
    for att in range(4):
        try: return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
        except Exception as e: print("  Fehler", e); time.sleep(5 + 5 * att)
def zaehle(ev, contest="1", liste="02_Ergebnisse|Einzel_Gesamtergebnisliste"):
    cfg = hole(f"https://my.raceresult.com/{ev}/RRPublish/data/config?page=results&noVisitor=1&lang=de")
    q = urllib.parse.urlencode({"key": cfg["key"], "listname": liste, "page": "results", "contest": contest, "r": "all", "l": "0"})
    d = hole(f"https://my.raceresult.com/{ev}/RRPublish/data/list?{q}")
    kopf = [f.get("Expression", "") + "|" + f.get("Label", "") for f in d.get("list", {}).get("Fields", [])]
    def zeilen(o):
        if isinstance(o, list):
            if o and all(not isinstance(x, (list, dict)) for x in o): yield o
            else:
                for x in o: yield from zeilen(x)
        elif isinstance(o, dict):
            for v in o.values(): yield from zeilen(v)
    rows = list(zeilen(d.get("data", {})))
    zeit = re.compile(r"^\d{1,2}:\d{2}:\d{2}")
    platz = re.compile(r"^\d+\.?$")
    mit = sum(1 for r in rows if any(platz.match(str(x).strip()) for x in r[1:3]) and any(zeit.match(str(x).strip()) for x in r))
    status = {}
    for r in rows:
        if any(zeit.match(str(x).strip()) for x in r): continue
        s = next((str(x).strip() for x in r if str(x).strip() in ("DNF", "DSQ", "DNS", "aufgegeben", "disqualifiziert", "nicht gestartet", "n.a.", "a.k.")), "sonstige")
        status[s] = status.get(s, 0) + 1
    return {"ereignis": ev, "name": cfg.get("eventname"), "wettbewerb": json.loads(json.dumps(cfg["contests"])).get(contest) if isinstance(cfg["contests"], dict) else contest,
            "liste": liste, "spalten": kopf, "eintraege": len(rows), "mit_platz_und_zeit": mit, "ohne_zeit": status}
if __name__ == "__main__":
    out = {}
    for jahr, ev in (("2026", 351479), ("2025", 298890), ("2024", 251383)):
        out[jahr] = zaehle(ev); print(jahr, json.dumps(out[jahr], ensure_ascii=False)); time.sleep(1)
    json.dump(out, open("../dl/ergebnisse/zahlen.json", "w"), ensure_ascii=False, indent=1)
